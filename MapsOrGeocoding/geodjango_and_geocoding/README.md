# GeoDjango and Geocoding (NEW)
Want to create a world-class geographic Web application through Django? **GeoDjango**, built on Python and Django, is a great 
toolkit to help you handle with spatial database and build a GIS Web application. When you have address information (like
a home address) and want to show them on a map, **Geocoding API** from google maps helps you convert the descriptive addresses 
into geographic coorindates (longitude and latitude) so that you can place markers on the map or position the map.
In this tutorial, we'll teach you how to create a GeoDjango project, and explain how Geocoding works.

Keywords:
* Start a GeoDjango project
* Install Django map widget
* Work with Geocoding API
***

## 1. Start a GeoDjango project
### a. Create a spatial database
Create a database as you would for other projects. Here are some tips for installing the selected databases:
* [PostGIS](https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/postgis/)
* [SpatialLite](https://docs.djangoproject.com/en/2.0/ref/contrib/gis/install/spatialite/)

### b. Create a new project
Again, nothing special here. Create a new project as you would for other projects.
```
$ django-admin startproject myProject
$ cd myProject
$ python manage.py startapp myApp
```

### c. Configure settings.py
Go to `settings.py` and edit your database connection to your spatial database:
```
settings.py

DATABASES = {
    'default': {
         'ENGINE': 'django.contrib.gis.db.backends.postgis',
         'NAME': '<the name of your spatial database>',
         'USER': '<your username>',
    },
}
```
Then, add `django.contrib.admin`, `django.contrib.gis`, and your created application to **INSTALLED_APPS** setting:
```
settings.py

INSTALLED_APPS = [
    'django.contrib.admin', # add this
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis', # add this
    'myApp', # add this
]
```

### d. Define a geographic model
To create a GeoDjango model, you need to import models from `django.contrib.gis.db`:
```
models.py

from django.contrib.gis.db import models

class Company(models.Model):
    # You may also use regular Django fields
    name = models.CharField(max_length=50)
    start_year = models.IntegerField(blank=True)
    address = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    
    # GeoDjango-specific: a geometry field (PointField)
    geographic_location = models.PointField(blank=True)
```
PointField is one of the spatial fields of GeoDjango, which, as its name suggests, displays the location as a point on the map
based on a pair of geographic coordinates(log, lat). Other spatial fields are:

Fields | Description | Examples
------ | ----------- | --------
GeometryField | either a Point, a LineString or a Polygon | 
PointField | a point | `>>> Point(1,1) #same as Point([1,1])`
LineStringField | either a sequence of coordinates or Point objects| `>>> LineStringRing((0,0), (1,1))` <br> `>>> LineString(Point(0,0), Point(1,1))`
PolygonField | contructed by passing parameters that represent <br> the rings of the polygon, and the parameters must <br> be either [LinearRing](https://docs.djangoproject.com/en/2.0/ref/contrib/gis/geos/#linearring) objects, or a sequence that <br> may be used to construct a LinearRing | [click me](https://docs.djangoproject.com/en/2.0/ref/contrib/gis/geos/#polygon)
MultiPointField | either by passing in Point objects as arguments, or a single sequence of Point objects| `>>> MultiPoint(Point(0,0), Point(1,1))` <br> `>>> MultiPoint( (Point(0,0), Point(1,1)) )`
MultiLineStringField | either by passing in LineString objects as arguments, or a single sequence of LineString objects | [click me](https://docs.djangoproject.com/en/2.0/ref/contrib/gis/geos/#multilinestring)
MultiPolygonField | either by passing Polygon objects as arguments, or a single sequence of Polygon objects | [click me](https://docs.djangoproject.com/en/2.0/ref/contrib/gis/geos/#multipolygon)
GeometryCollectionField | either by passing in other GEOSGeometry as arguments, or a single sequence of GEOSGeometry objects | [click me](https://docs.djangoproject.com/en/2.0/ref/contrib/gis/geos/#geometrycollection)
RasterField | currently only implemented for the PostGIS backend | [click me](https://docs.djangoproject.com/en/2.0/ref/contrib/gis/db-api/#creating-and-saving-models-with-raster-fields)

Or you may run **inspectdb** if you have an existing database, and then you can have models auto-generate based on your tables.
```
$ python manage.py inspectdb > models.py
```

### e. Run migrate
After defining your model, you need to sync it with your database. First, create a database migration:
```
$ python manage.py makemigrations

Migrations for 'myApp':
  myApp/migrations/0001_initial.py:
    - Create model Company
```
Then, you may check the table of your model generated by SQL:
```
$ python manage.py sqlmigrate myApp 0001
```
If the output looks correct, run **migrate** to create this table in the database:
```
$ python manage.py migrate
```

Now you have built a base for your GeoDjango appplication, and you may continue to build other features! Remember that almost every thing you usually import from `django.contrib`, like **admin**, should import from `django.contrib.gis`.

For more information, please refer to this [Django documentation](https://docs.djangoproject.com/en/2.0/ref/contrib/gis/tutorial/#introduction)

## 2. Install Django map widgets
Django-map-widgets does a great help to support the map services (ex. google maps) for your GeoDjango fields. It allows you to easily and properly use all GeoDjango widgets. 

### a. Get started
Install from PiPy
```
$ pip install django-map-widgets
```

Add `map_widgets` to **INSTALLED_APPS** in `settings.py`:
```
settings.py 

INSTALLED_APPS = [
     ...
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'mapwidgets',
]
```

Collect the static files into **STATIC_ROOT**:
```
$ python manage.py collectstatic
```

### b. Work with maps widgets
Django-map-widgets has four kinds of widgets:
* [Google map point field widget](http://django-map-widgets.readthedocs.io/en/latest/widgets/point_field_map_widgets.html)
* [Google map widget for Django admin inline](http://django-map-widgets.readthedocs.io/en/latest/widgets/point_field_inline_map_widgets.html)
* [Google map static widget](http://django-map-widgets.readthedocs.io/en/latest/widgets/google_static_map_widget.html#)
* [Google map static overlay widgets](http://django-map-widgets.readthedocs.io/en/latest/widgets/google_static_overlay_map_widget.html)

Here we will introduce the most commonly-used widget in our projects, **Google map point field widget**:
![ Google map point field widget ](https://github.com/HCDigitalScholarship/ds-cookbook/blob/master/images/Google%20map%20point%20field%20widget.png)

This widget has a Google Place Autocomplete widget as a default and a built-in geocoding support. Google geocoding will automatically fill the autocomplete input when you add a marker manually.

To use this widget, add a **MAP_WIDGETS** config in `settings.py`:
```
settings.py

MAP_WIDGETS = {
    "GooglePointFieldWidget": (
        ("zoom", 15),
        ("mapCenterLocationName", "newyork"), 
        ("GooglePlaceAutocompleteOptions", {'componentRestrictions': {'country': 'us'}}),
        ("markerFitZoom", 12),
    ),
    "GOOGLE_MAP_API_KEY": "<google-api-key>"
}
```

For `"mapCenterLocationName"`, you may give geographic coordinates instead of a specific location name:
```
settings.py

MAP_WIDGETS = {
    "GooglePointFieldWidget": (
        ("zoom", 15),
        ("mapCenterLocation", [57.7177013, -16.6300491]),
    ),
    "GOOGLE_MAP_API_KEY": "<google-map-api-key>"
}
```

**NOTES**: You may also give specific settings for each widget in `admin.py`, but **GOOGLE-MAP-API-KEY** must be set in `settings.py` for customized settings usage:
```
admin.py

from django.contrib.gis import admin
from mapwidgets.widgets import GooglePointFieldWidget

CUSTOM_MAP_SETTINGS = {
    "GooglePointFieldWidget": (
        ("zoom", 15),
        ("mapCenterLocation", [60.7177013, -22.6300491]),
    ),
}

class CompanyAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget(settings=CUSTOM_MAP_SETTINGS)}
    }
```

After you set the widget, you should add this widget to your pointfield, in `admin.py` if you want to have the map on **Django admin**:
```
admin.py

from django.contrib.gis import admin
from mapwidgets.widgets import GooglePointFieldWidget

class CompanyAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }
```

Or if you are using mapwidgets in your **regular django views**, create a `forms.py` and add this:
```
from django.contrib.gis import forms
from mapwidgets.widgets import GooglePointFieldWidget

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ("geographic_location",) # GeoDjango-specific fields
        widgets = {
            'geigraphic_location': GooglePointFieldWidget,
            # more here if you have more than one GeoDjango-specific field
        }
```
Remember to pass your form to a template in `views.py` and set an url for this view in `urls.py`.

In addition, you need to add {{ form.media }} to \<head\> or the end of \<body\> section of your corresponding templates:
```
template.html

<!DOCTYPE html>
<html>
<head>
  ...
  {{ form.media }}
</head>
<body>
  ...
  {{ form }}
</body>
</html>
```
**NOTES**: if you are using mapwidgets on the **Django admin**, you do **NOT** need to add {{ form.media }} any template files. The media variable is already in the default admin templates.

For more information, please go and check its [documentation](http://django-map-widgets.readthedocs.io/en/latest/index.html).

## 3. Working with Geocoding API
According to the definition given by Google Maps:
> Geocoding is the process of converting addresses (like a street address) into geographic coordinates (like latitude and longitude), which you can use to place markers on a map, or position the map.

When you only have address while your point fields or other GeoDjango-specific fields require geographic coordinates, you will need geocoding to help you get the coordinates.

### a. Installation
You need to install a Python client library for Google Maps API Web Services to your Django application:
```
$ pip install -U googlemaps
```

### b. Send the address to googlemaps
The codes for geocoding is very neat, all you need is an address in a string and, for sure, your **google-api-key**:
```
>>> import googlemaps
>>> address = '370 Lancaster Avenue, Haverford, PA, 19041, USA'
>>> gmaps = googlemaps.Client(key='<google-api-key>')
>>> geocode_result = gmaps.geocode(address)
>>> print (geocode_result)
```
The way of writing your address may be somewhat flexible, although technically it should be equivalent to the **postal address**. Here are some ways of writing addresses we have tried, which are fine with geocoding:
```
>>> 'Haverford College' # A direct and specific location name
>>> 'haverford collect' # NO caps
>>> 'Haverford College, Haverford, PA, 19041' # A somewhat detailed address
>>> '370 Lancaster Ave, Haverford, PA, 19041' # Shortcuts
>>> '370 Lancaster Avenue Haverford PA 19041' # NO comma
>>> '370 Lancaster Avenue, Haverford, PA, 19041, USA' # A full postal address
```

What does the **geocode_result** look like? Usually Google Maps will return something like this in JSON:
```
{
 "address_components" : [
    {
       "long_name" : "277",
       "short_name" : "277",
       "types" : [ "street_number" ]
    },
    {
       "long_name" : "Bedford Avenue",
       "short_name" : "Bedford Ave",
       "types" : [ "route" ]
    },
    {
       "long_name" : "Williamsburg",
       "short_name" : "Williamsburg",
       "types" : [ "neighborhood", "political" ]
    },
    {
       "long_name" : "Brooklyn",
       "short_name" : "Brooklyn",
       "types" : [ "political", "sublocality", "sublocality_level_1" ]
    },
    {
       "long_name" : "Kings County",
       "short_name" : "Kings County",
       "types" : [ "administrative_area_level_2", "political" ]
    },
    {
       "long_name" : "New York",
       "short_name" : "NY",
       "types" : [ "administrative_area_level_1", "political" ]
    },
    {
       "long_name" : "United States",
       "short_name" : "US",
       "types" : [ "country", "political" ]
    },
    {
       "long_name" : "11211",
       "short_name" : "11211",
       "types" : [ "postal_code" ]
    }
 ],
 "formatted_address" : "277 Bedford Ave, Brooklyn, NY 11211, USA",
 "geometry" : {
    "location" : {
       "lat" : 40.7142205, # Need this
       "lng" : -73.9612903 # Need this
    },
    "location_type" : "ROOFTOP",
    "viewport" : {
       "northeast" : {
          "lat" : 40.71556948029149,
          "lng" : -73.95994131970849
       },
       "southwest" : {
          "lat" : 40.7128715197085,
          "lng" : -73.9626392802915
       }
    }
 },
 "place_id" : "ChIJd8BlQ2BZwokRAFUEcm_qrcA",
 "types" : [ "street_address" ]
}
```
It returns more than one pair of geographic coordinates. And what you need to do is to extract the values of "lag" and "lng" of "location" from this long dictionary:
```
>>> lat = geocode_result[0]["geometry"]["location"]["lat"] # having index at the beginning is to get the dictionary from the JSON file
>>> lng = geocode_result[0]["geometry"]["location"]["lng"]
```
The final step is to update migrate the coordinates to your PointField (in our example, it is **geographic_location**):
```
>>> geographic_location = Point(x=lng, y=lat, srid=4326) # srid represents WGS84, the default spatial reference system for geometry fields
```

All codes in one file (by using the sample model **Company**, hopefully you still remember it):
```
import googlemaps

def geocoding_for_pointfield():
    for instance in Company.objects.all():
        full_address =  instance.address + ", " + instance.address2 + ", " + instance.city + ", " + instance.state + ", " + instance.zipcode + ", " + instance.country
        gmaps = googlemaps.Client(key='<google-api-key>')
        geocode_result = gmaps.geocode(full_address)
        if len(geocode_result) != 0: # for the cases when the addresses are empty
            lat = geocode_result[0]["geometry"]["location"]["lat"]
            lng = geocode_result[0]["geometry"]["location"]["lng"]
            instance.geographic_location = Point(x=lng, y=lat, srid=4326)
```
You got it! For more detailed information, please check [their website](https://developers.google.com/maps/documentation/geocoding/intro). 

You are welcome to edit and update this tutorial! Nice job and good luck!

