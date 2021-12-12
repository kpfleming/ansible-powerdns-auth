#!/usr/bin/env bash

echo starting Python build in ${1}

set -x

cd ${1}
./configure --disable-shared
make -j2 altinstall
