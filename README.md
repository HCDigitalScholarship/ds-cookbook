# ds-cookbook
*A repository for documentation and tutorials (recipes) that help us cook up great projects*
## Table of Contents
1. DSBasics
- [Djangology101](https://github.com/HCDigitalScholarship/ds-cookbook/blob/master/DSBasics/Djangology101.md)
- [CodeReview](https://github.com/HCDigitalScholarship/ds-cookbook/blob/master/DSBasics/code_review.md)
2. [DjangoCaptcha](https://github.com/HCDigitalScholarship/ds-cookbook/tree/master/Django-Captcha)
3. MapsOrGeocoding *create map visualizations*
- [GeoDjango](https://github.com/HCDigitalScholarship/ds-cookbook/tree/master/MapsOrGeocoding/geodjango_and_geocoding)
- [Mapbox](https://github.com/HCDigitalScholarship/ds-cookbook/blob/master/MapsOrGeocoding/mapbox/README.md)
- [LeafletMarkerCluster](https://github.com/HCDigitalScholarship/ds-cookbook/tree/master/MapsOrGeocoding/LeafletMarkerCluster)
4. [StoryMapJS](https://github.com/HCDigitalScholarship/ds-cookbook/blob/master/StoryMapJS/StoryMapJS.md)
5. [XSLT](https://github.com/HCDigitalScholarship/ds-cookbook/blob/master/XSLT/xslt.md)
6. [bridge-update](https://github.com/HCDigitalScholarship/ds-cookbook/tree/master/bridge-update) *I'm not sure why this is in the cookbook, it's a little too specific to be considered a "recipe." There should be a better place for this.*
7. dash
- [installing dash](https://github.com/HCDigitalScholarship/ds-cookbook/blob/master/dash/dash.md) *dash for dashboards and data viz*
- [django-plotly-dash](https://github.com/HCDigitalScholarship/ds-cookbook/blob/master/dash/django-plotly-dash%20.md)
8. [data tables server-side processing](https://github.com/HCDigitalScholarship/ds-cookbook/tree/master/datatables-server-side-processing)
9. [django autocomplete light](https://github.com/HCDigitalScholarship/ds-cookbook/tree/master/django-autocomplete)
10. [django email verification](https://github.com/HCDigitalScholarship/ds-cookbook/tree/master/django_email_verification)
11. [django flatpages and ckeditor](https://github.com/HCDigitalScholarship/ds-cookbook/tree/master/django_flatpages) *flatpages lets you add static html pages from admin and stores them in the database for serving up. CKEditor gives you a nice way to edit those pages in admin*
12. [django proxy model](https://github.com/HCDigitalScholarship/ds-cookbook/tree/master/django_proxy_model)
13. [google vison](https://github.com/HCDigitalScholarship/ds-cookbook/tree/master/google_vision)
14. [internationalization](https://github.com/HCDigitalScholarship/ds-cookbook/tree/master/internationalization)
15. linked_data
- [mediawiki](https://github.com/HCDigitalScholarship/ds-cookbook/blob/master/linked_data/mediawiki.md)
- [dbpedia](https://github.com/HCDigitalScholarship/ds-cookbook/blob/master/linked_data/dbpedia/dbpedia.md)
16. [pdf_building](https://github.com/HCDigitalScholarship/ds-cookbook/tree/master/pdf_building)
17. [scattertext](https://github.com/HCDigitalScholarship/ds-cookbook/tree/master/scattertext)
18. [django search](https://github.com/HCDigitalScholarship/ds-cookbook/tree/master/search_tools)
19. visualizations
- [django-to-mapbox](https://github.com/HCDigitalScholarship/ds-cookbook/blob/master/visualizations/Django-to-Mapbox.md)
- [django-to-d3](https://github.com/HCDigitalScholarship/ds-cookbook/blob/master/visualizations/Django-to-d3.md)
- [google sheets](https://github.com/HCDigitalScholarship/ds-cookbook/blob/master/visualizations/GoogleSheets.md)
- [bokeh](https://github.com/HCDigitalScholarship/ds-cookbook/blob/master/visualizations/bokeh.md)
- [simple networks](https://github.com/HCDigitalScholarship/ds-cookbook/blob/master/visualizations/simple_networks.md)

## More details about some of these technologies follow

### Flask and flatpages in Django
1. Django Flatpages and Ckeditor
  - Flatpages are used to create a standard template that can be applied to all static pages in a project. The standard template can include headers, footers, sidebars, etc. Additionally, the user can edit each individual flatpage to include its unique content. This allows users without html, css, or java knowledge to add and edit pages for their site. Ckeditor offers tools for the user to make edits to the contents of each page. The following tutorial describes how the basic Ckeditor configuration is installed, as well as offers instructions for installing the 'file upload' Ckeditor feature. The user can make additional alterations to this configuration to access editing tools that they find beneficial to the creation of their site.
    
### Dash app and Django
 1. dash
    - A dashboard offers multiple visualizations with ways to sort and filter the data simulatiously. There are many solutions available to create a dashboard. Our current favorite is called Dash, which offers a relatively easy way to define the layout and callbacks for a React.js app using Python. The layout determines what elements appear on the page, such as buttons, graphs and datatables. A callback defines how each element is updated. Dash apps can be added to Django projects with the django-plotly-dash app.

### PDF building
1. pdf_building
  - reportlab is a software for building PDFs from XML or Python instructions. Because it can interpret Python instructions, reportlab can be used to dynamically generate PDFs that vary in format and content. For instance, if we want to give site visitors the ability to view and download digitized resources as a PDF rather than a webpage, reportlab can be used in the backend to fill out a PDF template with the relevant content and metadata, or even make structural changes to a PDF document according to user specifications, database content, or other parameters.

### Search
1. search_tools
  - an advanced search tool like the one used in the Global Terrorism Research Project. All of the querying is handled with standard Django querying and filtering in addition with Django Q()'s. I recommend taking a look at those links for more details, or if you run into any problems.
### Translations in Django
1. internationalization
   - How to add translations to a django site

### Things related to maps and geography
 1. GeoDjango and Geocoding (NEW)
    - Want to create a world-class geographic Web application through Django? GeoDjango, built on Python and Django, is a great toolkit to help you handle with spatial database and build a GIS Web application. When you have address information (like a home address) and want to show them on a map, Geocoding API from google maps helps you convert the descriptive addresses into geographic coorindates (longitude and latitude) so that you can place markers on the map or position the map. 
 2. StoryMap JS
    - StoryMapJS is a tool to help you tell stories on either a map, a series of map or big image that highlight the locations of a series of events. StoryMapJS creates a JSON object that can be incoporated into an Django app, dispalyed on the Web application through Javascript in an HTML template. 
    
### Django toolkits miscellanea 

1. AutoComplete
2. Email Verification
3. Captcha Verification 
4. Datatable
5. Django Proxy Models
   - A proxy model is just another class that provides a different interface for the same underlying database model. A proxy model is a subclass of a database-table defining model. Typically creating a subclass of a model results in a new database table with a reference back to the original model’s table - multi-table inheritance. A proxy model doesn’t get its own database table. Instead it operates on the original table.
