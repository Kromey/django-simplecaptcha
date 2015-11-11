django-simplecaptcha
====================

A textual captcha for Django using simple decorator syntax.

So What Does it DO?
-------------------

simplecaptcha provides an easy decorator syntax to add a textual captcha
to your Django forms. The captcha is a simple arithmetic question:
Either add, subtract, or multiply two numbers between 1 and 10. No
server-side context is needed, as the captcha uses cryptographic
signatures to securely pass the context to the client, and then validate
the supplied answer on the back end.

In order to mitigate replay attacks, the signatures expire after a
configurable amount of time (default 5 minutes): enough time to fill out
and submit the form, but short enough to reduce the ability to reuse
signatures with known answers.

Why Make Another One?
---------------------

There's lots of Django captchas out there, including more than one that
uses arithmetic questions just like this one. So why do we need another?

Simply put, the others all lack in flexibility. When I set out to find
one for my form, I needed one that would allow me to manually render my
fields; the first few I found, however, hardcoded the question (as a
label) into the ``format_output()`` method, or even directly in the
``render()`` method itself. This meant I couldn't separately render the
label where I need it for my design. I kept digging, and found another
that offered the flexibility I needed in the layout, but put the captcha
generation logic in the field's ``__init__()`` method. While this sounds
great, Django's method of using class objects -- rather than instance
objects -- means that you get only a single captcha question per server
thread, period.

So I sat down to write a captcha that would give me the flexibility I
needed to fit into my front-end design, but that also would reliably
generate a fresh captcha question each time the page was loaded.

This is that captcha.

Installation
------------

From PyPi
~~~~~~~~~

(Recommended)
Install from PyPi with a simple ``pip install django-simplecaptcha``.

From Source
~~~~~~~~~~~

Download the source from GitHub, and simply make the ``simplecaptcha``
module available to Python in some way; on *nix systems, a simple symlink
in the root of your Django project to the ``simplecaptcha`` directory is
probably the most straightforward solution.

Using the Captcha
-----------------

Using simplecaptcha is simple:

.. code:: python

    from simplecaptcha import captcha

    @captcha
    class MyForm(Form):
        pass

This will add a field named "captcha" to MyForm. However, nothing else
need be done: the decorator takes care of adding the field and ensuring
it is always updated when a new form instance is created, as well as
validating bound forms and providing useful error messages for users.

Advanced Use
~~~~~~~~~~~~

Configuring simplecaptcha
^^^^^^^^^^^^^^^^^^^^^^^^^

simplecaptcha, as its name implies, is simple. It works straight out of
the box without any need to add any configuration in your Django
project. However, if you do want to modify its behavior, you can do that
as well, by simply adding any of these settings to your Django project's
settings module:

-  ``SIMPLECAPTCHA_DURATION``: Defines how long (in seconds) a captcha
   is considered valid for; default: 300 seconds (5 minutes)
-  ``SIMPLECAPTCHA_ITERATIONS``: The cryptographic signature passed to
   the client and used to validate the captcha is hashed multiple times
   for security. You can change the number of iterations used with this
   setting; default: 1024
-  ``SIMPLECAPTCHA_DEFAULT_FIELD_NAME``: The default field name used in
   the ``captcha`` decorator; default: 'captcha'

Controlling Field Order
^^^^^^^^^^^^^^^^^^^^^^^

The decorator will always add the captcha field to the end of your form.
If this is undesirable for any reason, you can of course always manually
render your form fields as `decribed in the Django
docs <https://docs.djangoproject.com/en/1.7/topics/forms/#rendering-fields-manually>`__.

Another option is to simply add a "dummy" field to your form with the
same name as that used by the decorator. The decorator would then
effectively replace the field in your form:

.. code:: python

    from simplecaptcha import captcha
    from simplecaptcha.fields import CaptchaField

    @captcha
    class MyForm(Form):
        field1 = CharField()
        field2 = CharField()
        captcha = CaptchaField()
        field3 = CharField()

(NOTE: Since the decorator will *replace* the field of the same name, it
does not matter what type of field you specify when using this approach.
Because of the way Django processes Form classes, however, you *must*
specify a Django field, or else Django will ignore it and you won't get
the desired effect.)

Now when you render MyForm in your template, fields will be ordered
precisely as they are in your source: field1, then field2, followed by
captcha, and finally field3.

Specifying the Field Name
^^^^^^^^^^^^^^^^^^^^^^^^^

If for any reason you don't want your captcha field to be named
"captcha", and you don't want to set
``SIMPLECAPTCHA_DEFAULT_FIELD_NAME`` in your Django settings module, you
can use the ``@captchaform`` decorator and supply the desired field name
as an argument, like so:

.. code:: python

    from simplecaptcha import captchaform

    @captchaform('securitycheck')
    class MyForm(Form):
        pass

This will add a field named "securitycheck" to MyForm that will contain
the form's captcha.

If you wish to do this and use the method in the previous section to
specify the field order, note that the "dummy" field you add must match
the name you passed into the decorator.

Multiple Captcha Fields
^^^^^^^^^^^^^^^^^^^^^^^

It is possible to add multiple captcha fields to your form simply by
decorating your form multiple times. However note that field order in
your form will be the *reverse* of the order that you write your
decorators:

.. code:: python

    from simplecaptcha import captchaform

    @captchaform('captcha')
    @captchaform('captcha2')
    class MyForm(Form):
        pass

In this example, when MyForm is rendered in your template, "captcha2"
will appear *first*, and then "captcha". This is a consequence of how
decorators in Python are processed; you simply have to remember that the
last captcha decorated into your form is the first one that will appear
in your templates.
