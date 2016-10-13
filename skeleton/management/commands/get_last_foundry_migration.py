from django.core.management.base import BaseCommand, CommandError

from south.migration.base import Migrations


class Command(BaseCommand):

    def handle(self, *args, **options):
        migrations = Migrations('foundry')
        print migrations[-1].name()
