from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                       UserViewSet, CommentViewSet, ReviewViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('titles', TitleViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register(r'users', UserViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='review')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment')
# router.register('auth/signup', SignUpView, basename='singup')
# router.register('auth/token', ConfirmCodeCheckView, basename='token')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/',
         TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/auth/token/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('v1/auth/signup/', SignUpView.as_view({'post': 'create'}), name='signup'),
    # path('v1/auth/token/', ConfirmCodeCheckView.as_view({'post': 'create'}), name='token')
]
