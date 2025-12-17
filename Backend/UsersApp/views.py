from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from .models import User
from .serializers import UserSerializer, UserUpdateSerializer
from .request import CreateUserRequest, UpdateUserRequest


class UserHandler(APIView):
    # ---------------------- CREATE ----------------------
    @swagger_auto_schema(request_body=CreateUserRequest)
    def post(self, request):
        serializer = CreateUserRequest(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_serializer = UserSerializer(data=serializer.validated_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response("The user is created", status=status.HTTP_201_CREATED)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserHandlerWithId(APIView):
    # ---------------------- GET (ALL or BY ID) ----------------------
    def get(self, request,id):
        if id:
            # GET by ID
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        # GET ALL
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    # ---------------------- UPDATE ----------------------
    @swagger_auto_schema(request_body=UpdateUserRequest)
    def put(self, request,id):
        user = User.objects.get(id=id)
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
    # ---------------------- DELETE ----------------------
    def delete(self, request,id):
        if not id:
            return Response({"error": "id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response("User deleted successfully", status=status.HTTP_200_OK)
