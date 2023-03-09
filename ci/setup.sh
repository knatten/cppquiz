#!/bin/bash

python -m pip install --upgrade pip || exit $?
pip install -r requirements.txt || exit $?
