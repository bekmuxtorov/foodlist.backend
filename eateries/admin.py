from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib import admin
from . import models


@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'code', 'created_at', 'updated_at')
    search_fields = ('name', 'code')
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(models.WiFi)
class WiFiAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'password', 'created_at', 'updated_at')
    search_fields = ('name', 'password')
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'phone_number', 'created_at', 'updated_at')
    search_fields = ('name', 'phone_number')
    list_filter = ('created_at', 'updated_at', 'currency')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 1
    fields = ('image',)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'id',
        'price',
        'category',
        'created_at',
        'updated_at'
    )
    search_fields = (
        'name',
        'price',
        'organization__name',
        'organization__short_name'
    )
    list_filter = ('created_at', 'updated_at', 'category', 'organization')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProductImageInline]


@admin.register(models.Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'id', 'organization', 'created_at', 'updated_at')
    search_fields = ('number', 'organization')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


class ProductOrder(admin.TabularInline):
    model = models.ProductOrder
    extra = 1


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "organization",
        "table",
        "status",
        "type",
        "total_price"
    )
    search_fields = ("organization__short_name", "table__number")
    ordering = ('-created_at',)
    list_filter = (
        "organization__short_name",
        "table__number",
        "status",
        "type"
    )
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProductOrder]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = '__all__'

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            return make_password(password)
        return password


@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileForm
    list_display = ('full_name', 'id', 'phone_number',
                    'created_at', 'updated_at')
    search_fields = ('full_name', 'phone_number')
    list_filter = ('created_at', 'updated_at', 'type')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('password', 'created_at', 'updated_at')
