from django.apps import AppConfig


class AppConfig(AppConfig):
    name = "app"


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    # add this
    def ready(self):
        import app.signals  # noqa
