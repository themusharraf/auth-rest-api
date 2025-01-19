from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import User, Post
from api.serializers import UserSerializer, PostSerializer, LoginSerializer
from api.permissions import IsAdmin


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user and return JWT tokens.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Hash the password and save the user
        user = serializer.save(password=make_password(serializer.validated_data['password']))

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Return user data along with tokens
        return Response({
            "refresh": str(refresh),
            "access": access_token,
            "user": serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Authenticate a user using email and password, then return JWT tokens.
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        user = User.objects.get(email=email)
        print(f"{user.email}")
        print(f"{user.password}")
        if user.check_password(password):
            if not user.is_active:
                return Response({"detail": "User account is inactive."}, status=status.HTTP_400_BAD_REQUEST)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "refresh": str(refresh),
                "access": access_token,
                "user": UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def get_users(request):
    """
    Retrieve all users (Admin-only access).
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def create_post(request):
    """
    Allow admins to create a post.
    """
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(admin=request.user)  # Attach the logged-in admin as the creator of the post
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
