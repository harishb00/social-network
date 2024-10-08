# Generated by Django 5.1.1 on 2024-09-24 02:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("friends", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="friendrequest",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddConstraint(
            model_name="friendrequest",
            constraint=models.UniqueConstraint(
                fields=("sender", "receiver"), name="unique_sender_receiver"
            ),
        ),
    ]
