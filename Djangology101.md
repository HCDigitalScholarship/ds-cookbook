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

- When nothing but the domain or ip address is entered.  
`path('', views.index, name='index'),`  
- When we receive a url with items/ at the end.  
`path('items/', views.items, name='items'),`  
- When we recive items followed by the name of an item.  
`path('items/<item_name>', views.item, name='item'),`  

***
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
def items(request, item_name):
    items = item.objects.filter(name__icontains==item_name)
    return render(request, 'items.html', { 'items':items })
```
- Note that we'll need to make the html file `items.html`.  In the application directory create a new directory called templates (`$ mkdir templates`).  Use a text editor to create and edit three html files.  The first is `base.html`, which can be used to add a header, import javascript and css.  It's a container for the dependencies that all our pages will need.  It's a good way to keep the design of the project consistent across pages.  Later we can add navbar, footer and other reusable blocks of html.      
*base.html*  
```html
{% load staticfiles %}
<!DOCTYPE HTML>
<html>
{% block content %}{% endblock %}
</html>
```
This next template will govern what's displayed whenever we want to view the items in our collection.  
*items.html*   
```
{% extends "base.html" %}
{% block content %}

<p>This text will appear in the browser!</b>

{% for item in items %}
{{ item }}
{% endfor %}

{% endblock  %}
```

Finally, let's make an index.html for the front page of the site.  
*items.html*   
```
{% extends "base.html" %}
{% block content %}
<h1>Welcome to a Haverford Digital Scholarship Project </h1>
<img src="https://www.kiplinger.com/kipimages/pages/13180.jpg">
<a href="{% url 'items'%}">Click here to see the items in our collection</a>
{% endblock  %}
```

These files are a mix of raw html with the [Django template language](https://docs.djangoproject.com/en/2.0/ref/templates/language/).  The most common tags used in our projects are:  
- `{% for item in items %} {{ item }} {% endfor %}`  This will iterate over each item in the items variable recieved from views.  
- `{% if items %} <p>There are items</p> {% endif %}` is the same as an if statement in Python.  The line "There are items" will only print if items is True. Otherwise, the text will not display in the browser.  
- `{% static %}` which loads files from the static directory of the project.  For example `<img src="{% static 'image.jpg' %}">` Note that you need to have `{% load static %}` in your base or elsewhere in the template or you'll get an error.   
- `{% url %}` which uses the paths defined in `urls.py`.  For example `<a href="{% url 'items' %}"></a>` will enter the path to the url with `name='items'`.  
-  `{% extends 'base.html %}`  This is a useful tag that adds a block before the current template. 
- `{% include 'navbar.html' %}`  This tag will add all of the contents of another template.
- `{{ item.content|safe }}`  For content that already has html tags and formatting, the `|safe` marks a string as not requiring further HTML escaping prior to output. 
- `{% trans "Fecha de desaparición" %}`.  The [trans tag means "translation."](https://docs.djangoproject.com/en/2.0/topics/i18n/translation/)  It is an easy way to mark your content for translation to other languages.  Run `$ python manage.py makemessages` and Django will search all of your code for the trans tags and generate a .po file. The contents of the .po file will look like this:  
```
msgid "Fecha de desaparición"
msgstr ""
```
Enter the English translation as `msgstr"Date of dissapearance"`.  Now `$ python manage.py compilemessages`.  User can now switch between languages and Django will server your content in the requested language. 

***		
*Models*

We now have `urls`, which refer to `views` and `templates`.  The item and items views refer to a data entity called an `item`.  We need to create that.  In the application directory, find the `models.py` file.  We're going to create a new entity.  
```python
class item(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    url = models.URLField(max_length=200, blank=True, null=True)
    file = models.FileField(upload_to='media/')
    essay = TextField(blank=True)

    def __str__(self):
       return self.title 
   ```
This will create an `item` entity with fields for title (a charachter field - CharField), file and essay.  
Manage.py runserver 
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
