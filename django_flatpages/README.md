# Django Flatpages and Ckeditor

In this tutorial (largely based on the Django [documentation](https://docs.djangoproject.com/en/2.0/ref/contrib/flatpages/) regarding the Flatpages app), I will go through how to install Flatpages and the Ckeditor by discussing the files that need to be edited.

---

## Flatpages

**_Settings.py_**

1. Instalation  

    Under **Installed_Apps** add the following:  
  
      * 'django.contrib.sites'  
    
      * 'django.contrib.flatpages'
     
    Set SITE_ID = 1

