#Working with data Django-to-d3
This document explains how to pull data from a django model to power a visualization you've created using d3. In short, you will use a python template in the views.py file to place particular django data into the format that d3 needs, then feed the data in this format to your .html file where the d3 visualization lives, waiting to take data.

End goal: give d3 a javascript list of several data points. Each data point should be of the format {"nameOfFirstVariable": pt1value, "nameOfSecondVariable": pt1value, .... }, {"nameOfFirstVariable": pt2value, "nameOfSecondVariable":pt2value ...}, and so forth. We must serialize data from the relevant django model such that we have all information in this <strong> exact </strong> format of curly braces, quotation marks, colons, and commas that d3 requires. 

##Step 1: Write a function in views.py which properly serializes data
 First, make a python template. <A href https://stackoverflow.com/questions/4288973/whats-the-difference-between-s-and-d-in-python-string-formatting> This stack overflow article </A> may help, but essentially you are creating a string in the proper format of your FIRST data point, but rather than including actual data, use placeholders for values (%d for string, %s for year, etc).
 
Declare a variable template and assign it, as below, to the general format that d3 requires. The one from the QMH project, where every data point is a year associated with a count of the number of Baptists, Catholics, etc., looks something like:
 template = \
	 ''' \
	{"date": %s, "Baptist": %d, "Catholic": %d, "Dutch Reformer": %d},
	'''
  <strong> Note the level of precision here: variable names in quotes, spaces after each colon, AND a comma following the close curly brace to accommodate another data point to follow it. </strong>
  
 One weird thing about d3 is that it will take a "date" as an integer value (hence the %s) but the value of any non-preset, unique variable (such as Baptist, Catholic, and Dutch Reformer) as the string of an integer (so, we might have a data point {"date": 1830, "Baptist": "2", "Catholic": "3", "Dutch Reformer": "200"}, for example, hence the %d). 
 
 ##Step 2: Accumulate all data, properly-formatted. Loop through data in the model, fitting it into the template each time.
 
 First, declare the variable output as:
 '''
 output = \
	    ''' \
'''
Copy-paste this code exactly. The funky quotes/backslashes sets up the header of the file properly.

Next, declare a list called something like rawData. We'll use this to hold onto all the information we first grab from django before we can format it.

Third, grab your data from your django model using a loop!
Write a for loop which works '''for''' element '''in''' NAME_OF_DJANGO_MODEL'''.objects.all() and append, as its own list, to rawData. For example, the QMH map version of this looks like:
'''
rawData = []
	for e in PlaceToMap.objects.all():
		rawDataB.append([e.latitude, e.longitude, e.Name, e.Year, e.Count])
'''
Here, PlaceToMap is the name of the model, and latitude, longitute, Name, Year, and Count are the names of the data fields.

At this point, rawData is a list of lists, where each sublist is a comma-separated list of data fields for each particular data point. 

Next,


##Last Step: Hook up all your work in views.py to the d3 in your template.
When you create d3 visualizations, you must set the variable data to be the data we've organized from django. To set 
'''
var data = # the stuff we want from django
'''
follow the below format:

'''
var data = [{{MyDataName|safe}}]
'''

Note that MyDataName is the name we gave when we called ''' return render(request, #...) ''' in the view for the page in views.py.

The '''|safe''' bit is what Django calls a filter. It is included immediately after is a way to ensure the data is handed to d3 in the correct format; without it, sometimes d3 is handed some weird unicode-y version of the data (extra ',/() characters, etc.) which is of course NOT the form d3 needs to handle it. 
