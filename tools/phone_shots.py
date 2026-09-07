"""Render the landing on an iPhone 13 profile and save one screenshot per screen-height of scroll,
plus a full-page capture. Scratch tool for the 7-Sep phone work; not part of the suite.

usage: python3 tools/phone_shots.py OUTDIR [URL] [--desktop]
"""
import sys, os, time
from playwright.sync_api import sync_playwright

out = sys.argv[1]
url = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else 'http://127.0.0.1:8765/index.html'
desktop = '--desktop' in sys.argv
os.makedirs(out, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    if desktop:
        ctx = browser.new_context(viewport={'width': 1440, 'height': 900}, device_scale_factor=1)
    else:
        dev = p.devices['iPhone 13']
        ctx = browser.new_context(**dev)
    page = ctx.new_page()
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto(url, wait_until='networkidle')
    time.sleep(1.5)
    vh = page.evaluate('window.innerHeight')
    vw = page.evaluate('window.innerWidth')
    total = page.evaluate('document.documentElement.scrollHeight')
    sw = page.evaluate('document.documentElement.scrollWidth')
    print(f'viewport {vw}x{vh}  page {sw}x{total}  screens {total/vh:.1f}')
    # where the pieces sit, in page pixels, so "does the field fit one screen" is a number
    boxes = page.evaluate('''() => { const q = s => { const e = document.querySelector(s); if (!e) return null;
        const r = e.getBoundingClientRect(); return [Math.round(r.top + scrollY), Math.round(r.bottom + scrollY), Math.round(r.width)]; };
        return { hero_copy: q('.hero-copy'), story_title: q('.hero-story'), card: q('.ffcard'), axis: q('.ffx-axis'),
                 our_read: q('.our-read'), story_cta: q('.story-cta'), p3: q('#read'), marquee: q('.marquee'), footer: q('footer') }; }''')
    for k, v in boxes.items():
        if v: print(f'  {k:12s} top {v[0]:5d}  bottom {v[1]:5d}  height {v[1]-v[0]:4d}  width {v[2]}')
    y = 0; i = 0
    while y < total:
        page.evaluate(f'window.scrollTo(0,{y})')
        time.sleep(2.4)   # page 3's blocks arrive over 1.8s once in view
        page.screenshot(path=f'{out}/s{i:02d}_y{y}.png')
        i += 1
        y += vh
        total = page.evaluate('document.documentElement.scrollHeight')
    page.evaluate('window.scrollTo(0,0)'); time.sleep(0.4)
    print('errors:', errors or 'none')
    print('shots:', i)
    browser.close()
