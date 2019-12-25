#!/bin/bash

if [ $# != 1 ]; then
    echo "USAGE: $0 <python_version>  (e.g. $0 3.6)"
    exit 1
fi

VERSION=$1
PYTHON=python$1

cd "$(dirname "$0")" || exit $?

echo "## Installing from requirements.txt"
$PYTHON -m pip install -r requirements.txt --upgrade -t ../lib/$PYTHON || exit $?
echo "## Version is now"
$PYTHON ../lib/$PYTHON/django/bin/django-admin.py --version || exit $?
echo "## Restarting apache"
../apache2/bin/restart || exit $?
