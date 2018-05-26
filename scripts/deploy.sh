#! /bin/sh

set -eux

ansible-playbook -i scripts/inventory.ini scripts/deploy.yml
