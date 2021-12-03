#!/bin/sh

apk update
apk add nano bash gcc musl-dev libffi-dev git python3 python3-dev

mkdir /mnt/gdrive-nfd-check
cd /mnt/gdrive-nfd-check

git clone https://github.com/szpeter80/gdrive-nfd-check .

cd setup
./setup.sh

