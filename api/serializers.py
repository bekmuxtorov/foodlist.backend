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
    UserProfile,
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


class OrderCreateSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    product_ids = serializers.CharField(write_only=True)
    table = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
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

    def validate_product_ids(self, value):
        try:
            ids = [int(i.strip())
                   for i in value.split(',') if i.strip().isdigit()]
            products = Product.objects.filter(id__in=ids)
            if not products.exists():
                raise serializers.ValidationError(
                    "Hech qanday mahsulot topilmadi.")
            return products
        except Exception:
            raise serializers.ValidationError(
                "Mahsulotlar ro‘yxatini noto‘g‘ri formatda yubordingiz.")

    def validate_table(self, value):
        organization = self.initial_data.get("organization")

        if not organization:
            raise serializers.ValidationError("organization maydoni kerak.")

        try:
            return Table.objects.get(number=value, organization=organization)
        except Table.DoesNotExist:
            raise serializers.ValidationError(
                f"{value} raqamli stol topilmadi yoki ushbu organizationga tegishli emas.")

    def create(self, validated_data):
        products = validated_data.pop('product_ids')   # queryset
        table_obj = validated_data.pop(
            'table')         # bu endi Table instance
        order = Order.objects.create(table=table_obj, **validated_data)
        order.products.set(products)
        return order


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


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "id",
            "phone_number",
            "full_name",
            "type",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "full_name",
            "type",
            "is_active",
            "created_at",
            "updated_at",
        )

    def validate_phone_number(self, value):
        """
        Telefon raqamining yagona ekanligini tekshiradi.
        """
        if UserProfile.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(
                "Bu telefon raqami allaqachon ro'yxatdan o'tgan. Iltimos, boshqa raqam kiriting."
            )
        return value

    def create(self, validated_data):
        """
        Yangi UserProfile obyektini yaratadi va kerakli default qiymatlarni o'rnatadi.
        """
        phone_number = validated_data["phone_number"]
        full_name = self._generate_full_name(phone_number)

        user = UserProfile.objects.create(
            phone_number=phone_number,
            full_name=full_name,
            type="customer",
            is_active=True,  # Default qiymat aniq belgilandi
        )
        return user

    def _generate_full_name(self, phone_number: str) -> str:
        """
        Telefon raqamidan foydalanib, full_name generatsiya qiladi.
        """
        return f"User {phone_number[-4:]}"
