from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User


UserModel = get_user_model()


class Profile(models.Model):
    email = models.EmailField(
        blank=False,
        null=False,
    )
    user = models.OneToOneField(
        UserModel,
        on_delete=models.DO_NOTHING,
        primary_key=True,
    )
