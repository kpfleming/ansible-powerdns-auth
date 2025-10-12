# SPDX-FileCopyrightText: 2025 Kevin P. Fleming <kevin@km6g.us>
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


class APIZoneWrapper(APIWrapper):
    def __init__(self, *, module, result, object_type, zone_id):
        super().__init__(module=module, result=result, object_type=object_type)
        self.zone_id = zone_id

    @api_exception_handler
    def axfrRetrieveZone(self):  # noqa: N802
        return self.raw_api.axfrRetrieveZone(
            server_id=self.server_id,
            zone_id=self.zone_id,
        ).result()

    @api_exception_handler
    def createZone(self, **kwargs):  # noqa: N802
        return self.raw_api.createZone(server_id=self.server_id, rrsets=False, **kwargs).result()

    @api_exception_handler
    def deleteZone(self):  # noqa: N802
        return self.raw_api.deleteZone(server_id=self.server_id, zone_id=self.zone_id).result()

    @api_exception_handler
    def listZone(self):  # noqa: N802
        return self.raw_api.listZone(
            server_id=self.server_id,
            zone_id=self.zone_id,
            rrsets=False,
        ).result()

    @api_exception_handler
    def listZones(self, **kwargs):  # noqa: N802
        return self.raw_api.listZones(server_id=self.server_id, **kwargs).result()

    @api_exception_handler
    def notifyZone(self):  # noqa: N802
        return self.raw_api.notifyZone(server_id=self.server_id, zone_id=self.zone_id).result()

    @api_exception_handler
    def putZone(self, **kwargs):  # noqa: N802
        return self.raw_api.putZone(
            server_id=self.server_id,
            zone_id=self.zone_id,
            **kwargs,
        ).result()


class APIZoneMetadataWrapper(APIWrapper):
    def __init__(self, *, module, result, object_type, zone_id):
        super().__init__(module=module, result=result, object_type=object_type)
        self.zone_id = zone_id

    @api_exception_handler
    def deleteMetadata(self, **kwargs):  # noqa: N802
        return self.raw_api.deleteMetadata(
            server_id=self.server_id,
            zone_id=self.zone_id,
            **kwargs,
        ).result()

    @api_exception_handler
    def listMetadata(self):  # noqa: N802
        return self.raw_api.listMetadata(server_id=self.server_id, zone_id=self.zone_id).result()

    @api_exception_handler
    def modifyMetadata(self, **kwargs):  # noqa: N802
        return self.raw_api.modifyMetadata(
            server_id=self.server_id,
            zone_id=self.zone_id,
            **kwargs,
        ).result()


class APITSIGKeyWrapper(APIWrapper):
    @api_exception_handler
    def createTSIGKey(self, **kwargs):  # noqa: N802
        return self.raw_api.createTSIGKey(server_id=self.server_id, **kwargs).result()

    @api_exception_handler
    def deleteTSIGKey(self, **kwargs):  # noqa: N802
        return self.raw_api.deleteTSIGKey(server_id=self.server_id, **kwargs).result()

    @api_exception_handler
    def getTSIGKey(self, **kwargs):  # noqa: N802
        return self.raw_api.getTSIGKey(server_id=self.server_id, **kwargs).result()

    @api_exception_handler
    def listTSIGKeys(self):  # noqa: N802
        return self.raw_api.listTSIGKeys(server_id=self.server_id).result()

    @api_exception_handler
    def putTSIGKey(self, **kwargs):  # noqa: N802
        return self.raw_api.putTSIGKey(server_id=self.server_id, **kwargs).result()
