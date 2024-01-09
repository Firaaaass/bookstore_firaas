from datetime import datetime

import bcrypt
from rest_framework import serializers

from bookstore_firaas.utils.response_validation_error import ResponseValidationError
from .models import Admin


class ParentAdminSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        serializer_data = AdminSerializer(value).data
        return serializer_data
    
    class Meta:
        model = Admin
        fields = ('__all__')


class AdminSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        min_length=4,
        trim_whitespace=False,
        write_only=True,
    )
    create_user_id = serializers.IntegerField()
    update_user_id = serializers.IntegerField(required=False)
    create_user = ParentAdminSerializer(required=False, write_only=False)
    update_user = ParentAdminSerializer(required=False, write_only=False)

    def validate_email(self, value):
        lower_email = value.lower()
        print(self.instance)
        if self.instance is None:
            if Admin.objects.filter(email=lower_email).exists():
                msg = 'Email is already registered.'
                raise ResponseValidationError({"status": "failed", "data": msg})
        elif self.instance.email != value:
            if Admin.objects.filter(email=lower_email).exists():
                msg = 'Email is already registered.'
                raise ResponseValidationError({"status": "failed", "data": msg})
        return lower_email
        
    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        create_user_id = validated_data['create_user_id']

        # converting password to array of bytes
        bytes = password.encode('utf-8')

        # generating the salt
        salt = bcrypt.gensalt()

        # Hashing the password
        hash = bcrypt.hashpw(bytes, salt)

        password = hash.decode('utf-8')

        user = Admin.objects.create(
            email=email,
            password=password,
            create_user_id=create_user_id
        )

        return user
    
    def update(self, instance, validated_data):
        password = validated_data.get('password', instance.password)

        instance.email = validated_data.get('email', instance.email)
        instance.update_user_id = validated_data.get('update_user_id', instance.update_user_id)
        instance.updated_at = datetime.now()

        if password is not None:
            # converting password to array of bytes
            bytes = password.encode('utf-8')

            # generating the salt
            salt = bcrypt.gensalt()

            # Hashing the password
            hash = bcrypt.hashpw(bytes, salt)

            instance.password = hash.decode('utf-8')
        
        instance.save()
        return instance
    
    class Meta:
        model = Admin
        fields = ('__all__')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }