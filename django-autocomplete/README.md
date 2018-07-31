# Django-autocomplete-light
In this tutorial, I will introduce how autocomplete works with forms like in *GAM* and *Bridge* projects by using Django-autocomplete-light. 
Normally, Django-autocomplete-light incorporates with model fields that have span relationships (ex. Foreignkey and ManyToMany), and how
to work with them is well documented by this [documentation](http://django-autocomplete-light.readthedocs.io/en/master/tutorial.html).
However, in our own projects, we applied autocomplete to **CharField**, and the way we did it is adapted from the documentation
and this [github issue](https://github.com/yourlabs/django-autocomplete-light/issues/913).

## Why autocomplete?
1. Being lazy. Not us, but our users. We want our application is handy enough for the users so that they can have an easy and happy
experience with our app. Having autocomplete is easy for users to search something.
2. Easy to check if what-we-are-looking-for is in the database. If it is there, it will show up in the autocomplete. This will be
very helpful for users who are editing the database.
3. Easy to create a new object to our database. If what-we-are-looking-for is not in the database, we can use autocomplete to create
one conveniently.

## Get started
1. `pip install django-autocomplete-light`
2. In `settings.py`, add the static files we need to INSTALLED_APPS, **before** `django.contrib.admin` and `grappelli` if present:
```
settings.py

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    # 'grappelli',
    'django.contrib.admin',
]
```
You are good to go!

## Working with CharField
Working with CharField is similar to working with Foreignkey or ManyToMany Fields, except Foreignkey or ManyToMany use a queryset of objects
while CharField needs a **list**. 

For example, now we have a model, Person, and we want to have autocomplete when we search its CharField, name:
```
models.py

class Person(models.Model):
    name =  models.CharField(max_length=200, null=True)
```

### 1. Create an autocomplete view
Instead of `Select2QuerySetView` which usually works for Foreignkey Field or ManyToMany Field, we use `Select2ListView` for CharField:
```
views.py

from dal import autocomplete
from myApp.models import Person

class PersonAutocomplete(autocomplete.Select2ListView):    
    def create(self, text): # To create a new object
        return text

    def get_list(self):
        # To filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return []
            
        list = [object.name for object in Person.objects.all()]
        
        if self.q:
            filter_result = Person.objects.all().filter(name__icontains=self.q)
            list = [object.name for object in filter_result]
        return list
```

### 2. Register the autocomplete view
```
urls.py 

from myApp.views import PersonAutocomplete
from django.urls import path

urlpatterns = [
    path('person-autocomplete/', PersonAutocomplete.as_view(), name='person-autocomplete'),
]
```
In python shell, ensure the url can be reversed:
```
python manage.py shell

In [1]: from django.urls import reverse
In [2]: reverse('person-autocomplete')
Out[2]: u'/person-autocomplete/'
```

### 3. Use the view in a Form widget
In the browser, try \<my droplet\>/person-autocomplete/, and we should go to a page having a queryset like this in which id and text are exactly same:

> {"results": [{"id": "Abby", "text": "Abby"}, {"id": "Ben", "text": "Ben"}, {"id": "Claire", "text": "Claire"}, {"id": "David", "text": "David"}]}

Now, we can use the autocomplete in our PersonForm. Because we want the field "name" have the autocomplete, we need to use a widget
to override its default ModelForm field; in our case we can pass the name of the url we have just registered to **ListSelect2**:
`widget=autocomplete.ListSelect2(url='person-autocomplete')`.

What's more, we need to use the field specific for list. According to the documentation, there are two fields, [Select2ListChoiceField](http://django-autocomplete-light.readthedocs.io/en/master/api.html#dal_select2.fields.Select2ListChoiceField)
and [Select2ListCreateChoiceField](http://django-autocomplete-light.readthedocs.io/en/master/api.html#dal_select2.fields.Select2ListCreateChoiceField)
that we can use to avoid problems when using Select2ListView. 

Our PersonForm should look similar to this:
```
forms.py

# To get a list of all Person objects
def get_choice_list():
    return [object.name for object in Person.objects.all()]

class PersonForm(forms.ModelForm):
    name = autocomplete.Select2ListCreateChoiceField(
        choice_list = get_choice_list,
        required=False,
        widget=autocomplete.ListSelect2(url='person-autocomplete')
    )
    class Meta:
        fields = ['name',]
        model = Person
```


### 4. Using autocompletes in the admin
We can use our autocomplete in the admin. 
```
admin.py 

from django.contrib import admin
from myApp.models import Person
from myApp.forms import PersonForm

class PersonAdmin(admin.ModelAdmin):
    form = PersonForm
admin.site.register(Person, PersonAdmin)
```
If you want to work inline, please check [this](http://django-autocomplete-light.readthedocs.io/en/master/tutorial.html#using-autocompletes-in-the-admin).

### 5. Using autocompletes outside the admin
To have the autocomplete outside the admin, first we need to have a view pass our PersonForm to a template:
```
views.py

from myApp.forms import PersonForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

class PersonView(request):
    form = PersonForm()
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            # Do something
            return HttpResponseRedirect( 'your/path' )
    return render(request, myTemplate.html, {'form':form})
```
And we need the url for this view:
```
urls.py

from myApp.views import PersonView

urlpatterns = [
    path('person-autocomplete/', PersonAutocomplete.as_view(), name='person-autocomplete'),
    path('person/', PersonView, name='person'),    
]
```
Now we can add our autocomplete form to the template. Make sure that jquery is loaded **before** {{ form.media }}:
```
myTemplate.html

{% extends 'base.html' %}
{# Don't forget that one ! #}
{% load static %}

<script type="text/javascript" src="{% static 'admin/js/vendor/jquery/jquery.js' %}"></script>

{% block content %}
<div>
    <form action="" method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <input type="submit" />
    </form>
    {{ form.media }}
</div>
{% endblock %}
```
Now we have an autocomplete form on our template!

For more information, please read their [documentation](http://django-autocomplete-light.readthedocs.io/en/master/tutorial.html#django-autocomplete-light-tutorial)
or their [github](https://github.com/yourlabs/django-autocomplete-light). Reading the issues in their repository could be very
helpful to solve your problem! Good luck!!!












