#!/usr/bin/env -S bash -xe

root=$(dirname ${BASH_SOURCE[0]})

image=docker.io/kpfleming/apaz-test-images:pdns4.3-python3

c=$(buildah from debian:buster)

buildah run ${c} -- apt update
buildah run ${c} -- apt install --yes gnupg python3 python3-venv git

buildah add ${c} ${root}/apt-repo-pdns-auth-43.list /etc/apt/sources.list.d
buildah add ${c} ${root}/apt-pref-pdns /etc/apt/preferences.d
curl https://repo.powerdns.com/FD380FBB-pub.asc | buildah run ${c} -- apt-key add
buildah run ${c} -- apt update
buildah run ${c} -- apt install --yes pdns-server

buildah run ${c} -- python3 -m venv /ansible
buildah run ${c} -- /ansible/bin/pip install wheel
buildah run ${c} -- /ansible/bin/pip install ansible
buildah run ${c} -- /ansible/bin/pip install bravado

buildah run ${c} -- rm -rf /var/lib/apt/lists/*
buildah run ${c} -- rm -rf /root/.cache

buildah rmi ${image}
buildah commit --squash --rm ${c} ${image}
