# ansible-powerdns-auth

<a href="https://opensource.org"><img height="150" align="left" src="https://opensource.org/files/OSIApprovedCropped.png" alt="Open Source Initiative Approved License logo"></a>
[![CI](https://github.com/kpfleming/ansible-powerdns-auth/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/kpfleming/ansible-powerdns-auth/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-31019/)
[![License - Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-9400d3.svg)](https://spdx.org/licenses/Apache-2.0.html)
[![Code Style and Quality - Ruff](https://img.shields.io/badge/Code%20Quality-Ruff-red.svg)](https://github.com/astral-sh/ruff)

This repo contains the `kpfleming.powerdns_auth` Ansible
Collection. The collection includes modules to work with [PowerDNS
Authoritative servers][2].

Open Source software: [Apache License 2.0][3]

## &nbsp;

## External requirements

The modules require the [Bravado][4] package for parsing the
Swagger/OpenAPI specification of the PowerDNS Authoritative Server
API.

As of PowerDNS Authoritative Server 4.9.x, the Swagger API
specification is not completely compliant, and as a result the
validation packages used by Bravado will not accept it. In order to
work around this problem, older versions of the validation packages
can be installed, like this:

```shell
pip install -r requirements.txt
```

This command can be executed in the environment on the Ansible
controller if the roles will be used only on 'localhost'; if they will
be used on Ansible-managed nodes, then the packages from the
requirements file will need to be installed there:

```yaml
- name: manage dependencies needed for powerdns_auth modules
  ansible.builtin.pip:
    name:
      - bravado
      - jsonschema<4
      - swagger-spec-validator==2.6.0
```

Add suitable parameters if the packages should be installed into a
virtual environment on the managed node.

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

See [Ansible Using collections][5] for more details.

Documentation of the collections's modules and their arguments/return
values can be found [here][1].

## Contributing to this collection

If you want to develop new content for this collection or improve what
is already here, the easiest way to work on the collection is to clone
it into one of the configured [`COLLECTIONS_PATH`][6], and work on it
there.

You can find more information in the [developer guide for
collections][7], and in the [Ansible Community Guide][8].

## More information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Collections Checklist](https://github.com/ansible-collections/overview/blob/master/collection_requirements.rst)

[1]: https://kpfleming.github.io/ansible-powerdns-auth
[2]: https://www.powerdns.com/auth.html
[3]: https://spdx.org/licenses/Apache-2.0.html
[4]: https://pypi.org/project/bravado/
[5]: https://docs.ansible.com/ansible/latest/user_guide/collections_using.html
[6]: https://docs.ansible.com/ansible/latest/reference_appendices/config.html#collections-paths
[7]: https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections
[8]: https://docs.ansible.com/ansible/latest/community/index.html
