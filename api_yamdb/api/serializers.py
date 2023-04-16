from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import User, USER_ROLES


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
