#!/usr/bin/env bash

set -e

root=$(dirname ${BASH_SOURCE[0]})
pdns=${1}

image=quay.io/kpfleming/apaa-test-images:tox

c=$(buildah from debian:buster)

buildcmd() {
    buildah run ${c} -- "$@"
}

buildah config --workingdir /root ${c}

buildcmd apt-get update
buildcmd apt-get install --yes --quiet=2 git

buildcmd apt-get install --yes --quiet=2 build-essential libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
for pyver in 3.5.9 3.6.11 3.7.8 3.8.4; do
    wget -O - https://www.python.org/ftp/python/${pyver}/Python-${pyver}.tgz | buildcmd tar xzf -
    buildah config --workingdir /root/Python-${pyver} ${c}
    buildcmd ./configure --enable-optimizations
    buildcmd make altinstall
    buildah config --workingdir /root ${c}
    buildcmd rm -rf /root/Python-${pyver}
done

buildcmd pip3.8 install tox
buildah copy ${c} tox.ini
buildcmd tox -eALL --notest --workdir /root/tox

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
