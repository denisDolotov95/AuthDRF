import os

from django.apps import AppConfig
from django.contrib.auth import get_user_model


class AppConfig(AppConfig):
    name = "pet_project.app"

    def ready(self):

        User = get_user_model()
        username = os.getenv("DJ_ADMIN_USER", "admin")
        email = os.getenv("DJ_ADMIN_EMAIL", "admin@example.com")
        password = os.getenv("DJ_ADMIN_PASSWORD", "admin")

        # Защита от создания дубликата
        try:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username, email=email, password=password
                )
        except Exception as e:
            pass
