G='#B68757'; W='#D9D3CA'; BG='#2E2E2E'
def g(inner,x,y,s=1): return f'<g transform="translate({x},{y}) scale({s})" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{inner}</g>'
# icons drawn in 160x160
prov=f'''<rect x="30" y="38" width="100" height="92" rx="4" stroke="{W}"/><path d="M30 62h100" stroke="{W}"/><path d="M70 130v-26h20v26" stroke="{W}"/><path d="M80 14v20M70 24h20" stroke="{G}" stroke-width="5"/><path d="M40 86h18l7-14 10 26 8-18 5 6h32" stroke="{G}"/><circle cx="46" cy="50" r="3" stroke="{W}"/><circle cx="58" cy="50" r="3" stroke="{W}"/>'''
life=f'''<path d="M62 22h36M70 22v38l-30 56a10 10 0 0 0 9 15h62a10 10 0 0 0 9-15L90 60V22" stroke="{W}"/><path d="M52 100h56" stroke="{G}"/><circle cx="70" cy="112" r="4" stroke="{G}"/><circle cx="88" cy="118" r="3" stroke="{G}"/><circle cx="82" cy="104" r="2.5" stroke="{G}"/><path d="M126 30v52a9 9 0 0 0 18 0V30M122 30h26M126 60h18" stroke="{G}"/><path d="M14 44c10 0 10 14 20 14M14 58c10 0 10-14 20-14M14 72c10 0 10 14 20 14M14 86c10 0 10-14 20-14" stroke="{W}"/>'''
prod=f'''<rect x="22" y="30" width="116" height="78" rx="6" stroke="{W}"/><path d="M34 72h20l8-20 12 38 10-28 6 10h36" stroke="{G}"/><path d="M60 108v18M100 108v18M46 128h68" stroke="{W}"/><circle cx="124" cy="44" r="4" stroke="{G}"/><path d="M34 44h30" stroke="{W}"/><path d="M118 132l22 16M136 132l-14 16" stroke="{G}"/>'''
phar=f'''<rect x="34" y="46" width="62" height="88" rx="6" stroke="{W}"/><rect x="42" y="28" width="46" height="18" rx="3" stroke="{W}"/><path d="M34 74h62M34 108h62" stroke="{W}"/><path d="M65 81v20M55 91h20" stroke="{G}" stroke-width="4"/><g transform="rotate(-35 122 96)"><rect x="100" y="84" width="48" height="24" rx="12" stroke="{G}"/><path d="M124 84v24" stroke="{G}"/></g><circle cx="120" cy="46" r="12" stroke="{G}"/><path d="M112 54l16-16" stroke="{G}"/>'''
icons=[prov,life,prod,phar]
# cover 816x590
c=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 816 590" width="816" height="590"><rect width="816" height="590" fill="{BG}"/>']
for k in range(0,17): c.append(f'<path d="M{k*51} 0V590" stroke="#383838" stroke-width="1"/>')
c.append(f'<path d="M0 262h160l14-30 22 62 18-46 12 14h150l14-30 22 62 18-46 12 14h150l14-30 22 62 18-46 12 14h158" fill="none" stroke="#4A4338" stroke-width="2"/>')
for i,ic in enumerate(icons): c.append(g(ic,48+i*180+10,168,1.0))
c.append('</svg>'); open('art/cover.svg','w').write(''.join(c))
alts=['clinic','lab','device','pharmacy']
for i,ic in enumerate(icons):
    s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 236 112" width="236" height="112"><rect width="236" height="112" fill="{BG}"/>'+g(ic,74,6,0.62)+f'<path d="M14 92h46M176 92h46" stroke="{G}" stroke-width="1.5"/></svg>'
    open(f'art/{alts[i]}.svg','w').write(s)
