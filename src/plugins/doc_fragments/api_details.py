# SPDX-FileCopyrightText: 2021 Kevin P. Fleming <kevin@km6g.us>
# SPDX-License-Identifier: Apache-2.0
# -*- coding: utf-8 -*-


class ModuleDocFragment:
    DOCUMENTATION = """
options:
  server_id:
    description:
      - ID of the server instance which holds the key.
    type: str
    required: false
    default: 'localhost'
  api_url:
    description:
      - URL of the API endpoint in the server.
    type: str
    required: false
    default: 'http://localhost:8081'
  api_spec_path:
    description:
      - Path of the OpenAPI (Swagger) API spec document in C(api_url).
    type: str
    required: false
    default: '/api/docs'
  api_key:
    description:
      - Key (token) used to authenticate to the API endpoint in the server.
    type: str
    required: true
"""
