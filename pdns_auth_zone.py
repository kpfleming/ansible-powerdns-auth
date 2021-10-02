#!/usr/bin/python
# SPDX-FileCopyrightText: 2020 Kevin P. Fleming <kevin@km6g.us>
# SPDX-License-Identifier: Apache-2.0
# -*- coding: utf-8 -*-

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
  api_spec_path:
    description:
      - Path of the OpenAPI (Swagger) API spec document in C(api_url).
      - Ignored when C(api_spec_file) is C(present).
    type: str
    required: false
    default: '/api/docs'
  api_spec_file:
    description:
      - Path to a file containing the OpenAPI (Swagger) specification for the
        API version implemented by the server.
    type: path
    required: false
  api_key:
    description:
      - Key (token) used to authenticate to the API endpoint in the server.
    type: str
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
          - List of nameserver names to be listed in NS records for zone.
            Only used when I(kind=Native) or I(kind=Master).
            Only used when zone is being created (I(state=present) and zone is not present).
          - Must be absolute names (ending with '.').
        type: list
        elements: str
      ttl:
        description:
          - Time to live for SOA and NS records.
            Only used when I(kind=Native) or I(kind=Master).
            Only used when zone is being created (I(state=present) and zone is not present).
        type: int
        required: false
        default: 86400
      soa:
        description:
          - SOA record fields.
            Only used when I(kind=Native) or I(kind=Master).
            Only used when zone is being created (I(state=present) and zone is not present).
        type: complex
        contains:
          mname:
            description:
              - DNS name (absolute, ending with '.') of primary name server for the zone.
            type: str
            required: true
          rname:
            description:
              - Email address of the 'responsible party' for the zone, formatted as a
                DNS name (absolute, ending with '.').
            type: str
            required: true
          serial:
            description:
              - Initial serial number.
            type: int
            required: false
            default: 1
          refresh:
            description:
              - Number of seconds after which secondary name servers should query the primary
                for the SOA record, to detect zone changes.
            type: int
            required: false
            default: 86400
          retry:
            description:
              - Number of seconds after which secondary name servers should retry to request
                the serial number from the primary if the primary does not respond.
              - Must be less than I(refresh).
            type: int
            required: false
            default: 7200
          expire:
            description:
              - Number of seconds after which secondary name servers should stop answering
                requests for this zone if the primary does not respond.
              - Must be bigger than the sum of I(refresh) and I(retry).
            type: int
            required: false
            default: 3600000
          ttl:
            description:
              - Time to live for purposes of negative caching.
            type: int
            required: false
            default: 172800
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
      api_rectify:
        description:
          - Rectify zone's record sets after changes made through the API.
        type: bool
      axfr_source:
        description:
          - IPv4 or IPv6 address to be used as the source address for AXFR and IXFR requests.
        type: str
      axfr_master_tsig:
        description:
          - List of TSIG keys used to validate NOTIFY requests from zone masters and to
            sign AXFR/IXFR requests to zone masters.
          - Note: only the first key in the list will be used.
        type: list
        elements: str
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
      notify_dnsupdate:
        description:
          - Send a NOTIFY to all slave servers after processing a DNSUPDATE request.
        type: bool
      nsec3narrow:
        description:
          - Indicates that this zone operations in NSEC3 'narrow' mode.
        type: bool
      nsec3param:
        description:
          - NSEC3 parameters for the zone when DNSSEC is used.
        type: str
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
          - If this is not set, the 'slave-renotify' setting in the server configuration
            will be applied to the zone.
        type: bool
      soa_edit:
        description:
          - Method to update the serial number in the SOA record when serving it.
        type: str
        choices: [ 'INCREMENT-WEEKS', 'INCEPTION-EPOCH', 'INCEPTION-INCREMENT', 'EPOCH', 'NONE' ]
      soa_edit_api:
        description:
          - Method to update the serial number in the SOA record after an API edit.
        type: str
        choices: [ 'DEFAULT', 'INCREASE', 'EPOCH', 'SOA-EDIT', 'SOA-EDIT-INCREASE' ]
        default: 'DEFAULT'
      soa_edit_dnsupdate:
        description:
          - Method to update the serial number in the SOA record after a DNSUPDATE.
        type: str
        choices: [ 'DEFAULT', 'INCREASE', 'EPOCH', 'SOA-EDIT', 'SOA-EDIT-INCREASE' ]
        default: 'DEFAULT'
      tsig_allow_axfr:
        description:
          - List of TSIG keys used to sign NOTIFY requests and to validate
            AXFR/IXFR requests.
          - Note: only the first key in the list will be used.
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
- name: check that zone exists
  pdns_auth_zone:
    name: d1.example.
    state: exists
    api_key: 'foobar'

- name: check that zone exists on a non-default server
  pdns_auth_zone:
    name: d1.example.
    state: exists
    api_key: 'foobar'
    api_url: 'http://pdns.server.example:80'

- name: send NOTIFY to slave servers for zone
  pdns_auth_zone:
    name: d1.example.
    state: notify
    api_key: 'foobar'

- name: retrieve zone from master server
  pdns_auth_zone:
    name: d1.example.
    state: retrieve
    api_key: 'foobar'

- name: create native zone
  pdns_auth_zone:
    name: d2.example.
    state: present
    api_key: 'foobar'
    properties:
      kind: 'Native'
      nameservers:
        - 'ns1.example.'
      soa:
        mname: 'localhost.'
        rname: 'hostmaster.localhost.'
    metadata:
      allow_axfr_from: ['AUTO-NS']
      axfr_source: '127.0.0.1'

- name: change native zone to master
  pdns_auth_zone:
    name: d2.example.
    state: present
    api_key: 'foobar'
    properties:
      kind: 'Master'

- name: delete zone
  pdns_auth_zone:
    name: d2.example.
    state: absent
    api_key: 'foobar'

- name: create slave zone
  pdns_auth_zone:
    name: d3.example.
    state: present
    api_key: 'foobar'
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
        api_rectify:
          description:
            - Rectify zone's record sets after changes made through the API.
          type: bool
        axfr_master_tsig:
          description:
            - List of TSIG keys used to validate NOTIFY requests from zone masters and to
              sign AXFR/IXFR requests to zone masters.
          type: list
          elements: str
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
        nsec3narrow:
          description:
            - Indicates that this zone operations in NSEC3 'narrow' mode.
          type: bool
        nsec3param:
          description:
            - NSEC3 parameters for the zone when DNSSEC is used.
          type: str
        publish_cdnskey:
          description:
            - Publish CDNSKEY records of the KSKs for the zone.
          type: bool
        publish_cds:
          description:
            - List of signature algorithm numbers for CDS records of the KSKs for the zone.
          type: list
          elements: str
        presigned:
          description:
            - Indicates that this zone zone carries DNSSEC RRSIGs, and is presigned.
          type: bool
        slave_renotify:
          description:
            - Re-send NOTIFY to slaves after receiving AXFR from master.
          type: bool
        soa_edit:
          description:
            - Method to update the serial number in the SOA record when serving it.
          type: str
          choices: [ 'INCREMENT-WEEKS', 'INCEPTION-EPOCH', 'INCEPTION-INCREMENT', 'EPOCH', 'NONE' ]
        soa_edit_api:
          description:
            - Method to update the serial number in the SOA record after an API edit.
          type: str
          choices: [ 'DEFAULT', 'INCREASE', 'EPOCH', 'SOA-EDIT', 'SOA-EDIT-INCREASE' ]
        soa_edit_dnsupdate:
          description:
            - Method to update the serial number in the SOA record after a DNSUPDATE.
          type: str
          choices: [ 'DEFAULT', 'INCREASE', 'EPOCH', 'SOA-EDIT', 'SOA-EDIT-INCREASE' ]
        tsig_allow_axfr:
          description:
            - List of TSIG keys used to sign NOTIFY requests and to validate
              AXFR/IXFR requests.
          type: list
          elements: str
        tsig_allow_dnsupdate:
          description:
            - List of TSIG keys for which DNSUPDATE requests will be accepted.
          type: list
          elements: str
"""

import sys

assert sys.version_info >= (3, 8), "This module requires Python 3.8 or newer."

from ansible.module_utils.basic import AnsibleModule

from urllib.parse import urlparse
from functools import wraps


module = None
result = None
api_exceptions_to_catch = ()


def APIExceptionHandler(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except api_exceptions_to_catch as e:
            module.fail_json(
                msg=f"API operation {func.__name__} returned '{e.swagger_result['error']}'",
                **result,
            )

    return wrapper


class APIZonesWrapper(object):
    def __init__(self, raw_api, server_id, zone_id):
        self.raw_api = raw_api
        self.server_id = server_id
        self.zone_id = zone_id

    @APIExceptionHandler
    def axfrRetrieveZone(self):
        return self.raw_api.axfrRetrieveZone(
            server_id=self.server_id, zone_id=self.zone_id
        ).result()

    @APIExceptionHandler
    def createZone(self, **kwargs):
        return self.raw_api.createZone(
            server_id=self.server_id, rrsets=False, **kwargs
        ).result()

    @APIExceptionHandler
    def deleteZone(self):
        return self.raw_api.deleteZone(
            server_id=self.server_id, zone_id=self.zone_id
        ).result()

    @APIExceptionHandler
    def listZone(self):
        return self.raw_api.listZone(
            server_id=self.server_id, zone_id=self.zone_id, rrsets=False
        ).result()

    @APIExceptionHandler
    def listZones(self, **kwargs):
        return self.raw_api.listZones(server_id=self.server_id, **kwargs).result()

    @APIExceptionHandler
    def notifyZone(self):
        return self.raw_api.notifyZone(
            server_id=self.server_id, zone_id=self.zone_id
        ).result()

    @APIExceptionHandler
    def putZone(self, **kwargs):
        return self.raw_api.putZone(
            server_id=self.server_id, zone_id=self.zone_id, **kwargs
        ).result()


class APIZoneMetadataWrapper(object):
    def __init__(self, raw_api, server_id, zone_id):
        self.raw_api = raw_api
        self.server_id = server_id
        self.zone_id = zone_id

    @APIExceptionHandler
    def deleteMetadata(self, **kwargs):
        return self.raw_api.deleteMetadata(
            server_id=self.server_id, zone_id=self.zone_id, **kwargs
        ).result()

    @APIExceptionHandler
    def listMetadata(self):
        return self.raw_api.listMetadata(
            server_id=self.server_id, zone_id=self.zone_id
        ).result()

    @APIExceptionHandler
    def modifyMetadata(self, **kwargs):
        return self.raw_api.modifyMetadata(
            server_id=self.server_id, zone_id=self.zone_id, **kwargs
        ).result()


class APIWrapper(object):
    def __init__(self, raw_api, server_id, zone_id):
        self.zones = APIZonesWrapper(raw_api.zones, server_id, zone_id)
        self.zonemetadata = APIZoneMetadataWrapper(
            raw_api.zonemetadata, server_id, zone_id
        )

    def setZoneID(self, zone_id):
        self.zones.zone_id = zone_id
        self.zonemetadata.zone_id = zone_id


class Metadata(object):
    map_by_api_kind = {}
    map_by_meta = {}

    def __init__(self, api_kind):
        self.api_kind = api_kind
        self.meta = api_kind.lower().replace("-", "_")
        self.immutable = False
        self.map_by_api_kind[self.api_kind] = self
        self.map_by_meta[self.meta] = self

    @classmethod
    def by_kind(cls, api_kind):
        return cls.map_by_api_kind.get(api_kind)

    @classmethod
    def by_meta(cls, meta):
        return cls.map_by_meta.get(meta)

    @classmethod
    def meta_defaults(cls):
        return {k: v.default() for k, v in cls.map_by_meta.items()}

    @classmethod
    def user_meta_from_api(cls, api_meta):
        user_meta = cls.meta_defaults()

        for k, v in {m["kind"]: m["metadata"] for m in api_meta}.items():
            meta_object = cls.by_kind(k)
            if meta_object:
                meta_object.user_meta_from_api(user_meta, v)

        return user_meta

    @classmethod
    def setters(cls, user_meta):
        res = []

        for meta, value in user_meta.items():
            m = cls.by_meta(meta)
            if m and not m.immutable:
                res.append(
                    lambda api_client, m=m, value=value: m.set(
                        value or m.default(), api_client
                    )
                )

        return res

    @classmethod
    def updaters(cls, old_user_meta, new_user_meta):
        res = []

        for k, v in cls.map_by_meta.items():
            if not v.immutable:
                res.append(
                    lambda api_client, k=k, v=v: v.update(
                        old_user_meta.get(k),
                        new_user_meta.get(k) or v.default(),
                        api_client,
                    )
                )

        return res


class MetadataBinaryValue(Metadata):
    def default(self):
        return False

    def user_meta_from_api(self, user_meta, api_meta_item):
        user_meta[self.meta] = api_meta_item[0] == "1"

    def set(self, value, api_client):
        if value:
            api_client.zonemetadata.modifyMetadata(
                metadata_kind=self.api_kind, metadata={"metadata": ["1"]}
            )

    def update(self, oldval, newval, api_client):
        if newval == oldval:
            return False

        if newval:
            api_client.zonemetadata.modifyMetadata(
                metadata_kind=self.api_kind, metadata={"metadata": ["1"]}
            )
        else:
            api_client.zonemetadata.deleteMetadata(metadata_kind=self.api_kind)
        return True


class MetadataBinaryPresence(Metadata):
    def default(self):
        return False

    def user_meta_from_api(self, user_meta, api_meta_item):
        user_meta[self.meta] = True

    def set(self, value, api_client):
        if value:
            api_client.zonemetadata.modifyMetadata(
                metadata_kind=self.api_kind, metadata={"metadata": [""]}
            )

    def update(self, oldval, newval, api_client):
        if newval == oldval:
            return False

        if newval:
            api_client.zonemetadata.modifyMetadata(
                metadata_kind=self.api_kind, metadata={"metadata": [""]}
            )
        else:
            api_client.zonemetadata.deleteMetadata(metadata_kind=self.api_kind)
        return True


class MetadataTernaryValue(Metadata):
    def default(self):
        return None

    def user_meta_from_api(self, user_meta, api_meta_item):
        user_meta[self.meta] = api_meta_item[0] == "1"

    def set(self, value, api_client):
        if value is not None:
            if value:
                api_client.zonemetadata.modifyMetadata(
                    metadata_kind=self.api_kind, metadata={"metadata": ["1"]}
                )
            else:
                api_client.zonemetadata.modifyMetadata(
                    metadata_kind=self.api_kind, metadata={"metadata": ["0"]}
                )

    def update(self, oldval, newval, api_client):
        if newval == oldval:
            return False

        if newval is not None:
            if newval:
                api_client.zonemetadata.modifyMetadata(
                    metadata_kind=self.api_kind, metadata={"metadata": ["1"]}
                )
            else:
                api_client.zonemetadata.modifyMetadata(
                    metadata_kind=self.api_kind, metadata={"metadata": ["0"]}
                )
        else:
            api_client.zonemetadata.deleteMetadata(metadata_kind=self.api_kind)
        return True


class MetadataListValue(Metadata):
    def default(self):
        return []

    def user_meta_from_api(self, user_meta, api_meta_item):
        user_meta[self.meta] = api_meta_item

    def set(self, value, api_client):
        if len(value) != 0:
            api_client.zonemetadata.modifyMetadata(
                metadata_kind=self.api_kind, metadata={"metadata": value}
            )

    def update(self, oldval, newval, api_client):
        if newval == oldval:
            return False

        if len(newval) != 0:
            api_client.zonemetadata.modifyMetadata(
                metadata_kind=self.api_kind, metadata={"metadata": newval}
            )
        else:
            api_client.zonemetadata.deleteMetadata(metadata_kind=self.api_kind)
        return True


class MetadataStringValue(Metadata):
    def default(self):
        return ""

    def user_meta_from_api(self, user_meta, api_meta_item):
        user_meta[self.meta] = api_meta_item[0]

    def set(self, value, api_client):
        if value:
            api_client.zonemetadata.modifyMetadata(
                metadata_kind=self.api_kind, metadata={"metadata": [value]}
            )

    def update(self, oldval, newval, api_client):
        if newval == oldval:
            return False

        if len(newval) != 0:
            api_client.zonemetadata.modifyMetadata(
                metadata_kind=self.api_kind, metadata={"metadata": [newval]}
            )
        else:
            api_client.zonemetadata.deleteMetadata(metadata_kind=self.api_kind)
        return True


class ZoneMetadata(object):
    map_by_zone_kind = {}
    map_by_meta = {}

    def __init__(self, api_kind, zone_kind):
        self.zone_kind = zone_kind
        self.meta = api_kind.lower().replace("-", "_")
        self.immutable = False
        self.map_by_zone_kind[self.zone_kind] = self
        self.map_by_meta[self.meta] = self

    @classmethod
    def by_kind(cls, zone_kind):
        return cls.map_by_zone_kind.get(zone_kind)

    @classmethod
    def by_meta(cls, meta):
        return cls.map_by_meta.get(meta)

    @classmethod
    def meta_defaults(cls):
        return {k: v.default() for k, v in cls.map_by_meta.items()}

    @classmethod
    def user_meta_from_api(cls, api_zone):
        user_meta = cls.meta_defaults()

        for k, v in api_zone.items():
            meta_object = cls.by_kind(k)
            if meta_object:
                meta_object.user_meta_from_api(user_meta, v)

        return user_meta

    @classmethod
    def setters(cls, user_meta):
        res = []

        for meta, value in user_meta.items():
            m = cls.by_meta(meta)
            if m and not m.immutable:
                res.append(
                    lambda zone_struct, m=m, value=value: m.set(
                        value or m.default(), zone_struct
                    )
                )

        return res

    @classmethod
    def updaters(cls, old_user_meta, new_user_meta):
        res = []

        for k, v in cls.map_by_meta.items():
            if not v.immutable:
                res.append(
                    lambda zone_struct, k=k, v=v: v.update(
                        old_user_meta.get(k),
                        new_user_meta.get(k) or v.default(),
                        zone_struct,
                    )
                )

        return res


class ZoneMetadataBinaryValue(ZoneMetadata):
    def default(self):
        return False

    def user_meta_from_api(self, user_meta, zone_meta_item):
        user_meta[self.meta] = zone_meta_item == "1"

    def set(self, value, zone_struct):
        if value:
            zone_struct[self.zone_kind] = "1"

    def update(self, oldval, newval, zone_struct):
        if newval != oldval:
            if newval:
                zone_struct[self.zone_kind] = "1"
            else:
                zone_struct[self.zone_kind] = "0"


class ZoneMetadataTernaryValue(ZoneMetadata):
    def default(self):
        return None

    def user_meta_from_api(self, user_meta, zone_meta_item):
        user_meta[self.meta] = zone_meta_item == "1"

    def set(self, value, zone_struct):
        if value is not None:
            if value:
                zone_struct[self.zone_kind] = "1"
            else:
                zone_struct[self.zone_kind] = "0"

    def update(self, oldval, newval, zone_struct):
        if newval != oldval:
            if newval is not None:
                if newval:
                    zone_struct[self.zone_kind] = "1"
                else:
                    zone_struct[self.zone_kind] = "0"
            else:
                zone_struct[self.zone_kind] = ""


class ZoneMetadataListValue(ZoneMetadata):
    def default(self):
        return []

    def user_meta_from_api(self, user_meta, zone_meta_item):
        user_meta[self.meta] = zone_meta_item

    def set(self, value, zone_struct):
        if value != []:
            zone_struct[self.zone_kind] = value

    def update(self, oldval, newval, zone_struct):
        if newval != oldval:
            zone_struct[self.zone_kind] = newval


class ZoneMetadataStringValue(ZoneMetadata):
    def default(self):
        return ""

    def user_meta_from_api(self, user_meta, zone_meta_item):
        user_meta[self.meta] = zone_meta_item

    def set(self, value, zone_struct):
        if value != "":
            zone_struct[self.zone_kind] = value

    def update(self, oldval, newval, zone_struct):
        if newval != oldval:
            zone_struct[self.zone_kind] = newval


MetadataListValue("ALLOW-DNSUPDATE-FROM")
MetadataListValue("ALLOW-AXFR-FROM")
MetadataListValue("ALSO-NOTIFY")
MetadataStringValue("AXFR-SOURCE")
MetadataBinaryPresence("FORWARD-DNSUPDATE")
MetadataStringValue("GSS-ACCEPTOR-PRINCIPAL")
MetadataStringValue("GSS-ALLOW-AXFR-PRINCIPAL")
MetadataBinaryValue("IXFR")
MetadataStringValue("LUA-AXFR-SCRIPT").immutable = True
MetadataBinaryValue("NOTIFY-DNSUPDATE")
MetadataBinaryValue("PUBLISH-CDNSKEY")
MetadataListValue("PUBLISH-CDS")
MetadataTernaryValue("SLAVE-RENOTIFY")
MetadataStringValue("SOA-EDIT-DNSUPDATE")
MetadataListValue("TSIG-ALLOW-DNSUPDATE")

ZoneMetadataBinaryValue("API-RECTIFY", "api_rectify")
ZoneMetadataListValue("AXFR-MASTER-TSIG", "slave_tsig_key_ids")
ZoneMetadataBinaryValue("NSEC3NARROW", "nsec3narrow")
ZoneMetadataStringValue("NSEC3PARAM", "nsec3param")
ZoneMetadataBinaryValue("PRESIGNED", "presigned").immutable = True
ZoneMetadataStringValue("SOA-EDIT", "soa_edit")
ZoneMetadataStringValue("SOA-EDIT-API", "soa_edit_api")
ZoneMetadataListValue("TSIG-ALLOW-AXFR", "master_tsig_key_ids")


def build_zone_result(api_client):
    api_zone = api_client.zones.listZone()
    api_meta = api_client.zonemetadata.listMetadata()
    z = {
        "exists": True,
        "name": api_zone["name"],
        "kind": api_zone["kind"],
        "serial": api_zone["serial"],
        "account": api_zone["account"],
        "dnssec": api_zone["dnssec"],
        "masters": api_zone["masters"],
        "metadata": {
            **Metadata.user_meta_from_api(api_meta),
            **ZoneMetadata.user_meta_from_api(api_zone),
        },
    }

    return api_zone, z


def main():
    module_args = {
        "state": {
            "type": "str",
            "default": "present",
            "choices": ["present", "absent", "exists", "notify", "retrieve"],
        },
        "name": {
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
        "api_spec_file": {
            "type": "path",
        },
        "api_key": {
            "type": "str",
            "required": True,
            "no_log": True,
        },
        "properties": {
            "type": "dict",
            "options": {
                "kind": {
                    "type": "str",
                    "choices": ["Native", "Master", "Slave"],
                    "required": True,
                },
                "account": {
                    "type": "str",
                },
                "nameservers": {
                    "type": "list",
                    "elements": "str",
                },
                "ttl": {
                    "type": "int",
                    "default": 86400,
                },
                "soa": {
                    "type": "dict",
                    "options": {
                        "mname": {
                            "type": "str",
                            "required": True,
                        },
                        "rname": {
                            "type": "str",
                            "required": True,
                        },
                        "serial": {
                            "type": "int",
                            "default": 1,
                        },
                        "refresh": {
                            "type": "int",
                            "default": 86400,
                        },
                        "retry": {
                            "type": "int",
                            "default": 7200,
                        },
                        "expire": {
                            "type": "int",
                            "default": 3600000,
                        },
                        "ttl": {
                            "type": "int",
                            "default": 172800,
                        },
                    },
                },
                "masters": {
                    "type": "list",
                    "elements": "str",
                },
            },
        },
        "metadata": {
            "type": "dict",
            "options": {
                "allow_axfr_from": {
                    "type": "list",
                    "elements": "str",
                },
                "allow_dnsupdate_from": {
                    "type": "list",
                    "elements": "str",
                },
                "also_notify": {
                    "type": "list",
                    "elements": "str",
                },
                "api_rectify": {
                    "type": "bool",
                },
                "axfr_source": {
                    "type": "str",
                },
                "axfr_master_tsig": {
                    "type": "list",
                    "elements": "str",
                },
                "forward_dnsupdate": {
                    "type": "bool",
                },
                "gss_acceptor_principal": {
                    "type": "str",
                },
                "gss_allow_axfr_principal": {
                    "type": "str",
                },
                "ixfr": {
                    "type": "bool",
                },
                "notify_dnsupdate": {
                    "type": "bool",
                },
                "nsec3narrow": {
                    "type": "bool",
                },
                "nsec3param": {
                    "type": "str",
                },
                "publish_cdnskey": {
                    "type": "bool",
                },
                "publish_cds": {
                    "type": "list",
                    "elements": "str",
                },
                "slave_renotify": {
                    "type": "bool",
                },
                "soa_edit": {
                    "type": "str",
                    "choices": [
                        "INCREMENT-WEEKS",
                        "INCEPTION-EPOCH",
                        "INCEPTION-INCREMENT",
                        "EPOCH",
                        "NONE",
                    ],
                },
                "soa_edit_api": {
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
                "tsig_allow_axfr": {
                    "type": "list",
                    "elements": "str",
                },
                "tsig_allow_dnsupdate": {
                    "type": "list",
                    "elements": "str",
                },
            },
        },
    }

    global module
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    try:
        from bravado.requests_client import RequestsClient
        from bravado.client import SwaggerClient
        from bravado.swagger_model import load_file
        from bravado.exception import (
            HTTPBadRequest,
            HTTPNotFound,
            HTTPConflict,
            HTTPUnprocessableEntity,
            HTTPInternalServerError,
        )
    except ImportError:
        module.fail_json(
            msg="The pdns_auth_zone module requires the 'bravado' package."
        )

    global api_exceptions_to_catch
    api_exceptions_to_catch = (
        HTTPBadRequest,
        HTTPNotFound,
        HTTPConflict,
        HTTPUnprocessableEntity,
        HTTPInternalServerError,
    )

    global result
    result = {
        "changed": False,
    }

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

    if module.params["api_spec_file"]:
        spec = load_file(module.params["api_spec_file"])
        spec["host"] = url.netloc
        spec["schemes"] = [url.scheme]

        raw_api = SwaggerClient.from_spec(spec, http_client=http_client)
    else:
        raw_api = SwaggerClient.from_url(
            module.params["api_url"] + module.params["api_spec_path"],
            http_client=http_client,
            request_headers={
                "Accept": "application/json",
                "X-API-Key": module.params["api_key"],
            },
        )

    # create an APIWrapper to proxy the raw_api object
    # and curry the server_id and zone_id into all API
    # calls automatically, along with handling
    # predictable exceptions
    api_client = APIWrapper(raw_api, server_id, None)

    result["zone"] = {}
    result["zone"]["name"] = zone
    result["zone"]["exists"] = False

    # first step is to get information about the zone, if it exists
    # this is required to translate the user-friendly zone name into
    # the zone_id required for subsequent API calls

    partial_zone_info = api_client.zones.listZones(zone=zone)

    if len(partial_zone_info) == 0:
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
        #
        # get the full zone info and populate the result dict
        zone_id = partial_zone_info[0]["id"]
        api_client.setZoneID(zone_id)
        zone_info, result["zone"] = build_zone_result(api_client)

    # if only an existence check was requested,
    # the operation is complete
    if state == "exists":
        module.exit_json(**result)

    # if absence was requested, remove the zone and exit
    if state == "absent":
        api_client.zones.deleteZone()
        result["changed"] = True
        module.exit_json(**result)

    # if NOTIFY was requested, process it and exit
    if state == "notify":
        if zone_info["kind"] == "Native":
            module.fail_json(
                msg="NOTIFY cannot be requested for 'Native' zones", **result
            )

        api_client.zones.notifyZone()
        result["changed"] = True
        module.exit_json(**result)

    # if retrieval was requested, process it and exit
    if state == "retrieve":
        if zone_info["kind"] != "Slave":
            module.fail_json(
                msg="Retrieval can only be requested for 'Slave' zones", **result
            )

        api_client.zones.axfrRetrieveZone()
        result["changed"] = True
        module.exit_json(**result)

    # state must be 'present'
    if not zone_id:
        # create the requested zone
        zone_struct = {
            "name": zone,
        }

        if not module.params["properties"]:
            module.fail_json(
                msg="'properties' must be specified for zone creation", **result
            )

        props = module.params["properties"]

        zone_struct["kind"] = props["kind"]

        if props["kind"] != "Slave":
            if not props["soa"]:
                module.fail_json(
                    msg="'properties -> soa' must be specified for zone creation",
                    **result,
                )

            # supply an empty nameserver list since NS records will be supplied in the rrsets
            zone_struct["nameservers"] = []

            zone_struct["rrsets"] = [
                {
                    "name": zone,
                    "type": "SOA",
                    "ttl": str(props["ttl"]),
                    "records": [
                        {
                            "disabled": False,
                            "content": " ".join(
                                [
                                    props["soa"]["mname"],
                                    props["soa"]["rname"],
                                    str(props["soa"]["serial"]),
                                    str(props["soa"]["refresh"]),
                                    str(props["soa"]["retry"]),
                                    str(props["soa"]["expire"]),
                                    str(props["soa"]["ttl"]),
                                ]
                            ),
                        },
                    ],
                },
                {
                    "name": zone,
                    "type": "NS",
                    "ttl": str(props["ttl"]),
                    "records": [
                        {"disabled": False, "content": ns}
                        for ns in props["nameservers"]
                    ],
                },
            ]

        if props["kind"] == "Slave":
            zone_struct["masters"] = props["masters"]

        if props["account"]:
            zone_struct["account"] = props["account"]

        if module.params["metadata"]:
            for setter in ZoneMetadata.setters(module.params["metadata"]):
                setter(zone_struct)

        partial_zone_info = api_client.zones.createZone(zone_struct=zone_struct)

        result["changed"] = True
        api_client.setZoneID(partial_zone_info["id"])

        if module.params["metadata"]:
            for setter in Metadata.setters(module.params["metadata"]):
                setter(api_client)

        zone_info, result["zone"] = build_zone_result(api_client)
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
                        mp_masters = sorted(props["masters"])
                        zi_masters = sorted(zone_info["masters"])

                        if zi_masters != mp_masters:
                            zone_struct["masters"] = props["masters"]

            if props["account"]:
                if zone_info["account"] != props["account"]:
                    zone_struct["account"] = props["account"]

        if module.params["metadata"]:
            for updater in ZoneMetadata.updaters(
                result["zone"]["metadata"], module.params["metadata"]
            ):
                updater(zone_struct)

        if len(zone_struct):
            api_client.zones.putZone(zone_struct=zone_struct)
            result["changed"] = True

        if module.params["metadata"]:
            for updater in Metadata.updaters(
                result["zone"]["metadata"], module.params["metadata"]
            ):
                if updater(api_client):
                    result["changed"] = True

        if result["changed"]:
            zone_info, result["zone"] = build_zone_result(api_client)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
