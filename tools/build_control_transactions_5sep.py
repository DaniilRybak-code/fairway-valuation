#!/usr/bin/env python3
"""
Builds data/raw/2026-09-05_control-transactions-claude.csv and its tag file: the three take-privates
Daniil listed on 5-Sep-2026 that were not yet in the file (Confluent, Verint, Learning Technologies
Group). Sapiens, Accolade and Udemy from the same list were loaded earlier the same evening from
data/raw/2026-09-05_private-rounds-claude.csv.

Every figure was read on the URL in its row on 5-Sep-2026: the deal terms from the target's own
release as filed (8-K, or the RNS on Investegate for LTG), the denominator built as LTM from the
target's last filed full year and the year-to-date periods either side, all three components quoted.
FX at the ECB reference rate on the announcement date. Rulebook B6: a control deal prices and carries
its label; the engine marks CONTROL rows as anchors and never lets them feed a range.

    python3 tools/build_control_transactions_5sep.py
"""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(HERE))

def header_of(path):
    for line in open(path, encoding='utf-8'):
        if not line.startswith('#'):
            return next(csv.reader([line.rstrip('\n')]))

ROUND_HDR = header_of('data/private-rounds.csv')
TAG_HDR = header_of('data/private-companies-tags.csv')
VER = 'CLAUDE_PULL_05SEP'
PULLED = 'Sourced and verified by Claude 05-Sep-2026 against the URL in this row, on Daniil\'s list of six control transactions. '
GBPUSD_2024_12_04 = 1.2667   # ECB reference rate, api.frankfurter.dev, read 5-Sep-2026

def r2(x): return round(x, 2)
rows, tags = [], []

def add(**k):
    row = {c: '' for c in ROUND_HDR}
    for kk, v in k.items():
        if kk not in row: raise SystemExit('unknown column %s' % kk)
        row[kk] = v
    calc = float(row['post_money_musd']) / float(row['revenue_musd'])
    assert abs(calc - float(row['ev_revenue_x'])) / calc < 0.02, (row['transaction_id'], calc)
    rows.append(row)

def tag(**k):
    row = {c: '' for c in TAG_HDR}
    for kk, v in k.items():
        if kk not in row: raise SystemExit('unknown tag column %s' % kk)
        row[kk] = v
    tags.append(row)

TAGNOTE = 'Tagged 05-Sep-2026 by Claude on sourcing the row. Archetype assigned on how the company earns money. M&A control-transaction row of a formerly listed company.'

# Confluent: LTM to 30-Sep-2025 = FY2024 963.642 + 9M-2025 851.929 - 9M-2024 702.422
cf_ltm = 963.642 + 851.929 - 702.422
add(transaction_id='confluent-2025-12', company_key='confluent', company_name='Confluent', date='Dec-25', date_iso='2025-12',
    round_type='Acquisition by IBM', capital_raised_musd='', post_money_musd='11000.0', valuation_status='Disclosed (enterprise value)',
    revenue_metric='Total revenue, LTM to 30-Sep-2025 (GAAP, filed)', revenue_musd=str(r2(cf_ltm)), revenue_status='Disclosed (SEC filings, 8-K)',
    ev_revenue_x=str(r2(11000/cf_ltm)), subsector_as_supplied='Data streaming platform (Apache Kafka), sold to developers on consumption',
    screening_category_as_supplied='Data, AI & Developer Tools',
    lead_key_investors='IBM (acquirer)',
    round_source_url='https://www.sec.gov/Archives/edgar/data/1699838/000110465925119081/tm2532777d2_ex99-1.htm',
    revenue_source_url='https://www.sec.gov/Archives/edgar/data/1699838/000169983825000011/cflt-20250930xexx991.htm',
    notes=PULLED + "CONTROL, TARGET WAS LISTED (Nasdaq: CFLT). Joint release of 8-Dec-2025, filed on Form 8-K: IBM to acquire Confluent for '$31 per share' in cash, 'representing an enterprise value of $11 billion'. Completed 17-Mar-2026 (Daniil, 5-Sep). No revenue in the deal release. DENOMINATOR IS LTM BUILT FROM THREE FILED FIGURES: FY2024 total revenue $963.642m (Q4-2024 release, 8-K of 11-Feb-2025, https://www.sec.gov/Archives/edgar/data/1699838/000095017025017884/cflt-ex99_1.htm, income statement in thousands: 963,642) plus nine months to 30-Sep-2025 $851.929m less nine months to 30-Sep-2024 $702.422m (Q3-2025 release, 8-K of 27-Oct-2025, the revenue URL: 851,929 and 702,422) = $1,113.1m. Growth 19% is the Q3-2025 year-on-year rate stated in that release; the nine-month rate is 21.3% by arithmetic and FY2024 was 24%. Valuation is ENTERPRISE value, so this is a true EV/revenue. Names the projectx, osseus and orchids lanes in the work order; a control premium travels with the row (B6).",
    transaction_type='CONTROL', denominator_basis='DISCLOSED_ACTUAL', bound='', in_medians='1', verification=VER,
    growth_band='MATURE', growth_pct_at_round='19', growth_band_basis='DISCLOSED', target_was_listed='1',
    revenue_basis='NET_REVENUE', revenue_period='LTM', valuation_basis='REVENUE',
    revenue_basis_source='STATED', basis_risk_note='GAAP subscription plus services revenue; net by construction. Valuation is EV.', valuation_pre_or_post='UNSPECIFIED')

# Verint: LTM to 31-Jul-2025 = FY2025 (to 31-Jan-2025) 909.186 + H1 FY26 416.104 - H1 FY25 431.447
vr_ltm = 909.186 + 416.104 - 431.447
add(transaction_id='verint-2025-08', company_key='verint', company_name='Verint Systems', date='Aug-25', date_iso='2025-08',
    round_type='Take-private (Thoma Bravo, merging with Calabrio)', capital_raised_musd='', post_money_musd='2000.0', valuation_status='Disclosed (enterprise value)',
    revenue_metric='Total revenue, LTM to 31-Jul-2025 (GAAP, filed)', revenue_musd=str(r2(vr_ltm)), revenue_status='Disclosed (SEC filings, 8-K)',
    ev_revenue_x=str(r2(2000/vr_ltm)), subsector_as_supplied='Customer-engagement and conversation analytics software (CX automation)',
    screening_category_as_supplied='Communications & Collaboration',
    lead_key_investors='Thoma Bravo (acquirer, via portfolio company Calabrio)',
    round_source_url='https://www.sec.gov/Archives/edgar/data/1166388/000119312525187836/d20307dex991.htm',
    revenue_source_url='https://www.sec.gov/Archives/edgar/data/1166388/000116638825000116/july312025earningsreleasee.htm',
    notes=PULLED + "CONTROL, TARGET WAS LISTED (Nasdaq: VRNT). Verint release of 25-Aug-2025, filed on Form 8-K: 'Verint common shareholders will receive $20.50 per share in cash' in 'an all-cash transaction reflecting an enterprise value of $2 billion'; Verint to merge with Thoma Bravo's Calabrio. No revenue figure in the deal release. DENOMINATOR IS LTM BUILT FROM THREE FILED FIGURES: FY2025 (year to 31-Jan-2025) total revenue $909.186m (Q4 FY2025 release, 8-K of 26-Mar-2025, https://www.sec.gov/Archives/edgar/data/1166388/000116638825000011/january312025earningsrelea.htm) plus six months to 31-Jul-2025 $416.104m less six months to 31-Jul-2024 $431.447m (Q2 FY2026 release, 8-K of 2-Sep-2025, the revenue URL, income statement in thousands) = $893.8m. The Q2 period closed before the deal and was published eight days after it. Growth -0.1% is FY2025 against FY2024 ($910.387m), arithmetic on the stated figures; revenue is flat to declining. Valuation is ENTERPRISE value. Names the wispr-flow, dograh and akkari lanes in the work order as the enterprise voice-analytics anchor; a control premium travels with the row (B6).",
    transaction_type='CONTROL', denominator_basis='DISCLOSED_ACTUAL', bound='', in_medians='1', verification=VER,
    growth_band='MATURE', growth_pct_at_round='-0.1', growth_band_basis='DERIVED', target_was_listed='1',
    revenue_basis='NET_REVENUE', revenue_period='LTM', valuation_basis='REVENUE',
    revenue_basis_source='STATED', basis_risk_note='GAAP recurring plus non-recurring revenue; net by construction. Valuation is EV.', valuation_pre_or_post='UNSPECIFIED')

# LTG: equity GBP 802.4m fully diluted; LTM to 30-Jun-2024 = FY2023 562.3 + H1-2024 250.3 - H1-2023 284.6
ltg_ltm_gbp = 562.3 + 250.3 - 284.6
ltg_eq_usd = 802.4 * GBPUSD_2024_12_04
ltg_ltm_usd = ltg_ltm_gbp * GBPUSD_2024_12_04
add(transaction_id='learning-technologies-group-2024-12', company_key='learning-technologies-group', company_name='Learning Technologies Group', date='Dec-24', date_iso='2024-12',
    round_type='Recommended cash acquisition (General Atlantic, Leopard UK Bidco)', capital_raised_musd='', post_money_musd=str(r2(ltg_eq_usd)), valuation_status='Disclosed (equity value, fully diluted, "approximately")',
    revenue_metric='Revenue, LTM to 30-Jun-2024 (IFRS, reported)', revenue_musd=str(r2(ltg_ltm_usd)), revenue_status='Disclosed (annual report and half-year results)',
    ev_revenue_x=str(r2(ltg_eq_usd/ltg_ltm_usd)), subsector_as_supplied='Corporate learning platforms and services (Open LMS, Bridge, GP Strategies)',
    screening_category_as_supplied='Online Learning',
    lead_key_investors='General Atlantic (through Leopard UK Bidco Limited)',
    round_source_url='https://www.investegate.co.uk/announcement/rns/learning-technologies-group--ltg/offer-for-learning-technologies-group-plc/8589841',
    revenue_source_url='https://ltgplc.com/news/half-year-results-2024/',
    notes=PULLED + "CONTROL, TARGET WAS LISTED (AIM: LTG). Rule 2.7 announcement of 4-Dec-2024 (RNS, read on Investegate): 'for each LTG Share: 100 pence in cash'; 'The Cash Offer values the entire issued, and to be issued, ordinary share capital of LTG at approximately GBP802.4 million on a fully diluted basis'; 'an implied enterprise value multiple of 9.4 times LTG's Adjusted EBIT of GBP88.7 million for the full year ended 31 December 2023'. Bidder Leopard UK Bidco Limited, owned by funds managed by General Atlantic. Court sanction 24-Mar-2025, scheme effective 31-Mar-2025 (Investegate). DENOMINATOR IS LTM BUILT FROM THREE REPORTED FIGURES: FY2023 revenue GBP562.3m (Annual Report 2023, https://ltgplc.com/wp-content/uploads/2024/04/LTG_Annual_Report_2023_Digital_pages.pdf: 'Revenue of GBP562.3 million') plus six months to 30-Jun-2024 GBP250.3m less six months to 30-Jun-2023 GBP284.6m (Half Year Results 2024, 19-Sep-2024, the revenue URL) = GBP528.0m, the last closed period before the offer. Converted at the ECB reference rate of 4-Dec-2024, 1.2667 USD/GBP; the multiple is currency-free. Growth -4.5% is FY2023 against FY2022 (GBP588.6m) by arithmetic on the annual report; H1-2024 was down 12% on H1-2023. Equity value, not EV (LTG carried net debt). Names the honen and bloomy lanes in the work order; a control premium travels with the row (B6).",
    transaction_type='CONTROL', denominator_basis='DISCLOSED_ACTUAL', bound='', in_medians='1', verification=VER,
    growth_band='MATURE', growth_pct_at_round='-4.5', growth_band_basis='DERIVED', target_was_listed='1',
    revenue_basis='NET_REVENUE', revenue_period='LTM', fx_ccy='GBP', fx_rate=str(GBPUSD_2024_12_04), fx_date='2024-12-04', valuation_basis='REVENUE',
    revenue_basis_source='STATED', basis_risk_note='IFRS revenue of a learning platform and services group; net by construction. Equity value, not EV.', valuation_pre_or_post='UNSPECIFIED')

tag(company_key='confluent', company_name='Confluent', archetype='Data, AI & Developer Tools', archetype_secondary='Cloud & Infrastructure', industry='Horizontal',
    function='IT & Integration', buyer='DEV', gtm_motion='PLG', revenue_model='CONSUMPTION', product_role='INFRA_LAYER', ai_stance='AI_EMBEDDED',
    product_tags='Data Streaming|Apache Kafka|Event Streaming|Cloud Execution Environment|Consumption Pricing|Developer Infrastructure|Real Time Data|Stream Processing',
    tags_as_of='2025-12', status_today='Acquired by IBM, completed 17-Mar-2026; CFLT delisted.', screening_category_as_supplied='Data, AI & Developer Tools', taxonomy_note=TAGNOTE,
    what_it_does='runs the managed data-streaming platform built on Apache Kafka that developers pay for by consumption, plus a self-managed licence')
tag(company_key='verint', company_name='Verint Systems', archetype='Communications & Collaboration', archetype_secondary='Marketing & Customer Engagement', industry='Horizontal',
    function='Customer Service', buyer='ENTERPRISE', gtm_motion='ENT_SALES', revenue_model='SEATS', product_role='PLATFORM_SUITE', ai_stance='AI_EMBEDDED',
    product_tags='Speech To Text|Conversation Analytics|Contact Centre Software|Voice Analytics|Workforce Engagement|CX Automation|AI Bots|Call Recording',
    tags_as_of='2025-08', status_today='Taken private by Thoma Bravo and merged with Calabrio; VRNT delisted.', screening_category_as_supplied='Communications & Collaboration', taxonomy_note=TAGNOTE + ' The enterprise anchor for voice and conversation analytics; named in the ticker request as the wispr-flow boundary.',
    what_it_does='sells contact-centre and conversation-analytics software to large enterprises on subscription, recording and analysing customer voice and text')
tag(company_key='learning-technologies-group', company_name='Learning Technologies Group', archetype='Online Learning', archetype_secondary='Business Applications', industry='Education',
    function='HR & Workforce', buyer='ENTERPRISE', gtm_motion='ENT_SALES', revenue_model='PLATFORM', product_role='PLATFORM_SUITE', ai_stance='AI_NEUTRAL',
    product_tags='Corporate Learning|Learning Management System|LMS|Workforce Development|Learning Content|Training Services|Talent Management|Compliance Training',
    tags_as_of='2024-12', status_today='Acquired by General Atlantic, scheme effective 31-Mar-2025; delisted from AIM.', screening_category_as_supplied='Online Learning', taxonomy_note=TAGNOTE + ' Corporate learning sold to employers, with a large services arm (GP Strategies), so PLATFORM rather than SEATS.',
    what_it_does='sells learning platforms, content and training services to employers, earning subscriptions on the platforms and fees on the services')

out = 'data/raw/2026-09-05_control-transactions-claude.csv'
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=ROUND_HDR, lineterminator='\n'); w.writeheader(); w.writerows(rows)
out2 = 'data/raw/2026-09-05_control-transactions-tags-claude.csv'
with open(out2, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=TAG_HDR, lineterminator='\n'); w.writeheader(); w.writerows(tags)
print('%d control rows, %d tag rows -> %s, %s' % (len(rows), len(tags), out, out2))
for r in rows:
    print('  %-38s post %9s rev %8s x %5s' % (r['transaction_id'], r['post_money_musd'], r['revenue_musd'], r['ev_revenue_x']))
