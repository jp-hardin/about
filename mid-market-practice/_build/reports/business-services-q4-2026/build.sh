#!/bin/sh
# Rebuilds the downloadable PDF and the site page from the print pages in pages/.
set -e
cd "$(dirname "$0")"
python3 pdf.py
python3 web.py
