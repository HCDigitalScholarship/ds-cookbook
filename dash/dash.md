For any project with a large dataset, it can be useful to create an interactive dashboard for users to engage and make sense of project data.  A dashboard offers multiple visualizations with ways to sort and filter the data simulatiously. There are many solutions available to create a dashboard.  Our current favorite is called [Dash](https://dash.plot.ly/), which offers a relatively easy way to define the layout and callbacks for a React.js app using Python. The layout determines what elements appear on the page, such as buttons, graphs and datatables.  A callback defines how each element is updated.   Dash apps can be added to Django projects with the [django-plotly-dash app](https://github.com/GibbsConsulting/django-plotly-dash). 

This tutorial will detail some of the basics for creating a Dash app and deploying it to an exiting Django project. 
This will serve as a suppliment to the [Dash documentation](https://dash.plot.ly/) and our existing dash-related repositories, such as Fiona and Shufan's [dashboard](https://github.com/HCDigitalScholarship/dashboard).

---

## First, install dash 
`pip install dash`  
Note: django-plotly-dash currently requires dash==0.39.0  Later versions will just show "Loading..." (April 17,2019)


## Next, import dependencies 
```python
import dash
import dash_core_components as dcc
import dash_html_components as html
```
Dash is clearly divided between core components and html components. 

[Core components](https://dash.plot.ly/dash-core-components) contains code for the main dashboard widgets and interactice features, including dropdowns, sliders, range sliders, text areas, check boxes and others.

[HTML components](https://dash.plot.ly/dash-html-components) contains objects for standard html, such as div tags (html.Div), headlines (html.H1) and so on. You can also use dcc.Markdown to add content in markdown.  

## The app 
Dash uses Flask, so much of the syntax for [Flask](http://flask.pocoo.org/) can be used here.  The simplest app you'll want is:    
`app = dash.Dash(__name__, external_stylesheets=external_stylesheets)`  

If you're deploying your app on a server, you'll want to add server:
`server = app.server`  
you can then have this at the end of the script:
```python
if __name__ == '__main__':
    app.run_server(debug=True, host='your_IP_or_domain', port=80)
```    
For deployment, you'll want to use uWsgi.  
```
## Layout 
The documentation [layout section](https://dash.plot.ly/getting-started) 
