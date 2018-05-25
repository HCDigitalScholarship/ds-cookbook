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
```python
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_name',
)
```
- Next you need to create a url path.  Edit `urls.py` so that a request for your url is directed to a view.  
```python
# When nothing but the domain or ip address is entered.
path('', views.index, name='index'),
# When we receive a url with items/ at the end.
path('items/', views.items, name='items'),
# When we recive items followed by the name of an item.
path('items/<item>', views.item, name='item'),
```
For projects running earlier versions of Django (<2.0)  
```python
# When nothing but the domain or ip address is entered.
url(r'^$', views.index, name = 'index'),
# When we receive a url with items/ at the end.
url(r'^items/$', views.items, name = "items"),
```  
- Next you'll need to create the views.  Let's use the example of index, item and items above. In the application directory edit `views.py`:  
To create the index view. 
```python
def index(request):
    return render(request, 'index.html')
```
The items view.  This will return all the items in the database. 
```python
def items(request):
    items = item.objects.all()
    return render(request, 'items.html', { 'items':items })
```
The item view.  This will return a specific item. 
```python
def items(request, item):
    item = item.objects.filter(name_icontains=item)
    return render(request, 'items.html', { 'item':items })
```
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
