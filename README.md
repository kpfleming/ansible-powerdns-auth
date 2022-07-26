# ansible-powerdns-auth

<a href="https://opensource.org"><img height="150" align="left" src="https://opensource.org/files/OSIApprovedCropped.png" alt="Open Source Initiative Approved License logo"></a>
[![CI](https://github.com/kpfleming/ansible-powerdns-auth/workflows/CI/badge.svg)](https://github.com/kpfleming/ansible-powerdns-auth/actions?query=workflow%3ACI)
[![Build Image](https://github.com/kpfleming/ansible-powerdns-auth/workflows/Build%20Image%20and%20CI/badge.svg)](https://github.com/kpfleming/ansible-powerdns-auth/actions?query=workflow%3A%22Build+Image+and+CI%22)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-3812/)

This repo contains the `kpfleming.powerdns_auth` Ansible Collection. The collection includes modules to work with
[PowerDNS Authoritative servers.](https://www.powerdns.com/auth.html)

Open Source software: Apache License 2.0

## &nbsp;

## External requirements

The modules require the [Bravado](https://pypi.org/project/bravado/)
package for parsing the Swagger/OpenAPI specification of the PowerDNS
Authoritative Server API.

## Included content

* Modules:
  * PowerDNS Authoritative Server:
    - kpfleming.powerdns_auth.tsigkey: manage TSIG keys
    - kpfleming.powerdns_auth.zone: manage zones

## Using this collection

In order to use this collection, you need to install it using the
`ansible-galaxy` CLI:

    ansible-galaxy collection install kpfleming.powerdns_auth

You can also include it in a `requirements.yml` file and install it
via `ansible-galaxy collection install -r requirements.yml` using the
format:

```yaml
collections:
  - name: kpfleming.powerdns_auth
```

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Contributing to this collection

If you want to develop new content for this collection or improve what
is already here, the easiest way to work on the collection is to clone
it into one of the configured
[`COLLECTIONS_PATH`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#collections-paths),
and work on it there.

You can find more information in the [developer guide for
collections](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections),
and in the [Ansible Community
Guide](https://docs.ansible.com/ansible/latest/community/index.html).

## More information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Collections Checklist](https://github.com/ansible-collections/overview/blob/master/collection_requirements.rst)
