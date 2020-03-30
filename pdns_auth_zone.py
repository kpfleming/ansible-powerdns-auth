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
      allow_axfr_from:
        description:
          - List of IPv4 and/or IPv6 subnets (or the special value AUTO-NS) from which AXFR requests will be accepted.
        type: list
        elements: str
      allow_dnsupdate_from:
        description:
          - List of IPv4 and/or IPv6 subnets from which DNSUPDATE requests will be accepted.
        type: list
        elements: str
      also_notify:
        description:
          - List of IPv4 and/or IPv6 addresses (with optional port numbers) which will receive NOTIFY for updates.
        type: list
        elements: str
      axfr_master_tsig:
        description:
          - Key to be used to AXFR the zone from its master.
        type: str
      axfr_source:
        description:
          - IPv4 or IPv6 address to be used as the source address for AXFR and IXFR requests.
        type: str
      forward_dnsupdate:
        description:
          - Forward DNSUPDATE requests to one of the zone's masters.
        type: bool
      gss_acceptor_principal:
        description:
          - Kerberos/GSS principal which identifies this server.
        type: str
      gss_allow_axfr_principal:
        description:
          - Kerberos/GSS principal which must be included in AXFR requests.
        type: str
      ixfr:
        description:
          - Attempt IXFR when retrieving zone updates.
        type: bool
      lua_axfr_script:
        description:
          - Script to be used to edit incoming AXFR requests; use 'NONE' to override a globally configured script.
        type: str
      notify_dnsupdate:
        description:
          - Send a NOTIFY to all slave servers after processing a DNSUPDATE request.
        type: bool
      publish_cdnskey:
        description:
          - Publish CDNSKEY records of the KSKs for the zone.
        type: bool
      publish_cds:
        description:
          - List of signature algorithm numbers for CDS records of the KSKs for the zone.
        type: list
        elements: str
      slave_renotify:
        description:
          - Re-send NOTIFY to slaves after receiving AXFR from master.
        type: bool
      soa_edit_dnsupdate:
        description:
          - Method to update the serial number in the SOA record after a DNSUPDATE.
        type: str
        choices: [ 'DEFAULT', 'INCREASE', 'EPOCH', 'SOA-EDIT', 'SOA-EDIT-INCREASE' ]
        default: 'DEFAULT'
      tsig_allow_axfr:
        description:
          - List of TSIG keys for which AXFR requests will be accepted.
        type: list
        elements: str
      tsig_allow_dnsupdate:
        description:
          - List of TSIG keys for which DNSUPDATE requests will be accepted.
        type: list
        elements: str

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
    exists:
      description: Indicate whether the zone exists
      returned: always
      type: bool
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


class Metadata(object):
    map_by_kind = {}
    map_by_prop = {}

    def __init__(self, kind):
        self.kind = kind
        self.prop = kind.lower().replace("-", "_")
        self.map_by_kind[self.kind] = self
        self.map_by_prop[self.prop] = self

    @classmethod
    def by_kind(cls, kind):
        return cls.map_by_kind.get(kind, None)

    @classmethod
    def by_prop(cls, prop):
        return cls.map_by_prop.get(prop, None)

    @classmethod
    def prop_defaults(cls):
        return {k: v.default() for k, v in cls.map_by_prop.items()}


class MetadataBooleanValue(Metadata):
    def default(self):
        return False

    def result_from_api(self, res, api):
        res[self.prop] = api["metadata"][0] != 0


class MetadataBooleanPresence(Metadata):
    def default(self):
        return False

    def result_from_api(self, res, api):
        res[self.prop] = True


class MetadataListValue(Metadata):
    def default(self):
        return []

    def result_from_api(self, res, api):
        res[self.prop] = api["metadata"]


class MetadataStringValue(Metadata):
    def default(self):
        return None

    def result_from_api(self, res, api):
        res[self.prop] = api["metadata"][0]


MetadataListValue("ALLOW-AXFR-FROM")
MetadataListValue("ALLOW-DNSUPDATE-FROM")
MetadataListValue("ALSO-NOTIFY")
MetadataStringValue("AXFR-MASTER-TSIG")
MetadataStringValue("AXFR-SOURCE")
MetadataBooleanPresence("FORWARD-DNSUPDATE")
MetadataStringValue("GSS-ACCEPTOR-PRINCIPAL")
MetadataStringValue("GSS-ALLOW-AXFR-PRINCIPAL")
MetadataBooleanValue("IXFR")
MetadataStringValue("LUA-AXFR-SCRIPT")
MetadataBooleanValue("NOTIFY-DNSUPDATE")
MetadataBooleanValue("PUBLISH-CDNSKEY")
MetadataListValue("PUBLISH-CDS")
MetadataBooleanValue("SLAVE-RENOTIFY")
MetadataStringValue("SOA-EDIT-DNSUPDATE")
MetadataListValue("TSIG-ALLOW-AXFR")
MetadataListValue("TSIG-ALLOW-DNSUPDATE")


def build_zone_result(api, server_id, zone_id):
    z = {}
    zone_info = api.zones.listZone(server_id=server_id, zone_id=zone_id).result()
    z["exists"] = True
    z["name"] = zone_info["name"]
    z["kind"] = zone_info["kind"]
    z["serial"] = zone_info["serial"]
    z["account"] = zone_info["account"]
    z["dnssec"] = zone_info["dnssec"]
    z["masters"] = zone_info["masters"]
    # initialize the metadata result dict
    z["metadata"] = Metadata.prop_defaults()
    z["metadata"]["api_rectify"] = zone_info["api_rectify"]
    z["metadata"]["nsec3narrow"] = zone_info["nsec3narrow"]
    z["metadata"]["nsec3param"] = zone_info["nsec3param"]
    z["metadata"]["soa_edit"] = zone_info["soa_edit"]
    z["metadata"]["soa_edit_api"] = zone_info["soa_edit_api"]

    zone_meta = api.zonemetadata.listMetadata(
        server_id=server_id, zone_id=zone_id
    ).result()
    for m in zone_meta:
        o = Metadata.by_kind(m["kind"])
        if o:
            o.result_from_api(z["metadata"], m)

    return z


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
        "metadata": {
            "type": "dict",
            "options": {
                "allow_axfr_from": {"type": "list", "elements": "str",},
                "allow_dnsupdate_from": {"type": "list", "elements": "str",},
                "also_notify": {"type": "list", "elements": "str",},
                "axfr_master_tsig": {"type": "str",},
                "axfr_source": {"type": "str",},
                "forward_dnsupdate": {"type": "bool",},
                "gss_acceptor_principal": {"type": "str",},
                "gss_allow_axfr_principal": {"type": "str",},
                "ixfr": {"type": "bool",},
                "lua_axfr_script": {"type": "str",},
                "notify_dnsupdate": {"type": "bool",},
                "publish_cndskey": {"type": "bool",},
                "publish_cds": {"type": "list", "elements": "str",},
                "slave_renotify": {"type": "bool",},
                "soa_edit_dnsupdate": {
                    "type": "str",
                    "default": "DEFAULT",
                    "choices": [
                        "DEFAULT",
                        "INCREASE",
                        "EPOCH",
                        "SOA-EDIT",
                        "SOA-EDIT-INCREASE",
                    ],
                },
                "tsig_allow_axfr": {"type": "list", "elements": "str",},
                "tsig_allow_dnsupdate": {"type": "list", "elements": "str",},
            },
        },
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
        # and populate the result dict
        zone_id = zone_info[0]["id"]
        zone_info = api.zones.listZone(server_id=server_id, zone_id=zone_id).result()

        result["zone"] = build_zone_result(api, server_id, zone_id)

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
        zone_info = api.zones.listZones(server_id=server_id, zone=zone).result()
        result["zone"] = build_zone_result(api, server_id, zone_info[0]["id"])
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
            result["zone"] = build_zone_result(api, server_id, zone_id)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
