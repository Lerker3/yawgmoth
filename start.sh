#!/bin/sh

export PYTHONIOENCODING=utf-8

while true; do
    python2 src/yawgmoth.py $1 $2
    RETURNCODE=$?
    echo $RETURNCODE
    if [ $RETURNCODE -ne 2 ]; then
        exit 0
    fi
    git pull
done

