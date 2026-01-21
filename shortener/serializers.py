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
        help_text="The long URL to shorten"
    )
    custom_code = serializers.CharField(
        max_length=10,
        required=False,
        allow_blank=True,
        help_text="Optional custom short code"
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
            if len(value) < 3:
                raise serializers.ValidationError(
                    "Custom code must be at least 3 characters"
                )
            if not value.isalnum():
                raise serializers.ValidationError(
                    "Custom code must contain only letters and numbers"
                )
        return value


class URLResponseSerializer(serializers.Serializer):
    """Serializer for short URL response."""
    
    short_code = serializers.CharField(read_only=True)
    original_url = serializers.URLField(read_only=True)
    short_url = serializers.SerializerMethodField()
    created = serializers.BooleanField(read_only=True)
    
    def get_short_url(self, obj):
        """Generate the full short URL."""
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f"/{obj['short_code']}")
        return f"/{obj['short_code']}"


class URLStatsSerializer(serializers.Serializer):
    """Serializer for URL statistics."""
    
    short_code = serializers.CharField(read_only=True)
    original_url = serializers.URLField(read_only=True)
    clicks = serializers.IntegerField(read_only=True)
    short_url = serializers.SerializerMethodField()
    
    def get_short_url(self, obj):
        """Generate the full short URL."""
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f"/{obj['short_code']}")
        return f"/{obj['short_code']}"
