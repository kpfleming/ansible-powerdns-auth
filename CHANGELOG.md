# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.8.0] - 2021-10-02

### Changed

- Removed support for Python 3.6 and 3.7, as Ansible will require 3.8 soon.

- Pinned 'jsonschema' to versions below 4 to maintain compatibiity with
the pinned version of `swagger-spec-validator'.

## [1.7.0] - 2021-08-31

### Changed

- Added testing against PowerDNS Authoritative Server 4.5.x.

- Added testing against Python 3.10 release candidates.

## [1.6.0] - 2021-04-20

### Changed

- Removed testing against PowerDNS Authoritative Server 4.2.x, which is no longer
supported.

- Added testing against PowerDNS Authoritative Server 4.4.x, which includes HTTP
support for obtaining the API schema.

- Corrected flaws in test playbooks.

## [1.5.0] - 2020-11-29

### Changed

- Support for creation of SOA and NS records during zone creation, eliminating
requirement to set server configuration properties to synthesize the records.

## [1.4.0] - 2020-11-23

### Changed

- Support for direct reading of the Swagger spec from the server (instead
of a local file) has been added; this feature will be available in PowerDNS
Authoritative Server 4.4.0.

## [1.3.0] - 2020-08-19

### Changed

- Python 3.5 support has been removed.

## [1.2.2] - 2020-08-17

### Changed

- Correct population of existing zone properties.
- Handle API-RECTIFY as a binary zone property instead of ternary.
- Improve performance by requesting that rrsets not be returned in zone API calls.

## [1.2.1] - 2020-08-15

### Changed

- Improved handling of zone metadata during zone creation; default values are
  no longer sent, as they can trigger errors using the current development
  branch of the server.

## [1.2.0] - 2020-06-12

### Changed

- Improved handling of predictable exceptions from API operations.
- Corrected handling of changes to list of masters in slave zones.

## [1.1.0] - 2020-04-09

### Added

- pdns_auth_tsigkey.py module for managing TSIG keys.

- Support for metadata-in-zone properties.

### Changed

- Removed metadata elements which are immutable from the module parameters list;
  they will still be included in the return value if set on a zone.

- Updated to 0.0.15 version of API specification which documents all response objects.

## 1.0.0 - 2020-04-03

First release!

### Added

- pdns_auth_zone.py module for managing zones.

### Changed

[unreleased]: https://github.com/kpfleming/ansible-pdns-auth-api/compare/v1.8.0...HEAD
[1.8.0]: https://github.com/kpfleming/ansible-pdns-auth-api/compare/v1.7.0...v1.8.0
[1.7.0]: https://github.com/kpfleming/ansible-pdns-auth-api/compare/v1.6.0...v1.7.0
[1.6.0]: https://github.com/kpfleming/ansible-pdns-auth-api/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.com/kpfleming/ansible-pdns-auth-api/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/kpfleming/ansible-pdns-auth-api/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/kpfleming/ansible-pdns-auth-api/compare/v1.2.2...v1.3.0
[1.2.2]: https://github.com/kpfleming/ansible-pdns-auth-api/compare/v1.2.1...v1.2.2
[1.2.1]: https://github.com/kpfleming/ansible-pdns-auth-api/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/kpfleming/ansible-pdns-auth-api/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/kpfleming/ansible-pdns-auth-api/compare/v1.0.0...v1.1.0
