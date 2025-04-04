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
