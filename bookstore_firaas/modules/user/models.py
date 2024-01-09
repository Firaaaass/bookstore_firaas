from datetime import datetime

from django.db import models

from bookstore_firaas.modules.admin.models import Admin


# Create your models here.

class User(models.Model):
    email = models.EmailField(null=False)
    name = models.CharField(null=False, max_length=200)
    password = models.CharField(max_length=200)
    create_user = models.ForeignKey(Admin, null=True, related_name="users_created_by", on_delete=models.SET_NULL)
    update_user = models.ForeignKey(Admin, null=True, related_name="users_updated_by", on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=False, null=True)
    deleted_at = models.DateTimeField(auto_now_add=False, null=True)

    class Meta:
        db_table = "users"

    def soft_delete(self):
        self.deleted_at = datetime.now()
        self.save()