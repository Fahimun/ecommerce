# Generated by Django 5.1.4 on 2025-03-13 05:51

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_alter_profile_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email_token',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
