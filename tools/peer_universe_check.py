# -*- coding: utf-8 -*-
"""The march-to-100 scoreboard, scored on the PEER UNIVERSE and nothing else.

Daniil, 3-Sep-2026: "On march to 100 this needs to be done without revenue figures. We just need to
make sure that for 100 random names we are able to refine the peer universe. Applying revenue (or
ARR or GMV or book value) number to the respective multiples is more mechanical and hopefully can be
tested afterwards."

So the gate is not "does this company get a priced range". It is "does the engine narrow the world
down to a defensible set of comparables for this company". That is testable today, with no revenue
on any fixture, which is why the march no longer waits on the fixture schema.

THE BAR. Daniil ruled the top line on 4-Sep-2026, closing the empty-lane question:

  0. TWO KINDS OF EVIDENCE, OR IT IS NOT A PASS. "Fixture must be a pass when we have at least
     1 lane based on public peers and 1 lane based on private peers." A listed lane says what the
     market pays for this kind of business today; a private lane says what an investor actually
     paid for a company at this stage. Neither substitutes for the other, and a football field
     drawn from one of them is a single point of view wearing the clothes of a range.
     PUBLIC is core OR secondary: either listed lane satisfies it.
  1. NEVER PRICE OFF ONE COMPARABLE. A lane with one usable name does not count as a lane.
  2. THREE REAL NAMES BEAT FIVE PADDED ONES. At least three distinct named comparables in total.
  3. NEVER SHOW AN UNRELATED COMPARABLE. At least one lane must reach better than the weakest
     overlap tier, so the set rests on something more than a shared archetype word.
  4. A BLANK IS A TRIGGER, NEVER A CONCLUSION. A fixture with no peers at all is the loudest
     failure, not a quiet one.

WHAT THE 4-SEP RULING CHANGED, both ways. It LOOSENED the old bar, which demanded the CORE lane
specifically and failed a company whose core was empty however good its secondary was. It also
TIGHTENED it: an empty secondary is now explicitly fine and no longer reported as an unruled
warning, while a fixture with no private evidence fails outright rather than passing on the listed
side alone. One caveat is written into the output rather than hidden here: nothing in the product
reads a SECONDARY range today (see the note on PRICING_LANES below), so a fixture that satisfies
rule 0 only through its secondary lane is passing on a number no founder currently sees. Those are
counted and named on their own line.

Reported per fixture so two agents can double-check the same company and compare, which is the
double-verification the gate asks for.
"""
import json
import os
import sys

WEAK = 'THIN_OVERLAP'
LANES = ('core', 'secondary', 'private')
# WHICH LANES ACTUALLY PRICE A FOUNDER. Narrowed 3-Sep-2026 after this check failed goldfish and
# honen on their SECONDARY lane while both had a healthy core.
#
# I checked what reads a secondary range before changing this rather than after. Nothing does.
# `all_ranges` and `triage` both price off the listed CORE and the private lane; the only place a
# secondary range is computed at all is golden.py's snapshot loop, which records it and shows it to
# nobody. Secondary is the wider ring of context names, exactly as the code comments describe it.
#
# Failing a company because a number no founder sees rests on one name is not a strict check, it is
# a wrong one, and it buries the six real failures under two false ones. A thin secondary is still
# reported, as a note.
PRICING_LANES = ('core', 'private')

# DANIIL'S RULING OF 4-SEP-2026, in code: one public lane and one private lane.
PUBLIC_LANES = ('core', 'secondary')
PRIVATE_LANE = 'private'
MIN_PRICED = 2                      # one name is not a range (rule 1)


def read(path):
    return json.load(open(path))['expected']


def best_n(e, lane):
    """The widest range this founder can actually be priced on IN THIS LANE, across every basis.

    Added 3-Sep-2026, when the exchange fork landed. A lender is priced on book, ARR, earnings and
    originations; an exchange on throughput. Judging a fixture on the REVENUE range alone would
    fail a company that has a perfectly good book or throughput range and no revenue line, which is
    the normal condition for both of those archetypes rather than an edge case.
    """
    ns = []
    rng = e.get(lane + '_range') or {}
    if isinstance(rng.get('n'), int):
        ns.append(rng['n'])
    for _b, r in ((e.get('all_ranges') or {}).get(lane) or {}).items():
        if isinstance(r.get('n'), int):
            ns.append(r['n'])
    return max(ns) if ns else None


def score(e):
    """Returns (verdict, reasons, facts, warnings) for one fixture snapshot."""
    names, per_lane, closeness, priced, sole = set(), {}, [], {}, []
    for lane in LANES:
        rows = e.get(lane) or []
        got = [r.get('company') for r in rows if r.get('company')]
        per_lane[lane] = len(got)
        names.update(got)
        rng = e.get(lane + '_range') or {}
        n = best_n(e, lane)
        if rng.get('closeness'):
            closeness.append(rng['closeness'])
        # The widest priced set this lane can offer, across every basis the fork supports. A lender
        # priced on book and an exchange priced on throughput both count here; judging on the
        # revenue range alone would fail companies for not holding a line they never had.
        priced[lane] = n if isinstance(n, int) else 0
        if rng.get('sole') or priced[lane] == 1:
            sole.append(lane)

    public_lane = next((l for l in PUBLIC_LANES if priced[l] >= MIN_PRICED), None)
    private_ok = priced[PRIVATE_LANE] >= MIN_PRICED

    fails = []
    if not names:
        fails.append('no comparables at all')
    elif len(names) < 3:
        fails.append('only %d distinct comparable(s); three real names is the floor' % len(names))
    # RULE 0, AND IT IS THE ONE THAT DECIDES MOST VERDICTS.
    if public_lane is None:
        fails.append('no public lane with %d priced comparables (core %d, secondary %d)'
                     % (MIN_PRICED, priced['core'], priced['secondary']))
    if not private_ok:
        fails.append('no private lane: %d priced round(s), and a listed lane alone is one point '
                     'of view, not a range' % priced[PRIVATE_LANE])
    if closeness and all(c == WEAK for c in closeness):
        fails.append('every lane is %s; the set rests on nothing but a shared word' % WEAK)
    if not closeness:
        fails.append('no lane produced a range object to judge closeness on')

    # WARNINGS ARE FACTS THAT DO NOT DECIDE THE VERDICT, and after the 4-Sep ruling an empty
    # secondary is one of them: it is explicitly allowed, so it is reported and nothing more.
    warns = []
    if names and public_lane == 'secondary':
        warns.append('passes rule 0 on SECONDARY: no founder sees a secondary range today')
    if names and per_lane['secondary'] == 0:
        warns.append('secondary lane empty (allowed since 4-Sep)')
    warns += ['%s lane rests on one priced name' % l for l in sole if priced[l] == 1]
    facts = dict(names=len(names), core=per_lane['core'], secondary=per_lane['secondary'],
                 private=per_lane['private'], public_lane=public_lane or '-',
                 closeness=','.join(sorted(set(closeness))) or '-')
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
    print('%-18s %-5s %6s %5s %5s %5s %9s %8s  %s'
          % ('fixture', 'verd', 'names', 'core', 'sec', 'priv', 'rule0 via', 'closeness', 'why it fails'))
    for key, verdict, fails, fc, warns in rows:
        note = '; '.join(fails) or ('WARN ' + '; '.join(warns) if warns else '')
        print('%-18s %-5s %6d %5d %5d %5d %9s %8s  %s'
              % (key, verdict, fc['names'], fc['core'], fc['secondary'], fc['private'],
                 fc['public_lane'], fc['closeness'][:8], note))
    n = len(rows)
    print('\n%d fixtures | %d refine the peer universe | %d do not' % (n, n - failed, failed))
    print('GATE: 100 companies must reach PASS here, each checked by two independent agents.')
    print('Currently at %d of 100 companies, %d of them passing.' % (n, n - failed))
    on_secondary = sorted(k for k, v, f, fc, w in rows
                          if v == 'PASS' and fc['public_lane'] == 'secondary')
    if on_secondary:
        print('\nPASSING ON THE SECONDARY LANE (%d): %s' % (len(on_secondary), ', '.join(on_secondary)))
        print('Rule 0 is satisfied, and nothing in the product reads a secondary range today, so')
        print('these pass on a number no founder currently sees. Either the reveal starts reading')
        print('the secondary range or these are a false pass. Flagged, not decided.')
    empty_secondary = sorted(k for k, v, f, fc, w in rows if v == 'PASS' and fc['secondary'] == 0)
    if empty_secondary:
        print('\nPASSING WITH AN EMPTY SECONDARY LANE (%d): %s'
              % (len(empty_secondary), ', '.join(empty_secondary)))
        print("Allowed by Daniil's ruling of 4-Sep: a public lane and a private lane is the bar,")
        print('and these have both. Reported so the sourcing list stays visible.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
