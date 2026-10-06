#!/bin/sh
# Rebuilds the site page and the downloadable PDF from content.md.
set -e
cd "$(dirname "$0")"
python3 web.py
python3 pdf.py
