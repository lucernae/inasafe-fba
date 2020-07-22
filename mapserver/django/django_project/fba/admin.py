__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '11/06/20'

from django.contrib.gis import admin
from fba.models.hazard_event import HazardEvent
from fba.models.hazard_event_queue import HazardEventQueue

admin.site.register(HazardEventQueue, admin.ModelAdmin)
admin.site.register(HazardEvent, admin.ModelAdmin)
