from datetime import datetime

from django.db import models

from bookstore_firaas.modules.admin.models import Admin
from bookstore_firaas.utils.upload import upload_to


class Product(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=upload_to("products/"))
    video = models.FileField(upload_to=upload_to("products/"))
    description = models.CharField(max_length=255)
    is_highlighted = models.BooleanField()
    price = models.IntegerField()
    is_available = models.BooleanField()
    stock = models.IntegerField()
    create_user = models.ForeignKey(Admin, blank=True, null=True, related_name="products_created_by",
                                    on_delete=models.SET_NULL)
    update_user = models.ForeignKey(Admin, blank=True, null=True, related_name="products_updated_by",
                                    on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=False, null=True)
    deleted_at = models.DateTimeField(auto_now_add=False, null=True)

    class Meta:
        db_table = "products"

    def soft_delete(self):
        self.deleted_at = datetime.now()
        self.save()
