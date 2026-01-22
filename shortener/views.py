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
        summary="API Root",
        description="Get welcome message and API endpoints",
        responses={200: {"type": "object"}}
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
        description="Check if the service is running",
        responses={200: {"type": "object", "properties": {"status": {"type": "string"}}}}
    )
    def get(self, request):
        """Health check endpoint."""
        return Response({"status": "healthy"}, status=status.HTTP_200_OK)


class ShortenURLView(APIView):
    """Create a shortened URL."""
    
    @extend_schema(
        summary="Create Short URL",
        description="Create a shortened URL for a given long URL",
        request=URLShortenSerializer,
        responses={201: URLResponseSerializer, 400: {"type": "object"}}
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
        description="Redirect to the original URL using the short code",
        parameters=[
            OpenApiParameter(
                name='short_code',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description='The short code to redirect'
            )
        ],
        responses={
            302: {"description": "Redirect to original URL"},
            404: {"type": "object", "properties": {"error": {"type": "string"}}}
        }
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
        description="Get statistics for a shortened URL including click count",
        parameters=[
            OpenApiParameter(
                name='short_code',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description='The short code to get stats for'
            )
        ],
        responses={200: URLStatsSerializer, 404: {"type": "object"}}
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
