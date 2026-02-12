"""
Django admin configuration for URL Shortener
"""

from django.contrib import admin
from .models import URLMapping


@admin.register(URLMapping)
class URLMappingAdmin(admin.ModelAdmin):
    """Admin interface for URL mappings."""
    
    list_display = ['short_code', 'original_url_preview', 'clicks', 'created_at']
    list_filter = ['created_at']
    search_fields = ['short_code', 'original_url']
    readonly_fields = ['created_at', 'clicks']
    ordering = ['-created_at']
    
    def original_url_preview(self, obj):
        """Show truncated URL in list view."""
        if len(obj.original_url) > 50:
            return f"{obj.original_url[:50]}..."
        return obj.original_url
    
    original_url_preview.short_description = 'Original URL'
