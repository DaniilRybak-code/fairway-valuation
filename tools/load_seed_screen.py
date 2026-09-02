#!/usr/bin/env python3
"""
Loads Daniil's Active Seed & Series A Investor Screen into the CALLABLE layer of
data/investors.csv. Imported by tools/build_investors_table.py; not run on its own.

Source: data/raw/2026-09-02_seed-investor-screen.csv, 88 deal rows, 25 funds, 8 sectors,
transcribed from three photographs of the workbook.

WHY THIS SUPERSEDES THE data-content.js SEED for any fund in both. The screen's gate is stricter
than ours: "Funds lacking a bounded, fund-stated initial-cheque range or two eligible
announcements were excluded." A fund-stated cheque range is exactly what our own promoted growth
houses cannot supply. Where a fund appears in both sources, the screen's numbers win because they
carry a stated range and two dated, sourced deals; the curated note is kept as a second thesis
line only if it adds something.

THE ONE THING A CARD MUST NOT IMPLY. The screen's own Read Me says "two latest attributable
announcements per included fund" and "sector lists are non-exclusive". So the two deals are per
FUND, not per sector: Seedcamp appears in six sectors carrying Embedd and EverSettled in all six.
A deal proves the fund is ACTIVE. It does not prove the sector claim beside it, which comes from
the fund's stated thesis. `deal_evidences_sector` below is 0 for every row for that reason, and
the renderer must not say "recently backed a company like yours" on the strength of it.
"""
import csv, io, os, re

SRC = 'data/raw/2026-09-02_seed-investor-screen.csv'

# The screen's eight sectors, mapped onto the categories our own files actually use, so the
# matcher can join on them. Checked against the values present in private-rounds*.csv rather
# than invented.
SECTOR_TO_CATEGORY = {
    'B2B software and AI tooling':
        'Enterprise Applications; Data, AI & Developer Tools; Vertical Software; Cloud & Infrastructure Software',
    'Payments and fintech infrastructure':
        'Merchant Acquiring & PSP; Commerce & Payments Software; Cross-Border & FX',
    'Digital banking and lending':
        'Digital Bank & Deposits; Lending & Credit',
    'Marketplaces':
        'Consumer Marketplace; Third-Party Marketplace; B2B Marketplace; Freelance & Services Marketplace',
    'Consumer brands and D2C':
        'D2C / Consumer Brand; Consumer Brand; Owned-Inventory Retail',
    'Delivery logistics and supply chain':
        'Local Delivery & On-Demand; Commerce Enablement & Fulfilment; E-commerce Enablement',
    'Healthcare and digital health':
        'Healthcare',
    'Insurance':
        'Insurance',
}


def _stage_from_cheque(low, high):
    """The screen spans a hundredfold. Playfair starts at 100k, Dawn at 10m. Band on the LOW
    end, because the low end is what tells a founder whether the first cheque could be theirs."""
    if low is None:
        return ''
    if low < 500_000:
        return 'Pre-seed; Seed'
    if low < 1_500_000:
        return 'Seed; Series A'
    if low < 5_000_000:
        return 'Series A'
    return 'Series A; Series B'


def load(path=SRC):
    """Returns {fund_key: row-dict ready for investors.csv}, or {} if the file is not there."""
    if not os.path.exists(path):
        return {}
    lines = [l for l in open(path) if not l.startswith('#')]
    deals = list(csv.DictReader(io.StringIO(''.join(lines))))

    def num(x):
        try:
            return float(x)
        except (TypeError, ValueError):
            return None

    MONTHS = {m: i for i, m in enumerate(
        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], 1)}

    def iso(my):
        m = re.match(r'^([A-Za-z]{3})-(\d{4})$', (my or '').strip())
        return '%s-%02d' % (m.group(2), MONTHS[m.group(1).title()]) if m else ''

    funds = {}
    for d in deals:
        f = funds.setdefault(d['fund'], dict(
            name=d['fund'], regions=set(), sectors=[], theses=set(), deals={}, index_src=0,
            low=num(d['cheque_low']), high=num(d['cheque_high']), ccy=d['currency']))
        f['regions'].add(d['region'])
        if d['sector'] not in f['sectors']:
            f['sectors'].append(d['sector'])
        f['theses'].add(d['thesis'])
        # keyed on company so the same deal repeated across sectors collapses to one
        f['deals'][d['company']] = (iso(d['month_year']), d['company'], d['source_url'])
        if d['source_is_index'] == '1':
            f['index_src'] += 1

    out = {}
    for name, f in funds.items():
        ds = sorted(f['deals'].values(), reverse=True)
        cats = []
        for s in f['sectors']:
            for c in SECTOR_TO_CATEGORY.get(s, '').split(';'):
                c = c.strip()
                if c and c not in cats:
                    cats.append(c)
        thesis = sorted(f['theses'], key=len, reverse=True)[0]
        region = sorted(f['regions'], key=len, reverse=True)[0]
        out[name] = dict(
            investor_name=name, house_type='Venture', layer='CALLABLE',
            geographies=region,
            stage_bands=_stage_from_cheque(f['low'], f['high']),
            first_cheque_low_m=round(f['low'] / 1e6, 3) if f['low'] else '',
            first_cheque_high_m=round(f['high'] / 1e6, 3) if f['high'] else '',
            cheque_currency=f['ccy'],
            round_size_low_m='', round_size_high_m='',
            thesis_one_liner=thesis,
            screening_categories='; '.join(cats),
            subsectors='; '.join(f['sectors']),
            recent_deal_1_company=ds[0][1] if ds else '',
            recent_deal_1_date=ds[0][0] if ds else '',
            recent_deal_1_source_url=ds[0][2] if ds else '',
            recent_deal_2_company=ds[1][1] if len(ds) > 1 else '',
            recent_deal_2_date=ds[1][0] if len(ds) > 1 else '',
            recent_deal_2_source_url=ds[1][2] if len(ds) > 1 else '',
            rounds_in_set=0, companies_in_set=0, companies_backed='',
            first_round='', last_round=ds[0][0] if ds else '',
            median_round_size_m='', last_verified='2026-09-02',
            deal_evidences_sector='0',
            provenance=('SEED SCREEN, data/raw/2026-09-02_seed-investor-screen.csv. Cheque range '
                        'is fund-stated. Deals are the fund\'s two latest overall, not sector '
                        'specific'
                        + ('; %d of its deal links point at an index page rather than the '
                           'announcement' % f['index_src'] if f['index_src'] else '') + '.'),
        )
    return out
