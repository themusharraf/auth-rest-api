from django.urls import path
from .views import register_user, login_user, get_users, create_post
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('users/', get_users, name='get_users'),
    path('posts/', create_post, name='create_post'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
