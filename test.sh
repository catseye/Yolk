#!/bin/sh

FIXTURES=''
if [ ! `which rpython`X = X ]; then
    FIXTURES="$FIXTURES fixtures/rpython-fixture.markdown"
    if [ ! -e ./yolk-c ]; then
        ./build.sh || exit $?
    fi
fi

falderal $FIXTURES README.markdown $*
