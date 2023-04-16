from django.db import models
from django.contrib.auth.models import AbstractUser

USER_ROLES = (
    ('user', 'Пользователь'),
    ('admin', 'Администратор'),
    ('moderator', 'Модератор'),
)


class User(AbstractUser):
    """Модель пользователя."""

    bio = models.TextField(max_length=200, verbose_name='Биография',
                           blank=True)
    role = models.CharField(max_length=20, verbose_name='Роль',
                            choices=USER_ROLES, default='user')
    is_superuser = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=200,
                                         verbose_name='Код подтверждения',
                                         blank=True)

    class Meta:
        """Уникальность полей в модели User."""

        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user'
            )
        ]
