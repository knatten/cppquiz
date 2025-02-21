#!/bin/bash

source $HOME/sites/cppquiz.org/venv/bin/activate || exit $?
python $HOME/sites/cppquiz.org/cppquiz/manage.py dump_published_questions > $HOME/static.cppquiz.org/published.json || exit $?
python $HOME/sites/cppquiz.org/cppquiz/manage.py generate_feeds rss > $HOME/static.cppquiz.org/rss.xml || exit $?
python $HOME/sites/cppquiz.org/cppquiz/manage.py generate_feeds atom > $HOME/static.cppquiz.org/atom.xml || exit $?

