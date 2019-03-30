# -*- coding: utf-8 -*-
# Copyright 2014 Google Inc. All rights reserved.
#
# Modifications Copyright (C) 2018 HeiGIT, University of Heidelberg.
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#

"""Tests for the Google module."""

from routingpy import Google
from tests.test_helper import *
import tests as _test

import responses
from copy import deepcopy


class GoogleTest(_test.TestCase):
    name = 'google'

    def setUp(self):
        self.key = 'sample_key'
        self.client = Google(api_key=self.key)

    @responses.activate
    def test_full_directions(self):
        query = ENDPOINTS_QUERIES[self.name]['directions']

        responses.add(responses.GET,
                      'https://maps.googleapis.com/maps/api/directions/json',
                      status=200,
                      json={},
                      content_type='application/json')

        routes = self.client.directions(**query)
        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://maps.googleapis.com/maps/api/directions/json?alternatives=true&arrival_time=1567512000&'
            'avoid=tolls%7Cferries&destination=49.445776%2C8.780916&key=sample_key&language=de&origin=49.420577%2C8.688641&'
            'profile=driving&region=de&traffic_model=optimistic&transit_mode=bus%7Crail&transit_routing_preference=less_walking&'
            'units=metrics&waypoints=49.415776%2C8.680916',
            responses.calls[0].request.url
        )

    @responses.activate
    def test_waypoint_generator_directions(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['directions'])
        query['coordinates'] = [
            PARAM_LINE_MULTI[1],
            Google.WayPoint('osazgqo@/@', 'enc', False),
            Google.WayPoint(PARAM_LINE_MULTI[1], 'coords', True),
            Google.WayPoint('EiNNYXJrdHBsLiwgNjkxMTcgSGVpZGVsYmVyZywgR2VybWFueSIuKiwKFAoSCdubgq0HwZdHEdclR2bm32EmEhQKEgmTG6mCBsGXRxF38ZZ8m5j3VQ', 'place_id', False),
            PARAM_LINE_MULTI[0],
        ]
        query['optimize'] = True

        responses.add(responses.GET,
                      'https://maps.googleapis.com/maps/api/directions/json',
                      status=200,
                      json={},
                      content_type='application/json')

        resp = self.client.directions(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://maps.googleapis.com/maps/api/directions/json?alternatives=true&arrival_time=1567512000&'
            'avoid=tolls%7Cferries&destination=49.420577%2C8.688641&key=sample_key&language=de&'
            'origin=49.415776%2C8.680916&profile=driving&region=de&traffic_model=optimistic&transit_mode=bus%7Crail&t'
            'ransit_routing_preference=less_walking&units=metrics&waypoints=optimize%3Atrue%7Cvia%3Aenc%3Aosazgqo%40%2F%40%3A%7C49.415776%2C8.680916%7C'
            'via%3Aplace_id%3AEiNNYXJrdHBsLiwgNjkxMTcgSGVpZGVsYmVyZywgR2VybWFueSIuKiwKFAoSCdubgq0HwZdHEdclR2bm32EmEhQKEgmTG6mCBsGXRxF38ZZ8m5j3VQ',
            responses.calls[0].request.url
        )

        # Test if 'bla' triggers a ValueError
        query['coordinates'].insert(1, Google.WayPoint(PARAM_LINE_MULTI[0], 'bla', True))

        with self.assertRaises(ValueError):
            resp = self.client.directions(**query)

        # Test if origin=WayPoint triggers a TypeError
        query['coordinates'] = [
            Google.WayPoint('osazgqo@/@', 'enc', False),
            Google.WayPoint(PARAM_LINE_MULTI[1], 'coords', True),
        ]

        with self.assertRaises(TypeError):
            self.client.directions(**query)

    @responses.activate
    def test_full_matrix(self):
        query = ENDPOINTS_QUERIES[self.name]['matrix']

        responses.add(responses.GET,
                      'https://maps.googleapis.com/maps/api/distancematrix/json',
                      status=200,
                      json={},
                      content_type='application/json')

        matrix = self.client.distance_matrix(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://maps.googleapis.com/maps/api/distancematrix/json?arrival_time=1567512000&avoid=tolls%7Cferries&'
            'destinations=49.420577%2C8.688641%7C49.415776%2C8.680916%7C49.445776%2C8.780916&key=sample_key&language=de&'
            'origins=49.420577%2C8.688641%7C49.415776%2C8.680916%7C49.445776%2C8.780916&profile=driving&region=de&'
            'traffic_model=optimistic&transit_mode=bus%7Crail&transit_routing_preference=less_walking&units=metrics',
            responses.calls[0].request.url
        )

    @responses.activate
    def test_few_sources_destinations_matrix(self):
        query = deepcopy(ENDPOINTS_QUERIES[self.name]['matrix'])
        query['sources'] = [1]
        query['destinations'] = [0]

        responses.add(responses.GET,
                      'https://maps.googleapis.com/maps/api/distancematrix/json',
                      status=200,
                      json={},
                      content_type='application/json')

        resp = self.client.distance_matrix(**query)

        query['sources'] = None
        query['destinations'] = [1, 2]

        responses.add(responses.GET,
                      'https://maps.googleapis.com/maps/api/distancematrix/json',
                      status=200,
                      json={},
                      content_type='application/json')

        resp = self.client.distance_matrix(**query)

        self.assertEqual(2, len(responses.calls))
        self.assertURLEqual(
            'https://maps.googleapis.com/maps/api/distancematrix/json?arrival_time=1567512000&avoid=tolls%7Cferries&'
            'destinations=49.420577%2C8.688641&key=sample_key&language=de&origins=49.415776%2C8.680916&profile=driving&'
            'region=de&traffic_model=optimistic&transit_mode=bus%7Crail&transit_routing_preference=less_walking&'
            'units=metrics',
            responses.calls[0].request.url
        )
        self.assertURLEqual(
            'https://maps.googleapis.com/maps/api/distancematrix/json?arrival_time=1567512000&avoid=tolls%7Cferries&'
            'destinations=49.415776%2C8.680916%7C49.445776%2C8.780916&key=sample_key&language=de&'
            'origins=49.420577%2C8.688641%7C49.415776%2C8.680916%7C49.445776%2C8.780916&profile=driving&region=de&'
            'traffic_model=optimistic&transit_mode=bus%7Crail&transit_routing_preference=less_walking&units=metrics',
            responses.calls[1].request.url
        )

    @responses.activate
    def test_waypoint_generator_matrix(self):
        query = ENDPOINTS_QUERIES[self.name]['matrix']
        query['coordinates'] = [
            PARAM_LINE_MULTI[1],
            Google.WayPoint('osazgqo@/@', 'enc', False),
            Google.WayPoint(PARAM_LINE_MULTI[1], 'coords', True),
            Google.WayPoint('EiNNYXJrdHBsLiwgNjkxMTcgSGVpZGVsYmVyZywgR2VybWFueSIuKiwKFAoSCdubgq0HwZdHEdclR2bm32EmEhQKEgmTG6mCBsGXRxF38ZZ8m5j3VQ', 'place_id', False),
            PARAM_LINE_MULTI[0],
        ]

        responses.add(responses.GET,
                      'https://maps.googleapis.com/maps/api/distancematrix/json',
                      status=200,
                      json={},
                      content_type='application/json')

        matrix = self.client.distance_matrix(**query)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            'https://maps.googleapis.com/maps/api/distancematrix/json?arrival_time=1567512000&avoid=tolls%7Cferries&'
            'destinations=49.415776%2C8.680916%7Cvia%3Aenc%3Aosazgqo%40%2F%40%3A%7C49.415776%2C8.680916%7Cvia%3Aplace_id%3A'
            'EiNNYXJrdHBsLiwgNjkxMTcgSGVpZGVsYmVyZywgR2VybWFueSIuKiwKFAoSCdubgq0HwZdHEdclR2bm32EmEhQKEgmTG6mCBsGXRxF38ZZ8m5j3VQ%7C49.420577%2C8.688641&'
            'key=sample_key&language=de&origins=49.415776%2C8.680916%7Cvia%3Aenc%3Aosazgqo%40%2F%40%3A%7C49.415776%2C8.680916%7Cvia%3Aplace_id%3AEiNNYXJrdHBsLiwgNjkxMTcgSGVpZGVsYmVyZywgR2VybWFueSIuKiwKFAoSCdubgq0HwZdHEdclR2bm32EmEhQKEgmTG6mCBsGXRxF38ZZ8m5j3VQ%7C49.420577%2C8.688641&'
            'profile=driving&region=de&traffic_model=optimistic&transit_mode=bus%7Crail&transit_routing_preference=less_walking&units=metrics',
            responses.calls[0].request.url
        )
  
