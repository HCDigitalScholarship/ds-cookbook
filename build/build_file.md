# Sustainable stack 

Building on the principles of [minimal computing](https://go-dh.github.io/mincomp/about/), we seek to reduce the environmental impact of our work, by creating projects that do not require an active server or database. A minimal approach makes our work accessible to students using mobile devices with limited processing power and with low internet connectivity.  By developing and publishing educational content in minimal form, we are also better able to maintain and preserve our projects. Static websites and microservices require very little maintenance. A "sustainable stack" can allow our projects to begin as a very simple HTML page and to add page templates, data models, and user authentication and other features as needed.  All projects rely on Bootstrap for responsive pages.  Templates use Jinja2, which is modeled on the Django template language, but adds extensions and better performance.  FastAPI projects can use the Tortoise ORM that is based on the Django ORM.  Jinja and Tortoise allow us to move up the pyramid from simple to complex projects without having to completely re-factor and re-build from scratch.     

At all levels of the stack, we are able to produce a distilled version of the project for publication that is consistent with minimal computing principles and the values of the College.     

![](https://haverfordds.netlify.app/stack.jpg)
