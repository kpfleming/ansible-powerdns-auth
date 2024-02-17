#!/usr/bin/env bash

set -ex

scriptdir=$(realpath "$(dirname "${BASH_SOURCE[0]}")")
basedir="$(realpath "${scriptdir}/..")"

rm -rf "${basedir}/docs"

apt-get update --quiet=2
apt-get install --yes --quiet=2 rsync

pip3 install ansible

ansible-galaxy collection install "${2}"

pip3 install -r "${basedir}/docs-build/requirements.txt"

"${basedir}/docs-build/build.sh" "${1}"

mv "${basedir}/docs-build/build/html" "${basedir}/docs"

touch "${basedir}/docs/.nojekyll"
