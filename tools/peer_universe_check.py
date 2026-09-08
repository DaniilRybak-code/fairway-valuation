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
  5. A SET A PERSON HAS STRUCK IS NOT A PASS. Added 8-Sep-2026 on Daniil's ruling, after march 1
     showed three aerospace companies passing rules 0 to 4 on restaurant and hospitality rounds:
     "such companies should immediately go into the no-comps list." The gate counts names found
     and cannot judge whether they make sense; a person can. A fixture carrying `struck` on its
     profile (the reason, in words, by whoever read the set) fails here whatever its lanes hold,
     and is printed as the fourth kind of entry on the No-comps list.

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
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(here, 'selector'))
    from golden_profiles import PROFILES             # noqa: E402
    struck_of = {k: p['struck'] for k, _l, p in PROFILES if p.get('struck')}
    rows, failed = [], 0
    for f in files:
        key = f[:-5]
        verdict, fails, facts, warns = score(read(os.path.join(fixdir, f)))
        # RULE 5. A person read the set and struck it; the names it found no longer count.
        if key in struck_of:
            verdict = 'FAIL'
            fails = ['struck on reading: ' + struck_of[key]] + fails
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
    # THE NO-COMPS LIST. Daniil named it on 5-Sep at 23:10 UK, and the name matters: it was briefly
    # called "the register", which in banking means a register of shareholders, so it is not used
    # here again.
    #
    # It holds TWO KINDS OF ENTRY and they belong together, because they are the same failure at
    # two depths. A company SERVED ON A LABEL got comparables the relevance gate would not allow,
    # admitted by the archetype fallback because its lane could not price at all. A company with NO
    # COMPARABLES AT ALL got nothing. In both cases the database could not answer the question the
    # founder asked, and in both cases the answer is a test company we should be able to serve and
    # cannot.
    #
    # WHAT HAPPENS TO IT. Nothing, until the bulk pass. Rule A12 part 3: the four dates before the
    # pilot (8, 11, 15 and 18 September) are MARCHES, 30 to 40 new test companies each, and the list
    # is resolved in ONE pass after the last of them and before launch. It is printed on every run
    # so it stays visible, not so it gets chased.
    import match_reference as M                      # noqa: E402
    del M.archetype_fallbacks[:]
    del M.pinned_names[:]
    for _k, _l, _p in PROFILES:
        M.peer_groups(_p, M.listed)
        M.select_private(_p, M.private)

    no_comps = sorted(k for k, v, f, fc, w in rows if v == 'FAIL')
    lanes_rescued = {(l, g) for l, g, _n, _a in M.archetype_fallbacks}
    print('\n' + '=' * 78)
    print('THE NO-COMPS LIST: every test company the database could not answer')
    # TWO COUNTS, NOT ONE SUM. A fixture can appear in both kinds at once (ultrasonium is rescued
    # on its private lane AND fails the gate), so adding them would count it twice, and this list
    # is the brief for the bulk pass. An inflated brief is a worse brief.
    print('  %d lanes served on a label   |   %d of %d fixtures not served at all, %d of them struck on reading'
          % (len(lanes_rescued), len(no_comps), len(rows), len(struck_of)))
    print('=' * 78)

    print('\n  KIND 1  SERVED ON A LABEL, NOT ON EVIDENCE')
    if M.archetype_fallbacks:
        by_founder = {}
        for lane, sig, name, arch in M.archetype_fallbacks:
            by_founder.setdefault((lane, sig), []).append('%s [%s]' % (name, arch))
        print('          %d comparables across %d lanes. These lanes could not price at all on'
              % (len(M.archetype_fallbacks), len(by_founder)))
        print('          shared vocabulary or a shared end market, so the archetype fallback')
        print('          opened. Each one is a hole in the database, not a feature.')
        for (lane, sig), names in sorted(by_founder.items()):
            print('   %-8s %s' % (lane, sig))
            print('            %s' % ', '.join(names[:6]))
    else:
        print('          None. No founder needed the archetype fallback and every lane priced on')
        print('          real evidence.')

    print('\n  KIND 2  NO COMPARABLES AT ALL, or not enough of them to be a range')
    if no_comps:
        print('          %d of %d fixtures. These are the gate failures above, listed again here'
              % (len(no_comps), len(rows)))
        print('          because a founder we cannot serve is the same problem whether we served')
        print('          them a label or served them nothing.')
        reason_of = {k: '; '.join(f) for k, v, f, fc, w in rows if v == 'FAIL'}
        for k in no_comps:
            print('   %-18s %s' % (k, reason_of[k][:96]))
    else:
        print('          None. Every fixture reached a defensible set on both lanes.')
    # KIND 3, added 6-Sep-2026 on Daniil's afternoon follow-ups. A comparable can clear the relevance
    # gate on evidence that is technically evidence and practically nothing: a word carried by 25 or
    # more companies ("marketplace", "ai", "platform"), or the end market alone with no product word
    # in common (any healthcare company for a clinical-trials marketplace). Daniil's examples:
    # DeHaat, an agritech marketplace, shown to inato on "marketplace" and "network"; Cityblock and
    # Tecsys shown to inato on Healthcare alone. These names are not removed here, because every
    # tightening of the gate that was measured on 6-Sep cost real peers elsewhere (see
    # docs/matching-refinement-6sep.md 3c). They are RECORDED, so the bulk pass can see them and a
    # banker reading the free-tier answers can strike them.
    def _kind3(prof, r, why):
        route = M.relevance_route(prof, r, why)
        A = {x.strip().lower() for x in (prof.get('product_tags') or '').split('|') if x.strip()}
        B = {x.strip().lower() for x in (r.get('product_tags') or '').split('|') if x.strip()}
        if A & B:
            return None
        shared = M.toks(prof.get('product_tags') or '') & M.toks(r.get('product_tags') or '')
        if route == 'shared product vocabulary':
            if max(M.TOKW.get(t, 1.0) for t in shared) <= 0.2:
                return 'generic words: ' + ', '.join(sorted(shared))
            return None
        if route == 'same specific end market' and not shared:
            return 'end market alone: ' + (prof.get('industry') or '')
        return None

    kind3 = {}
    kind3_n = slots = words = market = lanes_touched = 0
    bare = []
    for _k, _l, _p in PROFILES:
        core, _sec, _t = M.peer_groups(_p, M.listed)
        picked, _m, _t2 = M.select_private(_p, M.private)
        for lane, grp in (('listed', core), ('private', picked)):
            flags = []
            for (sc, why), r in grp:
                slots += 1
                tag = _kind3(_p, r, why)
                flags.append(bool(tag))
                if tag:
                    kind3.setdefault(_k, []).append('%s (%s; %s)' % (r['company_name'], lane, tag))
                    kind3_n += 1
                    if tag.startswith('generic'):
                        words += 1
                    else:
                        market += 1
            if any(flags):
                lanes_touched += 1
            if flags and all(flags):
                bare.append('%s %s' % (_k, lane))
    print('\n  PINNED BY NAME  (the also_compare list, rule A2 in reverse: a name, a founder, a reason)')
    if M.pinned_names:
        for lane, sig, name, reason in sorted(set(M.pinned_names)):
            print('   %-8s %-44s %-20s %s' % (lane, sig, name, reason[:90]))
    else:
        print('          None.')
    print('\n  KIND 3  SERVED ON A GENERIC WORD OR ON THE END MARKET ALONE')
    print('          %d of %d comparable slots (a name in a founder\'s lane) cleared the relevance gate'
          % (kind3_n, slots))
    print('          with no whole tag in common: %d on words carried by 25 or more companies, %d on'
          % (words, market))
    print('          the end market alone. %d fixtures and %d of %d lanes carry at least one.'
          % (len(kind3), lanes_touched, 2 * len(PROFILES)))
    print('          LANES RESTING ON NOTHING ELSE: %d%s' % (len(bare), (': ' + ', '.join(bare)) if bare else ''))
    print('          Kept in the lanes (every tighter gate measured on 6-Sep cost real peers elsewhere);')
    print('          recorded so the bulk pass and the banker read can see them.')
    for k in sorted(kind3):
        print('   %-18s %s' % (k, '; '.join(kind3[k])[:220]))

    # KIND 4, added 8-Sep-2026 on Daniil's ruling (rule 5 above). The gate passed Orca Aerospace,
    # Constellation Space and Zymbly on Samsara, Owner, Guesty and Restaurant365, because those
    # rows share the words "operations", "software" and "mission" and the archetype Vertical
    # Software, and nothing in rules 0 to 4 can tell that a satellite operator is not a
    # restaurant. A person can, and when they do the fixture is struck: it fails the gate and it
    # is listed here with what it was shown, so the bulk pass sees the hole and so the same names
    # are not shown to a founder in that market without a banker striking them first.
    print('\n  KIND 4  STRUCK ON READING: served on names a person judged irrelevant')
    if struck_of:
        print('          %d of %d fixtures. Each passed or would have passed rules 0 to 4; a person read'
              % (len(struck_of), len(rows)))
        print('          the set and struck it. They fail the gate and count above as not served.')
        for k in sorted(struck_of):
            print('   %-18s %s' % (k, struck_of[k]))
    else:
        print('          None.')

    print('\n  Resolved in ONE bulk pass after the 18 September march and before launch')
    print('  (rule A12 part 3). Not chased lane by lane in between.')

    empty_secondary = sorted(k for k, v, f, fc, w in rows if v == 'PASS' and fc['secondary'] == 0)
    if empty_secondary:
        print('\nPASSING WITH AN EMPTY SECONDARY LANE (%d): %s'
              % (len(empty_secondary), ', '.join(empty_secondary)))
        print("Allowed by Daniil's ruling of 4-Sep: a public lane and a private lane is the bar,")
        print('and these have both. Reported so the sourcing list stays visible.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
