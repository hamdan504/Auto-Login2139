#!/bin/bash
# Setup Python environment
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install asgiref

# Install Playwright and browser
pip install playwright
playwright install-deps
playwright install chromium