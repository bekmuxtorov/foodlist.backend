from django.db import models
from django.core.validators import RegexValidator


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Currency(BaseModel):
    name = models.CharField(
        max_length=255,
        verbose_name='Name'
    )
    code = models.CharField(
        max_length=3,
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
        upload_to="media/qr_codes/",
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
    name = models.CharField(
        max_length=255,
        verbose_name='Name'
    )
    logo = models.ImageField(
        upload_to="media/logos/",
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
        related_name='wifi_password',
        blank=True,
        null=True
    )
    wallpaper = models.ImageField(
        upload_to="media/wallpapers/",
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
        upload_to="media/categories/",
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
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Weight',
        blank=True,
        null=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Price'
    )
    image = models.ImageField(
        upload_to="media/products/",
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

    def __str__(self) -> str:
        return " | ".join([self.name, str(self.price)])

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


"""
	- Kategoriya
	[
		- nomi
		- rasmi
	]

	- Mahsulot
	[
		- status(qoldi/qomadi)
		- nomi
		- description
		- Og'irlik(g)(r)
		- narxi
		- rasm[bir nechta(max 3ta)]
		- kategoriya[FK Kategoriya]
		// - Chegirma(Boolean)
		   - Chegirma turi[Yo'q, Foiz, sovg'a]
			- chegirma_foizi(int)
			- sovga(FK Mahsulot)
		- during_time
	]

	- Stollar
		- nomeri
		- qr_code(rasm)
		 // - o'rindiqlar soni
		-

	Buyurtmalar
		- stol nomer
		- status[kutulmoqda, tayyorlandi, yetkizildi]
		- vaqti
		- taomlar[ManyToMany]
		- narxi
		// - loyality(phone_number)


"""
