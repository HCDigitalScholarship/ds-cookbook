# Setting up Captcha Verification in a Popup Modal Box
Online documentation available on [Using django-simple-captcha](https://django-simple-captcha.readthedocs.io/en/latest/usage.html#adding-to-a-form).

Captcha is basically adding another field to Django-Forms, so you will find documentaion on [Working with forms](https://docs.djangoproject.com/en/2.0/topics/forms/) helpful as well.

## Installing django-simple-catpcha package
Full procedures are on [Using django-simple-captcha](https://django-simple-captcha.readthedocs.io/en/latest/usage.html#adding-to-a-form). It is quite straight forward. 

1. Install `django-simple-captcha` via `pip install  django-simple-captcha`

2. In `settings.py`, add captcha to the `INSTALLED_APPS` :
```
  INSTALLED_APPS=(
    ...
    "captcha"
    )
```

3. Run python `manage.py migrate`

4. Add an entry to your `urls.py`:

Whether you are adding Captcha verification to a new page or an existed page, you just need to add this following entry to your `urls.py`. It is a step to finish installation of Captcha, don't worry about the name for url.
```
urlpatterns += [
    path('captcha/', include('captcha.urls')),
]
```

## Adding a form
1. in `forms.py`:
```
from django import forms
from captcha.fields import CaptchaField

class CaptchaForm(forms.Form):
   # Other fields you want to include"
   captcha = CaptchaField()
```
If you are adding `Capthca ` to an existed form, just add  `CaptchaField`

2. Add the form in template 

 I added this Captcha verification in a Foundation popup Modal box. If you don't need to do so, go straight to step 3).
 ### Using foundation Modal
 I used Foundation popup Modal. It is similar to Bootstrap, but read XXX if you use Bootstrap
1) You need to have Foundation package installed in your static directory and render them in your template HTML. You also need to run the Javascript for Modal in HTML template via:
```
$(document).foundation();

```

2) Link for pop up Modal box

 ```
 <a href="#" data-reveal-id="myModal"> PDF </a>
 ```
3) Create a Modal box and add the Captcha form there
```
            <div id="myModal" class="reveal-modal" data-reveal aria-labelledby="modalTitle" aria-hidden="true" role="dialog">
              <form action="." method='POST'>
                {% csrf_token %}
                {{ form.as_p }}
                <input type="submit" />
                <input type="hidden" id="manuscript_id" name="manuscript_ID" value="{{text.id_tei}}">
              </form>
              <a class="close-reveal-modal" aria-label="Close">&#215;</a>
            </div>
```
*It is important that `action ="."`; otherwises, the Captcha verification won't work. If you need to redirect the page to another url, we will do it in `views.py`.*

Because I need to pass variable to create a new url where I want to redirect to, so I created a hidden input where I can pass the variable to `views.py`.

## Validation of your Captcha form in `views.py`
In `views.py`:
```
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def someviewfunction(request):
    if request.POST:
        form = CaptchaForm(request.POST)
        print(dict(request.POST))
        if form.is_valid():
            human = True
            id=request.POST['manuscript_ID'] #name of the hidden input from the HTML template: 'yourtemplate.html'
            url=id+'.pdf'
            return redirect(url)

        else:
            raise ValidationError( _('Opps, wrong captcha key'))
            
    else:
        form = CaptchaForm()
    return render(request, 'yourtemplate.html', {"form":form, other variables you need}
```

I think that's it.

