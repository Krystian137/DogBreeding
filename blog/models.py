from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tytuł")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Adres URL (Slug)")
    content = models.TextField(verbose_name="Treść")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Utworzono")

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posty"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def main_photo(self):
        return self.photos.filter(is_main=True).first()


class PostPhoto(models.Model):
    post = models.ForeignKey("blog.Post", on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='posts/')
    order = models.PositiveIntegerField(default=0)
    is_main = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_main:
            PostPhoto.objects.filter(
                post=self.post,
                is_main=True
            ).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)
