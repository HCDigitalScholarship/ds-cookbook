## Dbpedia data (one of many ways to get it)

This is a short introduction to one way to quickly accessing data from Wikipedia and add it to an existing Django project.  In this example, we will be importing data about book authors. 

To begin, you will need the [requests](https://2.python-requests.org/en/master/) library and [pyspotlight](https://pypi.org/project/pyspotlight/)
```python
import requests 
import spotlight
```

Next we will import the model that we want to update called Author and create a queryset of all the existing objects. We have author names in the database and will use them in the query to dbpedia.
```python
from books_app.models import Author 
authors = Author.objects.all()
```

Spotlight needs the address of a dbpedia endpoint, which is defined here:
```pythin
url = 'http://model.dbpedia-spotlight.org/en/annotate'
```
Now we will iterate over each Author object and use spotlight to find a corresponding dbpedia entry and URI. We will then use requests to request the data as JSON from the URI.  Be careful, spotlight can return incorrect results.  You can add `confidence=0.8` to the spotlight.annotate function to select for only the most certain results. Also note that dbpedia entries are often missing data.  For example, if there is no birth date, I have chosen to just write an empty string to the database.  That may not be right for your project. 

```python
for author in authors:
    try:
        uri = spotlight.annotate(url, author.name)[0]['URI']
        name = uri.split('/')[-1]
        author_json = requests.get('http://dbpedia.org/data/{}.json'.format(name)).json()
        data = author_json['http://dbpedia.org/resource/{}'.format(name)]
        try:
            birth_date = data["http://dbpedia.org/ontology/birthDate"][0]['value']
        except:
            birth_date = ''
        try:
            death_date = data["http://dbpedia.org/ontology/deathDate"][0]['value']
        except:
            death_date = ''
        try:
            count = len(data["http://dbpedia.org/ontology/abstract"])
            for i in range(count):
                if data["http://dbpedia.org/ontology/abstract"][i]['lang'] == 'en':
                    abstract = data["http://dbpedia.org/ontology/abstract"][i]['value']
                else:
                    pass
        except:
            abstract = ''
        try:
            gender = data["http://xmlns.com/foaf/0.1/gender"][0]['value']
        except:
            gender = ''
            
        author = Author.objects.get(name=author.name)
        author.abstract = abstract
        author.birth_date = birth_date
        author.death_date = death_date
        author.gender = gender
        author.save()	
    
    except Exception as e:
        print(e)
```    
