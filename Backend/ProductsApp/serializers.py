from rest_framework import serializers
from .models import Product
from django.utils import timezone
from datetime import timedelta

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
class ProductExpDateSerializer(serializers.ModelSerializer):
    duration=serializers.SerializerMethodField()
    class Meta:
        model=Product
        fields=['id','image','name','duration']
    def get_duration(self,obj:Product):
        return (obj.expiration_date - timezone.now()).days