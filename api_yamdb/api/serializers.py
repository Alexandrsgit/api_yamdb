import datetime as dt
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from reviews.models import (Category, Genre, Title,
                            User, USER_ROLES, Comment, Review)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class TitleGETSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title при GET запросах."""
    category = CategorySerializer(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'category', 'genres')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title при небезопасных запросах."""
    genres = SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all())
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'category', 'genres')

    def validate_year(self, data):
        year_now = dt.date.today().year
        if self.initial_data['year'] > year_now:
            raise serializers.ValidationError(
                f'Год выпуска произведения не может быть больше {year_now}')
        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор дял модели User."""

    role = serializers.ChoiceField(choices=USER_ROLES, default='user')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')

        # Валидация на уникальность
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugField(
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate_score(self, value):
        if 0 > value < 10:
            raise serializers.ValidationError('Оценка по 10-бальной шкале!')
        raise value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Может существовать только один отзыв!')
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
