#!/usr/bin/python
# SPDX-FileCopyrightText: 2025 Mohamed Chamrouk <mohamed.chamrouk@proton.me>
# SPDX-License-Identifier: Apache-2.0
# -*- coding: utf-8 -*-

import sys

from ansible.module_utils.basic import AnsibleModule

from ..module_utils.api_module_args import API_MODULE_ARGS
from ..module_utils.api_wrapper import APIZoneWrapper

assert sys.version_info >= (3, 9), "This module requires Python 3.9 or newer."

DOCUMENTATION = """
%YAML 1.2
---
module: powerdns_auth_rrset

short_description: Manages an RRset in a zone of PowerDNS Authoritative server

description:
  - This module can create, delete or update an RRset inside a zone of
    PowerDNS Authoritative server.

requirements:
  - bravado

extends_documentation_fragment:
  - kpfleming.powerdns_auth.api_details

options:
  state:
    description:
      - If V(present) the RRset will be created unless it already exists
        in which case if O(keep=false) records will be replaces and if
        O(keep=true) new RRs will be added.
      - If V(absent) and O(keep=false) the whole RRset will be deleted
      - If V(absent) and O(keep=true) only the matching RRs will be
        deleted
      - If V(exists) a list of all RRsets in the zone will be returned
      - If V(exists) and O(name) and/or O(type) existence will be checked
        and matching RRsets will be returned
    choices: [ 'present', 'absent', 'exists' ]
    type: str
    required: false
    default: 'present'
  name:
    description:
      - Name of the RRset
      - Required if O(state=present) or O(state=absent)
    type: str
  zone_name:
    description:
      - Name of the zone
    type: str
    required: true
  keep:
    description:
      - Whether or not to keep existing records.
    type: bool
    default: false
  ttl:
    description:
      - TTL of the records, in seconds.
    type: int
    default: 3600
  type:
    description:
      - Type of resource record (e.g. A, PTR, NSEC...).
      - Required if O(state=absent) or O(state=present) and none of the RR types options are
        provided.
    type: str
  records:
    description:
      - Represents a list of records.
      - Required if O(type) and O(state=present).
    type: list
    elements: dict
    suboptions:
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false
      content:
        description:
          - The content of the RR.
        type: str
        required: true
  A:
    description:
      - RR of type A.
      - Required if O(state=present) or O(state=absent) and O(type) and O(records)
        and any of the other RR type option is not present.
    type: list
    elements: dict
    suboptions:
      address:
        description:
          - IPv4 address.
        type: str
        required: true
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false
  AAAA:
    description:
      - RR of type AAAA.
      - Required if O(state=present) or O(state=absent) and O(type) and O(records)
        and any of the other RR type option is not present.
    type: list
    elements: dict
    suboptions:
      address:
        description:
          - IPv6 address.
        type: str
        required: true
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false
  CAA:
    description:
      - Certificate Authority Authorization RR.
      - Required if O(state=present) or O(state=absent) and O(type) and O(records)
        and any of the other RR type option not present.
    type: list
    elements: dict
    suboptions:
      flags:
        description:
          - Critical flag for CAA record.
        type: int
        default: 0
        choices: [0, 1]
      tag:
        description:
          - Property tag for CAA record.
        type: str
        required: true
        choices: ["issue", "issuewild", "iodef"]
      value:
        description:
          - Property value for CAA record.
        type: raw
        required: true
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false
  CNAME:
    description:
      - Canonical name RR.
      - Required if O(state=present) or O(state=absent) and O(type) and O(records)
        and any of the other RR type option not present.
    type: list
    elements: dict
    suboptions:
      cname:
        description:
          - Canonical domain name.
        type: str
        required: true
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false
  DNSKEY:
    description:
      - DNS Key RR for DNSSEC.
      - Required if O(state=present) or O(state=absent) and O(type) and O(records)
        and any of the other RR type option not present.
    type: list
    elements: dict
    suboptions:
      flags:
        description:
          - Key flags field.
        type: int
        required: true
        choices: [256, 257]
      protocol:
        description:
          - Protocol field.
        type: int
        required: true
        choices: [3]
      algorithm:
        description:
          - Algorithm used for the key.
        type: int
        required: true
      public_key:
        description:
          - Base64 encoded public key.
        type: str
        required: true
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false
  DS:
    description:
      - Delegation Signer RR for DNSSEC.
      - Required if O(state=present) or O(state=absent) and O(type) and O(records)
        and any of the other RR type option not present.
    type: list
    elements: dict
    suboptions:
      key_tag:
        description:
          - Key tag field.
        type: int
        required: true
      algorithm:
        description:
          - Algorithm used for signing.
        type: int
        required: true
      digest_type:
        description:
          - Digest algorithm type.
        type: int
        required: true
        choices: [1, 2, 3, 4]
      digest:
        description:
          - Digest value.
        type: str
        required: true
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false
  HINFO:
    description:
      - Host information RR.
      - Required if O(state=present) or O(state=absent) and O(type) and O(records)
        and any of the other RR type option not present.
    type: list
    elements: dict
    suboptions:
      cpu:
        description:
          - CPU type.
        type: raw
        required: true
      os:
        description:
          - Operating system.
        type: raw
        required: true
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false
  HTTPS:
    description:
      - HTTPS service binding RR.
      - Required if O(state=present) or O(state=absent) and O(type) and O(records)
        and any of the other RR type option not present.
    type: list
    elements: dict
    suboptions:
      priority:
        description:
          - Priority of the target host.
        type: int
        required: true
      target:
        description:
          - Target hostname.
        type: str
        required: true
      params:
        description:
          - Service parameters.
        type: str
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false
  LOC:
    description:
      - Location RR.
      - Required if O(state=present) or O(state=absent) and O(type) and O(records)
        and any of the other RR type option not present.
    type: list
    elements: dict
    suboptions:
      latitude:
        description:
          - Latitude coordinate.
        type: str
        required: true
      longitude:
        description:
          - Longitude coordinate.
        type: str
        required: true
      altitude:
        description:
          - Altitude coordinate.
        type: str
        required: true
      size:
        description:
          - Size of the location.
        type: str
        default: "1.0m"
      horizontal_precision:
        description:
          - Horizontal precision.
        type: str
        default: "10000.0m"
      vertical_precision:
        description:
          - Vertical precision.
        type: str
        default: "10.0m"
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false
  MX:
    description:
      - Mail exchange RR.
      - Required if O(state=present) or O(state=absent) and O(type) and O(records)
        and any of the other RR type option not present.
    type: list
    elements: dict
    suboptions:
      preference:
        description:
          - Priority preference for mail delivery.
        type: int
        required: true
      exchange:
        description:
          - Mail server hostname.
        type: str
        required: true
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false
  NAPTR:
    description:
      - Name Authority Pointer RR.
      - Required if O(state=present) or O(state=absent) and O(type) and O(records)
        and any of the other RR type option not present.
    type: list
    elements: dict
    suboptions:
      order:
        description:
          - Order field for processing records.
        type: int
        required: true
      preference:
        description:
          - Preference field for records with same order.
        type: int
        required: true
      flags:
        description:
          - Flags field.
        type: raw
        required: true
      services:
        description:
          - Services field.
        type: raw
        required: true
      regexp:
        description:
          - Regular expression for substitution.
        type: raw
        required: true
      replacement:
        description:
          - Replacement domain name.
        type: str
        required: true
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false
  NS:
    description:
      - Name server RR.
      - Required if O(state=present) or O(state=absent) and O(type) and O(records)
        and any of the other RR type option not present.
    type: list
    elements: dict
    suboptions:
      host:
        description:
          - Name server hostname.
        type: str
        required: true
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false
  NSEC:
    description:
      - Next Secure RR for DNSSEC.
      - Required if O(state=present) or O(state=absent) and O(type) and O(records)
        and any of the other RR type option not present.
    type: list
    elements: dict
    suboptions:
      next_domain:
        description:
          - Next domain name in canonical order.
        type: str
        required: true
      type_bitmap:
        description:
          - Bitmap of record types present.
        type: str
        required: true
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false
  NSEC3PARAM:
    description:
      - NSEC3 parameters RR for DNSSEC.
      - Required if O(state=present) or O(state=absent) and O(type) and O(records)
        and any of the other RR type option not present.
    type: list
    elements: dict
    suboptions:
      hash_algorithm:
        description:
          - Hash algorithm used.
        type: int
        required: true
        choices: [1]
      flags:
        description:
          - Flags field.
        type: int
        required: true
        choices: [0, 1]
      iterations:
        description:
          - Number of hash iterations.
        type: int
        required: true
      salt:
        description:
          - Salt value for hashing.
        type: str
        required: true
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false
  PTR:
    description:
      - Pointer RR for reverse DNS lookup.
      - Required if O(state=present) or O(state=absent) and O(type) and O(records)
        and any of the other RR type option not present.
    type: list
    elements: dict
    suboptions:
      ptrdname:
        description:
          - Domain name for reverse lookup.
        type: str
        required: true
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false
  RP:
    description:
      - Responsible person RR.
      - Required if O(state=present) or O(state=absent) and O(type) and O(records)
        and any of the other RR type option not present.
    type: list
    elements: dict
    suboptions:
      mbox:
        description:
          - Mailbox domain name of responsible person.
        type: str
        required: true
      txt:
        description:
          - Domain name for TXT record with contact info.
        type: str
        required: true
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false
  SPF:
    description:
      - Sender Policy Framework RR.
      - Required if O(state=present) or O(state=absent) and O(type) and O(records)
        and any of the other RR type option not present.
    type: list
    elements: dict
    suboptions:
      strings:
        description:
          - SPF policy strings.
        type: raw
        required: true
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false
  SOA:
    description:
      - Start of Authority RR.
      - Required if O(state=present) or O(state=absent) and O(type) and O(records)
        and any of the other RR type option not present.
    type: list
    elements: dict
    suboptions:
      mname:
        description:
          - Primary master name server.
        type: str
        required: true
      rname:
        description:
          - Email address of zone administrator.
        type: str
        required: true
      serial:
        description:
          - Serial number of the zone.
        type: int
      refresh:
        description:
          - Refresh interval in seconds.
        type: int
      retry:
        description:
          - Retry interval in seconds.
        type: int
      expire:
        description:
          - Expire time in seconds.
        type: int
      minimum:
        description:
          - Minimum TTL in seconds.
        type: int
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false
  SRV:
    description:
      - Service RR.
      - Required if O(state=present) or O(state=absent) and O(type) and O(records)
        and any of the other RR type option not present.
    type: list
    elements: dict
    suboptions:
      priority:
        description:
          - Priority of the target host.
        type: int
        required: true
      weight:
        description:
          - Relative weight for records with same priority.
        type: int
        required: true
      port:
        description:
          - TCP or UDP port number.
        type: int
        required: true
      target:
        description:
          - Target hostname.
        type: str
        required: true
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false
  SSHFP:
    description:
      - SSH fingerprint RR.
      - Required if O(state=present) or O(state=absent) and O(type) and O(records)
        and any of the other RR type option not present.
    type: list
    elements: dict
    suboptions:
      algorithm:
        description:
          - SSH key algorithm.
        type: int
        required: true
        choices: [1, 2, 3, 4, 6]
      fp_type:
        description:
          - Fingerprint type.
        type: int
        required: true
        choices: [1, 2, 3]
      fingerprint:
        description:
          - SSH key fingerprint.
        type: str
        required: true
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false
  SVCB:
    description:
      - Service binding RR.
      - Required if O(state=present) or O(state=absent) and O(type) and O(records)
        and any of the other RR type option not present.
    type: list
    elements: dict
    suboptions:
      priority:
        description:
          - Priority of the target host.
        type: int
        required: true
      target:
        description:
          - Target hostname.
        type: str
        required: true
      params:
        description:
          - Service parameters.
        type: str
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false
  TLSA:
    description:
      - Transport Layer Security Authentication RR.
      - Required if O(state=present) or O(state=absent) and O(type) and O(records)
        and any of the other RR type option not present.
    type: list
    elements: dict
    suboptions:
      usage:
        description:
          - Certificate usage.
        type: int
        required: true
        choices: [0, 1, 2, 3]
      selector:
        description:
          - Selector field.
        type: int
        required: true
        choices: [0, 1]
      matching_type:
        description:
          - Matching type.
        type: int
        required: true
        choices: [0, 1, 2]
      cert_assoc_data:
        description:
          - Certificate association data.
        type: str
        required: true
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false
  TXT:
    description:
      - Text RR.
      - Required if O(state=present) or O(state=absent) and O(type) and O(records)
        and any of the other RR type option not present.
    type: list
    elements: dict
    suboptions:
      strings:
        description:
          - Text strings.
        type: raw
        required: true
      disabled:
        description:
          - Whether or not this RR is disabled.
        type: bool
        default: false


author: Mohamed Chamrouk (@mohamed-chamrouk)
"""

EXAMPLES = """
%YAML 1.2
---
- name: Creating an RRset of RR type A
  kpfleming.powerdns_auth.rrset:
    api_key: foo
    zone_name: zone.example.
    name: ns.zone.example.
    type: A
    records:
      - content: 192.168.0.1

- name: Creating an RRset of RR type A
  kpfleming.powerdns_auth.rrset:
    api_key: foo
    zone_name: zone.example.
    name: ns.zone.example.
    A:
      - address: 192.168.0.1

- name: Deleting an RRset
  kpfleming.powerdns_auth.rrset:
    api_key: foo
    zone_name: zone.example.
    name: ns.zone.example.
    type: A

- name: Replacing RR in an RRset
  kpfleming.powerdns_auth.rrset:
    api_key: foo
    zone_name: zone.example.
    name: ns.zone.example.
    A:
      - address: 192.168.1.1

- name: Adding RR to an RRset
  kpfleming.powerdns_auth.rrset:
    api_key: foo
    zone_name: zone.example.
    name: ns.zone.example.
    keep: true
    NS:
      - host: ns1.example.

- name: Deleting RR in RRset
  kpfleming.powerdns_auth.rrset:
    api_key: foo
    zone_name: zone.example.
    name: ns.zone.example.
    state: absent
    keep: true
    NS:
      - host: ns1.example.

- name: Listing all RRsets in a zone
  kpfleming.powerdns_auth.rrset:
    api_key: foo
    zone_name: zone.example.
    state: exists
"""

RETURN = """
%YAML 1.2
---
name:
  description: name of the RRset
  returned: always
  type: str
  sample: rrset.example.
exists:
  description: whether the provided name and type lead to existing RRset(s)
  returned: when state is exists and name and/or type provided
  type: bool
rrsets:
  description: list of existing RRsets or RRsets after changes are made
  returned: always
  type: list
  elements: dict
  contains:
    comments:
      description:
        - list of comments on the RRset
      type: list
      elements: str
    name:
      description:
        - name of the RRset
      type: str
    records:
      description:
        - RRs list
      type: list
      elements: str
    ttl:
      description:
        - TTL of the RRs, in seconds.
      type: int
    type:
      description:
        - RR type
      type: str
"""


def get_result_rrsets(rrsets, rrset_name, rrset_type):
    """
    Function to build the return object to the ansible module.
    rrsets refers to the existings RRsets.
    rrset_name and rrset_type can be None, if provided it will filter rrsets based on those.
    """
    r = {
        "rrsets": rrsets,
    }

    if rrset_name is not None:
        if rrset_type is not None:
            r = {
                "exists": False,
                "rrsets": [],
            }
            for rrset in rrsets:
                if rrset["name"] == rrset_name and rrset["type"] == rrset_type:
                    r = {
                        "exists": True,
                        "rrsets": [rrset],
                    }
        else:
            r = {
                "exists": False,
                "rrsets": [],
            }
            for rrset in rrsets:
                if rrset["name"] == rrset_name:
                    r["rrsets"] += [rrset]
                    r["exists"] = True
    elif rrset_type is not None:
        r = {
            "exists": False,
            "rrsets": [],
        }
        for rrset in rrsets:
            if rrset["type"] == rrset_type:
                r["rrsets"] += [rrset]
                r["exists"] = True

    return r


def get_rrsets(api_client):
    return api_client.listZone(rrsets=True)["rrsets"]


def safe_string_record(record_type, record, type_def):
    """
    PowerDNS expects some field of some records to have quotes.
    Said fields have type "raw", allowing for filtering.
    """
    record_spec = type_def[record_type]

    safe_record = record

    for field in record_spec["options"].items():
        if field[0] in record and field[1]["type"] == "raw":
            value = safe_record[field[0]]
            safe_record[field[0]] = '"' + value.removeprefix('"').removesuffix('"') + '"'

    return safe_record


def main():
    module_args = {
        "state": {
            "type": "str",
            "default": "present",
            "choices": ["present", "absent", "exists"],
        },
        "name": {
            "type": "str",
        },
        "zone_name": {
            "type": "str",
            "required": True,
        },
        **API_MODULE_ARGS,
        "keep": {
            "type": "bool",
            "default": False,
        },
        "ttl": {
            "type": "int",
            "default": 3600,
        },
        "type": {
            "type": "str",
        },
        "records": {
            "type": "list",
            "elements": "dict",
            "options": {
                "disabled": {
                    "type": "bool",
                    "default": False,
                },
                "content": {
                    "type": "str",
                    "required": True,
                },
            },
        },
        "A": {
            "type": "list",
            "elements": "dict",
            "options": {
                "address": {"type": "str", "required": True},
                "disabled": {"type": "bool", "required": False, "default": False},
            },
        },
        "AAAA": {
            "type": "list",
            "elements": "dict",
            "options": {
                "address": {"type": "str", "required": True},
                "disabled": {"type": "bool", "required": False, "default": False},
            },
        },
        "CAA": {
            "type": "list",
            "elements": "dict",
            "options": {
                "flags": {"type": "int", "required": False, "default": 0, "choices": [0, 1]},
                "tag": {
                    "type": "str",
                    "required": True,
                    "choices": ["issue", "issuewild", "iodef"],
                },
                "value": {"type": "raw", "required": True},
                "disabled": {"type": "bool", "required": False, "default": False},
            },
        },
        "CNAME": {
            "type": "list",
            "elements": "dict",
            "options": {
                "cname": {"type": "str", "required": True},
                "disabled": {"type": "bool", "required": False, "default": False},
            },
        },
        "DNSKEY": {
            "type": "list",
            "elements": "dict",
            "options": {
                "flags": {"type": "int", "required": True, "choices": [256, 257]},
                "protocol": {"type": "int", "required": True, "choices": [3]},
                "algorithm": {"type": "int", "required": True},
                "public_key": {"type": "str", "required": True},
                "disabled": {"type": "bool", "required": False, "default": False},
            },
        },
        "DS": {
            "type": "list",
            "elements": "dict",
            "options": {
                "key_tag": {"type": "int", "required": True},
                "algorithm": {"type": "int", "required": True},
                "digest_type": {"type": "int", "required": True, "choices": [1, 2, 3, 4]},
                "digest": {"type": "str", "required": True},
                "disabled": {"type": "bool", "required": False, "default": False},
            },
        },
        "HINFO": {
            "type": "list",
            "elements": "dict",
            "options": {
                "cpu": {"type": "raw", "required": True},
                "os": {"type": "raw", "required": True},
                "disabled": {"type": "bool", "required": False, "default": False},
            },
        },
        "HTTPS": {
            "type": "list",
            "elements": "dict",
            "options": {
                "priority": {"type": "int", "required": True},
                "target": {"type": "str", "required": True},
                "params": {"type": "str", "required": False},
                "disabled": {"type": "bool", "required": False, "default": False},
            },
        },
        "LOC": {
            "type": "list",
            "elements": "dict",
            "options": {
                "latitude": {"type": "str", "required": True},
                "longitude": {"type": "str", "required": True},
                "altitude": {"type": "str", "required": True},
                "size": {"type": "str", "required": False, "default": "1.0m"},
                "horizontal_precision": {"type": "str", "required": False, "default": "10000.0m"},
                "vertical_precision": {"type": "str", "required": False, "default": "10.0m"},
                "disabled": {"type": "bool", "required": False, "default": False},
            },
        },
        "MX": {
            "type": "list",
            "elements": "dict",
            "options": {
                "preference": {"type": "int", "required": True},
                "exchange": {"type": "str", "required": True},
                "disabled": {"type": "bool", "required": False, "default": False},
            },
        },
        "NAPTR": {
            "type": "list",
            "elements": "dict",
            "options": {
                "order": {"type": "int", "required": True},
                "preference": {"type": "int", "required": True},
                "flags": {"type": "raw", "required": True},
                "services": {"type": "raw", "required": True},
                "regexp": {"type": "raw", "required": True},
                "replacement": {"type": "str", "required": True},
                "disabled": {"type": "bool", "required": False, "default": False},
            },
        },
        "NS": {
            "type": "list",
            "elements": "dict",
            "options": {
                "host": {"type": "str", "required": True},
                "disabled": {"type": "bool", "required": False, "default": False},
            },
        },
        "NSEC": {
            "type": "list",
            "elements": "dict",
            "options": {
                "next_domain": {"type": "str", "required": True},
                "type_bitmap": {"type": "str", "required": True},
                "disabled": {"type": "bool", "required": False, "default": False},
            },
        },
        "NSEC3PARAM": {
            "type": "list",
            "elements": "dict",
            "options": {
                "hash_algorithm": {"type": "int", "required": True, "choices": [1]},
                "flags": {"type": "int", "required": True, "choices": [0, 1]},
                "iterations": {"type": "int", "required": True},
                "salt": {"type": "str", "required": True},
                "disabled": {"type": "bool", "required": False, "default": False},
            },
        },
        "PTR": {
            "type": "list",
            "elements": "dict",
            "options": {
                "ptrdname": {"type": "str", "required": True},
                "disabled": {"type": "bool", "required": False, "default": False},
            },
        },
        "RP": {
            "type": "list",
            "elements": "dict",
            "options": {
                "mbox": {"type": "str", "required": True},
                "txt": {"type": "str", "required": True},
                "disabled": {"type": "bool", "required": False, "default": False},
            },
        },
        "SPF": {
            "type": "list",
            "elements": "dict",
            "options": {
                "strings": {"type": "raw", "required": True},
                "disabled": {"type": "bool", "required": False, "default": False},
            },
        },
        "SOA": {
            "type": "list",
            "elements": "dict",
            "options": {
                "mname": {"type": "str", "required": True},
                "rname": {"type": "str", "required": True},
                "serial": {"type": "int", "required": False},
                "refresh": {"type": "int", "required": False},
                "retry": {"type": "int", "required": False},
                "expire": {"type": "int", "required": False},
                "minimum": {"type": "int", "required": False},
                "disabled": {"type": "bool", "required": False, "default": False},
            },
        },
        "SRV": {
            "type": "list",
            "elements": "dict",
            "options": {
                "priority": {"type": "int", "required": True},
                "weight": {"type": "int", "required": True},
                "port": {"type": "int", "required": True},
                "target": {"type": "str", "required": True},
                "disabled": {"type": "bool", "required": False, "default": False},
            },
        },
        "SSHFP": {
            "type": "list",
            "elements": "dict",
            "options": {
                "algorithm": {"type": "int", "required": True, "choices": [1, 2, 3, 4, 6]},
                "fp_type": {"type": "int", "required": True, "choices": [1, 2, 3]},
                "fingerprint": {"type": "str", "required": True},
                "disabled": {"type": "bool", "required": False, "default": False},
            },
        },
        "SVCB": {
            "type": "list",
            "elements": "dict",
            "options": {
                "priority": {"type": "int", "required": True},
                "target": {"type": "str", "required": True},
                "params": {"type": "str", "required": False},
                "disabled": {"type": "bool", "required": False, "default": False},
            },
        },
        "TLSA": {
            "type": "list",
            "elements": "dict",
            "options": {
                "usage": {"type": "int", "required": True, "choices": [0, 1, 2, 3]},
                "selector": {"type": "int", "required": True, "choices": [0, 1]},
                "matching_type": {"type": "int", "required": True, "choices": [0, 1, 2]},
                "cert_assoc_data": {"type": "str", "required": True},
                "disabled": {"type": "bool", "required": False, "default": False},
            },
        },
        "TXT": {
            "type": "list",
            "elements": "dict",
            "options": {
                "strings": {"type": "raw", "required": True},
                "disabled": {"type": "bool", "required": False, "default": False},
            },
        },
    }

    record_types = [
        "A",
        "AAAA",
        "CAA",
        "CNAME",
        "DNSKEY",
        "DS",
        "HINFO",
        "HTTPS",
        "LOC",
        "MX",
        "NAPTR",
        "NS",
        "NSEC",
        "NSEC3PARAM",
        "PTR",
        "RP",
        "SPF",
        "SOA",
        "SRV",
        "SSHFP",
        "SVCB",
        "TLSA",
        "TXT",
    ]

    # mutually_exclusive: prevent use of type and A,AAAA... at the same time
    # require_if: if state is absent, one of type, A, AAAA is required and so on
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False,
        mutually_exclusive=[(record_type, "records") for record_type in record_types]
        + [(record_type, "type") for record_type in record_types],
        required_if=[
            ("state", "absent", [*record_types, "type"], True),
            ("state", "present", ["name"]),
            ("state", "absent", ["name"]),
            ("state", "present", [*record_types, "type"], True),
        ],
    )

    state = module.params["state"]
    zone_name = module.params["zone_name"]

    result = {
        "changed": False,
    }

    api_client = APIZoneWrapper(module=module, result=result, object_type="zones", zone_id=None)

    partial_zone_info = api_client.listZones(zone=zone_name)

    if len(partial_zone_info) == 0:
        module.fail_json(f"Failed to find zone named {zone_name}")

    # get the zone_id from the zone_name
    zone_id = partial_zone_info[0]["id"]
    api_client.zone_id = zone_id
    params = module.params

    result.update({"name": params["name"]})

    zone_rrsets = get_rrsets(api_client)
    result_rrsets = get_result_rrsets(zone_rrsets, params["name"], params["type"])

    if state == "exists":
        result.update(result_rrsets)
        module.exit_json(**result)

    changetype = "REPLACE" if state == "present" else "DELETE"
    # The following variable refers to the DNS Record types options (A,AAAA,CAA...)
    rrset_record_types = set(p for p in params if params[p] is not None) & set(record_types)  # noqa: C401

    # Check couldn't fit in AnsibleModule args
    type_classic = "type" in params and "records" in params
    if params["state"] == "present" and not (type_classic or rrset_record_types):
        module.fail_json("State is present but no valid RR has been provided")

    if rrset_record_types:
        rrset_records = [
            {
                "type": record_type,
                "records": [
                    safe_string_record(
                        record_type, record, {t: module_args[t] for t in record_types}
                    )
                    for record in params[record_type]
                ],
            }
            for record_type in rrset_record_types
        ]

        rrsets_struct = []
        records = []

        for rrset in rrset_records:
            for record in rrset["records"]:
                disabled = record.pop("disabled")
                records += [{"disabled": disabled, "content": " ".join(map(str, record.values()))}]

            rrsets_struct += [
                {
                    "name": params["name"].lower(),
                    "type": rrset["type"],
                    "ttl": params["ttl"],
                    "keep": params["keep"],
                    "changetype": changetype,
                    "records": records,
                }
            ]

            records = []
    else:
        rrsets_struct = [
            {
                "name": params["name"].lower(),
                "type": params["type"],
                "ttl": params["ttl"],
                "keep": params["keep"],
                "changetype": changetype,
                "records": params.get("records", []),
            }
        ]

    zone_struct = {}

    for rrset in rrsets_struct:
        # Retrieving existing rrset, there can only be one
        # that matches "name" and "type" values.
        existing_rrset = next(
            (r for r in zone_rrsets if r["name"] == rrset["name"] and r["type"] == rrset["type"]),
            None,
        )

        rrset_changetype = rrset["changetype"]
        rrset_keep = rrset.pop(
            "keep"
        )  # Keeping the option out for cleaner zone_struct on subsequent unpacking

        if not existing_rrset or not rrset_keep:
            if rrset_changetype == "REPLACE":
                # For REPLACE, not wanting to keep existing records or not having any existing
                # records is the same
                if rrset["type"] is not None:
                    zone_struct.setdefault("rrsets", []).append(rrset)
                else:
                    module.fail_json("No valid record found for RRset creation.")
            elif rrset_changetype == "DELETE":
                if existing_rrset:
                    zone_struct.setdefault("rrsets", []).append(rrset)
                else:
                    module.fail_json(
                        f"No matching RRset found for name: {rrset['name']} \
                          and type: {rrset['type']}"
                    )
        elif rrset["records"] == existing_rrset["records"]:
            # Despite keep being present, if existing records and given ones match
            # exactly then for changetype="DELETE",
            # the final operation is to delete the whole rrset.
            # If the changetype is "REPLACE",
            # nothing is done for the rest of the rrset
            if rrset_changetype == "DELETE":
                # Using .setdefault to avoid creating a key on zone_struct dict
                # and keep the dict empty for idempotency
                zone_struct.setdefault("rrsets", []).append(
                    {
                        "name": rrset["name"],
                        "type": rrset["type"],
                        "changetype": "DELETE",
                    }
                )
        else:
            if rrset_changetype == "REPLACE":
                # Building a list of unique union of existing and provided records
                new_records_list = existing_rrset["records"] + [
                    record for record in rrset["records"] if record not in existing_rrset["records"]
                ]
            else:
                # Building a list of remaining records
                # after removing provided ones from existing ones
                new_records_list = [] + [
                    r for r in existing_rrset["records"] if r not in rrset["records"]
                ]

            if new_records_list != existing_rrset["records"]:
                zone_struct.setdefault("rrsets", []).append(
                    {
                        **rrset,
                        "records": new_records_list,
                        "changetype": "REPLACE",
                    }
                )

    if module.check_mode:
        module.exit_json(**result)

    if zone_struct:
        api_client.patchZone(zone_struct=zone_struct)
        result["changed"] = True
        result["rrsets"] = get_rrsets(api_client)

    module.exit_json(**result)


if __name__ == "__main__":
    main()
