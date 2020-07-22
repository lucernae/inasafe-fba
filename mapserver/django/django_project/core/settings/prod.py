# coding=utf-8

"""Project level settings."""
from .project import *  # noqa

ALLOWED_HOSTS = ['*']

# Comment if you are not running behind proxy
USE_X_FORWARDED_HOST = True

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False