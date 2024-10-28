from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Connection, Recipe, CustomUser, Like, Notification


@receiver(post_save, sender=Connection)
def connection_handler(sender, instance, *args, **kwargs):
    Notification.objects.create(
        content=instance.follower.username + "さんからフォローされました",
        sender=instance.follower,
        recipient=instance.followee,
    )


@receiver(post_save, sender=Recipe)
def recipe_handler(sender, instance, *args, **kwargs):
    followee = instance.written_by
    followers = CustomUser.objects.filter(is_follower__followee=followee).all()
    notifications = []
    for follower in followers:
        notifications.append(
            Notification(
                content=followee.username + "さんが新しいレシピを投稿しました",
                sender=followee,
                recipient=follower,
            )
        )
    Notification.objects.bulk_create(notifications)


@receiver(post_save, sender=Like)
def like_handler(sender, instance, *args, **kwargs):
    Notification.objects.create(
        content="レシピ『"
        + instance.recipe.title
        + "』について"
        + instance.given_by.username
        + "さんから「いいね」されました",
        sender=instance.given_by,
        recipient=instance.recipe.written_by,
    )
