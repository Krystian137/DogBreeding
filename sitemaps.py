# sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post
from pets.models import Dog, Litter


class StaticSitemap(Sitemap):
    """Strony statyczne"""
    priority = 1.0
    changefreq = 'monthly'

    def items(self):
        return [
            'blog:main',
            'rezerwacja:reservation-form',
            'zwierzaki:DogList',
            'zwierzaki:LitterList',
        ]

    def location(self, item):
        return reverse(item)


class PostSitemap(Sitemap):
    """Wszystkie posty z bloga"""
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.created_at  # ← POPRAWIONE z created_date

    def location(self, obj):
        """Zwraca URL dla posta"""
        return reverse('blog:post-detail', kwargs={'slug': obj.slug})


class DogSitemap(Sitemap):
    """Wszystkie psy"""
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Dog.objects.all()

    def lastmod(self, obj):
        return obj.birth_date  # ← Używam birth_date (nie ma created_at)

    def location(self, obj):
        """Zwraca URL dla psa"""
        return reverse('zwierzaki:DogProfile', kwargs={'slug': obj.slug})


class LitterSitemap(Sitemap):
    """Wszystkie mioty"""
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Litter.objects.all()

    def lastmod(self, obj):
        return obj.birth_date  # ← To było OK

    def location(self, obj):
        """Zwraca URL dla miotu"""
        return reverse('zwierzaki:LitterDetails', kwargs={'slug': obj.slug})