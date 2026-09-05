#!/usr/bin/env python3
"""
Builds data/raw/2026-09-05_private-rounds-claude.csv and data/raw/2026-09-05_private-companies-tags-claude.csv
from the rows Claude sourced and verified on 5-Sep-2026 (work order docs/prompts/work-order-claude-4sep.md).

Every figure below was read on the page named in its URL column on 5-Sep-2026 and the sentence is
quoted in the notes. Nothing is estimated. FX at the ECB reference rate on the pricing date
(Frankfurter/ECB), the same convention as the Klarna restatement of 3-Sep. Multiples are computed
here from the two stated figures and re-checked by tools/check_all.sh's identity check on load.

    python3 tools/build_claude_pull_5sep.py
"""
import csv, io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
os.chdir(ROOT)

def header_of(path):
    for line in open(path, encoding='utf-8'):
        if not line.startswith('#'):
            return next(csv.reader([line.rstrip('\n')]))
    raise SystemExit('no header in ' + path)

ROUND_HDR = header_of('data/private-rounds.csv')
TAG_HDR = header_of('data/private-companies-tags.csv')

VER = 'CLAUDE_PULL_05SEP'
PULLED = 'Sourced and verified by Claude 05-Sep-2026 against the URL in this row (docs/prompts/work-order-claude-4sep.md). '

# ECB reference rates on the pricing date, read from api.frankfurter.dev (ECB) on 5-Sep-2026.
FX = {
    ('INR', '2025-03-31'): 85.44,   # USD/INR
    ('INR', '2025-02-05'): 87.37,
    ('INR', '2026-01-23'): 91.86,
    ('EUR', '2026-08-05'): 1.1554,  # USD per EUR
}

def r2(x): return round(x, 2)

rows = []
def add(**k):
    row = {c: '' for c in ROUND_HDR}
    for kk, v in k.items():
        if kk not in row:
            raise SystemExit('unknown column %s' % kk)
        row[kk] = v
    # the identity every loaded row must pass: valuation / denominator = stored multiple (2% tolerance)
    post, rev = row['post_money_musd'], row['revenue_musd']
    if post != '' and rev != '' and row['ev_revenue_x'] != '':
        calc = float(post) / float(rev)
        assert abs(calc - float(row['ev_revenue_x'])) / calc < 0.02, (row['transaction_id'], calc, row['ev_revenue_x'])
    rows.append(row)

# ---------------------------------------------------------------- agentcard lane
add(transaction_id='slash-2026-04', company_key='slash', company_name='Slash', date='Apr-26', date_iso='2026-04',
    round_type='Series C', capital_raised_musd='100.0', post_money_musd='1400.0', valuation_status='Disclosed',
    revenue_metric='Annualized revenue (> threshold)', revenue_musd='250.0', revenue_status='Disclosed (company)',
    ev_revenue_x=str(r2(1400/250)), subsector_as_supplied='Business banking and corporate cards for modern businesses',
    screening_category_as_supplied='Card Issuing & BaaS',
    lead_key_investors='Ribbit Capital (led); Khosla Ventures; Goodwater Capital (co-led); NEA; Y Combinator',
    round_source_url='https://www.slash.com/blog/series-c-fundraise-release',
    revenue_source_url='https://www.slash.com/blog/series-c-fundraise-release',
    notes=PULLED + "Slash's own release of 16-Apr-2026: 'Slash Financial, Inc., the banking platform built for modern businesses, is now valued at $1.4 billion following a $100m Series C funding round led by Ribbit Capital' and 'The company surpassed $250 million in annualized revenue in 2025'. 'Surpassed' makes the denominator a floor, so 5.6x is a CEILING. TechCrunch the same day (https://techcrunch.com/2026/04/16/slash-a-ramp-competitor-founded-by-teenagers-raises-100m-at-1-4b-valuation/): 'the company is generating $300 million in annualized revenue, profitably', which would give 4.7x; the company's own figure is used and the press figure noted. Pre/post not stated. Release also says 'grew from $10 million to $250 million in annualized revenue in 24 months' and 'more than $30 billion in annualized payment volume'. 'Annualized revenue' on a card and banking platform is interchange plus interest and is likely gross of rewards cost; basis INFERRED, not stated. No secondary component mentioned.",
    transaction_type='PRIMARY', denominator_basis='DISCLOSED_THRESHOLD', bound='<=', in_medians='1', verification=VER,
    growth_band='HYPER', growth_pct_at_round='400', growth_band_basis='DERIVED',
    revenue_basis='ARR_RUNRATE', volume_metric='PAYMENT_VOLUME', volume_musd='30000.0', volume_period='Annualised at the round', volume_basis='PAYMENT_VOLUME',
    ev_volume_x=str(round(1400/30000, 4)), revenue_period='RUN_RATE', valuation_basis='REVENUE',
    revenue_basis_source='INFERRED', basis_risk_note='Card/banking platform; annualized revenue likely gross of rewards and interchange pass-through. Growth 400% is DERIVED from $10m to $250m over 24 months, geometric.',
    valuation_pre_or_post='UNSPECIFIED')

add(transaction_id='bvnk-2024-12', company_key='bvnk', company_name='BVNK', date='Dec-24', date_iso='2024-12',
    round_type='Series B', capital_raised_musd='50.0', post_money_musd='750.0', valuation_status='Reported (Fortune, "around")',
    revenue_metric='Annualized revenue', revenue_musd='40.0', revenue_status='Reported (Fortune, day of round)',
    ev_revenue_x=str(r2(750/40)), subsector_as_supplied='Stablecoin payments infrastructure',
    screening_category_as_supplied='Card Issuing & BaaS',
    lead_key_investors='Haun Ventures (led); Coinbase Ventures; Tiger Global',
    round_source_url='https://fortune.com/crypto/2024/12/17/exclusive-stablecoin-bvnk-750-million-series-b-bridge-stripe-haun',
    revenue_source_url='https://fortune.com/crypto/2024/12/17/exclusive-stablecoin-bvnk-750-million-series-b-bridge-stripe-haun',
    notes=PULLED + "Fortune, 17-Dec-2024: 'raise a $50 million, all-equity Series B funding round' led by Haun Ventures; 'The round values BVNK at around $750 million'; 'BVNK has an annualized revenue of $40 million and processes $10 billion in annualized transaction volume'. Valuation is 'around', so Reported not Disclosed. Stablecoin rails with a card product, closer to a payments-rails comparable than an issuer. Later marks carry no revenue: Citi/Visa strategic investment 2025, and Mastercard's agreement to acquire for up to $1.8bn (Mar-2026, $300m contingent) with no revenue disclosed, so that CONTROL deal is not a row.",
    transaction_type='PRIMARY', denominator_basis='REPORTED_CONTEMPORANEOUS', bound='', in_medians='1', verification=VER,
    revenue_basis='ARR_RUNRATE', volume_metric='PAYMENT_VOLUME', volume_musd='10000.0', volume_period='Annualised at the round', volume_basis='PAYMENT_VOLUME',
    ev_volume_x=str(round(750/10000, 4)), revenue_period='RUN_RATE', valuation_basis='REVENUE',
    revenue_basis_source='INFERRED', basis_risk_note='Payments rails; annualized revenue is take on volume, basis not stated.', valuation_pre_or_post='UNSPECIFIED')

eur = FX[('EUR', '2026-08-05')]
add(transaction_id='moss-2026-08', company_key='moss', company_name='Moss', date='Aug-26', date_iso='2026-08',
    round_type='Series C', capital_raised_musd=str(r2(30*eur)), post_money_musd=str(r2(1000*eur)), valuation_status='Reported (> threshold)',
    revenue_metric='ARR (> threshold)', revenue_musd=str(r2(70*eur)), revenue_status='Reported (> threshold)',
    ev_revenue_x=str(r2(1000/70)), subsector_as_supplied='Spend management: corporate cards, expenses, invoices',
    screening_category_as_supplied='Card Issuing & BaaS',
    lead_key_investors='Portage (led); Cherry Ventures',
    round_source_url='https://www.eu-startups.com/2026/08/berlin-based-moss-hits-unicorn-status-after-closing-e30-million-series-c-to-expand-its-finance-ai-suite/',
    revenue_source_url='https://thenextweb.com/news/moss-berlin-unicorn-30m-series-c-finance-ai',
    notes=PULLED + "HELD OUT OF MEDIANS, NEEDS A RULING: BOTH FIGURES ARE FLOORS. EU-Startups, 5-Aug-2026: 'closed its EUR30 million Series C funding round at a valuation north of EUR1 billion' and 'It is generating more than EUR70 million in ARR'; TNW, 6-Aug-2026: 'values the spend-management company at more than EUR1bn' and 'reports annual recurring revenue above EUR70m'. A floor over a floor has no direction, so 14.3x is the ratio of the two stated thresholds and not a bound. Converted at the ECB reference rate of 5-Aug-2026, 1.1554 USD/EUR; the multiple is currency-free. Spend-management comparable (Pleo, Spendesk are held), not an issuing API.",
    transaction_type='PRIMARY', denominator_basis='DISCLOSED_THRESHOLD', bound='', in_medians='0', verification=VER,
    revenue_basis='ARR', revenue_period='RUN_RATE', fx_ccy='EUR', fx_rate=str(eur), fx_date='2026-08-05', valuation_basis='REVENUE',
    revenue_basis_source='STATED', basis_risk_note='Both valuation and ARR are stated as thresholds.', valuation_pre_or_post='UNSPECIFIED')

# ---------------------------------------------------------------- paymentkit lane
add(transaction_id='zuora-2024-10', company_key='zuora', company_name='Zuora', date='Oct-24', date_iso='2024-10',
    round_type='Take-private (Silver Lake and GIC)', capital_raised_musd='', post_money_musd='1700.0', valuation_status='Disclosed (transaction value, equity)',
    revenue_metric='Total revenue, LTM to 31-Jul-2024 (GAAP, filed)', revenue_musd=str(r2(431.7 + 225.2 - 211.1)), revenue_status='Disclosed (SEC filings)',
    ev_revenue_x=str(r2(1700/(431.7 + 225.2 - 211.1))), subsector_as_supplied='Subscription billing and monetization suite',
    screening_category_as_supplied='Commerce & Payments Software',
    lead_key_investors='Silver Lake; GIC',
    round_source_url='https://www.silverlake.com/zuora-enters-into-definitive-agreement-to-be-acquired-by-silver-lake-and-gic-for-1-7-billion/',
    revenue_source_url='https://www.sec.gov/Archives/edgar/data/1423774/000142377424000231/a20240731q2earningsrelease.htm',
    notes=PULLED + "CONTROL, TARGET WAS LISTED (NYSE: ZUO). Joint release of 17-Oct-2024: 'Silver Lake and GIC will acquire all outstanding shares of Zuora common stock for $10.00 per share in cash' in 'a transaction valued at $1.7 billion', 'an 18% premium to the Company's unaffected closing stock price and a 20% enterprise value premium'. Closed 14-Feb-2025. The $1.7bn is the equity transaction value; EV was not stated. DENOMINATOR IS LTM BUILT FROM THREE FILED FIGURES, arithmetic shown: FY2024 total revenue $431.7m (8-K of 28-Feb-2024, https://www.sec.gov/Archives/edgar/data/1423774/000142377424000062/a20240131q4er991.htm: 'Total revenue was $431.7 million') plus six months to 31-Jul-2024 $225.2m less six months to 31-Jul-2023 $211.1m (8-K of 21-Aug-2024, the revenue URL: 'Total revenue was $115.4 million' for the quarter, six-month figures from the tables) = $445.8m. Growth 7% is the Q2 FY25 year-on-year rate stated in the same release. A control premium travels with this row (rulebook B6).",
    transaction_type='CONTROL', denominator_basis='DISCLOSED_ACTUAL', bound='', in_medians='1', verification=VER,
    growth_band='MATURE', growth_pct_at_round='7', growth_band_basis='DISCLOSED', target_was_listed='1',
    revenue_basis='NET_REVENUE', revenue_period='LTM', valuation_basis='REVENUE',
    revenue_basis_source='STATED', basis_risk_note='GAAP total revenue of a subscription software company; net by construction.', valuation_pre_or_post='UNSPECIFIED')

inr = FX[('INR', '2026-01-23')]
add(transaction_id='juspay-2026-01', company_key='juspay', company_name='Juspay', date='Jan-26', date_iso='2026-01',
    round_type='Series D follow-on', capital_raised_musd='50.0', post_money_musd='1200.0', valuation_status='Reported',
    revenue_metric='Revenue from operations, FY2025 (filed)', revenue_musd=str(r2(5400/inr)), revenue_status='Reported (Entrackr, from filed accounts)',
    ev_revenue_x=str(r2(1200/(5400/inr))), subsector_as_supplied='Payments orchestration infrastructure (HyperSwitch)',
    screening_category_as_supplied='Commerce & Payments Software',
    lead_key_investors='WestBridge Capital',
    round_source_url='https://entrackr.com/news/juspay-raises-50-mn-from-westbridge-capital-at-12-bn-valuation-11023645',
    revenue_source_url='https://entrackr.com/news/juspay-raises-50-mn-from-westbridge-capital-at-12-bn-valuation-11023645',
    notes=PULLED + "Entrackr, 23-Jan-2026: 'Juspay has raised $50 million in a Series D follow-on round from WestBridge Capital'; 'The latest funding round pegged its valuation at $1.2 billion, compared to around $900 million in the previous round'; 'The primary capital will be used to support global expansion and product development, while the secondary portion will provide partial liquidity to early investors', so MIXED; 'For the fiscal year ended March 2025, Juspay reported operating revenue of Rs 540 crore and a profit of Rs 62.28 crore'. STALE DENOMINATOR: FY2025 closed ten months before pricing and is the latest filed figure the investor had (rulebook B1), so 20.4x is best read as a ceiling on a growing business; bound left empty because no later figure is stated. INR 5,400m at the ECB reference rate of 23-Jan-2026, 91.86 INR/USD = $58.8m. Indian payments revenue from operations is gross of processing costs.",
    transaction_type='MIXED', denominator_basis='DISCLOSED_ACTUAL', bound='', in_medians='1', verification=VER,
    revenue_basis='GROSS_REVENUE', revenue_period='FY2025', fx_ccy='INR', fx_rate=str(round(1/inr, 6)), fx_date='2026-01-23', valuation_basis='REVENUE',
    revenue_basis_source='INFERRED', basis_risk_note='Revenue from operations of an Indian PSP: gross of processing cost. FY ended 31-Mar-2025, ten months before the round.', valuation_pre_or_post='UNSPECIFIED')

inr = FX[('INR', '2025-02-05')]
add(transaction_id='cashfree-2025-02', company_key='cashfree', company_name='Cashfree Payments', date='Feb-25', date_iso='2025-02',
    round_type='Series C', capital_raised_musd='53.0', post_money_musd='700.0', valuation_status='Reported (TechCrunch, source familiar)',
    revenue_metric='Revenue from operations, FY2024 (filed)', revenue_musd=str(r2(6427/inr)), revenue_status='Reported (Entrackr, from filed accounts)',
    ev_revenue_x=str(r2(700/(6427/inr))), subsector_as_supplied='Payment gateway and payouts PSP',
    screening_category_as_supplied='Merchant Acquiring & PSP',
    lead_key_investors='KRAFTON (led); Apis Growth Fund II',
    round_source_url='https://techcrunch.com/2025/02/04/krafton-leads-cashfrees-53m-funding-at-700m-valuation/',
    revenue_source_url='https://entrackr.com/news/cashfree-payments-raises-53-mn-led-by-krafton-8690967',
    notes=PULLED + "TechCrunch, 4-Feb-2025: 'has raised $53 million in a new round of funding' led by Krafton, valued 'at $700 million' according to a source familiar with the terms. Entrackr, 5-Feb-2025, in the round coverage: 'Cashfree's revenue from operations grew by 4.7% to Rs 642.7 crore from Rs 613.8 crore in FY23'. FY2024 (to 31-Mar-2024) is the latest filed year at pricing; FY2025 later came in flat at Rs 640 crore (Entrackr, Oct-2025, https://entrackr.com/fintrackr/cashfree-posts-rs-640-cr-revenue-in-fy25-losses-rise-14-10533753), so the denominator is not stale in practice. INR 6,427m at the ECB reference rate of 5-Feb-2025, 87.37 INR/USD = $73.6m. A 9.5x mark on a flat-revenue PSP; net loss Rs 135 crore. Processes 'more than $80 billion for its customers each year' (TechCrunch).",
    transaction_type='PRIMARY', denominator_basis='DISCLOSED_ACTUAL', bound='', in_medians='1', verification=VER,
    growth_band='MATURE', growth_pct_at_round='4.7', growth_band_basis='DISCLOSED',
    revenue_basis='GROSS_REVENUE', revenue_period='FY2024', fx_ccy='INR', fx_rate=str(round(1/inr, 6)), fx_date='2025-02-05', valuation_basis='REVENUE',
    revenue_basis_source='INFERRED', basis_risk_note='Revenue from operations of an Indian PSP: gross of processing cost.', valuation_pre_or_post='UNSPECIFIED')

# ---------------------------------------------------------------- finn lane
inr = FX[('INR', '2025-03-31')]
add(transaction_id='spinny-2025-03', company_key='spinny', company_name='Spinny', date='Mar-25', date_iso='2025-03',
    round_type='Series F', capital_raised_musd='131.0', post_money_musd='1500.0', valuation_status='Reported post-money (Entrackr, "around")',
    revenue_metric='Revenue from operations, FY2025 (filed)', revenue_musd=str(r2(46570/inr)), revenue_status='Reported (Entrackr, from filed accounts)',
    ev_revenue_x=str(r2(1500/(46570/inr))), subsector_as_supplied='Full-stack used-car retail on owned inventory, home delivery',
    screening_category_as_supplied='Owned-Inventory Retail',
    lead_key_investors='Accel Leaders Fund (led); Elevation Capital; Tiger Global; Fundamentum; WestBridge Capital (extension, Jun-2025)',
    round_source_url='https://entrackr.com/news/spinny-raises-131-mn-led-by-accel-leaders-fund-8910456',
    revenue_source_url='https://entrackr.com/fintrackr/spinny-posts-rs-4657-cr-revenue-in-fy25-cuts-losses-by-28-10509574',
    notes=PULLED + "Entrackr, 31-Mar-2025: 'Used car platform Spinny has raised $131 million led by US-based Accel Leaders Fund'; 'Spinny will be valued at around $1.5 billion post money'; 'Spinny is raising $110 million as primary funding, while the remaining $21 million will be secondary, which includes ESOP buybacks and exits for early backers', so MIXED. Entrackr, 28-Sep-2025: 'revenue from operations jumped 25% year-on-year to Rs 4,657 crore, up from Rs 3,730 crore in FY24'; net loss Rs 423 crore. FY2025 closes in the pricing month, so the denominator is at-pricing. The round grew to about $170m with WestBridge by Jun-2025 with no restated valuation ('In March this year, the company closed $170 million round'). Another outlet (thearcweb.com) put the valuation at $1.7bn to $1.8bn and flat; the anchored Entrackr figure is used and the range noted. INR 46,570m at the ECB reference rate of 31-Mar-2025, 85.44 INR/USD = $545.1m. Revenue is the full sale price of cars sold from owned stock: gross by size, NET in our sense because the retailer keeps the whole sale (rulebook B3).",
    transaction_type='MIXED', denominator_basis='DISCLOSED_ACTUAL', bound='', in_medians='1', verification=VER,
    growth_band='MATURE', growth_pct_at_round='25', growth_band_basis='DISCLOSED',
    revenue_basis='NET_REVENUE', revenue_period='FY2025', fx_ccy='INR', fx_rate=str(round(1/inr, 6)), fx_date='2025-03-31', valuation_basis='REVENUE',
    revenue_basis_source='INFERRED', basis_risk_note='First-party retailer: owns the car it sells, so revenue from operations is the sale price and is net of nobody. Filed, not audited by us.', valuation_pre_or_post='POST')

add(transaction_id='moove-2024-03', company_key='moove', company_name='Moove', date='Mar-24', date_iso='2024-03',
    round_type='Series B', capital_raised_musd='100.0', post_money_musd='750.0', valuation_status='Reported post-money',
    revenue_metric='ARR', revenue_musd='115.0', revenue_status='Reported (TechCrunch, day of round)',
    ev_revenue_x=str(r2(750/115)), subsector_as_supplied='Owned vehicle fleet placed with ride-hail and delivery drivers on weekly drive-to-own payments',
    screening_category_as_supplied='Owned-Inventory Retail',
    lead_key_investors='Uber (led); Mubadala Investment Company; The Latest Ventures; AfricInvest; Palm Drive Capital; Triatlum Advisors; Future Africa',
    round_source_url='https://techcrunch.com/2024/03/19/uber-leads-100m-investment-in-african-mobility-fintech-moove-as-valuation-hits-750m/',
    revenue_source_url='https://techcrunch.com/2024/03/19/uber-leads-100m-investment-in-african-mobility-fintech-moove-as-valuation-hits-750m/',
    notes=PULLED + "TechCrunch, 19-Mar-2024: 'has raised $100 million in a funding round', 'pushing Moove's post-money valuation to $750 million', Uber led per sources close to the deal; 'Moove's annual recurring revenue also increased from $90 million to $115 million during this period' (since the Aug-2023 round at $550m); 'The four-year-old mobility fintech buys fleets of vehicles, which it then sells to drivers through the platform'. ENTITY AND MODEL: an owned fleet financed to gig drivers on weekly payments, not a consumer car subscription; it is the nearest owned-fleet, recurring-payment vehicle business with both figures disclosed. Growth 52% is DERIVED: $90m to $115m over seven months, annualised geometrically.",
    transaction_type='PRIMARY', denominator_basis='REPORTED_CONTEMPORANEOUS', bound='', in_medians='1', verification=VER,
    growth_band='MATURE', growth_pct_at_round='52', growth_band_basis='DERIVED',
    revenue_basis='ARR_RUNRATE', revenue_period='RUN_RATE', valuation_basis='REVENUE',
    revenue_basis_source='INFERRED', basis_risk_note='ARR of a vehicle-financing fleet operator: recurring driver payments, likely including the financing element. Basis not stated.', valuation_pre_or_post='POST')

add(transaction_id='moove-2026-08', company_key='moove', company_name='Moove', date='Aug-26', date_iso='2026-08',
    round_type='Series C', capital_raised_musd='250.0', post_money_musd='2100.0', valuation_status='Disclosed',
    revenue_metric='ARR', revenue_musd='420.0', revenue_status='Disclosed (company, in the lead investor release)',
    ev_revenue_x=str(r2(2100/420)), subsector_as_supplied='Owned vehicle fleet, 42,000 vehicles, drive-to-own and robotaxi fleet operations',
    screening_category_as_supplied='Owned-Inventory Retail',
    lead_key_investors='Mubadala Investment Company (led); Woven Capital; Ion Pacific (co-led); Uber; BlackRock; Prosus Ventures',
    round_source_url='https://www.mubadala.com/en/news/moove-raises-250-million-at-2-1-billion-valuation-to-scale-the-global-infrastructure-layer-for-autonomous-mobility',
    revenue_source_url='https://www.mubadala.com/en/news/moove-raises-250-million-at-2-1-billion-valuation-to-scale-the-global-infrastructure-layer-for-autonomous-mobility',
    notes=PULLED + "Mubadala release, 5-Aug-2026: 'Moove has raised $250 million at a $2.1 billion valuation in a Series C funding round', 'Led by Mubadala Investment Company and co-led by Woven Capital, Toyota's Growth Fund, and Ion Pacific'; 'has grown to $420 million ARR'; 'operates approximately 42,000 vehicles across 29 cities (13 countries)'; growth 'through strategic acquisitions, including the full acquisition of Kovi in Brazil and Tokyo Taxi in Japan'. ENTITY HAS BROADENED since the Series B: ARR includes Kovi (Brazilian car subscription for drivers) and Tokyo Taxi, and the company now sells itself as autonomous-fleet infrastructure. Pre/post not stated. Second round of the same company: the multi-round rule (A3) applies, 5.0x here against 6.5x in Mar-2024. Growth 71% is DERIVED from $115m (Mar-2024) to $420m over 29 months, annualised, and includes acquired revenue.",
    transaction_type='PRIMARY', denominator_basis='DISCLOSED_ACTUAL', bound='', in_medians='1', verification=VER,
    growth_band='MATURE', growth_pct_at_round='71', growth_band_basis='DERIVED',
    revenue_basis='ARR_RUNRATE', revenue_period='RUN_RATE', valuation_basis='REVENUE',
    revenue_basis_source='INFERRED', basis_risk_note='ARR includes acquired Kovi and Tokyo Taxi; fleet operator, basis not stated.', valuation_pre_or_post='UNSPECIFIED')

# ---------------------------------------------------------------- bizmark lane
add(transaction_id='e2open-2025-05', company_key='e2open', company_name='E2open', date='May-25', date_iso='2025-05',
    round_type='Take-private (WiseTech Global)', capital_raised_musd='', post_money_musd='2100.0', valuation_status='Disclosed (enterprise value)',
    revenue_metric='Total GAAP revenue, FY2025 (to 28-Feb-2025)', revenue_musd='607.7', revenue_status='Disclosed (company results release)',
    ev_revenue_x=str(r2(2100/607.7)), subsector_as_supplied='Connected supply chain software network',
    screening_category_as_supplied='Commerce Enablement & Fulfilment',
    lead_key_investors='WiseTech Global (acquirer)',
    round_source_url='https://www.e2open.com/news/press-releases/e2open-announces-acquisition-by-wisetech-global-concluding-strategic-review',
    revenue_source_url='https://www.stocktitan.net/news/ETWO/e2open-announces-fiscal-2025-fourth-quarter-and-full-year-financial-exr0sr6982jy.html',
    notes=PULLED + "CONTROL, TARGET WAS LISTED (NYSE: ETWO). E2open release, 25-May-2025: 'e2open stockholders will receive $3.30 per share in cash', 'equating to an enterprise value of $2.1 billion'; completed 3-Aug-2025. Results release of 29-Apr-2025 (read on the stocktitan mirror of the Business Wire text): 'Total GAAP revenue for fiscal 2025 was $607.7 million, a decrease of 4.2% from the prior fiscal year' and 'GAAP subscription revenue for fiscal 2025 was $528.0 million ... 87% of total revenue'. Fiscal year closed three months before the deal. Valuation is ENTERPRISE value, unlike the equity values on most rows, so this multiple is a true EV/revenue. A shrinking, mature planning network priced at 3.5x with a control premium: an archetype mark for supply-chain software, not an agentic-software comparable.",
    transaction_type='CONTROL', denominator_basis='DISCLOSED_ACTUAL', bound='', in_medians='1', verification=VER,
    growth_band='MATURE', growth_pct_at_round='-4.2', growth_band_basis='DISCLOSED', target_was_listed='1',
    revenue_basis='NET_REVENUE', revenue_period='FY2025', valuation_basis='REVENUE',
    revenue_basis_source='STATED', basis_risk_note='GAAP total revenue, 87% subscription; net by construction. Valuation is EV.', valuation_pre_or_post='UNSPECIFIED')

# ---------------------------------------------------------------- manifold-robotics lane
add(transaction_id='berkshire-grey-2023-03', company_key='berkshire-grey', company_name='Berkshire Grey', date='Mar-23', date_iso='2023-03',
    round_type='Take-private (SoftBank Group)', capital_raised_musd='', post_money_musd='375.0', valuation_status='Disclosed (transaction value, "approximately")',
    revenue_metric='Revenue, FY2022 (GAAP)', revenue_musd='65.9', revenue_status='Disclosed (company results release)',
    ev_revenue_x=str(r2(375/65.9)), subsector_as_supplied='AI-powered robotic fulfilment and material-handling systems for warehouses',
    screening_category_as_supplied='Commerce Enablement & Fulfilment',
    lead_key_investors='SoftBank Group (acquirer, 26.9% holder before the deal)',
    round_source_url='https://www.stocktitan.net/news/BGRY/berkshire-grey-enters-into-definitive-merger-agreement-with-soft-po70iyl4n3ou.html',
    revenue_source_url='https://www.stocktitan.net/news/BGRY/berkshire-grey-reports-fourth-quarter-and-full-year-2022-uzxnkiofoxi3.html',
    notes=PULLED + "CONTROL, TARGET WAS LISTED (Nasdaq: BGRY), DISTRESSED. Release of 24-Mar-2023 (stocktitan mirror of Business Wire): 'SoftBank will acquire all of the outstanding capital stock of the Company not currently owned by SoftBank for $1.40 per share in an all-cash transaction valued at approximately $375 million', 'a premium of approximately 24% to the closing stock price as of March 24, 2023'. Results release of 29-Mar-2023, five days later: 'Revenue of $65.9 million, an increase of 29% compared to 2021'. WHAT THE $375m IS: the merger proxy (DEFM14A of 27-Jun-2023, https://www.sec.gov/Archives/edgar/data/1824734/000114036123031699/ny20008555x8_defm14a.htm) shows 243,349,085 shares outstanding at the record date and SoftBank at 26.9% of voting power; 243.3m x $1.40 = $340.7m basic, so $375m reads as a fully diluted whole-company equity value rather than the price of the minority alone. Systems seller, not robots-as-a-service: a segment mark for warehouse robotics at 5.7x trailing revenue with a control premium on a collapsed SPAC stock.",
    transaction_type='CONTROL', denominator_basis='DISCLOSED_ACTUAL', bound='', in_medians='1', verification=VER,
    growth_band='MATURE', growth_pct_at_round='29', growth_band_basis='DISCLOSED', target_was_listed='1',
    revenue_basis='NET_REVENUE', revenue_period='FY2022', valuation_basis='REVENUE',
    revenue_basis_source='STATED', basis_risk_note='GAAP product and service revenue; equity value not EV, company held cash.', valuation_pre_or_post='UNSPECIFIED')

# ---------------------------------------------------------------- marble lane
add(transaction_id='restaurant365-2023-05', company_key='restaurant365', company_name='Restaurant365', date='May-23', date_iso='2023-05',
    round_type='Growth round', capital_raised_musd='135.0', post_money_musd='1000.0', valuation_status='Disclosed (> threshold)',
    revenue_metric='Revenue (> threshold)', revenue_musd='100.0', revenue_status='Disclosed (CEO quote in the release, > threshold)',
    ev_revenue_x=str(r2(1000/100)), subsector_as_supplied='Restaurant accounting, inventory and back-office software',
    screening_category_as_supplied='Vertical Software',
    lead_key_investors='KKR; L Catterton (co-led); ICONIQ Growth; Bessemer Venture Partners',
    round_source_url='https://www.prnewswire.com/news-releases/restaurant365-announces-135m-funding-round-co-led-by-kkr-and-l-catterton-301829458.html',
    revenue_source_url='https://www.prnewswire.com/news-releases/restaurant365-announces-135m-funding-round-co-led-by-kkr-and-l-catterton-301829458.html',
    notes=PULLED + "HELD OUT OF MEDIANS, NEEDS A RULING: BOTH FIGURES ARE FLOORS. PR Newswire, 19-May-2023: '$135M funding round co-led by global investment firms KKR and L Catterton', the company 'surpasses $1B valuation', and the CEO: 'Having recently crossed exciting milestones of $100M in revenue and $1B in value, we can't wait for what's next.' Same sentence, same date, so the pair is honest, but a floor over a floor has no direction: 10.0x is the ratio of the two thresholds, not a bound. 'Revenue' is unspecified; the company is subscription SaaS. The May-2024 $175m round (ICONIQ) disclosed neither a valuation nor a revenue figure and is not a row.",
    transaction_type='PRIMARY', denominator_basis='DISCLOSED_THRESHOLD', bound='', in_medians='0', verification=VER,
    revenue_basis='ARR', revenue_period='NOT STATED', valuation_basis='REVENUE',
    revenue_basis_source='INFERRED', basis_risk_note='CEO says "$100M in revenue"; subscription software, taken as recurring revenue.', valuation_pre_or_post='UNSPECIFIED')

add(transaction_id='owner-2026-08', company_key='owner', company_name='Owner', date='Aug-26', date_iso='2026-08',
    round_type='Series D', capital_raised_musd='240.0', post_money_musd='2300.0', valuation_status='Disclosed',
    revenue_metric='ARR (> threshold)', revenue_musd='100.0', revenue_status='Disclosed (company, > threshold)',
    ev_revenue_x=str(r2(2300/100)), subsector_as_supplied='Websites, online ordering and marketing for independent restaurants',
    screening_category_as_supplied='Vertical Software',
    lead_key_investors='Growth Equity at Goldman Sachs Alternatives (led); Meritech; Redpoint; Headline',
    round_source_url='https://www.prnewswire.com/news-releases/owner-raises-240m-led-by-goldman-sachs-alternatives-to-build-the-ai-native-platform-for-every-local-business-302862420.html',
    revenue_source_url='https://www.prnewswire.com/news-releases/owner-raises-240m-led-by-goldman-sachs-alternatives-to-build-the-ai-native-platform-for-every-local-business-302862420.html',
    notes=PULLED + "PR Newswire, 28-Aug-2026: 'Owner announced it has raised $240 million and reached a $2.3 billion valuation', 'Growth Equity at Goldman Sachs Alternatives led the financing', 'Owner launched in 2020 and has surpassed $100 million in ARR'. 'Surpassed' makes the denominator a floor, so 23.0x is a CEILING. Front-of-house software for restaurants (ordering, website, marketing) rather than back office: same customer, different job. The May-2025 Series C ($120m at $1bn) carried no ARR figure and is not a row.",
    transaction_type='PRIMARY', denominator_basis='DISCLOSED_THRESHOLD', bound='<=', in_medians='1', verification=VER,
    revenue_basis='ARR', revenue_period='RUN_RATE', valuation_basis='REVENUE',
    revenue_basis_source='STATED', basis_risk_note='', valuation_pre_or_post='UNSPECIFIED')

# ---------------------------------------------------------------- payna lane
add(transaction_id='auditboard-2024-05', company_key='auditboard', company_name='AuditBoard', date='May-24', date_iso='2024-05',
    round_type='Acquisition by Hg', capital_raised_musd='', post_money_musd='3000.0', valuation_status='Disclosed (> threshold, transaction value)',
    revenue_metric='ARR (> threshold)', revenue_musd='200.0', revenue_status='Disclosed (company, > threshold, late 2023)',
    ev_revenue_x=str(r2(3000/200)), subsector_as_supplied='Audit, risk and compliance management platform',
    screening_category_as_supplied='Vertical Software',
    lead_key_investors='Hg (buyer); Battery Ventures (largest selling institutional shareholder)',
    round_source_url='https://hgcapital.com/insights/auditboard-agrees-to-be-acquired-by-hg',
    revenue_source_url='https://hgcapital.com/insights/auditboard-agrees-to-be-acquired-by-hg',
    notes=PULLED + "CONTROL. HELD OUT OF MEDIANS, NEEDS A RULING: BOTH FIGURES ARE FLOORS. Hg announcement, 23-May-2024: 'AuditBoard has reached an agreement to be acquired in a transaction valued at over $3 billion' and 'AuditBoard announced earlier this year it had crossed a milestone of $200 million in annual recurring revenue during late 2023'. A floor over a floor has no direction, so 15.0x is the ratio of the thresholds, not a bound, and the ARR date ('late 2023') sits about six months before the deal. Later, no valuation attached: 'surpassed $300 million in annual recurring revenue' on 14-Oct-2025 (https://www.prnewswire.com/news-releases/auditboard-surpasses-300-million-in-arr-accelerates-growth-trajectory-302582638.html). Compliance-workflow software for regulated functions, the nearest disclosed mark to licensing and regulatory filing.",
    transaction_type='CONTROL', denominator_basis='DISCLOSED_THRESHOLD', bound='', in_medians='0', verification=VER,
    revenue_basis='ARR', revenue_period='RUN_RATE', valuation_basis='REVENUE',
    revenue_basis_source='STATED', basis_risk_note='Both figures thresholds; ARR dated late 2023 against a May-2024 deal.', valuation_pre_or_post='UNSPECIFIED')

add(transaction_id='legora-2026-04', company_key='legora', company_name='Legora', date='Apr-26', date_iso='2026-04',
    round_type='Series D (extension)', capital_raised_musd='600.0', post_money_musd='5600.0', valuation_status='Disclosed post-money',
    revenue_metric='ARR (> threshold)', revenue_musd='100.0', revenue_status='Disclosed (company, > threshold, 2-Apr-2026)',
    ev_revenue_x=str(r2(5600/100)), subsector_as_supplied='Agentic legal AI workspace for law firms and in-house teams',
    screening_category_as_supplied='Vertical Software',
    lead_key_investors='Accel (led the $550m Series D, Mar-2026); Atlassian Ventures and NVentures (extension); Benchmark; Bessemer; General Catalyst; ICONIQ; Redpoint; Y Combinator',
    round_source_url='https://legora.com/newsroom/legora-extends-series-d-with-additional-50-million-welcomes-atlassian-and-nventures-as-investors',
    revenue_source_url='https://legora.com/newsroom/legal-teams-adoption-of-ai-propels-legora-past-100-million-in-annual-recurring-revenue',
    notes=PULLED + "Legora newsroom, 30-Apr-2026: 'a $50 million extension of its previously announced Series D financing', 'valuing the company at $5.6 billion post-money', 'bringing the total round to $600 million in equity', 'Legora recently surpassed $100 million in annual recurring revenue'. The $550m first close was on 10-Mar-2026 at $5.55bn led by Accel (TechCrunch, https://techcrunch.com/2026/03/10/legora-reaches-5-55-billion-valuation-as-ai-legaltech-boom-endures/). Legora newsroom, 2-Apr-2026: 'Going from $1 million to $100 million in ARR in 18 months'. ONE ROW FOR THE WHOLE ROUND at the extension's post-money; capital_raised is the $600m total. 'Surpassed' makes the denominator a floor, so 56.0x is a CEILING. Seat-based legal software, the same category as Harvey, which the lane already holds. Growth is DERIVED from $1m to $100m over 18 months and is off the scale of the bands.",
    transaction_type='PRIMARY', denominator_basis='DISCLOSED_THRESHOLD', bound='<=', in_medians='1', verification=VER,
    growth_band='HYPER', growth_pct_at_round='2000', growth_band_basis='DERIVED',
    revenue_basis='ARR', revenue_period='RUN_RATE', valuation_basis='REVENUE',
    revenue_basis_source='STATED', basis_risk_note='', valuation_pre_or_post='POST')

# ---------------------------------------------------------------- osseus lane
add(transaction_id='applied-intuition-2025-06', company_key='applied-intuition', company_name='Applied Intuition', date='Jun-25', date_iso='2025-06',
    round_type='Series F plus tender offer', capital_raised_musd='600.0', post_money_musd='15000.0', valuation_status='Disclosed',
    revenue_metric='ARR ("about"), end of 2024', revenue_musd='400.0', revenue_status='Reported (The Information, 12-Mar-2025, sourced; read on techstartups.com)',
    ev_revenue_x=str(r2(15000/400)), subsector_as_supplied='Vehicle intelligence: simulation, validation and autonomy software for moving machines',
    screening_category_as_supplied='Design & Engineering',
    lead_key_investors='BlackRock-managed funds and accounts; Kleiner Perkins (co-led); Qatar Investment Authority; Abu Dhabi Investment Council; Greycroft; General Catalyst; Lux Capital; Bond',
    round_source_url='https://www.appliedintuition.com/press-releases/series-f',
    revenue_source_url='https://techstartups.com/2025/03/12/autonomous-vehicle-testing-startup-applied-intuition-in-talks-to-raise-funding-at-15-billion-valuation/',
    notes=PULLED + "Company release, 17-Jun-2025: 'today announced it has closed a $600 million Series F fundraise and tender offer at a $15 billion valuation', 'co-led by BlackRock-managed funds and accounts and Kleiner Perkins'. The $600m mixes primary and tender with no split stated, so MIXED and capital_raised overstates primary. DENOMINATOR IS SOURCED, NOT COMPANY-STATED, AND SIX MONTHS STALE: The Information, 12-Mar-2025, as read on techstartups.com the same day: 'By the end of last year, Applied Intuition had reached about $400 million in annual recurring revenue (ARR), doubling its figure from the previous year', citing 'a source with direct knowledge'. The Information's own page (https://www.theinformation.com/articles/self-driving-software-supplier-applied-intuition-in-talks-for-funding-at-15-billion-valuation) is paywalled and only its headline was readable. On a doubling business a Dec-2024 ARR against a Jun-2025 price makes 37.5x a CEILING. Growth 100% is the 'doubling' in the same sentence. The Mar-2024 Series E ($250m at $6bn) disclosed no revenue and is not a row.",
    transaction_type='MIXED', denominator_basis='REPORTED_CONTEMPORANEOUS', bound='<=', in_medians='1', verification=VER,
    growth_band='GROWING', growth_pct_at_round='100', growth_band_basis='THIRD_PARTY_DATED',
    revenue_basis='ARR', revenue_period='RUN_RATE', valuation_basis='REVENUE',
    revenue_basis_source='INFERRED', basis_risk_note='ARR reported by a named publication citing a source, not by the company; dated Dec-2024, six months before pricing.', valuation_pre_or_post='UNSPECIFIED')

add(transaction_id='vention-2026-01', company_key='vention', company_name='Vention', date='Jan-26', date_iso='2026-01',
    round_type='Series D', capital_raised_musd='110.0', post_money_musd='1000.0', valuation_status='Reported (> threshold, CEO to The Logic)',
    revenue_metric='Annual revenue (< threshold)', revenue_musd='100.0', revenue_status='Reported (< threshold, CEO to The Logic)',
    ev_revenue_x=str(r2(1000/100)), subsector_as_supplied='AI software and hardware platform to design, program and deploy automation and robotics',
    screening_category_as_supplied='Design & Engineering',
    lead_key_investors='Investissement Quebec; Desjardins Capital; NVentures; Fidelity Investments Canada',
    round_source_url='https://thelogic.co/news/vention-series-d-industrial-robots-quebec/',
    revenue_source_url='https://thelogic.co/news/vention-series-d-industrial-robots-quebec/',
    notes=PULLED + "The Logic, 27-Jan-2026: 'Montreal-based Vention has raised US$110 million in new funding'; 'Vention's latest funding round increases the firm's valuation, which is over $1 billion, Lacroix said'; 'The firm's revenue is just under $100 million annually, according to Lacroix'. A floor on the valuation over a ceiling on the revenue makes 10.0x a FLOOR, so bound is >=. Currency of the valuation is not spelled out; the round is quoted in US dollars and the figure is treated as USD. Company release (https://www.prnewswire.com/news-releases/vention-raises-110m-usd-150m-cad-to-accelerate-physical-ai-deployment-across-global-manufacturing-302670544.html) carries no figures. Revenue is largely hardware and equipment orders on the platform ('orders range from $40,000 to nearly $5 million'), so this is a platform-plus-hardware hybrid, not a pure software developer platform.",
    transaction_type='PRIMARY', denominator_basis='DISCLOSED_THRESHOLD', bound='>=', in_medians='1', verification=VER,
    revenue_basis='GROSS_REVENUE', revenue_period='NOT STATED', valuation_basis='REVENUE',
    revenue_basis_source='INFERRED', basis_risk_note='Revenue is mostly hardware sold through the platform; taken as product revenue, not ARR.', valuation_pre_or_post='UNSPECIFIED')

# ---------------------------------------------------------------- wispr-flow lane
add(transaction_id='suno-2025-11', company_key='suno', company_name='Suno', date='Nov-25', date_iso='2025-11',
    round_type='Series C', capital_raised_musd='250.0', post_money_musd='2450.0', valuation_status='Disclosed post-money',
    revenue_metric='Annual revenue', revenue_musd='200.0', revenue_status='Disclosed (company to WSJ, relayed by TechCrunch)',
    ev_revenue_x=str(r2(2450/200)), subsector_as_supplied='AI music generation app, consumer subscription',
    screening_category_as_supplied='Consumer & Prosumer Software',
    lead_key_investors='Menlo Ventures (led); NVentures; Hallwood Media; Lightspeed; Matrix',
    round_source_url='https://techcrunch.com/2025/11/19/legally-embattled-ai-music-startup-suno-raises-at-2-45b-valuation-on-200m-revenue/',
    revenue_source_url='https://techcrunch.com/2025/11/19/legally-embattled-ai-music-startup-suno-raises-at-2-45b-valuation-on-200m-revenue/',
    notes=PULLED + "TechCrunch, 19-Nov-2025: 'raised a $250 million Series C round at a $2.45 billion post-money valuation', 'The round was led by Menlo Ventures with participation from Nvidia's venture arm NVentures, as well as Hallwood Media, Lightspeed, and Matrix'; 'It has now hit $200 million in annual revenue, Suno told The Wall Street Journal'. 'Annual revenue' is the company's wording; for a subscription app it is read as an annualised run rate, not a closed fiscal year. Label copyright suits were live at pricing (Warner settled the same month). Cleanest consumer-subscription pair in the lane.",
    transaction_type='PRIMARY', denominator_basis='DISCLOSED_ACTUAL', bound='', in_medians='1', verification=VER,
    revenue_basis='ARR_RUNRATE', revenue_period='RUN_RATE', valuation_basis='REVENUE',
    revenue_basis_source='INFERRED', basis_risk_note="Company says 'annual revenue'; period not stated, read as run rate.", valuation_pre_or_post='POST')

add(transaction_id='suno-2026-06', company_key='suno', company_name='Suno', date='Jun-26', date_iso='2026-06',
    round_type='Series D', capital_raised_musd='400.0', post_money_musd='5400.0', valuation_status='Disclosed',
    revenue_metric='ARR (27-Feb-2026)', revenue_musd='300.0', revenue_status='Disclosed (CEO on LinkedIn, reported by TechCrunch)',
    ev_revenue_x=str(r2(5400/300)), subsector_as_supplied='AI music generation app, consumer subscription',
    screening_category_as_supplied='Consumer & Prosumer Software',
    lead_key_investors='Bond Capital (led); IVP; Forerunner; Union Square Ventures; Alkeon; Quiet; Matrix; Lightspeed; Menlo; Schroders Capital',
    round_source_url='https://techcrunch.com/2026/06/03/still-facing-copyright-lawsuits-ai-music-generator-suno-raises-another-400m/',
    revenue_source_url='https://techcrunch.com/2026/02/27/ai-music-generator-suno-hits-2-million-paid-subscribers-and-300m-in-annual-recurring-revenue/',
    notes=PULLED + "TechCrunch, 3-Jun-2026: 'has raised a $400 million Series D round', 'valuing the company at $5.4 billion', 'led by Bond Capital'. TechCrunch, 27-Feb-2026: CEO Mikey Shulman on LinkedIn, '2 million paid subscribers' and '$300 million in annual recurring revenue'. DENOMINATOR IS THREE MONTHS OLD on a business that went from $200m (Nov-2025) to $300m (Feb-2026), so 18.0x is a CEILING. Pre/post not stated. Second round of the same company, multi-round rule A3 applies against 12.3x in Nov-2025. Paying subscribers loaded as a count: 2,000,000 PAYING_SUBSCRIBERS at 27-Feb-2026 against $5,400m is $2,700 of value per paying subscriber. Growth 406% is DERIVED from $200m to $300m over three months, annualised, and is noisy.",
    transaction_type='PRIMARY', denominator_basis='DISCLOSED_ACTUAL', bound='<=', in_medians='1', verification=VER,
    growth_band='HYPER', growth_pct_at_round='406', growth_band_basis='DERIVED',
    revenue_basis='ARR', volume_metric='PAYING_SUBSCRIBERS', volume_musd='2.0', volume_period='At 27-Feb-2026', volume_basis='PAYING_SUBSCRIBERS',
    ev_volume_x='2700.0', paying_users_k='2000', revenue_period='RUN_RATE', valuation_basis='REVENUE',
    revenue_basis_source='STATED', basis_risk_note='', valuation_pre_or_post='UNSPECIFIED')

add(transaction_id='framer-2025-08', company_key='framer', company_name='Framer', date='Aug-25', date_iso='2025-08',
    round_type='Series D', capital_raised_musd='100.0', post_money_musd='2000.0', valuation_status='Disclosed',
    revenue_metric='ARR', revenue_musd='50.0', revenue_status='Disclosed (CEO to TechCrunch)',
    ev_revenue_x=str(r2(2000/50)), subsector_as_supplied='No-code website builder, prosumer and small-business subscription',
    screening_category_as_supplied='Consumer & Prosumer Software',
    lead_key_investors='Meritech; Atomico (co-led)',
    round_source_url='https://techcrunch.com/2025/08/28/no-code-website-builder-framer-reaches-2b-valuation/',
    revenue_source_url='https://techcrunch.com/2025/08/28/no-code-website-builder-framer-reaches-2b-valuation/',
    notes=PULLED + "TechCrunch, 28-Aug-2025: 'reached a $2 billion valuation', 'raising a $100 million Series D funding round', 'led by existing investors Meritech and Atomico'; 'the company reached $50 million in annual recurring revenue this year, and aims to cross the $100 million threshold next year'; CEO Koen Bok: 'We've been break-even for the past year'. Figures are the CEO's to TechCrunch; no company release with numbers. Buyer is designers and small businesses, prosumer to SMB. Pre/post not stated.",
    transaction_type='PRIMARY', denominator_basis='DISCLOSED_ACTUAL', bound='', in_medians='1', verification=VER,
    revenue_basis='ARR', revenue_period='RUN_RATE', valuation_basis='REVENUE',
    revenue_basis_source='STATED', basis_risk_note='', valuation_pre_or_post='UNSPECIFIED')

add(transaction_id='genspark-2025-11', company_key='genspark', company_name='Genspark', date='Nov-25', date_iso='2025-11',
    round_type='Series B', capital_raised_musd='275.0', post_money_musd='1250.0', valuation_status='Disclosed post-money',
    revenue_metric='Annualized run rate (> threshold)', revenue_musd='50.0', revenue_status='Disclosed (investor release, > threshold, milestone reached within five months of launch)',
    ev_revenue_x=str(r2(1250/50)), subsector_as_supplied='Agentic AI workspace for knowledge workers, prosumer subscription',
    screening_category_as_supplied='Consumer & Prosumer Software',
    lead_key_investors='Emergence Capital Partners (led); SBI Investment; LG Technology Ventures; Pavilion Capital; Uphonest Capital; Lanchi Ventures',
    round_source_url='https://www.prnewswire.com/news-releases/lanchi-ventures-backed-genspark-raises-275m-series-b-launches-ai-workspace-to-put-busywork-on-autopilot-302622111.html',
    revenue_source_url='https://www.prnewswire.com/news-releases/lanchi-ventures-backed-genspark-raises-275m-series-b-launches-ai-workspace-to-put-busywork-on-autopilot-302622111.html',
    notes=PULLED + "PR Newswire, 20-Nov-2025, issued by investor Lanchi Ventures: 'Genspark today announced it has closed an oversubscribed $275 million Series B financing round at a $1.25 billion post-money valuation'; 'breaking $50 million in annualized run rate within five months'. The run rate is a milestone crossed months before the round, so the denominator is a floor and 25.0x is a CEILING, likely a loose one. The release is the investor's, not the company's.",
    transaction_type='PRIMARY', denominator_basis='DISCLOSED_THRESHOLD', bound='<=', in_medians='1', verification=VER,
    revenue_basis='ARR_RUNRATE', revenue_period='RUN_RATE', valuation_basis='REVENUE',
    revenue_basis_source='STATED', basis_risk_note='Run-rate milestone dated before the round; ceiling is loose.', valuation_pre_or_post='POST')

# ---------------------------------------------------------------- talent marketplaces (clera, standout, nursa, priori-legal)
add(transaction_id='mercor-2025-02', company_key='mercor', company_name='Mercor', date='Feb-25', date_iso='2025-02',
    round_type='Series B', capital_raised_musd='100.0', post_money_musd='2000.0', valuation_status='Disclosed',
    revenue_metric='ARR (latest month x 12)', revenue_musd='75.0', revenue_status='Disclosed (company to TechCrunch)',
    ev_revenue_x=str(r2(2000/75)), subsector_as_supplied='AI-vetted expert labour marketplace for AI labs, hourly finder fee',
    screening_category_as_supplied='Freelance & Services Marketplace',
    lead_key_investors='Felicis (led); Benchmark; General Catalyst; DST Global; Menlo Ventures',
    round_source_url='https://techcrunch.com/2025/02/20/mercor-an-ai-recruiting-startup-founded-by-21-year-olds-raises-100m-at-2b-valuation/',
    revenue_source_url='https://techcrunch.com/2025/02/20/mercor-an-ai-recruiting-startup-founded-by-21-year-olds-raises-100m-at-2b-valuation/',
    notes=PULLED + "TechCrunch, 20-Feb-2025: 'has raised $100 million in a Series B round', 'valuing Mercor at $2 billion, eight times its previous valuation', 'Felicis led the round'; '$75 million ARR', 'calculated by multiplying its latest monthly revenue by 12'; revenue 'by charging hourly finders' fees to its clients'; the platform 'automates resume screening and candidate matching, and offers AI-powered interviews and payroll management'. GROSS BASIS: the CEO later confirmed (TechCrunch, 9-Sep-2025) that Mercor's revenue 'includes the total amount that customers pay Mercor for services before its contractors receive their portion', so 26.7x is on gross billings, not net take (rulebook B3). Pre/post not stated.",
    transaction_type='PRIMARY', denominator_basis='DISCLOSED_ACTUAL', bound='', in_medians='1', verification=VER,
    revenue_basis='GROSS_REVENUE', revenue_period='RUN_RATE', valuation_basis='REVENUE',
    revenue_basis_source='STATED', basis_risk_note='ARR is gross of contractor pay, stated by the CEO in Sep-2025.', valuation_pre_or_post='UNSPECIFIED')

add(transaction_id='mercor-2025-10', company_key='mercor', company_name='Mercor', date='Oct-25', date_iso='2025-10',
    round_type='Series C', capital_raised_musd='350.0', post_money_musd='10000.0', valuation_status='Disclosed',
    revenue_metric='Annualized run-rate revenue (> threshold, 9-Sep-2025)', revenue_musd='450.0', revenue_status='Disclosed (CEO to TechCrunch, > threshold, seven weeks before the round)',
    ev_revenue_x=str(r2(10000/450)), subsector_as_supplied='AI-vetted expert labour marketplace for AI labs, hourly finder fee',
    screening_category_as_supplied='Freelance & Services Marketplace',
    lead_key_investors='Felicis (led); Benchmark; General Catalyst; Robinhood Ventures',
    round_source_url='https://www.mercor.com/blog/series-c/',
    revenue_source_url='https://techcrunch.com/2025/09/09/sources-ai-training-startup-mercor-eyes-10b-valuation-on-450m-run-rate/',
    notes=PULLED + "Mercor's own post, 27-Oct-2025: '$350 million Series C funding, led by Felicis with participation from Benchmark, General Catalyst, and Robinhood Ventures', 'This round values Mercor at $10 billion, 5x our Series B valuation'. TechCrunch, 9-Sep-2025: 'Mercor is approaching $450 million in annualized run-rate revenue, one person said' and the CEO 'said the company's ARR is higher than $450 million', clarifying that 'the company's revenue includes the total amount that customers pay Mercor for services before its contractors receive their portion'. The round article itself (https://techcrunch.com/2025/10/27/mercor-quintuples-valuation-to-10b-with-350m-series-c/) carries only a projection, 'on track to hit $500 million in ARR', so the hard figure is the CEO's floor seven weeks earlier: 22.2x is a CEILING on GROSS billings. Second round of the same company, multi-round rule A3 applies against 26.7x in Feb-2025. Growth is DERIVED from $75m (Feb-2025) to >$450m (Sep-2025), off the scale of the bands.",
    transaction_type='PRIMARY', denominator_basis='DISCLOSED_THRESHOLD', bound='<=', in_medians='1', verification=VER,
    growth_band='HYPER', growth_pct_at_round='2000', growth_band_basis='DERIVED',
    revenue_basis='GROSS_REVENUE', revenue_period='RUN_RATE', valuation_basis='REVENUE',
    revenue_basis_source='STATED', basis_risk_note='Gross of contractor pay, CEO-stated.', valuation_pre_or_post='UNSPECIFIED')

add(transaction_id='micro1-2025-09', company_key='micro1', company_name='Micro1', date='Sep-25', date_iso='2025-09',
    round_type='Series A', capital_raised_musd='35.0', post_money_musd='500.0', valuation_status='Disclosed',
    revenue_metric='ARR', revenue_musd='50.0', revenue_status='Disclosed (company to TechCrunch)',
    ev_revenue_x=str(r2(500/50)), subsector_as_supplied='AI recruiter that screens contractors for AI labs, managed labour marketplace',
    screening_category_as_supplied='Freelance & Services Marketplace',
    lead_key_investors='01 Advisors (led)',
    round_source_url='https://techcrunch.com/2025/09/12/micro1-a-competitor-to-scale-ai-raises-funds-at-500m-valuation/',
    revenue_source_url='https://techcrunch.com/2025/09/12/micro1-a-competitor-to-scale-ai-raises-funds-at-500m-valuation/',
    notes=PULLED + "TechCrunch, 12-Sep-2025: 'has raised a $35 million Series A funding round' that 'values the company at $500 million', 'led by 01 Advisors'; 'Micro1 is now generating $50 million in annual recurring revenue (ARR), up from $7 million at the start of 2025'; it 'helps AI companies find and manage human contractors for data labeling and training' and built 'Zara', an AI recruiter that interviews and vets applicants. LIKELY GROSS: TechCrunch in Aug-2026 described Micro1's later figures as a 'gross annual run rate' of which 'Micro1 retains roughly 60% to 70%'; the Sep-2025 page does not say, so basis is INFERRED as gross. Dec-2025 milestone with no valuation attached: 'surpassed $100 million in ARR' (https://techcrunch.com/2025/12/04/micro1-a-scale-ai-competitor-touts-crossing-100m-arr/). Growth is DERIVED from $7m to $50m in about eight months, off the scale of the bands. Pre/post not stated.",
    transaction_type='PRIMARY', denominator_basis='DISCLOSED_ACTUAL', bound='', in_medians='1', verification=VER,
    growth_band='HYPER', growth_pct_at_round='1500', growth_band_basis='DERIVED',
    revenue_basis='GROSS_REVENUE', revenue_period='RUN_RATE', valuation_basis='REVENUE',
    revenue_basis_source='INFERRED', basis_risk_note='ARR likely gross of contractor pay (later TechCrunch coverage); not stated on the round page.', valuation_pre_or_post='UNSPECIFIED')


# ---------------------------------------------------------------- control transactions named in the work order (B6: labelled anchors)
add(transaction_id='sapiens-2025-08', company_key='sapiens', company_name='Sapiens International', date='Aug-25', date_iso='2025-08',
    round_type='Take-private (Advent International)', capital_raised_musd='', post_money_musd='2500.0', valuation_status='Disclosed (transaction value, "approximately")',
    revenue_metric='Total revenue, LTM to 30-Jun-2025 (GAAP, filed)', revenue_musd=str(r2(542.4 + 277.7 - 271.0)), revenue_status='Disclosed (SEC filings, 6-K)',
    ev_revenue_x=str(r2(2500/(542.4 + 277.7 - 271.0))), subsector_as_supplied='Insurance software for carriers (policy, billing, claims)',
    screening_category_as_supplied='Insurance Technology',
    lead_key_investors='Advent International (acquirer)',
    round_source_url='https://www.sec.gov/Archives/edgar/data/885740/000121390025075257/ea025288001ex99-1_sapiens.htm',
    revenue_source_url='https://www.sec.gov/Archives/edgar/data/885740/000121390025075274/ea025222801ex99-1_sapiens.htm',
    notes=PULLED + "CONTROL, TARGET WAS LISTED (Nasdaq and TASE: SPNS). Named in the work order of 4-Sep as a control transaction for the insurance-software lanes (evergrove, insurf, florin, denta). Sapiens release of 13-Aug-2025, filed on Form 6-K: 'Sapiens shareholders will receive $43.50 per common share in cash' and 'Transaction values Sapiens at approximately $2.5 billion.' No revenue in the deal release. DENOMINATOR IS LTM BUILT FROM THREE FILED FIGURES, arithmetic shown: FY2024 revenue $542.4m (Q4-2024 release, 6-K of 18-Feb-2025, https://www.sec.gov/Archives/edgar/data/885740/000121390025014549/ea023133701ex99-1_sapiens.htm) plus six months to 30-Jun-2025 $277.7m less six months to 30-Jun-2024 $271.0m (Q2-2025 release, 6-K of 13-Aug-2025, the revenue URL, income statement in thousands: 277,707 and 271,049) = $549.1m. The Q2 release was filed the same day as the deal, so the denominator is at-pricing. Growth 5.4% is the FY2024 rate stated in the Q4-2024 release. Equity value, not EV. A control premium travels with this row (B6).",
    transaction_type='CONTROL', denominator_basis='DISCLOSED_ACTUAL', bound='', in_medians='1', verification=VER,
    growth_band='MATURE', growth_pct_at_round='5.4', growth_band_basis='DISCLOSED', target_was_listed='1',
    revenue_basis='NET_REVENUE', revenue_period='LTM', valuation_basis='REVENUE',
    revenue_basis_source='STATED', basis_risk_note='GAAP revenue of a software and services vendor; net by construction.', valuation_pre_or_post='UNSPECIFIED')

add(transaction_id='accolade-2025-01', company_key='accolade', company_name='Accolade', date='Jan-25', date_iso='2025-01',
    round_type='Acquisition by Transcarent', capital_raised_musd='', post_money_musd='621.0', valuation_status='Disclosed (transaction value, "approximately")',
    revenue_metric='Total revenue, LTM to 30-Nov-2024 (GAAP, filed)', revenue_musd=str(r2(414.3 + 321.887 - 289.461)), revenue_status='Disclosed (SEC filings, 10-Q and 8-K)',
    ev_revenue_x=str(r2(621/(414.3 + 321.887 - 289.461))), subsector_as_supplied='Payer- and employer-facing care navigation and advocacy',
    screening_category_as_supplied='Insurance Technology',
    lead_key_investors='Transcarent (acquirer)',
    round_source_url='https://www.sec.gov/Archives/edgar/data/1481646/000114036125000544/ny20041213x1_ex99-1.htm',
    revenue_source_url='https://www.sec.gov/Archives/edgar/data/1481646/000148164625000006/accd-20241130.htm',
    notes=PULLED + "CONTROL, TARGET WAS LISTED (Nasdaq: ACCD). Named in the work order of 4-Sep as a control transaction for the payer-facing lanes (insurf, evergrove). Accolade release of 8-Jan-2025, filed on Form 8-K: '$7.03 per share in cash', transaction value 'approximately $621M'; completed April 2025. No revenue in the deal release. DENOMINATOR IS LTM BUILT FROM THREE FILED FIGURES, arithmetic shown: FY2024 (year to 29-Feb-2024) revenue $414.3m (Q4 FY2024 earnings release, 8-K of 25-Apr-2024, https://www.sec.gov/Archives/edgar/data/1481646/000148164624000018/accd-20240425xexx991earnin.htm) plus nine months to 30-Nov-2024 $321.887m less nine months to 30-Nov-2023 $289.461m (10-Q for the quarter ended 30-Nov-2024, filed 10-Jan-2025, the revenue URL) = $446.7m. The 10-Q was filed two days after the deal and covers the last closed quarter before it. Growth 14% is the FY2024 rate in the Q4 FY2024 release ('$414.3 ... $363.1 ... 14%'); the nine-month rate is 11.2% by arithmetic. Equity value, not EV; a 1.4x mark on a loss-making care-navigation business bought by a private acquirer. A control premium travels with this row (B6).",
    transaction_type='CONTROL', denominator_basis='DISCLOSED_ACTUAL', bound='', in_medians='1', verification=VER,
    growth_band='MATURE', growth_pct_at_round='14', growth_band_basis='DISCLOSED', target_was_listed='1',
    revenue_basis='NET_REVENUE', revenue_period='LTM', valuation_basis='REVENUE',
    revenue_basis_source='STATED', basis_risk_note='Access fees and usage-based fees paid by employers and health plans; net by construction.', valuation_pre_or_post='UNSPECIFIED')

add(transaction_id='udemy-2025-12', company_key='udemy', company_name='Udemy', date='Dec-25', date_iso='2025-12',
    round_type='All-stock merger into Coursera', capital_raised_musd='', post_money_musd=str(r2(2500*0.41)), valuation_status='Derived from two stated figures: 41% of a $2.5bn combined implied equity value',
    revenue_metric='Total revenue, LTM to 30-Sep-2025 (GAAP, filed)', revenue_musd=str(r2(786.6 + 595.859 - 586.623)), revenue_status='Disclosed (SEC filings, 8-K)',
    ev_revenue_x=str(r2(2500*0.41/(786.6 + 595.859 - 586.623))), subsector_as_supplied='Online course marketplace, consumer and enterprise learning',
    screening_category_as_supplied='Online Learning',
    lead_key_investors='Coursera (acquirer, all-stock)',
    round_source_url='https://www.sec.gov/Archives/edgar/data/1651562/000114036125045770/ef20061429_ex99-1.htm',
    revenue_source_url='https://www.sec.gov/Archives/edgar/data/1607939/000160793925000138/q32025pressrelease.htm',
    notes=PULLED + "CONTROL, TARGET WAS LISTED (Nasdaq: UDMY). HELD OUT OF MEDIANS, NEEDS A RULING: THE VALUE IS ARITHMETIC ON TWO STATED FIGURES, NOT A STATED PRICE. Named in the work order of 4-Sep as a control transaction for the learning lanes (honen, wondering, befreed). Coursera release of 17-Dec-2025, filed on Form 8-K: 'Udemy stockholders will receive 0.800 shares of Coursera common stock for each share of Udemy common stock'; 'the implied equity value of the combined company is approximately $2.5 billion'; 'existing Coursera stockholders are expected to own approximately 59% and existing Udemy stockholders are expected to own approximately 41% of the combined company, on a fully diluted basis'; 'Pro Forma Annual Revenue of More Than $1.5 Billion'. No standalone Udemy value is stated anywhere in the release, so $1,025m is 41% of $2.5bn and moves with Coursera's share price; the closing value in the completed-merger 8-K (2026) is the figure to replace it with. DENOMINATOR IS LTM BUILT FROM THREE FILED FIGURES: FY2024 revenue $786.6m (Q4-2024 release, 8-K of 13-Feb-2025, https://www.sec.gov/Archives/edgar/data/1607939/000160793925000007/q42024pressrelease.htm: 'Total revenue increased 8% year-over-year to $786.6 million') plus nine months to 30-Sep-2025 $595.859m less nine months to 30-Sep-2024 $586.623m (Q3-2025 release, 8-K of 29-Oct-2025, the revenue URL) = $795.8m. Growth 8% is FY2024's stated rate; the nine-month 2025 rate is 1.6% by arithmetic. GROSS in our sense: Udemy books the full course price and pays instructors inside cost of revenue.",
    transaction_type='CONTROL', denominator_basis='DISCLOSED_ACTUAL', bound='', in_medians='0', verification=VER,
    growth_band='MATURE', growth_pct_at_round='8', growth_band_basis='DISCLOSED', target_was_listed='1',
    revenue_basis='GROSS_REVENUE', revenue_period='LTM', valuation_basis='REVENUE',
    revenue_basis_source='INFERRED', basis_risk_note='Marketplace revenue booked gross of instructor payouts; valuation is 41% of a stated combined implied equity value, not a stated standalone price.', valuation_pre_or_post='UNSPECIFIED')

# ------------------------------------------------------------------------------------------------
# TAG ROWS. Same vocabulary as private-companies-tags.csv. Archetype on how the company earns money.
# ------------------------------------------------------------------------------------------------
tags = []
def tag(**k):
    row = {c: '' for c in TAG_HDR}
    for kk, v in k.items():
        if kk not in row: raise SystemExit('unknown tag column %s' % kk)
        row[kk] = v
    tags.append(row)

TAGNOTE = 'Tagged 05-Sep-2026 by Claude on sourcing the row (docs/prompts/work-order-claude-4sep.md). Archetype assigned on how the company earns money, not on how it markets itself.'

tag(company_key='slash', company_name='Slash', archetype='Card Issuing & BaaS', archetype_secondary='Digital Bank & Deposits', industry='Horizontal',
    function='Finance & Payments', buyer='SMB', gtm_motion='PLG', revenue_model='TRANSACTION_FEE', product_role='PLATFORM_SUITE', ai_stance='AI_EMBEDDED',
    product_tags='Business Banking|Corporate Cards|Virtual Cards|Spend Management|Stablecoin Payments|Programmatic Spend Controls|Card API|Treasury',
    tags_as_of='2026-04', screening_category_as_supplied='Card Issuing & BaaS', taxonomy_note=TAGNOTE + ' Interchange and interest on business accounts; cards issued to modern businesses including agent-driven spend.',
    what_it_does='runs business checking accounts and issues corporate and virtual cards with spend controls, earning interchange and interest on balances')
tag(company_key='bvnk', company_name='BVNK', archetype='Card Issuing & BaaS', archetype_secondary='Crypto & Digital Assets', industry='Financial Services',
    function='Finance & Payments', buyer='ENTERPRISE', gtm_motion='ENT_SALES', revenue_model='TRANSACTION_FEE', product_role='INFRA_LAYER', ai_stance='AI_NEUTRAL',
    product_tags='Stablecoin Payments|Payment Rails|On Ramp Off Ramp|Embedded Wallets|Cross Border Settlement|Virtual Card Issuing|Machine To Machine Payments|Payments API',
    tags_as_of='2024-12', screening_category_as_supplied='Card Issuing & BaaS', taxonomy_note=TAGNOTE + ' Earns a take on stablecoin payment volume; card issuing is one product on the rails. Acquired by Mastercard in 2026 (terms in the round note).',
    what_it_does='moves money for businesses over stablecoin rails with wallets, on and off ramps and card issuing, earning a fee on every dollar settled')
tag(company_key='moss', company_name='Moss', archetype='Card Issuing & BaaS', archetype_secondary='Business Applications', industry='Horizontal',
    function='Finance & Payments', buyer='SMB', gtm_motion='MIDMARKET', revenue_model='PLATFORM', product_role='PLATFORM_SUITE', ai_stance='AI_EMBEDDED',
    product_tags='Corporate Cards|Spend Management|Expense Management|Invoice Processing|Virtual Cards|Programmatic Spend Controls|Finance Automation|Finance AI Agents',
    tags_as_of='2026-08', screening_category_as_supplied='Card Issuing & BaaS', taxonomy_note=TAGNOTE + ' Subscription plus interchange, so PLATFORM rather than SEATS; the same shape as Pleo and Spendesk.',
    what_it_does='issues corporate cards and runs expenses and invoices for European SMBs, earning a subscription and interchange on card spend')
tag(company_key='zuora', company_name='Zuora', archetype='Commerce & Payments Software', archetype_secondary='Business Applications', industry='Horizontal',
    function='Finance & Payments', buyer='ENTERPRISE', gtm_motion='ENT_SALES', revenue_model='SEATS', product_role='SOR', ai_stance='AI_EMBEDDED',
    product_tags='Subscription Billing|Billing Infrastructure|Revenue Recognition|Payments|Usage Based Billing|Monetization|Quote To Cash|Subscription Management',
    tags_as_of='2024-10', status_today='Taken private by Silver Lake and GIC, closed 14-Feb-2025; no longer an independent listed comparable.',
    screening_category_as_supplied='Commerce & Payments Software', taxonomy_note=TAGNOTE + ' M&A control-transaction row of a formerly listed company.',
    what_it_does='runs subscription billing, revenue recognition and payments for large subscription businesses, sold as enterprise software on an annual contract')
tag(company_key='juspay', company_name='Juspay', archetype='Commerce & Payments Software', archetype_secondary='Merchant Acquiring & PSP', industry='Financial Services',
    function='Finance & Payments', buyer='ENTERPRISE', gtm_motion='ENT_SALES', revenue_model='TRANSACTION_FEE', product_role='INFRA_LAYER', ai_stance='AI_NEUTRAL',
    product_tags='Payment Orchestration|Payments Failover|Processor Redundancy|Checkout|Payment Routing|Open Source Payments|Payments Infrastructure|India',
    tags_as_of='2026-01', screening_category_as_supplied='Commerce & Payments Software', taxonomy_note=TAGNOTE + ' Orchestration layer that routes across processors; earns on volume routed, so TRANSACTION_FEE.',
    what_it_does='sits between large merchants and many payment processors, routing and retrying each payment across them, earning a fee on volume')
tag(company_key='cashfree', company_name='Cashfree Payments', archetype='Merchant Acquiring & PSP', archetype_secondary='Commerce & Payments Software', industry='Financial Services',
    function='Finance & Payments', buyer='SMB', gtm_motion='PLG', revenue_model='TRANSACTION_FEE', product_role='INFRA_LAYER', ai_stance='AI_NEUTRAL',
    product_tags='Payment Gateway|Payouts|Payment Processing|Subscription Billing|Identity Verification|Payments API|India|Collections',
    tags_as_of='2025-02', screening_category_as_supplied='Merchant Acquiring & PSP', taxonomy_note=TAGNOTE,
    what_it_does='collects online payments and makes payouts for Indian businesses through an API, taking a fee on every transaction')
tag(company_key='spinny', company_name='Spinny', archetype='Owned-Inventory Retail', archetype_secondary='', industry='Retail & Commerce',
    function='Commerce Operations', buyer='CONSUMER', gtm_motion='PAID_ACQUISITION', revenue_model='OWNED_INVENTORY', product_role='DESTINATION', ai_stance='AI_NEUTRAL',
    product_tags='Used Cars|Owned Vehicle Inventory|Car Retail|Home Delivery|Refurbishment|Test Drive At Home|Ownership Alternative|India',
    tags_as_of='2025-03', screening_category_as_supplied='Owned-Inventory Retail', taxonomy_note=TAGNOTE + ' Buys, refurbishes and sells cars from its own stock; the revenue line is the car price.',
    what_it_does='buys used cars, refurbishes them and sells them from owned inventory with delivery to the door, keeping the full sale price')
tag(company_key='moove', company_name='Moove', archetype='Owned-Inventory Retail', archetype_secondary='Lending & Credit', industry='Logistics & Mobility',
    function='Operations', buyer='CONSUMER', gtm_motion='CHANNEL', revenue_model='SUBSCRIPTION_CONSUMER', product_role='DESTINATION', ai_stance='AI_NEUTRAL',
    product_tags='Car Subscription|Owned Vehicle Fleet|Drive To Own|Vehicle Financing|Gig Drivers|EV Fleet|Fleet Operations|Robotaxi Fleet',
    tags_as_of='2026-08', screening_category_as_supplied='Owned-Inventory Retail', taxonomy_note=TAGNOTE + ' Owns the fleet and collects weekly payments from drivers, so an owned-fleet subscription business with a financing element; sold through Uber and delivery platforms (CHANNEL). Kovi and Tokyo Taxi acquired before the 2026 round.',
    what_it_does='buys vehicles and places them with ride-hail and delivery drivers on weekly all-in payments that end in ownership, running the fleet itself')
tag(company_key='e2open', company_name='E2open', archetype='Commerce Enablement & Fulfilment', archetype_secondary='Business Applications', industry='Horizontal',
    function='Supply Chain', buyer='ENTERPRISE', gtm_motion='ENT_SALES', revenue_model='SEATS', product_role='SOR', ai_stance='AI_EMBEDDED',
    product_tags='Supply Chain Planning|Supplier Management|Demand Planning|Logistics Visibility|Trade Compliance|Supply Chain Network|Inventory Optimisation|Procurement',
    tags_as_of='2025-05', status_today='Acquired by WiseTech Global, completed 3-Aug-2025; no longer an independent listed comparable.',
    screening_category_as_supplied='Commerce Enablement & Fulfilment', taxonomy_note=TAGNOTE + ' M&A control-transaction row of a formerly listed company; subscription software, not a fulfilment operator.',
    what_it_does='connects manufacturers, suppliers and carriers on one planning and execution network, sold as multi-year enterprise subscriptions')
tag(company_key='berkshire-grey', company_name='Berkshire Grey', archetype='Commerce Enablement & Fulfilment', archetype_secondary='Design & Engineering', industry='Horizontal',
    function='Operations', buyer='ENTERPRISE', gtm_motion='ENT_SALES', revenue_model='PRODUCT_SALES', product_role='INFRA_LAYER', ai_stance='AI_NATIVE',
    product_tags='Warehouse Robotics|Fulfilment Automation|Material Handling|Robotic Picking|Robots As A Service|Order Fulfilment|Sortation|Robotic Labour',
    tags_as_of='2023-03', status_today='Taken private by SoftBank Group in 2023.', screening_category_as_supplied='Commerce Enablement & Fulfilment',
    taxonomy_note=TAGNOTE + ' Sells robotic systems (product revenue) with a RaaS option; M&A control-transaction row of a formerly listed company.',
    what_it_does='builds and installs AI-driven picking and sortation robots in warehouses, selling the systems and offering them as a service')
tag(company_key='restaurant365', company_name='Restaurant365', archetype='Vertical Software', archetype_secondary='Business Applications', industry='Hospitality',
    function='Operations', buyer='SMB', gtm_motion='MIDMARKET', revenue_model='SEATS', product_role='SOR', ai_stance='AI_EMBEDDED',
    product_tags='Restaurant Back Office|Restaurant Accounting|Inventory And Ordering|Food Cost Management|Vendor Invoice Automation|Scheduling|Payroll|Restaurant Operations',
    tags_as_of='2023-05', screening_category_as_supplied='Vertical Software', taxonomy_note=TAGNOTE,
    what_it_does='runs the accounting, inventory, scheduling and payroll of restaurant groups in one system, sold per location on subscription')
tag(company_key='owner', company_name='Owner', archetype='Vertical Software', archetype_secondary='Marketing & Customer Engagement', industry='Hospitality',
    function='Marketing', buyer='SMB', gtm_motion='MIDMARKET', revenue_model='SEATS', product_role='PLATFORM_SUITE', ai_stance='AI_NATIVE',
    product_tags='Restaurant Websites|Online Ordering|Restaurant Marketing|Loyalty|Restaurant Operations|Local Business Software|AI Marketing Agent|Direct Ordering',
    tags_as_of='2026-08', screening_category_as_supplied='Vertical Software', taxonomy_note=TAGNOTE + ' Front of house: website, ordering and marketing for independents, on a flat subscription.',
    what_it_does='builds and runs the website, online ordering and marketing of independent restaurants, sold as a monthly subscription')
tag(company_key='auditboard', company_name='AuditBoard', archetype='Vertical Software', archetype_secondary='Business Applications', industry='Horizontal',
    function='Legal & Compliance', buyer='LOB', gtm_motion='ENT_SALES', revenue_model='SEATS', product_role='SOR', ai_stance='AI_EMBEDDED',
    product_tags='Compliance Workflow|Audit Management|Risk Management|Regulatory Compliance|Controls Management|ESG Reporting|GRC|Compliance Automation',
    tags_as_of='2024-05', status_today='Acquired by Hg in 2024; renamed Optro in 2026.', screening_category_as_supplied='Vertical Software',
    taxonomy_note=TAGNOTE + ' Compliance and audit workflow for regulated functions; M&A control-transaction row.',
    what_it_does='runs audit, risk and compliance programmes for corporate compliance teams, sold per user to the finance and risk function')
tag(company_key='legora', company_name='Legora', archetype='Vertical Software', archetype_secondary='Data, AI & Developer Tools', industry='Legal & Professional Services',
    function='Legal & Compliance', buyer='LOB', gtm_motion='ENT_SALES', revenue_model='SEATS', product_role='PLATFORM_SUITE', ai_stance='AI_NATIVE',
    product_tags='Legal AI|Contract Review|Legal Research|Drafting Assistant|Document Review|Agentic Workflows|In-House Legal|Law Firm Software',
    tags_as_of='2026-04', screening_category_as_supplied='Vertical Software', taxonomy_note=TAGNOTE + ' The same category as Harvey.',
    what_it_does='agentic AI workspace for law firms and in-house teams that reviews, researches and drafts, licensed per lawyer')
tag(company_key='applied-intuition', company_name='Applied Intuition', archetype='Design & Engineering', archetype_secondary='Data, AI & Developer Tools', industry='Horizontal',
    function='Engineering & Design', buyer='ENT_IT', gtm_motion='ENT_SALES', revenue_model='SEATS', product_role='PLATFORM_SUITE', ai_stance='AI_NATIVE',
    product_tags='Simulation And Test|Autonomy Software|Vehicle Intelligence|Robotics Development Platform|Embedded Deployment|Validation Tooling|Sensor Simulation|Defense Autonomy',
    tags_as_of='2025-06', screening_category_as_supplied='Design & Engineering', taxonomy_note=TAGNOTE + ' Sells simulation and autonomy tooling to vehicle makers and defence; enterprise contracts, not self-serve.',
    what_it_does='sells the simulation, validation and autonomy software that vehicle and machine makers use to develop and test self-driving systems, on enterprise contracts')
tag(company_key='vention', company_name='Vention', archetype='Design & Engineering', archetype_secondary='Commerce Enablement & Fulfilment', industry='Horizontal',
    function='Engineering & Design', buyer='LOB', gtm_motion='PLG', revenue_model='PRODUCT_SALES', product_role='PLATFORM_SUITE', ai_stance='AI_EMBEDDED',
    product_tags='Robotics Development Platform|Automation Design|Robot Programming|Robot Fleet Tooling|Industrial Automation|Cobots|Manufacturing Automation|Hardware Marketplace',
    tags_as_of='2026-01', screening_category_as_supplied='Design & Engineering', taxonomy_note=TAGNOTE + ' Most revenue is hardware ordered through the design platform, so PRODUCT_SALES rather than SEATS.',
    what_it_does='browser platform where manufacturers design, program and order automation cells and robots, earning mainly on the hardware shipped')
tag(company_key='suno', company_name='Suno', archetype='Consumer & Prosumer Software', archetype_secondary='Streaming & Digital Media', industry='Media & Gaming',
    function='Content & Community', buyer='CONSUMER', gtm_motion='PLG', revenue_model='SUBSCRIPTION_CONSUMER', product_role='TOOL', ai_stance='AI_NATIVE',
    product_tags='AI Music Generation|Consumer AI|Creative Tools|Audio Generation|Consumer Subscription|Generative Media|Prosumer Creator Tools|Music App',
    tags_as_of='2026-06', screening_category_as_supplied='Consumer & Prosumer Software', taxonomy_note=TAGNOTE,
    what_it_does='generates full songs from a text prompt for consumers and creators, sold as a monthly subscription with a free tier')
tag(company_key='framer', company_name='Framer', archetype='Consumer & Prosumer Software', archetype_secondary='Design & Engineering', industry='Horizontal',
    function='Productivity', buyer='PROSUMER', gtm_motion='PLG', revenue_model='SEATS', product_role='TOOL', ai_stance='AI_EMBEDDED',
    product_tags='No Code Website Builder|Web Design|Site Hosting|Design Tool|Prosumer Subscription|AI Website Generation|Templates|Desktop Productivity',
    tags_as_of='2025-08', screening_category_as_supplied='Consumer & Prosumer Software', taxonomy_note=TAGNOTE,
    what_it_does='no-code website design and hosting tool for designers and small businesses, sold per site and per editor seat on subscription')
tag(company_key='genspark', company_name='Genspark', archetype='Consumer & Prosumer Software', archetype_secondary='Data, AI & Developer Tools', industry='Horizontal',
    function='Productivity', buyer='PROSUMER', gtm_motion='PLG', revenue_model='SUBSCRIPTION_CONSUMER', product_role='TOOL', ai_stance='AI_NATIVE',
    product_tags='AI Agent Workspace|Consumer AI|AI Search|Slides And Documents|Task Automation|Prosumer Subscription|Personal Productivity|Super Agent',
    tags_as_of='2025-11', screening_category_as_supplied='Consumer & Prosumer Software', taxonomy_note=TAGNOTE,
    what_it_does='general-purpose AI agent workspace that searches, drafts and runs tasks for knowledge workers, sold as a personal subscription')
tag(company_key='mercor', company_name='Mercor', archetype='Freelance & Services Marketplace', archetype_secondary='Data, AI & Developer Tools', industry='Horizontal',
    function='HR & Workforce', buyer='ENTERPRISE', gtm_motion='ENT_SALES', revenue_model='TAKE_RATE', product_role='AGGREGATOR', ai_stance='AI_NATIVE',
    product_tags='Talent Matching|Candidate Matching|AI Interviews|Applicant Screening|Hiring Marketplace|Expert Labour Marketplace|Recruiter Agents|AI Training Data',
    tags_as_of='2025-10', screening_category_as_supplied='Freelance & Services Marketplace', taxonomy_note=TAGNOTE + ' Revenue is gross of contractor pay, the staffing shape; demand is concentrated in AI labs.',
    what_it_does='screens experts with an AI interview and places them with AI labs and enterprises on hourly contracts, keeping a finder fee on every hour billed')
tag(company_key='micro1', company_name='Micro1', archetype='Freelance & Services Marketplace', archetype_secondary='Data, AI & Developer Tools', industry='Horizontal',
    function='HR & Workforce', buyer='ENTERPRISE', gtm_motion='ENT_SALES', revenue_model='TAKE_RATE', product_role='AGGREGATOR', ai_stance='AI_NATIVE',
    product_tags='AI Recruiter|Applicant Screening|Candidate Matching|Recruiting Automation|Talent Marketplace|Contractor Management|AI Training Data|Interview Automation',
    tags_as_of='2025-09', screening_category_as_supplied='Freelance & Services Marketplace', taxonomy_note=TAGNOTE + ' Same shape as Mercor: AI recruiter in front, managed contractor supply behind, gross billings.',
    what_it_does='AI recruiter that interviews and vets applicants, then supplies and manages the contractors for AI labs, billing the client and paying the worker')


tag(company_key='sapiens', company_name='Sapiens International', archetype='Vertical Software', archetype_secondary='Insurance Technology', industry='Financial Services',
    function='Operations', buyer='ENTERPRISE', gtm_motion='ENT_SALES', revenue_model='PLATFORM', product_role='SOR', ai_stance='AI_EMBEDDED',
    product_tags='Insurance Software|Policy Administration|Claims Management|Billing|Core Insurance Platform|Property And Casualty|Life And Pensions|Insurance Decisioning',
    tags_as_of='2025-08', status_today='Taken private by Advent International; SPNS delisted.', screening_category_as_supplied='Insurance Technology',
    taxonomy_note=TAGNOTE + ' Core systems sold to insurance carriers with a large implementation-services line, so PLATFORM rather than SEATS. M&A control-transaction row of a formerly listed company.',
    what_it_does='sells the policy, billing and claims systems that insurance carriers run on, as subscriptions and licences with implementation services')
tag(company_key='accolade', company_name='Accolade', archetype='Vertical Software', archetype_secondary='Insurance Technology', industry='Healthcare & Life Sciences',
    function='Customer Service', buyer='ENTERPRISE', gtm_motion='ENT_SALES', revenue_model='PLATFORM', product_role='PLATFORM_SUITE', ai_stance='AI_EMBEDDED',
    product_tags='Care Navigation|Health Advocacy|Payer Decisioning|Benefits Navigation|Virtual Primary Care|Utilisation Management|Claims Communication|Care Coordination',
    tags_as_of='2025-01', status_today='Acquired by Transcarent, completed April 2025; ACCD delisted.', screening_category_as_supplied='Insurance Technology',
    taxonomy_note=TAGNOTE + ' Per-member access fees from employers and health plans plus usage fees, so PLATFORM. M&A control-transaction row of a formerly listed company.',
    what_it_does='guides employees and plan members through care and benefits on behalf of employers and health plans, paid per member per month plus usage fees')
tag(company_key='udemy', company_name='Udemy', archetype='Online Learning', archetype_secondary='Third-Party Marketplace', industry='Education',
    function='Content & Community', buyer='CONSUMER', gtm_motion='PLG', revenue_model='TAKE_RATE', product_role='AGGREGATOR', ai_stance='AI_EMBEDDED',
    product_tags='Online Courses|Course Marketplace|Self Paced Learning|Skills Learning|Consumer Learning|Corporate Learning|Creator Led Education|Learning Subscription',
    tags_as_of='2025-12', status_today='Merged into Coursera, all-stock; UDMY delisted.', screening_category_as_supplied='Online Learning',
    taxonomy_note=TAGNOTE + ' Consumer course marketplace with an enterprise subscription (Udemy Business) that had grown to about half of revenue. M&A control-transaction row of a formerly listed company.',
    what_it_does='marketplace of instructor-made courses sold to individual learners, plus a business subscription to the same catalogue, sharing revenue with instructors')

# ---------------------------------------------------------------- write
os.makedirs('data/raw', exist_ok=True)
out = 'data/raw/2026-09-05_private-rounds-claude.csv'
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=ROUND_HDR, lineterminator='\n')
    w.writeheader(); w.writerows(rows)
out2 = 'data/raw/2026-09-05_private-companies-tags-claude.csv'
with open(out2, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=TAG_HDR, lineterminator='\n')
    w.writeheader(); w.writerows(tags)
keys = {r['company_key'] for r in rows}
assert keys == {t['company_key'] for t in tags}, keys ^ {t['company_key'] for t in tags}
print('%d rounds, %d companies, %d tag rows -> %s, %s' % (len(rows), len(keys), len(tags), out, out2))
for r in rows:
    print('  %-28s %-8s post %9s rev %8s x %6s bound %-2s med %s' % (r['transaction_id'], r['transaction_type'], r['post_money_musd'], r['revenue_musd'], r['ev_revenue_x'], r['bound'], r['in_medians']))
