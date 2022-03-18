#!/usr/bin/env bash

echo starting Python build in "${1}"

set -x

cd "${1}" || exit
./configure --disable-shared
make -j2 altinstall
