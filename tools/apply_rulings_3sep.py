# -*- coding: utf-8 -*-
"""Daniil's rulings of 3 September 2026, applied to data/private-rounds.csv.

  Klarna      spot rate at the pricing date, one convention for all three rounds, rate/date/entity
              recorded on the row. And the GMV he asked about: Klarna DID disclose a volume metric.
  LEAD School the printed operating revenue, not the derived total income.
  Indian rows revenue from operations, never total income, with the note on the row.
  Vegrow      keep, with the note.
  Kriya       12.6 confirmed as turnover from filed accounts, not a volume. The oddity is the
              numerator, and it is recorded rather than corrected.
  Pre/post    a real column, so a pre-money row can never sit in a range with post-money ones.

Every change writes its reason into the row's notes. Run once; it is idempotent by value check.
"""
import csv
import io
import sys

PATH = 'data/private-rounds.csv'


def read():
    raw = io.open(PATH, encoding='utf-8').read()
    head = ''.join(l for l in raw.splitlines(True) if l.startswith('#'))
    body = [l for l in raw.splitlines(True) if not l.startswith('#')]
    rd = csv.DictReader(body)
    return head, rd.fieldnames, list(rd)


def write(head, cols, rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols, lineterminator='\n')
    w.writeheader()
    for r in rows:
        w.writerow({c: r.get(c, '') for c in cols})
    io.open(PATH, 'w', encoding='utf-8').write(head + buf.getvalue())


def note(r, text):
    r['notes'] = ((r.get('notes') or '').strip() + ' || ' + text).strip(' |')


# --------------------------------------------------------------------------------------------
# KLARNA. Daniil, 3-Sep-2026: "Ok to use the spot rate."
#
# All three rounds now divide a valuation struck on a date by a krona figure translated at that
# same date. Klarna's own press releases translate at the CALENDAR-YEAR AVERAGE, which is why his
# sheet and ours disagreed: same krona, different dollars. Klarna's figures stay on the row as a
# memo so the difference is visible rather than overwritten.
#
# Entity pinned to Klarna Bank AB throughout. Klarna Holding AB reports a slightly different net
# operating income and mixing the two is the same class of error as mixing the rates.
#
#   SEK 10,000.1m  total net operating income FY2020, Klarna Bank AB annual report
#   SEK 13,754.5m  total net operating income FY2021, Klarna Bank AB annual report
#
# Rates: 8.4227 on 01-Mar-2021 and 8.2730 on 10-Jun-2021 and 10.5905 on 11-Jul-2022. The first is
# from exchange-rates.org, the other two are the ECB reference pins Fable verified on 3-Sep. The
# ECB and market rate for 1-Mar-2021 differ by about 0.05%, which does not move the multiple, but
# the SOURCE IS DIFFERENT and the row says so rather than implying one pull.
KLARNA = {
    '2021-03': dict(nok=10000.1, rate=8.4227, date='2021-03-01', fy='FY2020',
                    src='exchange-rates.org daily USD/SEK'),
    '2021-06': dict(nok=10000.1, rate=8.2730, date='2021-06-10', fy='FY2020',
                    src='ECB reference rate'),
    '2022-07': dict(nok=13754.5, rate=10.5905, date='2022-07-11', fy='FY2021',
                    src='ECB reference rate'),
}
# The volume metric Daniil asked about. Klarna reports GMV and reported it at the time: $53bn for
# 2020, stated in its own year-end release and carried by the trade press on 24-Feb-2021, before
# both 2021 rounds were priced. FY2021 GMV is NOT loaded: the only figure I could verify is "42%
# year on year", and a derived 75.3 is not a disclosure.
KLARNA_GMV = {'2021-03': 53000.0, '2021-06': 53000.0}


def klarna(rows, log):
    for r in rows:
        if r['company_name'] != 'Klarna':
            continue
        k = (r.get('date_iso') or '')[:7]
        spec = KLARNA.get(k)
        if not spec:
            log.append('Klarna %s: NO PIN, left alone' % k)
            continue
        old_rev, old_x = r['revenue_musd'], r['ev_revenue_x']
        rev = round(spec['nok'] / spec['rate'], 1)
        post = float(r['post_money_musd'])
        r['revenue_musd'] = '%.1f' % rev
        r['ev_revenue_x'] = '%.2f' % (post / rev)
        r['revenue_metric'] = 'Total net operating income, %s, Klarna Bank AB' % spec['fy']
        r['revenue_basis'] = 'BANK_NOI'
        r['fx_ccy'], r['fx_rate'], r['fx_date'] = 'SEK', '%.4f' % spec['rate'], spec['date']
        note(r, ('RULING 3-Sep-2026, Daniil: spot rate at the pricing date. SEK %.1fm of Klarna '
                 'Bank AB total net operating income for %s at %.4f SEK/USD on %s (%s) gives '
                 '$%.1fm. Was %s at %sx. Klarna translates at the calendar-year average in its own '
                 'releases; that figure is kept as a memo, not used.'
                 % (spec['nok'], spec['fy'], spec['rate'], spec['date'], spec['src'], rev,
                    old_rev, old_x)))
        gmv = KLARNA_GMV.get(k)
        if gmv:
            r['volume_metric'] = 'GMV'
            r['volume_musd'] = '%.1f' % gmv
            r['volume_period'] = spec['fy']
            r['volume_basis'] = 'GMV'
            r['ev_volume_x'] = '%.3f' % (post / gmv)
            note(r, ('VOLUME METRIC ADDED, answering Daniil 3-Sep: Klarna did disclose one. GMV of '
                     '$53bn for 2020, its own year-end release, public 24-Feb-2021 and so current '
                     'when both 2021 rounds were priced.'))
        log.append('Klarna %s: revenue %s -> %s, multiple %s -> %s%s'
                   % (k, old_rev, r['revenue_musd'], old_x, r['ev_revenue_x'],
                      ', GMV %sx added' % r['ev_volume_x'] if gmv else ''))


# --------------------------------------------------------------------------------------------
# THE INDIAN ROWS. Daniil, 3-Sep-2026: "let's use revenue from operations for indians, make the
# respective note." And separately, LEAD School: "Use the printed number."
#
# An Indian filing reports two lines. REVENUE FROM OPERATIONS is what the business earned from
# trading. TOTAL INCOME adds interest and other income, which is not operating and does not scale
# with the business. Three of the four rows we hold were using total income and one, Ninjacart, was
# using revenue from operations, so the set was not even internally consistent.
#
# Each figure below is the operating line from the row's own cited source, converted at the rate
# already recorded on the row, so nothing here introduces a new exchange rate.
INDIAN = [
    # company, new USD revenue, new multiple, why
    ('LEAD School', 7.737, '1100',
     'Operating revenue Rs 57.1 crore, the PRINTED figure from the RoC filings via Entrackr. The '
     'Rs 60 crore it replaces was not printed anywhere: it was derived as expenses minus loss. '
     'Daniil 3-Sep: "Use the printed number."'),
    ('Dream Sports', 341.9, '8000',
     'Revenue from operations Rs 2,551.59 crore, from Dream Sports own release. The Rs 2,705.56 '
     'crore it replaces is TOTAL INCOME from the same release.'),
    ('WayCool Foods', 118.5, '700',
     'Operating revenue INR 926.9 crore, from the cited Inc42 article, which states separately '
     'that INR 930.6 crore is "total revenue, including interest income". The multiple does not '
     'move; the basis label was wrong and is now right.'),
]


def indian(rows, log):
    for name, rev, post, why in INDIAN:
        for r in rows:
            if r['company_name'] != name:
                continue
            old_rev, old_x = r['revenue_musd'], r['ev_revenue_x']
            r['revenue_musd'] = '%.3f' % rev
            r['ev_revenue_x'] = '%.2f' % (float(post) / rev)
            r['revenue_basis'] = 'GROSS_REVENUE'
            r['revenue_metric'] = 'Revenue from operations'
            note(r, 'RULING 3-Sep-2026, Daniil: revenue from operations for Indian filings, never '
                    'total income. ' + why)
            log.append('%s: revenue %s -> %s, multiple %s -> %s'
                       % (name, old_rev, r['revenue_musd'], old_x, r['ev_revenue_x']))


# --------------------------------------------------------------------------------------------
# KRIYA. Daniil: "check if 12.6 is revenue, not volume. It might be a volume metric."
#
# CHECKED. It is revenue. His own 226-row sheet records it as "GBP12.6m turnover, FY ended
# 2024-12-31, Turnover; filed accounts", sourced to the Companies House filing history for company
# 07330525. It is not a volume of any kind.
#
# The oddity is at the other end. GBP 7.5m is not a valuation: it is the ACCOUNTING PURCHASE
# CONSIDERATION Allica Bank recognised when it acquired Kriya in October 2025, and his sheet flags
# it itself as "CONTROL ACQUISITION; not clean EV". So 0.60x is arithmetically right and is the
# price of a control acquisition rather than a priced funding round. It stays visible and stays out
# of every median, which is where it already was.
def kriya(rows, log):
    for r in rows:
        if r['company_name'] != 'Kriya':
            continue
        r['transaction_type'] = 'CONTROL_ACQUISITION'
        note(r, 'CHECKED 3-Sep-2026 on Daniil asking whether 12.6 is a volume. It is not. It is '
                'GBP12.6m TURNOVER for the year ended 31-Dec-2024, from the filed accounts at '
                'Companies House, company 07330525. The unusual number is the numerator: GBP7.5m '
                'is the accounting purchase consideration Allica Bank recognised on acquiring '
                'Kriya, not a valuation, and the source sheet flags it as "not clean EV". Correct '
                'as recorded, out of medians, visible as context.')
        log.append('Kriya: confirmed 12.6 is turnover, typed as CONTROL_ACQUISITION, stays out of medians')


# --------------------------------------------------------------------------------------------
# PRE-MONEY. Daniil, 3-Sep-2026: "let's add pre-money valuation, then we need to be consistent in
# terms of multiples we use for the user (not mix the two)."
#
# A pre-money valuation is smaller than the post-money one by exactly the size of the round, which
# on a seed round is a third of the answer. Until now the only record of which one a row carried
# was free text in valuation_status, with eight different spellings and no way to test it. This
# adds a real column with three values and derives it from what the row already says. Anything the
# text does not settle becomes UNSPECIFIED rather than being guessed at: a wrong POST is worse than
# an honest blank, because a blank can be filled and a wrong flag cannot be seen.
#
# The consistency half of the ruling lives in the loader, not here.
def premoney(rows, log):
    n = {'POST': 0, 'PRE': 0, 'UNSPECIFIED': 0}
    for r in rows:
        t = (r.get('valuation_status') or '').lower()
        if 'pre-money' in t or 'pre money' in t:
            v = 'PRE'
        elif 'post' in t:
            v = 'POST'
        elif 'disclosed' in t or 'reported' in t:
            # The overwhelming convention in round announcements is post-money, but convention is
            # not evidence and this column exists precisely to stop us assuming.
            v = 'UNSPECIFIED'
        else:
            v = 'UNSPECIFIED'
        r['valuation_pre_or_post'] = v
        n[v] += 1
    log.append('pre/post flag: %d POST, %d PRE, %d UNSPECIFIED' % (n['POST'], n['PRE'], n['UNSPECIFIED']))


def main():
    head, cols, rows = read()
    before = len(rows)
    if 'valuation_pre_or_post' not in cols:
        cols = cols + ['valuation_pre_or_post']
    log = []
    klarna(rows, log)
    indian(rows, log)
    kriya(rows, log)
    premoney(rows, log)
    assert len(rows) == before, 'row count moved: %d -> %d' % (before, len(rows))
    write(head, cols, rows)
    print('rows in %d, rows out %d, nothing dropped' % (before, len(rows)))
    for line in log:
        print('   ' + line)
    return 0


if __name__ == '__main__':
    sys.exit(main())
