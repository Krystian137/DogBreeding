from django.db import models
from django.db.models import SET_NULL
from datetime import date

class Litter(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nazwa miotu (np. Litera A)")
    birth_date = models.DateField(verbose_name="Data urodzenia")
    description = models.TextField(verbose_name="Opis", blank=True)
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
    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Dostępny'
        RESERVED = 'reserved', 'Zarezerwowany'
        SOLD = 'sold', 'Sprzedany'
        STAYED = 'stayed', 'Został w hodowli'

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
    vaccinations = models.TextField(null=True, blank=True, verbose_name="Szczepienia")
    achievements = models.TextField(null=True, blank=True, verbose_name="Osiągnięcia")
    weight = models.FloatField(verbose_name="Waga (kg)", help_text="Wpisz wagę w kilogramach")
    height = models.FloatField(verbose_name="Wzrost (cm)", help_text="Wpisz wzrost w cm")
    color = models.CharField(max_length=50, verbose_name="Umaszczenie")
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.AVAILABLE, verbose_name="Status"
    )
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Adres URL (Slug)")
    show_in_list = models.BooleanField(
        default=True,
        verbose_name="Pokazuj na liście psów"
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
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
        if years == 0:
            months = (today.year - self.birth_date.year) * 12 + today.month - self.birth_date.month
            return f"{months} msc"
        return f"{years} lat"

    @property
    def main_photo(self):
        return self.photos.filter(is_main=True).first()

    def __str__(self):
        return self.name


class DogPhoto(models.Model):
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='dogs/')
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    upload_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Zdjęcie"
        verbose_name_plural = "Zdjęcia"

    def save(self, *args, **kwargs):
        if self.is_main:
            DogPhoto.objects.filter(
                dog=self.dog,
                is_main=True
            ).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['order', 'upload_date']

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

    def __str__(self):
        return f"Zdjęcie {self.id} ({self.upload_date.strftime('%Y-%m-%d')})"

