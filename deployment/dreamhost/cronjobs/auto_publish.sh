#!/bin/bash

source $HOME/sites/cppquiz.org/venv/bin/activate || exit $?
python $HOME/sites/cppquiz.org/cppquiz/manage.py auto_publish || exit $?

