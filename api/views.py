from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters import rest_framework as filters

from api.serializers import (
    CurrencySerializer,
    WiFiSerializer,
    OrganizationSerializer,
    CategorySerializer,
    ProductSerializer
)
from eateries.models import (
    Currency,
    WiFi,
    Organization,
    Category,
    Product
)


# < ========= Currency ========= >
class CurrencyListAPIView(ListAPIView):
    serializer_class = CurrencySerializer
    queryset = Currency.objects.all()


# < ========= WiFi ========= >
class WiFiCreateAPIView(CreateAPIView):
    serializer_class = WiFiSerializer
    queryset = WiFi.objects.all()
    parser_classes = (MultiPartParser, FormParser)


class WiFiListAPIView(ListAPIView):
    serializer_class = WiFiSerializer
    queryset = WiFi.objects.all()
    parser_classes = (MultiPartParser, FormParser)


class WiFiUpdateAPIView(UpdateAPIView):
    serializer_class = WiFiSerializer
    queryset = WiFi.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class WiFiDestroyAPIView(DestroyAPIView):
    serializer_class = WiFiSerializer
    queryset = WiFi.objects.all()


# < ========= Organization ========= >
class OrganizationCreateAPIView(CreateAPIView):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    parser_classes = (MultiPartParser, FormParser)


class OrganizationRetrieveAPIView(RetrieveAPIView):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    parser_classes = (MultiPartParser, FormParser)


class OrganizationUpdateAPIView(UpdateAPIView):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


# < ========= Category ========= >
class CategoryListAPIView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    parser_classes = (MultiPartParser, FormParser)


class CategoryRetrieveAPIView(RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    parser_classes = (MultiPartParser, FormParser)


# < ========= Product ========= >
class ProductCreateAPIView(CreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    parser_classes = (MultiPartParser, FormParser)


class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    filterset_fields = ("organization", "category")
    search_fields = ("name", "description")


class ProductDetailAPIView(RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    parser_classes = (MultiPartParser, FormParser)


class ProductUpdateAPIView(UpdateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class ProductDestroyAPIView(DestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
