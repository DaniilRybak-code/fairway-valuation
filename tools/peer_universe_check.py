# -*- coding: utf-8 -*-
"""The march-to-100 scoreboard, scored on the PEER UNIVERSE and nothing else.

Daniil, 3-Sep-2026: "On march to 100 this needs to be done without revenue figures. We just need to
make sure that for 100 random names we are able to refine the peer universe. Applying revenue (or
ARR or GMV or book value) number to the respective multiples is more mechanical and hopefully can be
tested afterwards."

So the gate is not "does this company get a priced range". It is "does the engine narrow the world
down to a defensible set of comparables for this company". That is testable today, with no revenue
on any fixture, which is why the march no longer waits on the fixture schema.

THE BAR, taken from Daniil's own standing rules rather than invented here:
  1. NEVER PRICE OFF ONE COMPARABLE. A lane holding exactly one name fails.
  2. THREE REAL NAMES BEAT FIVE PADDED ONES. At least three distinct named comparables in total.
  3. NEVER SHOW AN UNRELATED COMPARABLE. At least one lane must reach better than the weakest
     overlap tier, so the set rests on something more than a shared archetype word.
  4. A BLANK IS A TRIGGER, NEVER A CONCLUSION. A fixture with no peers at all is the loudest
     failure, not a quiet one.

Reported per fixture so two agents can double-check the same company and compare, which is the
double-verification the gate asks for.
"""
import json
import os
import sys

WEAK = 'THIN_OVERLAP'
LANES = ('core', 'secondary', 'private')


def read(path):
    return json.load(open(path))['expected']


def score(e):
    """Returns (verdict, reasons, facts) for one fixture snapshot."""
    names, per_lane, closeness, sole_lanes = set(), {}, [], []
    for lane in LANES:
        rows = e.get(lane) or []
        got = [r.get('company') for r in rows if r.get('company')]
        per_lane[lane] = len(got)
        names.update(got)
        rng = e.get(lane + '_range') or {}
        n = rng.get('n')
        if rng.get('closeness'):
            closeness.append(rng['closeness'])
        if rng.get('sole') or (isinstance(n, int) and n == 1):
            sole_lanes.append(lane)
    fails = []
    if not names:
        fails.append('no comparables at all')
    elif len(names) < 3:
        fails.append('only %d distinct comparable(s); three real names is the floor' % len(names))
    if sole_lanes:
        fails.append('priced off ONE name in: %s' % ', '.join(sole_lanes))
    if closeness and all(c == WEAK for c in closeness):
        fails.append('every lane is %s; the set rests on nothing but a shared word' % WEAK)
    if not closeness:
        fails.append('no lane produced a range object to judge closeness on')
    # An EMPTY lane is not the same failure as a one-name lane, and it is not nothing either.
    # A fixture with zero core comparables is being priced entirely off the other lanes, which the
    # bar above does not forbid but Daniil has never ruled on. Report it as a warning, visible on
    # its own line in the summary, rather than folding it silently into a PASS or inventing a fail.
    warns = ['%s lane empty' % lane for lane in LANES if per_lane[lane] == 0] if names else []
    facts = dict(names=len(names), core=per_lane['core'], secondary=per_lane['secondary'],
                 private=per_lane['private'], closeness=','.join(sorted(set(closeness))) or '-')
    return ('PASS' if not fails else 'FAIL'), fails, facts, warns


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    fixdir = 'selector/golden'
    files = sorted(f for f in os.listdir(fixdir) if f.endswith('.json'))
    if not files:
        print('no fixtures found in %s' % fixdir)
        return 1
    rows, failed = [], 0
    for f in files:
        key = f[:-5]
        verdict, fails, facts, warns = score(read(os.path.join(fixdir, f)))
        rows.append((key, verdict, fails, facts, warns))
        if verdict == 'FAIL':
            failed += 1
    print('THE MARCH TO 100, SCORED ON PEER UNIVERSE ONLY. No revenue figure is used anywhere here.\n')
    print('%-18s %-5s %6s %5s %5s %8s  %s' % ('fixture', 'verd', 'names', 'core', 'priv', 'closeness', 'why it fails'))
    for key, verdict, fails, fc, warns in rows:
        note = '; '.join(fails) or ('WARN ' + '; '.join(warns) if warns else '')
        print('%-18s %-5s %6d %5d %5d %8s  %s'
              % (key, verdict, fc['names'], fc['core'], fc['private'],
                 fc['closeness'][:8], note))
    n = len(rows)
    print('\n%d fixtures | %d refine the peer universe | %d do not' % (n, n - failed, failed))
    print('GATE: 100 companies must reach PASS here, each checked by two independent agents.')
    print('Currently at %d of 100 companies, %d of them passing.' % (n, n - failed))
    warned = sorted(k for k, v, f, fc, w in rows if w and v == 'PASS')
    if warned:
        print('\nPASSING BUT WITH AN EMPTY LANE (%d): %s' % (len(warned), ', '.join(warned)))
        print('These price with no comparable at all in one lane. Not a fail under the bar above.')
        print('Daniil has not ruled on whether an empty lane should fail. Flagged, not decided.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
