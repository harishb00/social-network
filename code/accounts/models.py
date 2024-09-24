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

    # name of the field on the user model that is used as the unique identifier.
    USERNAME_FIELD = "email"
    # list of the field names that will be prompted for when creating a user via the createsuperuser management command.
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        super(CustomUser, self).save(*args, **kwargs)
