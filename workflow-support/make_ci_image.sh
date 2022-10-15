#!/usr/bin/env bash

set -ex

scriptdir=$(realpath "$(dirname "${BASH_SOURCE[0]}")")
base_image=${1}
image_name=${2}
pdns=${3}

lintdeps=(shellcheck)

case "${pdns}" in
    4.4)
	c=$(buildah from "${base_image}":buster-main)
	;;
    *)
	c=$(buildah from "${base_image}":bullseye-main)
	;;
esac

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
buildah config --env pdns_version=dummy "${c}"
buildcmd tox -eALL --notest --workdir /root/tox

buildcmd rm -rf /root/.cache

if buildah images --quiet "${image_name}"; then
    buildah rmi "${image_name}"
fi
buildah commit --squash --rm "${c}" "${image_name}"
