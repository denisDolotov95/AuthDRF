import os
import sys

from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.core.management import call_command


class AppConfig(AppConfig):
    name = "pet_project.app"

    def ready(self):

        # Проверяем, что приложение запущено командой runserver или gunicorn,
        # чтобы миграции не запускались при выполнении тестов или других команд
        if "runserver" in sys.argv or "gunicorn" in sys.argv or "uwsgi" in sys.argv:
            call_command("migrate", interactive=False)

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
