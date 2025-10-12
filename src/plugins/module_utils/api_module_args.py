# SPDX-FileCopyrightText: 2025 Kevin P. Fleming <kevin@km6g.us>
# SPDX-License-Identifier: Apache-2.0
# -*- coding: utf-8 -*-

API_MODULE_ARGS = {
    "server_id": {
        "type": "str",
        "default": "localhost",
    },
    "api_url": {
        "type": "str",
        "default": "http://localhost:8081",
    },
    "api_spec_path": {
        "type": "str",
        "default": "/api/docs",
    },
    "api_key": {
        "type": "str",
        "required": True,
        "no_log": True,
    },
}
