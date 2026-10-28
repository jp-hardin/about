"""Removes camera, editing, and author metadata from the site's images without re-encoding them.

  python3 strip_meta.py <folder>

JPEG: drops EXIF/XMP (APP1), Photoshop/IPTC (APP13), APP12 and comments; keeps JFIF, the colour profile (APP2) and
Adobe colour info (APP14). PNG: drops text, EXIF and time chunks. WebP: drops EXIF and XMP chunks. Pixels are untouched.
"""
import os
import struct
import sys


def jpeg(b):
    if b[:2] != b"\xff\xd8":
        return b
    out, i = [b[:2]], 2
    while i < len(b) - 1:
        if b[i] != 0xFF:
            return b
        marker = b[i + 1]
        if marker == 0xDA:                       # start of scan: the rest is image data
            out.append(b[i:])
            break
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            out.append(b[i:i + 2]); i += 2; continue
        size = struct.unpack(">H", b[i + 2:i + 4])[0]
        seg = b[i:i + 2 + size]
        if marker in (0xE1, 0xEC, 0xED, 0xFE):   # APP1, APP12, APP13, COM
            pass
        else:
            out.append(seg)
        i += 2 + size
    return b"".join(out)


def png(b):
    if b[:8] != b"\x89PNG\r\n\x1a\n":
        return b
    out, i = [b[:8]], 8
    while i < len(b):
        n = struct.unpack(">I", b[i:i + 4])[0]
        kind = b[i + 4:i + 8]
        chunk = b[i:i + 12 + n]
        if kind not in (b"tEXt", b"zTXt", b"iTXt", b"eXIf", b"tIME"):
            out.append(chunk)
        i += 12 + n
    return b"".join(out)


def webp(b):
    if b[:4] != b"RIFF" or b[8:12] != b"WEBP":
        return b
    chunks, i = [], 12
    while i < len(b):
        kind, n = b[i:i + 4], struct.unpack("<I", b[i + 4:i + 8])[0]
        chunks.append((kind, b[i:i + 8 + n + (n & 1)]))
        i += 8 + n + (n & 1)
    kept = []
    for kind, c in chunks:
        if kind in (b"EXIF", b"XMP "):
            continue
        if kind == b"VP8X":
            c = c[:8] + bytes([c[8] & ~0x0C]) + c[9:]   # clear the EXIF and XMP flags
        kept.append(c)
    body = b"WEBP" + b"".join(kept)
    return b"RIFF" + struct.pack("<I", len(body)) + body


def main(folder):
    changed = 0
    for d, _, files in os.walk(folder):
        for f in files:
            path, ext = os.path.join(d, f), f.lower().rsplit(".", 1)[-1]
            fn = {"jpg": jpeg, "jpeg": jpeg, "png": png, "webp": webp}.get(ext)
            if not fn:
                continue
            with open(path, "rb") as fh:
                b = fh.read()
            nb = fn(b)
            if nb != b:
                with open(path, "wb") as fh:
                    fh.write(nb)
                changed += 1
                print("stripped", os.path.relpath(path, folder), len(b) - len(nb), "bytes")
    print(changed, "images changed")


if __name__ == "__main__":
    main(sys.argv[1])
