from django.db import models
from django.db.models import SET_NULL
from datetime import date
from django.db.models import JSONField


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tytuł")
    content = models.TextField(verbose_name="Treść")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Utworzono")

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posty"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Litter(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nazwa miotu (np. Litera A)")
    birth_date = models.DateField(verbose_name="Data urodzenia")
    mother = models.ForeignKey(
        "Dog", on_delete=SET_NULL, null=True, blank=True,
        related_name='mother_litters', verbose_name="Matka",
        limit_choices_to={'gender': 'F'}
    )
    father = models.ForeignKey(
        "Dog", on_delete=SET_NULL, null=True, blank=True,
        related_name='father_litters', verbose_name="Ojciec",
        limit_choices_to={'gender': 'M'}
    )

    class Meta:
        verbose_name = "Miot"
        verbose_name_plural = "Mioty"

    def __str__(self):
        return f"{self.name} ({self.birth_date.year})"


class Dog(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Dostępny'
        RESERVED = 'reserved', 'Zarezerwowany'
        SOLD = 'sold', 'Sprzedany'
        STAYED = 'stayed', 'Został w hodowli'

    class Gender(models.TextChoices):
        MALE = 'M', 'Pies'
        FEMALE = 'F', 'Suka'

    name = models.CharField(max_length=100, verbose_name="Imię domowe/rodowodowe")
    litter = models.ForeignKey(
        Litter, on_delete=SET_NULL, null=True, blank=True,
        related_name='dogs', verbose_name="Miot"
    )
    gender = models.CharField(
        max_length=2, choices=Gender.choices, default=Gender.MALE, verbose_name="Płeć"
    )
    birth_date = models.DateField(verbose_name="Data urodzenia")
    description = models.TextField(verbose_name="Opis", blank=True)
    vaccinations = models.TextField(null=True, blank=True, verbose_name="Szczepienia")
    achievements = models.TextField(null=True, blank=True, verbose_name="Osiągnięcia")

    weight = models.FloatField(verbose_name="Waga (kg)", help_text="Wpisz wagę w kilogramach")
    height = models.FloatField(verbose_name="Wzrost (cm)", help_text="Wpisz wzrost w cm")
    color = models.CharField(max_length=50, verbose_name="Umaszczenie")
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.AVAILABLE, verbose_name="Status"
    )

    class Meta:
        verbose_name = "Pies"
        verbose_name_plural = "Psy"

    @property
    def age(self):
        if not self.birth_date:
            return None
        today = date.today()
        years = today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
        if years == 0:
            months = (today.year - self.birth_date.year) * 12 + today.month - self.birth_date.month
            return f"{months} msc"
        return f"{years} lat"

    def save(self, *args, **kwargs):
        if not self.birth_date and self.litter:
            self.birth_date = self.litter.birth_date
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Photo(models.Model):
    image = models.ImageField(upload_to='dog_photos/', verbose_name="Zdjęcie")
    upload_date = models.DateTimeField(auto_now_add=True)
    dog = models.ForeignKey(
        Dog, on_delete=models.CASCADE, null=True, blank=True, related_name='photos'
    )
    litter = models.ForeignKey(
        Litter, on_delete=models.CASCADE, null=True, blank=True, related_name='photos'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, blank=True, related_name='photos'
    )

    class Meta:
        verbose_name = "Zdjęcie"
        verbose_name_plural = "Zdjęcia"

    def __str__(self):
        return f"Zdjęcie {self.id} ({self.upload_date.strftime('%Y-%m-%d')})"