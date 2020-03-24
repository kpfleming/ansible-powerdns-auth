#!/usr/bin/env bash

set -e

if [ -z "${1}" ]; then
    echo "Must specify a PowerDNS Auth version (or 'master')."
    echo "Examples: 4.2, 4.3, master."
    exit 1
fi

root=$(dirname ${BASH_SOURCE[0]})
pdns=${1}

image=quay.io/kpfleming/apaz-test-images:pdns-${pdns}

c=$(buildah from debian:buster)

buildah run ${c} -- apt-get update
buildah run ${c} -- apt-get install --yes --quiet=2 gnupg python3 python3-venv git sqlite3

buildah add ${c} ${root}/apt-repo-pdns-auth-${pdns}.list /etc/apt/sources.list.d
buildah add ${c} ${root}/apt-pref-pdns /etc/apt/preferences.d
if [ "${pdns}" == "master" ]; then
    curl --silent --location https://repo.powerdns.com/CBC8B383-pub.asc | buildah run ${c} -- apt-key add
else
    curl --silent --location https://repo.powerdns.com/FD380FBB-pub.asc | buildah run ${c} -- apt-key add
fi
buildah run ${c} -- apt-get update --quiet=2
buildah run ${c} -- apt-get install --yes --quiet=2 pdns-server pdns-backend-sqlite3
buildah run ${c} -- apt-get purge --yes --quiet=2 pdns-backend-bind
buildah run ${c} -- sqlite3 /run/pdns.sqlite3 '.read /usr/share/doc/pdns-backend-sqlite3/schema.sqlite3.sql'

buildah run ${c} -- python3 -m venv /ansible
buildah run ${c} -- /ansible/bin/pip install wheel
buildah run ${c} -- /ansible/bin/pip install ansible
buildah run ${c} -- /ansible/bin/pip install bravado

buildah run ${c} -- rm -rf /var/lib/apt/lists/*
buildah run ${c} -- rm -rf /root/.cache

if buildah images --quiet ${image}; then
    buildah rmi ${image}
fi
buildah commit --squash --rm ${c} ${image}

if [ -z "${GITHUB_WORKFLOW}" ]; then
    echo New image is ${image}.
else
    echo "::set-env name=new_image::${image}"
fi
