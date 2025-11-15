#!/bin/bash

pdns_ver=${1}

exec /pdns/"${pdns_ver}"/pdns_server
