# SPDX-FileCopyrightText: 2021 Kevin P. Fleming <kevin@km6g.us>
# SPDX-License-Identifier: Apache-2.0
# -*- coding: utf-8 -*-

from functools import wraps
from urllib.parse import urlparse


class APIWrapper:
    def __init__(self, *, module, result, object_type):
        self.module = module
        self.server_id = module.params["server_id"]
        self.result = result

        try:
            from bravado.client import SwaggerClient
            from bravado.exception import (
                HTTPBadRequest,
                HTTPConflict,
                HTTPInternalServerError,
                HTTPNotFound,
                HTTPUnprocessableEntity,
            )
            from bravado.requests_client import RequestsClient
        except ImportError:
            module.fail_json(msg="This module requires the 'bravado' package.")

        self.api_exceptions_to_catch = (
            HTTPBadRequest,
            HTTPNotFound,
            HTTPConflict,
            HTTPUnprocessableEntity,
            HTTPInternalServerError,
        )

        url = urlparse(module.params["api_url"])

        http_client = RequestsClient()
        http_client.set_api_key(
            url.netloc,
            module.params["api_key"],
            param_name="X-API-Key",
            param_in="header",
        )

        full_api = SwaggerClient.from_url(
            module.params["api_url"] + module.params["api_spec_path"],
            http_client=http_client,
            request_headers={
                "Accept": "application/json",
                "X-API-Key": module.params["api_key"],
            },
        )
        self.raw_api = getattr(full_api, object_type)


def api_exception_handler(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except self.api_exceptions_to_catch as e:
            self.module.fail_json(
                msg=f"API operation {func.__name__} returned '{e.swagger_result['error']}'",
                **self.result,
            )

    return wrapper
