from django.core.management.base import BaseCommand
import os
from accounts.models import User, Roles


class Command(BaseCommand):
    help = "Seeds the admin account, roles, and gender options"

    def handle(self, *args, **kwargs):
        admin_username = os.getenv("DJANGO_ADMIN_USERNAME")
        admin_email = os.getenv("DJANGO_ADMIN_EMAIL")
        admin_password = os.getenv("DJANGO_ADMIN_PASSWORD")

        admin_role = Roles.objects.get(name="admin")

        if not User.objects.filter(username=admin_username).exists():
            usr = User.objects.create(
                username=admin_username,
                email=admin_email,
                role=admin_role,
            )
            usr.set_password(admin_password)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Admin account {admin_username} created successfully."
                )
            )
        else:
            self.stdout.write(self.style.WARNING("Admin account already exists."))
