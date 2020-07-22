__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '11/06/20'

import logging
import json
import os
from django.conf import settings
from datetime import datetime
from django.core.management.base import BaseCommand
from fba.models.hazard_event import HazardEvent
from fba.models.hazard_event_queue import HazardEventQueue

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """ Command to process first hazard event queue. """

    def handle(self, *args, **options):
        queue = HazardEventQueue.objects.order_by('id').first()

        logger.info('found {}'.format(queue))
        if queue and queue.queue_status != 1:
            start_time = datetime.now()
            # run the script
            queue.queue_status = 1
            queue.save()

            logger.info('run {}'.format(queue.id))
            HazardEvent.objects.get_or_create(
                flood_map_id=queue.flood_map_id,
                acquisition_date=queue.acquisition_date,
                forecast_date=queue.forecast_date,
                source=queue.source,
                notes=queue.notes,
                link=queue.link,
                trigger_status=queue.trigger_status,
                progress=queue.progress,
                hazard_type_id=queue.hazard_type_id
            )
            logger.info('done {}'.format(queue.id))

            # save report
            if not os.path.exists(settings.ANALYSIS_REPORT_FOLDER):
                os.makedirs(settings.ANALYSIS_REPORT_FOLDER)

            _filename = os.path.join(settings.ANALYSIS_REPORT_FOLDER, 'queue-{}'.format(queue.id))

            queue.delete()
            try:
                try:
                    os.remove(_filename)
                except IOError:
                    pass

                finish_time = datetime.now()
                content = {
                    'flood_map_id': queue.flood_map_id,
                    'acquisition_date': str(queue.acquisition_date),
                    'start': str(start_time),
                    'finish': str(finish_time),
                    'duration': str(finish_time - start_time)
                }
                _file = open(_filename, "w+")
                _file.write(json.dumps(content, indent=4))
                _file.close()
            except Exception:
                pass
        else:
            logger.info('skip')
