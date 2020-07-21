__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '11/06/20'

from django.core.management.base import BaseCommand
from django.db.models import Q
from fba.models.hazard_event import HazardEvent
from fba.models.hazard_event_queue import HazardEventQueue


class Command(BaseCommand):
    """ Command to process first hazard event queue. """

    def handle(self, *args, **options):
        HazardEventQueue.objects.all().update(queue_status=0)
