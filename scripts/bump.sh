#!/bin/bash

set -e

git checkout -b bump
pip-compile --upgrade requirements.in
pip install -r requirements.txt
python manage.py test
git add requirements.txt
git commit -m'Bump requirements'
git show
git push -u origin bump
git checkout master
git branch -D bump
