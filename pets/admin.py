from django.contrib import admin
from django.utils.html import format_html
from .models import Dog, Litter, DogPhoto, LitterPhoto


class DogPhotoInline(admin.TabularInline):
    model = DogPhoto
    extra = 1
    fields = ('image_preview', 'image', 'is_main', 'order')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:100px;height:100px;object-fit:cover;">',
                obj.image.url
            )
        return "—"
    image_preview.short_description = "Podgląd"


class LitterPhotoInline(admin.TabularInline):
    model = LitterPhoto
    extra = 1
    fields = ('image_preview', 'image', 'order')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:100px;height:100px;object-fit:cover;">',
                obj.image.url
            )
        return "—"
    image_preview.short_description = "Podgląd"


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'litter', 'gender', 'status', 'age', 'main_photo_preview')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('status', 'gender', 'litter')
    search_fields = ('name',)
    readonly_fields = ('age',)
    inlines = [DogPhotoInline]

    def main_photo_preview(self, obj):
        if obj.main_photo:
            return format_html(
                '<img src="{}" style="width:60px;height:60px;object-fit:cover;">',
                obj.main_photo.image.url
            )
        return "—"
    main_photo_preview.short_description = "Główne zdjęcie"


@admin.register(Litter)
class LitterAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'mother', 'father', 'total_puppies')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'mother__name', 'father__name')
    inlines = [LitterPhotoInline]
