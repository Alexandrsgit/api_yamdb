from django.contrib import admin

from .models import Comment, Review, Category, Genre, Title, User


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'year', 'description', 'category', 'title_genre')
    list_editable = ('category',)
    search_fields = ('name',)
    list_filter = ('year', 'category', 'genre')

    def title_genre(self, object):
        return ', '.join((genre.name for genre in object.genre.all()))
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


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'author',
        'score',
    )
    search_fields = ('pub_date',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )
    search_fields = ('review',)
    list_filter = ('review',)
    empty_value_display = '-пусто-'
