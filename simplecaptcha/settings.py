import sys


from django.conf import settings


"""A reference to the current module, used in `_setsettings()`"""
_self = sys.modules[__name__]

"""A prefix for namespacing simplecaptcha settings in Django's settings module"""
_DJANGO_SETTING_PREFIX = 'SIMPLECAPTCHA_'

def _getsetting(setting, default):
    """Get `setting` if set, fallback to `default` if not

    This method tries to return the value of the specified setting from Django's
    settings module, after prefixing the name with _DJANGO_SETTING_PREFIX. If
    this fails for any reason, the value supplied in `default` will be returned
    instead.
    """

    setting = _DJANGO_SETTING_PREFIX + setting

    try:
        return getattr(settings, setting)
    except:
        return default

def _setsetting(setting, default):
    """Dynamically sets the variable named in `setting`

    This method uses `_getsetting()` to either fetch the setting from Django's
    settings module, or else fallback to the default value; it then sets a
    variable in this module with the returned value.
    """
    value = _getsetting(setting, default)
    setattr(_self, setting, value)


"""DURATION defines how long, in seconds, a captcha is valid for

Default: 300 seconds (5 minutes)
"""
_setsetting('DURATION', default=5 * 60)


"""ITERATIONS defines how many hashing iterations are performed

Default: 1024
"""
_setsetting('ITERATIONS', default=1024)

"""DEFAULT_FIELD_NAME is used as the field in the shortcut @captcha decorator

Default: 'captcha'
"""
_setsetting('DEFAULT_FIELD_NAME', default='captcha')

