import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from recipes.models import Tag

DATA_ROOT = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    help = 'loading tags from data in json'

    def add_arguments(self, parser):
        parser.add_argument('filename', default='tags.json', nargs='?',
                            type=str)

    def handle(self, *args, **options):
        try:
            with open(os.path.join(DATA_ROOT, options['filename']), 'r',
                      encoding='utf-8') as f:
                data = json.load(f)
                for tag in data:
                    try:
                        Tag.objects.create(
                            name=tag["name"],
                            color=tag["color"],
                            slug=tag["slug"])
                    except IntegrityError:
                        print(f'Tag {tag["name"]} '
                              f'{tag["color"]} '
                              f'{tag["slug"]} '
                              f'is already in db.')
            print('Done.')

        except FileNotFoundError:
            raise CommandError("File isn't in the directory.")
