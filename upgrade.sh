#!/bin/bash
cd "$(dirname "$0")"

echo "## Installing from requirements.txt"
pip install -r requirements.txt --upgrade -t ../lib/python2.7
echo "## Version is now"
python ../lib/python2.7/django/bin/django-admin.py --version
echo "## Restarting apache"
../apache2/bin/restart
