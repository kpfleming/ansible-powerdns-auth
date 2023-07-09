#!/usr/bin/env bash

set -ex

pdns_dir=${1}
pdns_ver=${2}

cd "${pdns_dir}"

mkdir -p /pdns/"${pdns_ver}"

autoreconf -vi
./configure --prefix=/pdns/"${pdns_ver}" --with-modules="gsqlite3" --disable-lua-records

make -j2 -C pdns apidocfiles.h
make -j2 -C ext
make -j2 -C pdns pdns_server

cp pdns/pdns_server /pdns/"${pdns_ver}"

sqlite3 /pdns/"${pdns_ver}"/pdns.sqlite3 '.read modules/gsqlite3backend/schema.sqlite3.sql'
