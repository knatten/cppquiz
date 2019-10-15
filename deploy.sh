#!/bin/bash

usage() {
    echo "USAGE: $0 [beta|prod]"
}

deploy() {
    site=$1
    if [ "$site" == "prod" ]; then
        dir="/home/riktigbil/webapps/cppquiz_prod/cppquiz"
    else
        dir="/home/riktigbil/webapps/cppquiz_beta/cppquiz"
    fi
    ssh -X riktigbil@cppquiz.org "cd $dir && git pull && python3.6 manage.py migrate && python3.6 manage.py collectstatic --noinput && ../apache2/bin/restart"
}

if [ $# -ne 1 ]; then
    usage || exit 1
fi

site=$1

if [ $(git rev-parse --abbrev-ref HEAD) != "master" ]; then
    echo "You're not on master!"
    exit 1
fi

if [[ "$site" =~ ^(beta|prod)$ ]]; then
    python3.6 manage.py test || exit 1
    deploy $site || exit $?
else
    echo "Unknown site $site" || exit 1
fi
