from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from django.conf import settings
from django.contrib.auth.models import User
import jwt

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = str(request.headers.get('Authorization'))

        if not auth_header or not auth_header.startswith('Bearer '):
            return None # not authenticated as there is no Bearer token in auth header
        
        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token Expired!')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token!')
        
        
        if payload.get('type') != 'access':
            raise AuthenticationFailed('Expected an access token!')
        
        try: 
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            raise ('User does not exist!')
        
        return (user, payload)
    

    ## login, profile, crud tasks, otp generation, otp resend, otp verification, register, 