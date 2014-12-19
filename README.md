django-simplecaptcha
====================

A textual captcha for Django using simple decorator syntax.

Installation
------------

*TODO: Decide how this will be distributed, which will inform how it's installed*

Using the Captcha
-----------------

Using simplecaptcha is simple:

```python
from simplecaptcha.decorators import CaptchaForm

@CaptchaForm('captcha')
class MyForm(Form):
    pass
```

This will add a field named "captcha" to MyForm. However, nothing else need be
done: the decorator takes care of adding the field and ensuring it is always
updated when a new form instance is created, as well as validating bound forms
and providing useful error messages for users.

Note that the captcha fields are always added to the end of your form. If this
is undesirable for any reason, you can either manually render the form fields in
your templates, or else decorate a stub form and then subclass it with another
form that adds the fields you want to come after.

Advanced Use
------------

It is possible to add multiple captcha fields to your form simply by decorating
your form multiple times. However note that field order in your form will be the
*reverse* of the order that you write your decorators, i.e. if your first
decorator adds the field "captchaone" and the second adds "captchatwo", in your
form "captchatwo" will be first, followed by "captchaone".
