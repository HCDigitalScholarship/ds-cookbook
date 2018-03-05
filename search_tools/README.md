# Advanced Searching with Django Q()'s
In this tutorial, I'll cover how to make an advanced search tool like the one used in the [Global Terrorism Research Project](http://gtrp.haverford.edu/).
All of the querying is handled with [standard Django querying and filtering](https://docs.djangoproject.com/en/2.0/topics/db/queries/) in addition with [Django Q()'s](https://docs.djangoproject.com/en/2.0/topics/db/queries/#complex-lookups-with-q-objects).
I recommend taking a look at those links for more details, or if you run into any problems.

## Making the search bars (JavaScript and HTML)
Before we can query our data, we need the user to tell us what they want! I built my search bars in plain-old HTML and jQuery.
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

_Uh, this next part doesn't do anything?_ I think I was in the process of doing something else.
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
And we are done with the first part of it! Woo!

## The views page and associated functions (Python)

