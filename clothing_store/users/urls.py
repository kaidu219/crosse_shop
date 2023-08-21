from rest_framework.routers import DefaultRouter

from django.urls import path
from users.views import RegisterViewSet, LoginViewSet, FavoriteViewSet, UserDetailView

router = DefaultRouter()

router.register(r'register', RegisterViewSet, basename='register')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'favorites', FavoriteViewSet, basename='favorite')

urlpatterns = [
    path('users/detail/', UserDetailView.as_view(), name='user-detail'),
]

urlpatterns += router.urls
