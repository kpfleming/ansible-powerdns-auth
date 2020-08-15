# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[unreleased]: https://github.com/kpfleming/ansible-pdns-auth-api/compare/v1.2.1...HEAD
[1.2.1]: https://github.com/kpfleming/ansible-pdns-auth-api/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/kpfleming/ansible-pdns-auth-api/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/kpfleming/ansible-pdns-auth-api/compare/v1.0.0...v1.1.0
