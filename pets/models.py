from django.db import models
from django.db.models import SET_NULL
from datetime import date
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import os


class Litter(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nazwa miotu (np. Litera A)")
    birth_date = models.DateField(verbose_name="Data urodzenia")
    description = models.TextField(verbose_name="Opis", blank=True)

    # Matka - może być z hodowli lub spoza
    mother = models.ForeignKey(
        "Dog", on_delete=SET_NULL, null=True, blank=True,
        related_name='mother_litters', verbose_name="Matka",
        limit_choices_to={'gender': 'F'}
    )

    # Ojciec - może być z hodowli lub spoza
    father = models.ForeignKey(
        "Dog", on_delete=SET_NULL, null=True, blank=True,
        related_name='father_litters', verbose_name="Ojciec",
        limit_choices_to={'gender': 'M'}
    )

    boys_count = models.PositiveIntegerField(verbose_name="Liczba samców", default=0)
    girls_count = models.PositiveIntegerField(verbose_name="Liczba samic", default=0)
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Adres URL (Slug)")

    class Meta:
        verbose_name = "Miot"
        verbose_name_plural = "Mioty"

    @property
    def total_puppies(self):
        return self.boys_count + self.girls_count

    def __str__(self):
        return f"{self.name} ({self.birth_date.year}) ({self.total_puppies} szczeniąt)"


class Dog(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M', 'Samiec'
        FEMALE = 'F', 'Samica'

    name = models.CharField(max_length=100, verbose_name="Imię domowe/rodowodowe")
    litter = models.ForeignKey(
        Litter, on_delete=SET_NULL, null=True, blank=True,
        related_name='dogs', verbose_name="Miot"
    )

    mother = models.ForeignKey(
        'self', on_delete=SET_NULL, null=True, blank=True,
        related_name='children_as_mother',
        verbose_name="Matka (opcjonalnie)",
        limit_choices_to={'gender': 'F'},
        help_text="Zostaw puste jeśli rodzice są w miocie. Ustaw tylko dla głównych psów hodowlanych."
    )

    father = models.ForeignKey(
        'self', on_delete=SET_NULL, null=True, blank=True,
        related_name='children_as_father',
        verbose_name="Ojciec (opcjonalnie)",
        limit_choices_to={'gender': 'M'},
        help_text="Zostaw puste jeśli rodzice są w miocie. Ustaw tylko dla głównych psów hodowlanych."
    )

    gender = models.CharField(
        max_length=2, choices=Gender.choices, default=Gender.MALE, verbose_name="Płeć"
    )
    birth_date = models.DateField(verbose_name="Data urodzenia")
    description = models.TextField(verbose_name="Opis", blank=True)
    tests = models.TextField(null=True, blank=True, verbose_name="Badania")
    achievements = models.TextField(null=True, blank=True, verbose_name="Osiągnięcia")

    # ZMIENIONO: Waga i wzrost OPCJONALNE (null=True, blank=True)
    weight = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Waga (kg)",
        help_text="Wpisz wagę w kilogramach (opcjonalnie)"
    )
    height = models.FloatField(
        null=True,
        blank=True,
        verbose_name="Wzrost (cm)",
        help_text="Wpisz wzrost w cm (opcjonalnie)"
    )

    color = models.CharField(max_length=50, verbose_name="Umaszczenie")

    # ZMIENIONO: Slug OPCJONALNY (blank=True) - dla psów spoza hodowli można zostawić puste
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        verbose_name="Adres URL (Slug)",
        help_text="Zostaw puste dla psów spoza hodowli (bez własnej strony)"
    )

    show_in_list = models.BooleanField(
        default=True,
        verbose_name="Pokazuj na liście psów",
        help_text="Odznacz dla psów spoza hodowli (pojawią się tylko w rodowodach)"
    )

    class Meta:
        verbose_name = "Pies"
        verbose_name_plural = "Psy"

    @property
    def get_mother(self):
        if self.mother:
            return self.mother
        if self.litter and self.litter.mother:
            return self.litter.mother
        return None

    @property
    def get_father(self):
        if self.father:
            return self.father
        if self.litter and self.litter.father:
            return self.litter.father
        return None

    @property
    def get_maternal_grandmother(self):
        mother = self.get_mother
        return mother.get_mother if mother else None

    @property
    def get_maternal_grandfather(self):
        mother = self.get_mother
        return mother.get_father if mother else None

    @property
    def get_paternal_grandmother(self):
        father = self.get_father
        return father.get_mother if father else None

    @property
    def get_paternal_grandfather(self):
        father = self.get_father
        return father.get_father if father else None

    @property
    def age(self):
        if not self.birth_date:
            return None
        today = date.today()
        years = today.year - self.birth_date.year - (
                    (today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        if years == 0:
            months = (today.year - self.birth_date.year) * 12 + today.month - self.birth_date.month
            return f"{months} msc"
        return f"{years} lat"

    @property
    def main_photo(self):
        return self.photos.filter(is_main=True).first()

    @property
    def has_detail_page(self):
        """Czy pies ma swoją stronę (ma slug i jest show_in_list)"""
        return bool(self.slug)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Jeśli slug jest pusty, wygeneruj automatycznie z nazwy
        # (opcjonalnie - możesz to wyłączyć jeśli chcesz ręcznie kontrolować)
        # if not self.slug and self.show_in_list:
        #     from django.utils.text import slugify
        #     self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class DogPhoto(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='dogs/')
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    upload_date = models.DateTimeField(auto_now_add=True)
    tests = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Zdjęcie"
        verbose_name_plural = "Zdjęcia"
        ordering = ['order', 'upload_date']

    def save(self, *args, **kwargs):
        if self.is_main:
            DogPhoto.objects.filter(dog=self.dog, is_main=True).exclude(pk=self.pk).update(is_main=False)

        is_new_file = False
        if self.pk:
            try:
                old_instance = DogPhoto.objects.get(pk=self.pk)
                if self.image and old_instance.image != self.image:
                    is_new_file = True
            except DogPhoto.DoesNotExist:
                is_new_file = True
        else:
            is_new_file = True

        if self.image and is_new_file:
            self.image = self._optimize_image(self.image)

        super().save(*args, **kwargs)

    def _optimize_image(self, image_field):
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
                output, 'ImageField', new_filename, 'image/jpeg', sys.getsizeof(output), None
            )
        except Exception as e:
            print(f"Image optimization failed: {e}")
            return image_field

    def __str__(self):
        return f"Zdjęcie {self.id} ({self.upload_date.strftime('%Y-%m-%d')})"


class LitterPhoto(models.Model):
    litter = models.ForeignKey(Litter, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='litters/')
    order = models.PositiveIntegerField(default=0)
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Zdjęcie"
        verbose_name_plural = "Zdjęcia"
        ordering = ['order', 'upload_date']

    def save(self, *args, **kwargs):
        is_new_file = False
        if self.pk:
            try:
                old_instance = LitterPhoto.objects.get(pk=self.pk)
                if self.image and old_instance.image != self.image:
                    is_new_file = True
            except LitterPhoto.DoesNotExist:
                is_new_file = True
        else:
            is_new_file = True

        if self.image and is_new_file:
            self.image = self._optimize_image(self.image)

        super().save(*args, **kwargs)

    def _optimize_image(self, image_field):
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
                output, 'ImageField', new_filename, 'image/jpeg', sys.getsizeof(output), None
            )
        except Exception as e:
            print(f"Image optimization failed: {e}")
            return image_field

    def __str__(self):
        return f"Zdjęcie {self.id} ({self.upload_date.strftime('%Y-%m-%d')})"