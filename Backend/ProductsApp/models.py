from django.db import models
from django.utils import timezone
from UsersApp.models import User
class Product(models.Model):
    barcode = models.CharField(max_length=300)
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=1000, null=True, blank=True)
    brand = models.CharField(max_length=100, null=True, blank=True)

    ingredients = models.TextField(null=True, blank=True)

    calories = models.FloatField(null=True, blank=True)   # kcal per 100g
    fat = models.FloatField(null=True, blank=True)
    sugars = models.FloatField(null=True, blank=True)
    proteins = models.FloatField(null=True, blank=True)
    salt = models.FloatField(null=True, blank=True)

    expiration_date = models.DateTimeField(null=True, blank=True)
    creation_date = models.DateTimeField(
        default=timezone.now  # <- fills existing rows
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=2)
    def __str__(self):
        return f"{self.name} ({self.barcode})"


# ❗ NOT A DATABASE MODEL
class OpenFoodFactsProduct:
    def __init__(
        self,
        barcode,
        name=None,
        image_url=None,
        brand=None,
        ingredients=None,
        calories=None,
        fat=None,
        sugars=None,
        proteins=None,
        salt=None,
        expiration_date=None
    ):
        self.barcode = barcode
        self.name = name
        self.image_url = image_url
        self.brand = brand
        self.ingredients = ingredients
        self.calories = calories
        self.fat = fat
        self.sugars = sugars
        self.proteins = proteins
        self.salt = salt
        self.expiration_date = expiration_date

    @classmethod
    def from_api_response(cls, data: dict):
        product = data.get("product", {})
        nutriments = product.get("nutriments", {})

        return cls(
            barcode=data.get("code"),
            name=product.get("product_name"),
            image_url=product.get("image_front_url"),
            brand=product.get("brands"),
            ingredients=product.get("ingredients_text"),
            calories=nutriments.get("energy-kcal_100g"),
            fat=nutriments.get("fat_100g"),
            sugars=nutriments.get("sugars_100g"),
            proteins=nutriments.get("proteins_100g"),
            salt=nutriments.get("salt_100g"),
            expiration_date=product.get("expiration_date"),
        )
