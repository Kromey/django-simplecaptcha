import time


from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings


from .widgets import CaptchaWidget


try:
    CAPTCHA_DURATION = settings.CAPTCHA_DURATION
except:
    # Valid for 5 minutes by default
    CAPTCHA_DURATION = 60 * 5


class CaptchaField(forms.MultiValueField):
    widget = CaptchaWidget

    def __init__(self, *args, **kwargs):
        fields = (
                forms.CharField(),
                forms.CharField(),
                forms.CharField(),
                )
        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            hashed = self.widget.hash_answer(answer=data_list[0], timestamp=data_list[1])
            timestamp = time.time()

            if float(data_list[1]) < timestamp - CAPTCHA_DURATION:
                raise ValidationError("Captcha expired, please try again", code='invalid')
            elif hashed != data_list[2]:
                raise ValidationError("Incorrect answer", code='invalid')

            return data_list[0]
        else:
            return None

    @property
    def label(self):
        return self.widget._question

    @label.setter
    def label(self, value):
        pass

