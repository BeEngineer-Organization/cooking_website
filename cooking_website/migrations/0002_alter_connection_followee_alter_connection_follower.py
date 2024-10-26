# Generated by Django 5.1.1 on 2024-10-26 08:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cooking_website", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="connection",
            name="followee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="is_followee",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="connection",
            name="follower",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="is_follower",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
