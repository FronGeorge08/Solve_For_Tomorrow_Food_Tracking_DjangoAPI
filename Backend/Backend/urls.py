"""
URL configuration for Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from UsersApp.views import UserHandler,UserHandlerWithId
from ProductsApp.views import ProductHandler,ProductHandlerWithId
from ProductsApp.views import is_expiring_3days
from UsersApp.authview import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
schema_view = get_schema_view(
    openapi.Info(
        title="Your API",
        default_version="v1",
        description="API documentation for your project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="youremail@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name="schema-swagger-ui"),

    path("user/", UserHandler.as_view(), name="user"),
    path("user_with_id/<str:id>",UserHandlerWithId.as_view(),name="user_ID"),

    path("product/", ProductHandler.as_view(), name="product"),                     # POST (create) & GET (all)
    path("product/<int:id>/", ProductHandlerWithId.as_view(), name="product_id"),  # GET/PUT/DELETE by ID
    path("get_expiring/",is_expiring_3days,name='get_expiring_products'),

    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
