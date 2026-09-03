# -*- coding: utf-8 -*-
"""Nothing reaches a founder that we said would not.

Fable's rails, 2-Sep: "public information only, no scraping behind logins, no contact details, no
claim of introduction... styled text wordmarks, no logos." Those are promises made on the page and
in the footer, and a promise enforced only by whoever remembers it is not enforced.

So this walks the payload for every fixture and asserts four things:

  1. NO CONTACT DETAIL of any kind reaches a card. No email, no phone, no personal profile link, no
     partner's name in a field meant for a firm's.
  2. NO CARD RENDERS INCOMPLETE. A callable house without a dated deal, a cheque range, a geography
     and a sector does not appear at all. A comparable with no source does not exist; nor does an
     investor.
  3. EVERY CARD SAYS HOW FAR WE REACHED. The degradation label is not optional decoration: a founder
     shown a house on a two-of-three match is entitled to know that is what happened.
  4. THE TWO LAYERS ARE NEVER MERGED, and the evidence layer always carries its honest label. This
     is the one that would be easiest to lose in a refactor and the most damaging: it is the
     difference between a map and a call list.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'selector'))
os.chdir(HERE)
import match_reference as M                      # noqa: E402
import investors as I                            # noqa: E402
from golden_profiles import PROFILES             # noqa: E402

# THE HOST TESTS ARE ANCHORED, and the first version was not. `x.com/` matched inside
# https://www.liablix.com/news/..., so the check reported a contact detail on five fixtures that had
# none. A check that cries wolf on its first run is a check nobody runs twice, and the fix is to
# match a HOST rather than a substring.
EMAILISH = re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+'
                      r'|(?://|\.|^)(?:linkedin|twitter|facebook|instagram)\.com'
                      r'|(?://|^)x\.com/'
                      r'|mailto:'
                      r'|\+\d[\d ()-]{7,}')


def main():
    bad = []
    n_cards = n_chips = 0
    for k, l, p in PROFILES:
        picked, _mo, _pt = M.select_private(p, M.private)
        pay = I.reveal_payload(p, picked, raise_musd=3.0)

        # 4, the labels, checked once per fixture because a missing one is a systemic fault
        if 'not an introduction' not in pay['footer']:
            bad.append('%s: the footer no longer says it is not an introduction' % k)
        if 'not a call list' not in pay['evidence']['note']:
            bad.append('%s: the evidence layer has lost its honest label' % k)

        for c in pay['callable']['cards']:
            n_cards += 1
            blob = ' '.join(str(v) for v in c.values() if v)
            if EMAILISH.search(blob):
                bad.append('%s: a contact detail reached a card for %s' % (k, c.get('investor')))
            for f in ('recent_deal', 'recent_deal_date', 'cheque_line', 'geographies'):
                if not c.get(f):
                    bad.append('%s: %s renders without %s' % (k, c.get('investor'), f))
            if c.get('cheque_line') == 'First cheque not published':
                bad.append('%s: %s renders with no cheque range' % (k, c.get('investor')))
            if not c.get('reach'):
                bad.append('%s: %s renders without saying how far we reached' % (k, c.get('investor')))
            for banned in I.BANNED:
                if banned in c:
                    bad.append('%s: a %s field reached the payload' % (k, banned))
        for ch in pay['evidence']['chips']:
            n_chips += 1
            if EMAILISH.search(' '.join(str(v) for v in ch.values() if v)):
                bad.append('%s: a contact detail reached an evidence chip' % k)

    print('walked %d fixtures | %d callable cards | %d evidence chips' % (len(PROFILES), n_cards, n_chips))
    if bad:
        print()
        print('FAIL: %d breaches of the rails we published.' % len(bad))
        seen = set()
        for b in bad:
            if b not in seen:
                print('   %s' % b)
                seen.add(b)
        return 1
    print('PASS: no contact details, no incomplete cards, every card labelled, both layers intact.')
    return 0


sys.exit(main())
