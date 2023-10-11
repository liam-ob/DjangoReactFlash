import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Creates a superuser with username "admin", email "a@a.com", and password "admin"'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username=os.environ.get('SUPERUSER_USERNAME', 'admin'),
                email=os.environ.get('SUPERUSER_EMAIL', 'a@a.com'),
                password=os.environ.get('SUPERUSER_PASS', 'admin'),
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists.'))
