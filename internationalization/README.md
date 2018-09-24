# How to add translations to a django site 
*note you need to have tagged all items you wanted translated with the tag {% trans "whatever you wanted translated" %}*
1. First enter the server using your `username@ipaddress` ex: ssh jdoe@149.23.1003.12000
1. Make sure you are in the sudo group 
1. Use `sudo su` to switch to root
1. Next do cd into /usr/local/lib/python-virtualenv/gam_env
1. Activate the virtual env using source bin/activate
1. `cd` into `/srv/GAM`
1. Do python manage.py makemessages -l "language code"
1. `cd` into `/srv/GAM/gam_app/locale/"language code"/LC_MESSAGES`
1. `nano django.po` and translate each strin into desired language 
1. `manage.py compile messages`
