# -*- coding: utf-8 -*-
"""Check every private multiple's BASIS and PERIOD label against the row's own words.

Daniil, 31-Aug-2026: "make sure we know which are LTM vs NTM and which are gross vs net."

Having a label is not the same as having the RIGHT label, and a wrong label is worse than a blank
because a blank is honest while a wrong one silently prices somebody. So this reads the metric
wording and the notes on every row and reports where they contradict the label.

It ASSERTS NOTHING. It reports. A human decides, because the wording is often genuinely ambiguous
and a script that guesses is how we got here.
"""
import os, re, sys, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'selector'))
import match_reference as M

GROSS_WORDS = ('gross revenue', 'gross revenues', 'gross sales', 'gross merchandise', 'gmv',
               'turnover', 'pass-through', 'pass through', 'total payment volume', 'tpv',
               'gross booking', 'system-wide', 'billings')
NET_WORDS = ('net revenue', 'net revenues', 'take rate', 'commission', 'net sales')
FWD_WORDS = ('expected', 'projected', 'forecast', 'next twelve', 'ntm', 'guidance', 'will reach',
             'projecting to')
RUNRATE_WORDS = ('run rate', 'run-rate', 'annualized', 'annualised', r'\barr\b')
TRAIL_WORDS = ('fy20', 'fy21', 'fy22', 'fy23', 'fy24', 'fy25', 'year ended', 'last twelve',
               'ltm', 'trailing', 'full year')

def words(r):
    # ONLY THE METRIC WORDING AND THE DENOMINATOR BASIS. The notes field was in here on the first
    # pass and it poisoned the result: Klarna's note explains the annualisation of a DIFFERENT row
    # and the checker read that as Klarna's own denominator being a run rate. A checker that cries
    # wolf is worse than no checker, so it now reads only the two fields that describe THIS number.
    return ' '.join(str(r.get(f) or '') for f in ('revenue_metric', 'denominator_basis')).lower()

def main():
    priced = [r for r in M.private if r.get('mult') is not None]
    flags = collections.defaultdict(list)
    for r in priced:
        w = words(r)
        basis = (r.get('revenue_basis') or '').upper()
        period = (r.get('revenue_period') or '').upper()
        gross_said = any(x in w for x in GROSS_WORDS)
        net_said = any(x in w for x in NET_WORDS)
        rr_said = any((re.search(x, w) if x.startswith(chr(92)) else x in w) for x in RUNRATE_WORDS)
        fwd_said = any(x in w for x in FWD_WORDS)
        tr_said = any(x in w for x in TRAIL_WORDS)
        tag = '%s | %s | %s' % (r['company_name'], r['date'], r['mult'])

        if gross_said and basis in ('NET_REVENUE', 'ARR', 'ARR_RUNRATE'):
            flags['BASIS: wording says GROSS, label says net-equivalent'].append(
                (tag, basis, _snip(r)))
        if net_said and basis == 'GROSS_REVENUE':
            flags['BASIS: wording says NET, label says GROSS'].append((tag, basis, _snip(r)))
        if not gross_said and not net_said and basis in ('NET_REVENUE', 'GROSS_REVENUE'):
            flags['BASIS: label asserts a basis the wording never states'].append(
                (tag, basis, _snip(r)))
        if rr_said and period == 'LTM':
            flags['PERIOD: wording says RUN RATE, label says LTM'].append((tag, period, _snip(r)))
        if fwd_said and period != 'NTM':
            flags['PERIOD: wording is FORWARD LOOKING, label is not NTM'].append(
                (tag, period, _snip(r)))
        if tr_said and not rr_said and period == 'RUN_RATE':
            flags['PERIOD: wording names a CLOSED YEAR, label says run rate'].append(
                (tag, period, _snip(r)))

    print('%d private rows carry a multiple.\n' % len(priced))
    total = 0
    for k in sorted(flags):
        print('%s  (%d)' % (k, len(flags[k])))
        for tag, lab, snip in flags[k]:
            print('    %-46s label=%-14s %s' % (tag, lab, snip))
        print()
        total += len(flags[k])
    print('%d rows need a human to look at the label.' % total)
    print('%d rows agree with their own words.' % (len(priced) - total))
    return 0

def _snip(r):
    t = re.sub(r'\s+', ' ', str(r.get('revenue_metric') or ''))
    return ('"' + t[:88] + '"') if t else '(no metric wording recorded)'

if __name__ == '__main__':
    sys.exit(main())
