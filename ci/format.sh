#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR=$SCRIPT_DIR/..

cd $ROOT_DIR || exit $?

EXCLUDES=$(tr '\n' ',' < .gitignore)
EXCLUDES="$EXCLUDES,.*/migrations"

if [ "$1" == "--fix" ]; then
    autopep8 --in-place --recursive --exclude $EXCLUDES . || exit $?
fi

autopep8 --diff --recursive --exit-code --exclude $EXCLUDES . || exit $?
