#!/usr/bin/env bash

set -ex

# Arguments:
#
# 1: registry, name, and tag of base image
# 2: registry, name, and tag of image to be created

scriptdir=$(realpath "$(dirname "${BASH_SOURCE[0]}")")
containersrcdir="/__w/${GITHUB_REPOSITORY##*/}/${GITHUB_REPOSITORY##*/}"
base_image=${1}; shift
image_name=${1}; shift

pdns_build=(build-essential autoconf automake ragel bison flex libboost-all-dev pkg-config python3-venv libluajit-5.1-dev libssl-dev libsqlite3-dev sqlite3)
pdns_run=(libsqlite3-0 libluajit-5.1-2)
lint_deps=(shellcheck)
publish_deps=(yq)

toxenvs=(lint-action ci-action publish-action)
cimatrix=(py3{9,10,11,12,13})

c=$(buildah from "${base_image}")

build_cmd() {
    buildah run --network host "${c}" -- "$@"
}

build_cmd_with_source() {
    buildah run --network host --volume "$(realpath "${scriptdir}/.."):${containersrcdir}" --workingdir "${containersrcdir}" "${c}" -- "$@"
}

build_cmd apt-get update --quiet=2
build_cmd apt-get install --yes --quiet=2 "${pdns_build[@]}" "${pdns_run[@]}"
build_cmd apt-get install --yes --quiet=2 "${lint_deps[@]}"
build_cmd apt-get install --yes --quiet=2 "${publish_deps[@]}"

for pdns_ver in "${@}"; do
    case "${pdns_ver}" in
	master)
	    pdns_url=https://github.com/PowerDNS/pdns/archive/refs/heads/master.tar.gz
	    pdns_dir=pdns-master
	    ;;
	*)
	    pdns_url=https://github.com/PowerDNS/pdns/archive/refs/heads/rel/auth-"${pdns_ver}".x.tar.gz
	    pdns_dir=pdns-rel-auth-"${pdns_ver}".x
	    ;;
    esac

    wget --quiet --output-document - "${pdns_url}" | tar --extract --gzip
    buildah run --network host --volume "${scriptdir}:/scriptdir" --volume "$(pwd)/${pdns_dir}:/${pdns_dir}" "${c}" -- /scriptdir/pdns_build.sh "/${pdns_dir}" "${pdns_ver}"

    rm -rf "${pdns_dir}"
done

for env in "${toxenvs[@]}"; do
    case "${env}" in
	ci-action)
	    for py in "${cimatrix[@]}"; do
		build_cmd_with_source tox exec -e "${py}-${env}" -- pip list
	    done
	;;
	*)
	    build_cmd_with_source tox exec -e "${env}" -- pip list
	;;
    esac
done

build_cmd apt-get remove --yes --purge "${pdns_build[@]}"
build_cmd apt-get autoremove --yes --purge
build_cmd apt-get clean autoclean
build_cmd sh -c "rm -rf /var/lib/apt/lists/*"

build_cmd rm -rf /root/.cache

build_cmd git config --system --add safe.directory "${containersrcdir}"

if buildah images --quiet "${image_name}"; then
    buildah rmi "${image_name}"
fi
buildah commit --squash --rm "${c}" "${image_name}"
