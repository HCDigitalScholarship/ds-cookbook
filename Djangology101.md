## Notes from the Summer 2018 workshop on Django 

***
### Create a virtual enviornment 
[Anaconda](https://conda.io/docs/index.html) `conda create python=3 env_name`    
Virtualenv `virtualenv -p python3 new_app`    
Switch out of virtualenv
`source deactivate` (anaconda) or `deactivate` (virtualenv)    

***
### Create a new Django project
In the virtual environment `pip install django`.  If you need a specific version `pip install django==2.0.1`  

-  Create a new Django project with `django-admin startproject project_name`.  This will create a folder for the project with `manage.py`.  I'll refer to this going forward as the `project directory`.  You'll find `settings.py` and `urls.py` in a subdirectory of the project directory.    
-  Next create your first Django application.  Go to the project directory and type `manage.py startapp app_name`.    

![image](https://github.com/HCDigitalScholarship/ds-cookbook/blob/master/google_vision/why-django-for-web-development-8-638.jpg)  


- The migrate command will update the database based on the code in your `models.py` and other files.  To make the db reflect your current code, type `$ python manage.py migrate`.  This will update the db with the tables needed to create users and user groups.  

- Before you can log in to the admin page, you'll need to create a user by typing `$ python manage.py createsuperuser`.    
- To add you new app to the project, edit `settings.py`.  Use a text editor to add `'app_name',` to the INSTALLED_APPS section.  
`INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_name',
)`  
- edit urls.py  
- edit views.py  
- edit template/index.html  
- manage.py runserver  


***		
		
#Resources  
		[Lynda](https://www.lynda.com/allcourses)  
		[DS cookbook](https://github.com/HCDigitalScholarship/ds-cookbook)  
		[DS showcase app](https://github.com/HCDigitalScholarship/django-showcase)  
    [Django Packages](https://djangopackages.org/)  
		[Writing your first Django app, part 1](https://docs.djangoproject.com/en/2.0/intro/tutorial01/)  
***
Tuesday		
	Models
	
		applications/packages (https://djangopackages.org/)
		
		Writing your first Django app, part 2 (https://docs.djangoproject.com/en/2.0/intro/tutorial02/)
		Data Modeling
		migrations
		Admin
		
		importing data into Django 
		Ckeditor
***
Debuggin problems with nginx &uWsgi settings:
In your uwsgi ini file, check the...
1) project directory /srv/test  
2) environment /srv/test_env  
3) 
from settings.py  
WSGI_APPLICATION = 'FIRST.wsgi.application'  
4) check that 
uwsgi ini file  
`socket = /run/uwsgi/app/sourcebook/FIRST.socket`    
is the same as nginx sites-available  
`uwsgi_pass unix:/run/uwsgi/app/sourcebook/FIRST.socket`  

tail -f /var/log/uwsgi/app/app_name  
tail -f /var/log/nginx/error.log  
