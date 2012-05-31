============
django-voice
============

django-voice is a very simple application to enable user feedback that is integrated with your Django project. Originally built for Verb (http://verbapp.com).

Installation and Dependencies
=============================

To satisfy dependencies listed in REQUIREMENTS you can simply run this command:

::

  pip -r REQUIREMENTS


'pip' will automatically download and install dependencies required for django-voice. Next step is activating helper applications to run.

 * Activate django's comment system. (https://docs.djangoproject.com/en/dev/ref/contrib/comments/)
 * Add django-gravatar and django-voting to your INSTALLED_APPS in settings file.
 * Add comments and django-voice to your url configration.

After these steps, your INSTALLED_APPS in settings.py must be seen like this:

::

  INSTALLED_APPS = (
      ...
      'voting',
      'gravatar',
      'djangovoice'
  )

and urls.py like this:

::

  urlpatterns = patterns(
      ...
      url(r'^comments/', include('django.contrib.comments.urls')),
      url(r'^feedback/', include('djangovoice.urls')))

These are all that you need to do run django-voice.

AUTHORS
=======
DjangoVoice was originally created by Huw Wilkins (http://huwshimi.com/)

Contributors:

 * Ross Poulton http://rossp.org/
 * Gökmen Görgen http://gokmengorgen.net/
 * Mirat Can Bayrak http://miratcanbayrak.blogspot.com/
