#!/bin/sh

APPLIANCES='tests/appliances/yolk.py2.md tests/appliances/yolk.py3.md'
if [ -x ./bin/yolk-c ]; then
    APPLIANCES="$APPLIANCES tests/appliances/yolk-c.md"
fi

falderal $APPLIANCES README.md $*
