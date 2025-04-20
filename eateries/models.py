from django.utils import timezone
from datetime import timedelta, datetime
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.core.validators import RegexValidator

from .managers import UserManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(BaseModel):
    USER_TYPES = [
        ('manager', 'Meneger'),
        ('customer', 'Mijoz'),
    ]
    type = models.CharField(
        max_length=10,
        choices=USER_TYPES,
        default='customer'
    )
    full_name = models.CharField(
        verbose_name="Full name",
        max_length=255,
        blank=True,
        null=True,
    )
    phone_number = models.CharField(
        max_length=13,
        verbose_name='Phone number',
        validators=[
            RegexValidator(
                regex=r'^\+?\d{1,4}[\s-]?\(?\d{1,4}\)?[\s-]?\d{1,12}([\s-]?\d{1,12})?$',
                message=(
                    "Invalid phone number."
                )
            ),
        ],
        unique=True
    )
    telegram_id = models.CharField(
        max_length=20,
        verbose_name='Telegram ID',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Is active'
    )
    sms_code = models.CharField(
        max_length=6,
        verbose_name='SMS code',
        blank=True,
        null=True
    )
    password = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    auth_token = models.CharField(
        max_length=255,
        verbose_name='Auth Token',
        blank=True,
        null=True
    )
    token_expiry = models.DateTimeField(
        verbose_name="Token Expiry",
        blank=True,
        null=True
    )

    def set_token_expiry(self, hours):
        self.token_expiry = timezone.now() + timedelta(hours=hours)

    def is_token_valid(self):
        if self.token_expiry and self.token_expiry > timezone.now():
            return True
        return False

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    # def __str__(self) -> str:
    #     return " | ".join([self.id, self.phone_number])

    objects = UserManager()

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'
        ordering = ['-created_at']


class Currency(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name='Name'
    )
    code = models.CharField(
        max_length=8,
        verbose_name='Code'
    )

    def __str__(self) -> str:
        return " | ".join([self.name, self.code])

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'


class WiFi(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name='Name'
    )
    password = models.CharField(
        max_length=255,
        verbose_name='Password'
    )
    qr_code = models.ImageField(
        upload_to="qr_codes/",
        verbose_name='QR code',
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Wi-Fi password'
        verbose_name_plural = 'Wi-Fi passwords'


class Organization(BaseModel):
    user = models.ForeignKey(
        to=UserProfile,
        on_delete=models.CASCADE,
        verbose_name='User',
        related_name='organizations'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Name'
    )
    logo = models.ImageField(
        upload_to="logos/",
        verbose_name='Logo',
        blank=True,
        null=True
    )
    short_name = models.CharField(
        max_length=50,
        verbose_name='Short name'
    )
    currency = models.ForeignKey(
        to=Currency,
        on_delete=models.CASCADE,
        verbose_name='Currency'
    )
    phone_number = models.CharField(
        max_length=13,
        verbose_name='Phone number',
        validators=[
            RegexValidator(
                regex=r'^\+?\d{1,4}[\s-]?\(?\d{1,4}\)?[\s-]?\d{1,12}([\s-]?\d{1,12})?$',
                message=(
                    "Invalid phone number.")
            ),
        ]
    )
    address = models.CharField(
        max_length=255,
        verbose_name='Address'
    )
    wifi_password = models.ForeignKey(
        to=WiFi,
        on_delete=models.CASCADE,
        verbose_name='Wi-Fi password',
        related_name='organizations',
        blank=True,
        null=True
    )
    wallpaper = models.ImageField(
        upload_to="wallpapers/",
        verbose_name='Wallpaper',
        blank=True,
        null=True
    )
    service_fee = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Service fee'
    )
    description = models.TextField(
        verbose_name='Description',
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return " | ".join([self.short_name, self.phone_number])

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'


class Category(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name='Name'
    )
    image = models.ImageField(
        upload_to="categories/",
        verbose_name='Image',
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(BaseModel):
    organization = models.ForeignKey(
        to=Organization,
        on_delete=models.CASCADE,
        verbose_name='Organization',
        related_name='products'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Name'
    )
    description = models.TextField(
        verbose_name='Description',
        blank=True,
        null=True
    )
    weight = models.CharField(
        verbose_name="Weight text",
        max_length=128,
        blank=True,
        null=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Price'
    )
    image = models.ImageField(
        upload_to="products/",
        verbose_name='Image',
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        verbose_name='Category',
        related_name='products'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Is active'
    )

    def __str__(self) -> str:
        return " | ".join([self.name, str(self.price)])

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Table(BaseModel):
    organization = models.ForeignKey(
        to=Organization,
        on_delete=models.CASCADE,
        verbose_name='Organization',
        related_name='tables'
    )
    number = models.CharField(
        max_length=255,
        verbose_name='Number'
    )
    qr_code = models.ImageField(
        upload_to="qr_codes/",
        verbose_name='QR code',
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return self.number

    class Meta:
        verbose_name = 'Table'
        verbose_name_plural = 'Tables'


class ProductOrder(BaseModel):
    order = models.ForeignKey(
        to='Order',
        on_delete=models.CASCADE,
        verbose_name='Order',
        related_name='product_orders'
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        verbose_name='Product',
        related_name='product_orders'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Quantity'
    )

    def __str__(self) -> str:
        return " | ".join([self.product.name, str(self.quantity)])

    class Meta:
        unique_together = ('order', 'product')
        verbose_name = 'Product order'
        verbose_name_plural = 'Product orders'


class Order(BaseModel):
    user = models.ForeignKey(
        to=UserProfile,
        verbose_name='User',
        related_name='orders',
        on_delete=models.CASCADE,
    )
    organization = models.ForeignKey(
        to=Organization,
        verbose_name="Organization",
        related_name="orders",
        on_delete=models.CASCADE,
    )
    type = models.CharField(
        verbose_name="Type",
        max_length=10,
        choices=[
            ('on_table', 'Dine in'),
            ('take_away', 'Take away'),
        ],
        default='on_table'
    )
    table = models.ForeignKey(
        to=Table,
        verbose_name="Table",
        related_name="orders",
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=255,
        verbose_name='Status',
        choices=[
            ('waiting', 'Waiting'),
            ('ready', 'Ready'),
            ('delivered', 'Delivered')
        ],
        default='waiting'
    )
    products = models.ManyToManyField(
        to=Product,
        verbose_name='Products',
        related_name='orders'
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Total price'
    )

    def __str__(self):
        return " | ".join([self.organization.short_name, self.table.number])

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class ProductImage(BaseModel):
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        verbose_name='Product',
        related_name='images'
    )
    image = models.ImageField(
        upload_to="images/",
        verbose_name='Image',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
