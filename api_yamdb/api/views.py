from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets

from api.filters import TitleFilter
from api.serializers import (CategorySerializer,
                             GenreSerializer,
                             TitleSerializer,
                             TitleGETSerializer)
from reviews.models import Category, Genre, Title


class TitleViewSet(viewsets.ModelViewSet):
    """Обрабатываем запросы о произведениях."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # permission_classes = 
    # pagination_class = 
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Определяем, какой сериализатор будет
        использован в зависимости от метода запроса."""
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitleSerializer


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateListDestroyViewSet):
    """Обрабатываем запросы о категориях."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    # permission_classes = 
    # pagination_class = 


class GenreViewSet(CreateListDestroyViewSet):
    """Обрабатываем запросы о жанрах."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    # permission_classes = 
    # pagination_class = 
