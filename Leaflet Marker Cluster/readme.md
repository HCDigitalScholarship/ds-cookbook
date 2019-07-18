# Using Leaflet and the Marker Cluster Plugin
![ Google map point field widget ](https://github.com/fgould/ds-cookbook/blob/patch-1/Leaflet%20Marker%20Cluster/Screen%20Shot%202019-07-18%20at%203.17.56%20PM.png)

[Leaflet](https://leafletjs.com/) is a beautiful, lightweight javascript library that can be used to create interactive maps with any number of possible uses. Integrated with **GeoDjango** in our models/database, we have the tools to deal with large amount of spatial data and the easy ability to serve up that data on our templates for the user to interact with. If you don't know your way around GeoDjango and spatial database elements, I suggest getting aclimated with some reading first:

* [GeoDjango Documentation](https://docs.djangoproject.com/en/2.2/ref/contrib/gis/)
* [Cookbook entry](https://github.com/HCDigitalScholarship/ds-cookbook/tree/master/GeoDjango%20and%20Geocoding)

Now that we've gotten started, we can begin to create leaflet maps and then apply clustering. But first:

## 1. Dependencies
* Follow the installation instructions on the [documentation](https://github.com/Leaflet/Leaflet.markercluster) **OR**
* Include these lines at the start of each template where you use a cluster map for most of the functionality and style
```
<script src="https://unpkg.com/leaflet.markercluster@1.4.1/dist/leaflet.markercluster.js"></script>
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.Default.css">
```
* Make sure GeoDjango is installed and compatible with your database because djangos default sqlite won't be enough. Configuration can be found on the [GeoDjango Setup](https://docs.djangoproject.com/en/2.2/ref/contrib/gis/tutorial/#setting-up) 

## 2. Creating spatial model fields
### a. The basic PointField
Assuming you have already set up a django project and have a working database/admin site, we can begin to add spatial fields to models which we may want to map. In this example I create a person model and give it a [PointField](https://docs.djangoproject.com/en/2.2/ref/contrib/gis/model-api/) that references the person's location. 
```
from django.contrib.gis.db import models

class Person(models.Model):
        geom = models.PointField(null=True)
        name = models.CharField(max_length=200)
        city = models.CharField(max_length=200)
```
Now add whatever and however many people and locations you wish, the good thing about marker cluster is even if points are in the exact same location, we can still display them both!
### b. Adding popups 
A common use for our spatial data is to display it with a popup that gives some information we wish to convey to the user on a click or hover. To add popup information to each instance of a model, we add the @property popupcontent to the model.
```
        @property
        def popupcontent(self):
                return '<p>{} is currently in {}</strong>'.format(self.name, self.city)
```
Now each marker on the map will display its corresponding person's name and location! This method has the capability to do much more, but is dependent on its model fields and the queries that you may want to run within the method.

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
Here we begin to use Leaflet and Marker Clustering. After registering your template and its view in urls.py, you can begin adding the JavaScript to integrate the map.
### a. Create a map and a layer to put tiles on
Along with the following code, make sure to set up properly with [leaflet](https://leafletjs.com/examples/quick-start/) and clustering as mentioned above. Then add a map and a tile layer:
```
index.html

var mymap = L.map('mapid').setView([50.332721, 1.050860], 5);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
                '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
                'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox.streets'
}).addTo(mymap);

```
Feel free to edit around where you want to set the view, the max zoom, etc.

### b. Create your own icon
This creates a classic violet popup icon which will later be filled in with data from our model
```
       var violetIcon = new L.Icon({
  iconUrl: 'https://github.com/pointhi/leaflet-color-markers/raw/master/img/marker-icon-2x-violet.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});
```
### c. Pass in data and add it to the map
First, we create a new MarkerClusterGroup, making the following markers appear in a cluster (the circle with the numbers). As you zoom in, clusters will decrease in number or turn into single points. If there are multiple points at one location, the points will "spiderfy" out. For an example, look [here](https://leaflet.github.io/Leaflet.markercluster/example/marker-clustering-realworld.388.html). This behavior is incredibly useful to prevent points from stacking, and to neatly display what may be a massive amount of data.
```
var mcg = new L.MarkerClusterGroup();     
```
Next we will pass in our list of spatial data that we created in the view. It will get converted to json readable format that is safe for leaflet to begin working with
```
var people = {{ people|geojsonfeature:'popupcontent'|safe }};
```
Now we do the adding to the map by creating a layer with the spatial data we passed in as var people. For each element of spatial data the template will add a marker to the layer and have that marker display the popupcontent which we specified earlier in the model popupcontent.
```
var peopleLayer = L.geoJSON(people, {
  pointToLayer: function (feature, latlng) {
            return L.marker(latlng, {icon: violetIcon});
 },

  onEachFeature: function(feature, layer) {
      var props = feature.properties.popupcontent;
      var content = `<p>${props}</p>`;
      layer.bindPopup(content);
  }
});
mcg.addLayer(ownerLayer);
mymap.addLayer(mcg);
```
Now our data is added to the map. Reload your server and it should display something that looks like our examples. It should be noted this is the bare minimum you can do with spatial data and marker clustering. The marker cluster [documentation](https://github.com/Leaflet/Leaflet.markercluster) gives us numerous more ways to customize zoom levels, cluster display icons, spiderfy settings, etc. The leaflet [documentation](https://leafletjs.com/reference-1.5.0.html) is also worth digging into to explore the different ways you can display interactive data in a similar manner, and gives great examples on how to do more with maps, layers, markers, etc.
