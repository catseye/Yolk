#!/bin/sh

FIXTURES=''
if [ ! `which rpython`X = X ]; then
    if [ ! -e ./yolk-c ]; then
        ./build.sh || exit $?
    fi
    # Testing the RPython-built executable is disable until someone has
    # the time and inclination to hunt down why it always hangs and fixes it.
    #FIXTURES="$FIXTURES fixtures/rpython-fixture.markdown"
fi

falderal --substring-error $FIXTURES README.markdown $*
