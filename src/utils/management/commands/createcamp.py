# coding: utf-8
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Creates html files needed for a camp'

    def add_arguments(self, parser):
        parser.add_argument('camp_slug', type=str)

    def output(self, message):
        self.stdout.write('{}: {}'.format(
                timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
                message
            )
        )

    def local_dir(self, entry):
        return os.path.join(
            settings.DJANGO_BASE_PATH,
            entry
        )

    def handle(self, *args, **options):

        # files to create, relative to DJANGO_BASE_PATH
        files = [
            'sponsors/templates/{camp_slug}-sponsors.html',
            'camps/templates/{camp_slug}-camp_detail.html',
            'program/templates/{camp_slug}-call_for_speakers.html'
        ]

        # directories to create, relative to DJANGO_BASE_PATH
        dirs = [
            'static/img/{camp_slug}/logo'
        ]

        camp_slug = options['camp_slug']

        for _file in files:
            path = self.local_dir(_file.format(camp_slug=camp_slug))
            if os.path.isfile(_file):
                self.output('File {} exists...'.format(path))
            else:
                self.output('Creating {}'.format(path))
                with open(path, mode='w', encoding='utf-8') as f:
                    f.write(_file.format(camp_slug=camp_slug))

        for _dir in dirs:
            path = self.local_dir(_file.format(camp_slug=camp_slug))
            if os.path.exists(path):
                self.output('Path {} exists...'.format(path))
            else:
                self.output('Creating {}'.format(path))
                os.mkdir(path, mode=0o644)

        self.output('All there is left is to create:')
        self.output(
            self.local_dir(
                'static/img/{camp_slug}/logo/{camp_slug}-logo-large.png'.format(camp_slug=camp_slug)
            )
        )
        self.output(
            self.local_dir(
                'static/img/{camp_slug}/logo/{camp_slug}-logo-small.png'.format(camp_slug=camp_slug)
            )
        )
