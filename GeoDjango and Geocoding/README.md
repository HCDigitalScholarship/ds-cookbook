# GeoDjango and Geocoding
Want to create a world-class geographic Web application through Django? **GeoDjango**, built on Python and Django, is a great 
toolkit to help you handle with spatial database and build a GIS Web application. When you have address information (like
a home address) and want to show them on a map, **Geocoding API** from google maps helps you convert the descriptive addresses 
into geographic coorindates (longitude and latitude) so that you can place markers on the map or position the map.
In this tutorial, we'll teach you how to create a GeoDjango project, and explain how Geocoding works.

Keywords:
* Start a GeoDjango project
* Install Django map widget
* Work with googlemaps geocoding

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

Now you are ready to continue building your application! Remember that almost every thing you usually import from `django.contrib`, like **admin**, should import from `django.contrib.gis`.
