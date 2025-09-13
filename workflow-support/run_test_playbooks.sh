#!/bin/bash

set -e # in order to fail on any playbook

ansible-playbook -i localhost, workflow-support/ansible-"${1}"/test-tsigkey.yml
ansible-playbook -i localhost, workflow-support/ansible-"${1}"/test-zone.yml
ansible-playbook -i localhost, workflow-support/ansible-"${1}"/test-zone-issue-136.yml
ansible-playbook -i localhost, workflow-support/ansible-"${1}"/test-zone-rrset.yml
ansible-playbook -i localhost, workflow-support/ansible-"${1}"/test-rrset-record.yml
ansible-playbook -i localhost, workflow-support/ansible-"${1}"/test-cryptokey.yml
