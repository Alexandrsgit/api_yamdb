from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator
from api.filters import TitleFilter
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, TitleGETSerializer,
                             UserSerializer, CommentSerializer,
                             ReviewSerializer, UserNotSafeSerializer,
                             UserSignUp, ConfirmCodeCheck)
from rest_framework import filters, viewsets, mixins, status, generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.db import IntegrityError
from api.permissions import IsAdmin, IsModeraror, IsUser
from api.pagination import UserPagination
from reviews.models import Category, Genre, Title, User, Review, Comment


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
    http_method_names = ['get', 'post', 'patch', 'delete']
    search_fields = ('=username',)
    filterset_fields = ('role',)
    ordering_fields = ('username',)

    def get_serializer_class(self):
        """Выбор какой сериализатор будет использован, если метод не безопасен."""
        if self.request.method == 'GET' or (
                self.request.user.role == 'admin' or self.request.user.is_superuser is True):
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
                                status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(self_profile)
        return Response(serializer.data)

class SignUpView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSignUp

    def user_create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user, _ = User.objects.get_or_create(
                    **serializer.validated_data)
            except IntegrityError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                'confirmation code',
                confirmation_code,
                None,
                serializer.validated_data['email'],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

class ConfirmCodeCheckView(viewsets.ModelViewSet):
    serializer_class = ConfirmCodeCheck


    def user_check_and_give_token(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            confirmation_code = serializer.validated_data.get('confirmation_code')
            user, _ = User.objects.get(username=username)
            if default_token_generator.check_token(confirmation_code):
                return AccessToken(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes =

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        return review.comment.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes =

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
