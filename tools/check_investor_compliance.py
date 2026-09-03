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
import io
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


# WHAT THE RENDERER READS MUST BE WHAT THE ENGINE EMITS.
#
# investors.js draws the cards from reveal_payload(), and the two are in different languages in
# different directories with nothing joining them. A field renamed on the Python side leaves a
# blank on the page and no test anywhere goes red: that is the same seam that let a whole 509-row
# refresh sit unused for two days. So the JS is parsed for every `c.<field>` it reads off a card
# and every `e.<field>` off an evidence chip, and each one has to exist in the payload.
DERIVED = {'cheque_line', 'geography_line', 'reach', 'backed', 'n', 'investor',
           'not_published', 'recent_deal', 'recent_deal_date', 'recent_deal_url'}


def contract_breaches(pay):
    js = io.open(os.path.join(HERE, 'investors.js'), encoding='utf-8').read()
    card_keys = set(pay['callable']['cards'][0]) if pay['callable']['cards'] else set()
    chip_keys = set(pay['evidence']['chips'][0]) if pay['evidence']['chips'] else set()
    out = []
    for var, keys, what in (('c', card_keys | DERIVED, 'a callable card'),
                            ('e', chip_keys | DERIVED, 'an evidence chip')):
        for f in set(re.findall(r'\b%s\.([a-z_]+)\b' % var, js)):
            if f not in keys and f not in ('map', 'slice', 'join', 'length', 'indexOf'):
                out.append('investors.js reads %s off %s and the payload has no such field'
                           % (f, what))
    for f in ('heading', 'note', 'cards', 'chips', 'count'):
        if ('.' + f) not in js and f in ('heading', 'note', 'cards', 'chips'):
            out.append('investors.js never reads payload.%s, so that part of the block is dead' % f)
    if 'payload.footer' not in js:
        out.append('investors.js does not render the footer, which is binding on every rendering')
    return out


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
            # THE BAR MOVED ON 3-Sep AND THIS CHECK MOVED WITH IT, in the stricter direction.
            #
            # It used to fail a card whose cheque line read "First cheque not published", which
            # meant Benchmark, Thrive, Founders Fund and thirteen other active early-stage houses
            # could never reach a founder because their websites are thin. Daniil's ruling: "we
            # should definitely include Benchmark and Thrive, reality is they can do pretty much
            # anything." So an unpublished figure is no longer a breach.
            #
            # WHAT IS A BREACH is a card that stays silent about it. A blank where the cheque
            # should be reads as our omission; "First cheque not published" reads as a fact about
            # the fund. Every card must carry a dated sourced deal, a cheque line and a geography
            # line, and where the fund publishes nothing those lines must SAY nothing is published
            # rather than be empty.
            for f in ('recent_deal', 'recent_deal_date', 'recent_deal_url',
                      'cheque_line', 'geography_line', 'reach'):
                if not c.get(f):
                    bad.append('%s: %s renders without %s' % (k, c.get('investor'), f))
            if not (c.get('geographies') or '').strip() \
                    and c.get('geography_line') != 'No stated investing geography':
                bad.append('%s: %s has no geography and the card does not say so'
                           % (k, c.get('investor')))
            if not c.get('cheque_low_m') and not c.get('cheque_high_m') \
                    and 'not published' not in (c.get('cheque_line') or ''):
                bad.append('%s: %s has no cheque figure and the card does not say so'
                           % (k, c.get('investor')))
            if not c.get('reach'):
                bad.append('%s: %s renders without saying how far we reached' % (k, c.get('investor')))
            for banned in I.BANNED:
                if banned in c:
                    bad.append('%s: a %s field reached the payload' % (k, banned))
        for ch in pay['evidence']['chips']:
            n_chips += 1
            if EMAILISH.search(' '.join(str(v) for v in ch.values() if v)):
                bad.append('%s: a contact detail reached an evidence chip' % k)

    bad.extend(contract_breaches(pay))
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


# GUARDED, because it was not. `sys.exit(main())` sat at module level, so importing this file to
# reuse its fixture list ran the whole check and then killed the caller with SystemExit. Anything
# that wanted to walk the same 43 profiles had to copy them instead.
if __name__ == '__main__':
    sys.exit(main())
