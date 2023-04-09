#!/bin/bash

ansible-playbook -i localhost, workflow-support/test-tsigkey.yml
ansible-playbook -i localhost, workflow-support/test-zone.yml
ansible-playbook -i localhost, workflow-support/test-zone-issue-136.yml
