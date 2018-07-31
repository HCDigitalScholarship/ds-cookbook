
# Working with StoryMapJS in Django
This tutorial tries to explain how to create StoryMap from XML files using data from an Excel file stored as xlsx file in a Django project.

We create the Storymaps for QI project through a custom python manage.py command in `/management/commands/<command_name>.py,` store the data for Storymap as JSON object under /static/json, and get the Storymap JSON objects through Javascript on an HTML template. 
The command is finally excuted by calling `python manage.py <command_name> <aruguments>`.
The StoryMapJS JSON object should be a dictionary in the final.The structures of the JSON objects are defined on [StoryMapJS](https://storymap.knightlab.com/advanced/)

## Before you start:
In my project:
* The data of places, locations are stored as Excel files in the order of `id_tei, name, county, state, Latitude (N), Longitude (W)` under `static/xls`as an **xlsx** file.
* All manuscripts that are going to be used has already been transcribed into XML files, and stored under `static/xml`. 
* In your models, you need to have a ***Place*** class, and it includes two attributes: latitude and longitude

## Now let's begin the work.
* **I think I am only able to make slides** 

First, under your managemnt/commands directory, create a new python file, e.g. `generate.py`.
1. Include these following lines in the beginning:
```
from django.core.management.base import BaseCommand, CommandError
import os
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree
import json
import xlrd #xlrd is a library for reading data and formatting information from Excel files, whether they are .xls or .xlsx files.
from bs4 import BeautifulSoup
from QI.models import Place   ##replace with your models.py and the model(s) you need
```
2. Start your custom manage.py command with these three lines
```
class Command(BaseCommand):
	args = 'Arguments is not needed'
	help = 'Django admin custom command'
``` 
3. add arguments that are going to be passed into the python function for generating StoryMaps later 
```
	def add_arguments(self, parser):
		parser.add_argument('xml_file', nargs='+', type=str)
```
4. define the command, and pass the arguments 
```
	def handle(self, *args, **options):
		for xml_file in options['xml_file']: 
```
`*args` allows us to pass unknown number of arguments. In this case, we can pass multipes XML files at one time.

**All the following steps from ***Step 5*** to ***Step 9*** and codes should go under `handle(self, *args, **options)`**

5. Open the `XML` file(s) and the xlsx file, parse both of them 
```
			file_name = 'static/xml/' + xml_file + '.xml'
			workbook = xlrd.open_workbook('static/xls/TEI people, places, orgs.xlsx')
                        worksheet = workbook.sheet_by_name('Places')#LOCATION, sheet_by_name is built-in function from xlrd
			tree = etree.parse(file_name)
			root = tree.getroot() 
```   
6. create a list of `<div>s or <p>s` in your XML files that you are going to iterate through, and create one slide for each onr of them.
For example, I get a list of <div>s with `type = entry` for my StoryMaps:
```
			entries = []
			for div in root.iter(ns + 'div'):
			if div.get('type') == 'entry':
			entries.append(div)
			print (entries)	
```
#You could always add `print()` in your command. Print statements will be excuted when you run `python manage.pt command_name arguments`. They will be helpful in debugging. 

7. Create a empty python list that will hold each slide of the StoryMap at the end
* **Overview** : Get the content and attributes of each slide of the map, create a dictionary for each slide of your StoryMap, then a python array to hold each slide of your storymap, finally a dictionary which includes the python array and other attributes of the StoryMap.
```
			objects=[]
```
8. Iterate thorugh the list your have made in ***Step 6***, and get the content you want to put into your StoryMap from XML file:
e.g.:
```
			for f, e in enumerate(entries):
				div_text = ''
  			 	for child in e:
					if child.tag == 'p':
						text = etree.tostring(child, method='text')
						div_text == div_text+ "<br>" + child.text
						#because in my case, each entry has multiple <p>s
```				

For strings in headline, text, url, caption…, if you are intersted to see how we get them from xml files and our database, please check [generate.py].

9. Get the location on each slide of the map
i). you should be able to get the location from tags in your XML files under `<dateline>` tags,which should look like
`#<dateline><date when="xxx">xxx</date>.<placeName key="zz">yyy</placeName></dateline>` <br/>
Under `for child in e:`, on the same level of `if child.tag == 'p':` in ***Step 6***
```
						if child.tag == "dateline":
							dateline = child
							for child in dateline:
								if child.tag == ns + "placeName":
									place = child.get("key")
```
ii). Get latitude and longitude of the place from your database
```
				dj_place_list = Place.objects.filter(id_tei=place) #this list should only have one object at most
				if dj_place_list==None or dj_place_list==list() or len(dj_place_list)==0: 		
					print (place, "not found in database \n")
					#if the place is not in database, we can't create a StoryMap slide for it.
				else: 
					for i in dj_place_list:
						if i.latitude != None:
							dj_place = i 
							break
							 #if it passes the if statement, skip the loop 
						else:
							dj_place = i
							# either case will allow us to get the only object in dj_place_list
					lat = dj_place.latitude
					lon = dj_place.longitude
```
iii). StoryMapJS requires the input of latitude and longitude to be of float type. Therefore, we make them float; otherwise, we can default latitude and longitude. StoryMapJS requires the input of latitude and longitude to be of float type. Therefore, we make them float; otherwise, we can default latitude and longitude. 
```
					if lat =="" or lon== "":
						print ("No lat or lon for",place,"I set this to lat to 42 and lon to 83. \n")
						lat = 42 #LOCATION
						lon = 83#LOCATION
					else:
						print (place, "had lat, lon:",lat,lon,"\n")
					try:
						float(lat)
					except ValueError:
						print ("People are bad at entering data, lat for this is:", lat)
						lat = 42
						print ("set lat to 42")
					try:
						float(lon)
					except ValueError:
						print ("People are bad at entering data, lon for this is:", lon)
						lon = 83
						print ("set lon to 83")	
```
10. create JSON object following the syntax on https://storymap.knightlab.com/advanced/

i). Create a python array to hold each slide of your storymap.
Under `for f, e in enumerate(entries):` in ***Step 8***, at the same level of `for child in e:`
```
  				object = {
          				"location": {            // required for all slides except "overview" slide
          				"lat": lat,      // latitude of point on map, has to be decimal
		  			"lon": lon,       // longitude of point on map, has to be decimal
      				     },
      					"text": {                // optional if media present
        				"headline": string,
         				"text": div_text      // div_text in this examplemay contain HTML markup, has to be string 
     				     },
      					"media": {               // optional if text present
         			        "url": string,       // url for featured media
          				"caption": string,   // optional; brief explanation of media content
          				"credit": string     // optional; creator of media content
      				     }
  				}
  objects.append(object) #add each slide
```
**For strings in headline, text, url, caption…, if you are intersted to see how we get them from xml files and our database  please check [`generate.py from QI`](https://github.com/HCDigitalScholarship/QI/blob/e42ddab2bece8fb36168b936a46278a6d49d8c94/QI/management/commands/generate.py)

**I seperate lines for convenience to read, but in `generate.py`, put them on one line.** <br/>
ii). Add a slide of overview to be the first page of your StoryMap.
**After finishing the loop** `for f, e in enumerate(entries):`, put:
```
		cover = {
    			"type": "overview",      // optional; if present must be set to "overview"
       		 	"text": {                // optional if media present
        			"headline": string,
        			"text": string       // may contain HTML markup	
    			},
    			"media": {               // optional if text present
        			"url": string,       // url for featured media
        			"caption": string,   // optional; brief explanation of media content
        			"credit": string     // optional; creator of media content
    			}
		}
		objects.insert(0,cover)
```
iii). Put the `objects` list into the required data format 
```
		Map ={
		    "width": integer,                // required for embed tool; width of StoryMap
    		    "height": integer,               // required for embed tool; height of StoryMap
    		    "font_css": string,              // optional; font set
		    calculate_zoom: true,              // optional; defaults to true.
		    storymap: {
		        language: string,          // required; two-letter ISO language code
		        map_type: string,          // required
		        map_as_image: false,       // required
		        map_subdomains: string,    // optional
		        slides: objects           // required; array of slide objects we have created before
   		      }
		  }
```
		
11.  create a json file in static to hold your Storymap
```
		data = map
		with open('static/json/' + xml_file + '.json', 'w') as outfile:
				json.dump(data, outfile, sort_keys=True)
```

12.  Create an HTML template under `/templates/storymaps` to hold your StoryMap in `generate.py`, include Javascript for StoryMap in it.
```
		html_str =""" {% load staticfiles%}
             <!doctype html>
<html class=”no-js” lang=”en”>
<head>
<title>"""+ xml_file + """ StoryMapJS </title>
    <link rel="stylesheet" href="https://cdn.knightlab.com/libs/storymapjs/latest/css/storymap.css">
</head>

<body>
<div>
<div id = "story1" style = "background-color: #F0F8FF;">
	   <div>
	      <br />
	      <h2 class = "text-center" style = "font-family: 'Alegreya Sans SC'; font-weight: 400; color: black"> StoryMap for """+ xml_file + """</h2>
	        <!-- The StoryMap container can go anywhere on the page. Be sure to 
    specify a width and height.  The width can be absolute (in pixels) or 
    relative (in percentage), but the height must be an absolute value.  
    Of course, you can specify width and height with CSS instead -->
    <div id="mapdiv" style="width: 90%; height: 600px; margin:auto"></div> 
    <br />
    <br />
	  </div>  
</div>

<!-- Your script tags should be placed before the closing body tag. -->
    <script type="text/javascript" src="https://cdn.knightlab.com/libs/storymapjs/latest/js/storymap-min.js"></script>
     <script>
  // storymap_data can be an URL or a Javascript object
 
      //var storymap_data = "{% static "json/StoryMapData.json" %}"; 
      var storymap_data = "{% static "json/""" + xml_file + """.json" %}"; 
      
      // certain settings must be passed within a separate options object
      var storymap_options = {};
      var storymap = new VCO.StoryMap('mapdiv', storymap_data, storymap_options);
      window.onresize = function(event) {
          storymap.updateDisplay(); // this isn't automatic
      }          
  </script>
  
  
  </body>
</html>""" 

		html_file = open('templates/story_maps'+xml_file+'.html','w')
		html_file.write(html_str)
		html_file.close()
```
13. If you want a page as a menu which  lists all the StorMaps you have created, create another html templates `list_of_storymaps.html`
```
		newfile=""
		with open('templates/list_of_storymaps.html', 'r+') as f:
		html_as_string=f.read()
		soup = BeautifulSoup(html_as_string, 'html.parser')
		sml = soup.find(id='storymaplist')
		links = soup.find_all('a')
		newtag= soup.new_tag('a', id='SMLink', href=xml_file)
		atag= soup.new_tag('a', href=xml_file)
		imgtag= soup.new_tag('img', src='path to the image you want')
		litag = soup.new_tag('li', id='SMListitem')
		divtag = soup.new_tag('div', id="SMtext")
		divtagimg = soup.new_tag('div', id="SMimgdiv")
		soup.ul.append(litag)
		litag.append(atag)
		atag.append(divtagimg)
		divtagimg.append(imgtag)
		atag.append(divtag)
		divtag.append(newtag)
		newtag.string = title_fin
		newfile = soup.prettify()
		with open('templates/list_of_storymaps.html','w') as f:
		     f.write(newfile)
```
14 In your project directory:
`python manage.py generate XML_file`
