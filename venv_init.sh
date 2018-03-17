#!/bin/sh

# Setup virtual environment
python3.7 -m venv venv-py37
. ./venv-py37/bin/activate

pip install -r requirements.txt

