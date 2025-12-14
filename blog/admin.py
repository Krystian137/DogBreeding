from django.contrib import admin
from blog.models import Post
from pets.models import Photo

# Register your models here.

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    fields = ('image', 'dog', 'litter')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
    ordering = ('-created_at',)
    inlines = [PhotoInline]