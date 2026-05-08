import jwt
from django.conf import settings
from datetime import timedelta, datetime
from rest_framework.response import Response


def generate_access_token(user):
    payload = {
        'user_id': user.id,
        'user_email': user.email,
        'exp': datetime.now() + timedelta(minutes=15),
        'iat': datetime.now(),
        'type': 'access'
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HSA256')


def generate_refresh_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.now() + timedelta(days=7),
        'iat': datetime.now(),
        'type': 'refresh'
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HSA256')