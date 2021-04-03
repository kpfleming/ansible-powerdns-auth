#!/usr/bin/env bash

set -ex

sudo apt-get remove buildah
sudo apt-get -y install software-properties-common
sudo add-apt-repository -y ppa:alexlarsson/flatpak
sudo apt-get -y -qq update
sudo apt-get -y install bats libapparmor-dev libdevmapper-dev libglib2.0-dev libgpgme11-dev libseccomp-dev libselinux1-dev skopeo-containers go-md2man
sudo apt-get -y install golang-1.13
mkdir ~/buildah
pushd ~/buildah
export GOPATH=`pwd`
git clone https://github.com/containers/buildah ./src/github.com/containers/buildah
cd ./src/github.com/containers/buildah
git checkout release-1.19
PATH=/usr/lib/go-1.13/bin:$PATH make runc all SECURITYTAGS="apparmor seccomp"
sudo make install install.runc
buildah version
popd
