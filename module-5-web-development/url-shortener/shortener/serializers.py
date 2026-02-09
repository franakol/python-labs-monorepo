"""
DRF Serializers for URL Shortener
"""

from rest_framework import serializers
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError as DjangoValidationError


class URLShortenSerializer(serializers.Serializer):
    """Serializer for creating short URLs."""
    
    original_url = serializers.URLField(
        max_length=2048,
        required=True,
        help_text="The full URL you want to shorten (e.g., https://example.com/very/long/path)"
    )
    custom_code = serializers.CharField(
        min_length=6, 
        max_length=6, 
        required=False, 
        write_only=True,
        help_text="Optional custom 6-character code (alphanumeric)"
    )
    
    def validate_original_url(self, value):
        """Validate the URL format."""
        validator = URLValidator()
        try:
            validator(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Invalid URL format")
        
        # Check for blacklisted domains (optional)
        blacklisted_domains = ['localhost', '127.0.0.1']
        for domain in blacklisted_domains:
            if domain in value:
                raise serializers.ValidationError(
                    f"URLs from {domain} are not allowed"
                )
        
        return value
    
    def validate_custom_code(self, value):
        """Validate custom short code."""
        if value:
            if len(value) < 6: # Updated validation to match new min_length
                raise serializers.ValidationError(
                    "Custom code must be at least 6 characters"
                )
            if not value.isalnum():
                raise serializers.ValidationError(
                    "Custom code must contain only letters and numbers"
                )
        return value


class URLResponseSerializer(serializers.Serializer):
    """Response after creating a short URL."""
    
    short_code = serializers.CharField(
        min_length=6, 
        max_length=6, 
        read_only=True,
        help_text="The generated 6-character short code"
    )
    original_url = serializers.URLField(help_text="The original long URL to be shortened")
    short_url = serializers.SerializerMethodField(help_text="The full shortened URL")
    created_at = serializers.DateTimeField(read_only=True, help_text="When the URL was shortened")
    clicks = serializers.IntegerField(read_only=True, help_text="Number of times the short URL has been accessed")
    created = serializers.BooleanField(
        read_only=True,
        help_text="True if newly created, False if URL was already shortened before"
    )
    
    def get_short_url(self, obj):
        """Generate the full short URL."""
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f"/{obj['short_code']}")
        return f"/{obj['short_code']}"


class URLStatsSerializer(serializers.Serializer):
    """Statistics for a shortened URL."""
    
    short_code = serializers.CharField(
        read_only=True,
        help_text="The short code identifier"
    )
    original_url = serializers.URLField(
        read_only=True,
        help_text="The original long URL"
    )
    clicks = serializers.IntegerField(
        read_only=True,
        help_text="Total number of times this short URL has been accessed"
    )
    short_url = serializers.SerializerMethodField(
        help_text="The complete short URL"
    )
    
    def get_short_url(self, obj):
        """Generate the full short URL."""
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f"/{obj['short_code']}")
        return f"/{obj['short_code']}"
