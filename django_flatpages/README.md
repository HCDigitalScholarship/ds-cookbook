# Django Flatpages and Ckeditor

In this tutorial (largely based on the Django [documentation](https://docs.djangoproject.com/en/2.0/ref/contrib/flatpages/) regarding the Flatpages app), I will go through how to install Flatpages and Ckeditor by noting the files to be edited and what additions need to be made. 

Flatpages are used to offer a standard template that can be applied to all static pages. The standard template can include headers, footers, sidebars, etc. Additionally, the user can edit each page to include its unique content through admin. This allows users without html, css, or java knowledge to add and edit pages for the site. Ckeditor offers tools for the user to make edits to the contents of each page. The following tutorial describes how the basic Ckeditor configuration is installed, but the user can make alterations to this configuration based on what editing tools they find useful to their site.    

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
* If you do not plan on installing **Ckeditor**, remove the following line:
```
content = forms.CharField(widget=CKEditorWidget())
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
2. At the bottom of settings, add the following:

   ```
   CKEDITOR_CONFIGS = {
     "default": {
         "removePlugins": "stylesheetparser",
         'allowedContent' : True,
      }
    }
   ```
  This step is necessary to prevent Ckeditor from erasing your added html.
  
**_admin.py_**

1. Under the last **Flatpage** import, add the following:
  
  ```
  from ckeditor.widgets import CKEditorWidget
  ```

2. Note the line under **admin.py** in the installation of **flatpages** (do not add anything new):
  
  ```
  content = forms.CharField(widget=CKEditorWidget())
  ```
 ---
 ## Installing Ckeditor file upload (largely based on the Django [documentation](https://django-ckeditor.readthedocs.io/en/latest/#required-for-using-widget-with-file-upload), under 'required for using widget with file upload'):
 
 Pip install:
 
 ```
 pillow
 ```
  *  **This needs to be done in the virtual environment!**
 
 **_settings.py_**
 
 1. After STATIC_ROOT, add the following:
 
    ```
    MEDIA_ROOT= os.path.join(BASE_DIR, 'media/')
    
    MEDIA_URL = '/media/'
    ```
 2. Under **Installed_Apps**, add the following:
 
    ```
    'ckeditor_uploader'
    ```
 3. After Installed_Apps, add the following:
 
    ```
    CKEDITOR_UPLOAD_PATH = "uploads/"
    
    CKEDITOR_IMAGE_BACKEND = "pillow"
    ```
 **_admin.py_**
 
 1. After 'from ckeditor.widgets import CKEditorWidget', add the following:
 
    ```
    from ckeditor_uploader.widgets import CKEditorUploadingWidget
    ```
 2. Under **class FlatpageForm(FlatpageFormOld):**, make the following changes: 
 
    ```
    content = forms.CharField(widget=CkeditorUploadingWidget())
    ```
 **_urls.py_**
 
 1. Under **urlpatterns =**, add the following:
 
    ```
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
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
Changes made in admin:

After installing Flatpages, you should see a **Flat pages** section in admin.
To create a new page, click 'Add' and insert the following:

1. Url

   ```
   /medical/
   ```
    * replace 'medical' with the url name you added under urlpatterns
  
2. Sites

   ```
   138.197.80.38
   example.com
   ```
  
   **_Both should be highlighted_**
   * replace '138.197.80.38' with your site id
     
3. Advanced Options

  * Template name
  
  
     ```
     static_page.html
     ```
     * replace 'static_page' with the name of the 'flatpage' template that you created 
     
After installing Ckeditor, a toolbar will appear when editing your 'flatpage' page. This toolbar includes the basic configuration. Changes to the toolbar configuration will be made in **settings.py**. 
Here is a source that can assist you with editing these features: https://docs.ckeditor.com/ckeditor4/latest/guide/dev_toolbar.html
