"""
CRMsystem URL Configuration
"""

import logging

try:
    from django.contrib import admin
    from django.urls import path, include
    from django.conf import settings
    from django.conf.urls.static import static
except ImportError as e:
    raise ImportError(f"Failed to import required modules in project urls.py: {e}")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

try:
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('accounts.urls')),
    ]

    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

except Exception as e:
    logger.exception(f"Error while setting URL patterns in CRMsystem/urls.py: {e}")
    urlpatterns = []
