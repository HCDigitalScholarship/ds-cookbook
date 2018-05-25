## Notes from the Summer 2018 workshop on Django 

***
### Create a virtual enviornment 
Anaconda `conda create python=3 env_name`    
Virtualenv `virtualenv -p python3 new_app`    
Switch out of virtualenv
`source deactivate`  
`deactivate`  

***
Create a new Django project
in the virtual environment `pip install django`  
`django-admin startproject project_name`  
`manage.py migrate`  
`manage.py createsuperuser`  
`manage.py startapp`  
edit settings.py  
edit urls.py  
edit views.py  
edit template/index.html  
manage.py runserver  
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
