The codebook for setting up an email verification for django projects:
Note: we are using postfix app for setting up the email server.
Setting up Django registration for email verification:
Read django registration documentation carefully <https://django-registration.readthedocs.io/en/2.4.1/hmac.html#hmac-workflow>. Also read the django registration quick start guide <https://django-registration.readthedocs.io/en/2.4.1/quickstart.html>. We are using the HMAC activation flow. Also read a blog about how to set the setting.py of the django project and how to test it <http://cheng.logdown.com/posts/2015/06/08/django-send-email-using-postfix>
In the requirement.txt, include the installation of django-registration package or pip install django-registration in the virtual env.
i.e. “django-registration==2.3”
Update the required setting in the setting.py and add the required templates for registration according to the django registration HMAC activation workflow documentation 
In setting.py include the following
from django.conf.urls import include, url

urlpatterns = [
    # Other URL patterns ...
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    # More URL patterns ...
]
….
ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window; you may, of course, use a different value.

Have the required templates for registration added under the directory /templates/registration
registration/registration_form.html
registration/registration_complete.html
registration/activate.html
registration/activation_complete.html
registration/activation_email_subject.txt
registration/activation_email.txt
You can consult this github repo that gives an example about how to write those templates: <https://github.com/macdhuibh/django-registration-templates/tree/master/registration> This github repo offers very good examples.

Setting up Postfix email server:
Install postfix in the development droplet
Read the article “Configure Postfix to Send Mail Using Gmail and Google Apps on Debian or Ubuntu” <https://linode.com/docs/email/postfix/configure-postfix-to-send-mail-using-gmail-and-google-apps-on-debian-or-ubuntu/>
sudo apt-get install postfix
Follow the direction of the postfix installation in the above article.
Test the postfix email server with the following order:
telnet localhost 25
Once connected, enter the following:
     		mail from: whatever@whatever.com
		     rcpt to: your_real_email_addr@blah.com
		     	  data (press enter)
			       type whatever content you feel like to type
			       	    . (put an extra period on the last line and then press enter again)
If everything works out, you will see something like the following:
250 2.0.0 Ok: queued as CC732427AE
Then you check your test recipient email’s spam box to see if you have successfully installed the postfix
If you have received the test email, that means the postfix is installed successfully. Note that for right now the email that is sent through postfix email server will always end up in the recipient’s spam box. In fact, if the recipient email is haverford email, you won’t even receive the test email. We will try to resolve that later.
You can proceed to configure the django project

Configuring Django project to send email via postfix
Add the following codes to the django project’s settings.py:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 25
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_USE_TLS = False
    DEFAULT_FROM_EMAIL = 'Server <server@whatever.com>'
Test if you have successfully configured the django project with the following way:
     ./manage.py shell #open up a django shell
     >>> from django.core.mail import send_mail
     >>> send_mail('Subject here', 'Here is the message.', 'from@example.com',['to@example.com'], fail_silently=False)
Check your email’s spam box to see if you have received the test email. If you have received it, Congratulation! You have successfully set up an email verification for the django project!

I will do more research on how not to let the email verification end up in the user’s spam box...

Some additional features to look up:
Admin approval,
The privilege of the created user need to be considered and approved by admin.
