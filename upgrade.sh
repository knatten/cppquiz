#!/bin/bash
cd "$(dirname "$0")"

echo "## Installing from requirements.txt"
pip3.6 install -r requirements.txt --upgrade -t ../lib/python3.6
echo "## Version is now"
python3.6 ../lib/python3.6/django/bin/django-admin.py --version
echo "## Restarting apache"
../apache2/bin/restart
