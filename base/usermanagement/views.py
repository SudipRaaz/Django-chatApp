from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

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

class UserProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id=None, *args, **kwargs):
        if id is None:
            # Retrieve all users
            queryset = User.objects.all()
            serializers = UserSerializer(queryset, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            # Retrieve a specific user by ID
            try:
                user = User.objects.get(id=id)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": f"User with ID {id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self,request, id, *args, **kwargs):
        try:
            query = User.objects.get(id=id)
            serializer = UserSerializer(query)
            # query.delete()
            return Response({"message": f"{query}{serializer.data}"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": f"User with ID {id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id, *args, **kwargs):
        try:
            user = User.objects.get(id=id)
            if request.user != user:
                return Response({"message": "You can not modify this user"}, status=status.HTTP_403_FORBIDDEN)
            serializer = UserSerializer(user, data=request.data, partial= True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": f"User with ID {id} does not exist."}, status=status.HTTP_404_NOT_FOUND)
