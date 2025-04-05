from django.shortcuts import render
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="foodlist.menu API",
        default_version='v1',
        description="Foodlist.menu is a platform that allows users to view online menus of different eateries and restaurants.",
        contact=openapi.Contact(email="asadbekmuxtorov2@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def default_page(request):
    return render(request, "index.html")


urlpatterns = [
    path("", default_page),
    path("admin3/", admin.site.urls),
    path("swagger/", schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
    path("swagger.json", schema_view.without_ui(
        cache_timeout=0), name='schema-json'),
    path("api/v1/", include("api.urls")),
]
