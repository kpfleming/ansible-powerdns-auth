#!/bin/bash

pdns_ver=${1}

exec /pdns/"${pdns_ver}"/pdns_server --no-config --daemon --api --api-key=foo --disable-syslog --local-port=55353 --socket-dir=/run --launch=gsqlite3 --gsqlite3-database=/pdns/"${pdns_ver}"/pdns.sqlite3 --gsqlite3-dnssec=on
