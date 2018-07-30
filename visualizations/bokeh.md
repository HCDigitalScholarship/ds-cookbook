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

 
