# How to add translations to a django site 
*Note: you need to have tagged all items you wanted translated with the tag {% trans "whatever you wanted translated" %}.*
*The choice of language used inside {% trans %} tags should stay consistent.*
1. On a server, use `sudo su` to switch to root
1. Activate the virtual env using `source /usr/local/lib/python-virtualenv/<name of project>/bin/activate`
1. Make sure there is at least one directory called `locale` in the root of the project and/or any of the apps.
1. From the project's root directory, run `python manage.py makemessages -l <language code>` to load new site text into `django.po`.
1. For each locale directory, edit `/locale/"language code"/LC_MESSAGES/django.po`
    * `django.po` entries look like this:
    * ```
         #: path/to/template.html:18
         msgid "<Original Text>"
         msgstr "<Translated Text>"```
    * You can add new translations where it has nothing after `msgstr`, or edit existing translations.
    * If the original text on the site changes, Django doesn't want to throw out old translations, but will use a `#, fuzzy` tag to warn you that the translation may not be correct.
1. Run `python manage.py compilemessages` to load your new translations to the site.
