from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from difflib import get_close_matches

from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# create user
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# create super user
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

# login user
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed("User not found")
        if not user.check_password(password):
            raise AuthenticationFailed("Invalid Credentials")

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response({"refresh": str(refresh), "access": access_token}, status=status.HTTP_200_OK)

        # Set access token in cookie
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,  # Make cookie inaccessible for JavaScripts
            secure=True,  # Ensures cookie is only sent over HTTPS
            samesite='Lax',  # Helps protect against CSRF
        )
        return response

class UserProfile(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id=None, email=None, name=None, *args, **kwargs):
        if id is not None:
            # Retrieve a specific user by ID
            try:
                user = User.objects.get(id=id)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": f"User with ID {id} does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        elif email is not None:
            # Retrieve a specific user by email
            try:
                user = User.objects.get(email=email)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": f"User with email {email} does not exist."}, status=status.HTTP_404_NOT_FOUND)
        elif name:
            # Debugging print statements
            print(f"Searching for the closest match to the name: {name}")
            
            # Find the most similar username
            usernames = list(User.objects.values_list('name', flat=True)) or []
            print(f"Usernames retrieved from the database: {usernames}")
            
            if usernames:
                closest_match = get_close_matches(name, usernames, n=1, cutoff=0.6)
                print(f"Closest match found: {closest_match}") 
                
                if closest_match:
                    try:
                        user = User.objects.get(name=closest_match[0])
                        serializer = UserSerializer(user)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    except User.DoesNotExist:
                        return Response({"error": f"No user found for the closest match '{closest_match[0]}'."}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({"error": f"No similar username found for '{name}'."}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"error": "No users found in the database."}, status=status.HTTP_404_NOT_FOUND)
        
        else:
            # Retrieve all users if no specific filter is provided
            queryset = User.objects.all()
            serializers = UserSerializer(queryset, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)

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