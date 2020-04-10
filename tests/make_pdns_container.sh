#!/usr/bin/env bash

set -e

if [ -z "${1}" ]; then
    echo "Must specify a PowerDNS Auth version (or 'master')."
    echo "Examples: 4.2, 4.3, master."
    exit 1
fi

root=$(dirname ${BASH_SOURCE[0]})
pdns=${1}

image=quay.io/kpfleming/apaa-test-images:pdns-${pdns}

c=$(buildah from quay.io/kpfleming/apaa-test-images:tox)

buildcmd() {
    buildah run ${c} -- "$@"
}

buildah config --workingdir /root ${c}

buildcmd apt-get update
buildcmd apt-get install --yes --quiet=2 gnupg sqlite3

buildah copy ${c} ${root}/apt-repo-pdns-auth-${pdns}.list /etc/apt/sources.list.d
buildah copy ${c} ${root}/apt-pref-pdns /etc/apt/preferences.d
if [ "${pdns}" == "master" ]; then
    curl --silent --location https://repo.powerdns.com/CBC8B383-pub.asc | buildcmd apt-key add
else
    curl --silent --location https://repo.powerdns.com/FD380FBB-pub.asc | buildcmd apt-key add
fi
buildcmd apt-get update --quiet=2
buildcmd apt-get install --yes --quiet=2 pdns-server pdns-backend-sqlite3
buildcmd apt-get purge --yes --quiet=2 pdns-backend-bind
buildcmd sqlite3 /run/pdns.sqlite3 '.read /usr/share/doc/pdns-backend-sqlite3/schema.sqlite3.sql'

buildcmd rm -rf /var/lib/apt/lists/*
buildcmd rm -rf /root/.cache

if buildah images --quiet ${image}; then
    buildah rmi ${image}
fi
buildah commit --squash --rm ${c} ${image}

if [ -z "${GITHUB_WORKFLOW}" ]; then
    echo New image is ${image}.
else
    echo "::set-env name=new_image::${image}"
fi
