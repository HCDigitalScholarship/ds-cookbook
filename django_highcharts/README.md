# Highcharts.js with Django

In this tutorial (largely based on this coding [tutorial](https://simpleisbetterthancomplex.com/tutorial/2018/04/03/how-to-integrate-highcharts-js-with-django.html) describing how to use Highcharts in a Django template), I will explain how to install Highcharts and use it to display data from a Django model. 

Highcharts are used to create javascript charts that can be inserted into any html file. They include line charts, area charts, column charts, pie charts, and scatter charts. Additionally, each chart can have a legend, clickable links, data-tags, and more.   

---

## Highcharts example inside a Django template

1. Inside the 'body' tag of a Django template, add a 'div' tag with a unique class in the location you want to display the chart:  
  
   ```
   <body>
     <div id="id_of_the_container"></div>
   ```
  
2. Then, insert the Highcharts library CDN:
    
    ```
    <script src="https://code.highcharts.com/highcharts.src.js"></script>
    ```

3. Now you can insert the code that builds the chart inside a 'script' tag, using the basic structure:
    
    ```
    <script>
      Highcharts.chart('id_of_the_container', {
        // chart configuration
      });
    </script>
    ```

4. Below is code for an example chart. The 'type' field can be changed to any of the available chart types, each of which has a unique structure and fieldset. The 'data' field inside 'series' holds the names and values for each data point.

    ```
    <script>
      Highcharts.chart('container', {
        chart: {
          type: 'pie'
        },
        title: {
          text: 'Historic World Population by Region'
        },
        series: [{
          name: 'Brands',
          data: [{
            name: 'Chrome',
            y: 61.41,
          }, {
            name: 'Internet Explorer',
            y: 18.85
          }, {
            name: 'Safari',
            y: 17.90
          }, {
            name: 'Other',
            y: 11.84
          }]
        }]
      });
    </script>
    ```
    
---
## Using Highcharts on data from a Django model

You will want to follow the steps above to insert a Highcharts chart inside a Django template. Then, you will want to change the 'data' field to:

    ```
    data: [{% for object in Django_model_name %}{name: '{{ object.name }}', y: {{ object.value }} }{% if not forloop.last %}, {% endif %}{% endfor %}]
    ```

---
## Adding clickable links to a Highchart

Again, the initial setup for the chart can be found in the steps above. However, you will want to add the following steps to your process:

1. Add the 'plotOptions' field and its contents to your chart:

    ```
    chart: {type: 'pie'},
    title: {text: ''},
    plotOptions: {
      series: {
        cursor: 'pointer',
        point: {
          events: {
            click: function () {
              location.href = 'https://example_url/' + this.options.key;
            }
          }
        }
      }
    },
    ```

2. Add a 'key' field to each data point listed in the 'data' field:

    ```
    series: [{
      name: 'Brands',
      data: [{
        name: 'Chrome',
        y: 61.41,
        key: 'unique_url_end/'
      }, {
        name: 'Internet Explorer',
        y: 18.85
        key: 'other_url_end/'
      }, {
        name: 'Safari',
        y: 17.90
        key: 'different_url_end/'
      }, {
        name: 'Other',
        y: 11.84
        key: 'rare_url_end/'
      }]
    }]
    ```
