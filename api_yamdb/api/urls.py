from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet, import UserViewSet

app_name = 'api'

router = DefaultRouter()
router.register('titles', TitleViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
