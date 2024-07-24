from rest_framework import generics
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

User = get_user_model()

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



@api_view(['POST'])
def create_superuser(request):
    data = request.data.copy()
    # data['is_staff'] = request.data['is_staff']
    # data['is_superuser'] = True
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'detail': 'Superuser created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

