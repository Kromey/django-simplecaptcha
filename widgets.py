import random
import time


from django import forms
from django.conf import settings
from django.utils.crypto import salted_hmac
from django.utils.safestring import mark_safe


try:
    CAPTCHA_ITERATIONS = settings.CAPTCHA_ITERATIONS
except:
    CAPTCHA_ITERATIONS = 1024


class CaptchaWidget(forms.widgets.MultiWidget):
    def __init__(self, attrs=None):
        widgets = (
                forms.TextInput(attrs=attrs),
                forms.HiddenInput(),
                forms.HiddenInput()
                )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        return self._values

    def format_output(self, rendered_widgets):
        return ''.join(rendered_widgets)

    def render(self, name, value, attrs=None):
        value = self._values
        return super().render(name, value, attrs)

    def generate_captcha(self):
        self._question, answer = self._generate_question()

        timestamp = time.time()
        hashed = self.hash_answer(answer, timestamp)

        self._values = ['', timestamp, hashed]

    def _generate_question(self):
        x = random.randint(1, 10)
        y = random.randint(1, 10)

        operator = random.choice(('+', '-', '*',))
        if operator == '+':
            answer = x + y
        elif operator == '-':
            if x < y:
                x, y = y, x
            answer = x - y
        else:
            answer = x * y
            operator = '&times;'

        question = '{} {} {}'.format(x, operator, y)
        return mark_safe(question), answer

    def hash_answer(self, answer, timestamp):
        timestamp = str(timestamp)
        answer = str(answer)
        hashed = ''

        for _ in range(CAPTCHA_ITERATIONS):
            hashed = salted_hmac(timestamp, answer).hexdigest()

        return hashed

