from rest_framework import serializers

class CreateUserRequest(serializers.Serializer):
    name=serializers.CharField(max_length=20)
    username=serializers.CharField(max_length=20)
    email=serializers.EmailField()
    password=serializers.CharField(max_length=128)
    description=serializers.CharField(max_length=200)
    image=serializers.CharField(max_length=1000)
    is_active=serializers.BooleanField()

class UpdateUserRequest(serializers.Serializer):
    name = serializers.CharField(max_length=20, required=False)
    username = serializers.CharField(max_length=20, required=False)
    description = serializers.CharField(max_length=200, required=False)
    image = serializers.CharField(max_length=1000, required=False)

class LoginRequest(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)