# Using Mapbox for Data Visualization
## Overview
### Context
I created a [map](https://165.227.217.17/letters) that shows the origin and destination data of all the items in the Cope Evans Family Papers that have that data. The links on the map lead to Triptych (whose software is called CONTENTdm). This is where Haverford’s digitized collections live.

To make this map, I batch-queried the CONTENTdm server for the metadata (JSON) of the 5008 items using the requests library in a Python script. I then took this data and wrote Python scripts to batch-geocode using Mapbox’s geocoding API. I then added this information onto each item in the original JSON I received from the query. As an optimization to increase page load time, I deleted any attributes of the items that were not being served to the user and minified my JSON file.

Mapbox is not the difficult part. The hard part is getting the data in the right format and with the correct relation to the data you start with (not losing their relationship)

### Tools
1. Mapbox dynamically-rendering map (in contrast to a static map with which you would use Web Mercator math to plot coordinates).
2. [Mapbox's Geocoding API](https://docs.mapbox.com/api/search/#geocoding) to forward geocode (go from place name to location)

### Dead ends
1. [Google Maps Geocoding](https://developers.google.com/maps/documentation/): the data came out in JSON, but the JSON array returned by the service was greater than the number of requests made to the API. The data wasn't associative, so I decided to switch to Mapbox.
2. Dash: I had trouble configuring this for some reason, so I opted for chart.js

## Steps to create a map
### Account Creation
You need an API access token to associate your requests to your account. Also, there's an upper limit of how many geocoding requests and how many times you can serve a map to a user. Mapbox is pretty generous with these.

### A [base map](https://docs.mapbox.com/mapbox-gl-js/example/simple-map/)
```
<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8' />
<title>Display a map</title>
<meta name='viewport' content='initial-scale=1,maximum-scale=1,user-scalable=no' />
<script src='https://api.tiles.mapbox.com/mapbox-gl-js/v1.1.1/mapbox-gl.js'></script>
<link href='https://api.tiles.mapbox.com/mapbox-gl-js/v1.1.1/mapbox-gl.css' rel='stylesheet' />
<style>
body { margin:0; padding:0; }
#map { position:absolute; top:0; bottom:0; width:100%; }
</style>
</head>
<body>
 
<div id='map'></div>
<script>
mapboxgl.accessToken = '<your access token here>';
var map = new mapboxgl.Map({
container: 'map', // container id
style: 'mapbox://styles/mapbox/streets-v11', // stylesheet location
center: [-74.50, 40], // starting position [lng, lat]
zoom: 9 // starting zoom
});
</script>
</body>
</html>
```
**Note:** You might have to change `var map` to something else like `var mymap`. This is because javascript has a map function, and doesn't want you naming variables map.
#### var map
This is your map variable. I will give a brief overview of its attributes.
#### container
Here, put the name of the div you want your map to appear in. In this case we want `map` because `<div id='map'></div>` is our div.
#### style
The style attribute points to a style sheet for your map. You can create one on the Mapbox site and it will be associated with your Mapbox account.
#### center 
The code above renders a mapbox map centered at someplace in New Jersey whose coordinates are [-74.50, 40]. The format is [longitude, latitude]. 
#### zoom
You can use this to change how close up the map starts to the center.

### Adding a legend
I found [this](https://docs.mapbox.com/mapbox-gl-js/example/updating-choropleth/) very useful for adding a legend to my map.



