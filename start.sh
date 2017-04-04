#!/bin/sh

export PYTHONIOENCODING=utf-8

while true; do
    python3 src/yawgmoth.py
    RETURNCODE=$?
    echo $RETURNCODE
    if [ $RETURNCODE -ne 2 ]; then
        exit 0
    fi
    sleep 2
    echo Attempting Git Pull
    git pull
    sleep 5
done