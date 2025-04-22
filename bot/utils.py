from rest_framework_simplejwt.tokens import AccessToken

from django.conf import settings


def create_jwt_token(user):
    access = AccessToken.for_user(user)
    return str(access)
