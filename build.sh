#!/bin/bash
# Setup Python environment
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright
pip install playwright

# Download and install Chromium
mkdir -p /tmp/chromium
playwright install chromium
playwright install-deps

# Move Chromium to the correct location
mv /home/sbx_user1051/.cache/ms-playwright/chromium-*/chrome-linux/* /tmp/chromium/

# Set executable permissions
chmod +x /tmp/chromium/chrome