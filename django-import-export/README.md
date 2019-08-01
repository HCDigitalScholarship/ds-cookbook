# Django-import-export

This tutorial explains how to use django-import-export application and library for importing
and exporting data with included admin integration.

Features:

* support multiple formats (Excel, CSV, JSON, XLS, XLSX, TSV, and YAML 

* admin integration for importing

* preview import changes

* admin integration for exporting

* export data respecting admin filters

.. image:: docs/_static/images/django-import-export-change.png

## Installation and configuration

django-import0export can be installed by standard python tools like pip. Type the following 
in your command line:

` $ pip install django-import-export `

If you want to use django-import-export from the admin as well, add it to your **[INSTALLED_APPS]**
and django will collect its static files.

```
# settings.py
INSTALLED_APPS = (
    ...
    'import_export',
)
```

Then type the following line:
`$ python manage.py collectstatic`

## Creating import-export resource

To integrate django-import-export with your model, go to `app/admin.py` and add the following line:

`from import_export.admin import ImportExportModelAdmin`

Your admin section should now have the Import and Export sections:

![ import-export example ](https://django-import-export.readthedocs.io/en/stable/_images/django-import-export-change.png)




