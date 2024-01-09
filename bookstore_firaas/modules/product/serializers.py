from rest_framework import serializers

from bookstore_firaas.modules.admin.serializers import AdminSerializer
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255)
    image = serializers.ImageField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    video = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    description = serializers.CharField(max_length=255)
    is_highlighted = serializers.BooleanField()
    price = serializers.IntegerField()
    is_available = serializers.BooleanField()
    stock = serializers.IntegerField()
    create_user_id = serializers.IntegerField()
    create_user = AdminSerializer(required=False, write_only=False)
    update_user_id = serializers.IntegerField(required=False)
    update_user = AdminSerializer(required=False)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)
    deleted_at = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        print(validated_data)
        if validated_data['stock'] > 0:
            validated_data['is_available'] = True
        else:
            validated_data['is_available'] = False
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if validated_data['stock'] > 0:
            validated_data['is_available'] = True
        else:
            validated_data['is_available'] = False
        return super().update(instance, validated_data)

    class Meta:
        model = Product
        fields = ('__all__')
