# django-plotly-dash 

Embed one or multiple plotly-dash app(s) into an existing Django app. This documentation is adapted from <https://buildmedia.readthedocs.org/media/pdf/django-plotly-dash/latest/django-plotly-dash.pdf>. 
The orginal source code and exampe is in <https://github.com/GibbsConsulting/django-plotly-dash/tree/c50decc7028f0dc8825632e551da94212afb8027>  

## 0 What you need before you preceed.


*  A Django 2.0 or greater project
*  A plotly-dash app using dash == 0.38.0 (** exactly 0.38.0 version, other versions(lower and higher) do not work currently)
* put the folder for your plotly-dash app in the same directory of your Django `views.py`.
## 1 Installation
1. First, install the django-plotly-dash package.
```
pip install django_plotly_dash
```
2. Install the package in your Django project in `settings.py`
```
INSTALLED_APPS = [
    ...
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    ...
    ]
```
You can also include optional settings for django-plotly-dash if needed. Read [1.9 Configuration options](https://buildmedia.readthedocs.org/media/pdf/django-plotly-dash/latest/django-plotly-dash.pdf) from the official documentation.

## 2 Register your plotly-dash app in `urls.py`
in urls.py
```
import Django_Dash_app.dashplotly.dashboard_app
#fullpath to your app.py file. my app.py file is named as "dashboard_app.py"
urlpatterns = [
...
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
...]
```
run `python manage.py migrate`

## 3 make changes in your plotly-dash app
In the app.py of your plotly-dash app:
```
#django
from django_plotly_dash import DjangoDash

app = DjangoDash('SimpleExample') 
#orignally app=dash.Dash(__name__). 
#You will need this name "SimpleExample" to call your app in Django template(s).

#delete
"""
if __name__ == '__main__':
    app.run_server(debug=True)
"""
```
## 4. Embed your plotly-dash app in a Django template
in template.html
```
{%load plotly_dash%}
{%plotly_app name="SimpleExample"%}
```
`plotly_app` will embed an iFrame.


