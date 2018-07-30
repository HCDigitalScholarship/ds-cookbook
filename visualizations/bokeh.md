# Working with Bokeh and postegresql/csv and ngnix/systemd configuration and Django
This document explains how to use Bokeh and pull data from a postgresql database or a csv to power a visualization you've created. 

End goal: give Bokeh data from postgresql database or a csv while being able to run the Bokeh server simulanteously as the current server you are working on.

## Step 1: Make sure Bokeh is downloaded
  Go to Bokeh's documentation and gallery in order to see the installation process and inspiration on what kind of visualization you want: https://bokeh.pydata.org/en/latest/
## Step 2: Create the Bokeh visualization
  First create a separate python file for the visualization you want to create in the project folder. Import all the necessary Bokeh packages that pretain to your visulization.
  ### Using postgresql data
  Make sure you have psycopg2 is installed in your virtualenv by doing
  ```
  pip freeze
  ```
  in your terminal and seeing if psycopg2 is there. If it is then in order to use the postgresql database do 
  ```
import psycopg2
import psycopg2.extras
try:
        conn = psycopg2.connect("dbname='<dbname>' user='<user>' host='<host>' password='<password>'")
except:
        print("I am unable to connect to the database")
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
from psycopg2 import sql
query = sql.SQL("select * from {}")
cur.execute(query.format(sql.Identifier('FriendsAsylum_patiententry')))
rows = cur.fetchall()
```
 In order to connect to the database you want that is what this line is doing:
 ```
 conn = psycopg2.connect("dbname='<dbname>' user='<user>' host='<host>' password='<password>'")
 ```
 You can find this information in your settings file of the project. 
 ```
 query = sql.SQL("select * from {}")
 ```
 This line is the query you want to use to get information from the database and use in your visulization. The {} is the database table we are trying to use and will need '' around the database name and putting it directly will cause errors with parantheses. This next line will allow you to put the info that you want in the {}:
 ```
 cur.execute(query.format(sql.Identifier('<what you want to put in the {}>')))
 ```
 This is next line take all the information from the query and puts it in a variable:
 ```
 rows = cur.fetchall()
 ```
 Then to use the information in <strong>rows</strong> you can do:
 ```
 for i in rows:
    j = i['<column of the query result>']
```

### Using csv

 In order to use a csv file you will need to install pandas with:
 ```
 pip install pandas
 ```
 In your python file import pandas:
 ```
 import pandas as pd
 ```
 Then to use the csv:
 ```
 df = pd.read_csv('<csv file>')
 ```
 You can then use df to extract data you can do
 ```
 df['<column from the csv>']
 ```
 You can also change the query to include only specific data from a clumn sush as:
 ```
 df = df[df['<column from the csv'>] == '<specific data name from column>']]
 ```
 You can read more on how pandas works: https://pandas.pydata.org/
 
 ### Creating the plot and figure
 Here are some links to the Bokeh documentation and gallery for inspiration on what plots are useful to your project:
 
 https://bokeh.pydata.org/en/latest/docs/gallery.html
 https://bokeh.pydata.org/en/latest/docs/user_guide/interaction.html
 https://bokeh.pydata.org/en/latest/docs/user_guide/interaction/widgets.html
 
 Widgets allow you to update or show more information on the plot and change the plot by using a callback to change the data presented to the plot. 
 https://github.com/bokeh/bokeh/blob/master/examples/app/sliders.py
 With another example:
 ```
 df = pd.read_csv('Copy_of_SUPER_SPREADSHEET_2.csv')
for key,value in df.items():
	df[key] = list(value.fillna(0))
source = ColumnDataSource(data=df)
#print(source.data)

p = figure(tools=[hover, "pan,box_zoom,reset,save"])
#df['AgeAdmitted'] = list(df['AgeAdmitted'].fillna(0))
#df['DaysinAsylum'] = list(df['DaysinAsylum'].fillna(0))
p.circle(x='AgeAdmitted', y='DaysinAsylum', source=source, size=20, color="navy", alpha=0.5)
slider = Slider(start=df['YearAdmitted'].iloc[df['YearAdmitted'].nonzero()[-1]].min(), end=df['YearAdmitted'].max(), value=df['YearAdmitted'].min(), step=1, title="Year")
sliderrange = RangeSlider(start=0, end=10, value=(1,9), step=.1, title="Stuff")
print("value of sliderrange ", sliderrange.value, " ", sliderrange.value[0], " ", sliderrange.value[1])
def callback(attr, old, new):
	N = slider.value
	print(N)
	source1 = df[df['YearAdmitted'] >= N]
	#print(source1)
	'''
	for key,value in source1.items():
		print("in loop")
		df[key] = list(pd.Series(value).fillna(0))
	'''
	print("outside loop")
	source.data = ColumnDataSource(data=source1).data
	print(source.data)
	#source.data = new1.data
print(slider.on_change('value', callback))
slider.on_change('value', callback)
```
With source holding the data you want to use which will then be used in the plot and later in the widget such as a slider to change the plot and data. The callback function is a function that changes the data depending what the user puts in the widget. Then with variable slider being the widget Slider in the plot, the slider.on_change('value', callback) calls the callback function with the value in the slider and changes the data depending on the slider.

### Connecting the plot to the server

At the end of the python file you want the plot to be seen when you start the server so you add:
```
curdoc().add_root(<things you want to be seen>)
```
In the add_root you can make the plot and widgets been seen in a column() or row(). Adding to the example above you can do:
```
curdoc().add_root(column(slider, p, sliderrange))
```
## Connecting the website server and bokeh server
In order to see the plot and allow the widgets to change the plot, you will need to start a bokeh server by running this command in terminal:
```
bokeh serve <name of bokeh python file>
```
However in order to see the plot, you will need to start the server everytime manually which is tedious, thus you will need to configure ngnix and systemd to allow the Bokeh server to be run at all times. 
### Make a Bash file
You will need to make a bash file so when you configure systemd it will automatically run the bash file and start the bokeh server. A bash file is a set of terminal commands so when the bash file is run all the commands are executed at once. 
