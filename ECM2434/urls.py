"""
Root URL configuration for ECM2434 project.

This module contains the root URL configuration for the entire project,
connecting all app-specific URL patterns to their respective apps.

URL Patterns:
    - admin/: Django admin interface
    - /: Main application entry point (Accounts app)
    - accounts/: User authentication and profile management
    - ecoworld/: EcoWorld game functionality
    - qrcode/: QR code scanning and processing
    - garden/: Virtual garden management
    - guides/: Sustainability guides and resources
    - leaderboards/: User rankings and achievements
    - glass-disposal/: Glass recycling information
    - game/: Sustainability game features
    - forum/: Community discussion board

For more information on URL configuration, see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/

Author:
    Lewis Farley (lf507@exeter.ac.uk)
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("Accounts.urls")),
    path("accounts/", include("Accounts.urls")),
    path("ecoworld/", include("EcoWorld.urls")),
    path("qrcode/", include("qrCodes.urls")),
    path("garden/", include("Garden.urls")),
    path("guides/", include("guides.urls")),
    path("leaderboards/", include("leaderboards.urls")),
    path("glass-disposal/", include("glassDisposal.urls")),
    path('game/', include('SustainabilityGame.urls')),
    path('forum/', include('forum.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
print(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
print(urlpatterns[1])
