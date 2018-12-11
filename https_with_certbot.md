## HTTP VS HTTPS  

Hyper Text Transfer Protocol Secure (HTTPS) is the secure version of HTTP, the protocol over which data is sent between your browser and the website that you are connected to. The 'S' at the end of HTTPS stands for 'Secure'. It means all communications between your browser and the website are encrypted. HTTPS is often used to protect highly confidential online transactions like online banking and online shopping order forms.
Web browsers such as Internet Explorer, Firefox and Chrome also display a padlock icon in the address bar to visually indicate that a HTTPS connection is in effect.
[source](https://www.instantssl.com/ssl-certificate-products/https.html)

Certbot is an easy-to-use automatic client that fetches and deploys SSL/TLS certificates for your web server. Certbot was developed by EFF and others as a client for Let’s Encrypt and was previously known as “the official Let’s Encrypt client” or “the Let’s Encrypt Python client.” Certbot will also work with any other CAs that support the ACME protocol.
[source](https://certbot.eff.org/about/)

## Certbot on Ubuntu and nginx 
Install
On Ubuntu systems, the Certbot team maintains a PPA. You can add it to your list of repositories and install Certbot by running the following commands.
```
$ sudo apt-get update
$ sudo apt-get install software-properties-common
$ sudo add-apt-repository universe
$ sudo add-apt-repository ppa:certbot/certbot
$ sudo apt-get update
$ sudo apt-get install python-certbot-nginx 
```
Get Started
Certbot has an Nginx plugin, which is supported on many platforms, and automates certificate installation.

`$ sudo certbot --nginx`

You will then need to enter an email address.  You're welcome to use Mike or Andy's Haverford email addresses. 
```
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator nginx, Installer nginx
Enter email address (used for urgent renewal and security notices) (Enter 'c' to
cancel): ajanco@haverford.edu
```
Accept the terms of service 
```
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Please read the Terms of Service at
https://letsencrypt.org/documents/LE-SA-v1.2-November-15-2017.pdf. You must
agree in order to register with the ACME server at
https://acme-v02.api.letsencrypt.org/directory
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(A)gree/(C)ancel: a
```
We are already signed up for the mailing list and highly recommend that you support this important work however you choose to do so. 
```
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Would you be willing to share your email address with the Electronic Frontier
Foundation, a founding partner of the Let's Encrypt project and the non-profit
organization that develops Certbot? We'd like to send you email about our work
encrypting the web, EFF news, campaigns, and ways to support digital freedom.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(Y)es/(N)o: n
```
Next you need to select which domain you could like to certify.  Note that you need to add the name of the domain in your nginx configuration.
This file can usually be found in `/etc/nginx/sites-available/`. For example: 
```
server {
  server_name bridge.haverford.edu; 
  
  location / {
  } ...
}
```
```
Which names would you like to activate HTTPS for?
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
1: bridge.haverford.edu
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Select the appropriate numbers separated by commas and/or spaces, or leave input
blank to select all options shown (Enter 'c' to cancel): 1
```
If all goes well, you'll see something like the following: 
```Obtaining a new certificate
Performing the following challenges:
http-01 challenge for bridge.haverford.edu
Waiting for verification...
Cleaning up challenges
Deploying Certificate to VirtualHost /etc/nginx/sites-enabled/bridge3
```
Next you'll need to redirect all HTTP traffic to HTTPS.
```
Please choose whether or not to redirect HTTP traffic to HTTPS, removing HTTP access.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
1: No redirect - Make no further changes to the webserver configuration.
2: Redirect - Make all requests redirect to secure HTTPS access. Choose this for
new sites, or if you're confident your site works on HTTPS. You can undo this
change by editing your web server's configuration.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Select the appropriate number [1-2] then [enter] (press 'c' to cancel): 2
Redirecting all traffic on port 80 to ssl in /etc/nginx/sites-enabled/bridge3
```

```
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Congratulations! You have successfully enabled https://bridge.haverford.edu

You should test your configuration at:
https://www.ssllabs.com/ssltest/analyze.html?d=bridge.haverford.edu
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
```




