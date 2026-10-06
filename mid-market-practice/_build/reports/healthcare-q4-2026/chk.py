import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/opt/pw-browsers/chromium' if __import__('os').path.isfile('/opt/pw-browsers/chromium') else None)
        pg=await b.new_page(viewport={'width':816,'height':1056})
        await pg.goto('file://'+__import__('os').path.abspath('preview.html')); await pg.wait_for_timeout(2500)
        r=await pg.evaluate('''()=>[...document.querySelectorAll('.pg')].map(p=>{const f=p.querySelector('[data-fit]');let last=0;f.querySelectorAll('*').forEach(e=>{const r=e.getBoundingClientRect();if(r.height&&r.width)last=Math.max(last,r.bottom)});const fr=f.getBoundingClientRect();let right=0;p.querySelectorAll('[data-fit] *').forEach(e=>{const r=e.getBoundingClientRect();right=Math.max(right,r.right-p.getBoundingClientRect().left)});return [p.dataset.fn,+f.dataset.fit,Math.round(last-fr.top),Math.round(right)]})''')
        for x in r: print(x, 'OVER' if x[2]>x[1] or x[3]>770 else '')
        if len(sys.argv)>1:
            await pg.pdf(path='out.pdf',width='8.5in',height='11in',print_background=True)
            for i in [int(a) for a in sys.argv[1:]]:
                await pg.locator('.pg').nth(i).screenshot(path=f'shot{i}.png')
        await b.close()
asyncio.run(main())
