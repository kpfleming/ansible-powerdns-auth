# SPDX-FileCopyrightText: 2025 Kevin P. Fleming <kevin@km6g.us>
# SPDX-License-Identifier: Apache-2.0
# -*- coding: utf-8 -*-

from typing import Any

from api_client import AuthenticatedClient
from api_client.api import tsigkey
from api_client.models import error, tsig_key


class APIWrapper:
    def __init__(self, *, module, result):
        self.module = module
        self.server_id = module.params["server_id"]
        self.result = result

        self.client = AuthenticatedClient(
            base_url=module.params["api_url"],
            verify_ssl=False,
            auth_header_name="X-API-Key",
            token=module.params["api_key"],
        )


class TSIGKey(APIWrapper):
    def create(self, key: tsig_key.TSIGKey) -> tsig_key.TSIGKey | error.Error:
        return tsigkey.create_tsig_key.sync(server_id=self.server_id, client=self.client, body=key)

    def delete(self, key_id: str) -> Any | error.Error:
        return tsigkey.delete_tsig_key.sync(
            server_id=self.server_id, client=self.client, tsigkey_id=key_id
        )

    def get(self, key_id: str) -> tsig_key.TSIGKey | error.Error:
        return tsigkey.get_tsig_key.sync(
            server_id=self.server_id, client=self.client, tsigkey_id=key_id
        )

    def list(self) -> list[tsig_key.TSIGKey] | error.Error:
        return tsigkey.list_tsig_keys.sync(server_id=self.server_id, client=self.client)

    def put(self, key_id: str, key: tsig_key.TSIGKey) -> tsig_key.TSIGKey | error.Error:
        return tsigkey.put_tsig_key.sync(
            server_id=self.server_id, client=self.client, tsigkey_id=key_id, body=key
        )
