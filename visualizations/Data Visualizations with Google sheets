# Data Visualizations with Google sheets

In this tutorial ( largely based on Greg Baugues' [article](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html) ), I will go through how to use the [Google APIs Console](https://console.developers.google.com/) to set up a service account and OAuth2 credentials to 'programmatically' access your spreadsheet. The programming side of this can be done in multiple languages, but I will be using the Python package [gspread](https://github.com/burnash/gspread).

---

## Google Drive API and Service Accounts

1. Go to the [Google APIs Console](https://console.developers.google.com/).
2. Create a new project.
3. Click Enable API. Search for and enable the Google Drive API.
4. Click create credentials and select for a Web Server to access Application Data ( For *Where will you be calling the API from?*), *Application Data* and *No* for using Google App Engine .
5. Name the service account and grant it a Role of Editor. Leave *Key Type* as JSON.
6. Download the JSON file.
7. Copy the JSON file to your project's directory and rename it to `client_secret.json`

Within the file `client_secret.json` find the field `client_email` ( you'll need this in a second ). Go back to your spreadsheet and Share the spreadsheet with the client email to give it edit rights. If you skip this step your .py file will have no way to access spreadsheet.

## Retreiving data with Python

With all of your credentials in place and in your project directory, you are almost reading to start coding in python!  First make sure you have the following two packages which are required to access a Google spreadsheet in Python:  
1. [oauth2client](https://github.com/google/oauth2client) – to authorize with the Google Drive API using OAuth 2.0
2. [gspread](https://github.com/burnash/gspread) – to interact with Google Spreadsheets

Install both of these packages with:

```
pip install gspread oauth2client
```

Now we can move onto the coding !!!

Create the file `spreadsheet.py` and then paste the following code:
```
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("NAME_OF_YOUR_SPREADSHEET").sheet1

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()
print(list_of_hashes)
```
(NOTE: you need to replace `NAME_OF_YOUR_SPREADSHEET` with the exact name of your spreadsheet. )

If you'd like to get the data into a list of lists instead of a list of hashes you can replace the last line with 	`print(sheet.get_all_values())`

In case you're new to data manipulation with python the following table

| Name | Age | Eye_Color |
|------|-----|-----------|
|'Maddy'|22|'Green'|
|'Jess'|18|'Blue'|
|'Miles'|21|'Brown'|

would look like this as a list of hashes:
```
[{'Name': 'Maddy','Age':22 ,'Eye_Color':'Green' },
 {'Name': 'Jess' ,'Age': 18,'Eye_Color':'Blue' },
 {'Name': 'Miles','Age': 21,'Eye_Color':'Brown' }
  ]
```

and would look like this as a list of lists:
```
[ [ 'Name' , 'Age' , 'Eye_Color' ],
  [ 'Maddy', 22 , 'Green'],
  [ 'Jess' , 18 , 'Blue'],
  [ 'Miles' , 21 , 'Brown'] ]
```

## Caveat

Essentially with the use of Google APIs, you will have created credentials ( looks an email ) and then gave that email/credential r/w rights on the spreadsheet just as you would give any user access. And its this email/credential that is accessing the sheet every time you run your code. The one caveat is that since you have created the credential, once you graduate :sob:, your Haverford account will be deactivated and with it this credential will be deleted.  

## Other capabilities not mentioned
Below are just some capabilities I found interesting - if you want to do something that is not listed here please check [this great documentation](http://gspread.readthedocs.io/en/latest/) ... there's no point in recreating the wheel !


You can just pull the data from a single row, column, or cell:
```
sheet.row_values(1)

sheet.col_values(1)

sheet.cell(1, 1).value
```

You can write to the spreadsheet by changing a specific cell:

```
sheet.update_cell(1, 1, "I just wrote to a spreadsheet using Python!")
```
Or you can insert a row in the spreadsheet:

```
row = ["I'm","inserting","a","row","into","a,","Spreadsheet","with","Python"]
index = 1
sheet.insert_row(row, index)
```
You can also delete a row from the spreadsheet:

```
sheet.delete_row(1)
```
And find out the total number of rows:

```
sheet.row_count
```

But this is just scratching the surface ! please check out the [documentation](http://gspread.readthedocs.io/en/latest/)


## Contributors :tada:
:octocat: [Maddy Hodges](https://github.com/Mfhodges)
