# DataTables: Server Side Processing
[DataTables](https://datatables.net/) is a handy plug-in to build HTML tables with advanced interaction controls. 
However, because DataTables basically uses javascript and asks your browser to process the data, it is very slow when you 
have more than 1,000 rows of data. In this situation, you need to switch the side of data processing to the server in order to
speed up your DataTables. [django-datatables-view](https://bitbucket.org/pigletto/django-datatables-view/overview) is a very
convenient tool to switch DataTables to the server side. It simplifies the handling of sorting, filtering and creating JSON output.
This tutorial is to provide you some basic information for getting start with this tool!

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

## Get start with django-datatables-view
### 1. Install  
`pip install django-datatables-view`  
(Notes: you do NOT need to install django-datatables-views in `settings.py`)

