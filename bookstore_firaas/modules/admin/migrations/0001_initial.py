# Generated by Django 5.0.1 on 2024-01-08 07:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('create_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admins_created_by', to='bookstore_firaas_modules_admin.admin')),
                ('update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admins_updated_by', to='bookstore_firaas_modules_admin.admin')),
            ],
            options={
                'db_table': 'admins',
            },
        ),
    ]
