from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from .models import User
from .serializers import UserSerializer, UserUpdateSerializer
from .request import CreateUserRequest, UpdateUserRequest, LoginRequest

from rest_framework_simplejwt.tokens import RefreshToken

# -------------------- CRUD USERS --------------------
class UserHandler(APIView):
    @swagger_auto_schema(request_body=CreateUserRequest)
    def post(self, request):
        serializer = CreateUserRequest(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # Create user instance
        user = User(
            name=data["name"],
            username=data["username"],
            email=data["email"],
            description=data["description"],
            image=data["image"],
            is_active=data.get("is_active", True),
            role=data.get("role", "user")
        )

        # Hash password before saving
        user.set_password(data["password"])
        user.save()

        return Response("User created successfully", status=status.HTTP_201_CREATED)

class UserHandlerWithId(APIView):
    def get(self, request, id=None):
        if id:
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = UserSerializer(user)
            return Response(serializer.data)

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UpdateUserRequest)
    def put(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        request_serializer = UpdateUserRequest(data=request.data)
        if not request_serializer.is_valid():
            return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        update_serializer = UserUpdateSerializer(
            user,
            data=request_serializer.validated_data,
            partial=True
        )
        if update_serializer.is_valid():
            update_serializer.save()
            return Response("User updated successfully")
        return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response("User deleted successfully", status=status.HTTP_200_OK)


# -------------------- AUTHENTICATION --------------------
class RegisterView(APIView):
    """Register a new user with hashed password."""

    @swagger_auto_schema(request_body=CreateUserRequest)
    def post(self, request):
        serializer = CreateUserRequest(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # Check uniqueness
        if User.objects.filter(username=data["username"]).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=data["email"]).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Create user instance
        user = User(
            name=data["name"],
            username=data["username"],
            email=data["email"],
            description=data["description"],
            image=data["image"],
            is_active=data.get("is_active", True),
            role="user"
        )

        # Hash password
        user.set_password(data["password"])
        user.save()

        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    """Login with email + password and return JWT tokens."""

    @swagger_auto_schema(request_body=LoginRequest)
    def post(self, request):
        serializer = LoginRequest(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({"error": "Account is inactive"}, status=status.HTTP_403_FORBIDDEN)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        refresh["email"] = user.email
        refresh["id"] = user.id
        refresh["role"] = user.role

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)