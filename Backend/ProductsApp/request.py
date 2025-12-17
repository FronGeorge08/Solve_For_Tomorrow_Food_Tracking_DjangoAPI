from rest_framework import serializers


class CreateProductRequest(serializers.Serializer):
    barcode = serializers.CharField(required=True, max_length=300)
    expire_date=serializers.DateTimeField()
    user_id=serializers.IntegerField()


class UpdateProductRequest(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    image = serializers.CharField(max_length=1000, required=False)
    brand = serializers.CharField(max_length=100, required=False)
    ingredients = serializers.CharField(required=False)

    calories = serializers.FloatField(required=False)
    fat = serializers.FloatField(required=False)
    sugars = serializers.FloatField(required=False)
    proteins = serializers.FloatField(required=False)
    salt = serializers.FloatField(required=False)

    expiration_date = serializers.DateTimeField(required=False)
