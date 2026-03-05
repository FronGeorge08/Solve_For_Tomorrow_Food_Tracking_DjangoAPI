from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from .models import User
from .serializers import UserSerializer, UserUpdateSerializer
from .request import (
    CreateUserRequest,
    UpdateUserRequest,
    LoginRequest,
    VerifyEmailRequest
)

from rest_framework_simplejwt.tokens import RefreshToken

from .services import generate_verification_code, send_verification_email


# -------------------- CRUD USERS --------------------

class UserHandler(APIView):

    @swagger_auto_schema(request_body=CreateUserRequest)
    def post(self, request):

        serializer = CreateUserRequest(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        user = User(
            name=data["name"],
            username=data["username"],
            email=data["email"],
            description=data["description"],
            image=data["image"],
            is_active=data.get("is_active", True),
            role="user"
        )

        user.set_password(data["password"])
        user.save()

        return Response("User created successfully", status=status.HTTP_201_CREATED)


class UserHandlerWithId(APIView):

    def get(self, request, id=None):

        if id:
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)

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
            return Response({"error": "User not found"}, status=404)

        request_serializer = UpdateUserRequest(data=request.data)

        if not request_serializer.is_valid():
            return Response(request_serializer.errors, status=400)

        update_serializer = UserUpdateSerializer(
            user,
            data=request_serializer.validated_data,
            partial=True
        )

        if update_serializer.is_valid():
            update_serializer.save()
            return Response("User updated successfully")

        return Response(update_serializer.errors, status=400)

    def delete(self, request, id):

        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        user.delete()

        return Response("User deleted successfully")


# -------------------- REGISTER --------------------

class RegisterView(APIView):

    @swagger_auto_schema(request_body=CreateUserRequest)
    def post(self, request):

        serializer = CreateUserRequest(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.validated_data

        if User.objects.filter(username=data["username"]).exists():
            return Response({"error": "Username already exists"}, status=400)

        if User.objects.filter(email=data["email"]).exists():
            return Response({"error": "Email already exists"}, status=400)

        verification_code = generate_verification_code()

        user = User(
            name=data["name"],
            username=data["username"],
            email=data["email"],
            description=data["description"],
            image=data["image"],
            verification_code=verification_code,
            is_verified=False
        )

        user.set_password(data["password"])
        user.save()

        send_verification_email(user)

        return Response(
            {"message": "User registered. Verification email sent."},
            status=201
        )


# -------------------- VERIFY EMAIL --------------------

class VerifyEmailView(APIView):

    @swagger_auto_schema(request_body=VerifyEmailRequest)
    def post(self, request):

        serializer = VerifyEmailRequest(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if user.verification_code != code:
            return Response({"error": "Invalid verification code"}, status=400)

        user.is_verified = True
        user.verification_code = None
        user.save()

        return Response({"message": "Email verified successfully"})


# -------------------- LOGIN --------------------

class LoginView(APIView):

    @swagger_auto_schema(request_body=LoginRequest)
    def post(self, request):

        serializer = LoginRequest(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=401)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=401)

        if not user.is_active:
            return Response({"error": "Account inactive"}, status=403)

        if not user.is_verified:
            return Response({"error": "Email not verified"}, status=403)

        refresh = RefreshToken.for_user(user)

        refresh["email"] = user.email
        refresh["id"] = user.id
        refresh["role"] = user.role

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        )