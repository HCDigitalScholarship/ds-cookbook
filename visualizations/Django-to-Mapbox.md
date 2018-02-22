# Working with data Django-to-Mapbox
This document explains how to pull data from a django model into a Mapbox layer. In short, you will use a python template in the views.py file to create a mapbox FeatureCollection of geoJSON data. 

End goal: give mapbox a javascript list of several data points in the proper geoJSON format, also in accordance with Mapbox's FeatureCollection data category. The generalized format is:
``` 
"coordinates" : [latitude, longitude]},
"properties" : { "NameOfProperty1" : "Value1", "NameOfProperty2" : "Value2"} 
```
and so forth. We must serialize data from the relevant django model such that we have all information in this exact format of curly braces, quotation marks, colons, and commas that Mapbox requires.	    

(Aside: newer versions of django have a built-in geoJSON serializer which was ridiculously/surprisingly difficult to install. Stop reading if you can figure that out tho!)

## Step 1: Write a helper function in views.py to properly serialize data from the model you're working with.
In views.py, define a helper function. It might be something like:
```
def mapData_ToGeoJSON():
``` 
Within this function, make a python template. [This stack overflow article](https://stackoverflow.com/questions/4288973/whats-the-difference-between-s-and-d-in-python-string-formatting) may help, but essentially you are creating a string in the proper format of any single data point, except that rather than including actual data, use placeholders for values (%d for string, %s for integers, etc). In other words, include every variable you want to have mapbox ultimately work with in proper geoJSON format with a placeholder for each variable's value.
 
To do so, declare a variable template and assign it, as below, to the geoJSON that mapbox requires. Below is a template from the QMH Map projec, which relied on a place Name, Year, and Count in addition to a place latitude/longitutde coordinate. It looked like:
```
def mapData_ToGeoJSON():

template = \
	    ''' \
	    {"type" : "Feature",
	        "geometry" : {
	        "type" : "Point",
	        "coordinates" : [%s,%s]},
	    "properties" : { "Name" : "%s", "Year" : "%s", "Count": "%s"}
	    },
	'''
```
Copy and past the variable template declaration, replacing each of the data field names ("Name", "Year", and "Count" in this example) with those which match the data fields of the Django model you're working with, preserving the double quotation marks, and changing the letter after each % to match the type of the expected value. To clarify, "Name", "Year", and "Count" are both the names of attributes for each data point in Django and the names of the properties I used in geoJSON, which I found helped keep things straight! 
<strong> It is important to keep the leading \ and opening/closing ''' (triple-single-quotes) so Mapbox can read everything properly </strong>.

Note the level of precision here: variable names in quotes, spaces after each colon, <strong> AND a comma following the close curly brace </strong> to anticipate that another data point will follow it. 
  
 ## Step 2: Accumulate all data, properly-formatted. Loop through data in the model, fitting it into the template each time.
 Now, we want to effectively grab all of our data from Django, force it through our tailored template one data point at a time, and collect up all of the properly-formatted data into a big list. 
 
 First, declare the variable output as:
 ```
 # the head of the geojson file
	output = \
	    ''' \
	
	    '''
```
Copy-paste this code exactly. The funky quotes/backslashes sets up the header of the file properly. Ultimately, output is what this mapData_ToGeoJSON() function will return.

Next, declare an empty list called something like rawData. We'll use this to hold onto all the information we first grab from django before we can format it. Then, grab your data from your django model using a loop! Write a for loop which works ```for``` element ```in``` NAME_OF_DJANGO_MODEL```.objects.all()``` and append, as its own list, to rawData. For example, the QMH map version of this looks like:
```
# the head of the geojson file
	output = \
	    ''' \
	
	    '''
	    
rawData = []
	for e in PlaceToMap.objects.all():
		rawData.append([e.latitude, e.longitude, e.Name, e.Year, e.Count]) #Note that we're appending a list here. 
```
Here, PlaceToMap is the name of the model, and latitude, longitute, Name, Year, and Count are the names of the data fields. This is the django way to talk about a model's data points and data fields in views.py! Note that this ordering matches our template exactly: geoJSON wants latitude and longitude first (in the "coordinates" fields) then our properties in arbitrary but particular order we specified when we made the template. 

At this point, rawData is a list of lists, where each sublist is a comma-separated list of data fields for each particular data point. 
Now, we want to force all of this raw data, one point at a time, through the template we made and accumulate it into a variable to return. 
The code for this step from the QMH example looks like:
```
for row in rawData:
	lat = row[0]
	lon = row[1]
	name = row[2]
	year = row[3]
	count = row[4]
	output += template % (row[0], (row[1]), row[2], row[3], row[4])
```
In short, for each element of rawData, shove that data into the template and then accumulate into the output variable, which we'll return in the next step. One trick to this whole process is to remember the order in which you are pulling and placing each field's values; we know the value corresponding to latitute comes first since we append it to rawData first, etc. Be careful to not mix up data values! That's why variables lat, lon, name, year, and count are declared even though we don't end up actually using them :). 

Simply modify this for loop to fit your data, keeping in mind that the 0th item of each sublist in rawData corresponds to the first data field, the 1st to the second, etc. 

## Step 3: Returning the formatted data
Now that we have all of our data in the proper templated format all together in the variable ```output```, the last lines of this function should be:
```
output += \
	    ''' \
	    ]
	}
	    '''
	return(output)
```
After we put all of the templated data into output, this adds the close braces and brackets we need to complete the picky geoJSON format.


Now, all that's left is to put this output in the right place to hand to the template where the javascript code for our map is waiting for a data source.

Somewhere else in views.py, you should have a function which renders each template. An example: The ```causes``` function below, for example, simply enables the FriendsVIS.html template to be loaded when users request the page marked "causes". There should be a bunch of similar functions just like this in views.py, so all your templates can be loaded! 
```
def causes(request):
	return render(request, 'FriendsVIS.html')
```

In whichever rendering function is relevant to the data/template you're using, declare some variable to hold the result of the formatting function we just wrote. This function should return a rendering of the proper template, plus some funny django business:

```
def some_relevant_name(request):
	places_list = mapData_toGEOJSON()
	return render(request, 'QMHMap.html', {'places': places_list})
```

The above code creates a variable with the formatted data we just made in mapData_toGEOJSON(), places_list, and says that when the QMHMAP.html page is loaded, django will know to pass the places_list data <strong> and will call it places when we want to talk about this data in the .html file. </strong>

You can call these things whatever you want, but the curly braces, single quotes, and colon are important! 


## Step 4: Hook up all your work in views.py to the Mapbox code in your template.
When you create a mapbox map in your .HTML file, you must set the map source variable to be the data we've just organized from django.

Under the declaration for ``` var map = new mapboxgl.Map({ //....}); ``` and within (and towards the top of) the ```map.on('load', function(){ ``` Follow the below format:
```
     map.addSource("django-data", {
            "type": "geojson",
            "data": { "type" : "FeatureCollection",
            "features" : [{{places|safe}}, 
        }) //If this extra parenthese goes away, the whole map breaks. It looks like it's extra, but it closes the GeoJSON format. 
```

Here, <strong> we name our data django-data (which can change to be whatever you'd like) </strong> and specify that it's a FeatureCollection where each feature is the stuff from places, which we just named our templated variable from views.py. 

The ```|safe``` bit is what Django calls a filter. It is included immediately after as a way to ensure the data is handed to d3 in the correct format; without it, sometimes d3 is handed some weird  version of the data (extra characters like &lt, &#39, &amp, all over the place!) which is of course NOT the form d3 needs to handle it. [Check out this link](https://docs.djangoproject.com/en/1.7/topics/templates/) and scroll to the "Automatic HTML Escaping" section for details. 

Pretty much everthing above you should copy and paste into the top of your 'on load' function, just making sure to change the information after ```"features" : ``` to match whatever name you used for "the stuff to be returned" in views.py. Note that in the code above, places is the name we gave when we called ``` return render(request, #...) ``` in the view for the page in the previous step, just without the single quotes. 

Also heed the comment about the extra parentheses! At least in Alison's text editor, this close parenthese is highlighted as if it's a problem, but if you delete it, the whole map breaks...

It's also important that we have the list ([ ]) around ```{{places|safe}}```—all of the features must be as a list. 

In summary, you've taken each data entry from django, fitted it into the applicable GeoJSON format, given the formatted data a name to talk about upon the relevant template's load, then told Mapbox to populate the map with a FeatureCollection of the information we're calling by that same name. But all of this has been just to establish the django data as a distinct (properly-formatted) data source. next, we have to add it to a layer!

## Step 5: Add Visual Data to a Layer
From here on, I'll include the information to turn the data about each point into circles of varying size and color [using mapbox stops](https://www.mapbox.com/help/how-map-design-works/) but some bits of this may be modified and extended as needed (for example, the QMH project also hooks the circle generation up to a date slider, etc.). But no matter what you do, you first have to append data to a layer, as so:

```
 map.addLayer({
        'id': 'QMH_Hometowns',
        'type': 'circle',
        "source": "django-data",
         'paint': {
```

Here, I create a layer with id QMH_Hometowns (IMPORTANT: this must be consistent with any layer ID if you ever work on this project in mapbox studio, but no biggie otherwise), specify that each data point should be represented as a circle, <strong> and that this layer's data source should be what we called django-data above </strong>. 

Within paint, we draw our circles! <strong> The beauty of all of what we've done is that Mapbox lets you paint by data field (i.e. property in django) </strong>

An example is the best way to see this. Here is what this looks like in the QMH Map project (with some of the stops omitted to save space):

```
//Creates a layer called QMH_Hometowns, populated by circles, whose source is the django-data from above and who is styled as specified below:
        map.addLayer({
        'id': 'QMH_Hometowns',
        'type': 'circle',
        "source": "django-data",
        //'source-layer': 'QMH_Hometowns',
         'paint': {
              'circle-opacity': 0.6,
            // Makes size proportional to # of people
       'circle-radius': {
                property:"Count",
                type:'categorical',
                stops:[
                    ['0', 0], ['1',8], ['2',9], ['3',10], ['4',11], ['5',12],['6',13], ['7',13], ['8',13], ['9', 14], ['10',14],
                    ['11',14]
		    ] 
		    },
	'circle-color':{
                 property:"Year",
                 type:'categorical',
                 stops: [
                    ['1817', '#f7d5a1'],
                    ['1818', '#f7d5a1'],
                    ['1819', '#f5cc8e'],
                    ['1820', '#f5cc8e'],
                    ['1821', '#f4c47c'],
                    ['1822', '#f4c47c'],
                    ['1823', '#f2bb69']
		    ]
		       },
        }); //end of addLayer
		    
		    
```	

Each <strong> stops </strong> field is a list of lists, where each sublist corresponds to ['data value', what-to-assign-to-that-data-value]. So, I set the circle radius to depend on the <strong>property<strong> Count, where a count of 0 has a radius of zero, a count of 1 has a radius of 8, and so on. Then, I set the circle color to depend on the Year <strong>property<strong>, where each year is given its own hexcolor [made with this handy site](https://coolors.co/484538-cad49d-43aa8b-d4eac8-c0d8e0) (but also [check out this link for super handy color-picking for super advanced webdev](https://color.hailpixel.com) and mouse around for hue, scroll for saturation). 

Anyways:
After all of this, I have the closing brace and parenthese to end the addLayer function. 

You should be all done, and see circles representing your django model!

## Note:
This method assumes that all of your data has been collected and tallied appropriately before you even entered it into Django. If this is not the case (data entries represent individual observations, which you would like to collect in some way and display these aggregations) you can add another step to tally up data in views.py. It really depends on what you're doing, but look to the TotalReligionDiversityData_toJSON() function in the QMH project's views.py to see an example. 

## Contributors :tada:
:octocat: [Alison Rosenman](https://github.com/alisonrosenman) :information_desk_person:
