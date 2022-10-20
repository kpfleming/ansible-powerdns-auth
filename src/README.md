## kpfleming.powerdns_auth.zone

This module can be used to create, remove, and manage zones. It can
also trigger some zone-related actions: NOTIFY and AXFR.

Note that if any 'metadata' attributes are specified when `state` is
set to `present`, *all* metadata attributes on the zone will be
updated or removed, depending on their defaults. As a result, you
must specify *all* metadata attributes that you wish to have set
on the zone.

Examples:
```
- name: create native zone
  kpfleming.powerdns_auth.zone:
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
  kpfleming.powerdns_auth.zone:
    name: d2.example.
    state: present
    api_key: 'foobar'
    properties:
      kind: 'Master'

- name: delete zone
  kpfleming.powerdns_auth.zone:
    name: d2.example.
    state: absent
    api_key: 'foobar'
```

## kpfleming.powerdns_auth.tsigkey

This module can be used to create, remove, and manage TSIG keys.

Examples:
```
- name: create key with default algorithm
  kpfleming.powerdns_auth.tsigkey:
    name: key2
    state: present
    api_key: 'foobar'

- name: remove key
  kpfleming.powerdns_auth.tsigkey:
    name: key2
    state: absent
    api_key: 'foobar'

- name: create key with algorithm and content
  kpfleming.powerdns_auth.tsigkey:
    name: key3
    state: present
    api_key: 'foobar'
    algorithm: hmac-sha256
    key: '+8fQxgYhf5PVGPKclKnk8ReujIfWXOw/aEzzPPhDi6AGagpg/r954FPZdzgFfUjnmjMSA1Yu7vo6DQHVoGnRkw=='
```
