from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import Product
from .serializers import ProductExpDateSerializer, ProductSerializer
from .request import CreateProductRequest, UpdateProductRequest
from .services import save_product_from_barcode
from django.utils import timezone
from datetime import timedelta

class ProductHandler(APIView):
    """
    Handles:
    - POST /products/   -> Create product from barcode (Open Food Facts)
    - GET  /products/   -> Get all products
    """

    # ---------------------- CREATE ----------------------
    @swagger_auto_schema(request_body=CreateProductRequest)
    def post(self, request):
        # Validate request body
        serializer = CreateProductRequest(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        barcode = serializer.validated_data["barcode"]
        # Fetch product from Open Food Facts & save to DB
        product = save_product_from_barcode(barcode)
        product.user_id=request.data.get("user_id")
        product.expiration_date=request.data.get("expire_date")
        product.save()
        if not product:
            return Response(
                {"error": "Product not found in Open Food Facts"},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            ProductSerializer(product).data,
            status=status.HTTP_201_CREATED
        )
    # ---------------------- GET ALL ----------------------
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class ProductHandlerWithId(APIView):
    """
    Handles:
    - GET    /products/{id}/
    - PUT    /products/{id}/
    - DELETE /products/{id}/
    """
    
    # ---------------------- GET BY ID ----------------------
    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    # ---------------------- UPDATE ----------------------
    @swagger_auto_schema(request_body=UpdateProductRequest)
    def put(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        request_serializer = UpdateProductRequest(data=request.data)
        if not request_serializer.is_valid():
            return Response(
                request_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        update_serializer = ProductSerializer(
            product,
            data=request_serializer.validated_data,
            partial=True
        )

        if update_serializer.is_valid():
            update_serializer.save()
            return Response(
                "Product updated successfully",
                status=status.HTTP_200_OK
            )

        return Response(
            update_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    # ---------------------- DELETE ----------------------
    def delete(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        product.delete()
        return Response(
            "Product deleted successfully",
            status=status.HTTP_200_OK
        )
@api_view(["GET"])
def is_expiring_3days(request):
        products = Product.objects.all()
        about_to_expire=[]
        print (products[0].expiration_date)
        for i in products:
            if i.expiration_date - timezone.now() <= timedelta(days=3):              
                about_to_expire.append(i)
        return Response(ProductExpDateSerializer(about_to_expire,many=True).data)