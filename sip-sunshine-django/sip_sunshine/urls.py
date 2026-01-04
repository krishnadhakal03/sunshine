from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView

def favicon_view(request):
    """Serve favicon from static files"""
    from django.http import FileResponse
    import os
    favicon_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'favicon.svg')
    return FileResponse(open(favicon_path, 'rb'), content_type='image/svg+xml')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', favicon_view),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('', include('restaurant.urls')),
    prefix_default_language=False
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve static files from the 'static' folder directly
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
