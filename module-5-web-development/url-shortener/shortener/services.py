"""
URL Shortener Service

Provides core business logic for URL shortening using Redis as storage backend.
"""

import redis
import string
import random
from typing import Optional, Dict
from decouple import config


class URLShortenerService:
    """Service for managing URL shortening operations with Redis."""
    
    # Characters for base62 encoding
    BASE62_CHARS = string.ascii_letters + string.digits
    SHORT_CODE_LENGTH = 6
    
    def __init__(self):
        """Initialize Redis connection."""
        redis_url = config('REDIS_URL', default='redis://localhost:6379/0')
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        
        # Key prefixes for organization
        self.URL_PREFIX = "url:"          # url:<short_code> -> original_url
        self.CLICKS_PREFIX = "clicks:"    # clicks:<short_code> -> click_count
        self.REVERSE_PREFIX = "reverse:"  # reverse:<url_hash> -> short_code
    
    def generate_short_code(self) -> str:
        """
        Generate a random short code using base62 encoding.
        
        Returns:
            str: A 6-character short code
        """
        while True:
            short_code = ''.join(
                random.choice(self.BASE62_CHARS) 
                for _ in range(self.SHORT_CODE_LENGTH)
            )
            
            # Check for collisions
            if not self.redis_client.exists(f"{self.URL_PREFIX}{short_code}"):
                return short_code
    
    def shorten_url(self, original_url: str, custom_code: Optional[str] = None) -> Dict[str, str]:
        """
        Create a short URL for the given original URL.
        
        Args:
            original_url: The long URL to shorten
            custom_code: Optional custom short code (if available)
            
        Returns:
            dict: Contains 'short_code' and 'original_url'
            
        Raises:
            ValueError: If custom code already exists
        """
        # Check if URL already has a short code
        url_hash = hash(original_url)
        existing_code = self.redis_client.get(f"{self.REVERSE_PREFIX}{url_hash}")
        
        if existing_code:
            return {
                'short_code': existing_code,
                'original_url': original_url,
                'created': False
            }
        
        # Use custom code or generate new one
        if custom_code:
            if self.redis_client.exists(f"{self.URL_PREFIX}{custom_code}"):
                raise ValueError(f"Short code '{custom_code}' already exists")
            short_code = custom_code
        else:
            short_code = self.generate_short_code()
        
        # Store in Redis
        url_key = f"{self.URL_PREFIX}{short_code}"
        reverse_key = f"{self.REVERSE_PREFIX}{url_hash}"
        clicks_key = f"{self.CLICKS_PREFIX}{short_code}"
        
        # Set URL mapping with 1 year expiration (optional)
        self.redis_client.setex(url_key, 31536000, original_url)  # 1 year TTL
        self.redis_client.setex(reverse_key, 31536000, short_code)
        self.redis_client.set(clicks_key, 0)
        
        return {
            'short_code': short_code,
            'original_url': original_url,
            'created': True
        }
    
    def get_original_url(self, short_code: str) -> Optional[str]:
        """
        Retrieve the original URL for a given short code.
        
        Args:
            short_code: The short code to lookup
            
        Returns:
            str: Original URL if found, None otherwise
        """
        url_key = f"{self.URL_PREFIX}{short_code}"
        return self.redis_client.get(url_key)
    
    def increment_clicks(self, short_code: str) -> int:
        """
        Increment the click count for a short code.
        
        Args:
            short_code: The short code to increment
            
        Returns:
            int: New click count
        """
        clicks_key = f"{self.CLICKS_PREFIX}{short_code}"
        return self.redis_client.incr(clicks_key)
    
    def get_stats(self, short_code: str) -> Optional[Dict]:
        """
        Get statistics for a short code.
        
        Args:
            short_code: The short code to get stats for
            
        Returns:
            dict: Stats including original_url and clicks, or None if not found
        """
        original_url = self.get_original_url(short_code)
        
        if not original_url:
            return None
        
        clicks_key = f"{self.CLICKS_PREFIX}{short_code}"
        clicks = int(self.redis_client.get(clicks_key) or 0)
        
        return {
            'short_code': short_code,
            'original_url': original_url,
            'clicks': clicks
        }
    
    def delete_url(self, short_code: str) -> bool:
        """
        Delete a short code and its associated data.
        
        Args:
            short_code: The short code to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        url_key = f"{self.URL_PREFIX}{short_code}"
        original_url = self.redis_client.get(url_key)
        
        if not original_url:
            return False
        
        # Delete all associated keys
        url_hash = hash(original_url)
        reverse_key = f"{self.REVERSE_PREFIX}{url_hash}"
        clicks_key = f"{self.CLICKS_PREFIX}{short_code}"
        
        self.redis_client.delete(url_key, reverse_key, clicks_key)
        return True


# Singleton instance
url_shortener_service = URLShortenerService()
