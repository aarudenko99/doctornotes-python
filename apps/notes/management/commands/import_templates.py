import re
import os
import json
from os.path import join, dirname

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db.utils import IntegrityError
from django.utils.text import slugify
from bs4 import BeautifulSoup

from apps.notes.models import Note


class Command(BaseCommand):
    help = 'Import JSON from .html templates to database'

    def handle(self, *args, **options):
        temp_dir = join(dirname(settings.BASE_DIR), 'temp')
        template_files = os.listdir(temp_dir)
        for file_name in template_files:
            file = join(temp_dir, file_name)
            with open(file, "r") as f:
                contents = f.read()
                soup = BeautifulSoup(contents, 'lxml')
                div_content = soup.find('div', {'class': 'pad dngLeftContent'})
                if div_content:
                    cont = re.sub('\s+', ' ', div_content.text).strip()
                    cont = (cont
                            .replace('var dngJsonData = ', '')
                            .replace("\'", "\"")
                            .replace('}, ', '},')
                            .replace('" }', '"}')
                            .replace(', }', ',}')
                            .replace('{ "', '{"')
                            .replace('[ {', '[{')
                            .replace('} ]', '}]')
                            .replace(',}', '}')
                            .replace(',]', ']')
                            )
                    try:

                        json_content = json.loads(cont)
                    except json.decoder.JSONDecodeError as e:
                        print(cont[600: 620])
                        self.stdout.write(self.style.ERROR(f'-- JSONDecodeError -- {file_name}:{e}'))
                        continue

                    note_title = file_name.replace('.html', '')
                    note_title = f'{note_title[:90]}{note_title[6:0:-1]}' if len(
                        note_title) >= 100 else note_title
                    try:
                        Note.objects.create(
                            title=note_title.title(),
                            slug=slugify(note_title),
                            json=json_content
                        )
                    except IntegrityError as e:
                        self.stdout.write(self.style.WARNING(f'-- duplicate -- {note_title}:{e}'))
                        continue

                    self.stdout.write(self.style.SUCCESS(f'Successfully created "{note_title}"'))
