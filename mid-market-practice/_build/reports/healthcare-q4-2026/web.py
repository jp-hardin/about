import re,os
ROOT=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(ROOT,'preview.html')).read()
body=src[src.index('<body>')+6:src.rindex('</body>')]
# drop the one-pager (last .pg, data-fn ONEPAGER)
i=body.find('<div class="pg" data-fn="ONEPAGER"'); body=body[:i] if i>=0 else body
m={'/_blob/0ec74a82d64ca48c5a0589fe8fbe222d':'img/knot.png','/_blob/4dd1bb932520e4f56865210abba6a736':'../assets/img/brand/benchmark-logo-white.png','/_blob/70432026c2e1430aa486f0faff90dbbc':'../assets/img/team/jared-hardin.jpg','art/':'img/'}
for k,v in m.items(): body=body.replace(k,v)
# remove the two illustrations that have no local file
body,n1=re.subn(r'<div style="width: 280px; position: relative"><img src="/_blob/1d7f[^>]*><div[^>]*></div></div>','',body)
body=body.replace('<div style="width: 408px; display: flex; flex-direction: column; gap: 14px; text-align: justify">','<div style="width: 720px; display: flex; flex-direction: column; gap: 14px; text-align: justify">')
body,n2=re.subn(r'<div style="width: 344px; display: flex; flex-direction: column">\s*<img src="/_blob/1053[^>]*>\s*<div[^>]*></div>\s*</div>','',body)
assert n1==1 and n2==1,(n1,n2); assert '/_blob/' not in body
body=body.replace('object-fit: cover','object-fit: cover').replace('border-radius: 50%">','border-radius: 50%; object-fit: cover">')
body=re.sub(r'<a href="(https?://[^"]+)"',r'<a target="_blank" rel="noopener" href="\1"',body)
body=body.replace('<div class="pg"','<section class="pg"').replace('; page-break-after: always">','">')
# sections were closed with </div>; rebuild by splitting
parts=body.split('<section class="pg"')[1:]
out=[]
for p in parts:
    p=p.rstrip(); assert p.endswith('</div>'); out.append('<section class="pg"'+p[:-6]+'</section>')
doc=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Healthcare Q4 2026 M&amp;A Sector Report | Mid-Market | Benchmark International</title>
<meta name="description" content="Benchmark International Mid-Market: Q4 2026 M&amp;A sector report for healthcare providers, life sciences and diagnostics, medical products and distribution, and pharmacy and healthcare services.">
<meta name="theme-color" content="#231f20">
<link rel="icon" href="../assets/img/brand/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500&family=Newsreader:ital,opsz,wght@0,6..72,500;0,6..72,600;1,6..72,500;1,6..72,600&family=Quicksand:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
html{{background:#231f20}}
body{{margin:0;background:#231f20;font-family:'Quicksand','Avenir Next','Segoe UI',sans-serif}}
.bar{{position:sticky;top:0;z-index:5;display:flex;justify-content:space-between;align-items:center;gap:16px;padding:12px 20px;background:#231f20;border-bottom:1px solid #3a3536;font-size:12px;font-weight:700;letter-spacing:1.6px;text-transform:uppercase}}
.bar a{{color:#bc9163;text-decoration:none}} .bar a:hover{{color:#fff}}
.bar .cta{{border:2px solid #bc9163;padding:8px 14px;color:#fff;background:#bc9163}}
.stack{{display:flex;flex-direction:column;align-items:center;gap:18px;padding:24px 12px 48px}}
.fit{{width:816px}}
.pg{{display:block;box-shadow:0 2px 18px rgba(0,0,0,.45)}}
.pg a{{color:#8C6239;text-decoration-thickness:.5px;text-underline-offset:2px}} .pg a:hover{{color:#5E4126}}
.pg + .pg{{margin-top:18px}}
@media print{{html,body{{background:#fff}}.bar{{display:none}}.stack{{padding:0;gap:0}}.fit{{zoom:1!important}}.pg{{box-shadow:none;margin:0!important;page-break-after:always}}@page{{size:8.5in 11in;margin:0}}}}
</style>
</head>
<body>
<div class="bar"><a href="../industries/healthcare.html">&larr; Healthcare</a><a class="cta" href="../index.html#form">Start the Conversation</a></div>
<main class="stack"><div class="fit" id="fit">
{chr(10).join(out)}
</div></main>
<script>
(function(){{var f=document.getElementById('fit');function z(){{var s=Math.min(1,(document.documentElement.clientWidth-24)/816);f.style.zoom=s;}}z();window.addEventListener('resize',z);}})();
</script>
</body>
</html>
'''
open(os.path.join(ROOT,'..','..','..','reports','healthcare-q4-2026.html'),'w').write(doc)
print(len(out),'pages',round(len(doc)/1024),'KB')
