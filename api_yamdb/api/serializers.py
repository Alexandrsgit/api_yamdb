import datetime as dt
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Genre, Title, User, USER_ROLES


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


class UserSignUp(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]

    def validate_username(self, data):
        if self.initial_data['username'] == 'me':
            raise serializers.ValidationError('username не может быть - "me"')
        return data
