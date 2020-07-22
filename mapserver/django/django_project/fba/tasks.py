import logging
from fba.celery import app
from django.core import management

logger = logging.getLogger(__name__)


@app.task(name='fba.process_hazard_event_queue')
def process_hazard_event_queue():
    logger.log(logging.INFO, 'process event queue')
    management.call_command(
        'process_hazard_event_queue'
    )
