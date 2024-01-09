import secrets
from datetime import datetime, timedelta

from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from bookstore_firaas.modules.middleware.authentication import JWTAuthentication
from bookstore_firaas.modules.oauth.serializers import OauthSerializer, OauthAccessTokenSerializer, OauthRefreshTokenSerializer


@permission_classes((permissions.AllowAny,))
class OauthViews(APIView):

    def post(self, request):
        # Check login
        serializer = OauthSerializer(data=self.request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Generate JWT
            jwt_token = JWTAuthentication.create_jwt(user)

            # Insert to oauth access token table
            dataOauthAccessToken = {
                'oauth_client_id': self.request.data['client_id'],
                'user_id': user.id,
                'token': jwt_token['token'],
                'scope': "*",
                'expired_at': datetime.fromtimestamp(jwt_token['exp'])
            }

            serializerOauthAccessToken = OauthAccessTokenSerializer(data=dataOauthAccessToken)

            if serializerOauthAccessToken.is_valid():
                saveOauthAccessToken = serializerOauthAccessToken.save()

                # Insert to oauth refresh token table
                dataOauthRefreshToken = {
                    'oauth_access_token_id': saveOauthAccessToken.id,
                    'user_id': user.id,
                    'token': secrets.token_hex(64),
                    'scope': "*",
                    'expired_at': datetime.now() + timedelta(days=366)
                }

                serializerOauthRefreshToken = OauthRefreshTokenSerializer(data=dataOauthRefreshToken)

                if serializerOauthRefreshToken.is_valid():
                    serializerOauthRefreshToken.save()
                else:
                    print(serializerOauthRefreshToken.errors)
            else:
                print(serializerOauthAccessToken.errors)

            return Response({'status': 'success', "data": {
                "access_token": jwt_token['token'],
                "refresh_token": dataOauthRefreshToken['token'],
                "expired_at": jwt_token['exp'],
                "token_type": "Bearer"
            }}, status=200)
        else:
            return Response({'status': 'failed', "data": serializer.errors}, status=400)
