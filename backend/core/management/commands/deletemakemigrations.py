import os

from django.core.management.base import BaseCommand
from django.conf import settings
from django.apps import apps


class Command(BaseCommand):
    help = 'Deletes all migration files from each app'

    def handle(self, *args, **kwargs):
        installed_apps = settings.INSTALLED_APPS

        for app in installed_apps:
            if os.path.exists(os.path.join(settings.BASE_DIR, app, 'migrations')):
                for file in os.listdir(os.path.join(settings.BASE_DIR, app, 'migrations')):
                    if file == '__init__.py' or file == '__pycache__':
                        continue
                    try:
                        os.remove(os.path.join(settings.BASE_DIR, app, 'migrations', file))
                    except Exception as e:
                        print(f'Could not delete {file} from {app}.\tError: {e}')

        print('All migration files have been deleted.')

        if os.path.exists(os.path.join(settings.BASE_DIR, 'db.sqlite3')):
            os.remove(os.path.join(settings.BASE_DIR, 'db.sqlite3'))
            print('Database db.sqlite3 file has been deleted.')
        else:
            print('Database db.sqlite3 could not be found.')
