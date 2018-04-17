## Writing an Nginx configuration file

In our [LEMP stack setup tutorial](https://github.com/HCDigitalScholarship/documentation/blob/master/lemp_stack.md) there's a sample Nginx configuration that provides a good starting point for most projects. It looks like this:

```
server {
    listen 80;

    location /static {
        alias /path/to/your/mysite/static;
    }

    location / {
        uwsgi_pass  unix:/run/uwsgi/app/<projectname>/<projectname>.socket;
        include     /srv/<projectname>/uwsgi_params;
    }
}
```

But most projects will eventually need something more complicated. Let's start by breaking down what's actually going on in this file.

`listen 80;` tells Nginx to listen on port 80, the standard port for HTTP requests. If your project is being served over a secure HTTPS connection, you'll need to use port 443 instead.

Why 80 and 443? [Random artifacts of internet history.](https://www.howtogeek.com/233383/why-was-80-chosen-as-the-default-http-port-and-443-as-the-default-https-port/)

Each `location` parameter gives instructions for what to do with URLs matching a particular prefix. Unlike Django urls, which tries patterns in the order they're written, Nginx chooses the longest matching pattern.

`alias` tells Nginx to serve static files out of a given location on the machine. A similar directive is `root`, which differs in that it appends the location to the root when looking for files. For instance, if you're serving files out of the directory `/var/www/app/static`, you could write:

```
location /static/ {
  root /var/www/app/;
}
```

or

```
location /static/ {
  alias /var/www/app/static/;
}
```

`uwsgi_pass` hands a request off to uWSGI to handle, which unlike Nginx knows how to serve Python. The socket is automatically created by uWSGI. `include` tells it where to find the parameters for running uWSGI.

This is a basic set of directives but you might need more. Here's a look at Ticha's Nginx config:

```
server {
  listen 80 default_server;
  server_name ticha.haverford.edu;
  return 301 https://$host$request_uri;
}

server {
  listen 443 ssl;
  server_name ticha.haverford.edu;
  ssl_certificate /etc/ssl/certs/ticha_haverford_edu_chained.cer;
  ssl_certificate_key /etc/ssl/private/ticha_haverford_edu.key;

  root /var/www/html;
  client_max_body_size 25M;
  uwsgi_read_timeout 500;

  #remove .html extensions from URLs to handle requests for old Ticha site
  rewrite ^(/.*)\.html(\?.*)?$ $1$2 permanent;

  --- lots of other locations omitted ---

  location /img {
    try_files $uri /srv/ticha-site/img;
  }

  location /images {
    root /var/www/html/images;
  }

  # Other Django config
  location /static/ {
    alias /var/www/html/static/;
  }

  location / {
    include /srv/ticha-django-site/uwsgi_params;
    uwsgi_pass unix:/run/uwsgi/app/ticha-django/ticha-django.socket;
  }

  # php-fpm config
  # Edit /etc/php5/fpm/php.ini and set cgi.fix_pathinfo = 0

  location ~ \.php$ {
    fastcgi_split_path_info ^(.+\.php)(/.+)$;
    include /etc/nginx/fastcgi_params;
    fastcgi_pass unix:/var/run/php5-fpm.sock;
    fastcgi_intercept_errors on;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
  }
}
```

The first thing you might notice is that Ticha has two `server` codeblocks. These correspond to two types of connections - HTTP (insecure) and HTTPS (encrypted).

The directive `return 301 https://$host$request_uri;` is a redirect, telling Nginx to send the client to the same host (domain name or IP address) and request URI (the path after the domain name) but with HTTPS instead of HTTP. Just like 404 means "not found" and 500 means "server error", 301 is the response code for a redirect.

The `server_name` parameter, which can have any number of domain names or IPs afterward, allows you to use different sets of instructions for different hosts, which can be handy for serving multiple sites off the same server.

The `ssl_certificate` and `ssl_certificate_key` point to the certificates the server uses to ensure secure communication.

`rewrite` can alter the requesting URI.

`try_files` is similar to `alias` but will move on to the next directive if it doesn't find the file requested. You can string together several `try_files` directives to search through multiple locations in order.

The `location ~ \.php$` codeblock matches any URI ending in `.php`, then uses FastCGI to interpret and serve PHP files.
