from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Creates a superuser by the user: admin and password: admin'

    def handle(self, *args, **kwargs):
        if get_user_model().objects.filter(is_superuser=True).count() < 1:
            get_user_model().objects.create_superuser(
                'admin',
                'admin@example.com',
                'admin'
            )
            print('created superuser')
        else:
            print('superuser already created')
