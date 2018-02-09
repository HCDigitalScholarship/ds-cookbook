# Working with data Django-to-d3
This document explains how to pull data from a django model to power a visualization you've created using d3. In short, you will use a python template in the views.py file to place particular django data into the format that d3 needs, then feed the data in this format to your .html file where the d3 visualization lives, waiting to take data.

End goal: give d3 a javascript list of several data points in the proper JSON format:
```{"nameOfFirstVariable": pt1value, "nameOfSecondVariable": pt1value, .... }, {"nameOfFirstVariable": pt2value, "nameOfSecondVariable":pt2value ...},``` 
and so forth. We must serialize data from the relevant django model such that we have all information in this <strong> exact </strong> format of curly braces, quotation marks, colons, and commas that d3 requires. 

(Aside: newer versions of django have a built-in JSON serializer which was ridiculously/surprisingly difficult to install. Stop reading if you can figure that out tho!)

## Step 1: Write a helper function in views.py to properly serialize data from the model you're working with.
In views.py, define a helper function. It might be something like:
```
def modelDataToJSON():
``` 
Within this function, make a python template. [This stack overflow article](https://stackoverflow.com/questions/4288973/whats-the-difference-between-s-and-d-in-python-string-formatting) may help, but essentially you are creating a string in the proper format of any single data point, except that rather than including actual data, use placeholders for values (%d for string, %s for integers, etc). In other words, include every variable you want to have d3 ultimately work with in proper JSON format with a placeholder for each variable's value.
 
To do so, declare a variable template and assign it, as below, to the general format that d3 requires. In the case of the QMH project example, a d3 stacked bar graph shows tallies of hospital patients by year, broken down into their religious affiliations. So, the template for this looks like:
```
def modelDataToJSON():

 template = \
	 ''' \
	{"date": %s, "Baptist": %d, "Catholic": %d, "Dutch Reformer": %d},
	'''
```
Copy and past the variable template declaration, replacing each of the data field names with those relevant to your project, preserving the double quotation marks, and changing the letter after each % to match the type of the expected value. <strong> It is important to keep the leading \ and opening/closing ''' (triple-single-quotes) so d3 can read everything properly </strong>.

Note the level of precision here: variable names in quotes, spaces after each colon, <strong> AND a comma following the close curly brace </strong> to accommodate another data point to follow it. 
  
One weird thing about d3 is that it will take a "date" as an integer value (hence the %s) but the value of any non-preset, unique variable (such as Baptist, Catholic, and Dutch Reformer) as the string of an integer (so, we might have a filled-in data point {"date": 1830, "Baptist": "2", "Catholic": "3", "Dutch Reformer": "200"}, for example, hence the %d). 
 
 ## Step 2: Accumulate all data, properly-formatted. Loop through data in the model, fitting it into the template each time.
 Now, we want to effectively grab all of our data from Django, force it through the template one data point at a time, and collect up all of the properly-formatted data into a big list. 
 
 First, declare the variable output as:
 ```
 output = \
	    ''' \
```
Copy-paste this code exactly. The funky quotes/backslashes sets up the header of the file properly. Ultimately, output is what this modelDataToJSON() function will return.

Next, declare an empty list called something like rawData. We'll use this to hold onto all the information we first grab from django before we can format it. Then, grab your data from your django model using a loop! Write a for loop which works ```for``` element ```in``` NAME_OF_DJANGO_MODEL```.objects.all()``` and append, as its own list, to rawData. For example, the QMH map version of this looks like:
```
rawData = []
	for e in PlaceToMap.objects.all():
		rawData.append([e.latitude, e.longitude, e.Name, e.Year, e.Count])
```
Here, PlaceToMap is the name of the model, and latitude, longitute, Name, Year, and Count are the names of the data fields. This is the django way to talk about a model's data points and data fields in views.py!

At this point, rawData is a list of lists, where each sublist is a comma-separated list of data fields for each particular data point. 
Now, we want to force all of this raw data, one point at a time, through the template we made and accumulate it into a variable to return. 
The code for this step from the maps example looks like:
```
for row in rawData:
	lat = row[0]
	lon = row[1]
	name = row[2]
	pop = row[3]
	output += template % (row[0], (row[1]), row[2], row[3], row[4])
```
In short, for each element of rawData, shove that data into the template and then accumulate into the output variable, which we'll return in the next step. One trick to this whole process is to remember the order in which you are pulling and placing each field's values; we know the value corresponding to latitute comes first since we append it to rawData first, etc. Be careful to not mix up data values! That's why variables lat, lon, name, and pop are declared even though we don't end up actually using them :). 

Simply modify this for loop to fit your data, keeping in mind that the 0th item of each sublist in rawData corresponds to the first data field, the 1st to the second, etc. 

## Step 3: Returning the formatted data (and doing it with each template!)
Now that we have all of our data in the proper templated format all together in the variable ```output```, the last line of this function should be:
```
return output
```
Now, all that's left is that we have to put this output in the right place to hand to the template where our d3 visualization is waiting for a data source.

Somewhere else in views.py, you should have a function which renders each template. An example: The ```causes``` function below, for example, simply enables the FriendsVIS.html template to be loaded when users request the page marked "causes". There should be several similar functions just like this in views.py, so all your templates can be loaded! 
```
def causes(request):
	return render(request, 'FriendsVIS.html')
```

In whichever rendering function is relevant to the data/template you're using, declare some variable to hold the result of the formatting function we just wrote. This function should return a rendering of the proper template, plus some funny django business:

```
def some_relevant_name(request):
	resultFromFormatting = modelDataToJSON()   ###store the result of modelDataToJSON(), namely, output. 
	return render(request, 'NAME_OF_HTML_FILE_WHERE_D3_VIS_EXISTS.html', {'formattedData': resultFromFormatting})
```

The above code creates a variable with the formatted data, resultFromFormatting, and says that when the NAME_OF_HTML_FILE_WHERE_D3_VIS_EXISTS.html page is loaded, django will know to pass the resultFromFormatting data and will call it formattedData. 

You can call formattedData and both places you use resultFromFormatting whatever you want, but the curly braces, single quotes, and colon are important! 


## Last Step: Hook up all your work in views.py to the d3 in your template.
When you create d3 visualizations in your .HTML file, you must set the variable data to be the data we've just organized from django.  To set 
```
var data = // the stuff we want from django
```
follow the below format:

```
var data = [{{formattedData|safe}}]
```

Note that formattedData is the name we gave when we called ``` return render(request, #...) ``` in the view for the page in the previous step, just without the single quotes. 

The ```|safe``` bit is what Django calls a filter. It is included immediately after as a way to ensure the data is handed to d3 in the correct format; without it, sometimes d3 is handed some weird  version of the data (extra characters like &lt, &#39, &amp, all over the place!) which is of course NOT the form d3 needs to handle it. [Check out this link](https://docs.djangoproject.com/en/1.7/topics/templates/) and scroll to the "Automatic HTML Escaping" section for details. 

It's also important that we have the list ([ ]) around ```{{formattedData|safe}}```—d3 takes multiple JSON elements as a list. 


In summary, you've taken each data entry from django, fitted it into the applicable JSON format, given the formatted data a name to talk about upon the relevant template's load, then told d3 that the visualization's data = that same name. You should be all done now!

## Note:
If you take a look at the ReligionDiversityData_toJSON() and TotalReligionDiversityData_toJSON() functions in the QMH project's views.py, you'll see that this process is not so simple. That's because, unlike with the map data, the data for the religious diversity feature had not been tallied. Basically, after I had the initial loop ```for e in ReligiousDiversityData.objects.all```, I then used some extra accumulators and lists etc. to tally up data by year and religion. This extra wrinkle is tedious but allows for new data to be entered easily; a new discovery of a non-quaker patient need not affect the value of any stored total/tally, since django does all the tallying itself after data entry.

## Contributors :tada:
:octocat: [Alison Rosenman] (https://github.com/alisonrosenman) :information_desk_person:
