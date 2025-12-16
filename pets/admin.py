from django.contrib import admin
from django.utils.html import format_html
from pets.models import Dog, Litter, Photo

# Register your models here.
class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    fields = ('image_preview', 'image')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: 100px; object-fit: cover;"/>', obj.image.url)
        return "Bralo zdjęcia"
    image_preview.short_description = "Podgląd zdjęcia"

@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'litter', 'gender', 'status', 'age')
    list_filter = ('status', 'gender', 'litter')
    search_fields = ('name',)
    readonly_fields = ('age',)
    inlines = [PhotoInline]

    def avatar_preview(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="width: 100px; height: 100px; object-fit: cover;"/>', obj.main_image.url)
        return "-"
    avatar_preview.short_description = "Awatar"


@admin.register(Litter)
class LitterAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'mother', 'father', 'boys_count', 'girls_count', 'total_puppies_display')
    def total_puppies_display(self, obj):
        return obj.total_puppies
    total_puppies_display.short_description = "Łączna liczba szczeniąt"


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'dog', 'litter', 'post', 'upload_date')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover;"/>', obj.image.url)

    image_preview.short_description = "Podgląd"