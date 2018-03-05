# Advanced Searching with Django Q()'s
In this tutorial, I'll cover how to make an advanced search tool like the one used in the [Global Terrorism Research Project](http://gtrp.haverford.edu/).
All of the querying is handled with [standard Django querying and filtering](https://docs.djangoproject.com/en/2.0/topics/db/queries/) in addition with [Django Q()'s](https://docs.djangoproject.com/en/2.0/topics/db/queries/#complex-lookups-with-q-objects).
I recommend taking a look at those links for more details, or if you run into any problems.

## Making the search bars (JavaScript and HTML)
Before we can query our data, we need the user to tell us what they want! I built my search bars in plain-old HTML and jQuery. For me, this is just on the index page, but you might want it somewhere else.
The first thing we do is build a form. We don't actually have any search bars yet though! We will add those in dynamically with javascript later.

```
<form id="searchers_form"  action="mysite:searchview" method="GET">
    <div class="form-group" id="searchers">
        <div id="searcher1"></div>
    </div>
    <input id="full_info" type="hidden" value='' name="full_info">
</form>
```
`full_info` will be a string that keeps track of the complete user query. We can pass this around easily and build it up if the user later wants to refine their results. You want the action to point the 'search' function in your views. If you are following this, that does not exist yet. Don't worry, you can leave it blank for now!

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

Unfortunately, the views part is so easy because we use a function that does not yet exists. This part is easy because we saved the work for later! Let's do it now and making the filtering functions. 

### filtering.py and advanced_search.py

Make a new python file, I called it `filtering.py`. We will be basically the same stuff when we are filtering and when we are just doing this initial search, so the view just calls filtering, then filtering calls advanced search.

Let's take a look at filtering.py:
```
from models import *
from django.db.models import Q
import time
import generate_keywords_from_statement_list
import advanced_search
import datetime
import json
```

As a standard first step, we import some things. Both `generate_keywords_from_statement_list` and `advanced_search` are functions we are going to write.

Let's actually take a look at the `advanced_search` part of it, which is much more relevant to what we have done thus far. Go ahead and make a file called `advanced_search.py`.

What does advanced search look like. Good question!
```
from models import *
from django.db.models import Q
import time
import generate_keywords_from_statement_list
```
Again, we import something we need to write. We can look at that after we sort out advanced_search.

The next thing we do is split our full_info up into nice python data structures. Our finished product is a list of dictionaries, each of which has three entries: `search_string` which is the string we want to search on, `logic` which is the logical operator that was selected and `field` which natually is the field that was chosen. 

```
def advanced_search(request):

    # right now it looks like [Iraq^^Any Field^Iran^OR^Keyword^]
    # so we split on ^ and delete the last one (there is always a tailing empty list
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
The next thing we do is actually make the query, which is a Django Q object. We string together the bits of queries with `&` and `|` which are the logical operators for Django Q's. There is also `~` which is the not operator. We also use a function we need to write. Go ahead a make this one just a bit further down the page.

NEXT STEP MAKE QUERY PART
```
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
    statement_list = Statement.objects.all()
    print "Here is your query", query
    statement_list = statement_list.filter(query).distinct()
    print "generating statement_list took", time.time() - start, "seconds"

    # now generate the list of keywords
    # This is a little slow
    start = time.time()
    keywords_and_counts = generate_keywords_from_statement_list.generate_top_n_keywords(statement_list, 20)
    keywords = [key_count[0] for key_count in keywords_and_counts]
    print "generating keywords took", time.time() - start, "seconds"
    for statement in statement_list:
	print statement
    context = {'results' : statement_list, 'keywords' : keywords, 'keywords_and_counts' : keywords_and_counts, 'search' : search_string, 'full_info' : request.GET["full_info"], 'num_results' : len(statement_list)}
    return context


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





Next we get into the filtering part of it. This is how we will refine our search.

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
Here we are looking at the request and seeing what all is included and excluded.
```
    # base query without any filtering (including or excluding)
    # we will build it up with relevant filtering
    start = time.time()
    query = advanced_search.advanced_search_make_query(request) 
    print "Time for generating intial query", time.time() - start
    # query = request.POST.get('search', False)

    print "Query: ", query

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
    include_keywords_and_counts = generate_keywords_from_statement_list.generate_top_n_keywords(statement_list, 50)
    print include_keywords_and_counts
    # Add the excluded keywords back to the list, and truncate it to 20 entries.
    exclude_keywords_and_counts = include_keywords_and_counts[:]
    for exc in exclude:
        exclude_keywords_and_counts.insert(0, [exc, 'x'])
    exclude_keywords_and_counts = exclude_keywords_and_counts[:20]
    keywords = [key_count[0] for key_count in include_keywords_and_counts]
    if 'filter_by_date' in request.GET:
        if request.GET['filter_by_date']=='date_ON':
            date_query, date_list = filter_by_date(request)
            statement_list =  statement_list.filter(date_query)

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

