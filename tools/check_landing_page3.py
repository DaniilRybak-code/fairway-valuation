# -*- coding: utf-8 -*-
"""Check 18: does every pool figure and every investor row on landing page 3 come from the data?

WHY THIS EXISTS. Page 3 of the landing ("Under the hood") shows four figures about the pool
(listed companies tracked, private rounds tracked, and how many of each share the example
company's business model) and nine investor rows (published first cheque, geography, most recent
deal). Daniil's rule: a statistic on the page is never typed by hand. So this tool WRITES the
four figures from the data files and CHECKS the nine rows against data/investors.csv, and the
suite fails when either drifts.

    python3 tools/check_landing_page3.py            # check (what check_all.sh runs)
    python3 tools/check_landing_page3.py --write    # rewrite landing-counts.js and the four
                                                    # figures in index.html from the data

What it writes (--write): landing-counts.js (read by landing-p3.js) and the text of the four
<b data-count="..."> elements in index.html, so the page is right with or without the script.
What it checks: those four figures against the engine's loader (selector/match_reference), and
each .p3-ivr row's cheque figures, currency conversion and deal against data/investors.csv.
Pound figures on the landing are shown at the rate on page 2 (1.35 $/£, 4 Sep 2026).
"""
import csv, io, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(HERE, 'index.html')
COUNTS_JS = os.path.join(HERE, 'landing-counts.js')
INVESTORS = os.path.join(HERE, 'data', 'investors.csv')
GBP_USD = 1.35   # the rate page 2 states, 4 Sep 2026
EXAMPLE_ARCHETYPE = 'Marketing & Customer Engagement'   # the example company is marketing software


def pool_counts():
    sys.path.insert(0, os.path.join(HERE, 'selector'))
    import match_reference as M
    def same(rows):
        return sum(1 for r in rows if EXAMPLE_ARCHETYPE in (r.get('archetype', ''), r.get('archetype_secondary', '')))
    return {
        'listed': len(M.listed),
        'private_rounds': len(M.private),
        'listed_same_model': same(M.listed),
        'private_same_model': same(M.private),
    }


def read_index():
    return open(INDEX, encoding='utf-8').read()


def html_counts(html):
    out = {}
    for m in re.finditer(r'<b data-count="([a-z_]+)">([^<]*)</b>', html):
        out[m.group(1)] = m.group(2).strip()
    return out


def write_counts(counts):
    from datetime import date
    body = ('/* Written by tools/check_landing_page3.py from the data files on %s. Never edit by hand:\n'
            '   run  python3 tools/check_landing_page3.py --write  after a data load instead. */\n'
            'window.FAIRWAY_COUNTS = {\n'
            '  listed: %d,              /* listed companies the engine loads */\n'
            '  private_rounds: %d,      /* private rounds the engine loads */\n'
            '  listed_same_model: %d,    /* listed rows carrying "%s" */\n'
            '  private_same_model: %d,   /* private rounds carrying the same label */\n'
            '  archetype: "%s",\n'
            '  written: "%s"\n'
            '};\n') % (date.today().isoformat(), counts['listed'], counts['private_rounds'],
                       counts['listed_same_model'], EXAMPLE_ARCHETYPE, counts['private_same_model'],
                       EXAMPLE_ARCHETYPE, date.today().isoformat())
    open(COUNTS_JS, 'w', encoding='utf-8').write(body)
    html = read_index()
    for k, v in counts.items():
        html, n = re.subn(r'(<b data-count="%s">)[^<]*(</b>)' % k, r'\g<1>%d\g<2>' % v, html)
        if n != 1:
            print('  data-count="%s" found %d times in index.html, expected 1' % (k, n))
            return False
    open(INDEX, 'w', encoding='utf-8').write(html)
    return True


def investors():
    body = ''.join(l for l in open(INVESTORS, encoding='utf-8') if not l.startswith('#'))
    rows = list(csv.DictReader(io.StringIO(body)))
    return {r['investor_name']: r for r in rows}


def money(s):
    """'$500k' -> 0.5, '$1.25m' -> 1.25, '$5m' -> 5.0 (all in $m)."""
    m = re.match(r'\$([\d.]+)(k|m)', s)
    if not m:
        return None
    v = float(m.group(1))
    return v / 1000.0 if m.group(2) == 'k' else v


def usd_m(value, ccy):
    v = float(value)
    return round(v * GBP_USD, 3) if ccy == 'GBP' else v


MONTHS = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
          'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}


def page_rows(html):
    sec = html[html.index('id="read"'):]
    out = []
    for m in re.finditer(r'<div class="p3-ivr">(.*?)</div>', sec, flags=re.S):
        block = m.group(1)
        name = re.search(r'<span class="nm">([^<]+)</span>', block).group(1)
        deal = re.search(r'<span class="deal">(Backed|Led) <b>([^<]+)</b> <em>([A-Z][a-z]{2})-(\d\d)</em></span>', block)
        ln = re.search(r'<span class="ln(?: none)?">([^<]+)</span>', block).group(1)
        out.append(dict(name=name, verb=deal.group(1), deal=deal.group(2),
                        deal_date='20%s-%s' % (deal.group(4), MONTHS[deal.group(3)]),
                        line=ln.replace('&middot;', '·').replace('&pound;', '£')))
    return out


def check_rows(html):
    table = investors()
    ok = True
    rows = page_rows(html)
    if not rows:
        print('  no investor rows found on page 3')
        return False
    for r in rows:
        t = table.get(r['name'])
        if not t:
            print('  %-22s NOT IN data/investors.csv' % r['name']); ok = False; continue
        # the deal: company and month must be one of the two recent deals the table holds
        deals = {(t.get('recent_deal_1_company', ''), t.get('recent_deal_1_date', '')),
                 (t.get('recent_deal_2_company', ''), t.get('recent_deal_2_date', ''))}
        if (r['deal'], r['deal_date']) not in deals:
            print('  %-22s deal on page %s %s, table holds %s' % (r['name'], r['deal'], r['deal_date'], sorted(deals))); ok = False
        # the cheque: figures on the page against the table, pounds converted at the stated rate
        lo, hi, ccy = t.get('first_cheque_low_m', ''), t.get('first_cheque_high_m', ''), t.get('cheque_currency', 'USD')
        figs = [money(x) for x in re.findall(r'\$[\d.]+(?:k|m)', r['line'])]
        if not lo and not hi:
            if figs:
                print('  %-22s page shows a cheque, table publishes none' % r['name']); ok = False
            continue
        want = []
        if lo: want.append(usd_m(lo, ccy))
        if hi and hi != lo: want.append(usd_m(hi, ccy))
        got = [round(f, 3) for f in figs]
        # the page rounds a converted figure the way page 2 does ($2.025m shows as $2.0m):
        # allow 1.5 per cent, never more, and never a different count of figures
        close = len(want) == len(got) and all(abs(w - g) <= max(0.005, 0.015 * w) for w, g in zip(want, got))
        if not close:
            print('  %-22s cheque on page %s, table gives %s %s (%s)' % (r['name'], got, lo, hi, ccy)); ok = False
        # geography: the page may shorten it, but it must not publish one the table lacks
        if not t.get('geographies') and '·' in r['line']:
            print('  %-22s page names a geography, table has none' % r['name']); ok = False
    print('  %d investor rows on page 3, each checked against the table' % len(rows))
    return ok


def main():
    write = '--write' in sys.argv
    counts = pool_counts()
    if write:
        if not write_counts(counts):
            return 1
        print('WROTE landing-counts.js and the four figures in index.html: %s' % counts)
    html = read_index()
    ok = True
    shown = html_counts(html)
    for k, v in counts.items():
        if shown.get(k) != str(v):
            print('  index.html shows %s = %s, data says %d  (run --write)' % (k, shown.get(k), v)); ok = False
    js = open(COUNTS_JS, encoding='utf-8').read() if os.path.exists(COUNTS_JS) else ''
    for k, v in counts.items():
        if not re.search(r'\b%s:\s*%d\b' % (k, v), js):
            print('  landing-counts.js does not carry %s = %d  (run --write)' % (k, v)); ok = False
    if ok:
        print('  pool figures on page 3 match the data: %s' % counts)
    ok = check_rows(html) and ok
    # the two world figures carry their source on the page; make sure the stamps are still there
    for stamp in ('World Bank, 2025', 'Crunchbase'):
        if stamp not in html[html.index('id="read"'):]:
            print('  the source stamp "%s" is missing from page 3' % stamp); ok = False
    print('OK: page 3 figures and investor rows come from the data' if ok else 'FAIL: page 3 has a figure the data does not back')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
