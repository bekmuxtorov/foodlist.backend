import jwt
from datetime import datetime, timedelta
from django.conf import settings


def create_jwt_token(user, hours=1):
    payload = {
        'user_id': user.id,
        'exp': datetime.now() + timedelta(hours=hours),
        'iat': datetime.now(),
    }
    secret_key = settings.SECRET_KEY

    token = jwt.encode(payload, secret_key, algorithm=settings.JWT_ALGORITHM)
    return token


def decode_jwt_token(token):
    try:
        secret_key = settings.SECRET_KEY

        payload = jwt.decode(token, secret_key, algorithms=[
                             settings.JWT_ALGORITHM])
        return payload

    except jwt.ExpiredSignatureError:
        raise Exception("Tokenning muddati o'tgan.")
    except jwt.InvalidTokenError:
        raise Exception("Noto'g'ri token.")
