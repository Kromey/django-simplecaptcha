from django.conf import settings


SETTING_PREFIX = 'SIMPLECAPTCHA_'

def getsetting(setting, default):
    """Get `setting` if set, fallback to `default` if not

    This method tries to return the value of the specified setting from Django's
    settings module. If this fails for any reason, the value supplied in
    `default` will be returned instead.

    This method adds the SETTING_PREFIX to the supplied setting name, which
    helps to namespace the settings in the Django settings module but is
    downright silly to use over and over (and over...) within this package.
    """

    setting = SETTING_PREFIX + setting

    try:
        return getattr(settings, setting)
    except:
        return default


"""DURATION defines how long, in seconds, a captcha is valid for

This setting can either be supplied in your Django project's settings.py file,
or left out; in the latter case, the default of 5 minutes will be used.
"""
DURATION = getsetting('DURATION', default=5 * 60)


"""ITERATIONS defines how many hashing iterations are performed

This can be set in Django's settings module; if left unset, it will default
to using 1024 iterations.
"""
ITERATIONS = getsetting('ITERATIONS', default=1024)

