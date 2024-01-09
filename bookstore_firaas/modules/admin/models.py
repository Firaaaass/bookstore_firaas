from datetime import datetime

from django.db import models

# Create your models here.
class Admin(models.Model):
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    create_user = models.ForeignKey("self", null=True, related_name="admins_created_by", on_delete=models.SET_NULL)
    update_user = models.ForeignKey("self", null=True, related_name="admins_updated_by", on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=False, null=True)
    deleted_at = models.DateTimeField(auto_now_add=False, null=True)

    class Meta:
        db_table = "admins"

    def soft_delete(self):
        self.deleted_at = datetime.now()
        self.save()