from rest_framework import filters
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from api.permissions import IsAdmin, IsModeraror, IsUser
from api.serializers import UserSerializer
from api.pagination import UserPagination
from reviews.models import User


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

    @action(methods=['GET', 'PATCH'], detail=False, url_path='me',
            permission_classes=(IsUser,))
    def user_self_profile(self, request):
        """Получение и изменение информации пользователя о себе users/me."""
        # request.uesr.username(get_user = request.user)
        get_selfuser_username = 'admin'
        self_profile = get_object_or_404(User, username=get_selfuser_username)
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
