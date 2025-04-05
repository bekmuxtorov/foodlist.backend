from rest_framework import serializers
from eateries.models import (
    Currency,
    WiFi,
    Organization,
    Category,
    Product,
    Table,
)


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"


class WiFiSerializer(serializers.ModelSerializer):
    qr_code = serializers.ImageField(
        max_length=None, use_url=True
    )

    class Meta:
        model = WiFi
        fields = ("id", "name", "password", "qr_code")


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"
        read_only_fields = ["qr_code"]
