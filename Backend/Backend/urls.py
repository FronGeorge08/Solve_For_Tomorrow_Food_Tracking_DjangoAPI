from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from UsersApp.views import UserHandler, UserHandlerWithId, RegisterView, LoginView, VerifyEmailView
from ProductsApp.views import ProductHandler, ProductHandlerWithId, is_expiring_3days
from UsersApp.authview import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

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

    # -------------------- ADMIN --------------------
    path("admin/", admin.site.urls, name="admin-panel"),

    # -------------------- API DOCS --------------------
    path("docs/", schema_view.with_ui('swagger', cache_timeout=0), name="api-docs"),

    # ==================== USERS ====================

    # Create user / list users
    path("users/", UserHandler.as_view(), name="users-list-create"),

    # Retrieve / update / delete single user
    path("users/<int:id>/", UserHandlerWithId.as_view(), name="users-detail"),

    # ==================== PRODUCTS ====================

    # Create product / list products
    path("products/", ProductHandler.as_view(), name="products-list-create"),

    # Retrieve / update / delete single product
    path("products/<int:id>/", ProductHandlerWithId.as_view(), name="products-detail"),

    # Expiring products
    path("products/expiring/", is_expiring_3days, name="products-expiring-soon"),

    # ==================== AUTH ====================

    # Register
    path("register/", RegisterView.as_view()),

    #Login
    path("login/", LoginView.as_view()),

    #Email-Verification
    path("verify-email/", VerifyEmailView.as_view()),

    # JWT Obtain
    path("auth/token/", MyTokenObtainPairView.as_view(), name="auth-token-obtain"),

    # JWT Refresh
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="auth-token-refresh"),
]