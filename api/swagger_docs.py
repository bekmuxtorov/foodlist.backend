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


cheking_phone_number = swagger_auto_schema(
    operation_description="Send a confirmation message to the telegram bot with the phone number",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'phone_number': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Phone number',
                example='+998901234567'
            )
        },
        required=['phone_number',]
    ),
    responses={
        200: openapi.Response(
            description="This checks whether a user matching the phone number exists and returns a status of sending a confirmation message.",
            examples={
                'application/json': {
                    "exists": True,
                    "has_confirmation_message_been_sent": True
                }
            }
        ),
        400: openapi.Response(description="Invalid data"),
        404: openapi.Response(description="phone_number not found"),
    }
)

checking_token = swagger_auto_schema(
    operation_description="Checking token",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'token': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Token',
                example='asdfasdfasdfadfasdfasdfasdfasdf'
            )
        },
        required=['token',]
    ),
    responses={
        200: openapi.Response(
            description="This checks whether a user matching the token exists and returns a status of sending a confirmation message.",
            examples={
                'application/json': {
                    "user_id": 36,
                    "is_valid": True
                }
            }
        ),
        400: openapi.Response(description="Invalid data"),
        404: openapi.Response(description="token not found"),
    }
)

filter_for_table = swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'organization', openapi.IN_QUERY,
                description="Tashkilot ID", type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'search', openapi.IN_QUERY,
                description="Stol raqami bo‘yicha qidirish", type=openapi.TYPE_STRING
            ),
        ]
    )

filter_for_wifi = swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'organization', openapi.IN_QUERY,
                description="Tashkilot ID", type=openapi.TYPE_INTEGER
            ),
        ]
    )