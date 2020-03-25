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
module: pdns_auth_zone

short_description: Manages a zone in a PowerDNS Authoritative server

description:
  - This module allows a task to manage the presence and configuration
    of a zone in a PowerDNS Authoritative server.

requirements:
  - bravado

options:
  state:
    description:
      - If C(present) the zone will be created if necessary; if it
        already exists, its configuration will be updated to match
        the provided properties.
      - If C(absent) the zone will be removed it if exists.
      - If C(exists) the zone's existence will be checked, but it
        will not be modified. Any configuration properties provided
        will be ignored.
      - If C(notify) and the zone kind is C(Master), then NOTIFY
        will be sent to the zone's slaves.
      - If C(notify) and the zone kind is C(Slave), then the slave
        zone will be updated as if a NOTIFY had been received.
      - If C(retrieve) and the zone kind is C(Slave), then the slave
        zone will be retrieved from the master.
    choices: [ 'present', 'absent', 'exists', 'notify', 'retrieve' ]
    type: str
    required: false
    default: 'present'
  name:
    description:
      - Name of the zone to be managed.
    type: str
    required: true
  server_id:
    description:
      - ID of the server instance which holds the zone.
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
  properties:
    description:
      - Zone properties. Ignored when I(state=exists), I(state=absent), I(state=notify), or I(state=retrieve).
    type: complex
    contains:
      kind:
        description:
          - Zone kind.
        choices: [ 'Native', 'Master', 'Slave' ]
        type: str
        required: true
      account:
        description:
          - Optional string used for local policy.
        type: str
      nameservers:
        description:
          - List of nameserver names listed in SOA record for zone.
            Only used when I(kind=Native) or I(kind=Master).
        type: list
        elements: str
      masters:
        description:
          - List of IPv4 or IPv6 addresses which are masters for this zone.
            Only used when I(kind=Slave).
        type: list
        elements: str
  metadata:
    description:
      - Zone metadata. Ignored when I(state=exists), I(state=absent), I(state=notify), or I(state=retrieve).
    type: complex
    contains:

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

- name: check that zone exists
  pdns_auth_zone:
    name: d1.example.
    state: exists
    api_key: 'foobar'
    api_spec_file: "{{ temp_file.path }}"

- name: check that zone exists on a non-default server
  pdns_auth_zone:
    name: d1.example.
    state: exists
    api_key: 'foobar'
    api_url: 'http://pdns.server.example:80'
    api_spec_file: "{{ temp_file.path }}"

- name: send NOTIFY to slave servers for zone
  pdns_auth_zone:
    name: d1.example.
    state: notify
    api_key: 'foobar'
    api_spec_file: "{{ temp_file.path }}"

- name: retrieve zone from master server
  pdns_auth_zone:
    name: d1.example.
    state: retrieve
    api_key: 'foobar'
    api_spec_file: "{{ temp_file.path }}"

- name: create native zone
  pdns_auth_zone:
    name: d2.example.
    state: present
    api_key: 'foobar'
    api_spec_file: "{{ temp_file.path }}"
    properties:
      kind: 'Native'
      nameservers:
        - 'ns1.example.'

- name: change native zone to master
  pdns_auth_zone:
    name: d2.example.
    state: present
    api_key: 'foobar'
    api_spec_file: "{{ temp_file.path }}"
    properties:
      kind: 'Master'

- name: delete zone
  pdns_auth_zone:
    name: d2.example.
    state: absent
    api_key: 'foobar'
    api_spec_file: "{{ temp_file.path }}"

- name: create slave zone
  pdns_auth_zone:
    name: d3.example.
    state: present
    api_key: 'foobar'
    api_spec_file: "{{ temp_file.path }}"
    properties:
      kind: 'Slave'
      masters:
        - '1.1.1.1'
        - '::1'
"""

RETURN = """
%YAML 1.2
---
zone:
  description: Information about the zone
  returned: always
  type: complex
  contains:
    name:
      description: Name
      returned: always
      type: str
      sample: "domain.example."
    exists:
      description: Indicate whether the zone exists
      returned: always
      type: bool
      sample: yes
    kind:
      description: Kind
      returned: when present
      type: str
      choices: [ Native, Master, Slave ]
    serial:
      description: Serial number from SOA record
      returned: when present
      type: int
    dnssec:
      description: Flag indicating whether zone is signed with DNSSEC
      returned: when present
      type: bool
    masters:
      description: IP addresses of masters (only for slave zones)
      returned: when present
      type: list
      elements: str
    metadata:
      description: Zone metadata
      returned: when present
      type: complex
      contains:
"""

from ansible.module_utils.basic import AnsibleModule

from urllib.parse import urlparse
from ipaddress import ip_address


def validate_params(module):
    params = module.params

    name = params["name"]
    if not name.endswith("."):
        module.fail_json(msg=f"Zone name '{name}' does not end with '.'")

    if params["properties"]:
        props = params["properties"]

        if props["nameservers"]:
            if props["kind"] == "Slave":
                module.fail_json(
                    msg="'nameservers' cannot be specified for 'Slave' zones."
                )

            for ns in props["nameservers"]:
                if not ns.endswith("."):
                    module.fail_json(
                        msg=f"Nameserver name '{ns}' does not end with '.'"
                    )

        if props["masters"]:
            if props["kind"] != "Slave":
                module.fail_json(
                    msg="'masters' cannot be specified for non-'Slave' zones."
                )

            for m in props["masters"]:
                try:
                    ip_address(m)
                except ValueError:
                    module.fail_json(msg=f"Master '{m}' is not a valid IP address.")


def populate_metadata_result(m, res):
    def boolean_value(m, r, k):
        r[k] = m["metadata"][0] != 0

    def boolean_presence(m, r, k):
        r[k] = True

    def list_value(m, r, k):
        r[k] = m["metadata"]

    def string_value(m, r, k):
        r[k] = m["metadata"][0]

    map = {
        "ALLOW-AXFR-FROM": list_value,
        "ALLOW-DNSUPDATE-FROM": list_value,
        "ALSO-NOTIFY": list_value,
        "AXFR-MASTER-TSIG": string_value,
        "AXFR-SOURCE": string_value,
        "FORWARD-DNSUPDATE": boolean_presence,
        "GSS-ACCEPTOR-PRINCIPAL": string_value,
        "GSS-ALLOW-AXFR-PRINCIPAL": string_value,
        "IXFR": boolean_value,
        "LUA-AXFR-SCRIPT": string_value,
        "NOTIFY-DNSUPDATE": boolean_value,
        "PUBLISH-CDNSKEY": boolean_value,
        "PUBLISH-CDS": list_value,
        "SLAVE-RENOTIFY": boolean_value,
        "SOA-EDIT-DNSUPDATE": string_value,
        "TSIG-ALLOW-AXFR": list_value,
        "TSIG-ALLOW-DNSUPDATE": list_value,
    }
    l = map.get(m["kind"])
    if l:
        l(m, res, m["kind"].lower().replace("-", "_"))


def main():
    module_args = {
        "state": {
            "type": "str",
            "default": "present",
            "choices": ["present", "absent", "exists", "notify", "retrieve"],
        },
        "name": {"type": "str", "required": True,},
        "server_id": {"type": "str", "default": "localhost",},
        "api_url": {"type": "str", "default": "http://localhost:8081",},
        "api_key": {"type": "str", "required": True, "no_log": True,},
        "api_spec_file": {"type": "path", "required": True,},
        "properties": {
            "type": "dict",
            "options": {
                "kind": {
                    "type": "str",
                    "choices": ["Native", "Master", "Slave"],
                    "required": True,
                },
                "account": {"type": "str",},
                "nameservers": {"type": "list", "elements": "str",},
                "masters": {"type": "list", "elements": "str",},
            },
        },
        "metadata": {"type": "dict", "options": {},},
    }

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    try:
        from bravado.requests_client import RequestsClient
        from bravado.client import SwaggerClient
        from bravado.swagger_model import load_file
    except ImportError:
        module.fail_json(
            msg="The pdns_auth_zone module requires the 'bravado' package."
        )

    result = {
        "changed": False,
    }

    validate_params(module)

    state = module.params["state"]
    server_id = module.params["server_id"]
    zone = module.params["name"]

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

    result["zone"] = {}
    result["zone"]["name"] = zone
    result["zone"]["exists"] = False

    # first step is to get information about the zone, if it exists
    # this is required to translate the user-friendly zone name into
    # the zone_id required for subsequent API calls

    zone_info = api.zones.listZones(server_id=server_id, zone=zone).result()

    if len(zone_info) == 0:
        if (state == "exists") or (state == "absent"):
            # exit as there is nothing left to do
            module.exit_json(**result)
        elif state == "notify":
            module.fail_json(
                msg="NOTIFY cannot be requested for a non-existent zone", **result
            )
        elif state == "retrieve":
            module.fail_json(
                msg="Retrieval cannot be requested for a non-existent zone", **result
            )
        else:
            # state must be 'present'
            zone_id = None
    else:
        # get the full zone info
        # and populate the results dict
        zone_id = zone_info[0]["id"]
        zone_info = api.zones.listZone(server_id=server_id, zone_id=zone_id).result()
        result["zone"]["exists"] = True
        result["zone"]["kind"] = zone_info["kind"]
        result["zone"]["serial"] = zone_info["serial"]
        result["zone"]["account"] = zone_info["account"]
        result["zone"]["dnssec"] = zone_info["dnssec"]
        result["zone"]["masters"] = zone_info["masters"]
        # initialize the metadata result dict
        result["zone"]["metadata"] = {
            "allow_axfr_from": [],
            "allow_dnsupdate_from": [],
            "also_notify": [],
            "api_rectify": zone_info["api_rectify"],
            "axfr_master_tsig": None,
            "axfr_source": None,
            "gss_acceptor_principal": None,
            "gss_allow_axfr_principal": None,
            "forward_dnsupdate": False,
            "ixfr": False,
            "lua_axfr_script": None,
            "nsec3narrow": zone_info["nsec3narrow"],
            "nsec3param": zone_info["nsec3param"],
            "notify_dnsupdate": False,
            "publish_cdnskey": False,
            "publish_cds": [],
            "slave_renotify": False,
            "soa_edit": zone_info["soa_edit"],
            "soa_edit_api": zone_info["soa_edit_api"],
            "soa_edit_dnsupdate": None,
            "tsig_allow_axfr": [],
            "tsig_allow_dnsupdate": [],
        }
        zone_meta = api.zonemetadata.listMetadata(
            server_id=server_id, zone_id=zone_id
        ).result()
        for m in zone_meta:
            populate_metadata_result(m, result["zone"]["metadata"])

    # if only an existence check was requested,
    # the operation is complete
    if state == "exists":
        module.exit_json(**result)

    # if absence was requested, remove the zone and exit
    if state == "absent":
        api.zones.deleteZone(server_id=server_id, zone_id=zone_id).result()
        result["changed"] = True
        module.exit_json(**result)

    # if NOTIFY was requested, process it and exit
    if state == "notify":
        if zone_info["kind"] == "Native":
            module.fail_json(
                msg="NOTIFY cannot be requested for 'Native' zones", **result
            )

        api.zones.notifyZone(server_id=server_id, zone_id=zone_id).result()
        result["changed"] = True
        module.exit_json(**result)

    # if retrieval was requested, process it and exit
    if state == "retrieve":
        if zone_info["kind"] != "Slave":
            module.fail_json(
                msg="Retrieval can only be requested for 'Slave' zones", **result
            )

        api.zones.axfrRetrieveZone(server_id=server_id, zone_id=zone_id).result()
        result["changed"] = True
        module.exit_json(**result)

    # state must be 'present'
    if not zone_id:
        # create the requested zone
        zone_struct = {
            "name": zone,
        }

        if module.params["properties"]:
            props = module.params["properties"]

            if props["kind"]:
                zone_struct["kind"] = props["kind"]

                if props["kind"] != "Slave":
                    zone_struct["nameservers"] = props["nameservers"]

                if props["kind"] == "Slave":
                    zone_struct["masters"] = props["masters"]

            if props["account"]:
                zone_struct["account"] = props["account"]

        api.zones.createZone(
            server_id=server_id, rrsets=False, zone_struct=zone_struct
        ).result()
        result["changed"] = True
    else:
        # compare the zone's attributes to the provided
        # options and update it if necessary
        zone_struct = {}

        if module.params["properties"]:
            props = module.params["properties"]

            if props["kind"]:
                if zone_info["kind"] != props["kind"]:
                    zone_struct["kind"] = props["kind"]

                if props["kind"] == "Slave":
                    if props["masters"]:
                        mp_masters = props["masters"].sort()
                        zi_masters = zone_info["masters"].sort()

                        if zi_masters != mp_masters:
                            zone_struct["masters"] = props["masters"]

            if props["account"]:
                if zone_info["account"] != props["account"]:
                    zone_struct["account"] = props["account"]

        if len(zone_struct):
            api.zones.putZone(
                server_id=server_id, zone_id=zone_id, zone_struct=zone_struct
            ).result()
            result["changed"] = True

    module.exit_json(**result)


if __name__ == "__main__":
    main()
