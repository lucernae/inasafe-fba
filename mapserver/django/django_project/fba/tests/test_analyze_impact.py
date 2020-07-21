__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '15/06/20'

import datetime
import json
import os
import requests
import time
from django.conf import settings
from django.test import TestCase
from django.utils.dateparse import parse_datetime


class TestAnalyzeImpact(TestCase):

    def setUp(self):
        self.forecast_date_range_start = "1990-01-01T17:00:00.000Z"
        self.forecast_date_range_end = "1990-01-30T17:00:00.000Z"
        # we check if our queue is empty
        url = os.path.join(
            settings.POSTGREST_BASE_URL,
            'hazard_event_queue')
        is_empty = False
        while not is_empty:
            response = requests.get(url)
            is_empty = len(response.json()) == 0
            if not is_empty:
                time.sleep(10)

    def test_peformance(self):
        """ Test impact calculation peformance
        and also return time of progress
        """
        timedeltas = []
        for file in os.listdir(settings.ANALYSIS_REPORT_FOLDER):
            _file = open(os.path.join(settings.ANALYSIS_REPORT_FOLDER, file), "r")
            report = json.loads(_file.read())
            timedeltas.append(
                parse_datetime(report['finish']) - parse_datetime(report['start']))
            _file.close()

        # number of queue
        print('NUMBER OF QUEUE = {}'.format(len(timedeltas)))

        # get average time
        average_timedelta = sum(timedeltas, datetime.timedelta(0)) / len(timedeltas)
        print('AVERAGE = {}'.format(average_timedelta))
        self.assertTrue(average_timedelta < datetime.timedelta(minutes=3))

        # get total process time
        total = timedeltas[0]
        for delta in timedeltas[:1]:
            total += delta
        print('TOTAL = {}'.format(total))
        self.assertTrue(total < datetime.timedelta(minutes=3 * len(timedeltas)))

    def test_event_historical(self):
        """ Test for return list of historical event
        """
        url = os.path.join(
            settings.POSTGREST_BASE_URL,
            'rpc/flood_event_historical_forecast_list_f')
        events = requests.post(url, data={
            'forecast_date_range_start': self.forecast_date_range_start,
            'forecast_date_range_end': self.forecast_date_range_end
        }).json()
        self.assertTrue(len(events) != 0)

    def test_hazard_event(self):
        """ Test of hazard event in date of tests
        """

        url = os.path.join(
            settings.POSTGREST_BASE_URL,
            'hazard_event?and=(forecast_date.gte.{},forecast_date.lt.{})'
            '&order=acquisition_date.desc'.format(
                self.forecast_date_range_start, self.forecast_date_range_end
            ))
        events = requests.get(url).json()

        # district summary fixture
        district_summary_fixture = os.path.join(
            settings.FIXTURES, 'test', 'district_summary.json')
        with open(district_summary_fixture, 'r') as _file:
            district_summary_fixture = json.load(_file)

        # road district summary fixture
        road_district_summary_fixture = os.path.join(
            settings.FIXTURES, 'test', 'road_district_summary.json')
        with open(road_district_summary_fixture, 'r') as _file:
            road_district_summary_fixture = json.load(_file)

        # world pop district summary fixture
        world_pop_district_summary = os.path.join(
            settings.FIXTURES, 'test', 'world_pop_district_summary.json')
        with open(world_pop_district_summary, 'r') as _file:
            world_pop_district_summary = json.load(_file)

        for event in events:
            # check district summary
            url = os.path.join(
                settings.POSTGREST_BASE_URL,
                'mv_flood_event_district_summary?flood_event_id=eq.{}'.format(
                    event['id']))
            for summary in requests.get(url).json():
                fixture = district_summary_fixture[summary['name']]
                for key, value in summary.items():
                    if key == 'flood_event_id':
                        return
                    self.assertEqual(value, fixture[key])

            # check road district summary
            url = os.path.join(
                settings.POSTGREST_BASE_URL,
                'mv_flood_event_road_district_summary?flood_event_id=eq.{}'.format(
                    event['id']))
            for summary in requests.get(url).json():
                fixture = road_district_summary_fixture[summary['name']]
                for key, value in summary.items():
                    if key == 'flood_event_id':
                        return
                    self.assertEqual(value, fixture[key])

            # check world pop district summary
            url = os.path.join(
                settings.POSTGREST_BASE_URL,
                'mv_flood_event_world_pop_district_summary?flood_event_id=eq.{}'.format(
                    event['id']))
            for summary in requests.get(url).json():
                fixture = world_pop_district_summary[summary['name']]
                for key, value in summary.items():
                    if key == 'flood_event_id':
                        return
                    self.assertEqual(value, fixture[key])
