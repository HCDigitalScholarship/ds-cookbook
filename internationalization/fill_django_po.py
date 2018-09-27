import re
import sys
from googleapiclient.discovery import build

def translate(source_lc, target_lc, translation_service, text):
    return translation_service.translations().list(source=source_lc, target=target_lc, q=[text]).execute()['translations'][0]['translatedText']

def create_translations(source_lc, target_lc, translation_service, content):
    first_match = re.search('msgid "([^"]+)"\s*\nmsgstr ""', content)
    
    if first_match is None: #if no match was found, i.e., there are no untranslated messages
        return content
    
    source_text = first_match.groups()[0]
    translated_text = translate(source_lc, target_lc, translation_service, source_text)
    print("Translated %s to %s" % (source_text, translated_text))

    begin,end = first_match.span()
    beginning = content[:begin]
    match = 'msgid "%s"\nmsgstr "%s"\n#. Autotranslated' % (source_text, translated_text)
    rest_of_file = create_translations(source_lc, target_lc, translation_service, content[end:]) # recursive call to translate rest of file
    return beginning + match + rest_of_file

def fill_django_po(source_lc, target_lc, translation_service, filename):
    with open(filename,"r",encoding="utf-8") as fh:
        original_content = fh.read()

    content_with_new_translations = create_translations(source_lc, target_lc, translation_service, original_content)

    with open(filename,"w",encoding="utf-8") as fh:
        fh.write(content_with_new_translations)

def print_help():
    print("""
This is a script to autogenerate translations for a django.po file, using the Google Translate API.
It will not alter existing translations, only find and translate untranslated messages.
It will leave a comment `#. Autotranslated` underneath any translations it generates.

The correct usage for the script is:

    python fill_django_po.py <source language code> <target language code> path/to/django.po <Google Cloud API key>
""")

if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "help":
        print_help()
    else:
        try:
            source_lc = sys.argv[1]
            target_lc = sys.argv[2]
            filename = sys.argv[3]
            APIKEY = sys.argv[4]
            
            translation_service = build('translate', 'v2', developerKey=APIKEY)
            fill_django_po(source_lc, target_lc, translation_service, filename)
        except BaseException as e:
            print(e)
            print_help()
