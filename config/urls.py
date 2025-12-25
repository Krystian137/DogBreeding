from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from sitemaps import StaticSitemap, PostSitemap, DogSitemap, LitterSitemap
from django.views.generic import TemplateView

sitemaps = {
    'static': StaticSitemap,
    'posts': PostSitemap,
    'dogs': DogSitemap,
    'litters': LitterSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('blog.urls', 'blog'), namespace='blog')),
    path('rezerwacja/', include(('reservation.urls', 'reservation'), namespace='rezerwacja')),
    path('psy/', include(('pets.urls', 'pets'), namespace='zwierzaki')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(
            template_name='robots.txt',
            content_type='text/plain'
        )),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)