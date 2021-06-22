#!/bin/sh

APPLIANCES='tests/appliances/yolk.py2.md tests/appliances/yolk.py3.md'
if [ -x ./bin/yolk-c ]; then
    # Testing the RPython-built executable is still disabled, but at least
    # we now know a little more about why it only passes 14 of the 45 tests.
    #
    # It appears to be the case that RPython is just dismal at recursion,
    # and the Yolk evaluator is highly recursive.  So the compiled executable
    # sometimes fails with "Fatal RPython error: MemoryError", but more often,
    # just segfaults.
    #
    # To make this work, we would need to rewrite the evaluation function in
    # an iterative style.
    #
    # Some work in that direction -- or vaguely in that direction -- has been
    # done in the Scheme implementation -- namely, rewriting the evaluator
    # in continuation-passing style -- but that's just a sketch and would
    # still require defunctionalization/trampolining afterwards, as RPython
    # can't handle function values.
    #
    # APPLIANCES="$APPLIANCES tests/appliances/yolk-c.md"
    echo 'pass' >/dev/null
fi

falderal $APPLIANCES README.md $*
