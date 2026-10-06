# Draws the cover and the four segment illustrations used by the PDF. Run from this folder: python3 mkart.py
G = '#B68757'; W = '#D9D3CA'; BG = '#2E2E2E'
def g(inner, x, y, s=1):
    return f'<g transform="translate({x},{y}) scale({s})" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{inner}</g>'
# Icons are drawn on a 160 x 160 grid.
food = (f'<path d="M54 22h14v20l8 14v70a6 6 0 0 1-6 6H52a6 6 0 0 1-6-6V56l8-14z" stroke="{W}"/>'
        f'<path d="M46 82h30M46 106h30M54 32h14" stroke="{W}"/>'
        f'<path d="M114 136V58" stroke="{G}"/>'
        f'<path d="M114 58c-6-9-6-18 0-27c6 9 6 18 0 27M114 78c-11-3-14-11-14-19c9 2 13 9 14 19M114 78c11-3 14-11 14-19c-9 2-13 9-14 19'
        f'M114 100c-11-3-14-11-14-19c9 2 13 9 14 19M114 100c11-3 14-11 14-19c-9 2-13 9-14 19'
        f'M114 122c-11-3-14-11-14-19c9 2 13 9 14 19M114 122c11-3 14-11 14-19c-9 2-13 9-14 19" stroke="{G}"/>')
brands = (f'<path d="M36 58h80l8 76H28z" stroke="{W}"/><path d="M58 58V46a18 18 0 0 1 36 0v12" stroke="{W}"/>'
          f'<path d="M76 80l5.5 11.5 12.5 1.5-9.3 8.6 2.6 12.4L76 107.8 64.700 114l2.600-12.400L58 93l12.500-1.500z" stroke="{G}"/>'
          f'<path d="M124 30l14 14M138 30l-14 14M131 26v22M120 37h22" stroke="{G}" stroke-width="1.6"/>')
service = (f'<rect x="16" y="50" width="80" height="58" rx="3" stroke="{W}"/><path d="M96 68h26l20 22v18H96z" stroke="{W}"/>'
           f'<path d="M106 78h13l9 11h-22z" stroke="{W}"/><path d="M16 108h126" stroke="{W}"/>'
           f'<circle cx="46" cy="114" r="11" stroke="{G}" fill="{BG}"/><circle cx="118" cy="114" r="11" stroke="{G}" fill="{BG}"/>'
           f'<path d="M44 62v30M38 62v9a6 6 0 0 0 12 0v-9M66 92V62c9 4 9 17 0 21" stroke="{G}"/>')
store = (f'<path d="M28 72v60h104V72" stroke="{W}"/><path d="M24 44h112l8 26H16z" stroke="{W}"/>'
         f'<path d="M16 70a12.8 12.8 0 0 0 25.600 0a12.800 12.800 0 0 0 25.600 0a12.800 12.800 0 0 0 25.600 0a12.800 12.800 0 0 0 25.600 0a12.800 12.800 0 0 0 25.600 0" stroke="{G}"/>'
         f'<path d="M68 132V100h24v32" stroke="{W}"/><rect x="38" y="96" width="20" height="18" stroke="{W}"/><rect x="102" y="96" width="20" height="18" stroke="{W}"/>'
         f'<path d="M60 30h40" stroke="{G}" stroke-width="4"/><circle cx="86" cy="116" r="1.6" stroke="{G}"/>')
icons = [('food', food), ('brands', brands), ('service', service), ('store', store)]
c = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 816 590" width="816" height="590"><rect width="816" height="590" fill="{BG}"/>']
for k in range(0, 17):
    c.append(f'<path d="M{k * 51} 0V590" stroke="#383838" stroke-width="1"/>')
c.append('<path d="M0 316h816" fill="none" stroke="#4A4338" stroke-width="2"/>')
for i, (_, ic) in enumerate(icons):
    c.append(g(ic, 48 + i * 180 + 10, 168, 1.0))
c.append('</svg>')
open('art/cover.svg', 'w').write(''.join(c))
for name, ic in icons:
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 236 112" width="236" height="112"><rect width="236" height="112" fill="{BG}"/>'
         + g(ic, 74, 6, 0.62) + f'<path d="M14 92h46M176 92h46" stroke="{G}" stroke-width="1.5"/></svg>')
    open(f'art/{name}.svg', 'w').write(s)
print('wrote art/cover.svg and', len(icons), 'segment illustrations')
