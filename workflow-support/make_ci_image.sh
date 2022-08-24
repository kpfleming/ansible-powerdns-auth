#!/usr/bin/env bash

set -ex

if [ -z "${1}" ]; then
    echo "Must specify a PowerDNS Auth version (or 'master')."
    echo "Examples: 4.5, 4.6, master."
    exit 1
fi

scriptdir=$(realpath "$(dirname "${BASH_SOURCE[0]}")")
pdns=${1}

lintdeps=(shellcheck)

c=$(buildah from quay.io/km6g-ci-images/python:main)

buildcmd() {
    buildah run --network host "${c}" -- "$@"
}

buildcmd mkdir /etc/apt/keyrings
buildah copy "${c}" "${scriptdir}/apt-repo-pdns-auth-${pdns}.list" /etc/apt/sources.list.d
buildah copy "${c}" "${scriptdir}/apt-pref-pdns" /etc/apt/preferences.d
buildah copy "${c}" "${scriptdir}/CBC8B383-pub.asc" /etc/apt/keyrings
buildah copy "${c}" "${scriptdir}/FD380FBB-pub.asc" /etc/apt/keyrings

buildcmd apt-get update --quiet=2
buildcmd apt-get install --yes --quiet=2 "${lintdeps[@]}"
buildcmd apt-get install --yes --quiet=2 gnupg sqlite3
buildcmd apt-get install --yes --quiet=2 pdns-server pdns-backend-sqlite3
buildcmd apt-get purge --yes --quiet=2 pdns-backend-bind
buildcmd sqlite3 /run/pdns.sqlite3 '.read /usr/share/doc/pdns-backend-sqlite3/schema.sqlite3.sql'

buildcmd apt-get autoremove --yes --purge
buildcmd apt-get clean autoclean
buildcmd sh -c "rm -rf /var/lib/apt/lists/*"

buildah copy "${c}" "${scriptdir}/../tox.ini" /root/tox.ini
buildcmd tox -eALL --notest --workdir /root/tox

buildcmd rm -rf /root/.cache

# shellcheck disable=SC2154 # image_name set in external environment
if buildah images --quiet "${image_name}"; then
    buildah rmi "${image_name}"
fi
buildah commit --squash --rm "${c}" "${image_name}"
