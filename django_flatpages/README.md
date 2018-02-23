# Django Flatpages and Ckeditor

In this tutorial (largely based on the Django [documentation](https://docs.djangoproject.com/en/2.0/ref/contrib/flatpages/) regarding the Flatpages app), I will go through how to install Flatpages and the Ckeditor by discussing the files that need to be edited.

---

## Flatpages

**_Settings.py_**

1. Under **Installed_Apps**, add the following:  
  
      ```
      'django.contrib.sites',  
      'django.contrib.flatpages'
      ```
     
    Set SITE_ID = 1
  
2. Under **Middleware_classes**, add the following:
    
    ```
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
    ```

**_Urls.py_**

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
        
**_Run command: 'manage.py migrate'_**

---
## Ckeditor

**_Settings.py_**

1. Under **Installed_Apps**, add the following:  

   ```
   'ckeditor'
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
