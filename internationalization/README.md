# How to add translations to a django site 
*Note: you need to have tagged all items you wanted translated with the tag {% trans "whatever you wanted translated" %}.*
*The choice of language used inside {% trans %} tags should stay consistent.*
1. On a server, use `sudo su` to switch to root
1. Activate the virtual env using `source /usr/local/lib/python-virtualenv/<name of project>/bin/activate`
1. Make sure there is at least one directory called `locale` in the root of the project and/or any of the apps.
1. From the project's root directory, run `python manage.py makemessages -l <language code>` to load new site text into `django.po`.
1. For each locale directory, edit `/locale/<language code>/LC_MESSAGES/django.po`
    * `django.po` entries look like this:
    * ```
         #: path/to/template.html:18
         msgid "<Original Text>"
         msgstr "<Translated Text>"```
    * You can add new translations where it has nothing after `msgstr`, or edit existing translations.
    * If the original text on the site changes, Django doesn't want to throw out old translations, but will use a `#, fuzzy` tag to warn you that the translation may not be correct.
1. Run `python manage.py compilemessages` to load your new translations to the site.
   
1. If you would like to automatically generate translations using Google Translate, use [this file](https://raw.githubusercontent.com/HCDigitalScholarship/ds-cookbook/master/internationalization/django_google_translate_po_file.py).  Add it to your application's management/commands directory.  You'll need to change line 4 to point to your Google API key.  Then run, for example, '$ python manage.py google_translate_po_file es de /home/ajanco/GAM/gam_app/locale/de/LC_MESSAGES/django.po'  This will translate the django.po file in the gam_app's German locale directory from Spanish (es) to German (de).  Then run compilemessages and you have a fully translated site that can be customized with feedback from users. 
