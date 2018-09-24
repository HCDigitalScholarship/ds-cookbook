import re
import sys
from googleapiclient.discovery import build

def translate(source, target, q):
    return service.translations().list(source=source, target=target, q=[q]).execute()['translations'][0]['translatedText']

def fill_django_po(source, target, filename):
    with open(filename,"r",encoding="utf-8") as fh:
        po_content = fh.read()

    new_content = create_translations(source,target,po_content)

    with open(filename,"w",encoding="utf-8") as fh:
        fh.write(new_content)

def create_translations(source, target, content):
    first_match = re.search('msgid "([^"]+)"\s*\nmsgstr ""',content)
    if first_match is None:
        return content
    begin,end = first_match.span()
    source_text = first_match.groups()[0]
    return content[:begin] + ('msgid "%s"\nmsgstr "%s"\n#. Autotranslated' % (source_text,translate(source,target,source_text))) + create_translations(source, target, content[end:])

if __name__ == "__main__":
    source = sys.argv[1]
    target = sys.argv[2]
    filename = sys.argv[3]
    APIKEY = sys.argv[4]

    service = build('translate', 'v2', developerKey=APIKEY)
    fill_django_po(source, target, filename)
    
