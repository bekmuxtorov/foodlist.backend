from django.urls import path, include

from .views import pages

urlpatterns = [
    path("dashboard/", pages.home, name="home"),
    path("organization/", pages.organization, name="organization"),
]
