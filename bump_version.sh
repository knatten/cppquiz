#!/bin/bash

if [ $# -ne 1 ]; then
    echo "USAGE: $0 <version>"
    exit 1
fi

VERSION=$1
TEMPLATE=templates/base.html

echo "Modifying template"
cat "$TEMPLATE" | sed -e "s/\(<\!-- version --> v\)[0-9][0-9]*\.[0-9][0-9]*/\1$VERSION/" > "$TEMPLATE.new" || exit 1
mv "$TEMPLATE.new" "$TEMPLATE" || exit 1

echo "Committing"
git checkout -b "bump-$VERSION"
git add "$TEMPLATE" || exit 1
git commit -v -m"Bumped version to $VERSION" || exit 1

echo
echo "--------------------------------------"
echo "Now make a PR, merge it, and do"
echo "git tag v$VERSION && git push origin v$VERSION"
echo "--------------------------------------"
echo
