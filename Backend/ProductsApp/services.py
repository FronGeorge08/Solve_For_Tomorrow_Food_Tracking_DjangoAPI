import requests
from datetime import datetime
from .models import Product, OpenFoodFactsProduct

OPEN_FOOD_FACTS_URL = "https://world.openfoodfacts.org/api/v2/product/{}"


def fetch_product_by_barcode(barcode: str):
    try:
        response = requests.get(OPEN_FOOD_FACTS_URL.format(barcode), timeout=5)
    except requests.RequestException:
        return None

    if response.status_code != 200:
        return None

    data = response.json()

    if data.get("status") != 1:
        return None

    return OpenFoodFactsProduct.from_api_response(data)


def save_product_from_barcode(barcode: str):
    off_product = fetch_product_by_barcode(barcode)
    if not off_product:
        return None
    expiration_date = None
    if off_product.expiration_date:
        try:
            expiration_date = datetime.strptime(
                off_product.expiration_date, "%Y-%m-%d"
            )
        except ValueError:
            pass

    product= Product.objects.create(
        barcode=off_product.barcode,
        name= off_product.name or "Unknown product",
        image= off_product.image_url,
        brand= off_product.brand,
        ingredients= off_product.ingredients,
        calories= off_product.calories,
        fat= off_product.fat,
        sugars= off_product.sugars,
        proteins= off_product.proteins,
        salt= off_product.salt,
        expiration_date= expiration_date,
    )

    return product
