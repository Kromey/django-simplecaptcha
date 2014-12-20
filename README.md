# django-simplecaptcha

A textual captcha for Django using simple decorator syntax.

## Installation

*TODO: Decide how this will be distributed, which will inform how it's installed*

## Using the Captcha

Using simplecaptcha is simple:

```python
from simplecaptcha import captcha

@captcha
class MyForm(Form):
    pass
```

This will add a field named "captcha" to MyForm. However, nothing else need be
done: the decorator takes care of adding the field and ensuring it is always
updated when a new form instance is created, as well as validating bound forms
and providing useful error messages for users.

### Advanced Use

#### Controlling Field Order

The decorator will always add the captcha field to the end of your form. If this
is undesirable for any reason, you can of course always manually render your form
fields as [decribed in the Django docs](https://docs.djangoproject.com/en/1.7/topics/forms/#rendering-fields-manually).

Another option is to simply add a "dummy" field to your form with the same name
as that passed into the decorator. The decorator would then effectively replace
the field in your form:

```python
from simplecaptcha import captcha
from simplecaptcha.fields import CaptchaField

@captcha
class MyForm(Form):
    field1 = CharField()
    field2 = CharField()
    captcha = CaptchaField()
    field3 = CharField()
```

(NOTE: Since the decorator will *replace* the field of the same name, it does not
matter what type of field you specify when using this approach. Because of the way
Django processes Form classes, however, you *must* specify a Django field, or else
Django will ignore it and you won't get the desired effect.)

Now when you render MyForm in your template, fields will be ordered precisely as
they are in your source: field1, then field2, followed by captcha, and finally
field3.

#### Specifying the Field Name

If for any reason you don't want your captcha field to be named "captcha", you
can use the @captchaform decorator and supply the desired field name as an
argument, like so:

```python
from simplecaptcha import captchaform

@captchaform('securitycheck')
class MyForm(Form):
    pass
```

This will add a field named "securitycheck" to MyForm that will contain the
form's captcha.

If you wish to do this and use the method in the previous section to specify the
field order, note that the "dummy" field you add must match the name you passed
into the decorator.

#### Multiple Captcha Fields

It is possible to add multiple captcha fields to your form simply by decorating
your form multiple times. However note that field order in your form will be the
*reverse* of the order that you write your decorators:

```python
from simplecaptcha import captchaform

@captchaform('captcha')
@captchaform('captcha2')
class MyForm(Form):
    pass
```

In this example, when MyForm is rendered in your template, "captcha2" will appear
*first*, and then "captcha". This is a consequence of how decorators in Python are
processed; you simply have to remember that the last captcha decorated into your
form is the first one that will appear in your templates.

