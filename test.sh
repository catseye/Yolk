#!/bin/sh

APPLIANCES='tests/appliances/yolk.py2.md tests/appliances/yolk.py3.md'
if [ ! `which rpython`X = X ]; then
    if [ ! -e ./yolk-c ]; then
        ./build.sh || exit $?
    fi
    # Testing the RPython-built executable is disable until someone has
    # the time and inclination to hunt down why it always hangs and fixes it.
    #APPLIANCES="$APPLIANCES tests/appliances/yolk-c.md"
fi

falderal $APPLIANCES README.md $*
