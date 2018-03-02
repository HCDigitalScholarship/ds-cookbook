# Django Flatpages and Ckeditor

In this tutorial (largely based on the Django [documentation](https://docs.djangoproject.com/en/2.0/ref/contrib/flatpages/) regarding the Flatpages app), I will go through how to install Flatpages and the Ckeditor by noting the files to be edited and what additions need to be made.

---

## Flatpages

**_settings.py_**

1. Under **Installed_Apps**, add the following:  
  
      ```
      'django.contrib.sites',  
      'django.contrib.flatpages'
      ```
     
    Set SITE_ID = 1
  
2. Under **Middleware_classes**, add the following to the bottom of the list:
    
    ```
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
    ```

**_urls.py_**

1. Add the following:

    ```
    from django.contrib.flatpages import views as flat_views
    ```
   
 2. Under **urlpatterns**, add the following:
 
    ```
    url(r'^medical/$', flat_views.flatpage, {'url': '/medical/'}, name = 'medical'),
    ```
   
       * replace 'medical' with the name of your page
       * if your page previously had a url, comment it out 
        
* **_Run command: 'manage.py migrate'_**

**_admin.py_**

1. Add the following after the last import:

```
from django.contrib.flatpages.models import FlatPage

#Note: We are renaming the original Admin and Form as we import them!
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOld

from django import forms
from ckeditor.widgets import CKEditorWidget

class FlatpageForm(FlatpageFormOld):
  content = forms.CharField(widget=CKEditorWidget())
  class Meta:
    model = FlatPage # this is not automatically inherited from FlatpageFormOld
    fields = '_ _ all_ _'
    
class FlatPageAdmin(FlatPageAdminOld):
  form = FlatpageForm
  
#We have to unregister the normal admin, and then reregister ours
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
```

---
## Ckeditor

Pip install:

  ```
  django-ckeditor
  ```
   *  **This needs to be done in the virtual environment!**
   
**_settings.py_**

1. Under **Installed_Apps**, add the following:  

   ```
   'ckeditor'
   ```
**_admin.py_**

* note the lines under **admin.py** in the installation of **flatpages**:
  
  ```
  from ckeditor.widgets import CKEditorWidget
  ```
  ```
  content = forms.CharField(widget=CKEditorWidget())
  ```
---
## Creating a 'Flatpages' template

```
<!DOCTYPE html>
<html>
<head>
<title>{{ flatpage.title }}</title>
</head>
<body>
{{ flatpage.content }}
</body>
</html>
```

---
## Creating a 'Flatpages' page
Changes made in admin

1. Url

   ```
   /medical/
   ```
  
2. Sites

   ```
   138.197.80.38
   example.com
   ```
  
   **_Both should be highlighted_**
     
3. Advanced Options

    * Template name
  
  
     ```
     static_page.html
     ```
