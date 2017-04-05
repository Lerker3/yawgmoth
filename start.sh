#!/bin/sh

export PYTHONIOENCODING=utf-8

while true; do
    python3 ~/testGIT/yawgmoth/src/yawgmoth.py
    RETURNCODE=$?
    echo $RETURNCODE
    if [ $RETURNCODE -ne 2 ] && [ $RETURNCODE -ne 3 ]; then
        exit 0
    fi
    sleep 2
    if [ $RETURNCODE -eq 2 ]; then
        echo Attempting Git Pull
        git pull
    fi
    if [ $RETURNCODE -eq 3 ]; then
        echo Reboot No Git
    fi
    sleep 5
done
