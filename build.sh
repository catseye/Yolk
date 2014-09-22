#!/bin/sh

if [ `which rpython`X = X ]; then
    echo 'RPython not found.  Not building.  Use CPython instead.'
else
    rpython src/yolk.py
fi
