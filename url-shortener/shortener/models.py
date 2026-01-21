"""
Django models for URL Shortener

Since we're using Redis as the primary storage, these models are minimal
and mainly for Django admin and potential future database integration.
"""

from django.db import models


class URLMapping(models.Model):
    """
    Optional database model for URL mappings.
    Primary storage is Redis, but this can serve as backup or for admin.
    """
    short_code = models.CharField(max_length=10, unique=True, db_index=True)
    original_url = models.URLField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'URL Mapping'
        verbose_name_plural = 'URL Mappings'
    
    def __str__(self):
        return f"{self.short_code} -> {self.original_url[:50]}"
