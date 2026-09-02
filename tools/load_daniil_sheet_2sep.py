#!/usr/bin/env python3
"""
Loads the 63 rows of data/raw/2026-09-01_private-transactions-daniil.csv whose companies were
never inserted into data/private-rounds.csv. WHOOP, Revolut, Stripe, Plaid, Monzo, Chime and 40
more.

WHY THEY SAT UNLOADED. Nothing was missing from Daniil's sheet. Its nine columns are complete on
191 of 191 rows. What was missing was OUR step: his sheet carries no screening category, and the
matcher joins on that field, so every company needs placing in our vocabulary before its round
can be selected for anyone. That step was queued behind the investor build and the sector screen
and should not have been.

VERIFICATION TIER. These load as `SHEET_02SEP`, not VERIFIED. In this file VERIFIED means a human
opened the source and checked the figure against the sentence in it. These have not had that.
The figures, the bases and both URLs are Daniil's; the categories, bounds and median flags are
ours. Precedent for a lower tier already exists in the file, SOURCED_31AUG and RULED_31AUG.

WHAT IS HELD OUT OF THE MEDIANS, and why, since that is the decision that matters:

  Volume-only metrics (13 rows). LOANS_ORIGINATED, PAYMENT_VOLUME, PAID_SUBSCRIBERS and
  OTHER_VOLUME do not produce a revenue multiple at all. They load into the volume fields with
  the revenue fields empty, exactly as the GMV rows already do.

  Deposit-taking banks and neobanks (10 rows). Standing rule: lenders and deposit-taking banks
  price on book, never on EV/revenue. Revolut, Monzo, Chime, N26, Atom Bank, Mercury and Qonto
  load with their revenue multiple recorded and in_medians 0 until a book figure exists.

  Entity-proxy denominators (2 rows). SumUp Dec-23 is a "revenue / entity proxy" and
  Checkout.com is "UK entity revenue". A single legal entity is not the group, so the multiple
  is not comparable.

  Stated proxies (2 rows). Cohere's "annual revenue / ARR proxy" and Coalition's "annualized GWP
  / revenue proxy". GWP is premium written, not the insurer's revenue.

  One arithmetic doubt (1 row). Kriya, post-money 7.5 against revenue 12.6, giving 0.60x. A
  seven-and-a-half-million post-money on a company with twelve million of revenue is possible but
  unlikely; more likely the post-money is in a different unit. Loaded, flagged, held out.
"""
import csv, io, os, re, sys

RAW = 'data/raw/2026-09-01_private-transactions-daniil.csv'
DST = 'data/private-rounds.csv'

# company -> (screening category, subsector). Categories are taken from the vocabulary already in
# data/private-rounds.csv and tools/load_seed_screen.py. Two are new and are named in the report:
# "Connected Hardware & Wearables" and "Crypto & Digital Assets".
CAT = {
  'WHOOP': ('Connected Hardware & Wearables', 'Wearable health hardware with subscription'),
  'Revolut': ('Digital Bank & Deposits', 'Consumer neobank'),
  'Kriya': ('Lending & Credit', 'B2B embedded lending'),
  'Supabase': ('Cloud & Infrastructure Software', 'Open-source backend / Postgres platform'),
  'Strava': ('Personal Software / Productivity', 'Fitness social network and subscription'),
  'Plaid': ('Financial Data', 'Bank data connectivity'),
  'Mercury': ('Digital Bank & Deposits', 'Business banking platform'),
  'Stripe': ('Merchant Acquiring & PSP', 'Online payments'),
  'Olive & June': ('D2C / Consumer Brand', 'Nail care'),
  'Alan': ('Insurance', 'Digital health insurer'),
  'Monzo': ('Digital Bank & Deposits', 'Consumer neobank'),
  'Chime': ('Digital Bank & Deposits', 'Consumer neobank'),
  'SumUp': ('Merchant Acquiring & PSP', 'SMB card acceptance'),
  'Checkout.com': ('Merchant Acquiring & PSP', 'Enterprise online acquiring'),
  'Atom Bank': ('Digital Bank & Deposits', 'App-based bank'),
  'Cohere': ('Data, AI & Developer Tools', 'Foundation models / generative AI'),
  'Raisin': ('Financial Data', 'Deposit marketplace'),
  'Incredible Health': ('Vertical Software', 'Healthcare staffing marketplace'),
  'Contentsquare': ('Data, AI & Developer Tools', 'Digital experience analytics'),
  'Wefox': ('Insurance', 'Insurtech distribution'),
  'Coalition': ('Insurance', 'Cyber insurance MGA'),
  'Xpansiv': ('Financial Data', 'Environmental commodity markets'),
  'Chainalysis': ('Cybersecurity', 'Blockchain analytics and compliance'),
  'Stenn': ('Lending & Credit', 'Trade finance'),
  'Remote': ('Enterprise Applications', 'HR, payroll and global workforce'),
  'Blockchain.com': ('Crypto & Digital Assets', 'Crypto exchange and wallet'),
  'Wayflyer': ('Lending & Credit', 'E-commerce revenue-based finance'),
  'Fireblocks': ('Cybersecurity', 'Digital-asset custody infrastructure'),
  'AG1 (Athletic Greens)': ('D2C / Consumer Brand', 'Nutrition subscription'),
  'Spendesk': ('Vertical Software', 'Spend management / corporate cards'),
  'Brex': ('Vertical Software', 'Spend management / corporate cards'),
  'Qonto': ('Digital Bank & Deposits', 'SMB business banking'),
  'Mambu': ('Cloud & Infrastructure Software', 'Core banking SaaS'),
  'Pleo': ('Vertical Software', 'Spend management / corporate cards'),
  'Tipalti': ('Enterprise Applications', 'Accounts payable automation'),
  'MoonPay': ('Crypto & Digital Assets', 'Crypto on-ramp payments'),
  'N26': ('Digital Bank & Deposits', 'Consumer neobank'),
  'Tala': ('Lending & Credit', 'Emerging-market consumer lending'),
  'Flo Health': ('Personal Software / Productivity', "Women's health app subscription"),
  'Packable': ('Owned-Inventory Retail', 'Amazon marketplace aggregator'),
  'Carta': ('Vertical Software', 'Cap table and fund administration'),
  'Rapyd': ('Merchant Acquiring & PSP', 'Cross-border payments platform'),
  'Clearco': ('Lending & Credit', 'E-commerce revenue-based finance'),
  'Mollie': ('Merchant Acquiring & PSP', 'European online payments'),
  'Calm': ('Personal Software / Productivity', 'Meditation subscription'),
  'Buffer': ('Marketing & Customer Engagement', 'Social media scheduling'),
}

BANKS = {'Revolut', 'Monzo', 'Chime', 'N26', 'Atom Bank', 'Mercury', 'Qonto'}
VOLUME = {'LOANS_ORIGINATED', 'PAYMENT_VOLUME', 'OTHER_VOLUME', 'GMV'}

# per-row reasons for holding a row out of the medians, keyed on company + date
HOLD = {
  ('SumUp', '2023-12-11'): 'Denominator is a single-entity revenue proxy, not the group.',
  ('Checkout.com', '2023-12-01'): 'Denominator is UK entity revenue, not the group.',
  ('Cohere', '2023-06-08'): 'Denominator is described as an ARR proxy, not a disclosed figure.',
  ('Coalition', '2022-07-08'): 'Denominator is annualised gross written premium used as a revenue '
                               'proxy. GWP is premium written, not the insurer\'s revenue.',
  ('Kriya', '2025-10'): 'Post-money 7.5 against revenue 12.6 gives 0.60x. The post-money is '
                        'probably in a different unit. Held out until confirmed.',
  ('Rapyd', '2021-01-13'): 'Basis text says it is unclear whether the period had closed.',
  ('Tipalti', '2021-12'): 'Basis text says the annual period is not specified.',
}

MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']


def basis_of(metric, text):
    t = (text or '').lower()
    if metric == 'ARR':
        return 'ARR'
    if metric in ('RUN_RATE',):
        return 'ARR_RUNRATE'
    if metric == 'GROSS_REVENUE':
        return 'GROSS_REVENUE'
    if metric == 'REVENUE':
        return 'NET_REVENUE' if 'net revenue' in t else 'GROSS_REVENUE'
    return 'NONE'


def period_of(metric, text):
    t = (text or '').lower()
    if metric in ('ARR', 'RUN_RATE'):
        return 'RUN_RATE'
    if 'forward' in t or 'expect' in t:
        return 'NTM'
    if metric == 'REVENUE':
        return 'LTM'
    return ''


def main():
    def rd(p):
        lines = [l for l in open(p) if not l.startswith('#')]
        return csv.DictReader(io.StringIO(''.join(lines)))

    raw = list(rd(RAW))
    dstr = rd(DST)
    cols = dstr.fieldnames
    existing = list(dstr)
    key = lambda n: re.sub(r'[^a-z0-9]', '', (n or '').lower())
    have = set(key(r['company_name']) for r in existing)
    try:
        cons = list(rd('data/private-rounds-consumer.csv'))
        have |= set(key(r.get('company_name') or '') for r in cons)
    except IOError:
        pass

    todo = [r for r in raw if key(r['company']) not in have]
    unknown = sorted(set(r['company'] for r in todo if r['company'] not in CAT))
    if unknown:
        sys.exit('no category for: ' + ', '.join(unknown))

    new, held = [], 0
    for r in todo:
        c = r['company']
        cat, sub = CAT[c]
        d = r['txn_date']
        m = re.match(r'^(\d{4})-(\d{2})(?:-(\d{2}))?$', d)
        yr, mo = m.group(1), int(m.group(2))
        iso = '%s-%02d' % (yr, mo)
        pretty = '%s-%s' % (MONTHS[mo - 1], yr[2:])
        metric, val, mult = r['metric_type'], r['metric_value_m'], r['mult_reported']
        basis_txt = r['denominator_basis']

        row = {k: '' for k in cols}
        row.update(
            transaction_id='%s-%s' % (key(c), iso),
            company_key=key(c), company_name=c, date=pretty, date_iso=iso,
            post_money_musd='%.1f' % float(r['post_money_m']),
            valuation_status='Disclosed',
            subsector_as_supplied=sub, screening_category_as_supplied=cat,
            round_source_url=r['valuation_source_url'].split(' | ')[0],
            revenue_source_url=r['revenue_source_url'].split(' | ')[0],
            transaction_type='PRIMARY', verification='SHEET_02SEP',
            denominator_basis=basis_txt,
        )

        reasons = []
        if metric in VOLUME:
            row.update(volume_metric=metric, volume_musd=val, volume_period=basis_txt,
                       volume_basis=metric, ev_volume_x=mult, revenue_basis='NONE',
                       revenue_metric='', revenue_musd='', ev_revenue_x='')
            reasons.append('Volume metric only (%s). No revenue multiple exists for this row.' % metric)
        elif metric == 'PAID_SUBSCRIBERS':
            row.update(paying_users_k='%.1f' % (float(val) * 1000), revenue_basis='NONE',
                       volume_metric=metric, volume_musd=val, volume_period=basis_txt)
            reasons.append('Paying-subscriber count, in millions, not a revenue figure. '
                           'Recorded as %s000k paying users.' % val)
        else:
            row.update(revenue_metric=basis_txt, revenue_musd='%.3f' % float(val),
                       revenue_status='Disclosed', ev_revenue_x=mult,
                       revenue_basis=basis_of(metric, basis_txt),
                       revenue_period=period_of(metric, basis_txt))
            if '>' in basis_txt or 'threshold' in basis_txt.lower():
                row['bound'] = '<='
                reasons.append('Denominator is a threshold, so the multiple is a ceiling.')

        if c in BANKS:
            reasons.append('Deposit-taking bank or neobank. Standing rule: these price on book, '
                           'never on EV/revenue. The revenue multiple is recorded but held out of '
                           'the medians until a book figure exists.')
        if (c, d) in HOLD:
            reasons.append(HOLD[(c, d)])

        row['in_medians'] = '0' if reasons else '1'
        if row['in_medians'] == '0':
            held += 1
        row['notes'] = ('LOADED 02-Sep-2026 from Daniil\'s 191-row sheet, '
                        'data/raw/2026-09-01_private-transactions-daniil.csv. Figures, basis and '
                        'both URLs are his; category, bound and median flag are ours. Not yet '
                        'source-verified line by line, hence verification SHEET_02SEP. '
                        + ' '.join(reasons))
        new.append(row)

    allrows = existing + new
    allrows.sort(key=lambda r: r['date_iso'], reverse=True)

    head = ''.join(l for l in open(DST).read().splitlines(True) if l.startswith('#'))
    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=cols, lineterminator='\n')
    w.writeheader()
    w.writerows(allrows)
    open(DST, 'w').write(head + out.getvalue())
    print('loaded %d rows (%d in medians, %d held out); file now %d rows'
          % (len(new), len(new) - held, held, len(allrows)))


if __name__ == '__main__':
    main()
