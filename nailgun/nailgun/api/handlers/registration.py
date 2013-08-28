# -*- coding: utf-8 -*-

#    Copyright 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Product registration handlers
"""

import base64
import json
import os
import web


from nailgun.settings import settings
from nailgun.api.handlers.base import JSONHandler, content_json


class FuelKeyHandler(JSONHandler):
    """
    Version info handler
    """

    @content_json
    def GET(self):
        """
        :returns: FUEL/FUELWeb commit SHA, release version.
        :http: * 200 (OK)
        """
        key_data = {
            "sha": settings.COMMIT_SHA,
            "release": settings.PRODUCT_VERSION,
            "uuid": settings.FUEL_KEY
        }
        signature = base64.b64encode(json.dumps(key_data))
        key_data["signature"] = signature
        returns {"key": base64.b64encode(json.dumps(key_data))}