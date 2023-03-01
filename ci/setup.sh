#!/bin/bash

python -m pip install --upgrade pip || exit $?
pip install -r requirements.frozen.txt || exit $?
