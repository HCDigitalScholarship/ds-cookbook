First enter the server using your username@ipaddress ex: ssh jdoe@149.23.1003.12000
make sure you are in the sudo group 
and then use "sudo su" to switch to root
Next do cd into /usr/local/lib/python-virtualenv/gam_env
activate the virtual env using source bin/activate
cd out 
cd into /srv/GAM
then do python manage.py makemessages -l "language code"
cd into /srv/GAM/gam_app/locale/"language code"/LC_MESSAGES#
nano django.po and translate each strin into desired language 
manage.py compile messages
