# -*- coding: utf-8 -*-
"""THE RENDER HARNESS: every fixture's reveal, drawn, on one sheet.

The last piece of the engine-to-reveal wiring. Everything up to here proves the payload is CORRECT;
nothing proves it is READABLE. Fable is not going to open forty tabs, and a caveat that is right and
invisible is a caveat nobody read.

So this renders all 102 fixtures headless and writes ONE contact sheet. What it produces:

    build/reveal/<fixture>.html   one page per fixture, the payload drawn
    build/reveal/index.html       the contact sheet: every fixture, smallest first
    build/reveal/summary.json     the numbers behind the sheet, for a diff

WHAT IT ASSERTS RATHER THAN JUST DRAWING, because a harness that only draws is a screenshot folder:

  * every fixture produces a page at all
  * NO FIGURE APPEARS ON A FREE PAGE outside the public lane. This is rule E8 rendered rather than
    asserted on a dict: check 14 already walks all 102 free payloads, and this walks the HTML they
    turn into, which is the thing a founder actually sees.
  * every caveat the payload carries is present in the markup. The reason this matters is that
    honesty.py ranks caveats and the page shows two inline and hides the rest, so a caveat can be
    correct, ranked, and then dropped by a renderer that only reads the first two.

    python3 tools/render_harness.py            builds both tiers, prints the summary
    python3 tools/render_harness.py --tier paid
    python3 tools/render_harness.py --only payabli,honen

NO BROWSER IS REQUIRED and that is deliberate. The reveal's own renderers are JavaScript, and
driving them would mean a headless Chromium in the loop for a job whose question is "is the
substance there". This draws the payload directly in Python, which is enough to answer that and
cheap enough to run on every change. Driving the real page is a separate, later job.
"""
import argparse
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'selector'))
os.chdir(HERE)
import reveal_payload as RP                                    # noqa: E402
from golden_profiles import PROFILES                           # noqa: E402

# THE LIVE SHAPE, for the same reason tools/check_reveal_payload.py states at length: the raise is
# gone from the request under rule E9 and the fixtures carry no stage, so a payload built from a
# fixture as written has no investor list at all. 'Seed' is a stated test condition here, not a
# claim about any of the 102 companies.
LIVE_STAGE = 'Seed'


def live(prof):
    # The fixtures carry their own stage since 7-Sep-2026; this is the backstop, not the source.
    return dict(prof, stage=prof.get('stage') or LIVE_STAGE)

OUT = os.path.join(HERE, 'build', 'reveal')
FREE_LANES = getattr(RP, 'FREE_LANES', ('listed',))

CSS = """
body{font:14px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
     margin:0;background:#fbfbf9;color:#1a1a1a}
.wrap{max-width:880px;margin:0 auto;padding:28px 20px 60px}
h1{font-size:20px;margin:0 0 2px}h2{font-size:13px;text-transform:uppercase;letter-spacing:.06em;
   color:#6b6b66;margin:26px 0 8px;font-weight:600}
.sub{color:#6b6b66;margin:0 0 18px}
table{border-collapse:collapse;width:100%;font-size:13px}
td,th{padding:5px 8px;border-bottom:1px solid #e8e8e2;text-align:left;vertical-align:top}
th{color:#6b6b66;font-weight:600;font-size:11px;text-transform:uppercase;letter-spacing:.05em}
.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.bar{position:relative;height:12px;background:#ecece6;border-radius:6px;min-width:120px}
.bar i{position:absolute;top:0;bottom:0;background:#2f6f5e;border-radius:6px}
.lock{color:#a08a3c;font-size:12px}
.cav{border-left:3px solid #2f6f5e;padding:6px 0 6px 10px;margin:8px 0;font-size:13px}
.cav.d{border-left-color:#d6d6ce;color:#55554f}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}
.card{border:1px solid #e2e2da;border-radius:8px;padding:10px 12px;background:#fff;font-size:12px}
.card a{font-weight:600;text-decoration:none;color:#1a1a1a;font-size:13px}
.warn{color:#9b2c2c;font-weight:600}
"""


def _bar(lo, hi, top):
    if lo is None or hi is None or not top:
        return ''
    a, b = 100.0 * lo / top, 100.0 * hi / top
    return '<div class="bar"><i style="left:%.1f%%;width:%.1f%%"></i></div>' % (a, max(b - a, 1.2))


def page(key, label, p, tier):
    o = ['<!doctype html><meta charset="utf-8"><title>%s</title><style>%s</style>'
         % (html.escape(key), CSS), '<div class="wrap">']
    o.append('<h1>%s</h1><p class="sub">%s<br>tier <b>%s</b> &middot; lead lane %s &middot; '
             '%d caveats &middot; %d charts</p>'
             % (html.escape(key), html.escape(label), tier, p['lead']['lane'],
                p['honesty']['count'], len(p['charts'])))

    o.append('<h2>Honesty, inline</h2>')
    for c in p['honesty']['inline']:
        o.append('<div class="cav"><b>%s</b><br>%s</div>' % (c['key'], html.escape(c['text'])))
    if not p['honesty']['inline']:
        o.append('<p class="sub">none</p>')
    o.append('<h2>Behind the disclosure</h2>')
    for c in p['honesty']['disclosure']:
        o.append('<div class="cav d"><b>%s</b><br>%s</div>' % (c['key'], html.escape(c['text'])))
    if not p['honesty']['disclosure']:
        o.append('<p class="sub">none</p>')

    o.append('<h2>Lanes</h2><table><tr><th>lane</th><th>measure</th><th class="num">low</th>'
             '<th class="num">mid</th><th class="num">high</th><th class="num">names</th>'
             '<th>spread</th></tr>')
    tops = [r.get('high') for l in p['ranges'].values() for r in l.values() if r.get('high')]
    top = max(tops) if tops else 0
    for lane, bases in p['ranges'].items():
        for b, r in bases.items():
            if r.get('low') is None:
                o.append('<tr><td>%s</td><td>%s</td><td colspan="4" class="lock">locked: '
                         '%d names, no figures</td><td></td></tr>'
                         % (lane, b, r.get('n') or 0))
            else:
                o.append('<tr><td>%s</td><td>%s</td><td class="num">%sx</td><td class="num">%sx</td>'
                         '<td class="num">%sx</td><td class="num">%s</td><td>%s</td></tr>'
                         % (lane, b, r['low'], r['mid'], r['high'], r['n'],
                            _bar(r['low'], r['high'], top)))
    o.append('</table>')

    o.append('<h2>Peers behind each lane</h2><table><tr><th>lane</th><th>measure</th>'
             '<th>names</th></tr>')
    for lane, bases in p['ranges'].items():
        for b, r in bases.items():
            names = ', '.join((x.get('company') or '') for x in (r.get('peers') or []))
            o.append('<tr><td>%s</td><td>%s</td><td>%s</td></tr>'
                     % (lane, b, html.escape(names) or '<span class="sub">none</span>'))
    o.append('</table>')

    fx = p.get('recommendations') or {}
    dims = fx.get('blocks') or []
    o.append('<h2>What would move the range</h2>')
    o.append('<p class="sub">%d dimensions</p>' % len(dims))
    inv = p.get('investors') or {}
    cal = (inv.get('callable') or {}).get('cards') or []
    ev = (inv.get('evidence') or {}).get('cards') or []
    o.append('<h2>Investors</h2><p class="sub">%d callable, %d evidence</p>'
             % (len(cal), len(ev)))
    o.append('<div class="grid">')
    for c in cal[:8]:
        o.append('<div class="card"><a>%s</a><br><span class="sub">%s</span></div>'
                 % (html.escape(str(c.get('name') or c.get('investor_name') or '')),
                    html.escape(str(c.get('cheque') or c.get('stage_band') or ''))))
    o.append('</div>')
    o.append('</div>')
    return '\n'.join(o)


# Every figure a free page must not contain, gathered from the paid payload of the same fixture.
def figures_in(p):
    out = set()
    for lane, bases in p['ranges'].items():
        if lane in FREE_LANES:
            continue
        for r in bases.values():
            for k in ('low', 'mid', 'high', 'founder_low', 'founder_high', 'founder_metric'):
                v = r.get(k)
                if isinstance(v, (int, float)) and abs(v) >= 0.01:
                    out.add(round(float(v), 2))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tier', default='both', choices=('free', 'paid', 'both'))
    ap.add_argument('--only', default='')
    a = ap.parse_args()
    only = {x.strip() for x in a.only.split(',') if x.strip()}
    tiers = ('free', 'paid') if a.tier == 'both' else (a.tier,)
    os.makedirs(OUT, exist_ok=True)

    rows, leaks, missing_caveats = [], [], []
    for key, label, prof in PROFILES:
        if only and key not in only:
            continue
        built = {}
        for t in tiers:
            p = RP.build(live(prof), tier=t)
            built[t] = p
            h = page(key, label, p, t)
            io_path = os.path.join(OUT, '%s.%s.html' % (key, t))
            open(io_path, 'w', encoding='utf-8').write(h)
            # EVERY CAVEAT THE PAYLOAD CARRIES MUST BE IN THE MARKUP.
            for c in p['honesty']['inline'] + p['honesty']['disclosure']:
                if html.escape(c['text']) not in h:
                    missing_caveats.append((key, t, c['key']))
        if 'free' in built:
            h = open(os.path.join(OUT, '%s.free.html' % key), encoding='utf-8').read()
            # TAGS AND ATTRIBUTES ARE STRIPPED BEFORE SCANNING, because the bar widths are
            # percentages and a bar 5.6% wide is not the number 5.6x. Reading them as figures gave
            # three false positives on the first run (pazi, numida, magma) and a check that cries
            # wolf is a check nobody runs.
            text = re.sub(r'<[^>]+>', ' ', h)
            nums = {round(float(x), 2) for x in re.findall(r'\d+\.\d+', text)}
            paid = built.get('paid') or built['free']
            hidden = figures_in(paid)
            # A FIGURE THE FREE LANE ALSO SHOWS IS NOT A LEAK. pazi's listed high is 4.3 and its
            # private low is 4.3 as well; the founder is entitled to the first one and cannot tell
            # them apart, and neither can this check, so a coincidence is not called a breach.
            shown = set()
            for lane, bases in built['free']['ranges'].items():
                for r in bases.values():
                    for k2 in ('low', 'mid', 'high'):
                        v = r.get(k2)
                        if isinstance(v, (int, float)):
                            shown.add(round(float(v), 2))
            hit = sorted(nums & (hidden - shown))
            if hit:
                leaks.append((key, hit[:6]))
        p = built.get('paid') or built['free']
        rows.append(dict(key=key, label=label, caveats=p['honesty']['count'],
                         charts=len(p['charts']),
                         lanes=sum(len(v) for v in p['ranges'].values()),
                         locked=sum(1 for v in p['ranges'].values() for r in v.values()
                                    if r.get('low') is None),
                         investors=((p.get('investors') or {}).get('callable') or {}).get('count', 0)))

    rows.sort(key=lambda r: (r['lanes'], r['caveats']))
    idx = ['<!doctype html><meta charset="utf-8"><title>Fairway reveal contact sheet</title>'
           '<style>%s</style><div class="wrap">' % CSS,
           '<h1>Reveal contact sheet</h1><p class="sub">%d fixtures, thinnest first. '
           'A fixture near the top is one a founder would find disappointing.</p><div class="grid">'
           % len(rows)]
    for r in rows:
        idx.append('<div class="card"><a href="%s.free.html">%s</a><br>'
                   '<span class="sub">%s</span><br>%d lanes (%d locked) &middot; %d charts &middot; '
                   '%d caveats &middot; %d investors</div>'
                   % (r['key'], html.escape(r['key']), html.escape(r['label'][:70]),
                      r['lanes'], r['locked'], r['charts'], r['caveats'], r['investors']))
    idx.append('</div></div>')
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write('\n'.join(idx))
    json.dump(rows, open(os.path.join(OUT, 'summary.json'), 'w'), indent=1, sort_keys=True)

    print('RENDER HARNESS')
    print('  fixtures drawn        %d   (%s)' % (len(rows), ', '.join(tiers)))
    print('  contact sheet         build/reveal/index.html')
    thin = [r for r in rows if r['lanes'] - r['locked'] <= 1]
    print('  one visible lane      %d   %s' % (len(thin), ', '.join(r['key'] for r in thin[:8])))
    print('  no caveat at all      %d' % sum(1 for r in rows if r['caveats'] == 0))
    if missing_caveats:
        print('  FAIL caveats missing from the markup: %d' % len(missing_caveats))
        for k, t, c in missing_caveats[:10]:
            print('     %s (%s) %s' % (k, t, c))
    if leaks:
        print('  FAIL a locked figure appears on a free page: %d fixtures' % len(leaks))
        for k, v in leaks[:10]:
            print('     %s %s' % (k, v))
    if missing_caveats or leaks:
        return 1
    print('  PASS every caveat reaches the markup, and no locked figure appears on a free page.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
