from django.contrib import admin
from .models import Categoria, ImagemPost, Post

class ImagemPostInline(admin.TabularInline):
    model = ImagemPost
    extra = 1

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nome",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("titulo",)}
    inlines = [ImagemPostInline]