# -*- coding: utf-8 -*-
"""Does the engine convert a founder's revenue onto the basis each comparable was built on?

FABLE'S ITEM 1, and it had been the top item for three days. The concern is exact and correct: all
43 golden fixtures return NO_REVENUE_GIVEN on all 152 period spans, so `founder_revenue_for` has
never converted anything in any test we run. The path that decides whether a founder is priced
correctly against a forward multiple has been untested since it was written.

The fixtures cannot fix that. None of the 43 has a revenue we know, and injecting a synthetic one
was tried on 3-Sep and reverted the same hour because it moved the peer selection of 42 of them:
growth is not just a display field, `band_compatible` gates the private lane on it, so a made-up
60 per cent excluded every mature round. Nothing invented may decide which real companies a founder
is compared against.

So the conversion is tested here instead, directly, with known inputs and known answers. It is
arithmetic on the founder's own number and not a property of the comparable set, so this is where
it belongs.

Daniil, 31-Aug-2026: "Public comps are priced on NTM basis, hence we need to ask / derive client's
NTM revenue." Every listed multiple we hold is enterprise value over NEXT twelve months revenue and
every quiz fork asks for the LAST twelve months. On a founder growing 80 per cent that gap is 80
per cent of the answer.
"""
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'selector'))
os.chdir(HERE)
import match_reference as M                      # noqa: E402

# profile, period asked for, expected value, expected basis label
CASES = [
    ('trailing asked for, trailing given, nothing to do',
     dict(revenue=10.0, growth=60.0), 'LTM', 10.0, 'AS_GIVEN_TRAILING'),
    ('an empty period means trailing',
     dict(revenue=10.0, growth=60.0), '', 10.0, 'AS_GIVEN_TRAILING'),
    ('FORWARD asked for: the whole point. 10 growing 60 per cent is 16',
     dict(revenue=10.0, growth=60.0), 'NTM', 16.0, 'DERIVED_FROM_TRAILING_AND_GROWTH'),
    ('a run rate is forward too, and Daniil ruled it takes the forward treatment',
     dict(revenue=10.0, growth=60.0), 'RUN_RATE', 16.0, 'DERIVED_FROM_TRAILING_AND_GROWTH'),
    ('an ARR comparable is a forward basis',
     dict(revenue=10.0, growth=60.0), 'ARR', 16.0, 'DERIVED_FROM_TRAILING_AND_GROWTH'),
    ('NO GROWTH GIVEN: the trailing figure is used and the label SAYS SO. It must never '
     'silently pretend to be forward',
     dict(revenue=10.0), 'NTM', 10.0, 'TRAILING_USED_UNCHANGED_NO_GROWTH_GIVEN'),
    ('zero growth is a real answer and is not the same as no answer',
     dict(revenue=10.0, growth=0.0), 'NTM', 10.0, 'DERIVED_FROM_TRAILING_AND_GROWTH'),
    ('SHRINKING. A negative rate must reduce the forward figure, not be ignored',
     dict(revenue=10.0, growth=-25.0), 'NTM', 7.5, 'DERIVED_FROM_TRAILING_AND_GROWTH'),
    ('no revenue at all is the honest empty answer, which is what all 43 fixtures return',
     dict(growth=60.0), 'NTM', None, 'NO_REVENUE_GIVEN'),
    ('a period we do not recognise falls back to trailing AND SAYS SO',
     dict(revenue=10.0, growth=60.0), 'FY2027', 10.0, 'UNRECOGNISED_PERIOD_TRAILING_USED'),
]


def main():
    bad = 0
    print('CONVERTING A FOUNDER\'S OWN REVENUE ONTO EACH COMPARABLE\'S BASIS\n')
    for why, prof, period, want_v, want_b in CASES:
        v, b = M.founder_revenue_for(prof, period)
        ok = (v == want_v) and (b == want_b)
        if not ok:
            bad += 1
        print('%-4s %-9s -> %-8s %-38s %s'
              % ('ok' if ok else 'FAIL', period or "''", v, b, why))
        if not ok:
            print('     expected %s / %s' % (want_v, want_b))

    # AND THE SPAN, which is what a range actually carries: one founder figure per basis present in
    # the comparable set, so the reveal multiplies row by row instead of applying one median to one
    # number.
    print()
    prof = dict(revenue=10.0, growth=60.0)
    rows = [((0.0, []), {'revenue_period': p}) for p in ('LTM', 'NTM', 'RUN_RATE', '')]
    span = M._period_span(prof, rows)
    want = {'LTM': 10.0, 'NTM': 16.0, 'RUN_RATE': 16.0}
    for k, v in sorted(span.items()):
        exp = want.get(k)
        ok = v['founder_revenue'] == exp
        if not ok:
            bad += 1
        print('%-4s span %-9s founder_revenue=%-8s %s' % ('ok' if ok else 'FAIL', k,
                                                          v['founder_revenue'], v['basis']))
    print()
    if bad:
        print('FAIL: %d period conversions are wrong.' % bad)
        return 1
    print('PASS: %d conversions and the span all behave as specified.' % len(CASES))
    print('The 43 golden fixtures still read NO_REVENUE_GIVEN and that is CORRECT: we do not know')
    print('their revenue, and inventing one would decide which real companies they are shown.')
    return 0


sys.exit(main())
