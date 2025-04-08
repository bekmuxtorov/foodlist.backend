from django.urls import path
from api.views import (
    CurrencyListAPIView,
    WiFiListAPIView,
    WiFiCreateAPIView,
    WiFiUpdateAPIView,
    WiFiDestroyAPIView,
    OrganizationRetrieveAPIView,
    OrganizationCreateAPIView,
    OrganizationUpdateAPIView,
    CategoryListAPIView,
    CategoryRetrieveAPIView,
    ProductCreateAPIView,
    ProductListAPIView,
    ProductDetailAPIView,
    ProductUpdateAPIView,
    ProductDestroyAPIView,
    TableListAPIView,
    TableDetailAPIView,
    TableUpdateAPIView,
    TableDestroyAPIView,
    TableCreateCollectionAPIView,
    OrderCreateAPIView,
    OrderListAPIView,
    OrderDetailAPIView,
    OrderDestroyAPIView,
    OrderUpdateAPIView
)

urlpatterns = [
    path(
        "currensies/",
        CurrencyListAPIView.as_view()
    ),

    # WiFi
    path(
        "wifi/",
        WiFiListAPIView.as_view()
    ),
    path(
        "wifi/create/",
        WiFiCreateAPIView.as_view()
    ),
    path(
        "wifi/update/<int:pk>/",
        WiFiUpdateAPIView.as_view()
    ),
    path(
        "wifi/delete/<int:pk>/",
        WiFiDestroyAPIView.as_view()
    ),

    # Organization
    path(
        "organizations/create/",
        OrganizationCreateAPIView.as_view()
    ),
    path(
        "organizations/<int:pk>/",
        OrganizationRetrieveAPIView.as_view()
    ),
    path(
        "organizations/update/<int:pk>/",
        OrganizationUpdateAPIView.as_view()
    ),

    # Category
    path(
        "categories/",
        CategoryListAPIView.as_view()
    ),
    path(
        "categories/<int:pk>/",
        CategoryRetrieveAPIView.as_view()
    ),

    # Product
    path(
        "products/create/",
        ProductCreateAPIView.as_view()
    ),
    path(
        "products/",
        ProductListAPIView.as_view()
    ),
    path(
        "products/<int:pk>/",
        ProductDetailAPIView.as_view()
    ),
    path(
        "products/update/<int:pk>/",
        ProductUpdateAPIView.as_view()
    ),
    path(
        "products/delete/<int:pk>/",
        ProductDestroyAPIView.as_view()
    ),

    # Table
    path(
        "tables/create_collection/",
        TableCreateCollectionAPIView.as_view()
    ),
    path(
        "tables/",
        TableListAPIView.as_view()
    ),
    path(
        "tables/<int:pk>/",
        TableDetailAPIView.as_view()
    ),
    path(
        "tables/update/<int:pk>/",
        TableUpdateAPIView.as_view()
    ),
    path(
        "tables/delete/<int:pk>/",
        TableDestroyAPIView.as_view()
    ),

    # Order
    path(
        "orders/create/",
        OrderCreateAPIView.as_view()
    ),
    path(
        "orders/",
        OrderListAPIView.as_view()
    ),
    path(
        "orders/<int:pk>/",
        OrderDetailAPIView.as_view()
    ),
    path(
        "orders/update/<int:pk>/",
        OrderUpdateAPIView.as_view()
    ),
    path(
        "orders/delete/<int:pk>/",
        OrderDestroyAPIView.as_view()
    ),
]
