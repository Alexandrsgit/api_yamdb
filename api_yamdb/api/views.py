from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.mixins import CreateListDestroyViewSet
from api.pagination import UserPagination
from api.permissions import IsAdmin, IsModerOrAdminOrAuthor, IsUser
from api.serializers import (CategorySerializer, CommentSerializer,
                             ConfirmCodeCheck, GenreSerializer,
                             ReviewSerializer, TitleGETSerializer,
                             TitleSerializer, UserNotSafeSerializer,
                             UserSerializer, UserSignUp)
from reviews.models import Category, Genre, Review, Title, User


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
        """Определяем, какой сериализатор будет использован в зависимости
        от метода запроса."""
        if self.request.method in ['GET']:
            return TitleGETSerializer
        return TitleSerializer

    def get_permissions(self):
        """Выбираем permissions с правами доступа в зависимости от метода
        запроса."""
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
        """Выбор какой сериализатор будет использован,
        если метод не безопасен.
        """
        if self.request.method == 'GET' or (
                self.request.user.role == 'admin'
                or self.request.user.is_superuser is True):
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
    """Регистрация пользователя."""

    permission_classes = (AllowAny,)
    serializer_class = UserSignUp
    queryset = User.objects.all()

    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        if (User.objects.filter(email=email).exists()
                and User.objects.filter(username=username).exists()):
            user = User.objects.get(email=email)
            confirmation_code = default_token_generator.make_token(user)
            send_mail('confirmation code', confirmation_code, None,
                      [email], fail_silently=False,)
            return Response(status=status.HTTP_200_OK)
        else:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                username = serializer.validated_data.get('username')
                usermail = serializer.validated_data.get('email')
                user = User.objects.create(username=username, email=usermail)
                confirmation_code = default_token_generator.make_token(user)
                send_mail('confirmation code', confirmation_code, None,
                          [usermail], fail_silently=False,)
            return Response(serializer.data, status=status.HTTP_200_OK)


class ConfirmCodeCheckView(generics.ListCreateAPIView):
    """Проверка пользователя и кода подтверждения."""

    permission_classes = (AllowAny,)
    serializer_class = ConfirmCodeCheck
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        username = serializer.validated_data.get('username')
        confirmation_code = (
            serializer.validated_data.get('confirmation_code'))
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(f'token: {str(AccessToken.for_user(user))}',
                        status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsModerOrAdminOrAuthor,)
    pagination_class = UserPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsModerOrAdminOrAuthor,)
    pagination_class = UserPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
