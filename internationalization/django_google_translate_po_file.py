import re
import sys
from django.core.management.base import BaseCommand, CommandError
from archivo.settings_secret import API_KEY
from googleapiclient.discovery import build



class Command(BaseCommand):
    help = "Uses Google Translate to automatically populate the Django po file with translations. Don't forget to makemessages to update the po file first. Ex. '$ python manage.py google_translate_po_file es de /home/ajanco/GAM/gam_app/locale/de/LC_MESSAGES/django.po'  Takes arguments for source language, target language and file path. Note: English = en, Spanish = es, German = de."

    def add_arguments(self, parser):
        parser.add_argument('source', nargs='+', type=str, help='The language of the source text, set to one of the language codes listed in Language Support. If the source language is not specified, the API will attempt to detect the source language automatically and return it within the response.')
        parser.add_argument('target', nargs='+', type=str, help='The language to use for translation of the input text, set to one of the language codes listed in Language Support.')
        parser.add_argument('filename', nargs='+', type=str, help='The path and filename of the django.po file you want to update.')

    def handle(self, *args, **options):
        from archivo.settings_secret import API_KEY

        source = options['source'][0]
        target = options['target'][0]
        filename = options['filename'][0]

        def translate(source, target, q):
            return service.translations().list(source=source, target=target, q=[q]).execute()['translations'][0][
                'translatedText']

        def fill_django_po(source, target, filename):
            with open(filename, "r", encoding="utf-8") as fh:
                po_content = fh.read()

            new_content = create_translations(source, target, po_content)

            with open(filename, "w", encoding="utf-8") as fh:
                fh.write(new_content)

        def create_translations(source, target, content):
            first_match = re.search('msgid "([^"]+)"\s*\nmsgstr ""', content)
            if first_match is None:
                return content
            begin, end = first_match.span()
            source_text = first_match.groups()[0]
            return content[:begin] + ('msgid "%s"\nmsgstr "%s"\n#. Autotranslated' % (
            source_text, translate(source, target, source_text))) + create_translations(source, target, content[end:])

        service = build('translate', 'v2', developerKey=API_KEY)
        fill_django_po(source, target, filename)

