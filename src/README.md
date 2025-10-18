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

## kpfleming.powerdns_auth.rrset

This module can be used to create and remove RRsets. It can also manage resource records in any RRset.
Two modes are available for RRs management, you can either use the "standard" way :
```yaml
- name: Creating an RRset of RR type A
  kpfleming.powerdns_auth.rrset:
    api_key: foo
    zone_name: zone.example.
    name: ns.zone.example.
    type: A
    records:
      - content: 192.168.0.1
```
or use the resource record options from one of the supported types :
```yaml
- name: Creating an RRset of RR type A
  kpfleming.powerdns_auth.rrset:
    api_key: foo
    zone_name: zone.example.
    name: ns.zone.example.
    A:
      - address: 192.168.0.1
```

The supported types are :
A,AAAA,CAA,CNAME,DNSKEY,DS,HINFO,HTTPS,LOC,MX,NAPTR,NS,PTR,RP,SPF,SOA,SRV,SSHFP,SVCB,TLSA,TXT

Idempotency is only supported when the `keep` option is provided.

Examples:
```yaml
- name: Deleting an RRset
  kpfleming.powerdns_auth.rrset:
    api_key: foo
    zone_name: zone.example.
    name: ns.zone.example.
    type: A

- name: Replacing an RR in an RRset
  kpfleming.powerdns_auth.rrset:
    api_key: foo
    zone_name: zone.example.
    name: ns.zone.example.
    A:
      - address: 192.168.1.1

- name: Adding an RR to an RRset
  kpfleming.powerdns_auth.rrset:
    api_key: foo
    zone_name: zone.example.
    name: ns.zone.example.
    keep: true
    NS:
      - host: ns1.example.

- name: Deleting an RR in an RRset
  kpfleming.powerdns_auth.rrset:
    api_key: foo
    zone_name: zone.example.
    name: ns.zone.example.
    state: absent
    keep: true
    NS:
      - host: ns1.example.

- name: Listing all RRsets in a given zone
  kpfleming.powerdns_auth.rrset:
    api_key: foo
    zone_name: zone.example.
    state: exists
```

## kpfleming.powerdns_auth.cryptokey

This module can create, delete, activate/deactivate, publish/unpublish a CryptoKey in a zone of PowerDNS Authoritative server.

Note that for keytype, by default if only one key is present it will be used as a csk regardless ofthe provided type. For the key to assume its role another key of the opposite type has to be present (zsk for ksk and vice-versa).

Examples:
```yaml
- name: Generate key
  kpfleming.powerdns_auth.cryptokey:
    api_key: foo
    zone_name: crypto.example.
    state: present
    keytype: csk
    algorithm: ed25519
    active: true

- name: Import key
  kpfleming.powerdns_auth.cryptokey:
    api_key: foo
    zone_name: crypto.example.
    state: present
    keytype: zsk
    dnskey: "257 3 15 lMu/7quhLeSueMcdlt3T0sxln32yhrhASCKKDB1xJOk="
    privatekey: 'Private-key-format: v1.2\n
                 Algorithm: 15 (ED25519)\n
                 PrivateKey: Rnt2dv3mWMmP8bU/8koayZ4R5dWdI86zJmZ0nnjPe6Q=\n'
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
    active: true

- name: Listing a specific key
  kpfleming.powerdns_auth.cryptokey:
    api_key: foo
    zone_name: crypto.example.
    state: exists
    id: 1

- name: Listing all keys in the zone
  kpfleming.powerdns_auth.cryptokey:
    api_key: foo
    zone_name: crypto.example.
    state: exists
```
