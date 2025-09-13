#!/usr/bin/python
# SPDX-FileCopyrightText: 2025 Mohamed Chamrouk <mohamed.chamrouk@proton.me>
# SPDX-License-Identifier: Apache-2.0
# -*- coding: utf-8 -*-

import sys

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.kpfleming.powerdns_auth.plugins.module_utils.api_wrapper import (
    APIWrapper,
    api_exception_handler,
)

assert sys.version_info >= (3, 9), "This module requires Python 3.9 or newer."

DOCUMENTATION = """
%YAML 1.2
---
module: powerdns_auth_cryptokey

short_description: Manages a cryptokey in a zone of PowerDNS Authoritative server

description:
  - This module can create, delete, activate/deactivate, publish/unpublish a cryptokey
    in a zone of PowerDNS Authoritative server.

requirements:
  - bravado

extends_documentation_fragment:
  - kpfleming.powerdns_auth.api_details

options:
  state:
    description:
      - If V(present) the cryptokey will be created
      - If V(present) and O(cryptokey_id) the cryptokey will be updated
      - If V(absent) the cryptokey will be deleted
      - If V(exists) lists all the keys in the zone
      - If V(exists) and O(cryptokey_id) returns the corresponding cryptokey
    choices: [ 'present', 'absent', 'exists' ]
    type: str
    required: false
    default: 'present'
  zone_name:
    description:
      - Name of the zone
    type: str
    required: true
  server_id:
    description:
      - ID of the server managed.
    type: str
    default: localhost
  api_url:
    description:
      - URL of the API of the PowerDNS Authoritative server.
    type: str
    default: 'http://localhost:8081'
  api_spec_path:
    description:
      - API endpoint of the swagger resource.
    type: str
    default: /api/docs
  api_key:
    description:
      - Key of the PowerDNS API.
    type: str
    required: true
  cryptokey_id:
    description:
      - The cryptokey id.
    type: str
  cryptokey:
    description:
      - Cryptokey object definition.
    type: dict
    suboptions:
      keytype:
        description:
          - The type of key, either zone signing key (zsk), key signing key (ksk)
            or combined signing key (csk)
          - Note that by default if only one key is present it will be used as a csk regardless of
            the provided type. For the key to assume its role another key of the opposite type has
            to be present (zsk for ksk and vice-versa).
        type: str
        choices: [ 'zsk', 'ksk', 'csk']
        required: true
      active:
        description:
          - Whether the key is active or not.
        type: bool
        default: false
      published:
        description:
          - Whether the key is published or not.
        type: bool
        default: true
      dnskey:
        description:
          - The DNSKEY record for the cryptokey.
          - Required alongside O(privatekey) for cryptokey creation if O(algorithm)
            is not present.
        type: str
      privatekey:
        description:
          - The privatekey in ISC format.
          - Required if O(dnskey)
        type: str
      algorithm:
        description:
          - Algorithm for key generation.
        type: str
      bits:
        description:
          - Size of the key in bits when O(algorithm) is a variant of RSA.
        type: int
        default: 4096

author:
  - Mohamed Chamrouk (@mohamed-chamrouk)
"""

EXAMPLES = """
%YAML 1.2
---
- name: Generate key
  kpfleming.powerdns_auth.cryptokey:
    api_key: foo
    zone_name: crypto.example.
    state: present
    cryptokey:
      keytype: csk
      algorithm: ed25519
      active: true

- name: Import key
  kpfleming.powerdns_auth.cryptokey:
    api_key: foo
    zone_name: crypto.example.
    state: present
    cryptokey:
      keytype: zsk
      dnskey: "257 3 15 lMu/7quhLeSueMcdlt3T0sxln32yhrhASCKKDB1xJOk="
      privatekey: |
        Private-key-format: v1.2
        Algorithm: 15 (ED25519)
        PrivateKey: Rnt2dv3mWMmP8bU/8koayZ4R5dWdI86zJmZ0nnjPe6Q=
      active: true

- name: Delete key
  kpfleming.powerdns_auth.cryptokey:
    api_key: foo
    zone_name: crypto.example.
    state: absent
    cryptokey_id: 1

- name: Activating key
  kpfleming.powerdns_auth.cryptokey:
    api_key: foo
    zone_name: crypto.example.
    state: present
    cryptokey_id: 1
    cryptokey:
      active: true

- name: Listing a specific key
  kpfleming.powerdns_auth.cryptokey:
    api_key: foo
    zone_name: crypto.example.
    state: exists
    cryptokey_id: 1

- name: Listing all keys in the zone
  kpfleming.powerdns_auth.cryptokey:
    api_key: foo
    zone_name: crypto.example.
    state: exists
"""

RETURN = """
%YAML 1.2
---
exists:
  description:
    - If cryptokey_id is provided, whether a corresponding key exists
    - Otherwise if there is any key in the zone
  returned: when state is exists
  type: bool
cryptokey:
  description:
    - The corresponding key when state is exists and cryptokey_id is provided
  returned: when state is exists and cryptokey_id is provided
  type: dict
  contains:
    active:
      description: whether or not the key is active
      type: bool
    algorithm:
      description: the key algorithm
      type: str
    bits:
      description: size in bits, used in dnskey record
      type: int
    dnskey:
      description: the dnskey record
      type: str
    ds:
      description: when key is ksk or csk, used to create the DS record on the parent zone
      type: list
      elements: str
    flags:
      description: flags
      type: str
    id:
      description: the id of the key
      type: str
    keytype:
      description: the type of the key
      type: str
    published:
      description: whether or not the key is published
      type: bool
    type:
      description: always Cryptokey
      type: str
cryptokeys:
  description:
    - List of existing cryptokeys after all the changes are made.
  returned: always except when cryptokey is returned
  type: list
  elements: dict
  contains:
    active:
      description: whether or not the key is active
      type: bool
    algorithm:
      description: the key algorithm
      type: str
    bits:
      description: size in bits, used in dnskey record
      type: int
    dnskey:
      description: the dnskey record
      type: str
    ds:
      description: when key is ksk or csk, used to create the DS record on the parent zone
      type: list
      elements: str
    flags:
      description: flags
      type: str
    id:
      description: the id of the key
      type: str
    keytype:
      description: the type of the key
      type: str
    published:
      description: whether or not the key is published
      type: bool
    type:
      description: always Cryptokey
      type: str
"""


class APIZoneWrapper(APIWrapper):
    def __init__(self, *, module, result, object_type, zone_id):
        super().__init__(module=module, result=result, object_type=object_type)
        self.zone_id = zone_id

    @api_exception_handler
    def listZones(self, **kwargs):  # noqa: N802
        return self.raw_api.listZones(server_id=self.server_id, **kwargs).result()


class APICryptokeyWrapper(APIWrapper):
    def __init__(self, *, module, result, object_type, zone_id, cryptokey_id):
        super().__init__(module=module, result=result, object_type=object_type)
        self.zone_id = zone_id
        self.cryptokey_id = cryptokey_id

    @api_exception_handler
    def listCryptokeys(self):  # noqa: N802
        return self.raw_api.listCryptokeys(
            server_id=self.server_id,
            zone_id=self.zone_id,
        ).result()

    @api_exception_handler
    def createCryptokey(self, **kwargs):  # noqa: N802
        return self.raw_api.createCryptokey(
            server_id=self.server_id,
            zone_id=self.zone_id,
            **kwargs,
        ).result()

    @api_exception_handler
    def getCryptokey(self):  # noqa: N802
        return self.raw_api.getCryptokey(
            server_id=self.server_id, zone_id=self.zone_id, cryptokey_id=self.cryptokey_id
        ).result()

    @api_exception_handler
    def modifyCryptokey(self, **kwargs):  # noqa: N802
        return self.raw_api.modifyCryptokey(
            server_id=self.server_id, zone_id=self.zone_id, cryptokey_id=self.cryptokey_id, **kwargs
        ).result()

    @api_exception_handler
    def deleteCryptokey(self):  # noqa: N802
        return self.raw_api.deleteCryptokey(
            server_id=self.server_id, zone_id=self.zone_id, cryptokey_id=self.cryptokey_id
        ).result()


def main():
    module_args = {
        "state": {
            "type": "str",
            "default": "present",
            "choices": ["present", "absent", "exists"],
        },
        "zone_name": {
            "type": "str",
            "required": True,
        },
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
        "cryptokey_id": {
            "type": "str",
        },
        "cryptokey": {
            "type": "dict",
            "options": {
                "keytype": {"type": "str", "required": False, "choices": ["zsk", "ksk", "csk"]},
                "active": {"type": "bool", "default": False},
                "published": {"type": "bool", "default": True},
                "dnskey": {"type": "str", "required": False},
                "privatekey": {"type": "str", "required": False},
                "algorithm": {"type": "str", "required": False},
                "bits": {"type": "int", "default": 4096},
            },
        },
    }

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_if=(("state", "present", ["cryptokey"]), ("state", "absent", ["cryptokey_id"])),
    )

    result = {"changed": False, "cryptokey": {}, "cryptokeys": []}

    params = module.params
    state = params["state"]
    zone_name = params["zone_name"]

    api_zone_client = APIZoneWrapper(
        module=module, result=result, object_type="zones", zone_id=None
    )

    api_cryptokey_client = APICryptokeyWrapper(
        module=module, result=result, object_type="zonecryptokey", zone_id=None, cryptokey_id=None
    )

    partial_zone_info = api_zone_client.listZones(zone=zone_name)

    if len(partial_zone_info) == 0:
        module.fail_json(msg=f"No zone found for name {zone_name}", **result)

    # get the zone_id from the zone_name
    zone_id = partial_zone_info[0]["id"]
    api_cryptokey_client.zone_id = zone_id

    existing_zone_keys = api_cryptokey_client.listCryptokeys()

    if state == "exists":
        result["exists"] = False
        if params["cryptokey_id"] is not None:
            api_cryptokey_client.cryptokey_id = params["cryptokey_id"]
            result["cryptokey"] = api_cryptokey_client.getCryptokey()
            # nonexistent key id is handled by the API error handler
        else:
            result["cryptokeys"] = existing_zone_keys

        if result["cryptokey"] or result["cryptokeys"]:
            result["exists"] = True
    elif state == "present":
        cryptokey_def = params["cryptokey"]
        if params["cryptokey_id"] is None:
            # Creating the cryptokey
            if cryptokey_def["keytype"] is None:
                module.fail_json(msg="Missing keytype option in cryptokey definition", **result)

            generated_key_fields = ["algorithm"]
            imported_key_fields = ["dnskey", "privatekey"]
            common_fields = ["keytype", "active", "published"]

            if cryptokey_def["algorithm"] is not None:
                if "rsa" in cryptokey_def["algorithm"].lower():
                    # RSA type algorithm requires the bits field
                    generated_key_fields += ["bits"]
                result_fields = common_fields + generated_key_fields
            elif cryptokey_def["privatekey"] is not None and cryptokey_def["dnskey"] is not None:
                result_fields = common_fields + imported_key_fields
            else:
                module.fail_json(msg="Wrong options provided for cryptokey creation", **result)

            cryptokey = {field: cryptokey_def[field] for field in result_fields}

            api_cryptokey_client.createCryptokey(cryptokey=cryptokey)
        else:
            # Updating the cryptokey
            cryptokeys_ids = [str(key["id"]) for key in existing_zone_keys]

            if params["cryptokey_id"] in cryptokeys_ids:
                cryptokey = {
                    "active": cryptokey_def["active"],
                    "published": cryptokey_def["published"],
                }
            else:
                module.fail_json(
                    msg=f"Key of id {params['cryptokey_id']} not found \
                          for zone {params['zone_name']}",
                    **result,
                )

            api_cryptokey_client.cryptokey_id = params["cryptokey_id"]
            api_cryptokey_client.modifyCryptokey(cryptokey=cryptokey)

        result["changed"] = True
    else:
        # when state is absent
        cryptokeys_ids = [str(key["id"]) for key in existing_zone_keys]
        cryptokey_id = params["cryptokey_id"]

        if cryptokey_id in cryptokeys_ids:
            api_cryptokey_client.cryptokey_id = cryptokey_id
            api_cryptokey_client.deleteCryptokey()
        else:
            module.fail_json(
                msg=f"Key of id {params['cryptokey_id']} not found for zone {params['zone_name']}",
                **result,
            )

        result["changed"] = True

    if result["changed"]:
        result["cryptokeys"] = api_cryptokey_client.listCryptokeys()

    module.exit_json(**result)


if __name__ == "__main__":
    main()
