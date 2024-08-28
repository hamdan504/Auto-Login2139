#!/bin/bash
# Setup Python environment
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright
pip install playwright

# Download Chromium binary
CHROMIUM_URL="https://playwright.azureedge.net/builds/chromium/1045/chromium-linux.zip"
mkdir -p /tmp/chromium
curl -L $CHROMIUM_URL | unzip -q -d /tmp/chromium -

# Set executable permissions
chmod +x /tmp/chromium/chrome-linux/chrome