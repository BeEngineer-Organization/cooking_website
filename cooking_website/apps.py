from django.apps import AppConfig


class CookingWebsiteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cooking_website"

    def ready(self):
        try:
            from . import signals
        except ImportError:
            pass
