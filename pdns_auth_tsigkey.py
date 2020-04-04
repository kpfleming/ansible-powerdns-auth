#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Kevin P. Fleming <kevin@km6g.us>
# Apache License 2.0 (see LICENSE)

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
%YAML 1.2
---
module: pdns_auth_tsigkey

short_description: Manages a TSIG key in a PowerDNS Authoritative server

description:
  - This module allows a task to manage the presence and content
    of a TSIG key in a PowerDNS Authoritative server.

requirements:
  - bravado

options:
  state:
    description:
      - If C(present) the zone will be created if necessary; if it
        already exists, its configuration will be updated to match
        the provided attributes.
      - If C(absent) the key will be removed it if exists.
      - If C(exists) the key's existence will be checked, but it
        will not be modified.
    choices: [ 'present', 'absent', 'exists' ]
    type: str
    required: false
    default: 'present'
  name:
    description:
      - Name of the key to be managed.
    type: str
    required: true
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
  api_key:
    description:
      - Key (token) used to authenticate to the API endpoint in the server.
    type: str
    required: true
  api_spec_file:
    description:
      - Path to a file containing the OpenAPI (Swagger) specification for the
        API version implemented by the server.
    type: path
    required: true
  algorithm:
    description:
      - The message digest algorithm, as specified by RFC 2845 and its updates,
        which will be used to validate requests including this key.
      - Required when C(state) is C(present).
    choices: [ 'hmac-md5', 'hmac-sha1', 'hmac-sha224', 'hmac-sha256', 'hmac-sha384',  'hmac-sha512' ]
    type: str
    required: false
    default: 'hmac-md5'
  key:
    description:
      - The base-64 encoded key value.
    type: str

author:
  - Kevin P. Fleming (@kpfleming)
"""

EXAMPLES = """
%YAML 1.2
---
# create and populate a file which holds the API specification
- name: temp file to hold spec
  tempfile:
    state: file
    suffix: '.json'
    register: temp_file

- name: populate spec file
  copy:
    src: api-swagger.json
    dest: "{{ temp_file.path }}"

- name: check that key exists
  pdns_auth_tsigkey:
    name: key1
    state: exists
    api_key: 'foobar'
    api_spec_file: "{{ temp_file.path }}"

- name: create key with default algorithm
  pdns_auth_tsigkey:
    name: key2
    state: present
    api_key: 'foobar'
    api_spec_file: "{{ temp_file.path }}"

- name: remove key
  pdns_auth_tsigkey:
    name: key2
    state: absent
    api_key: 'foobar'
    api_spec_file: "{{ temp_file.path }}"

- name: create key with algorithm and content
  pdns_auth_tsigkey:
    name: key3
    state: present
    api_key: 'foobar'
    api_spec_file: "{{ temp_file.path }}"
    algorithm: hmac-sha256
    key: '+8fQxgYhf5PVGPKclKnk8ReujIfWXOw/aEzzPPhDi6AGagpg/r954FPZdzgFfUjnmjMSA1Yu7vo6DQHVoGnRkw=='
"""

RETURN = """
%YAML 1.2
---
key:
  description: Information about the key
  returned: always
  type: complex
  contains:
    name:
      description: Name
      returned: always
      type: str
    exists:
      description: Indicate whether the key exists
      returned: always
      type: bool
    algorithm:
      description:
        - The message digest algorithm, as specified by RFC 2845 and its updates,
          which will be used to validate requests including this key.
      returned: always
      type: str
    key:
      description:
        - The base-64 encoded key value.
      returned: always
      type: str
"""

from ansible.module_utils.basic import AnsibleModule

from urllib.parse import urlparse


def main():
    module_args = {
        "state": {
            "type": "str",
            "default": "present",
            "choices": ["present", "absent", "exists"],
        },
        "name": {"type": "str", "required": True,},
        "server_id": {"type": "str", "default": "localhost",},
        "api_url": {"type": "str", "default": "http://localhost:8081",},
        "api_key": {"type": "str", "required": True, "no_log": True,},
        "api_spec_file": {"type": "path", "required": True,},
        "algorithm": {
            "type": "str",
            "default": "hmac-md5",
            "choices": [
                "hmac-md5",
                "hmac-sha1",
                "hmac-sha224",
                "hmac-sha256",
                "hmac-sha384",
                "hmac-sha512",
            ],
        },
        "key": {"type": "str"},
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    try:
        from bravado.requests_client import RequestsClient
        from bravado.client import SwaggerClient
        from bravado.swagger_model import load_file
    except ImportError:
        module.fail_json(
            msg="The pdns_auth_tsigkey module requires the 'bravado' package."
        )

    result = {
        "changed": False,
    }

    state = module.params["state"]
    server_id = module.params["server_id"]
    key = module.params["name"]

    if module.check_mode:
        module.exit_json(**result)

    url = urlparse(module.params["api_url"])

    http_client = RequestsClient()
    http_client.set_api_key(
        url.netloc, module.params["api_key"], param_name="X-API-Key", param_in="header"
    )

    spec = load_file(module.params["api_spec_file"])
    spec["host"] = url.netloc
    spec["schemes"] = [url.scheme]

    api = SwaggerClient.from_spec(spec, http_client=http_client)

    result["key"] = {"name": key, "exists": False}

    # first step is to get information about the key, if it exists
    # this is required to translate the user-friendly key name into
    # the key_id required for subsequent API calls

    partial_key_info = [
        k
        for k in api.tsigkey.listTSIGKeys(server_id=server_id).result()
        if k["name"] == key
    ]

    if len(partial_key_info) == 0:
        if (state == "exists") or (state == "absent"):
            # exit as there is nothing left to do
            module.exit_json(**result)
        else:
            # state must be 'present'
            key_id = None
    else:
        # get the full key info and populate the result dict
        key_id = partial_key_info[0]["id"]
        key_info = api.tsigkey.getTSIGKey(
            server_id=server_id, tsigkey_id=key_id
        ).result()
        result["key"]["exists"] = True
        result["key"]["algorithm"] = key_info["algorithm"]
        result["key"]["key"] = key_info["key"]

    # if only an existence check was requested,
    # the operation is complete
    if state == "exists":
        module.exit_json(**result)

    # if absence was requested, remove the zone and exit
    if state == "absent":
        api.tsigkey.deleteTSIGKey(server_id=server_id, tsigkey_id=key_id).result()
        result["changed"] = True
        module.exit_json(**result)

    # state must be 'present'
    if not key_id:
        # create the requested key
        key_struct = {
            "name": key,
            "algorithm": module.params["algorithm"],
        }

        if module.params["key"]:
            key_struct["key"] = module.params["key"]

        key_info = api.tsigkey.createTSIGKey(
            server_id=server_id, tsigkey=key_struct
        ).result()
        result["changed"] = True
        result["key"]["exists"] = True
        result["key"]["algorithm"] = key_info["algorithm"]
        result["key"]["key"] = key_info["key"]
    else:
        # compare the key's attributes to the provided
        # options and update it if necessary
        key_struct = {}

        if module.params["algorithm"]:
            if module.params["algorithm"] != key_info["algorithm"]:
                key_struct["algorithm"] = module.params["algorithm"]

        if module.params["key"]:
            if module.params["key"] != key_info["key"]:
                key_struct["key"] = module.params["key"]

        if len(key_struct):
            key_info = api.tsigkey.putTSIGKey(
                server_id=server_id, tsigkey_id=key_id, tsigkey=key_struct
            ).result()
            result["changed"] = True

        if result["changed"]:
            result["key"]["algorithm"] = key_info["algorithm"]
            result["key"]["key"] = key_info["key"]

    module.exit_json(**result)


if __name__ == "__main__":
    main()
