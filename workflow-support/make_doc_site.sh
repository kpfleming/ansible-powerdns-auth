#!/usr/bin/env bash

set -ex

scriptdir=$(realpath "$(dirname "${BASH_SOURCE[0]}")")
basedir="$(realpath "${scriptdir}/..")"
workdir="/work"
base_image="docker.io/python:3.11"

rm -rf "${basedir}/docs-build"

c=$(buildah from "${base_image}")

build_cmd() {
    buildah run --network host --volume "${basedir}:${workdir}" --workingdir "${workdir}" "${c}" -- "$@"
}

build_cmd apt-get update --quiet=2
build_cmd apt-get install --yes --quiet=2 rsync

build_cmd pip3 install ansible antsibull-docs

build_cmd ansible-galaxy collection install kpfleming.powerdns_auth

build_cmd mkdir docs-build

build_cmd antsibull-docs sphinx-init --fail-on-error --use-current --dest-dir docs-build kpfleming.powerdns_auth

buildah rm "${c}"
