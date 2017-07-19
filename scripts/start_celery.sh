#! /bin/bash
set -x

# export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
workon mycroft

eval $(./scripts/env_converter.py)

celery worker -A library -l info
