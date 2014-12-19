import time


from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings


from .widgets import CaptchaWidget


"""CAPTCHA_DURATION defines how long, in seconds, a captcha is valid for

This setting can either be supplied in your Django project's settings.py file,
or left out; in the latter case, the default of 5 minutes will be used.
"""
try:
    CAPTCHA_DURATION = settings.CAPTCHA_DURATION
except:
    # Valid for 5 minutes by default
    CAPTCHA_DURATION = 60 * 5


class CaptchaField(forms.MultiValueField):
    """A field that contains and validates a simple catcha question

    WARNING: If you use this field directly in your own forms, you may be
    caught by surprise by the fact that Django forms rely upon class object
    rather than instance objects for its fields. This means that your captcha
    will not be updated when you instantiate a new form, and you'll end up
    asking your users the same question over and over -- largely defeating the
    purpose of a captcha! To solve this, either use the @decorator instead, or
    be sure to call upon the widget to update its captcha question.
    """
    widget = CaptchaWidget

    def __init__(self, *args, **kwargs):
        """Sets up the MultiValueField"""
        fields = (
                forms.CharField(),
                forms.CharField(),
                forms.CharField(),
                )
        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        """Validates the captcha answer and returns the result

        If no data is provided, this method will simply return None. Otherwise,
        it will validate that the provided answer and timestamp hash to the
        supplied hash value, and that the timestamp is within the configured
        time that captchas are considered valid.
        """
        if data_list:
            # Calculate the hash of the supplied values
            hashed = self.widget.hash_answer(answer=data_list[0], timestamp=data_list[1])
            # Current time
            timestamp = time.time()

            if float(data_list[1]) < timestamp - CAPTCHA_DURATION:
                raise ValidationError("Captcha expired, please try again", code='invalid')
            elif hashed != data_list[2]:
                raise ValidationError("Incorrect answer", code='invalid')

            # Return the supplied answer
            return data_list[0]
        else:
            return None

    @property
    def label(self):
        """The captcha field's label is the captcha question itself"""
        return self.widget._question

    @label.setter
    def label(self, value):
        """The question is generated by the widget and cannot be externally set"""
        pass

