#!/bin/bash

source $HOME/cppquiz.org/venv/bin/activate || exit $?
python $HOME/cppquiz.org/cppquiz/manage.py auto_publish || exit $?

