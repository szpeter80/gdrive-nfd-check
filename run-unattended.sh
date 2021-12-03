#!/bin/bash

LOG_FN=$(date "+report__%Y_%m_%d__%H_%M.txt")

# shellcheck disable=SC1091
. ./project-venv/bin/activate
python ./nfd-checker.py  --print_tree --debug --no-dry_run 2>&1 | tee "./reports/$LOG_FN"
deactivate
