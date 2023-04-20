from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.mixins import CreateListDestroyViewSet
from api.filters import TitleFilter
from api.permissions import IsAdmin, IsModeraror, IsUser
from api.pagination import UserPagination
from api.serializers import (CategorySerializer,
                             GenreSerializer,
                             TitleSerializer,
                             TitleGETSerializer,
                             UserSerializer,
                             UserNotSafeSerializer)
from reviews.models import (Category, Genre, Title, User)


class TitleViewSet(viewsets.ModelViewSet):
    """Обрабатываем запросы о произведениях."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    permission_classes = (IsAdmin,)
    pagination_class = UserPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    search_fields = ('=name',)

    def get_serializer_class(self):
        """Определяем, какой сериализатор будет
        использован в зависимости от метода запроса."""
        if self.request.method in ['GET']:
            return TitleGETSerializer
        return TitleSerializer

    def get_permissions(self):
        """Выбираем permissions с правами доступа
        в зависимости от метода запроса."""
        if self.request.method == 'GET':
            return (IsAuthenticatedOrReadOnly(),)
        return super().get_permissions()


class CategoryViewSet(CreateListDestroyViewSet):
    """Обрабатываем запросы о категориях."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    """Обрабатываем запросы о жанрах."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    pagination_class = UserPagination
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,
                       filters.OrderingFilter)
    search_fields = ('=username',)
    filterset_fields = ('role',)
    ordering_fields = ('username',)

    def get_serializer_class(self):
        """Выбор какой сериализатор будет
        использован, если метод не безопасен."""
        if self.request.method == 'GET' or self.request.user.role == 'admin':
            return UserSerializer
        return UserNotSafeSerializer

    @action(methods=['GET', 'PATCH'], detail=False, url_path='me',
            permission_classes=(IsUser,))
    def user_self_profile(self, request):
        """Получение и изменение информации пользователя о себе users/me."""
        self_profile = get_object_or_404(User, username=request.user.username)
        if request.method == 'PATCH':
            serializer = self.get_serializer(self_profile, data=request.data,
                                             partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(self_profile)
        return Response(serializer.data)
