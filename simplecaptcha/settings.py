from django.conf import settings


"""SIMPLECAPTCHA_DURATION defines how long, in seconds, a captcha is valid for

This setting can either be supplied in your Django project's settings.py file,
or left out; in the latter case, the default of 5 minutes will be used.
"""
try:
    SIMPLECAPTCHA_DURATION = settings.SIMPLECAPTCHA_DURATION
except:
    # Valid for 5 minutes by default
    SIMPLECAPTCHA_DURATION = 60 * 5


"""SIMPLECAPTCHA_ITERATIONS defines how many hashing iterations are performed

This can be set in Django's settings module; if left unset, it will default
to using 1024 iterations.
"""
try:
    SIMPLECAPTCHA_ITERATIONS = settings.SIMPLECAPTCHA_ITERATIONS
except:
    SIMPLECAPTCHA_ITERATIONS = 1024

