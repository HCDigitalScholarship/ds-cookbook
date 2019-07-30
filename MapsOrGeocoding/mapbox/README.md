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

### Adding markers
#### using javascript's map function to retain access to the index
In the following code `place_points` is a javascript array that contains the destination coordinates I want to map (in your case it should contain whichever coordinates you want to plot). `letters` contains JSON associated with each of the points. I draw data from `letters` for the descriptions. This is why I needed to maintain access to an index.
```
const place_coordinates = place_points.map((point, index) => ({
            type: 'Feature',
            properties: {
              description: 'Title: ' + (letters['origins'][index] != undefined && 'title' in letters['origins'][index] ? letters['origins'][index]['title'] : 'Untitled') + '<br><a href=' + (letters['origins'][index] != undefined && 'dmrecord' in letters['origins'][index] ? baseurl + letters['origins'][index]['dmrecord'] : '#') + ' target=newtab >See this item in Triptych</a>' + '<br>Creation: ' + (letters['origins'][index] != undefined && 'creato' in letters['origins'][index] ? letters['origins'][index]['creato'] : 'N/A') + '<br>Origin'
            },
            geometry: {
              type: 'Point',
              coordinates: point
            }
          }));
```
**Description:** You can see that the description is HTML, so if you want breaks, pop in `<br>`'s.

#### Adding the markers as a layer
Here I add the markers as one layer. `place_coordinates` are the features to be plotted (the variable we created just now). `circle` specifies the markers will be circles. 

**Note:** you can't put addLayer in a loop, the previous addLayers in the loop are overridden even if you make sure to change the layerid. If you want to add multiple layers, you need to do the previous step again for your other array and then replicate the code below for that array.
```
mappie.addLayer({
            'id': layers[0], // string with name of your layer
            'type': 'circle', // shape of the markers
            'paint': {
              'circle-color': colors[0], // string with color code
            },
            'source': {
              'type': 'geojson', // basically geographic json
              'data': {
                'type': 'FeatureCollection', // FeatureCollection because we have a bunch of points
                'features': place_coordinates // const variable just created
              }
            }
          });
```

### Adding a legend
I found [this](https://docs.mapbox.com/mapbox-gl-js/example/updating-choropleth/) very useful for adding a legend to my map.

In my case, I added the following div to my code
```
<div id='mapdiv'></div>
<div class='map-overlay' id='legend'></div>	<div id='map-legend' class='legend'>
  <h4>Color Legend</h4>
  <div><span style='background-color: #00CED1'></span>Item Origin</div>
  <div><span style='background-color: #FF0000'></span>Item Destination</div>
</div>
```
The colors here are the colors I used for the map markers.

I added the following styling to the legend
```
.legend {
    background-color: #fff;
    border-radius: 3px;
    bottom: 30px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.10);
    font: 12px/20px 'Helvetica Neue', Arial, Helvetica, sans-serif;
    padding: 10px;
    position: absolute;
    right: 10px;
    z-index: 1;
    }

    .legend h4 {
    margin: 0 0 10px;
    }

    .legend div span {
    border-radius: 50%;
    display: inline-block;
    height: 10px;
    margin-right: 5px;
    width: 10px;
    }
```

## My map code
[JavaScript](https://github.com/HCDigitalScholarship/cope-evans/blob/master/newsite/static/js/letters.js)<br>
[HTML](https://github.com/HCDigitalScholarship/cope-evans/blob/master/newsite/templates/letters.html)



