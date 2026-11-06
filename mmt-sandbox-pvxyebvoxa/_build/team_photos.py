#!/usr/bin/env python3
"""Optimizes the Middle Market team photo shoot for the site.

Usage: python3 team_photos.py <folder of original JPEGs>

The originals live in the "MMT Team Images For Website" folder on Google Drive (3000x2000 camera JPEGs, about
1 MB each) and are not kept in the repository. For each photo this writes two WebP files to
assets/img/team-photos/, with the camera data (EXIF, GPS, camera settings) removed and the orientation applied:

    <name>.webp      2000 px on the long side, for full-width banners and heroes
    <name>-sm.webp   1000 px on the long side, for cards, grids and side images

and lists every photo with its size and orientation in assets/img/team-photos/photos.json. Reruns skip
photos that are already done.
"""
import json
import os
import sys

from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'assets', 'img', 'team-photos')
SIZES = (('', 2000, 80), ('-sm', 1000, 78))


def main(src):
    os.makedirs(OUT, exist_ok=True)
    manifest_path = os.path.join(OUT, 'photos.json')
    manifest = {p['name']: p for p in json.load(open(manifest_path))} if os.path.exists(manifest_path) else {}
    for fn in sorted(os.listdir(src)):
        if not fn.lower().endswith(('.jpg', '.jpeg')):
            continue
        name = os.path.splitext(fn)[0].lower()
        if name in manifest and all(os.path.exists(os.path.join(OUT, name + s + '.webp')) for s, _, _ in SIZES):
            continue
        im = ImageOps.exif_transpose(Image.open(os.path.join(src, fn))).convert('RGB')
        entry = {'name': name, 'orientation': 'landscape' if im.width > im.height else 'portrait' if im.height > im.width else 'square'}
        for suffix, edge, quality in SIZES:
            copy = im.copy()
            copy.thumbnail((edge, edge), Image.LANCZOS)
            path = os.path.join(OUT, name + suffix + '.webp')
            copy.save(path, 'WEBP', quality=quality, method=6)  # no exif= argument, so no camera data is written
            entry['large' if not suffix else 'small'] = {'file': name + suffix + '.webp', 'width': copy.width,
                                                          'height': copy.height, 'bytes': os.path.getsize(path)}
        manifest[name] = entry
        print('wrote', name, entry['large']['bytes'] // 1024, 'KB +', entry['small']['bytes'] // 1024, 'KB')
    json.dump(sorted(manifest.values(), key=lambda p: p['name']), open(manifest_path, 'w'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1])
