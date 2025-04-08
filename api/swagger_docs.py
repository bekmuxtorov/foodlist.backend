from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

table_create_schema = swagger_auto_schema(
    operation_description="Create tables and generate QR codes for them",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'organization_id': openapi.Schema(
                type=openapi.TYPE_INTEGER, description='The ID of the organization'),
            'table_count': openapi.Schema(
                type=openapi.TYPE_INTEGER, description='The number of tables to create'),
        },
        required=['organization_id', 'table_count']
    ),
    manual_parameters=[
        openapi.Parameter(
            'table_number',
            openapi.IN_QUERY,
            description="Stol raqami",
            type=openapi.TYPE_INTEGER
        )
    ],
    responses={
        200: openapi.Response(
            description="Tables created successfully",
            examples={
                'application/json': {
                    "message": "5 ta table yaratildi",
                    "tables": [
                        {"id": 1, "number": 1,
                            "qr_code": "http://localhost:8000/media/qr_codes/qr_orgname_1.png"},
                        # boshqa stollar ro'yxati
                    ]
                }
            }
        ),
        400: openapi.Response(description="Invalid data"),
        404: openapi.Response(description="Organization not found"),
    }
)

table_in_organization = swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            't',
            openapi.IN_QUERY,
            description="Stol raqami",
            type=openapi.TYPE_INTEGER
        )
    ]
)
