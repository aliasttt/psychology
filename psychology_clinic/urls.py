"""
URL configuration for psychology_clinic project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse

from blog.sitemaps import PostSitemap
from services.sitemaps import ServiceSitemap

sitemaps = {
    'posts': PostSitemap,
    'services': ServiceSitemap,
}

def robots_txt(request):
    """Serve robots.txt file"""
    content = """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /static/
Disallow: /media/

Sitemap: https://psychotherapy-clinic.com/sitemap.xml
"""
    return HttpResponse(content, content_type='text/plain')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('blog/', include('blog.urls')),
    path('services/', include('services.urls')),
    path('appointments/', include('appointments.urls')),
    path('contact/', include('contact.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
