from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('register/', views.UserCreate.as_view(), name='user-register'),
    path('create_superuser/', views.create_superuser, name='create-superuser'),
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

   
    path('login/', views.LoginView.as_view(), name='token_obtain_pair'),     # login with cookies set 
    path('login/token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', views.UserProfile.as_view(), name='user list'),  # get the list of all users
    path('users/<int:id>/', views.UserProfile.as_view(), name='specific user'), # get a particular user with given ID
    # path('users/<str:email>/', views.UserProfile.as_view(), name='specific user'), # get a particular user with given ID
    path('users/<str:name>/', views.UserProfile.as_view(), name='specific user'), # get a particular user with given ID
]
