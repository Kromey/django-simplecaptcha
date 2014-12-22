from django.conf import settings


def getsetting(setting, default):
    """Get `setting` if set, fallback to `default` if not

    This method tries to return the value of the specified setting from Django's
    settings module. If this fails for any reason, the value supplied in
    `default` will be returned instead.
    """
    try:
        return getattr(settings, setting)
    except:
        return default


"""SIMPLECAPTCHA_DURATION defines how long, in seconds, a captcha is valid for

This setting can either be supplied in your Django project's settings.py file,
or left out; in the latter case, the default of 5 minutes will be used.
"""
SIMPLECAPTCHA_DURATION = getsetting('SIMPLECAPTCHA_DURATION', 5 * 60)


"""SIMPLECAPTCHA_ITERATIONS defines how many hashing iterations are performed

This can be set in Django's settings module; if left unset, it will default
to using 1024 iterations.
"""
SIMPLECAPTCHA_ITERATIONS = getsetting('SIMPLECAPTCHA_ITERATIONS', 1024)

