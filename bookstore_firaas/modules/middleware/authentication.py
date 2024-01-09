from datetime import datetime, timedelta

import environ
import jwt
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError

from bookstore_firaas.modules.admin.models import Admin
from bookstore_firaas.modules.user.models import User

# reading .env file
env = environ.Env()


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Extract the JWT from the Authorization header
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            return None
        
        jwt_token = JWTAuthentication.get_the_token_from_header(jwt_token) # clean the token
        # Decode the JWT and verify its signature
        try:
            payload = jwt.decode(jwt_token, env('JWT_SECRET'), algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except:
            raise ParseError()
        
        is_admin = payload.get('is_admin')
        id = payload.get('id')

        if id is None:
            raise AuthenticationFailed('User not found')
        
        if is_admin is False:
            user = User.objects.get(id=id)

            if user is None:
                raise AuthenticationFailed('User not found')
            
            user.is_staff = False
        elif is_admin is True:
            user = Admin.objects.get(id=id)

            if user is None:
                raise AuthenticationFailed('User not found')

            user.is_staff = True

        user.is_authenticated = True

        # Return the user and token payload
        return user, payload
    
    def authenticate_header(self, request):
        return 'Bearer'
    
    @classmethod
    def create_jwt(cls, user):
        # Create the JWT payload
        payload = {
            'id': user.id,
            'exp': int((datetime.now() + timedelta(days=365)).timestamp()),
            'iat': datetime.now().timestamp(),
            'email': user.email,
            'is_admin': False
        }

        if isinstance(user, Admin):
            payload['is_admin'] = True

        # Encode the JWT with your secret key
        jwt_token = jwt.encode(payload, env('JWT_SECRET'), algorithm='HS256')

        payload['token'] = jwt_token
        return payload
    
    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace('Bearer', '').replace(' ', '') # clean the token
        return token