#!/usr/bin/python
# SPDX-FileCopyrightText: 2026 Kevin P. Fleming <kevin@km6g.us>
# SPDX-License-Identifier: Apache-2.0
# -*- coding: utf-8 -*-

import sys

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common import validation as param_validation

from ..module_utils.api_module_args import API_MODULE_ARGS
from ..module_utils.api_wrapper import APITSIGKeyWrapper

assert sys.version_info >= (3, 10), "This module requires Python 3.10 or newer."

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

extends_documentation_fragment:
  - kpfleming.powerdns_auth.api_details

options:
  state:
    description:
      - If C(present) the key will be created if necessary; if it
        already exists, its configuration will be updated to match
        the provided attributes.
      - If C(absent) the key will be removed it if exists.
      - If C(exists) the key's existence will be checked, but it
        will not be modified.
    choices: [ 'present', 'absent', 'exists' ]
    type: str
    required: false
    default: 'present'
  id:
    description:
      - ID of the key to be managed.
    type: str
  name:
    description:
      - Name of the key to be managed if C(id) is not provided, otherwise if C(state)
        is C(present) and the key's name should be changed then the new name for the
        key identified by C(id).
    type: str
  algorithm:
    description:
      - The message digest algorithm, as specified by RFC 2845 and its updates,
        which will be used to validate requests including this key.
      - Required when C(state) is C(present).
    choices: [ 'hmac-md5',
               'hmac-sha1',
               'hmac-sha224',
               'hmac-sha256',
               'hmac-sha384',
               'hmac-sha512',
             ]
    type: str
    default: 'hmac-md5'
  key:
    description:
      - The Base64 encoded key value.
    type: str

author:
  - Kevin P. Fleming (@kpfleming)
"""

EXAMPLES = """
%YAML 1.2
---
- name: check that key exists
  pdns_auth_tsigkey:
    name: key1
    state: exists
    api_key: 'foobar'

- name: create key with default algorithm
  register: _key
  pdns_auth_tsigkey:
    name: key2
    state: present
    api_key: 'foobar'

- name: remove key by ID
  pdns_auth_tsigkey:
    id: _key.id
    state: absent
    api_key: 'foobar'

- name: create key with algorithm and content
  register: _key
  pdns_auth_tsigkey:
    name: key3
    state: present
    api_key: 'foobar'
    algorithm: hmac-sha256
    key: '+8fQxgYhf5PVGPKclKnk8ReujIfWXOw/aEzzPPhDi6AGagpg/r954FPZdzgFfUjnmjMSA1Yu7vo6DQHVoGnRkw=='

- name: change name of key
  pdns_auth_tsigkey:
    id: _key.id
    state: present
    name: key4
"""

RETURN = """
%YAML 1.2
---
key:
  description: Information about the key
  returned: always
  type: complex
  contains:
    id:
      description: ID
      type: str
    name:
      description: Name
      type: str
    exists:
      description: Indicate whether the key exists
      returned: always
      type: bool
    algorithm:
      description:
        - The message digest algorithm, as specified by RFC 2845 and its updates,
          which will be used to validate requests including this key.
      type: str
    key:
      description:
        - The Base64 encoded key value.
      type: str
"""


def main():
    module_args = {
        **API_MODULE_ARGS,
        "state": {
            "type": "str",
            "default": "present",
            "choices": ["present", "absent", "exists"],
        },
        "id": {
            "type": "str",
        },
        "name": {
            "type": "str",
        },
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

    module = AnsibleModule(
        argument_spec=module_args, supports_check_mode=True, required_one_of=[["id", "name"]]
    )

    result = {
        "changed": False,
    }

    params = module.params

    state = params["state"]

    # for "exists" and "absent" only one of 'id' and 'name' can be provided
    if state in ("exists", "absent"):
        param_validation.check_mutually_exclusive([["id", "name"]], params)

    if module.check_mode:
        module.exit_json(**result)

    # create an object to proxy the raw API object and curry the
    # server_id into all API calls automatically, along with handling
    # predictable exceptions
    api_client = APITSIGKeyWrapper(module=module, result=result, object_type="tsigkey")

    result["key"] = {"exists": False}

    # if 'id' was provided, look up the key with that ID, otherwise look up the key by name
    if "id" in params:
        key_info = api_client.getTSIGKey(params["id"], allow_not_found=True)
        if key_info is None:
            result["key"]["id"] = params["id"]
            match state:
                case "exists" | "absent":
                    # exit as there is nothing left to do
                    module.exit_json(**result)
                case "present":
                    # report an error since 'state=present' with 'id'
                    # specified requires that they key already exists
                    module.fail_json(msg="Cannot modify a non-existent key", **result)
        key_id = key_info["id"]
    else:
        partial_key_info = [k for k in api_client.listTSIGKeys() if k["name"] == params["name"]]
        if len(partial_key_info) == 0:
            match state:
                case "exists" | "absent":
                    # exit as there is nothing left to do
                    result["key"]["name"] = params["name"]
                    module.exit_json(**result)
                case "present":
                    key_id = None
        else:
            key_id = partial_key_info[0]["id"]
            key_info = api_client.getTSIGKey(key_id)

    if key_id:
        result["key"]["exists"] = True
        result["key"]["id"] = key_id
        result["key"]["name"] = key_info["name"]
        result["key"]["algorithm"] = key_info["algorithm"]
        result["key"]["key"] = key_info["key"]

    match state:
        case "exists":
            # if only an existence check was requested,
            # the operation is complete
            pass

        case "absent":
            # if absence was requested, remove the key
            api_client.deleteTSIGKey(key_id)
            result["changed"] = True

        case "present":
            if not key_id:
                # create the requested key
                key_struct = {
                    "name": params["name"],
                    "algorithm": params["algorithm"],
                }

                if params["key"]:
                    key_struct["key"] = params["key"]

                key_info = api_client.createTSIGKey(tsigkey=key_struct)
                result["changed"] = True
                result["key"]["exists"] = True
                result["key"]["id"] = key_info["id"]
                result["key"]["name"] = key_info["name"]
                result["key"]["algorithm"] = key_info["algorithm"]
                result["key"]["key"] = key_info["key"]
            else:
                # compare the key's attributes to the provided
                # options and update them if necessary
                key_struct = {}

                if (mod_name := params["name"]) and mod_name != key_info["name"]:
                    key_struct["name"] = mod_name

                if (mod_alg := params["algorithm"]) and mod_alg != key_info["algorithm"]:
                    key_struct["algorithm"] = mod_alg

                if (mod_key := params["key"]) and mod_key != key_info["key"]:
                    key_struct["key"] = mod_key

                if key_struct:
                    key_info = api_client.putTSIGKey(key_id, tsigkey=key_struct)
                    result["changed"] = True

                result["key"]["id"] = key_info["id"]
                result["key"]["name"] = key_info["name"]
                result["key"]["algorithm"] = key_info["algorithm"]
                result["key"]["key"] = key_info["key"]

    module.exit_json(**result)


if __name__ == "__main__":
    main()
