"""
Development settings
"""

from .base import *

DEBUG = True

# Allow all hosts in development
ALLOWED_HOSTS = ['*']

# CORS allow all in development
CORS_ALLOW_ALL_ORIGINS = True
