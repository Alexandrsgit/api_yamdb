import datetime as dt
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.hashers import make_password

from reviews.models import Category, Genre, Title, User, USER_ROLES


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        fields = ('name', 'slug',)
        lookup_field = 'slug'


class TitleGETSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title при GET запросах."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Title при небезопасных запросах."""

    genre = SlugRelatedField
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all())
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')

    def validate_year(self, data):
        year_now = dt.date.today().year
        if int(self.initial_data['year']) > year_now:
            raise serializers.ValidationError(
                f'Год выпуска произведения не может быть больше {year_now}')
        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

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
    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'нельзя использовать "me" как username')
        return value

    def validate(self, data):
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError(
                'Данный email уже используется'
            )
        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError(
                'Данный username уже используется'
            )
        return data

class UserNotSafeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    role = serializers.ChoiceField(choices=USER_ROLES, read_only=True)

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
