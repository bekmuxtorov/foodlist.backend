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
    ProductOrder,
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


class ProductOrderSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    category = CategorySerializer(source='product.category', read_only=True)
    images = ProductImageSerializer(
        source='product.images', many=True, read_only=True)
    price = serializers.DecimalField(
        source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = ProductOrder
        fields = ['product', 'product_name',
                  'category', 'images', 'price', 'quantity']


class OrderCreateSerializer(serializers.ModelSerializer):
    table_number = serializers.IntegerField(write_only=True)
    table = TableSerializer(read_only=True)
    product_orders = ProductOrderSerializer(many=True, write_only=True)
    full_product_orders = ProductOrderSerializer(
        many=True, read_only=True, source='product_orders')

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
            'table_number',
            'table',
            'type',
            'product_orders',
            'full_product_orders',
        )

    # def validate_product_orders(self, value):
    #     try:
    #         ids = [int(i.strip())
    #                for i in value.split(',') if i.strip().isdigit()]
    #         products = Product.objects.filter(id__in=ids)
    #         if not products.exists():
    #             raise serializers.ValidationError(
    #                 "Hech qanday mahsulot topilmadi.")
    #         return products
    #     except Exception:
    #         raise serializers.ValidationError(
    #             "Mahsulotlar ro‘yxatini noto‘g‘ri formatda yubordingiz.")

    def validate_table_number(self, value):
        organization = self.initial_data.get("organization")

        if not organization:
            raise serializers.ValidationError("organization maydoni kerak.")

        try:
            return Table.objects.get(number=value, organization=organization)
        except Table.DoesNotExist:
            raise serializers.ValidationError(
                f"{value} raqamli stol topilmadi yoki ushbu organizationga tegishli emas.")

    def create(self, validated_data):
        table_number = validated_data.pop('table_number')
        organization = validated_data.pop('organization')
        table_obj = Table.objects.filter(
            number=table_number, organization=organization).first()
        product_orders_data = validated_data.pop('product_orders')
        order = Order.objects.create(
            table=table_obj,
            organization=organization,
            **validated_data
        )
        for po_data in product_orders_data:
            ProductOrder.objects.create(order=order, **po_data)

        return order


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            "id",
            "phone_number",
            "full_name",
            "type",
            "auth_token",
            "token_expiry",
            "is_active",
            "telegram_id",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "full_name",
            "type",
            "auth_token",
            "token_expiry",
            "is_active",
            "telegram_id",
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


class PhoneCheckSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13)

    def validate_phone_number(self, value):
        phone_number = value.replace("+", "")
        if not phone_number.isdigit():
            raise serializers.ValidationError(
                "Telefon raqami faqat raqamlardan iborat bo'lishi kerak.")
        if len(phone_number) != 12:
            raise serializers.ValidationError(
                "Telefon raqami 13 ta raqamdan iborat bo'lishi kerak.")
        return value
