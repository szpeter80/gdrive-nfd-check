#!/bin/bash
. ../project-venv/bin/activate

PKG_LIST=$(pip list --outdated | cut -d ' ' -f 1 | tail -n +3)

for x in $PKG_LIST;
do
    pip install --upgrade $x
done

deactivate