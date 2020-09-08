from django.core.management.base import BaseCommand, CommandError
from main.models import *
from pathlib import Path 
from django.shortcuts import render
from django.template.loader import render_to_string
from distutils.dir_util import copy_tree
from django.conf import settings
import requests 
import json 
import shutil
from bs4 import BeautifulSoup
import paramiko
from mappingEE.secrets import HOST, PORT, USERNAME, PASSWORD
from fabric import Connection
import patchwork.transfers


static_dir = settings.STATICFILES_DIRS[0]
media_dir = settings.MEDIA_ROOT


class Command(BaseCommand):
    help = 'Build a static site from current project'

    #def add_arguments(self, parser):
    #    parser.add_argument('out_dir', nargs='+', type=str, help='The directory where the site build will be saved',)

    def handle(self, *args, **options):
        out_path = Path('/tmp/site') #Path(options['out_dir'][0])
        if not out_path.exists():
            out_path.mkdir(parents=True, exist_ok=True)

        #copy all media 
        site_media = (out_path / 'media')
        if not site_media.exists():
            site_media.mkdir(parents=True, exist_ok=True)
        copy_tree(media_dir, str(site_media))

        #copy all static 
        site_static = (out_path / 'static')
        if not site_static.exists():
            site_static.mkdir(parents=True, exist_ok=True)
        copy_tree(static_dir, str(site_static))
        #TODO remove admin, autocomplete_light, jet and other static not needed

        #index.html
        context = {}
        context['categories'] = Category.objects.all()
        context['items'] = Item.objects.all() 
        index = render_to_string('index.html', context)

        index = index.replace('''href="/category/Historical%20Overviews"''', '''href="/category/historical-overviews"''')
        index = index.replace('''href="/category/Historicial%20Overviews"''', '''href="/category/historical-overviews"''')
        
        index = index.replace('''href="/category/Case-Studies"''', '''href="/category/case-studies"''')
        index = index.replace('''href="/category/Notices"''', '''href="/category/short-notices"''')
        index = index.replace('''href="/category/Reviews"''', '''href="/category/reviews"''')
        
        index = index.replace('''url: '/category-autocomplete/',''', '''url: '/category-autocomplete.json',''')
        index = index.replace('''url: '/subject-autocomplete/',''', '''url: '/subject-autocomplete.json',''')
        index = index.replace('''url: '/location-autocomplete/',''', '''url: '/location-autocomplete.json',''')
        index = index.replace('''url: '/medium-autocomplete/',''', '''url: '/medium-autocomplete.json',''')
        index = index.replace('''url: '/keyword-autocomplete/',''', '''url: '/keyword-autocomplete.json',''')
        index = index.replace('''href="/help/"''', '''href="/help"''')
        index = index.replace('''href="/#map"''', '''href="/index.html#map"''')
    
        # footer links to about and help 
        #index = index.replace('''href="/about/"''', '''href="/about.html"''')
        #index = index.replace('''href="/help/"''', '''href="/help.html"''')


        (out_path / 'index.html').write_text(index)               
        
        #help.html
        context = {}
        help = render_to_string('help.html', context) 
        (out_path / 'help.html').write_text(help)  
        
        #about.html
        context = {}
        about = render_to_string('about.html', context) 
        (out_path / 'about.html').write_text(about)  
        
        # category pages
        if not (out_path / 'category').exists():
            (out_path / 'category' ).mkdir(parents=True, exist_ok=True)
        for category in Category.objects.all():
            context = {}
            if category.name == 'Case-Studies':
                context['tags'] = [item.tag.name for item in Item.objects.filter(category__name__icontains='Case-Studies') if item.tag]
                context['category'] = category
                context['items'] = Item.objects.filter(category__name__icontains=category.name)
                cat_page = render_to_string('case-studies.html', context) 
            if category.name == 'Reviews':
                context['tags'] = [item.tag.name for item in Item.objects.filter(category__name__icontains='Reviews') if item.tag]
                context['category'] = category
                context['items'] = Item.objects.filter(category__name__icontains=category.name)
                cat_page = render_to_string('reviews.html', context) 
            else:
                context['category'] = category
                context['items'] = Item.objects.filter(category__name__icontains=category.name)
                cat_page = render_to_string('category.html', context) 
            file_name = category.slug + '.html'
            (out_path / 'category' / file_name).write_text(cat_page)
           
        # item pages 
        item_dir = (out_path / 'item')
        if not item_dir.exists():
            item_dir.mkdir(parents=True, exist_ok=True)
        for item in Item.objects.all():
            context = {}
            context['item'] = item
            item_page = render_to_string('item.html', context) 
            file_name = item.slug + '.html'
            (out_path / 'item' / file_name).write_text(item_page)

        # autocomplete json files
        # TODO currently requires URL path, but should work

        category_autocomplete = requests.get('https://mapping.apjan.co/category-autocomplete/')
        (out_path / 'category-autocomplete.json').write_bytes(category_autocomplete.content)

        subject_autocomplete = requests.get('https://mapping.apjan.co/subject-autocomplete/')
        (out_path / 'subject-autocomplete.json').write_bytes(subject_autocomplete.content)

        location_autocomplete = requests.get('https://mapping.apjan.co/location-autocomplete/')
        (out_path / 'location-autocomplete.json').write_bytes(location_autocomplete.content)

        medium_autocomplete = requests.get('https://mapping.apjan.co/medium-autocomplete/')
        (out_path / 'medium-autocomplete.json').write_bytes(medium_autocomplete.content)
        
        keyword_autocomplete = requests.get('https://mapping.apjan.co/keyword-autocomplete/')
        (out_path / 'keyword-autocomplete.json').write_bytes(keyword_autocomplete.content)

        
        shutil.make_archive(str(out_path), 'zip', str(out_path))
        zip_file = str(out_path).split('/')[-1]+'.zip'
        with Connection('{}@{}:{}'.format(USERNAME,HOST, PORT), connect_kwargs=dict(password=PASSWORD)) as c:
            c.put(str(out_path)+'.zip', '/home/mappingee/public_html')
            c.run('unzip -o public_html/{} -d public_html/'.format(zip_file))
    

        self.stdout.write(self.style.SUCCESS('Site deployed to {}'.format(HOST)))
