#!/bin/bash
mkdir ../reports
python3 -m venv ../project-venv
. ../project-venv/bin/activate
pip install -r ./requirements.txt

echo "The installation is complete. Don't forget to copy the setup/settings.yaml.example to settings.yaml and edit the app credentials."
