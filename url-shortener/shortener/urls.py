"""
URL routing for shortener app
"""

from django.urls import path
from .views import ShortenURLView, RedirectView, URLStatsView, HealthCheckView

app_name = 'shortener'

urlpatterns = [
    # API endpoints
    path('api/shorten/', ShortenURLView.as_view(), name='shorten'),
    path('api/stats/<str:short_code>/', URLStatsView.as_view(), name='stats'),
    path('health/', HealthCheckView.as_view(), name='health'),
    
    # Redirect endpoint (must be last to avoid conflicts)
    path('<str:short_code>/', RedirectView.as_view(), name='redirect'),
]
