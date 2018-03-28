# Advanced Searching with Django Q()'s
In this tutorial, I'll cover how to make an advanced search tool like the one used in the [Global Terrorism Research Project](http://gtrp.haverford.edu/).
All of the querying is handled with [standard Django querying and filtering](https://docs.djangoproject.com/en/2.0/topics/db/queries/) in addition with [Django Q()'s](https://docs.djangoproject.com/en/2.0/topics/db/queries/#complex-lookups-with-q-objects).
I recommend taking a look at those links for more details, or if you run into any problems.

## Making the search bars (JavaScript and HTML)
Before we can query our data, we need the user to tell us what they want! I built my search bars in plain-old HTML and jQuery. For me, this is just on the index page, but you might want it somewhere else.
The first thing we do is build a form. We don't actually have any search bars yet though! We will add those in dynamically with javascript later.

```
<form id="searchers_form"  action="mysite:search" method="GET">
    <div class="form-group" id="searchers">
        <div id="searcher1"></div>
    </div>
    <input id="full_info" type="hidden" value='' name="full_info">
</form>
```
`full_info` will be a string that keeps track of the complete user query. We can pass this around easily and build it up if the user later wants to refine their results. You want the action to point the 'search' function in your views. If you are following this, that does not exist yet. You can assume we will call it `search`, or you can leave it blank for now and I'll remind you later!

The next thing we do is add the buttons.
```
    <span> Add a search term </span>
    <input type="hidden" id="searcher_counter" name="seacher_count" value="1">
    <button type="button" id="OR_search" class="btn btn-primary">OR</button>
    <button type="button" id="AND_search" class="btn btn-primary">AND</button>
<button type="button" id="NOT_search" class="btn btn-primary">NOT</button>
```
Again, we have a hidden field. This will keep track of how many `searchers` (search bars) we have floating around.

You also might need to load in jQuery, if you haven't already.
```
    <script src="{% static 'gtr_site/jquery.js' %}"></script>
    <script src="{% static 'gtr_site/jquery-ui.js' %}"></script>

```
Loading jQuery multiple times can mess things up, so this might be a sticking point.


Now we are setup to write our search bar adding script!

The first thing we do is reset our searchbar counter to 1 on page loads. In my opinion, when a user reloads the page, the search bars should reset. If you want different functionality, this is something you would have to change.
```
<script>
      // reset counter to 1
      // might want to get rid of this if we load based on previous counter
      $(document).ready(function(){
        $("#searcher_counter").val("1");
        });
```
Now we define long variables that are featured in each of the search bars: things like the field options, and the delete button. Actually, just those two things. You'll need to customize the `select_fields` to fit with your data and your goals. They will be the fields in the dropdown that you are able to filter on.
```
      // These long lines are just html we will be using and reusing
      var select_fields = "<select class='form-control field_option'> <option>Any field</option> <option>Title</option>  <option>Keyword</option></select>";
      var delete_button = "<button class='delete_searcher' type='button'><span class='glyphicon glyphicon-remove delete_searcher'></span><button>";
```

Now we make the logical drop down that lets users switch which operator they picked. I made this a function because it makes it easier to correctly start with the one they oiginally picked showing. Or maybe it is a function for some other reason, I honestly do not remember.
```      
      function createLogicDropdown(operator) {
        if(operator=="AND") {
            return  "<select class='form-control logic_option'> <option value='OR'>OR</option> <option value='AND' selected='selected'>AND</option> <option value='NOT'>NOT</option></select>";
        }
        else if (operator=="OR") {
            return  "<select class='form-control logic_option'> <option selected='selected' value='OR'>OR</option> <option value='AND'>AND</option> <option value='NOT'>NOT</option></select>";
        }
        else {
            return  "<select class='form-control logic_option'> <option value='OR'>OR</option> <option value='AND'>AND</option> <option selected='selected' value='NOT'>NOT</option></select>";
        }
      }
```
We finally get to make our first search bar! How exciting! Since this one is the first, let's make it special. This one will be undeletable and it doesn't really have a logical operator like the other one's do (because they are binary expressions! Well, NOT isn't, you could add support to NOT the first item if you feel passionate, although there is currently a way to generate that query.)
```
      // make first search bar. This one can't be deleted
      $("#searcher1").append("<span><div class='input-group stylish-input-group'><input type='text' class='form-control search_text' name='search' placeholder='Search...'><span class='input-group-addon'><button type='submit'><span class='glyphicon glyphicon-search'></span></button></span></div> in " + select_fields + "</span>");
```

_Uh, this next part doesn't do anything?_ I think I was in the process of doing something else. If you are an eager reader and are eagerly reading this, go ahead and skip this next code block.
```
        $("#filter_form").submit(function( event) {
          for(i=1; i <= $("#searcher_counter").val(); i++) {
            var dateValues = $("#searcher"+i).dateRangeSlider("values");
            //$("#dateLow"+i).val(dateValues.min.toString());
            //$("#dateHigh"+i).val(dateValues.max.toString());
          }     
        });
```

Now we define what happens when you click the `AND`, `OR` and `NOT` buttons we made early. They add searchers!

Some things to note: I make it so you can't have more than 11 search bars. There isn't really a reason for that, it just seems like it should stop at some point. Also in each of these processes, we increment the hidden `searcher_counter`, append our a div shell for our new searcher to our list of searchers, the searcher labeled by our incremented `searcher_counter`. Finally, we fill in the empty div shell with the actual search bar, drop down, and delete button. We do this for each option you can click! 
```
      // what happens when you click AND
      $("#AND_search").click(function(event) {
        if($("#searcher_counter").val() < 11) {
          // the plus              here tells javascript to do as number addition so 1+1 doesn't equal 11.
          $("#searcher_counter").val(+$("#searcher_counter").val() + 1);
          var id_num = $("#searcher_counter").val();
          $("#searchers").append("<div id='searcher"+ id_num +"' class='form-group'></div>");
          $("#searcher" + id_num).append("<span>" + createLogicDropdown("AND") + "<br/><div class='input-group stylish-input-group'><input type='text' class='form-control search_text' name='AND_search' placeholder='Search...'><span class='input-group-addon'>" + delete_button + "</span></div> in " + select_fields + "</span>");
        }
      });

      // what happens when you click OR
      $("#OR_search").click(function(event) {
        if($("#searcher_counter").val() < 11) {
          // the plus              here tells javascript to do as number addition so 1+1 doesn't equal 11.
          $("#searcher_counter").val(+$("#searcher_counter").val() + 1);
          var id_num = $("#searcher_counter").val();
          $("#searchers").append("<div id='searcher"+ id_num +"'></div>");
          $("#searcher" + id_num).append("<span>" + createLogicDropdown("OR") + "<br/><div class='input-group stylish-input-group'><input type='text' class='form-control search_text' name='OR_search' placeholder='Search...'><span class='input-group-addon'>" + delete_button + "</span></div> in " + select_fields + "</span>");
        }
      });

      // what happens when you click NOT
      $("#NOT_search").click(function(event) {
        if($("#searcher_counter").val() < 11) {
          // the plus              here tells javascript to do as number addition so 1+1 doesn't equal 11.
          $("#searcher_counter").val(+$("#searcher_counter").val() + 1);
          var id_num = $("#searcher_counter").val();
          $("#searchers").append("<div id='searcher"+ id_num +"'></div>");
          $("#searcher" + id_num).append("<span>" + createLogicDropdown("NOT") + "<br/><div class='input-group stylish-input-group'><input type='text' class='form-control search_text' name='NOT_search' placeholder='Search...'><span class='input-group-addon'>" + delete_button + "</span></div> in " + select_fields + "</div>");
        }
      });
```

We also need to handle what happens when a user presses the delete button. This is actually a little awkward to do because the thing we are deleting doesn't exist when the page loads. We need to use event delegation, which is something you can google to learn more about or look [here](https://learn.jquery.com/events/event-delegation/) to get started.
```
      // what happens when you click Delete
      // Need to use event delegation because these deletes don't 
      // exist on the initial page load
      $("#searchers").on("click", ".delete_searcher", function(event) {
          event.preventDefault();
          $(event.target).parent().parent().parent().parent().remove();
          $("#searcher_counter").val(+$("#searcher_counter").val() - 1);
       });
```

Finally, we handle what happens when the user presses submit. We grab all the values that are in the form, and generate a big string that we can pass around between functions and handle nicely in python. This is the `full_info` thing we made earlier.
As I mention in the comments to this code, I kind of think this is a bad way of doing things. It depends on the structure of the page? Wouldn't it be nice to just be able to grab them by a certain ID or class? I couldn't get that to work, but you could try!
```
      // on submit we generate full_info
      $("#searchers_form").submit(function(event) {
        // uncomment to prevent page submit
        // event.preventDefault();
        var the_request = "";
        $("#searchers").children().each(function() {
          // THIS IS A BAD WAY OF DOING IT THAT DEPENDS ON THE STRUCTURE OF THE PAGE
          var text  = $(this).children().children().children(".search_text").val();
          var logic = $(this).children().children(".logic_option").val();
          var field = $(this).children().children(".field_option").val();
          the_request += text + "^" + logic + "^" + field+"^";

        });        
        $("#full_info").val(the_request);
      });
    </script>
```
And we are done with the first part of it! Woo! You should be able to click around and make sure everything except the submit button works. You could even uncomment the one line in the submit section and add a `console.log()` to see if it is generating `full_info` correctly! 

## The views page and associated functions (Python)

### views.py
Good news! This part is really easy!
```

def search(request):
    context = filtering.filter_by_keyword(request)
    return render(request, 'search/search.html', context)
```
Remember when we left the action of our form blank? Go back and fill that in, have it call this! If you have namespacing set up, it looks like `action="{% url 'mysite:search' %}`. Otherwise, it looks like `action="{% url 'search' %}"`. Either way, you also need a url in `urls.py` that looks like:
```
url(r'^search_results/$', views.search, name='search'),
```
Note that `'search/search.html'` is the template that is our results page. It might be good to start calling it `'search/results_page.html'` or something else that makes you even more happy.

Bad news! The views part is so easy because we use a function that does not yet exists. We effectively are saving the work for later! Will get to it in just a sec, but first let's make that basic results page.

### results page
Again, I'd probably call this something like results_page.html, but in GTRP it is called search.html and with the file path`templates/search/search.html`. I might even change the filename in GTRP, it is never too late!

UPDATE: I did change it to `results_page`. So now it is at `templates/search/results_page.html`


We start by making the head of the document. Since we are using dataTables for this, we need to include that in the head of our html, which we do in the template format by adding it to the `extra_static` block. We also set up the head of the table.

```
{% block extra_static %}
<link rel="stylesheet" type="text/css" href="http://code.jquery.com/ui/1.10.4/themes/ui-lightness/jquery-ui.css"/>
<link rel="stylesheet" href="//cdn.datatables.net/1.10.16/css/jquery.dataTables.min.css">
<link rel="stylesheet" href="{% static 'gtr_site/css/iThing.css' %}" type="text/css" />
<script src="//cdn.datatables.net/1.10.16/js/jquery.dataTables.min.js"></script>
<script src="{% static 'gtr_site/js/search_results.js' %}"></script>
{% endblock %}

{% block content %}
<div class= "col-md-9 top-buffer" id="search_table">
  <table id="mainTable" class="table table-bordered">
    <thead>
      <tr>
        <!-- this is where the table headers go-->
        <th>Title</th>
        <th>Author</th>
        <th>Issue Date</th>
      </tr>
    </thead>
```

Now we are going to be making the body of the table. As we iterate through the results our search function is going to be giving us, each result is an instance of the object/model we wanted to search on. In the case of GTRP, the results are statements. The Statment model has fields like `title`, `author`, and `issue_date`. `get_absolute_url` is a method the statement class/model has. All the statements have affiliated statement pages that contain all the metadata for that statement. `get_absolute_url` makes an actual link the that page. If you need something like this, in GTRP, it looks like this: 
```
    def get_absolute_url(self):
        return reverse('gtr_site:statement', args=[self.statement_id])
```
But you don't neccessarily need that.

Now, the table body code:
```
    <tbody>
    <!-- now we iterate through the results -->
    {% for result in results %}
      <tr>
        <!-- this is how each row is filled with data -->
        <td><a href="{{ result.get_absolute_url }}">{{ result.title }}</a></td>
        <td><a href="author/{{ result.author }}">{{ result.author }}</a></td>
        <td>{{ result.issue_date}}</td>
        <td>{{ result.keyword_str }}</td> <!-- What's this? I don't really know, it might be a feature of datatables? When I delete it, things went bad, including the ability to sort ascending/descending on columns -->
      </tr>
    {% endfor %}
    </tbody>
  </table>
  </div>
  {% endblock %}
```

Again, you will need to change this a little so it matches what you want to display, which is a big thing to think about! Now we can move on the the actual searching functions.

### filtering.py and advanced_search.py

If you remember from before, our view function called something from `filtering.py`. We will be doing basically the same stuff when we are filtering and when we are just doing an initial search, so the view just calls filtering, then filtering calls something in `advanced_search.py` and then some other stuff if additional filtering is involved. In fact, we probably want to look at `advanced_search.py` first, so let's do it!

#### advanced_search.py

```
from models import *
from django.db.models import Q
import time
import generate_keywords_from_statement_list
```
We almost always start by importing things, and here we import something we still need to write. We can look at that after we sort out advanced_search.

Now we get into the meat of the `advanced_search` function. Remember the `full_info` string we made with javascript in the first part? The first thing we do is split `full_info` up into nice python data structures. Our finished product is a list of dictionaries, each of which has three entries: `search_string` which is the string we want to search on, `logic` which is the logical operator that was selected and `field` which natually is the field that was chosen. In python style that's:

`[{search_string : 'the_first_searched_string', logic : '', field : 'Any Field'}, 
  {search_string : 'the_second_searched_string', logic : 'OR', field : 'Keyword'},
  .
  .
  .
  {search_string : 'the_last_searched_string', logic : 'AND', field : 'Any Field'}]`
  
Notice the first entry does not have a logical operator. That's okay, I actually meant to do that. And now, here is how we make the data structure:
```
def advanced_search(request):

    # right now it looks like [Iraq^^Any Field^Iran^OR^Keyword^]
    # so we split on ^ and delete the last one (there is always a tailing empty list)
    request_list = request.GET["full_info"].split("^")[:-1]
    print "full info in advanced_search", request.GET["full_info"]
    # request list needs to be split into threes
    # right now it looks like ['Iraq','','Any Field', 'Iran', 'OR', 'Keyword,...]
    # note that the first one will not have the logical operator
    start = time.time() 
    formatted_request_list = []
    ticker = 1
    three_pair = {}
    for item in request_list:
        if ticker == 1:
            three_pair["search_string"] = item
        elif ticker == 2:
            three_pair["logic"] = item
        elif ticker == 3:
            three_pair["field"] = item
            formatted_request_list.append(three_pair)
            three_pair = {}
            ticker = 0 # set to zero since we are going inc after
        ticker += 1
```
The next thing we do is actually make the query, which is a Django Q object. We string together the query pieces with `&` and `|` which are the logical operators for Django Q's. There is also `~` which is the `NOT` operator. To get the 'query pieces' or `query_parts`'s as I call them in the code, we need a new function. Go ahead and make the new function, `make_query_part` a little bit down your page. 

```
def make_query_part(search_string, field):
    print field
    if field == "Any field":
        query_part = Q( 
                 Q(title__icontains=search_string) |
                 Q(statement_id__icontains=search_string) |
                 Q(author__person_name__icontains=search_string) |
                 Q(released_by__org_name__icontains=search_string) |
                 Q(keywords__main_keyword__word=search_string) |
                 Q(keywords__context__word=search_string)
                ) 
    elif field == 'Title':
        query_part = Q(title__icontains=search_string)
    elif field == 'Statement ID':
        query_part = Q(statement_id__icontains=search_string)
    elif field == 'Author':
        query_part = Q(author__person_name__icontains=search_string)
    elif field == 'Organization':
        query_part = Q(released_by__org_name__icontains=search_string)
    elif field == 'Keyword':
        query_part = Q(keywords__main_keyword__word=search_string)
    elif field == 'Context':
        query_part = Q(keywords__context__word=search_string)
    elif field == 'Keyword in Context':
        # at this point, I assume the user separates it with '->'
        # this may not be what we want 
        try:
            keyword, context = search_string.split('->')
        except ValueError:
            print "Keyword in Context should be in the form 'keyword->Context'"
            return False 
        keyword = keyword.strip()
        context = context.strip()
        query_part = Q(keywords__main_keyword__word=keyword) & Q(keywords__context__word=context)
    else:
        query_part = None
    return query_part

```
Basically, we create a Q() object for the selected field, filtering with the given `search_string`. I think this function is generally pretty clear if you have a grip on navigating Django foreign key/many-to-many fields. If you don't, I'll briefly talk about it!

Each of these Q() objects is going to be searching for statements. So the first word, say `released_by`, is a field of the statement model that we want to be able to search on. The `__org_name` follows backwards along a foreign key relation since organizations are their own model and looks at the field `org_name` in that organization model. Then we use a special Django Q() thing `__icontains` which tells the Q() to match a statement if the field contains whatever is in `search_string`. So in summary, `Q(released_by__org_name__icontains=search_string)` means 'match statements that for the field `released_by` have `search_string` contained in the `org_name` field of organization.

You *absolutely* will need to change this function to match your data, but it will likely will be very much in the same style. First you have the `Any Field` option. This query is just all the other field options OR'd together. Then, we just have a bunch of elseif's to match the field options we had in our drop dowm. For GTRP, we had to do some fancy-footwork for the `Keyword in Context` field, something you might not have to do, but I left it in to remind you that you can! 

Now that we have query_parts, we can combine them. Let's pop back into the main body of `advanced_search.py`, we are going to make a query!

```
def advanced_search(request):
    .
    .
    .
    for item in request_list:
        if ticker == 1:
            three_pair["search_string"] = item
        elif ticker == 2:
            three_pair["logic"] = item
        elif ticker == 3:
            three_pair["field"] = item
            formatted_request_list.append(three_pair)
            three_pair = {}
            ticker = 0 # set to zero since we are going inc after
        ticker += 1
	
    ### HERE IS THE NEW STUFF WHERE WE BUILD A QUERY ###

    query = []
    for request_part in formatted_request_list:
            search_string = request_part["search_string"]
            logic         = request_part["logic"]
            field         = request_part["field"]
            query_part = make_query_part(search_string, field)
            if query and query_part:
               if   logic == "AND":
                   query = query & query_part
               elif logic == "OR":
                   query = query | query_part
               elif logic == "NOT":
                   query = query & ~query_part 
            elif query_part:
               query = query_part
            else:
               return False
    print "Here is your query", query
```
Woo, we made a query! We iterate through all our dictionaries, making query parts and then adding them on to the rest of our query with the appropriate logic.

Next we just run the query, and return the appropriate context, which is easy money!
```
    statement_list = Statement.objects.all()
    statement_list = statement_list.filter(query).distinct()	
    context = {'results' : statement_list, 'search' : search_string, 'full_info' : request.GET["full_info"], 'num_results' : len(statement_list)}
    return context
```
And that's the end of it! If you temporarily change the `search` view so it calls this instead of `filtering`, we should be able to test what we have thus far! Try it and see if something goes wrong, I am regrettably not following along on my own machine. 

If you are happy with this level of functionality, you can probably stop here! The next thing we are going to be doing is adding additional filtering capabilities, so that we can refine the results of our query. If you want to continue and do that, it turns out we don't really use the function we just wrote :(

We do something _super_ similar though. Instead executing the query, we just make it, so that we can give that to filtering and then make an even bigger query! Here is what that looks like for me, I made a separate function and just deleted the last couple steps of the old one, adding in a `return query` line.

```
# used for filtering
def advanced_search_make_query(request):
    print request
    request_list = request.GET["full_info"].split("^")
    print "Request List in advanced_search_make_query", request_list
    # request list needs to be split into threes
    # right now it looks like ['Iraq','','Any Field', 'Iran', 'OR', 'Keyword,...]
    # note that the first one will not have the logical operator
    formatted_request_list = []
    ticker = 1
    three_pair = {}
    for item in request_list:
        if ticker == 1:
            three_pair["search_string"] = item
        elif ticker == 2:
            three_pair["logic"] = item
        elif ticker == 3:
            three_pair["field"] = item
            formatted_request_list.append(three_pair)
            three_pair = {}
            ticker = 0 # set to zero since we are going inc after
        ticker += 1

    query = []
    for request_part in formatted_request_list:
            search_string = request_part["search_string"]
            logic         = request_part["logic"]
            field         = request_part["field"]
            query_part = make_query_part(search_string, field)
            if query and query_part:
               if   logic == "AND":
                   query = query & query_part
               elif logic == "OR":
                   query = query | query_part
               elif logic == "NOT":
                   query = query & ~query_part 
            elif query_part:
               query = query_part
return query
```

#### filtering.py
Go ahead and make a new file, call it `filtering.py`. As a standard first step, we import some things. `generate_keywords_from_statement_list` is a function we are going to write, but don't worry about it yet.
 
```
from models import *
from django.db.models import Q
import time
import generate_keywords_from_statement_list
import advanced_search
import datetime
import json
```

Here we are looking at the request and seeing what all is included and excluded. We put `a_keyword = 'key_ON'` if we want to include `a_keyword` e.g. `'Iraq = 'key_ON`. Similarly, we put `a_keyword = 'key_OFF'` if we want to exclude a keyword. This information will be coming to us hot from the `results_page` template.

```
def filter_by_keyword(request):
    include = []
    exclude = []
    print request.GET
    for key in request.GET:
        key_ON_OFF = request.GET[key]
	if   key_ON_OFF == 'key_ON':
            include.append(key)
        elif key_ON_OFF == 'key_OFF':
            exclude.append(key)
```
Next we generate the base query using the `advanced_search` function we wrote!

```
    # base query without any filtering (including or excluding)
    # we will build it up with relevant filtering
    start = time.time()
    query = advanced_search.advanced_search_make_query(request) 
    print "Time for generating intial query", time.time() - start
    # query = request.POST.get('search', False)

    print "Query: ", query
```
Next, we call the query we have so far, then further refine that list of statements based on the items in include and exclude. We run the filtering for each item in the list, because it didn't work when I tried to build up another query. Looking back, maybe if we _don't_ call the initial query and build more on that it would work. But, it doesn't actually take that long to query, so I don't think it is worth me testing out.
```
    start - time.time()
    statement_list = Statement.objects.all()
    statement_list = statement_list.filter(query).distinct()
    print "Time for all unique_keywords", time.time() - start

    print "Including Statements with Keywords:", include
    start = time.time()
    if include:
        include_query = Q(keywords__main_keyword__word=include[0])
        for keyword in include[1:]:
	    include_query = include_query | Q(keywords__main_keyword__word=keyword)
        print "Include query: ", include_query
	statement_list = statement_list.filter(include_query).distinct()
    print "Time for all including", time.time() - start

    print "Excluding Statements with Keywords:", exclude
    start = time.time()
    if exclude:
        exclude_query = Q(keywords__main_keyword__word=exclude[0])
        for keyword in exclude[1:]:
	    exclude_query = exclude_query | Q(keywords__main_keyword__word=keyword)
        query = query & ~exclude_query
        statement_list = statement_list.filter(~exclude_query).distinct()
    print "Time for all excluding", time.time() - start
```    
In gtrp, we also wanted to get a count of the number of statements the keyword appears in. This is what `generate_keywords_from_statement_list` does. You'll probably need a list of things to filter on too, but I would highly recommend setting up the data in a different way. I'm not sure if I am doing something stupid, or if the models were set up poorly, but this takes a computationally long time to do.
    
You can make a separate file called `generate_keywords_from_statement_list`. The code for this pretty close to stands on its own. In `generate_keywords_dictionary`, `get_keywords_unique` is a method in the statement model that gives us all the keyowrds for that statement. We iterate through that set, adding to a count if the keyword is in keywords_dict, or adding it to the dictionary if it isn't already there. The other functions just build on that function and make it convinient to call.
    
```
"""
Functions currently used in filtering.py pertaining to getting the right keywords for display.
"""
from models import *
import time

def generate_keywords_dictionary(statement_list):
    """
       given a list of statement (like the one returned when you query the DB)
       find all the keywords linked to those statements and the number of time the are linked
       return a dictionary where keys are keywords and values are that number:  {Iraq : 300}
    """

    start = time.time()
    keywords_dict = {}
    for statement in statement_list:
        statement_keywords = statement.get_keywords_unique()
	for keyword in statement_keywords:
	    if keyword in keywords_dict:
	        keywords_dict[keyword]+=1
	    else:
		keywords_dict[keyword] = 1
    print "generating keywords took", time.time() - start, "seconds"
    return keywords_dict


def get_top_keywords(keywords_dict, top_n):
    """
    Used to get the top results to display for keyword filtering
    Given a dictionary of keywords as keys and the number of times that keyword is linked to a statement in the search results: {Iraq : 300}
    Returns the top n results as as list of pairs, ordered by appearances: [(Iraq, 300), (Iran, 200)]
    """
    return sorted(keywords_dict.items(), key=lambda student: student[1], reverse=True)[:top_n]


    
def generate_top_n_keywords(statement_list, top_n):
    """
     Generates and gets top n keywords.
    """
    return get_top_keywords(generate_keywords_dictionary(statement_list), top_n)

def generate_just_keywords(statement_list):
    """
       You might need this and I already wrote it!
       but nothing uses it as of right now...
       Returns a set of keywords
    """
    start = time.time()
    keywords = set()
    keyword_sets = [set(statement.get_keywords()) for statement in qs_list]
    keywords = keywords.union(*keyword_sets)
    print "generating keywords took", time.time() - start, "seconds"
return keywords
```
Now we go back to where we were in `filtering.py` and use our shiny new function.
    
    ```
    include_keywords_and_counts = generate_keywords_from_statement_list.generate_top_n_keywords(statement_list, 50)
    print include_keywords_and_counts
    # Add the excluded keywords back to the list, and truncate it to 20 entries.
    exclude_keywords_and_counts = include_keywords_and_counts[:]
    for exc in exclude:
        exclude_keywords_and_counts.insert(0, [exc, 'x'])
    exclude_keywords_and_counts = exclude_keywords_and_counts[:20]
    keywords = [key_count[0] for key_count in include_keywords_and_counts]
    ```
We also do some filtering by date in gtrp, but I haven't written about that. You can check it out in the code, or just not do it. Regardless, this next line related to that.
    ```
    if 'filter_by_date' in request.GET:
        if request.GET['filter_by_date']=='date_ON':
            date_query, date_list = filter_by_date(request)
            statement_list =  statement_list.filter(date_query)
    ```
Now we want to save some things so our results can carry over. We might not need to do this anymore, we really changed the way we were filtering. We started filtering with javascript on the client side, and I didn't really do that. I can tell you we now dump all the data into a json object a hand that over to the client, then it filters really quickly!

```
    # now we store what we have included and excluded
    # passing it in the context
    # so the checked buttons and the shown statement carry over to the next filtering sesh

    include_str = '["' + '", "'.join(include) + '"]'
    exclude_str = '["' + '", "'.join(exclude) + '"]'
    start = time.time()
    all_keywords = set()
    for statement in statement_list:
        unique_keywords = set(kic.main_keyword.word for kic in statement.keywords.all())
        all_keywords |= unique_keywords
        statement.keyword_str = '|' + '|'.join(unique_keywords) + '|'
    print "Time for all unique_keywords", time.time() - start
    context = {'results' : statement_list,
               'json_results': serialize_statements(statement_list),
               'keywords' : keywords,
               'include_buttons': include_str,
               'exclude_buttons': exclude_str,
               'include_keywords_and_counts': [],
               'exclude_keywords_and_counts': [],
               'full_info' : request.GET['full_info'],
               'num_results' : len(statement_list),
               'all_keywords': json.dumps(list(all_keywords))
              }
    if 'filter_by_date' in request.GET:
        context['slider_count'] = request.GET['slider_count']
        context['date_list'] = date_list
    return context

```

Here are some more functions to deal with fitlering by date and serializing our objects to json. 
```
def filter_by_date(request):
    print request.GET
    date_list = []
    for i in range(1, int(request.GET['slider_count']) + 1):
	lowDate = datetime.datetime.strptime(request.GET["date_low"+str(i)][:24], "%a %b %d %Y %X")
	highDate = datetime.datetime.strptime(request.GET["date_high"+str(i)][:24], "%a %b %d %Y %X")
        date_list.append((lowDate.strftime("%Y, %m, %d"), highDate.strftime("%Y, %m, %d")))
	if i==1:
	    date_query = Q(issue_date__gte=lowDate,
                           issue_date__lte=highDate)
	else:
	    date_query = date_query | Q(issue_date__gte=lowDate, issue_date__lte=highDate)
    return date_query, date_list


def filter_by_context():
    pass


def filter_by_keycon():
    pass


def update_full_info(include=[], exclude=[]):
    for keyword in include:
        pass
    # here for next time


def serialize_statements(statement_list):
    """Serialize a list of Statement objects into a JSON list so that it can be loaded and
    manipulated by the client-side JavaScript.
    """
    return json.dumps([statement_to_dictionary(st) for st in statement_list])

def statement_to_dictionary(statement):
    """Convert a Statement object into a dictionary (in prep for JSON serialization)."""
    keywords = [kic.main_keyword.word for kic in statement.keywords.all()]
    author = statement.author.person_name
return {'title': statement.title, 'author': author, 'keywords': keywords}
```
#### A final update to results page
We have just this last thing to do. I'm sure you will have to debug too!. We now filter based in additional keyword constraints, but the user doesn't have a good way of exploring and selecting the keyword they want to filter with. Basically, we are going to add a bunch of checkboxes. Going back to `templates/search/results_page.html`, add in on the top:
```
<div class="row">
  <div class="col-md-3 top-buffer" id="search_filter">
    <h3>Your query returned {{ num_results }} results</h3>
    <h3>Filter Keywords</h3>
    <h4>Include</h4>
      <ul class="list-group" id="include-buttons">
      {% for keyword in keywords %}
        <li class="list-group-item justify-content-between">
          <input type="checkbox" name="{{ keyword }}" value="key_ON" class="filter_check form-check-input include-checkbox">
          {{ keyword }}
          <span class="badge badge-default badge-pill">-1</span>
        </li>
      {% endfor %}
      </ul>
      <h4>Exclude</h4>
      <ul class="list-group" id="exclude-buttons">
      {% for keyword in keywords %}
        <li class="list-group-item justify-content-between">
          <input type="checkbox" name="{{ keyword }}" value="key_OFF" class="filter_check form-check-input exclude-checkbox">
            {{ keyword }}
            <span class="badge badge-default badge-pill">{{ -1 }}</span>
        </li>
      {% endfor %}
      </ul>
</div>
```

Also, add this at the end, before the end of the content block
```
<script>
{% autoescape off %}
var jsonResults = {{ json_results }};
var allKeywords = {{ all_keywords }};
{% endautoescape %}
</script>
```

So, all together you should have:
```
{% block extra_static %}
<link rel="stylesheet" type="text/css" href="http://code.jquery.com/ui/1.10.4/themes/ui-lightness/jquery-ui.css"/>
<link rel="stylesheet" href="//cdn.datatables.net/1.10.16/css/jquery.dataTables.min.css">
<link rel="stylesheet" href="{% static 'gtr_site/css/iThing.css' %}" type="text/css" />
<script src="//cdn.datatables.net/1.10.16/js/jquery.dataTables.min.js"></script>
<script src="{% static 'gtr_site/js/search_results.js' %}"></script>
{% endblock %}

{% block content %}
<div class="row">
  <div class="col-md-3 top-buffer" id="search_filter">
    <h3>Your query returned {{ num_results }} results</h3>
    <h3>Filter Keywords</h3>
    <h4>Include</h4>
      <ul class="list-group" id="include-buttons">
      {% for keyword in keywords %}
        <li class="list-group-item justify-content-between">
          <input type="checkbox" name="{{ keyword }}" value="key_ON" class="filter_check form-check-input include-checkbox">
          {{ keyword }}
          <span class="badge badge-default badge-pill">-1</span>
        </li>
      {% endfor %}
      </ul>
      <h4>Exclude</h4>
      <ul class="list-group" id="exclude-buttons">
      {% for keyword in keywords %}
        <li class="list-group-item justify-content-between">
          <input type="checkbox" name="{{ keyword }}" value="key_OFF" class="filter_check form-check-input exclude-checkbox">
            {{ keyword }}
            <span class="badge badge-default badge-pill">{{ -1 }}</span>
        </li>
      {% endfor %}
      </ul>
 </div>
 <div class= "col-md-9 top-buffer" id="search_table">
  <table id="mainTable" class="table table-bordered">
    <thead>
      <tr>
        <!-- this is where the table headers go-->
        <th>Title</th>
        <th>Author</th>
        <th>Issue Date</th>
      </tr>
    </thead>
    <tbody>
    <!-- now we iterate through the results -->
    {% for result in results %}
      <tr>
        <!-- this is how each row is filled with data -->
        <td><a href="{{ result.get_absolute_url }}">{{ result.title }}</a></td>
        <td><a href="author/{{ result.author }}">{{ result.author }}</a></td>
        <td>{{ result.issue_date}}</td>
        <td>{{ result.keyword_str }}</td> <!-- What's this? I don't really know, it might be a feature of datatables? When I delete it, things went bad, including the ability to sort ascending/descending on columns -->
      </tr>
    {% endfor %}
    </tbody>
  </table>
  </div>
</div> <!-- end of row div -->
<script>
{% autoescape off %}
var jsonResults = {{ json_results }};
var allKeywords = {{ all_keywords }};
{% endautoescape %}
</script>
  {% endblock %}
```

Now you should have nice pushy buttons on your results page!
