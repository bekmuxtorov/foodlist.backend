from rest_framework_simplejwt.authentication import JWTAuthentication
from eateries.models import UserProfile
from rest_framework.exceptions import AuthenticationFailed


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token.get('user_id')
            user = UserProfile.objects.get(id=user_id)
            if not user.is_active:
                raise AuthenticationFailed('User is not active')
            return user
        except UserProfile.DoesNotExist:
            raise AuthenticationFailed('No such user exists')
        except Exception as e:
            raise AuthenticationFailed(str(e))
