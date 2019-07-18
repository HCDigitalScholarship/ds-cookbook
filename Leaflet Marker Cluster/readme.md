# Using Leaflet and the Marker Cluster Plugin
![ Google map point field widget ](https://github.com/fgould/ds-cookbook/blob/patch-1/Leaflet%20Marker%20Cluster/Screen%20Shot%202019-07-18%20at%201.50.05%20PM.png)

[Leaflet](https://leafletjs.com/) is a beautiful, lightweight javascript library that can be used to create interactive maps with any number of possible uses. Integrated with **GeoDjango** in our models/database, we have the tools to deal with large amount of spatial data and the easy ability to serve up that data on our templates for the user to interact with. If you don't know your way around GeoDjango and spatial database elements, I suggest getting aclimated with some reading first:

* [GeoDjango Documentation](https://docs.djangoproject.com/en/2.2/ref/contrib/gis/)
* [Cookbook entry](https://github.com/HCDigitalScholarship/ds-cookbook/tree/master/GeoDjango%20and%20Geocoding)

Now that we've gotten started, we can begin to create leaflet maps and then apply clustering. But first:

## 1. Dependencies
* Follow the installation instructions on the [documentation](https://github.com/Leaflet/Leaflet.markercluster) **or**
* Include these lines at the start of each template where you use a cluster map for most of the functionality and style
```
<script src="https://unpkg.com/leaflet.markercluster@1.4.1/dist/leaflet.markercluster.js"></script>
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.Default.css">
```
* Make sure GeoDjango is installed and compatible with your database because djangos default sqlite won't be enough. Configuration can be found on the [GeoDjango Setup](https://docs.djangoproject.com/en/2.2/ref/contrib/gis/tutorial/#setting-up) 

## 2. Creating spatial model fields
Assuming you have already set up a django project and have a working database/admin site, we can begin to add spatial fields to models which we may want to map. In this example I create a person model and give it a [PointField](https://docs.djangoproject.com/en/2.2/ref/contrib/gis/model-api/) that references the person's location. 
```
from django.contrib.gis.db import models

class Person(models.Model):
        geom = models.PointField(null=True, blank=True)
        name = models.CharField(max_length=200)
```
Now add whatever and however many people and locations you wish, the good thing about marker cluster is even if points are in the exact same location, we can still display them both!

## 3. Deciding which locations to display in the view
Before we can map data in the templates we have to create a list of the geom objects we wish to display. We do this in the views:
```
views.py

from django.shortcuts import render
from books_app.models import *

def index(request):
    people = Person.text.all()
    return render(request,'index.html', {'people': people})
```
This is the minimum you can do in the view. The ability to use apply user input or other variable data to query which objects you want is applied here. Just make sure you are only passing objects into the template that have spatial data.

## 4. Creating a map in the template
Here we begin to use Leaflet and Marker Clustering


