from .fields import CaptchaField


def captchaform(field_name):
    """Decorator to add a simple captcha to a form

    To use this decorator, you must specify the captcha field's name as an
    argument to the decorator. For example:

    @captchaform('captcha')
    class MyForm(Form):
        pass

    This would add a new form field named 'captcha' to the Django form MyForm.
    Nothing else is needed; the captcha field and widget expect to be left fully
    to their own devices, and tinkering with them may produce the unexpected.

    It is also possible using this decorator to add multiple captchas to your
    forms:

    @captchaform('captchatwo')
    @captchaform('captchaone')
    class MyForm(Form):
        pass

    Note that the captchas are added to your fields in the inverse order that
    the decorators appear in your source; in this example, 'captchaone' appears
    first in the form, followed by 'captchatwo'.
    """
    def wrapper(orig_form):
        """The actual function that wraps and modifies the form"""

        # Get the original init method so we can call it later
        orig_init = orig_form.__init__

        def new_init(self, *args, **kwargs):
            """This is the captchaform replacement init method

            This method replaces a decorated form with one that properly handles
            ensuring that the captcha is always updated when the form is
            instantiated.
            """
            # Call the original init method so we have a proper form
            orig_init(self, *args, **kwargs)

            # Ensure a fresh captcha on each generation of the form
            self.fields[field_name].widget.generate_captcha()

        # Create a new captcha field to be used in our form
        captcha = CaptchaField()

        # Replace the form's init method with our own
        orig_form.__init__ = new_init

        # Add the captcha field to the form's base and declared fields
        orig_form.base_fields.update({field_name: captcha})
        orig_form.declared_fields.update({field_name: captcha})

        return orig_form

    return wrapper

