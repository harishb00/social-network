from django.contrib.auth.models import AbstractUser
from django.db import models


class CaseInsensitiveEmailField(models.EmailField):
    def get_prep_value(self, value):
        return value.lower() if value else value


class CustomUser(AbstractUser):
    name = models.CharField(
        max_length=100,
    )
    email = CaseInsensitiveEmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )

    USERNAME_FIELD = "email"  # name of the field on the user model that is used as the unique identifier.
    REQUIRED_FIELDS = [
        "username"
    ]  # list of field names that will be prompted when creating a user via the createsuperuser management command.

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        super(CustomUser, self).save(*args, **kwargs)
