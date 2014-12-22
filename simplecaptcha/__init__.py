from .decorators import captchaform
from . import settings

# A simple shortcut/"default" field name for the captcha
captcha = captchaform(settings.DEFAULT_FIELD_NAME)
