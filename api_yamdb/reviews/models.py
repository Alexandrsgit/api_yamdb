from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

CHOICES_CATEGORY = (
    ('Книга', 'book'),
    ('Музыка', 'music'),
    ('Фильм', 'movie'),
)


class Category(models.Model):
    """Модель для категорий."""
    name = models.CharField(
        max_length=256,
        verbose_name='Hазвание',
        choices=CHOICES_CATEGORY)
    slug = models.SlugField(
        max_length=50,
        verbose_name='slug',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Slug категории содержит недопустимые символы'
        )])

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель для жанров."""
    name = models.CharField(
        max_length=256,
        verbose_name='Hазвание',)
    slug = models.SlugField(
        max_length=50,
        verbose_name='slug',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
            message='Slug жанра содержит недопустимые символы'
        )])

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель для произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Hазвание произведения')
    year = models.IntegerField(
        verbose_name='Год выпуска')
    description = models.TextField(
        verbose_name='Описание',
        blank=True)
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        related_name='titles',
        null=True,
        on_delete=models.SET_NULL)
    genres = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр',
        related_name='titles')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', 'year']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    """Дополнительная модель, связывающая произведения и жанры."""
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
