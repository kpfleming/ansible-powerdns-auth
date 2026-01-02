#!/usr/bin/env bash

set -ex

pdns_dir=${1}
pdns_ver=${2}

cd "${pdns_dir}"

mkdir -p /pdns/"${pdns_ver}"/etc

autoreconf -vi
./configure --prefix=/pdns/"${pdns_ver}" --with-modules="lmdb" --disable-lua-records

make -j2 -C pdns apidocfiles.h
make -j2 -C ext
make -j2 -C pdns

cp pdns/pdns_server /pdns/"${pdns_ver}"
cp pdns/pdnsutil /pdns/"${pdns_ver}"

cat <<EOF > /pdns/"${pdns_ver}"/etc/pdns.conf
api=yes
api-key=foo
daemon=yes
disable-syslog=yes
local-port=55353
socket-dir=/run
launch=lmdb
lmdb-filename=/pdns/${pdns_ver}/pdns.lmdb
lmdb-shards=1
lmdb-random-ids=yes
lmdb-map-size=16
EOF
