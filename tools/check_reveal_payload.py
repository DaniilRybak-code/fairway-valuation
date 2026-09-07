# -*- coding: utf-8 -*-
"""Does the one reveal payload hold together for every fixture?

The reason this check exists on day one, rather than after the page reads the payload: the honesty
strings have been correct and unread since 26 August. `honesty.py` produced them, `honesty_check.py`
printed them, and no founder ever saw one, because nothing carried them from the engine to the page.
A payload with no check is the same shape of problem one layer up.

WHAT IT ASSERTS, and each line is a thing that would be wrong on the page rather than a thing that
would crash:

  1. IT BUILDS AT ALL, for all 102 fixtures, with no exception escaping.
  2. NOTHING LEAKS. Every range dict holds only whitelisted keys, so the engine's working (band
     internals, positioning tables, raw peer rows) cannot arrive on the page by accident. This is
     the same wall check 13 keeps around the fix list.
  3. NO NET AND GROSS IN ONE ROW (rule B3a). Where a lane offers both revenue readings they are two
     entries with two labels, and the same company never appears in both. A company counted twice
     would be one round voting twice, which is the cross-file rule D-something in miniature.
  4. EVERY NUMBER THE PAGE MULTIPLIES IS THE RIGHT ONE. founder_low and founder_high are the
     founder's own figure for THAT basis times that basis's own low and high, recomputed here from
     the parts rather than trusted.
  5. A LANE WITH NOTHING IN IT IS ABSENT, NOT EMPTY. Rule E8's shape: the page renders what is
     there and says nothing about what is not, so an empty dict must never be handed over.

It reports, it does not decide the gate. A fixture with no range is not a failure here; it is a
failure in check 8, which is where it belongs.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'selector'))
os.chdir(HERE)
import reveal_payload as RP                      # noqa: E402
from golden_profiles import PROFILES             # noqa: E402

ALLOWED = set(RP.RANGE_FIELDS) | {'peers'}


def close(a, b):
    if a is None or b is None:
        return a is None and b is None
    return abs(a - b) <= max(0.01, abs(b) * 0.005)


# THE RAISE IS GONE FROM THE LIVE PATH, SO THIS CHECK MUST NOT PASS ONE. Corrected 7-Sep-2026,
# when standing up /api/payload showed that RP.build(prof, raise_musd=None) returns ZERO callable
# investors for all 102 fixtures while this check, passing 3.0, reported all 102 carrying a house.
#
# Neither number was wrong; the check was answering a question the product had stopped asking. Rule
# E9 took the raise out of the request on 6 September, and _stage_for was changed the same day to
# read the founder's STATED stage instead, which is the answer to step 1 of the quiz. That fix
# works and the live endpoint gets its 8 cards a founder from it.
#
# What nothing noticed is that THE FIXTURES CARRY NO STAGE. They are peer-universe fixtures: they
# were written to test which comparables a business nature finds, and a stage was never part of
# that. So with the raise removed and no stage on the profile there is nothing for the stage gate
# to match, and the check went on passing because it was still handing over a raise the live path
# cannot have.
#
# So the profile is given a stage HERE, as a stated test condition, and the raise is not passed.
# 'Seed' is not a claim about any of the 102 companies; it is the middle of the three buttons the
# quiz offers, and the 6-September measurement covered all three (813 cards at Seed, 724 at
# Pre-seed, 797 at Series A). Putting a real stage on each fixture is a better answer and it is
# data somebody has to decide rather than a line of code, so it is written up instead of invented.
LIVE_STAGE = 'Seed'


def live(prof):
    """The profile as the live path presents it: a stated stage and no raise.

    SINCE 7-SEP-2026 THE FIXTURES CARRY THEIR OWN STAGE (Daniil's ruling; see the note in
    selector/golden_profiles.py), so this no longer supplies one and is kept only as the single
    place that says what shape the live path has. If a fixture ever loses its stage, this keeps the
    check honest instead of letting it report an empty investor list as a pass."""
    return dict(prof, stage=prof.get('stage') or LIVE_STAGE)


def main():
    bad, built = [], 0
    lanes_with_both = 0
    dual_fixtures = []
    honesty_reached = 0
    multi_chart = 0
    fix_reached = 0
    inv_reached = 0
    for key, _label, prof in PROFILES:
        try:
            p = RP.build(live(prof))
        except Exception as exc:                                   # noqa: BLE001
            bad.append('%s: build raised %s: %s' % (key, type(exc).__name__, exc))
            continue
        built += 1

        if p['honesty']['count']:
            honesty_reached += 1
        if p['recommendations']['count']:
            fix_reached += 1
        if p['investors']['callable']['count']:
            inv_reached += 1
        # A FOUNDER WHO TYPES NOTHING IS THE NORMAL CASE FOR A FIXTURE, and Daniil's instruction of
        # 6-Sep is that such a founder still sees how their peers trade. Every fixture carries no
        # revenue, so this counts exactly that founder's reveal.
        if len([c for c in p.get('charts') or [] if not c.get('priced')]) >= 2:
            multi_chart += 1

        for lane, bases in p['ranges'].items():
            if not bases:
                bad.append('%s / %s: empty lane handed over; it should be absent' % (key, lane))
            for basis, rng in bases.items():
                leaked = set(rng) - ALLOWED
                if leaked:
                    bad.append('%s / %s / %s: fields outside the whitelist reached the payload: %s'
                               % (key, lane, basis, ', '.join(sorted(leaked))))
                # 4. THE ARITHMETIC THE PAGE WILL SHOW.
                v = rng.get('founder_metric')
                if v is not None:
                    for end in ('low', 'high'):
                        want = round(v * rng[end], 2)
                        if not close(rng.get('founder_' + end), want):
                            bad.append('%s / %s / %s: founder_%s is %s, and %s times %s is %s'
                                       % (key, lane, basis, end, rng.get('founder_' + end),
                                          v, rng[end], want))
                if not rng.get('basis_label'):
                    bad.append('%s / %s / %s: a range with no label on the measure it is built on'
                               % (key, lane, basis))
            # 3. NET AND GROSS ARE TWO ROWS AND NEVER SHARE A COMPANY.
            if 'REVENUE' in bases and 'REVENUE_GROSS' in bases:
                lanes_with_both += 1
                dual_fixtures.append('%s/%s' % (key, lane))
                net = {c.get('company') for c in bases['REVENUE'].get('peers', [])}
                gross = {c.get('company') for c in bases['REVENUE_GROSS'].get('peers', [])}
                both = net & gross
                if both:
                    bad.append('%s / %s: %s price the net AND the gross range, so one round votes '
                               'twice (rule B3a)' % (key, lane, ', '.join(sorted(both))))
                if bases['REVENUE']['basis_label'] == bases['REVENUE_GROSS']['basis_label']:
                    bad.append('%s / %s: the two revenue rows carry the same label, so a founder '
                               'cannot tell which is which' % (key, lane))

    # THE PAYWALL IS A BOUNDARY IN THE DATA, AND THIS IS WHAT KEEPS IT ONE.
    #
    # Rule E8 as amended by Daniil on 6-Sep-2026: the public lane is free and complete, everything
    # non-public is blurred, and hovering a blurred range shows the comparable NAMES without their
    # multiples. The names are new; the numbers are not. A blur over a figure sitting in the DOM is
    # not a paywall, it is a dare, so this walks every free payload and asserts that no figure
    # behind the lock is in it at all.
    #
    # It checks the WHOLE object, not just the lanes, because the same numbers reach the page by
    # more than one door: `lead` carries the private range, and `charts` carries low, mid and high
    # for every bar. Missing either would hand over exactly what the lock is over.
    FORBIDDEN = ('low', 'mid', 'high', 'multiple', 'founder_low', 'founder_high', 'founder_metric',
                 'spread', 'mult')
    free_ok = 0
    for key, _label, prof in PROFILES:
        try:
            fp = RP.build(live(prof), tier='free')
        except Exception as exc:                                   # noqa: BLE001
            bad.append('%s: free payload raised %s: %s' % (key, type(exc).__name__, exc))
            continue
        free_ok += 1
        for lane, bases in (fp.get('ranges') or {}).items():
            if lane in RP.FREE_LANES:
                continue
            for basis, rng in bases.items():
                if not rng.get('locked'):
                    bad.append('%s / %s / %s: a non-public lane is not marked locked on the free '
                               'tier' % (key, lane, basis))
                leaked = [f for f in FORBIDDEN if rng.get(f) is not None]
                if leaked:
                    bad.append('%s / %s / %s: the free payload carries %s behind the lock'
                               % (key, lane, basis, ', '.join(leaked)))
                for c in rng.get('peers') or []:
                    leaked = [f for f in FORBIDDEN if c.get(f) is not None]
                    if leaked:
                        bad.append('%s / %s / %s: a locked comparable carries %s'
                                   % (key, lane, basis, ', '.join(leaked)))
                    if not c.get('company'):
                        bad.append('%s / %s / %s: a locked comparable has no name, so the hover '
                                   'shows nothing' % (key, lane, basis))
        for c in fp.get('charts') or []:
            if c.get('lane') in RP.FREE_LANES or not c.get('locked'):
                continue
            leaked = [f for f in FORBIDDEN if c.get(f) is not None]
            if leaked:
                bad.append('%s: a locked CHART carries %s' % (key, ', '.join(leaked)))
        lead = (fp.get('lead') or {}).get('range')
        if lead and (fp.get('lead') or {}).get('lane') not in RP.FREE_LANES:
            bad.append('%s: the free payload carries the private lead range, which is the exact '
                       'set of numbers the lock is over' % key)

        # AND THE SAME NUMBERS CAN LEAVE IN PROSE. Added 7-Sep-2026, after the render harness drew
        # fundraisly's free page and it said "At most 12.2x", 12.2 being the high of the private
        # lane the founder had not paid for. The loop above reads FIELDS and a caveat is a STRING,
        # so eleven fields could be clean while the sentence under them gave the number away.
        #
        # Every figure the paid payload holds behind the lock is looked for in every free caveat.
        # A figure the FREE lanes also show is not a leak: pazi's listed high and private low are
        # both 4.3, the founder is entitled to the first, and nothing can tell them apart.
        try:
            pp = RP.build(live(prof), tier='paid')
        except Exception:                                          # noqa: BLE001
            pp = None
        if pp:
            hidden, shown = set(), set()
            for lane, bases in (pp.get('ranges') or {}).items():
                for rng in bases.values():
                    for f in ('low', 'mid', 'high', 'founder_low', 'founder_high'):
                        v = rng.get(f)
                        if isinstance(v, (int, float)) and abs(v) >= 0.01:
                            (shown if lane in RP.FREE_LANES else hidden).add(round(float(v), 2))
            for c in fp['honesty']['inline'] + fp['honesty']['disclosure']:
                nums = {round(float(x), 2) for x in re.findall(r'\d+\.\d+', c['text'])}
                hit = sorted(nums & (hidden - shown))
                if hit:
                    bad.append('%s: the free caveat "%s" prints %s, which is a figure from a '
                               'locked lane. Rule E8 is over the numbers wherever they are written.'
                               % (key, c['key'], ', '.join(str(x) for x in hit)))

    n = len(PROFILES)
    print('ONE PAYLOAD, BUILT FOR EVERY FIXTURE\n')
    print('BUILT     %d of %d profiles assembled without an exception' % (built, n))
    print('HONESTY   %d carry at least one caveat  (these reach a founder for the first time)'
          % honesty_reached)
    print('FIX LIST  %d carry at least one dimension' % fix_reached)
    print('INVESTORS %d carry at least one callable house' % inv_reached)
    print('NET+GROSS %d lanes offer both revenue readings side by side, never merged' % lanes_with_both)
    print('FREE TIER %d free payloads built; public lane complete, every other lane locked to names'
          % free_ok)
    print('CHARTS    %d of %d fixtures can show two or more peer bar charts with NO founder figure'
          % (multi_chart, n))
    if dual_fixtures:
        print('          %s%s' % (', '.join(dual_fixtures[:10]),
                                  ' ...' if len(dual_fixtures) > 10 else ''))
    print()
    if bad:
        print('FAIL: %d problems.' % len(bad))
        for b in bad[:40]:
            print('   %s' % b)
        if len(bad) > 40:
            print('   ... and %d more' % (len(bad) - 40))
        return 1
    print('PASS: every payload builds, nothing leaks past the whitelist, every founder figure')
    print('multiplies out to the range beside it, and no round is counted on both bases.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
