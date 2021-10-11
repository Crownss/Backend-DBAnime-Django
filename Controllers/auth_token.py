from Models.models import User
import jwt
from rest_framework import authentication
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

class JWT_AUTH(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)
        if not auth_data:
            return None
        
        token, created=auth_data.decode('utf-8').split(' ')
        print(token, auth_data, created)
        try:
            payload=jwt.decode(created, settings.SECRET_KEY, algorithms='HS256')
            user=User.objects.get(id=payload['id'])
            return user, created
        except jwt.InvalidSignatureError:
            raise AuthenticationFailed('The token is invalid')
        except jwt.DecodeError:
            raise AuthenticationFailed('Decoding is invalid')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('The token is invalid')
        return super().authenticate(request)