from .fields import CaptchaField


def CaptchaForm(field_name):
    def wrapper(orig_form):
        orig_init = orig_form.__init__

        def new_init(self, *args, **kwargs):
            orig_init(self, *args, **kwargs)

            #Ensure a fresh captcha on each generation of the form
            self.fields[field_name].widget.generate_captcha()

        captcha = CaptchaField()

        orig_form.__init__ = new_init
        orig_form.base_fields.update({field_name: captcha})
        orig_form.declared_fields.update({field_name: captcha})

        return orig_form

    return wrapper

