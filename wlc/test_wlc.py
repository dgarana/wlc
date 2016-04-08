# -*- coding: utf-8 -*-
#
# Copyright © 2016 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate Client <https://github.com/nijel/wlc>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""Test the module."""
from __future__ import unicode_literals

from unittest import TestCase
from wlc import Weblate
import httpretty
import os

DATA_TEST_BASE = os.path.join(os.path.dirname(__file__), 'test_data', 'api')


def register_uri(path, domain='http://127.0.0.1:8000/api'):
    """Simplified URL registration"""
    filename = os.path.join(DATA_TEST_BASE, path)
    url = '/'.join((domain, path, ''))
    print url, filename
    with open(filename, 'rb') as handle:
        httpretty.register_uri(
            httpretty.GET,
            url,
            body=handle.read(),
            content_type='application/json'
        )


def register_uris():
    """Register URIs for httpretty."""
    paths = (
        'projects',
    )
    for path in paths:
        register_uri(path)

    register_uri('projects', domain='https://example.net')


class WeblateTest(TestCase):

    """Testing of Weblate class."""

    weblate = None

    @httpretty.activate
    def test_projects(self):
        """Test getting balance."""
        register_uris()
        self.assertEqual(
            len(Weblate().list_projects()),
            2,
        )
