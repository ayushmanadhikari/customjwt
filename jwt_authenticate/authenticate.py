from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from django.conf import settings
from django.contrib.auth.models import User
import jwt

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(request):
        auth_header = str(request.header.get('Authorization'))

        if not auth_header or not auth_header.startswith('Bearer '):
            return None # not authenticated as there is no Bearer token in auth header
        
        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HSA256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired!')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token!')
        
        
        if payload.get('type') != 'access':
            raise AuthenticationFailed('Expected an access token!')
        
        try: 
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            raise AuthenticationFailed('User does not exist!')
        
        return (user, payload)