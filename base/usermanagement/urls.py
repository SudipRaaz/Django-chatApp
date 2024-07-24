from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserCreate.as_view(), name='user-register'),
    path('create_superuser/', views.create_superuser, name='create-superuser'),
]
