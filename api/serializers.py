from rest_framework import serializers
from django.utils import timezone
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
        fields = "__all__"


class WiFiSerializerForOrganization(serializers.ModelSerializer):
    class Meta:
        model = WiFi
        fields = ('id', 'name', 'password')


class OrganizationSerializer(serializers.ModelSerializer):
    currency_detail = serializers.SerializerMethodField()
    wifi_passwords = WiFiSerializerForOrganization(many=True, write_only=True)
    wifi_passwords_detail = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = "__all__"
        extra_kwargs = {
            'currency': {'write_only': True}
        }

    def get_currency_detail(self, obj):
        if obj.currency_id is None:
            return None
        return CurrencySerializer(obj.currency).data

    def get_wifi_passwords_detail(self, obj):
        wifi_qs = getattr(obj, 'wifi', None)
        if wifi_qs is None:
            return []
        return WiFiSerializerForOrganization(wifi_qs.all(), many=True).data

    def create(self, validated_data):
        wifi_data = validated_data.pop('wifi_passwords', [])
        organization = super().create(validated_data)
        WiFi.objects.bulk_create([
            WiFi(organization=organization, **wifi)
            for wifi in wifi_data
        ])
        return organization


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = ProductImage
        fields = ['image', ]


class ProductSerializer(serializers.ModelSerializer):
    category_detail = serializers.SerializerMethodField(read_only=True)
    images_detail = serializers.SerializerMethodField(read_only=True)
    images = ProductImageSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Product
        fields = [
            'id',
            'organization',
            'name',
            'description',
            'weight',
            'price',
            'images',
            'category',
            'is_active',
            'category_detail',
            'images_detail'
        ]
        extra_kwargs = {
            'category': {'write_only': True}
        }
        read_only_fields = ('category_detail', 'images_detail')

    def get_category_detail(self, obj):
        if obj.category_id is None:
            return None
        return CategorySerializer(obj.category).data

    def get_images_detail(self, obj):
        images_qs = getattr(obj, 'images', None)
        if images_qs is None:
            return []
        return ProductImageSerializer(obj.images.all(), many=True).data

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        product = super().create(validated_data)

        if images_data:
            ProductImage.objects.bulk_create([
                ProductImage(product=product, image=image_data['image'])
                for image_data in images_data
            ])

        return product


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
    phone_number = serializers.CharField(
        source='user.phone_number', read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'phone_number',
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


class CheckTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)

    def validate_token(self, value):
        try:
            user = UserProfile.objects.get(auth_token=value)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError(
                "Token noto'g'ri yoki mavjud emas.")

        if user.token_expiry < timezone.now():
            user.is_active = False
            user.save()
            raise serializers.ValidationError("Token muddati o'tgan.")

        # foydalanuvchini kontekstda saqlab qolamiz
        self.context['user'] = user
        return value
