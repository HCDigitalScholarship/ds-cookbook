# This is an entry on how to generate a simple network visualization using Django and D3.  (based off of [this](http://bl.ocks.org/jose187/4733747))

The data for this example is a list of bestselling novels.  Each bestseller has an author, a title and a publisher. 
First off, let's create a view.  We'll load all of the BestsellerList objects from the database and create a dictionary with the formatting expected by D3.

```json
{
      "nodes":[
            {"name":"node1","group":1},
            {"name":"node2","group":2},
            {"name":"node3","group":2},
            {"name":"node4","group":3}
        ],
        "links":[
            {"source":2,"target":1,"weight":1},
            {"source":0,"target":2,"weight":3}
        ]
    }
```
The view creates a list of each distinct author, title and publisher.  We then add each author, title and publisher to the list of nodes.
Finally, we iterate over all the bestsellers and create edges in the graph.  Currently, we're creating author to title edges, author to publisher,
and publisher to title edges.  These can be changed based on your project.  The end result is a url that serves all of the json needed for the visualization. 

```python
def network_json(request):

    bestsellers = BestsellerList.objects.all()
    graph = {"nodes": [], "links": []}

    # create nodes for authors, titles, publishers,
    authors = set([bestseller.author for bestseller in bestsellers])
    for author in authors:
        graph['nodes'].append({"name":author,"group":1},)

    publishers = set([bestseller.publisher for bestseller in bestsellers])
    for publisher in publishers:
        graph['nodes'].append({"name":publisher,"group":1},)
    titles = set([bestseller.title for bestseller in bestsellers])
    for title in titles:
        graph['nodes'].append({"name":title,"group":1},)

    for bestseller in bestsellers:

        author = graph['nodes'].index({"name":bestseller.author,"group":1},)
        title = graph['nodes'].index({"name":bestseller.title,"group":1},)
        publisher = graph['nodes'].index({"name":bestseller.publisher,"group":1},)

        # author-title edge
        graph['links'].append({"source": author, "target": title, "weight": 1},)
        # author-publisher edge
        graph['links'].append({"source": author, "target": publisher, "weight": 1},)
        # publisher-title edge
        graph['links'].append({"source": publisher, "target": title, "weight": 1},)

    response = JsonResponse(graph)
    return response
    ```
    
    In the template,  you'll need a couple of things: 
    1) The code for D3
    <script src="http://d3js.org/d3.v2.min.js?2.9.3"></script>
    
    2) Some CSS for the visualization:
    ```html
    <style>

.link {
  stroke: #FC9CE7;
}

.node text {
stroke:#333;
cursos:pointer;
}

.node circle{
stroke:#AA9CFC;
stroke-width:3px;
fill:#555;
}

</style>
```

3) An html tag to place the graph, in this case, it's just <body>

4) Finally here's the javascript needed to create the graph.  Note the Django template url reference.  There is a path in urls.py called network_json, which
in turn points to the view above (also named network_json):
```javascript
<script>

var width = 1200,
    height = 1200

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

var force = d3.layout.force()
    .gravity(.05)
    .distance(100)
    .charge(-100)
    .size([width, height]);

d3.json("{% url 'network_json' %}", function(json) {
  force
      .nodes(json.nodes)
      .links(json.links)
      .start();

  var link = svg.selectAll(".link")
      .data(json.links)
    .enter().append("line")
      .style("fill", function (d) { return '#FC9CE7'; })
      .attr("class", "link")
    .style("stroke-width", function(d) { return Math.sqrt(d.weight); });

  var node = svg.selectAll(".node")
      .data(json.nodes)
    .enter().append("g")
      .style("fill", function (d) { return '#AA9CFC'; })
      .attr("class", "node")
      .call(force.drag);

  node.append("circle")
      .attr("r","5");


  node.append("text")
      .style("fill", function (d) { return '#AA9CFC'; })
      .attr("dx", 12)
      .attr("dy", ".35em")
      .text(function(d) { return d.name });

  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
  });
});

```
