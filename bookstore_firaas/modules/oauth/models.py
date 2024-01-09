from django.db import models

from bookstore_firaas.modules.admin.models import Admin


# Create your models here.

class OauthClient(models.Model):
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    redirect = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    scope = models.CharField(max_length=255)
    create_user = models.ForeignKey(Admin, null=True, related_name="oauth_clients_created_by",
                                    on_delete=models.SET_NULL)
    update_user = models.ForeignKey(Admin, null=True, related_name="oauth_clients_updated_by",
                                    on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=False, null=True)
    deleted_at = models.DateTimeField(auto_now_add=False, null=True)

    class Meta:
        db_table = "oauth_clients"


class OauthAccessToken(models.Model):
    oauth_client = models.ForeignKey(OauthClient, null=True, related_name="oauth_access_tokens_created_by",
                                     on_delete=models.SET_NULL)
    user_id = models.IntegerField()
    token = models.TextField()
    scope = models.CharField(max_length=255)
    expired_at = models.DateTimeField(auto_now_add=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=False, null=True)
    deleted_at = models.DateTimeField(auto_now_add=False, null=True)

    class Meta:
        db_table = "oauth_access_tokens"


class OauthRefreshToken(models.Model):
    oauth_access_token = models.ForeignKey(OauthAccessToken, null=True, related_name="oauth_access_tokens_created_by",
                                           on_delete=models.SET_NULL)
    user_id = models.IntegerField()
    token = models.TextField()
    expired_at = models.DateTimeField(auto_now_add=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=False, null=True)
    deleted_at = models.DateTimeField(auto_now_add=False, null=True)

    class Meta:
        db_table = "oauth_refresh_tokens"
