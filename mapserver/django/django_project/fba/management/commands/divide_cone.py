import requests
import json

from django.core.management.base import BaseCommand
from fba.scripts.cone_divider import ConeDivider


class Command(BaseCommand):
    """ Command to process first hazard event queue. """
    base_url = 'https://geocris2.cdema.org/'

    def handle(self, *args, **options):
        valid_time = '1600052400000'
        cone_url = 'https://geocris2.cdema.org/noaa/collections/noaa.coneforecastal202020/items.json?validtime=' + valid_time
        points_url = 'https://geocris2.cdema.org/noaa/collections/noaa.centerpositionforecastal202020/items.json?validtime={}&orderBy=ogc_fid'.format(valid_time)

        # Fetch cone
        response = requests.get(cone_url)
        cone_json = response.json()

        # Fetch center points
        response = requests.get(points_url)
        points_json = response.json()

        cone_divider = ConeDivider(
            points=points_json,
            cone_json=cone_json
        )

        geojson_data = cone_divider.get_cones()
        geojson_data_string = json.dumps(geojson_data, indent=4)
        print(geojson_data_string)
