from django import views

from django.shortcuts import render


def home(request):
    return render(request, "dashboard.html")


def organization(request):
    return render(request, "organization.html")
