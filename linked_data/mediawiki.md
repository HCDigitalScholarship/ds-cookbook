This is a tutorial of how to use MediaWiki to get specific information of using the name of a person or organization.


## Getting Started

To interact with the MediaWiki API, an endpoint9 (i.e. an url) including specific information of what you want. An example endpoint is:

<https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles=Stack%20Overflow>

which gives a result of the text of the introduction section. In this tutorial we will be creating a similar endpoint using JQuery and AJAX to get only the information contained in the introduction section of the wiki page of each person or organization. 

## Creating MediaWiki Data and an AJAX request

To create an AJAX request to the MediaWiki API, you need to first create the data object that will be added as a parameter into the request. This data object is basically an object type (or dictionary) made up of key and value pairs specific to the API. Depending on the type of action that is being performed, these key/value pairs will be different.

```
	var dataObj1 = { format: "json", action: "query", prop: "extracts", exintro: "", explaintext: "", redirects: true};
	var x = "titles";
	var url_path = (window.location.pathname).split("/")[2];
        var auth_name = decodeURIComponent(url_path);
        dataObj1[x] = auth_name;
```
The first line defines the data for the AJAX request where format indicates the format in which you want the data returned in. You have the choice between json, jsonfm , php, txt and many more. (Follow this link for information about formats: https://www.mediawiki.org/wiki/API:Data_formats) The action key allows users to specify how they would like to receive information from the API. In this tutorial we use action: “query” , which directly fetches information from the API. (Follow this link for information about other parameters for action: https://en.wikipedia.org/w/api.php) The prop: “extracts” key value pair “returns plain-text or limited HTML extracts of the given pages.”(https://www.mediawiki.org/wiki/Extension:TextExtracts) As an extension to prop:"extracts", the keys exintro and explain text are included in the data object. Both these keys take boolean values, where no values indicates a false value (follow this link to read more about prop:extracts and its extensions > https://www.mediawiki.org/wiki/Extension:TextExtracts). The next key, redirects, is set to true so that in the case the api cannot find an exact wiki page for a given search text, it redirects to a different wiki page that is in some way related to the original search text. The last key that is added to the data object is the titles key. The titles key is where users request a specific wiki page using the name of the object, person, place, etc. In this case, we are requesting the wiki page of mainly people and organizations. To access the name of the person or organization, the url path is broken down and decoded so that the text at the end of the url (i.e the name of the organization or person) is retrieved and used as the value of the titles key.

Once the data is assembled. An AJAX request is made to the Media Wiki API using the data created above. For more information about how to format an AJAX request using jquery go to http://api.jquery.com/jquery.ajax/.

```
 	$.ajax({
                url: "https://en.wikipedia.org/w/api.php",
                data: dataObj1,
                dataType: 'jsonp',
                success: function (data) {
                        var auth_wiki_intro = Object.keys(data.query.pages)[0];
                        if(auth_wiki_intro == "-1"){
                                var noInfo = "No information currently avaliable for " + auth_name + ".";
                                $('#article').append($('<h4></h4>').html(noInfo));
                        } else{
                                var abt_header = "About " + auth_name;
                                $('#article').append($('<h4></h4>').html(abt_header));

                                var markup = data.query.pages[auth_wiki_intro].extract;

                                var i = $('<div></div>').html(markup);  
                                $('#article').append(i);
                        }

                }
	});
```
Once a call is made to the API, the request returns a json object where if there is no wiki page for the person or organization, (i.e. "Abu-Yahya al-Libi" in this case) the json object looks like:

```
	{
	  "batchcomplete": "",
	  "query": {
	    "pages": {
	      "-1": {
		"ns": 0,
		"title": "Abu-Yahya al-Libi",
		"missing": ""
	      }
	    }
	  }
	}
```
However, if there is a wiki page for the searched person or name, the json has an extract key which has the requested information.

```
	{
	  "batchcomplete": "",
	  "query": {
	    "pages": {
	      "22468": {
		"pageid": 22468,
		"ns": 0,
		"title": "Osama bin Laden",
		"extract": "Usama ibn Mohammed ibn Awad ibn Ladin (Arabic: أسامة بن محمد بن عوض بن لادن‎, usāmah ibn muḥammad ibn ‘awaḍ ibn lādin), often anglicized as Osama bin Laden (; March 10, 1957 – May 2, 2011) was the founder of al-Qaeda, the organization that was responsible for the September 11 attacks on the United States, along with numerous other mass-casualty attacks worldwide. He was a Saudi Arabian, a member of the wealthy bin Laden family, and an ethnic Yemeni Kindite.\nBin Laden was born to the family of billionaire Mohammed bin Awad bin Laden in Saudi Arabia. He studied at university in the country until 1979, when he joined Mujahideen forces in Pakistan fighting against the Soviet Union in Afghanistan. He helped to fund the Mujahideen by funneling arms, money and fighters from the Arab world into Afghanistan, and gained popularity among many Arabs. In 1988, he formed al-Qaeda. He was banished from Saudi Arabia in 1992, and shifted his base to Sudan, until U.S. pressure forced him to leave Sudan in 1996. After establishing a new base in Afghanistan, he declared a war against the United States, initiating a series of bombings and related attacks. Bin Laden was on the American Federal Bureau of Investigation's (FBI) lists of Ten Most Wanted Fugitives and Most Wanted Terrorists for his involvement in the 1998 U.S. embassy bombings.\nFrom 2001 to 2011, bin Laden was a major target of the United States, as the FBI placed a $25 million bounty on him in their search for him. On May 2, 2011, bin Laden was shot and killed inside a private residential compound in Abbottabad, where he lived with a local family from Waziristan, during a covert operation conducted by members of the United States Naval Special Warfare Development Group and Central Intelligence Agency SAD/SOG operators on the orders of U.S. President Barack Obama."
	      }
	    }
	  }
	}
```
To access only the information in the extract key and display it, you first have to check if the key pages has a value of -1. As described above, if the value is -1 then there is no wiki page for the person/organization and therefore no information to display. However, if the value is not -1, then the json object returned has an extracts key whose value is the text of the introduction from the wiki page of the person/organization. The code below handles the checking of the pages value and what to do in each case.

```
	var auth_wiki_intro = Object.keys(data.query.pages)[0];
	if(auth_wiki_intro == "-1"){
		var noInfo = "No information currently avaliable for " + auth_name + ".";
		$('#article').append($('<h4></h4>').html(noInfo));
	} else {
		var abt_header = "About " + auth_name;
		$('#article').append($('<h4></h4>').html(abt_header));
		
		var markup = data.query.pages[auth_wiki_intro].extract;
		var i = $('<div></div>').html(markup); 
		
		$('#article').append(i);
	}

```

In the first case where the value is -1, the text "No information currently avaliable " is added to the html and displayed. On the other hand, the text from the wiki page is added to the html and then displayed.
