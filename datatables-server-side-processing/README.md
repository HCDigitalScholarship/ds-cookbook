# DataTables: Server Side Processing
[DataTables](https://datatables.net/) is a handy plug-in to build HTML tables with advanced interaction controls. However, because DataTables basically uses javascript and asks your browser to process the data, it is very slow when you have more than 1,000 rows of data. In this situation, you need to switch the side of data processing to the server in order to speed up your DataTables. [django-datatables-view](https://bitbucket.org/pigletto/django-datatables-view/overview) is a very convenient tool to switch DataTables to the server side. It simplifies the handling of sorting, filtering and creating JSON output. This tutorial is to provide you some basic information for getting start with this tool! And in the end, we will introduce some useful functions of DataTables we have discovered so far that make our tables more powerful!

## Some tips for using DataTables alone!
1. Remember to include these two files in your template:  
CSS `<link rel="stylesheet" href="//cdn.datatables.net/1.10.19/css/jquery.dataTables.min.css">`  
JS `<script src="//cdn.datatables.net/1.10.19/js/jquery.dataTables.min.js"></script>`  
  
   Probably, you will need this file as well:  
`<script scr="//code.jquery.com/jquery-3.3.1.js"></script>`

2. Call this function:  
```
$(document).ready( function () {  
    $('#myTable').DataTable();  
} );
```
3. Make sure the format of your HTML tables is complete:  
```
<table>
  <thead>
     <tr>
        <th> Name </th>
        <th> Country </th>
     </tr>
  </thead>
  <tbody>
     <tr>
        <td> my name </td>  <!-- make sure the number of columns is the same as the header -->
        <td> my country </td>
     </tr>
  </tbody>
</table>
```

## Now, let's get start with django-datatables-view
### 1. Install  
`pip install django-datatables-view`  
(Notes: you do NOT need to install django-datatables-views in `settings.py`)

### 2. Edit views.py
Django-datatables-view uses **GenericViews**, so your view should just inherit the base view, **BaseDatatableView**. Here is a basic example adapted from GAM project:
```
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

class ImageListJson(BaseDatatableView):
    # the model you're going to show
    model = Image
    
    # define columns that will be returned
    # they should be the fields of your model, and you may customize their displaying contents in render_column()
    # don't worry if your headers are not the same as your field names, you will define the headers in your template
    columns = ['name', 'description', 'status', 'translation']

    # define column names that will be used in sorting 
    # order is important and should be same as order of columns displayed by datatables
    # for non sortable columns use empty value like ''
    order_columns = ['name', '', 'status', 'translation']

    # set max limit of records returned
    # this is used to protect your site if someone tries to attack your site and make it return huge amount of data
    max_display_length = 500

    def render_column(self, row, column):
        # we want to render 'translation' as a custom column, because 'translation' is defined as a Textfield in Image model,
        # but here we only want to check the status of translating process.
        # so, if 'translation' is empty, i.e. no one enters any information in 'translation', we display 'waiting';
        # otherwise, we display 'processing'.
        if column == 'translation':
            if row.translation == '':
                # escape HTML for security reasons
                return escape('waiting')
            else:
                return escape('processing')
        else:
            return super(ImageListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset
        
        # here is a simple example
        search = self.request.GET.get('search[value]', None)
        if search:
            q = Q(name__icontains=search) | Q(description_icontains=search)
            qs = qs.filter(q)
        return qs

```
In the views, you may have a lot of fun by overriding with *render_columns()* and *filter_queryset*. If you have a more advanced customization, you could go to their official tutorial and learn from their [examples](https://bitbucket.org/pigletto/django-datatables-view).  

Some more examples about overriding *render_columns()* that we have done in GAM project so far:
* links  
` return format_html("<a href='/{0}/{1}/{2}/{3}/{4}'>{1}/{2}/{3}/{4}</a>".format(row.archivo, row.colección, row.caja, row.legajo, row.carpeta, row.número_de_imagen,)`

* alignment  
` format_html("<div align='left'>{0}</div>".format(row.description))`

### 3. Edit urls.py
Back to the example of Image model:
```
from django.contrib.auth.decorators import login_required

path('/datatable/image/', login_required(ImageListJson.as_view()), name='image_list_json'),
```
At the browser, check '<ip address>/datatable/image' to see if you can see the result.
  
### 4. Edit HTML and JavaScript
In the template where your DataTables should display, add the tags of a HTML table, and define your headers. Notice that you do NOT need to include the body part of your table here.
```
<table class="myTable">
  <thead>
     <tr>
        <th> Name </th>
        <th> Description </th>
        <th> Transcription Status </th>
        <th> Translation Status </th>
     </tr>
  </thead>
</table>
```

Then add the JavaScript in the same file. All the data from 'image_list_json' will automatically fill the body part of your table:
```
<script>
$(document).ready(function() {
    $('.myTable').DataTable( {
        // ... 
        "processing": true,
        "serverSide": true,
        "ajax": "{% url 'image_list_json' %}",       
    } );
    // ...
} );
</script>
```

## Some powerful functions of DataTables we have discovered so far, and you are invited to update them XD
#### * pagination
This one is simple:
```
$(document).ready( function () {  
    $('#myTable').DataTable( {
    "pageLength": 10,    
    } );  
} );
```

#### * multilingual function
```
$(document).ready( function () {  
    $('#myTable').DataTable( {
    {% if LANGUAGE_CODE == 'es' %}
    "language": {
        "url": "//cdn.datatables.net/plug-ins/1.10.19/i18n/Spanish.json"
    },
    {% elif LANGUAGE_CODE == 'de' %}
    "language": {
        "url": "//cdn.datatables.net/plug-ins/1.10.19/i18n/German.json"
    },
    {% endif %} 
    } );  
} );
```
That's it! If you have any question, please go to their webpages for detailed information. And if you find out any mistake in this tutorial, please feel free to update them! Thank you!
