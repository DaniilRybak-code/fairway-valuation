#!/usr/bin/env python3
"""
THE ROW-ACCOUNTING CHECK. Run it after every load, and before every commit.

    python3 tools/check_raw_coverage.py          exits 1 if any supplied row is unaccounted for

WHY IT EXISTS. Daniil spends hours building a sheet and sending it through as photographs. Twice
now his work has been silently lost after arriving safely:

  02-Sep-2026  the loader deduplicated on COMPANY rather than on company AND round, so six rounds
               belonging to companies we already held were skipped without a word
  01/02-Sep    two screenshot batches carried source URLs in columns AA and AB and the target
               schema had no field for them, so they landed nowhere and nothing counted their
               absence

Durability rule 11 fixed the second by requiring the schema to carry every column. This tool fixes
the first, and it is the general answer: **EVERY ROW HE SUPPLIES MUST BE ACCOUNTED FOR BY NAME,
either loaded or listed in EXCLUSIONS below with a written reason.** Silence is not an outcome.

The check is deliberately dumb. It matches on company plus year-month, never on company alone,
because company-alone matching is the exact bug it was written to catch.

HOW TO ADD A NEW SUPPLIED FILE. Add one entry to SOURCES. If a row genuinely should not be loaded,
add it to EXCLUSIONS with a reason a stranger could audit. Never make this pass by deleting a row
from a raw file: raw files are the record of what Daniil sent and are append-only.
"""
import csv, io, os, re, sys

# supplied file -> (company column, date column, the loaded files it may land in)
SOURCES = {
    'data/raw/2026-09-01_private-transactions-daniil.csv': (
        'company', 'txn_date',
        ['data/private-rounds.csv', 'data/private-rounds-consumer.csv']),
    'data/raw/2026-09-02_sector-screen-fixed.csv': (
        'company_name', 'transaction_date',
        ['data/private-rounds.csv', 'data/private-rounds-consumer.csv']),
    'data/raw/2026-09-03_lending-screen-v2.csv': (
        'company_name', 'transaction_date',
        ['data/private-rounds.csv', 'data/private-rounds-consumer.csv']),
}

# (supplied file, company, YYYY-MM) -> the reason it is not loaded. Auditable, or it does not count.
EXCLUSIONS = {
    ('data/raw/2026-09-01_private-transactions-daniil.csv', 'Figma', '2024-05'):
        'Same round as our Figma Jul-24 row, same Axios URL. We re-dated it from tender LAUNCH to '
        'tender CLOSE, which is the honest date for a tender. Same $12.5bn, $700m ARR, 17.9x.',
    ('data/raw/2026-09-01_private-transactions-daniil.csv', 'Canva', '2024-05'):
        'Same round as our Canva Apr-24 row, same Forbes URL. The $26bn secondary completed in '
        'early April 2024 and there is no May-2024 Canva share sale. Priced 02-Sep-2026 on Daniil\'s '
        'ruling off Canva\'s own published figure of more than US$2.2bn annualised revenue.',
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Ninjacart', '2021-12'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Vegrow', '2023-12'):
        "HELD. The revenue source is gokulnk.com, personal research notes. Its author does appear to work at Vegrow, but the page makes no claim of authority, gives 'Gross Revenue 100 cr and 361 cr' with NO year attached, and cites thekredible for its figures. The sheet assigns the 361 cr to FY ended 31-Mar-2023 on no stated basis. Inc42 has FY24 at Rs 407.9 crore but no FY23. Needs a dated FY2023 source before it prices anything.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'ElasticRun', '2022-02'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'DeHaat', '2022-10'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'eFishery', '2023-07'):
        'Not loaded. Reported figures were later found to be fabricated; the sheet marks it excluded with no usable denominator.',
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'WayCool Foods', '2022-06'):
        'CLEARED on ruling 1. Denominator INR 9,306m is total revenue including interest and other operating income; operating revenue was INR 926.9 crore. The multiple is 5.9x either way. Load with revenue_basis = TOTAL_INCOME and a note.',
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Octopus Energy Group', '2021-12'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Octopus Energy Group', '2023-12'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Fuse Energy', '2025-12'):
        'Not loaded. No public valuation: the cited sources do not state one, so there is no numerator. NOT FOUND, not an estimate.',
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Octopus Energy Group', '2022-07'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Octopus Energy Group', '2021-09'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Octopus Energy Group', '2024-05'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Enpal', '2023-01'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Blockworks', '2023-05'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'BlockFi', '2021-03'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Celsius Network', '2021-10'):
        'Not loaded. Bankruptcy and fraud findings; the sheet calculates the 25.8x but marks the row excluded.',
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'MoonPay', '2021-11'):
        'CLEARED TO LOAD, but this round is ALREADY in private-rounds.csv at 3,400 over 150 = 22.67x. Do not double-load. The sector screen is right that the $150m is an eleven-month year-to-date figure at Nov-2021; the engine currently calls it revenue_period = LTM, which is wrong and should be corrected there.',
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Fireblocks', '2022-01'):
        "NOT LOADED. The sector screen's $50m denominator is the ARR at the JULY 2021 Series D, which already prices its own row in private-rounds.csv at 2,000 over 50 = 40.0x. Applying it to the Jan-2022 Series E gives 160.0x, double the truth; the engine's 8,000 over 100 ARR = 80.0x stands. The sheet's own basis cell says 'Prior year / FY2021', which is the admission.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'ConsenSys', '2022-03'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Thirty Madison', '2021-06'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Cityblock Health', '2021-09'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Alan', '2022-05'):
        "PARTLY LOADED. The Sep-2024 round is already in private-rounds.csv and was CORRECTED on 02-Sep-2026 to USD 500m ARR (9.00x) on this sheet's evidence. The May-2022 and Jun-2026 Alan rounds are cleared to load and are not duplicates.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Devoted Health', '2021-10'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Doctolib', '2022-03'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Virta Health', '2021-04'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Aledade', '2023-06'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Ro', '2021-03'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'upGrad', '2021-08'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'LEAD School', '2022-01'):
        'CLEARED on ruling 1. Denominator INR 600m is total income; entrackr reads operating revenue of Rs 57.1 crore from the RoC filings. The cited Forbes India source returns 403 and could not be checked. Load with revenue_basis = TOTAL_INCOME, a note, and 135.3x. Highest multiple in the set; treat as an outlier.',
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'MasterClass', '2021-05'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Vedantu', '2021-09'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'BetterUp', '2021-10'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Guild Education', '2022-06'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'EGYM', '2023-07'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Restore Hyper Wellness', '2021-12'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Oura', '2024-12'):
        "CLEARED on ruling 3, with a user-facing note. The $225m denominator rests on Sacra alone, which is tier 4, and the cited TechCrunch article carries no revenue figure. Load with source_tier 4 and an honesty note. The sheet's denominator_basis says FY2024 expected while its metric period says FY2023 estimate; FY2023 is the correct label, since the ~$500m forward figure sits in forward_metric.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Athletic Greens (AG1)', '2022-01'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Noom', '2021-05'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'wefox', '2022-07'):
        "NOT LOADED. The Jul-2022 round is already in private-rounds.csv at 4,500 over 320 FY2021 = 14.06x, which the TechCrunch source supports and which matches the basis used by this sheet's own wefox Series C row. The sheet's $200m four-month stub is the weaker basis. The May-2021 Series C row is a separate round and is cleared to load.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'The Zebra', '2021-04'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Alan', '2024-09'):
        "PARTLY LOADED. The Sep-2024 round is already in private-rounds.csv and was CORRECTED on 02-Sep-2026 to USD 500m ARR (9.00x) on this sheet's evidence. The May-2022 and Jun-2026 Alan rounds are cleared to load and are not duplicates.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Alan', '2026-06'):
        "PARTLY LOADED. The Sep-2024 round is already in private-rounds.csv and was CORRECTED on 02-Sep-2026 to USD 500m ARR (9.00x) on this sheet's evidence. The May-2022 and Jun-2026 Alan rounds are cleared to load and are not duplicates.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'wefox', '2021-05'):
        "NOT LOADED. The Jul-2022 round is already in private-rounds.csv at 4,500 over 320 FY2021 = 14.06x, which the TechCrunch source supports and which matches the basis used by this sheet's own wefox Series C row. The sheet's $200m four-month stub is the weaker basis. The May-2021 Series C row is a separate round and is cleared to load.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Roblox', '2021-01'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Epic Games', '2021-04'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Voodoo', '2021-08'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Discord', '2021-09'):
        "CLEARED, and NOT dropped. Daniil's instruction to drop was conditional on there being no matching denominator. There is one. The round priced Sep-2021, so the last completed year at pricing is FY2020 and $130m is the right figure, confirmed against multiple sources. The $310m FY2021 number is a LATER ACTUAL, which his own reconciliation principle forbids. Load at 115.4x with the basis label corrected from FY2021 to FY2020.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Epic Games', '2022-04'):
        "CLEARED TO LOAD on Daniil's ruling of 02-Sep-2026. Transcribed and arithmetically verified from his screenshots. Remove this entry when the row lands in private-rounds.csv.",
    ('data/raw/2026-09-02_sector-screen-fixed.csv', 'Dream Sports', '2021-11'):
        'CLEARED on ruling 1 (use whatever is available, with the note). Denominator INR 27,060m is TOTAL INCOME (Rs 2,705.56 crore); revenue from operations was Rs 2,551.59 crore. Load with revenue_basis = TOTAL_INCOME and a note, giving 22.1x. On revenue from operations it would be 23.4x.',
    ('data/raw/2026-09-03_lending-screen-v2.csv', 'Konfio', '2021-09'):
        'CLEARED TO LOAD as a revenue or ARR multiple. One of only 7 rows in this sheet with a periodic revenue denominator. See docs/lending-screen-verdicts-2sep.md.',
    ('data/raw/2026-09-03_lending-screen-v2.csv', 'Creditas', '2022-01'):
        "ALREADY LOADED at 4,800 over 200 = 24.00x. Agrees exactly. This sheet labels the denominator REVENUE where the engine says ARR_RUNRATE; the sheet's own basis text ('annualised revenue as described by CEO, not audited FY revenue') supports ARR_RUNRATE. No change needed.",
    ('data/raw/2026-09-03_lending-screen-v2.csv', 'Tabby', '2025-02'):
        'NOT LOADED AS A REVENUE MULTIPLE. The denominator is a cumulative-since-inception volume figure, so valuation over it compares a point-in-time price to everything the company has ever done. It falls as the company ages and is not a multiple. Volume overlay or nothing. See the verdicts doc.',
    ('data/raw/2026-09-03_lending-screen-v2.csv', 'Tabby', '2023-11'):
        'NOT LOADED. Annualised transaction volume, not revenue, and the implied-multiple cell could not be read from the screenshot. Confirm the cell before anything else.',
    ('data/raw/2026-09-03_lending-screen-v2.csv', 'MNT-Halan', '2023-02'):
        "NOT LOADED. Cumulative loans disbursed over a floor valuation, and the implied-multiple cell could not be read. Floor over floor, which the sheet's own header says it marks NM.",
    ('data/raw/2026-09-03_lending-screen-v2.csv', 'Klarna', '2022-07'):
        'ALREADY LOADED. In private-rounds.csv at 6,700 over 1,303.7 BANK_NOI = 5.1x. This sheet says 1,600 for the same FY2021 net operating income; the gap is the SEK/USD rate, not the basis. Settle the FX date, do not load a second row.',
    ('data/raw/2026-09-03_lending-screen-v2.csv', 'Atom Bank', '2022-02'):
        'NOT LOADED AS A REVENUE MULTIPLE. The denominator is a cumulative-since-inception volume figure, so valuation over it compares a point-in-time price to everything the company has ever done. It falls as the company ages and is not a multiple. Volume overlay or nothing. See the verdicts doc.',
    ('data/raw/2026-09-03_lending-screen-v2.csv', 'Wayflyer', '2022-02'):
        'CLEARED TO LOAD as an ORIGINATIONS multiple. The engine holds this round at a 1,600 post-money with no denominator and out of the medians. FY2021 originations of 500 prices it at 3.20x. Not a revenue multiple; label it as originations.',
    ('data/raw/2026-09-03_lending-screen-v2.csv', 'Monzo Bank', '2021-12'):
        'CLEARED TO LOAD as a revenue or ARR multiple. One of only 7 rows in this sheet with a periodic revenue denominator. See docs/lending-screen-verdicts-2sep.md.',
    ('data/raw/2026-09-03_lending-screen-v2.csv', 'Fundbox', '2021-11'):
        'NOT LOADED. The engine already prices this round on 100 ARR at 11.00x. This sheet adds a cumulative transaction-volume figure, which is a different metric and not a conflict.',
    ('data/raw/2026-09-03_lending-screen-v2.csv', 'Zilch', '2021-11'):
        'NOT LOADED. Cumulative sales since launch over a floor valuation. The implied-multiple cell could not be read; it computes to 14.9x, which would be badly misleading against a cumulative denominator.',
    ('data/raw/2026-09-03_lending-screen-v2.csv', 'Billie', '2021-10'):
        'NOT LOADED AS A REVENUE MULTIPLE. The denominator is a cumulative-since-inception volume figure, so valuation over it compares a point-in-time price to everything the company has ever done. It falls as the company ages and is not a multiple. Volume overlay or nothing. See the verdicts doc.',
    ('data/raw/2026-09-03_lending-screen-v2.csv', 'Klarna', '2021-06'):
        'ALREADY LOADED at 45,600 over 1,212.1 BANK_NOI = 37.6x. This sheet labels the same figure FULL-YEAR REVENUE at 1,000. The label is wrong, it is net operating income, and the value gap is the SEK/USD rate. Do not load a second row.',
    ('data/raw/2026-09-03_lending-screen-v2.csv', 'Pipe', '2021-05'):
        'NOT LOADED AS A REVENUE MULTIPLE. The denominator is a cumulative-since-inception volume figure, so valuation over it compares a point-in-time price to everything the company has ever done. It falls as the company ages and is not a multiple. Volume overlay or nothing. See the verdicts doc.',
    ('data/raw/2026-09-03_lending-screen-v2.csv', 'Clearco (then Clearbanc)', '2021-04'):
        'NOT LOADED AS A REVENUE MULTIPLE. The denominator is a cumulative-since-inception volume figure, so valuation over it compares a point-in-time price to everything the company has ever done. It falls as the company ages and is not a multiple. Volume overlay or nothing. See the verdicts doc.',
    ('data/raw/2026-09-03_lending-screen-v2.csv', 'Starling Bank', '2021-03'):
        'CLEARED TO LOAD, with a flag: the 7.59x is struck on a PRE-money valuation while the other six revenue multiples in this sheet are post-money. Not like for like, and it is the lowest of the seven.',
    ('data/raw/2026-09-03_lending-screen-v2.csv', 'Klarna', '2021-03'):
        'CLEARED TO LOAD, but as net operating income and not as the FULL-YEAR REVENUE this sheet labels it. Klarna has no revenue line, now confirmed from a second independent pull, which settles open decision 2.',
    ('data/raw/2026-09-03_lending-screen-v2.csv', 'Upgrade', '2021-11'):
        'NOT LOADED. This sheet carries 6,000 PRE-money; the engine already holds the round at a 6,280 post-money, which is the same number plus the raise. The engine is right. The denominator is cumulative credit delivered in any case.',
    ('data/raw/2026-09-03_lending-screen-v2.csv', 'Tala', '2021-10'):
        'NOT LOADED as a revenue multiple. Cumulative credit delivered since launch. The engine already holds this round unpriced; this does not price it on a revenue basis.',
    ('data/raw/2026-09-03_lending-screen-v2.csv', 'Upgrade', '2021-08'):
        'NOT LOADED. This sheet carries 3,325 PRE-money; the engine holds 3,430 post-money. Same round, engine correct. Cumulative denominator in any case.',
    ('data/raw/2026-09-03_lending-screen-v2.csv', 'Nubank', '2021-06'):
        'CLEARED TO LOAD as a revenue or ARR multiple. One of only 7 rows in this sheet with a periodic revenue denominator. See docs/lending-screen-verdicts-2sep.md.',
    ('data/raw/2026-09-03_lending-screen-v2.csv', 'Happy Money', '2022-02'):
        'NOT LOADED AS A REVENUE MULTIPLE. The denominator is a cumulative-since-inception volume figure, so valuation over it compares a point-in-time price to everything the company has ever done. It falls as the company ages and is not a multiple. Volume overlay or nothing. See the verdicts doc.',
}


def rows_of(path):
    lines = [l for l in open(path) if not l.startswith('#')]
    return list(csv.DictReader(io.StringIO(''.join(lines))))


def key(name):
    return re.sub(r'[^a-z0-9]', '', (name or '').lower())


_MON = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}


def ym(value):
    # The sheets arrive in three date shapes. All three must parse, or a row that IS
    # loaded looks unaccounted for and the check cries wolf until somebody stops reading it.
    v = (value or '').strip()
    m = re.match(r'^(\d{4})-(\d{2})', v)
    if m:
        return '%s-%s' % (m.group(1), m.group(2))
    m = re.match(r'^(\d{1,2})-([A-Za-z]{3})[a-z]*-(\d{4})$', v)
    if m:
        return '%s-%02d' % (m.group(3), _MON[m.group(2).lower()])
    m = re.match(r'^([A-Za-z]{3})[a-z]*-(\d{4})$', v)
    if m:
        return '%s-%02d' % (m.group(2), _MON[m.group(1).lower()])
    return ''


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    failures = 0

    for src, (ccol, dcol, targets) in SOURCES.items():
        if not os.path.exists(src):
            print('MISSING SUPPLIED FILE %s' % src)
            failures += 1
            continue
        supplied = rows_of(src)

        loaded = set()
        for t in targets:
            if not os.path.exists(t):
                continue
            for r in rows_of(t):
                loaded.add((key(r.get('company_name')), ym(r.get('date_iso'))))

        unaccounted = []
        excused = 0
        for r in supplied:
            k = (key(r[ccol]), ym(r[dcol]))
            if k in loaded:
                continue
            if (src, r[ccol], ym(r[dcol])) in EXCLUSIONS:
                excused += 1
                continue
            unaccounted.append(r)

        print('%s' % src)
        print('   supplied %d | loaded %d | excluded with a written reason %d | UNACCOUNTED %d'
              % (len(supplied), len(supplied) - len(unaccounted) - excused, excused,
                 len(unaccounted)))
        for r in unaccounted:
            print('   UNACCOUNTED  %-24s %s' % (r[ccol], r[dcol]))
        failures += len(unaccounted)

    print()
    if failures:
        print('FAIL: %d supplied rows are neither loaded nor excluded with a reason.' % failures)
        print('Load them, or add them to EXCLUSIONS in this file with a reason. Do not delete them '
              'from the raw file: raw files are the record of what was sent and are append-only.')
        sys.exit(1)
    print('PASS: every supplied row is accounted for.')


if __name__ == '__main__':
    main()
