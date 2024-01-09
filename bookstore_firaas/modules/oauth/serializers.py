import bcrypt
from rest_framework import serializers

from bookstore_firaas.modules.admin.models import Admin
from bookstore_firaas.modules.admin.serializers import AdminSerializer
from bookstore_firaas.modules.user.models import User
from bookstore_firaas.utils.response_validation_error import ResponseValidationError
from .models import OauthClient, OauthAccessToken, OauthRefreshToken


class OauthSerializer(serializers.Serializer):
    email = serializers.CharField(
        label="Email",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    client_id = serializers.CharField(
        label="client_id",
        write_only=True
    )
    client_secret = serializers.CharField(
        label="client_secret",
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        client_id = attrs.get('client_id')
        client_secret = attrs.get('client_secret')

        if email and password:
            oauthClient = OauthClient.objects.filter(client_id=client_id, client_secret=client_secret).first()

            if oauthClient is None:
                msg = 'client id or client secret is invalid.'
                raise ResponseValidationError({"status": "failed", "data": msg})
            else:
                user = None

                # Web
                if oauthClient.client_id == "1":
                    # Check email user
                    user = User.objects.filter(email=email).first()

                    if user is None:
                        msg = 'Email or password is invalid.'
                        raise ResponseValidationError({"status": "failed", "data": msg})
                elif oauthClient.client_id == "2":
                    # Check email admin
                    user = Admin.objects.filter(email=email).first()

                    if user is None:
                        msg = 'Email or password is invalid.'
                        raise ResponseValidationError({"status": "failed", "data": msg})

                # encoding user password
                userBytes = password.encode('utf-8')

                # checking password
                passwordHash = bcrypt.checkpw(userBytes, user.password.encode('utf-8'))

                if passwordHash is False:
                    msg = 'Email or password is invalid.'
                    raise ResponseValidationError({"status": "failed", "data": msg})

        else:
            raise ResponseValidationError({
                "status": "failed",
                "message": "Both email and password are required.",
            })

        attrs['user'] = user
        return attrs


class OauthClientTokenSerializer(serializers.ModelSerializer):
    client_id = serializers.CharField(max_length=255)
    client_secret = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    redirect = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    scope = serializers.CharField(max_length=255)
    create_user = AdminSerializer(required=False, write_only=False)
    update_user = AdminSerializer(required=False)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)
    deleted_at = serializers.DateTimeField(required=False)

    class Meta:
        model = OauthClient
        fields = ('__all__')


class OauthAccessTokenSerializer(serializers.ModelSerializer):
    oauth_client_id = serializers.IntegerField()
    oauth_client = OauthClientTokenSerializer(required=False, write_only=False)
    user_id = serializers.IntegerField()
    token = serializers.CharField()
    scope = serializers.CharField(max_length=255)
    create_user = AdminSerializer(required=False, write_only=False)
    update_user = AdminSerializer(required=False)
    expired_at = serializers.DateTimeField(required=False)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)
    deleted_at = serializers.DateTimeField(required=False)

    class Meta:
        model = OauthAccessToken
        fields = ('__all__')


class OauthRefreshTokenSerializer(serializers.ModelSerializer):
    oauth_access_token_id = serializers.IntegerField()
    oauth_access_token = OauthAccessTokenSerializer(required=False, write_only=False)
    user_id = serializers.IntegerField()
    token = serializers.CharField()
    expired_at = serializers.DateTimeField(required=False)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)
    deleted_at = serializers.DateTimeField(required=False)

    class Meta:
        model = OauthRefreshToken
        fields = ('__all__')
