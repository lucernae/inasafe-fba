from celery.schedules import crontab
import os
import ast

SCHEDULE_HAZARD_EVENT_QUEUE = ast.literal_eval(os.environ.get(
    'SCHEDULE_HAZARD_EVENT_QUEUE', '{}'))
# Default to minutely
SCHEDULE_HAZARD_EVENT_QUEUE = SCHEDULE_HAZARD_EVENT_QUEUE or {
    'minute': '*'
}

CELERYBEAT_SCHEDULE = {
    'hazard_event_queue': {
        'task': 'fba.process_hazard_event_queue',
        'schedule': crontab(**SCHEDULE_HAZARD_EVENT_QUEUE),
    },
}

CELERY_TIMEZONE = 'UTC'

#BROKER_URL = 'memory://localhost'
BROKER_URL = 'amqp://guest:guest@rabbitmq'
CELERY_RESULT_BACKEND = 'rpc://'

