#!/usr/bin/env python3
"""Does every number in Fairway's read trace back to something real.

Fable's Day 3 acceptance test, written down as a check rather than left as a reading: "renders for
all fixtures with zero invented figures (every number in a recommendation traces to a profile field
or a range object)".

A reading by a person cannot hold that line. A recommendation is prose, the numbers are inside the
prose, and a sentence that says "the top quartile prices at 5.8x" looks exactly as trustworthy
whether 5.8 was computed from the peers in front of the founder or typed into a format string. So
each dimension declares its figures and this check does three things:

  1  EVERY NUMBER PRINTED TO A FOUNDER IS DECLARED. Company names are removed first, then every
     numeral in every sentence must match a declared figure. A number that appears in a sentence
     and not in the figures list fails the check, which is what stops a future edit adding a
     plausible constant to a string.

  2  EVERY DECLARED FIGURE IS RECOMPUTED. A median is re-taken from the values it claims to be the
     median of, a percentile is recounted, a count is re-counted, a spread and a gap are
     re-subtracted, a profile figure is read off the profile, and a peer figure has to be a member
     of the set it claims to come from. Declaring provenance is not the same as having it.

  3  THE PAGE PAYLOAD CARRIES ONLY THE WHITELIST. reveal_payload may hand the reveal the sentences
     and the ordering, never the read objects, the peer values or the figures.

Run:  python3 tools/recommendations_check.py
"""
import os
import re
import statistics as st
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'selector'))
os.chdir(HERE)
import match_reference as M                      # noqa: E402
import recommendations as R                      # noqa: E402
from golden_profiles import PROFILES             # noqa: E402

NUM = re.compile(r'-?\d+(?:\.\d+)?')
DIMENSIONS = ('quality of revenue', 'growth story', 'unit economics',
              'market position', 'evidence gaps')


def renders(v):
    """Every way a figure could honestly be printed."""
    out = set()
    try:
        f = float(v)
    except (TypeError, ValueError):
        return out
    for fmt in ('%g', '%.0f', '%.1f', '%.2f'):
        out.add(fmt % f)
        out.add(fmt % abs(f))          # the sign may be dropped by the sentence around it
    out.add(str(v))
    if f.is_integer():
        out.add(str(int(f)))
        out.add(str(abs(int(f))))
    return out


def close(a, b, dp=1):
    try:
        return round(float(a), dp) == round(float(b), dp)
    except (TypeError, ValueError):
        return False


def check_figure(fig, prof, ranges):
    """Recompute one declared figure from what it says it came from. Returns a reason or None."""
    src, v, ins = fig.get('source', ''), fig.get('value'), fig.get('inputs')
    if src.startswith('profile.'):
        got = prof.get(src.split('.', 1)[1])
        return None if close(got, v, 2) else 'profile field %r is %r, sentence says %r' % (src, got, v)
    if src == 'peer.observed':
        if not ins:
            return 'peer figure declares no set to be a member of'
        return None if any(close(x, v, 1) for x in ins) else \
            'peer figure %r is not one of the %d values it claims to come from' % (v, len(ins))
    if src.startswith('range.'):
        r = ((ranges.get(fig.get('lane')) or {}).get(fig.get('basis')) or {})
        got = r.get(src.split('.', 1)[1])
        return None if close(got, v, 2) else 'range %s %s is %r, sentence says %r' % (
            fig.get('lane'), fig.get('basis'), got, v)
    if src == 'derived.median':
        return None if ins and close(st.median([float(x) for x in ins]), v, 1) else \
            'median of the declared inputs is not %r' % (v,)
    if src == 'derived.count':
        return None if ins is not None and len(ins) == v else 'count of the declared inputs is not %r' % (v,)
    if src == 'derived.percentile':
        if not ins:
            return 'percentile declares no distribution'
        below = len([1 for x in ins if float(x) < float(fig.get('against'))])
        return None if round(100.0 * below / len(ins)) == v else \
            'percentile recomputes to %d, sentence says %r' % (round(100.0 * below / len(ins)), v)
    if src == 'derived.spread':
        return None if ins and len(ins) == 2 and close(float(ins[0]) - float(ins[1]), v, 1) else \
            'spread of the declared inputs is not %r' % (v,)
    if src == 'derived.gap':
        if not ins or len(ins) != 2:
            return 'gap declares the wrong number of inputs'
        d = abs(float(ins[0]) - float(ins[1]))
        return None if (close(d, v, 1) or close(round(d, 0), v, 1)) else \
            'gap of the declared inputs is not %r' % (v,)
    return 'unknown provenance %r' % (src,)


def main():
    bad, rendered, seen = [], 0, {d: 0 for d in DIMENSIONS}
    thin, negative = [], []
    for key, label, prof in PROFILES:
        core, _sec, listed_tier = M.peer_groups(prof, M.listed)
        picked, _months, priv_tier = M.select_private(prof, M.private)
        ranges = M.all_ranges(prof, core, listed_tier, picked, priv_tier)
        dims = R.build(prof, core, ranges)
        rendered += 1
        # A NEGATIVE MULTIPLE IS NOT A PRICE, and this dimension is the first thing that reads a
        # range low out loud to a founder in a sentence rather than drawing it as a bar. Reported,
        # not asserted, on the pattern of golden.py --peers: it is a data question for Daniil to
        # rule on, and failing the build tonight would not answer it.
        for lane in ('listed', 'private'):
            for b, r in (ranges.get(lane) or {}).items():
                if r.get('low') is not None and r['low'] <= 0:
                    who = [t for t in (r.get('table') or []) if (t.get('multiple') or 0) <= 0]
                    negative.append((key, lane, b, r['low'], r.get('high'),
                                     ', '.join(str(t.get('company')) for t in who)))
        if len(dims) < 2:
            thin.append((key, len(dims)))
        prev = None
        for d in dims:
            name = d.get('dimension')
            seen[name] = seen.get(name, 0) + 1
            if name not in DIMENSIONS:
                bad.append((key, name, 'dimension is not one of the five in the rubric'))
            # 1  ORDERED BY RANGE IMPACT, NOT BY RUBRIC ORDER.
            imp = float(d.get('impact') or 0)
            if prev is not None and imp > prev + 1e-9:
                bad.append((key, name, 'fix list is out of impact order'))
            prev = imp
            if len(d.get('lines') or []) != 3:
                bad.append((key, name, 'a dimension renders three sentences, this one renders %d'
                            % len(d.get('lines') or [])))
            text = ' '.join(d.get('lines') or [])
            for nm in (d.get('names') or []):
                if nm:
                    text = text.replace(nm, ' ')
            allowed = set()
            for fig in (d.get('figures') or []):
                allowed |= renders(fig.get('value'))
            for tok in NUM.findall(text):
                if tok not in allowed:
                    bad.append((key, name, 'the number %s is printed to a founder and is not a '
                                           'declared figure' % tok))
            for fig in (d.get('figures') or []):
                why = check_figure(fig, prof, ranges)
                if why:
                    bad.append((key, name, why))
        # 3  THE PAYLOAD CARRIES ONLY THE WHITELIST.
        pay = R.reveal_payload(prof, core, ranges)
        for b in pay['blocks']:
            extra = set(b) - set(R.BLOCK_FIELDS)
            if extra:
                bad.append((key, 'payload', 'fields past the whitelist reach the page: %s'
                            % ', '.join(sorted(extra))))

    # THE THREE DIMENSIONS NO FIXTURE CAN EXERCISE, EXERCISED.
    #
    # Every one of the 102 real fixtures carries growth=None and gm=None on purpose: a synthetic
    # growth figure was tried on 3-Sep and reverted within minutes because it moved the peer
    # selection of 42 of 43 fixtures (the note above snap() in selector/golden.py). Retention is
    # never held for a private company at all. So retention, growth and margin can be read for a
    # real founder answering the quiz and for nobody in the suite, and the three dimensions that
    # depend on them would sit untested for ever behind a green check.
    #
    # The same shape as the geography test in tools/investor_coverage.py: declared inputs, made
    # here, used only to prove the path runs and its figures survive recomputation. Nothing
    # synthetic reaches a fixture, a range or the golden suite.
    base = dict(PROFILES[0][2])
    core, _sec, lt = M.peer_groups(base, M.listed)
    picked, _mo, pt = M.select_private(base, M.private)
    rng = M.all_ranges(base, core, lt, picked, pt)
    exercised = []
    for label, prof, fn in (
            ('growth story', dict(base, growth=64.0), R.growth_story),
            ('unit economics', dict(base, gm=41.0), R.unit_economics),
            ('quality of revenue', dict(base, nrr=118.0), R.quality_of_revenue)):
        d = fn(prof, core)
        if not d:
            exercised.append((label, 'no read: the listed set does not disclose enough of it'))
            continue
        text = ' '.join(d['lines'])
        allowed = set()
        for fig in d['figures']:
            allowed |= renders(fig.get('value'))
        for tok in NUM.findall(text):
            if tok not in allowed:
                bad.append(('SYNTHETIC', label, 'undeclared number %s' % tok))
        for fig in d['figures']:
            why = check_figure(fig, prof, rng)
            if why:
                bad.append(('SYNTHETIC', label, why))
        exercised.append((label, 'reads, %d sentences, impact %.1fx' % (len(d['lines']), d['impact'])))

    print('RENDERED  %d fixtures' % rendered)
    for d in DIMENSIONS:
        print('          %-20s %3d fixtures' % (d, seen.get(d, 0)))
    print('DECLARED  the three dimensions no fixture can exercise, on declared inputs:')
    for label, how in exercised:
        print('          %-20s %s' % (label, how))
    if thin:
        # NOT A FAILURE. A dimension with no evidence behind it is meant to stay silent, and the
        # count is the sourcing signal: these founders get a short read because their peers
        # disclose little, not because the rubric is broken.
        print('THIN      %d fixtures get fewer than two dimensions: %s'
              % (len(thin), ', '.join('%s (%d)' % t for t in thin[:12])))
    if negative:
        print('NEGATIVE  %d range(s) reach a founder with a low at or below zero. A negative '
              'multiple is not a price:' % len(negative))
        for key, lane, b, lo, hi, who in negative:
            print('          %-16s %s %s   %.1fx to %.1fx   from %s' % (key, lane, b, lo, hi, who))
    if bad:
        print('\nFAILED %d checks' % len(bad))
        for key, name, why in bad[:40]:
            print('  %-16s %-20s %s' % (key, name, why))
        return 1
    print('\nEvery number printed traces to a profile field, a peer row or a range object.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
