from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from bot.bot import send_confirmation_message_to_user
from .utils import create_qr_code_for_tables, safe_filename
from .swagger_docs import table_create_schema, table_in_organization, cheking_phone_number
from api.serializers import (
    CurrencySerializer,
    WiFiSerializer,
    OrganizationSerializer,
    CategorySerializer,
    ProductSerializer,
    TableSerializer,
    TableCreateCollectionSerializer,
    OrderCreateSerializer,
    UserCreateSerializer,
    PhoneCheckSerializer,
    CheckTokenSerializer,
)
from eateries.models import (
    Currency,
    WiFi,
    Organization,
    Category,
    Product,
    Table,
    Order,
    UserProfile,
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

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class ProductDestroyAPIView(DestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


# < ========= Table ========= >
class TableCreateCollectionAPIView(APIView):
    @table_create_schema
    def post(self, request):
        serializer = TableCreateCollectionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        organization_id = serializer.validated_data['organization_id']
        table_count = serializer.validated_data['table_count']

        organization = Organization.objects.filter(id=organization_id).first()
        if not organization:
            return Response({"error": "Organization not found"}, status=404)

        short_name = safe_filename(
            organization.short_name or f"org_{organization.id}")
        created_tables = []

        for table_number in range(1, int(table_count) + 1):
            table, _ = Table.objects.get_or_create(
                organization=organization,
                number=table_number
            )

            qr_code_path = create_qr_code_for_tables(
                short_name, str(table_number))
            table.qr_code = qr_code_path
            table.save()

            created_tables.append({
                "id": table.id,
                "number": table.number,
                "qr_code": request.build_absolute_uri(table.qr_code.url)
                if hasattr(table.qr_code, 'url') else table.qr_code
            })

        return Response({
            "tables": created_tables
        },
            status=200
        )

    def get_queryset(self):
        return Table.objects.all()


class TableListAPIView(ListAPIView):
    serializer_class = TableSerializer
    queryset = Table.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    filterset_fields = ("organization",)
    search_fields = ("number",)


class TableDetailAPIView(RetrieveAPIView):
    serializer_class = TableSerializer
    queryset = Table.objects.all()
    parser_classes = (MultiPartParser, FormParser)


class TableUpdateAPIView(UpdateAPIView):
    serializer_class = TableSerializer
    queryset = Table.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class TableDestroyAPIView(DestroyAPIView):
    serializer_class = TableSerializer
    queryset = Table.objects.all()


class TableInOrganization(APIView):
    def get_queryset(self):
        return Organization.objects.all()

    @table_in_organization
    def get(self, request, short_name):
        table_number = request.GET.get('t')
        organization = self.get_queryset().filter(
            short_name=short_name
        ).first()
        if not organization:
            return Response({"error": "Organization not found"}, status=404)
        organization_serializer = OrganizationSerializer(
            organization, context={"request": request})

        table = organization.tables.filter(
            number=table_number
        ).first()
        if not table:
            return Response({"error": "Table not found"}, status=404)
        table_serializer = TableSerializer(table, context={"request": request})

        products = table.organization.products.filter(
            is_active=True
        ).order_by("category__name")
        product_serializer = ProductSerializer(
            instance=products,
            many=True,
            context={"request": request}
        )

        return Response(
            {
                "organization": organization_serializer.data,
                "table": table_serializer.data,
                "products": product_serializer.data
            }
        )


# < ========= Order ========= >
class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer


class OrderListAPIView(ListAPIView):
    serializer_class = OrderCreateSerializer
    queryset = Order.objects.all().order_by('-created_at')
    filterset_fields = ("organization", "table", "status", "type", "user")
    search_fields = ("organization__short_name", "table__number")


class OrderDetailAPIView(RetrieveAPIView):
    serializer_class = OrderCreateSerializer
    queryset = Order.objects.all()
    parser_classes = (MultiPartParser, FormParser)


class OrderUpdateAPIView(UpdateAPIView):
    serializer_class = OrderCreateSerializer
    queryset = Order.objects.all()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class OrderDestroyAPIView(DestroyAPIView):
    serializer_class = OrderCreateSerializer
    queryset = Order.objects.all()


class OrganizationCategoryListAPIView(APIView):
    def get_queryset(self):
        return Category.objects.all()

    def get(self, request, pk):
        organization = Organization.objects.filter(id=pk).first()
        if not organization:
            return Response({"error": "Organization not found"}, status=404)

        categories = Category.objects.filter(
            products__organization=organization
        ).distinct()
        serializer = CategorySerializer(
            categories, many=True, context={"request": request}
        )
        return Response(serializer.data)


class UserCreateAPIView(CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


class UserDetailAPIView(RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserCreateSerializer


class PhoneCheckAPIView(APIView):
    permission_classes = [AllowAny]

    def get_queryset(self):
        return UserProfile.objects.all()

    @cheking_phone_number
    def post(self, request):
        serializer = PhoneCheckSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data["phone_number"]
            user, created = UserProfile.objects.get_or_create(
                phone_number=phone_number
            )
            if not created:
                send_confirmation_message_to_user(user_id=user.telegram_id)
                return Response({"user_id": user.id, "exists": True, "has_confirmation_message_been_sent": True})
            else:
                return Response({"user_id": user.id, "exists": False, "has_confirmation_message_been_sent": False})
        return Response(serializer.errors, status=400)


class CheckTokenAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CheckTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.context['user']
            return Response({
                "is_valid": True,
                "user_id": user.id
            }, status=status.HTTP_200_OK)

        return Response({
            "is_valid": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
