#!/bin/bash

exec pdns_server --no-config --daemon --api --api-key=foo --disable-syslog --local-port=55353 --launch=random --socket-dir=/run
