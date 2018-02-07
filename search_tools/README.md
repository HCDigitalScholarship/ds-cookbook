# Advanced Searching with Django Q()'s
In this tutorial, I'll cover how to make an advanced search tool like the one used in the [Global Terrorism Research Project](http://gtrp.haverford.edu/).
All of the querying is handled with [standard Django querying and filtering](https://docs.djangoproject.com/en/2.0/topics/db/queries/) in addition with [Django Q()'s](https://docs.djangoproject.com/en/2.0/topics/db/queries/#complex-lookups-with-q-objects).
I recommend taking a look at those links for more details, or if you run into any problems.

## Making the search bars (JavaScript and HTML)
Before we can query our data, we need the user to tell us what they want! I built my search bars in plain-old HTML and JQUERY.
The first thing we do is build a form. We don't actually have and searchbars yet though! We will add those in dynamically with javascript later.

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

