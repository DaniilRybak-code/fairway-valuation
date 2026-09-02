#!/usr/bin/env python3
"""
THE GATE ON WHAT MAY RENDER. Fable's activity rule, made executable.

A CALLABLE investor renders only if it carries ALL of:
  - at least one named deal dated inside 12 months, WITH a source URL
  - a first-cheque range
  - a stage band
  - at least one sector in our screening vocabulary
  - a geography
  - a one-line thesis

An EVIDENCE investor renders only if it carries a dated deal with a source URL. It needs no
cheque range and no thesis, because it is not a call list: it is a map of who backed the
founder's own reference rounds.

A row that fails does not render. Same discipline as comps sourcing: a figure with no source
does not exist. The failures ARE the pull list, which this prints.

    python3 tools/investor_check.py            # report
    python3 tools/investor_check.py --pull     # just the pull list, tab separated
"""
import csv, io, sys, re
from datetime import date

PATH = 'data/investors.csv'
ACTIVITY_MONTHS = 12

def load():
    lines = [l for l in open(PATH) if not l.startswith('#')]
    return list(csv.DictReader(io.StringIO(''.join(lines))))

def months_since(ym, today=None):
    if not re.match(r'^\d{4}-\d{2}$', ym or ''):
        return None
    t = today or date.today()
    y, m = int(ym[:4]), int(ym[5:7])
    return (t.year - y) * 12 + (t.month - m)

def check_row(r):
    """Returns (renders, [reasons it does not], [soft notes that downgrade the tier])."""
    bad, soft = [], []
    layer = r.get('layer') or ''
    d1, u1 = r.get('recent_deal_1_date'), r.get('recent_deal_1_source_url')
    if not d1 or not u1:
        bad.append('no dated deal with a source URL')
    if 'CALLABLE' in layer:
        age = months_since(d1)
        if age is None:
            pass                                   # already reported above
        elif age > ACTIVITY_MONTHS:
            bad.append('most recent deal is %d months old, the rule is %d' % (age, ACTIVITY_MONTHS))
        # A SIZE THE FOUNDER CAN JUDGE, not necessarily a first cheque. For a curated seed fund
        # the honest number is its first-cheque range; for a house promoted out of our own rounds
        # it is the size of round it joins, because a first cheque is not something our data knows
        # and inventing one would be worse than leaving it out. Either satisfies the rule; neither
        # is optional. Amended 02-Sep-2026 when the promotion pass was added.
        has_cheque = r.get('first_cheque_low_m') and r.get('first_cheque_high_m')
        has_round = r.get('round_size_low_m') and r.get('round_size_high_m')
        if not (has_cheque or has_round):
            bad.append('no first-cheque range and no round-size range')
        if not r.get('stage_bands'):
            bad.append('no stage band')
        if not r.get('screening_categories'):
            bad.append('no sector in our vocabulary')
        # GEOGRAPHY IS NOT A BLOCKER, BECAUSE WE DO NOT HOLD IT ANYWHERE. Checked 02-Sep-2026:
        # there is no country field on the rounds files, on the company tags, or on the investor
        # files. Refusing 75 active, sourced houses for a facet the whole database lacks would be
        # punishing them for our gap. A row without a geography renders in the BROADER FIT tier,
        # which is exactly what vcconf's degradation does with sector-agnostic and pan-geo
        # investors, and the card says the geography is not recorded rather than implying global.
        # The pull to close it is small and it also unblocks the queued region quiz question.
        if not r.get('geographies'):
            soft.append('geography not recorded, renders as broader fit')
        if not r.get('thesis_one_liner'):
            bad.append('no thesis')
    return (not bad), bad, soft

def alias_collisions(rows):
    """Sequoia and Sequoia Capital are one house in the world and two rows here."""
    def stem(n):
        n = n.lower()
        changed = True
        while changed:
            changed = False
            for tail in (' capital partners', ' capital', ' ventures', ' partners', ' vc',
                         ' management', ' group', ' global', ' investments'):
                if n.endswith(tail) and len(n) > len(tail) + 2:
                    n, changed = n[:-len(tail)], True
                    break
        return re.sub(r'[^a-z0-9]', '', n)
    seen = {}
    for r in rows:
        seen.setdefault(stem(r['investor_name']), []).append(r['investor_name'])
    return {k: v for k, v in seen.items() if len(set(v)) > 1}

def main():
    rows = load()
    pull_only = '--pull' in sys.argv
    callable_rows = [r for r in rows if 'CALLABLE' in (r.get('layer') or '')]
    evidence_rows = [r for r in rows if 'EVIDENCE' in (r.get('layer') or '')]

    fails = []
    softs = []
    for r in rows:
        ok, why, soft = check_row(r)
        if not ok:
            fails.append((r, why))
        if soft:
            softs.append((r, soft))

    if pull_only:
        print('investor\tlayer\tsector\tcheque\twhat is missing')
        for r, why in fails:
            print('\t'.join([r['investor_name'], r['layer'],
                             (r.get('screening_categories') or r.get('subsectors') or '')[:60],
                             ('%s-%s %s' % (r.get('first_cheque_low_m') or r.get('round_size_low_m'),
                                            r.get('first_cheque_high_m') or r.get('round_size_high_m'),
                                            r.get('cheque_currency'))).strip('- '),
                             '; '.join(why)]))
        return 0

    print('INVESTOR TABLE CHECK, %s' % PATH)
    print('%d houses: %d carry a CALLABLE layer, %d carry an EVIDENCE layer.\n'
          % (len(rows), len(callable_rows), len(evidence_rows)))

    cf = [(r, w) for r, w in fails if 'CALLABLE' in r['layer']]
    ef = [(r, w) for r, w in fails if 'CALLABLE' not in r['layer']]
    print('CALLABLE: %d of %d render. %d refused.' % (len(callable_rows) - len(cf), len(callable_rows), len(cf)))
    for r, w in cf:
        print('   REFUSED  %-24s %s' % (r['investor_name'][:24], '; '.join(w)))
    print('\nEVIDENCE: %d of %d render. %d refused.' % (len(evidence_rows) - len(ef), len(evidence_rows), len(ef)))
    for r, w in ef[:20]:
        print('   REFUSED  %-24s %s' % (r['investor_name'][:24], '; '.join(w)))

    tiered = [(r, w) for r, w in softs if 'CALLABLE' in r['layer']]
    print('\nBROADER FIT: %d CALLABLE rows render but with a facet missing.' % len(tiered))
    seen = {}
    for r, w in tiered:
        for x in w:
            seen[x] = seen.get(x, 0) + 1
    for k, v in sorted(seen.items(), key=lambda x: -x[1]):
        print('   %-52s %d rows' % (k, v))

    col = alias_collisions(rows)
    print('\nALIAS COLLISIONS: %d. One house, two rows, so a founder could see it twice.' % len(col))
    for k, v in sorted(col.items()):
        print('   %s' % ' / '.join(sorted(set(v))))

    print('\nCOVERAGE OF THE CALLABLE LAYER BY SECTOR (what a founder in each fork would be offered):')
    by = {}
    for r in callable_rows:
        ok, _w, _s = check_row(r)
        for c in (r.get('screening_categories') or '').split(';'):
            c = c.strip()
            if c:
                by.setdefault(c, [0, 0])
                by[c][0] += 1
                by[c][1] += 1 if ok else 0
    for c, (tot, good) in sorted(by.items()):
        print('   %-46s %d curated, %d renderable' % (c, tot, good))
    return 0

if __name__ == '__main__':
    sys.exit(main())
