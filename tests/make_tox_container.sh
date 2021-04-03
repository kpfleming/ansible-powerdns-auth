#!/usr/bin/env bash

set -ex

scriptdir=$(realpath $(dirname ${BASH_SOURCE[0]}))
pdns=${1}
pydeps=(build-essential libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev)

${scriptdir}/buildah_fix.sh

c=$(buildah from debian:buster)

buildcmd() {
    buildah run --network host ${c} -- "$@"
}

buildah config --workingdir /root ${c}
buildah config --env pdns_version=dummy ${c}

buildcmd apt-get update --quiet=2
buildcmd apt-get install --yes --quiet=2 git

buildcmd apt-get install --yes --quiet=2 ${pydeps[@]}
for pyver in 3.6.13 3.7.10 3.8.9 3.9.3; do
    wget -O - https://www.python.org/ftp/python/${pyver}/Python-${pyver}.tgz | buildcmd tar xzf -
    buildah config --workingdir /root/Python-${pyver} ${c}
    buildcmd ./configure --disable-shared
    buildcmd make -j2 altinstall
    buildah config --workingdir /root ${c}
    buildcmd rm -rf /root/Python-${pyver}
done

buildcmd sh -c "rm -rf /usr/local/bin/python3.?m*"

buildcmd pip3.9 install tox
buildah copy ${c} ${scriptdir}/../tox.ini /root/tox.ini
buildcmd tox -eALL --notest --workdir /root/tox

buildcmd apt-get remove --yes --purge ${pydeps[@]}
buildcmd apt-get autoremove --yes --purge
buildcmd apt-get clean autoclean
buildcmd sh -c "rm -rf /var/lib/apt/lists/*"
buildcmd rm -rf /root/.cache

if buildah images --quiet ${image_name}; then
    buildah rmi ${image_name}
fi
buildah commit --squash --rm ${c} ${image_name}
