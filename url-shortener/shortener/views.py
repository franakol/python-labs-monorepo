"""
REST API Views for URL Shortener
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .services import url_shortener_service
from .serializers import (
    URLShortenSerializer,
    URLResponseSerializer,
    URLStatsSerializer
)


class RootView(APIView):
    """Root API view with welcome message and links."""
    
    @extend_schema(
        summary="API Root - Welcome Page",
        description="""Returns a welcome message with links to all available API endpoints.
        
        This is the landing page for the URL Shortener API. Use the returned links
        to navigate to the Swagger documentation, create short URLs, or access other endpoints.
        """,
        responses={200: {"type": "object"}},
        tags=['General']
    )
    def get(self, request):
        """Root endpoint with API info."""
        base_url = request.build_absolute_uri('/')
        return Response({
            "message": "Welcome to URL Shortener API",
            "version": "1.0.0",
            "endpoints": {
                "health": f"{base_url}health/",
                "shorten": f"{base_url}api/shorten/",
                "stats": f"{base_url}api/stats/<short_code>/",
                "documentation": {
                    "swagger": f"{base_url}api/docs/",
                    "redoc": f"{base_url}api/redoc/",
                    "schema": f"{base_url}api/schema/"
                }
            }
        }, status=status.HTTP_200_OK)


class HealthCheckView(APIView):
    """Health check endpoint."""
    
    @extend_schema(
        summary="Health Check",
        description="""Verify that the URL Shortener service is up and running.
        
        Returns a simple health status. Use this endpoint for:
        - Load balancer health checks
        - Monitoring and uptime tracking
        - Docker container health verification
        
        **Example Response:**
        ```json
        {"status": "healthy"}
        ```
        """,
        responses={200: {"type": "object", "properties": {"status": {"type": "string"}}}},
        tags=['General']
    )
    def get(self, request):
        """Health check endpoint."""
        return Response({"status": "healthy"}, status=status.HTTP_200_OK)


class ShortenURLView(APIView):
    """Create a shortened URL."""
    
    @extend_schema(
        summary="Create Short URL",
        description="""Generate a shortened URL from a long URL.
        
        **How it works:**
        1. Send a POST request with your long URL in the `original_url` field
        2. The API generates a random 6-character short code (or uses your custom code)
        3. Returns the short code and complete short URL you can share
        
        **Smart Deduplication:**
        If you shorten the same URL twice, you'll get the same short code back.
        The `created` field tells you if it's a new short URL or an existing one.
        
        **Example Request:**
        ```json
        {
          "original_url": "https://www.example.com/very/long/path/to/page"
        }
        ```
        
        **Example Response:**
        ```json
        {
          "short_code": "aB3xYz",
          "original_url": "https://www.example.com/very/long/path/to/page",
          "short_url": "http://localhost:8000/aB3xYz",
          "created": true
        }
        ```
        """,
        request=URLShortenSerializer,
        responses={201: URLResponseSerializer, 400: {"type": "object"}},
        tags=['URL Shortening']
    )
    def post(self, request):
        """Create a new short URL."""
        serializer = URLShortenSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        original_url = serializer.validated_data['original_url']
        custom_code = serializer.validated_data.get('custom_code')
        
        try:
            result = url_shortener_service.shorten_url(
                original_url,
                custom_code=custom_code
            )
            
            response_serializer = URLResponseSerializer(
                result,
                context={'request': request}
            )
            
            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED if result['created'] else status.HTTP_200_OK
            )
            
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class RedirectView(APIView):
    """Redirect to original URL."""
    
    @extend_schema(
        summary="Redirect to Original URL",
        description="""Automatically redirect to the original long URL.
        
        **How to use:**
        1. Visit the short URL in your browser: `http://localhost:8000/<short_code>`
        2. You'll be instantly redirected (HTTP 302) to the original URL
        3. Each visit increments the click counter
        
        **Example:**
        - Short URL: `http://localhost:8000/aB3xYz`
        - Redirects to: `https://www.example.com/very/long/path/to/page`
        
        **Note:** This endpoint doesn't return JSON - it performs an HTTP redirect.
        Perfect for sharing links in emails, social media, or QR codes!
        """,
        parameters=[
            OpenApiParameter(
                name='short_code',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description='The 6-character short code (e.g., "aB3xYz")'
            )
        ],
        responses={
            302: {"description": "Successfully redirected to original URL"},
            404: {"type": "object", "properties": {"error": {"type": "string"}}}
        },
        tags=['URL Shortening']
    )
    def get(self, request, short_code):
        """Redirect to the original URL."""
        original_url = url_shortener_service.get_original_url(short_code)
        
        if not original_url:
            return Response(
                {'error': 'Short code not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Increment click count
        url_shortener_service.increment_clicks(short_code)
        
        # Redirect to original URL
        return HttpResponseRedirect(original_url)


class URLStatsView(APIView):
    """Get URL statistics."""
    
    @extend_schema(
        summary="Get URL Statistics",
        description="""Retrieve analytics and statistics for a shortened URL.
        
        **What you get:**
        - Original long URL
        - Short code
        - Complete short URL
        - Total click count (number of times the short URL has been accessed)
        
        **Example Response:**
        ```json
        {
          "short_code": "aB3xYz",
          "original_url": "https://www.example.com/page",
          "short_url": "http://localhost:8000/aB3xYz",
          "clicks": 42
        }
        ```
        
        **Use cases:**
        - Track link popularity
        - Measure campaign effectiveness
        - Monitor traffic sources
        """,
        parameters=[
            OpenApiParameter(
                name='short_code',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description='The short code to retrieve statistics for'
            )
        ],
        responses={200: URLStatsSerializer, 404: {"type": "object"}},
        tags=['Analytics']
    )
    def get(self, request, short_code):
        """Get statistics for a short code."""
        stats = url_shortener_service.get_stats(short_code)
        
        if not stats:
            return Response(
                {'error': 'Short code not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = URLStatsSerializer(stats, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
