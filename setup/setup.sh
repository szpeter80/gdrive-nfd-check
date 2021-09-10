#!/bin/bash
mkdir ../reports
python3 -m venv ../project-venv
. ../project-venv/bin/activate
pip install -r ./requirements.txt