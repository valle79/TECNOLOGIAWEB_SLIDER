#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Note: Database schema should be imported manually via Render's MySQL dashboard
echo "Build completed successfully!"
