#!/bin/sh
# Rebuilds the site page, page images and downloadable PDF from brief.pptx. See README.md.
set -e
cd "$(dirname "$0")/.."
python3 brief.py "$(basename "$(dirname "$0")")"
