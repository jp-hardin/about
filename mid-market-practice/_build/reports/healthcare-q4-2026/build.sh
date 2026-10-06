#!/bin/sh
# Rebuilds the print layout, the downloadable PDF and the site page.
set -e
cd "$(dirname "$0")"
python3 gen.py
python3 pdf.py
python3 web.py
