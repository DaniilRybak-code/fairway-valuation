# -*- coding: utf-8 -*-
"""Apply Daniil's rulings of 31-Aug-2026 to the private rounds, and add the source URLs.

HIS RULINGS, VERBATIM WHERE THEY SET A STANDING RULE:

  ZEPZ. "take the number from the round announcement (and should be the rule elsewhere - this is
  the primary source usually, should be higher priority than accounts). Save the net figure just in
  case too, but make a note of it."

  That is a GENERAL rule and it is recorded here as one: where a round announcement and later filed
  accounts both describe the same period, the ANNOUNCEMENT WINS, because it is what the investor
  actually priced against. The accounts figure is kept in the note, never silently discarded.

  MARQETA. "use contemporaneous source (Forbes)."
  RAZORPAY. "so we do NOT have the number for denominator at the time of pricing? Why do we keep it
  then?" Dropped.
  PINE LABS. "choose 1 source of denominator, explain why you did it."
  BETTER.COM. "ok to use SPAC valuation, with the respective comment."
"""
import csv, io, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

def split(p):
    L = open(p).readlines()
    head, body, started = [], [], False
    for l in L:
        if not started and (l.lstrip('"').startswith('#') or not l.strip()):
            head.append(l); continue
        started = True; body.append(l)
    return head, list(csv.DictReader(io.StringIO(''.join(body))))

def write(p, head, rows):
    w = io.StringIO(); o = csv.DictWriter(w, fieldnames=list(rows[0].keys()))
    o.writeheader(); o.writerows(rows)
    open(p, 'w').write(''.join(head) + w.getvalue())

# tid -> {field: value}
EDITS = {
 # ZEPZ. The announcement figure wins over the filed accounts, per the new standing rule.
 'zepz-2021-08': dict(
    revenue_musd='338.0', ev_revenue_x='14.8', revenue_metric='FY2021 revenue as stated in the round announcement',
    verification='RULED_31AUG', in_medians='1',
    notes=('RULED BY DANIIL 31-Aug-2026, AND THE RULING IS A GENERAL RULE. Where a round '
           'announcement and later filed accounts both describe the same period, the ANNOUNCEMENT '
           'WINS: it is the primary source and it is what the investor priced against. $338m is the '
           'round-announcement figure and gives 14.8x. The filed-accounts figure for the same period '
           'is $238m, which would give 21.0x, and it is kept here on purpose rather than discarded. '
           'BASIS RISK, UNRESOLVED: the two figures differ by 42 per cent, which is the size of a '
           'gross-versus-net gap on a remittance business. If $338m turns out to be gross, this row '
           'is a gross multiple and must leave the net-revenue range.')),
 # MARQETA. Contemporaneous Forbes, which is a floor, so the multiple is a ceiling. Context only.
 'marqeta-2020-05': dict(
    revenue_musd='300.0', ev_revenue_x='14.3', bound='<=', revenue_basis='GROSS_REVENUE',
    revenue_metric='FY2019 estimated revenue, "more than" / "exceeded" $300m',
    denominator_basis='CONTEMPORANEOUS_PRESS_THRESHOLD', in_medians='0', verification='RULED_31AUG',
    revenue_source_url='https://www.forbes.com/sites/jeffkauflin/2020/05/28/payments-startup-marqeta-more-than-doubles-valuation-to-43-billion/',
    round_source_url='https://www.marqeta.com/blog/marqeta-raises-150-million-in-new-capital',
    notes=('RULED BY DANIIL 31-Aug-2026: use the contemporaneous Forbes figure. It was published on '
           'the pricing date; the S-1 net-revenue figure of $143.267m was published a year later and '
           'nobody pricing this round had seen it. "More than $300m" is a THRESHOLD, so 14.3x is a '
           'CEILING, not a point. The basis is unstated and probably gross, so this row is context '
           'and stays out of every range.')),
 # RAZORPAY. No denominator existed at pricing, so there is nothing to divide by.
 'razorpay-2021-12': dict(
    ev_revenue_x='', in_medians='0', display_gate='NO_FIELD', verification='RULED_31AUG',
    notes=('DROPPED BY DANIIL 31-Aug-2026: "so we do NOT have the number for denominator at the '
           'time of pricing? Why do we keep it then?" FY2022 revenue was not available at the '
           'Dec-2021 pricing and FY2021 is on the wrong side of the gross-versus-net question. The '
           'row is kept for audit with no multiple, and cannot reach a founder.')),
 # PINE LABS. One denominator chosen, with the reason.
 'pinelabs-2021-05': dict(
    verification='RULED_31AUG', in_medians='1',
    revenue_source_url='https://entrackr.com/2022/07/pine-labs-revenue-drops-14-in-fy21-as-losses-surge-2-64x/',
    notes=('DENOMINATOR CHOSEN 31-Aug-2026 AND HERE IS WHY. Two figures were in play: the FY2021 '
           'statutory total revenue of Rs 726.16 crore, and a cited "$107m / Rs 800 crore" net '
           'revenue on an undefined basis. We use Rs 726.16 crore, about $99.08m at Rs 73.27 on the '
           'pricing date, giving 30.3x against the $3.0bn post-money. Three reasons: it is a defined '
           'and auditable line for a period that closed on 31-Mar-2021, before the 17-May-2021 '
           'pricing; the rival figure states neither a definition nor a period, so we would not know '
           'what we were dividing by; and it is the figure the market actually cites. THE CHOICE '
           'BARELY MATTERS, WHICH IS ITSELF THE ARGUMENT FOR KEEPING THE ROW: $3,000m over $99.08m '
           'is 30.3x and over $107m is 28.0x, an eight per cent difference rather than the order of '
           'magnitude that would justify dropping it. CAVEAT ON THE FILE: the statutory figure was '
           'first reported in July 2022, fourteen months after pricing, so no investor priced '
           'against this exact number.')),
 # BETTER.COM. Kept, with the comment he asked for.
 'better-2021-05': dict(
    verification='RULED_31AUG', in_medians='1',
    notes=('KEPT BY DANIIL 31-Aug-2026: "ok to use SPAC valuation, with the respective comment." '
           'THE COMMENT: a SPAC valuation is NEGOTIATED between the sponsor and the target, not '
           'cleared by a market of competing buyers, so it is weaker evidence than a priced venture '
           'round. Better.com in particular closed far below this level. Use it as evidence of what '
           'was agreed in May 2021, not as a market clearing price. The workbook covers a different '
           'Better.com transaction, the April 2021 secondary, and marks that one not usable.')),
}

def main():
    for f in ('private-rounds.csv', 'private-rounds-consumer.csv'):
        p = os.path.join(D, f)
        head, rows = split(p)
        n = 0
        for r in rows:
            e = EDITS.get(r['transaction_id'])
            if not e: continue
            for k, v in e.items():
                if k not in r:
                    print('  WARNING: %s has no column %s, skipped' % (f, k)); continue
                r[k] = v
            n += 1
            print('  %-26s ruled' % r['transaction_id'])
        if n: write(p, head, rows)
    print('done')

if __name__ == '__main__':
    main()
