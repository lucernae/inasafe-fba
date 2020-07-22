__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '09/06/20'

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

default_app_config = 'fba.apps.Config'
