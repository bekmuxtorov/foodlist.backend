from rest_framework import serializers
from eateries.models import (
    Currency,
    WiFi,
    Organization,
    Category,
    Product,
    Table,
    Order,
    ProductImage,
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
    currency_detail = CurrencySerializer(source='currency', read_only=True)
    wifi_password_detail = WiFiSerializer(
        source='wifi_password', read_only=True)

    class Meta:
        model = Organization
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', ]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"
        read_only_fields = ["qr_code"]


class TableCreateCollectionSerializer(serializers.Serializer):
    organization_id = serializers.IntegerField(required=True)
    table_count = serializers.IntegerField(min_value=1, required=True)


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        many=True,
        write_only=True,
        source='products'
    )

    class Meta:
        model = Order
        fields = (
            'id',
            'created_at',
            'updated_at',
            'status',
            'total_price',
            'organization',
            'table',
            'type',
            'products',
            'product_ids'
        )
