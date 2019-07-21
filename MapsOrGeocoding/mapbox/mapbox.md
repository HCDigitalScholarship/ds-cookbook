
### I used
1. Mapbox dynamically-rendering map (in contrast to a static map with which you would use Web Mercator math to plot coordinates).
2. Mapbox's Geocoding API to forward geocode (go from place name to location)

### What did not work
1. Google Maps Geocoding: the data came out in JSON, but the JSON array returned by the service was greater than the number of requests made to the API. The data wasn't associative, so I decided to switch to Mapbox.

### Overview of my process and what I made:
I created a map that  shows the origin and destination data of all the items in the Cope Evans Family Papers that have that data. The links on the map lead to Triptych (whose software is called CONTENTdm). This is where Haverford’s digitized collections live.

To make this map, I batch-queried the CONTENTdm server for the metadata (JSON) of the 5008 items using the requests library in a Python script. I then took this data and wrote Python scripts to batch-geocode using Mapbox’s geocoding API. I then added this information onto each item in the original JSON I received from the query. As an optimization to increase page load time, I deleted any attributes of the items that were not being served to the user and minified my JSON file.

Mapbox is not the difficult part. The hard part is getting the data in the right format and with the correct relation to the data you start with (not losing their relationship)