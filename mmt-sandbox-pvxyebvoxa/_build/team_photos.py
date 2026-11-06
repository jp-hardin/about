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
# Crops for the photos placed on the site: (left, top, right, bottom, faces) as fractions of the original. Each
# starts just above the highest head and ends around the waist of the people in front; "faces" is the eye line.
# The site centers each crop on that line (object-position, stored as focus_y), so a thin, wide band shows the
# faces and a tall box shows heads to waist: whatever the screen's aspect ratio, nobody is cut off at the
# shoulders. Written as <name>-crop.webp (2000 px long side) and <name>-crop-sm.webp (1000 px).
CROPS = {
    'dsc07371': (0.0, 0.22, 1.0, 0.80, 0.38),   # standing group outside the office (default social image)
    'dsc06817': (0.0, 0.38, 1.0, 0.95, 0.64),   # home hero: the open office (no breakroom sign)
    'dsc07322': (0.0, 0.22, 1.0, 0.80, 0.38),   # home stats band: the full boardroom
    'dsc07199': (0.0, 0.05, 1.0, 0.85, 0.25),   # journey card 1: a one-on-one conversation
    'dsc06716': (0.0, 0.12, 1.0, 0.90, 0.30),   # journey card 2: analysis at the desk
    'dsc07004': (0.0, 0.12, 1.0, 0.92, 0.20),   # journey card 3 and hero slide: the deal team around the laptop (focus high so the standing heads stay in a thin band)
    'dsc07035': (0.00, 0.18, 1.00, 0.95, 0.38),   # Who We Help (portrait)
    'dsc07355': (0.00, 0.12, 1.00, 0.90, 0.26),   # home contact band
    'dsc07193': (0.0, 0.18, 1.0, 0.88, 0.37),   # closing band on other pages
    'dsc07343': (0.00, 0.16, 1.00, 0.85, 0.30),   # About hero: the team at the boardroom table
    'dsc07122': (0.0, 0.27, 1.0, 0.82, 0.47),   # Transactions hero: the boardroom
    'dsc06747': (0.0, 0.15, 1.0, 0.85, 0.38),   # Insights hero: research at the desk
    'dsc06809': (0.00, 0.15, 1.00, 0.90, 0.33),   # Industries hero: the open office (no breakroom sign)
    # Home hero carousel slides that appear nowhere else on the site
    'dsc07116': (0.0, 0.05, 1.0, 0.85, 0.25),   # Alexandra with two colleagues by the window
    'dsc07374': (0.0, 0.20, 1.0, 0.78, 0.40),   # the standing group, Alexandra in the center
    'dsc06680': (0.0, 0.05, 1.0, 0.85, 0.32),   # Alexandra smiling at her desk
    'dsc07005': (0.0, 0.20, 1.0, 0.95, 0.40),   # the full boardroom
    'dsc07187': (0.0, 0.15, 1.0, 0.90, 0.36),   # Alexandra at the table
    'dsc07178': (0.0, 0.15, 1.0, 0.90, 0.38),   # a meeting at the table
    # Third photo in each industry page's photo strip (4:3 boxes, close to the photos' own shape, so uncropped)
    'dsc07163': (0.0, 0.0, 1.0, 1.0, 0.28),     # Industrials: conversation at the window table
    'dsc07155': (0.0, 0.0, 1.0, 1.0, 0.33),     # Business Services: the boardroom, laughing
    'dsc07065': (0.0, 0.0, 1.0, 1.0, 0.35),     # Consumer: the lounge
    'dsc07345': (0.0, 0.0, 1.0, 1.0, 0.42),     # Healthcare: the team smiling at the table
    'dsc07033': (0.0, 0.0, 1.0, 1.0, 0.38),     # Technology: the group around the laptop
}


def main(src):
    os.makedirs(OUT, exist_ok=True)
    manifest_path = os.path.join(OUT, 'photos.json')
    manifest = {p['name']: p for p in json.load(open(manifest_path))} if os.path.exists(manifest_path) else {}
    for fn in sorted(os.listdir(src)):
        if not fn.lower().endswith(('.jpg', '.jpeg')):
            continue
        name = os.path.splitext(fn)[0].lower()
        if name in manifest and all(os.path.exists(os.path.join(OUT, name + s + '.webp')) for s, _, _ in SIZES) \
                and (manifest[name].get('crop_box') == list(CROPS.get(name, [])) or (name not in CROPS and 'crop' not in manifest[name])):
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
        if name in CROPS:
            entry['crop_box'] = list(CROPS[name])
            l, t, r, b, face = CROPS[name]
            entry['focus_y'] = round(100 * (face - t) / (b - t))
            crop = im.crop((round(l * im.width), round(t * im.height), round(r * im.width), round(b * im.height)))
            for suffix, edge, quality in (('-crop', 2000, 80), ('-crop-sm', 1000, 78)):
                copy = crop.copy()
                copy.thumbnail((edge, edge), Image.LANCZOS)
                path = os.path.join(OUT, name + suffix + '.webp')
                copy.save(path, 'WEBP', quality=quality, method=6)
                entry['crop' if suffix == '-crop' else 'crop_small'] = {'file': name + suffix + '.webp', 'width': copy.width,
                                                                       'height': copy.height, 'bytes': os.path.getsize(path)}
        manifest[name] = entry
        print('wrote', name, entry['large']['bytes'] // 1024, 'KB +', entry['small']['bytes'] // 1024, 'KB')
    json.dump(sorted(manifest.values(), key=lambda p: p['name']), open(manifest_path, 'w'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1])
