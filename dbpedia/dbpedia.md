## Dbpedia data

This is a short introduction to quickly accessing data from Wikipedia and adding to an existing Django project.  In this example, we will be importing data about book authors. 

import requests 
import spotlight
from books_app.models import Author 

url = 'http://model.dbpedia-spotlight.org/en/annotate'

authors = Author.objects.all()

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
            print('no dod')
        try:
            count = len(data["http://dbpedia.org/ontology/abstract"])
            for i in range(count):
                if data["http://dbpedia.org/ontology/abstract"][i]['lang'] == 'en':
                    abstract = data["http://dbpedia.org/ontology/abstract"][i]['value']
                else:
                    pass
        except:
            abstract = ''
            print('no abstract')
        try:
            gender = data["http://xmlns.com/foaf/0.1/gender"][0]['value']
        except:
            gender = ''
            print('no gender data')
        
        author = Author.objects.get(name=author.name)
        author.abstract = abstract
        author.birth_date = birth_date
        author.death_date = death_date
        author.gender = gender
        author.save()	
    except Exception as e:
        print(e)
	        
