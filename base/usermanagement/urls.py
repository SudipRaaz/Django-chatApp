from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('register/', views.UserCreate.as_view(), name='user-register'),
    path('create_superuser/', views.create_superuser, name='create-superuser'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', views.UserProfile.as_view(), name='user list'),
    path('users/<int:id>/', views.UserProfile.as_view(), name='specific user'),
]
