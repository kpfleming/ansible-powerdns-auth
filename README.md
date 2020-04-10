# ansible-pdns-auth-api

<a href="https://opensource.org"><img height="150" align="left" src="https://opensource.org/files/OSIApprovedCropped.png" alt="Open Source Initiative Approved License logo"></a>
[![CI](https://github.com/kpfleming/ansible-pdns-auth-zone/workflows/CI/badge.svg)](https://github.com/kpfleming/ansible-pdns-auth-zone/workflows/CI/badge.svg?branch=master)
[![build-image](https://github.com/kpfleming/ansible-pdns-auth-zone/workflows/build-image/badge.svg)](https://github.com/kpfleming/ansible-pdns-auth-zone/workflows/build-image/badge.svg?branch=master)
[![Python](https://img.shields.io/badge/python-3.5+-blue.svg)](https://www.python.org/download/releases/3.5.0/)

Ansible modules which can be used to manage zones and other content in
[PowerDNS Authoritative servers.](https://www.powerdns.com/auth.html)

Open Source software: Apache License 2.0

## &nbsp;

## pdns_auth_zone.py

This module can be used to create, remove, and manage zones. It can
also trigger some zone-related actions: NOTIFY and AXFR. Put the
module file into a suitable 'library' directory for your Ansible
installation, role, or playbook.

Note that if any 'metadata' attributes are specified when `state` is
set to `present`, *all* metadata attributes on the zone will be
updated or removed, depending on their defaults. As a result, you
must specify *all* metadata attributes that you wish to have set
on the zone.

Examples:
```
- name: create native zone
  pdns_auth_zone:
    name: d2.example.
    state: present
    api_key: 'foobar'
    api_spec_file: 'api-swagger.json'
    properties:
      kind: 'Native'
      nameservers:
        - 'ns1.example.'
    metadata:
      allow_axfr_from: ['AUTO-NS']
      axfr_source: '127.0.0.1'

- name: change native zone to master
  pdns_auth_zone:
    name: d2.example.
    state: present
    api_key: 'foobar'
    api_spec_file: 'api-swagger.json'
    properties:
      kind: 'Master'

- name: delete zone
  pdns_auth_zone:
    name: d2.example.
    state: absent
    api_key: 'foobar'
    api_spec_file: 'api-swagger.json'
```

## pdns_auth_tsigkey.py

This module can be used to create, remove, and manage TSIG keys.  Put
the module file into a suitable 'library' directory for your Ansible
installation, role, or playbook.

Examples:
```
- name: create key with default algorithm
  pdns_auth_tsigkey:
    name: key2
    state: present
    api_key: 'foobar'
    api_spec_file: 'api-swagger.json'

- name: remove key
  pdns_auth_tsigkey:
    name: key2
    state: absent
    api_key: 'foobar'
    api_spec_file: 'api-swagger.json'

- name: create key with algorithm and content
  pdns_auth_tsigkey:
    name: key3
    state: present
    api_key: 'foobar'
    api_spec_file: 'api-swagger.json'
    algorithm: hmac-sha256
    key: '+8fQxgYhf5PVGPKclKnk8ReujIfWXOw/aEzzPPhDi6AGagpg/r954FPZdzgFfUjnmjMSA1Yu7vo6DQHVoGnRkw=='
```

## Notes

In PowerDNS Authoritative Server releases prior to 4.4.0, the server
is not able to provide the OpenAPI/Swagger specification which this
module requires. In order to use this module, you'll need to copy
`api-swagger.json` to your Ansible control host (in the `files`
directory of the role or playbook), and use tasks similar to the ones
below to place a copy on the host where the module will be invoked.

```
- name: temp file to hold spec
  tempfile:
    state: file
    suffix: '.json'
    register: temp_file

- name: populate spec file
  copy:
    src: api-swagger.json
    dest: "{{ temp_file.path }}"
```
