from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    profile = models.TextField(
        verbose_name="プロフィール", null=True, blank=True, max_length=1000
    )
    image = models.ImageField(
        verbose_name="画像", null=True, blank=True, upload_to="images/user/"
    )

    def __str__(self):
        return self.username
