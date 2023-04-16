from django.contrib import admin

from .models import Category, Genre, Title, User


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'year', 'description', 'category', 'title_genre')
    list_editable = ('category',)
    search_fields = ('name',)
    list_filter = ('year', 'category', 'genres')

    def title_genre(self, object):
        return ', '.join((genres.name for genres in object.genres.all()))
    title_genre.short_description = 'Жанры'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)

admin.site.register(User)
