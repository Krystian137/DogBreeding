from django.contrib import admin
from django.utils.html import format_html
from blog.models import Post, PostPhoto


class PostPhotoInline(admin.TabularInline):
    model = PostPhoto
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


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'main_photo_preview')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    inlines = [PostPhotoInline]

    def main_photo_preview(self, obj):
        if obj.main_photo:
            return format_html(
                '<img src="{}" style="width:60px;height:60px;object-fit:cover;">',
                obj.main_photo.image.url
            )
        return "—"
    main_photo_preview.short_description = "Główne zdjęcie"
