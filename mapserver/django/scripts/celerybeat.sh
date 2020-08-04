# Absolute or relative path to the 'celery' command:
CELERY_BIN="/usr/local/bin/celery"
#CELERY_BIN="/virtualenvs/def/bin/celery"

# App instance to use
# comment out this line if you don't use an app
CELERY_APP="fba.tasks:app"
# or fully qualified:
#CELERY_APP="proj.tasks:app"

# Where to chdir at start.
CELERYBEAT_CHDIR="/opt/inasafe-fba/mapserver/django/django_project"

# Extra arguments to celerybeat
CELERYBEAT_OPTS="--schedule=/var/run/celery/celerybeat-schedule"
