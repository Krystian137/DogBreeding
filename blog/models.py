from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import os


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

    class Meta:
        verbose_name = "Zdjęcie"
        verbose_name_plural = "Zdjęcia"
        ordering = ['order']

    def save(self, *args, **kwargs):
        if self.is_main:
            PostPhoto.objects.filter(
                post=self.post,
                is_main=True
            ).exclude(pk=self.pk).update(is_main=False)
        if self.pk:
            try:
                old_instance = PostPhoto.objects.get(pk=self.pk)
                is_new_file = self.image != old_instance.image
            except PostPhoto.DoesNotExist:
                is_new_file = True
        else:
            is_new_file = True

        if self.image and is_new_file:
            self.image = self._optimize_image(self.image)

        super().save(*args, **kwargs)

    def _optimize_image(self, image_field):
        """Optimize image: resize and compress"""
        try:
            img = Image.open(image_field)

            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img)
                img = background

            max_size = (1920, 1920)
            if img.width > max_size[0] or img.height > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)

            output = BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)

            filename = os.path.basename(image_field.name)
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}.jpg"

            return InMemoryUploadedFile(
                output,
                'ImageField',
                new_filename,
                'image/jpeg',
                sys.getsizeof(output),
                None
            )
        except Exception as e:
            print(f"Image optimization failed: {e}")
            return image_field

    def __str__(self):
        return f"Zdjęcie posta: {self.post.title}"