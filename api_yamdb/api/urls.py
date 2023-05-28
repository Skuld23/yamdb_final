from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentsViewSet, GenreViewSet,
                    ReviewsViewSet, TitleViewSet, UserViewSet, get_jwt_token,
                    signup)

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register('titles', TitleViewSet, basename='titles')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewsViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', get_jwt_token, name='login'),
    path('v1/', include('djoser.urls')),  # Работа с пользователями
    path('v1/', include('djoser.urls.jwt')),  # Работа с jwt токенами
]
