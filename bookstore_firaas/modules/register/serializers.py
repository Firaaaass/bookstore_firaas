import bcrypt
from rest_framework import serializers

from bookstore_firaas.modules.user.models import User
from bookstore_firaas.utils.response_validation_error import ResponseValidationError


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        write_only=True
    )
    name = serializers.CharField(
        write_only=True
    )
    password = serializers.CharField(
        min_length=4,
        trim_whitespace=False,
        write_only=True,
    )
    
    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email=lower_email).exists():
            msg = 'Email is already registered.'
            raise ResponseValidationError({"status": "failed", "data": msg})
        return lower_email
        
    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        name = validated_data['name']

        # converting password to array of bytes
        bytes = password.encode('utf-8')

        # generating the salt
        salt = bcrypt.gensalt()

        # Hashing the password
        hash = bcrypt.hashpw(bytes, salt)

        password = hash.decode('utf-8')

        user = User.objects.create(
            email=email,
            password=password,
            name=name,
        )

        return user
    
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'name') 
        