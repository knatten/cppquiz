#!/bin/bash

source $HOME/cppquiz.org/venv/bin/activate || exit $?
python $HOME/cppquiz.org/cppquiz/manage.py dump_published_questions > $HOME/cppquiz.org/public/static/published.json || exit $?

