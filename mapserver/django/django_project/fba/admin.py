__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '11/06/20'

from django.contrib.gis import admin
from fba.models.all import *


class ConfigAdmin(admin.ModelAdmin):
    list_display = (
        'key', 'value'
    )


class WorldPopDistrictStatsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in WorldPopDistrictStats._meta.get_fields()]


class WorldPopSubDistrictStatsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in WorldPopSubDistrictStats._meta.get_fields()]


class WorldPopVillageStatsAdmin(admin.ModelAdmin):
    list_display = [f.name for f in WorldPopVillageStats._meta.get_fields()]


admin.site.register(BuildingTypeClass)
admin.site.register(HazardEventQueue, admin.ModelAdmin)
admin.site.register(HazardEvent, admin.ModelAdmin)
admin.site.register(Census)
admin.site.register(Config, ConfigAdmin)
admin.site.register(Country)
admin.site.register(HazardClass)
admin.site.register(HazardType)
admin.site.register(WorldPop)
admin.site.register(WorldPopDistrictStats, WorldPopDistrictStatsAdmin)
admin.site.register(WorldPopSubDistrictStats, WorldPopSubDistrictStatsAdmin)
admin.site.register(WorldPopVillageStats, WorldPopVillageStatsAdmin)
admin.site.register(HazardMap)
