============
django-voice
============

django-voice is a very simple application to enable user feedback that is integrated with your Django project. Originally built for Verb (http://verbapp.com).

IMPORTANT: Upgrading to 0.4 from older versions
===============================================
If you upgrade django-voice to 0.4 from older versions, you will take an error about database changing::

    DatabaseError at /feedback/

    no such column: djangovoice_feedback.email

You have two ways for fixing the problem.

If you use South..
------------------
Run this command::

    python manage.py migrate djangovoice

If you think to use South..
---------------------------
Pass first migration and implement second migration::

    python manage.py migrate --fake djangovoice 0001
    python manage.py migrate djangovoice

If you don't want to use South..
--------------------------------
Open your SQL shell and add email column to djangovoice_feedback::

    python manage.py dbshell

    sqlite> ALTER TABLE "djangovoice_feedback" ADD COLUMN "email" varchar(75) NULL;
    sqlite> ALTER TABLE "djangovoice_feedback" ADD COLUMN "slug" varchar(10) NULL;

That's it..

Installation and Dependencies
=============================

To satisfy dependencies listed in REQUIREMENTS you can simply run this command:

::

  pip -r REQUIREMENTS


'pip' will automatically download and install dependencies required for django-voice. Next step is activating helper applications to run.

* Activate django's comment system. (https://docs.djangoproject.com/en/dev/ref/contrib/comments/)
* Add django-gravatar and django-voting to your INSTALLED_APPS in settings file.
* Add comments and django-voice to your url configration.
* Create at least one Type and Status either through the admin or fixtures.

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

Remember to create and save at least one Type and Status model instance.

That's all you need to run django-voice.

Settings
========

::

  VOICE_ALLOW_ANONYMOUS_USER_SUBMIT (default: False)
    Allow unsigned user to submit feedback. Asks user e-mail and marks
    the feedback as private to prevent public spam.

AUTHORS
=======
DjangoVoice was originally created by Huw Wilkins (http://huwshimi.com/)

Contributors:

 * Ross Poulton http://rossp.org/
 * Gökmen Görgen http://gokmengorgen.net/
 * Mirat Can Bayrak http://miratcanbayrak.blogspot.com/
 * Simon Ye https://github.com/yesimon
