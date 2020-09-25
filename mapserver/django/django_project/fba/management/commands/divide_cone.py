import requests
import random
import hashlib
import psycopg2 as driv

from postgis.psycopg import register

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from django.db.models import Q
from fba.models.hazard_event import HazardEvent
from fba.models.hazard_event_queue import HazardEventQueue
from fba.models.all import District


class Command(BaseCommand):
    """ Command to process first hazard event queue. """
    base_url = 'https://geocris2.cdema.org/'
    limit = 10

    def handle(self, *args, **options):
        valid_time = '1600052400000'
        cone_url = 'https://geocris2.cdema.org/noaa/collections/noaa.coneforecastal202020/items.html?validtime=1600052400000'
        points_url = 'https://geocris2.cdema.org/noaa/collections/noaa.centerpositionforecastal202020/items.html?validtime=1600052400000'
        tracks_url = 'https://geocris2.cdema.org/noaa/collections/noaa.tracklineforecastal202020/items.html?validtime=1600052400000'
