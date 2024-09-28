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


class Connection(models.Model):
    followee = models.ForeignKey(
        CustomUser, related_name="followee", on_delete=models.CASCADE
    )
    follower = models.ForeignKey(
        CustomUser, related_name="follower", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.followee} is followed by {self.follower}"


class Recipe(models.Model):
    title = models.CharField(verbose_name="タイトル", max_length=100)
    image = models.ImageField(
        verbose_name="画像", null=True, blank=True, upload_to="images/recipe/"
    )
    description = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    written_by = models.ForeignKey(
        CustomUser, related_name="written_by", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class Like(models.Model):
    recipe = models.ForeignKey(Recipe, related_name="recipe", on_delete=models.CASCADE)
    given_by = models.ForeignKey(
        CustomUser, related_name="given_by", on_delete=models.CASCADE
    )
