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
    'dsc06817': (0.0, 0.45, 1.0, 1.0, 0.62, 0.60),   # home hero: the open office (no breakroom sign)
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
    # Home hero carousel slides (appear nowhere else on the site). These start just above the highest head and the
    # carousel pins them to the top (object-position y 0), so on any screen the heads are in frame, at worst near
    # the bottom. The sixth value is where to center on narrow (phone) screens (in the image as shown, after any flip);
    # 'flip' mirrors the photo.
    'dsc07116': (0.0, 0.03, 1.0, 1.0, 0.25, 0.85),   # Alexandra with two colleagues by the window
    'dsc06557': (0.0, 0.05, 1.0, 1.0, 0.25, 0.68),   # Alex smiling at his desk
    'dsc07374': (0.0, 0.23, 1.0, 0.98, 0.40, 0.50),  # the standing group, Alexandra in the center
    'dsc07161': (0.0, 0.15, 1.0, 1.0, 0.35, 0.78),   # Alex at the boardroom table
    'dsc07005': (0.0, 0.24, 1.0, 1.0, 0.40, 0.50),   # the full boardroom
    'dsc06947': (0.0, 0.15, 1.0, 1.0, 0.30, 0.66),   # Jordan laughing at the table
    # Tall shots shown in place of the wide ones on phones and portrait tablets (one person each, so no one is sliced
    # at the sides); same rules: start just above the head, pinned to the top, centered on the person.
    'dsc06700': (0.0, 0.20, 1.0, 1.0, 0.40, 0.50),   # phone: the office
    'dsc07220': (0.0, 0.24, 1.0, 1.0, 0.40, 0.52),   # phone: Alexandra
    'dsc07245': (0.0, 0.20, 1.0, 1.0, 0.35, 0.50),   # phone: Alex
    'dsc07251': (0.0, 0.20, 1.0, 1.0, 0.35, 0.50),   # phone: colleague at the table
    'dsc07264': (0.0, 0.20, 1.0, 1.0, 0.35, 0.50),   # phone: colleague at the table
    'dsc07260': (0.0, 0.20, 1.0, 1.0, 0.35, 0.50),   # phone: colleague at the table
    'dsc06886': (0.0, 0.14, 1.0, 1.0, 0.30, 0.45),   # phone: Jordan at his desk
    'dsc07130': (0.0, 0.34, 1.0, 1.0, 0.48, 0.74),   # phone: Michael (right) with a colleague
    'dsc07204': (0.0, 0.08, 1.0, 1.0, 0.28, 0.66, 'flip'),   # Michael at the table, flipped so he sits clear of the hero text
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
            l, t, r, b, face = CROPS[name][:5]
            if 'flip' in CROPS[name][5:]:  # mirrored so the subject sits on the right, clear of the hero text
                im = ImageOps.mirror(im)
            entry['focus_y'] = round(100 * (face - t) / (b - t))
            fx = CROPS[name][5] if len(CROPS[name]) > 5 and not isinstance(CROPS[name][5], str) else 0.5
            entry['focus_x'] = round(100 * (fx - l) / (r - l))
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
