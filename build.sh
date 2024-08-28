#!/bin/bash
# Setup Python environment
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt