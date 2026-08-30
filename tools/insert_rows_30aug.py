# -*- coding: utf-8 -*-
"""Insert the nine re-verified private rounds, 30-Aug-2026.

These were verified in August, approved, and never written to the file. The session holding them was
compacted; they were reconstructed from research transcripts and then RE-CHECKED from scratch
against primary sources before being written here. Five of the original fourteen did not survive the
re-check and are deliberately absent: Loadsmart (no stated period at all), Getir (a Dutch sub-group
denominator divided into a global valuation), Gorillas (an unaudited run-rate asserted by the lead
investor), Jobandtalent (one journalist's paraphrase, gross billings inferred), Lalamove (primary
filing reached only through secondary reporting). See Fairway_verified_rows_30Aug.md.

Run once from the repo root:  python3 tools/insert_rows_30aug.py
It refuses to run twice.
"""
import csv, io, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROUNDS = os.path.join(HERE, 'data', 'private-rounds.csv')
TAGS = os.path.join(HERE, 'data', 'private-companies-tags.csv')

# ev_revenue_x is CARRIED, not computed, so that the file records the multiple that was verified
# rather than one produced by re-dividing rounded inputs.
ROWS = [
 dict(transaction_id='better-2021-05', company_key='better', company_name='Better.com',
      date='May-21', date_iso='2021-05', round_type='SPAC merger pricing',
      capital_raised_musd='', post_money_musd='7700.0', valuation_status='Disclosed',
      revenue_metric='Net revenue', revenue_musd='875.6', revenue_status='Filed (SEC EX-99.2)',
      ev_revenue_x='8.79', subsector_as_supplied='Digital mortgage origination',
      screening_category_as_supplied='Lending & Credit',
      lead_key_investors='Aurora Acquisition Corp; SoftBank Vision Fund 2; Activant',
      round_source_url='https://www.businesswire.com/news/home/20210511005602/en/',
      revenue_source_url='https://www.sec.gov/Archives/edgar/data/1835856/000110465921064244/tm2115798d1_ex99-2.htm',
      notes=('SEC-filed investor presentation, 11-May-2021: FY2020A revenue $875.6m. Businesswire the '
             'same day gives $7.7bn post-money and $6.9bn pre-money equity value, BOTH EXPLICITLY '
             'LABELLED, which is rare in this set. NOT the April-2021 SoftBank round at $6bn: no '
             'revenue figure with a stated period was public at that date, so that round is not '
             'priceable. An earlier working note of 6.85x used it and was withdrawn on 30-Aug-2026.'),
      transaction_type='PRIMARY', denominator_basis='DISCLOSED_EXACT', bound='',
      in_medians='1', verification='VERIFIED', revenue_basis='NET_REVENUE',
      revenue_period='FY2020', valuation_basis='REVENUE'),

 dict(transaction_id='marqeta-2020-05', company_key='marqeta', company_name='Marqeta',
      date='May-20', date_iso='2020-05', round_type='Private round',
      capital_raised_musd='150.0', post_money_musd='4300.0', valuation_status='Reported',
      revenue_metric='Net revenue', revenue_musd='143.3', revenue_status='Filed (SEC S-1)',
      ev_revenue_x='30.0', subsector_as_supplied='Card issuing and processing',
      screening_category_as_supplied='Merchant Acquiring & PSP',
      lead_key_investors='Undisclosed',
      round_source_url='https://www.businesswire.com/news/home/20200528005169/en/',
      revenue_source_url='https://www.sec.gov/Archives/edgar/data/1522540/000119312521162113/d64065ds1.htm',
      notes=('S-1, 14-May-2021, verbatim: "Our total net revenue was $143.3 million and $290.3 '
             'million for the years ended December 31, 2019 and 2020, respectively." AN EARLIER '
             'WORKING NOTE READ $290.3m AS FY2019 GROSS REVENUE. It is FY2020 net. The multiple is '
             'unchanged at 30.0x but the basis would have been recorded wrongly. FY2019 net revenue '
             'is 0.66% of FY2019 TPV of $21.7bn. Forbes on the pricing date said revenue "exceeded '
             '$300 million" in 2019, which would give <=14.3x, but the basis is undefined and no '
             'filing corroborates it. PRE or POST not specified by the release.'),
      transaction_type='PRIMARY', denominator_basis='DISCLOSED_EXACT', bound='',
      in_medians='1', verification='VERIFIED', revenue_basis='NET_REVENUE',
      revenue_period='FY2019', valuation_basis='REVENUE'),

 dict(transaction_id='dlocal-2021-04', company_key='dlocal', company_name='dLocal',
      date='Apr-21', date_iso='2021-04', round_type='Late-stage private round',
      capital_raised_musd='150.0', post_money_musd='5000.0', valuation_status='Reported',
      revenue_metric='Total revenues', revenue_musd='104.1', revenue_status='Filed (SEC F-1)',
      ev_revenue_x='48.0', subsector_as_supplied='Cross-border payments, emerging markets',
      screening_category_as_supplied='Cross-Border & FX',
      lead_key_investors='Alkeon Capital; BOND; D1 Capital; Tiger Global',
      round_source_url='https://techcrunch.com/2021/04/02/uruguayan-payments-startup-dlocal-quadruples-valuation-to-5b-with-150m-raise/',
      revenue_source_url='https://www.sec.gov/Archives/edgar/data/1846832/000095010321006779/dp150583_f1.htm',
      notes=('F-1 verbatim: "Our total revenues were US$104.1 million and US$55.3 million for 2020 '
             'and 2019." REVENUE IS NET OF VOLUME BUT GROSS OF PROCESSING COST. TPV $2.1bn in 2020, '
             'a 4.96% take rate; cost of services $44.1m sits below the line, so on gross profit of '
             '$60.1m the multiple is 83.2x. dLocal own release of 2-Apr-2021 confirms the $150m and '
             'states NO valuation; the $5bn is press-attributed. FY2020 accounts were not public at '
             'pricing but the period had closed, which the at-pricing rule admits.'),
      transaction_type='PRIMARY', denominator_basis='DISCLOSED_EXACT', bound='',
      in_medians='1', verification='VERIFIED', revenue_basis='NET_REVENUE',
      revenue_period='FY2020', valuation_basis='REVENUE'),

 dict(transaction_id='zepz-2021-08', company_key='zepz', company_name='Zepz',
      date='Aug-21', date_iso='2021-08', round_type='Primary financing round',
      capital_raised_musd='292.0', post_money_musd='5000.0', valuation_status='Disclosed',
      revenue_metric='Group revenue', revenue_musd='238.0', revenue_status='Reported (company release)',
      ev_revenue_x='21.0', subsector_as_supplied='Cross-border remittance',
      screening_category_as_supplied='Cross-Border & FX',
      lead_key_investors='Farallon Capital; LeapFrog Investments; Accel; TCV',
      round_source_url='https://www.businesswire.com/news/home/20210822005041/en/',
      revenue_source_url='https://www.prnewswire.com/news-releases/global-cross-border-payment-group-zepz-appoints-new-cfo-as-it-reaches-profitability-in-h1-22-301633640.html',
      notes=('TWO ZEPZ FIGURES EXIST FOR FY2020 AND ONLY ONE IS RIGHT. The round release, 22-Aug-2021, '
             'says brands "enabled $338m of revenues" in 2020: that is PRO-FORMA FOR SENDWAVE, which '
             'Zepz did not own until February 2021, so Sendwave contributed nothing to FY2020 group '
             'revenue. Zepz own later release, 27-Sep-2022, gives group revenue "$238M in 2020 to '
             '$399M in 2021". The $238m is the group figure and is what is stored. The $338m '
             'alternative would give 14.8x and is a perimeter error. Gross send volume of about '
             '$10bn is correctly excluded. PRE or POST not labelled.'),
      transaction_type='PRIMARY', denominator_basis='DISCLOSED_EXACT', bound='',
      in_medians='1', verification='VERIFIED', revenue_basis='NET_REVENUE',
      revenue_period='FY2020', valuation_basis='REVENUE'),

 dict(transaction_id='pinelabs-2021-05', company_key='pinelabs', company_name='Pine Labs',
      date='May-21', date_iso='2021-05', round_type='Private round, first close',
      capital_raised_musd='285.0', post_money_musd='3000.0', valuation_status='Reported',
      revenue_metric='Revenue from operations', revenue_musd='99.0',
      revenue_status='Filed accounts (MCA, via Inc42)',
      ev_revenue_x='30.3', subsector_as_supplied='Merchant commerce and payments',
      screening_category_as_supplied='Merchant Acquiring & PSP',
      lead_key_investors='Baron Capital; Duro; Marshall Wace; Moore Strategic Ventures',
      round_source_url='https://techcrunch.com/2021/05/16/merchant-commerce-platform-pine-labs-raises-285-million/',
      revenue_source_url='https://inc42.com/buzz/pine-labs-fy21-loss-widens-to-inr-248-cr-revenue-declines-14-percent-to-inr-726-cr/',
      notes=('Operating revenue Rs 726 Cr FY21, converted at about 73.3. NOTE THE DIRECTION: revenue '
             'FELL 14.2% from Rs 846 Cr in FY20, so this is a declining denominator, not a growing '
             'one. TPV is excluded; this is the fee line. The $3bn is press-attributed only: Pine '
             'Labs own release confirms the $285m first close and the investors and states no '
             'valuation, and Entrackr sources put it at $3.0bn to $3.2bn. Period closed 31-Mar-2021, '
             'six weeks before pricing, the cleanest staleness in the Indian set.'),
      transaction_type='PRIMARY', denominator_basis='DISCLOSED_EXACT', bound='',
      in_medians='1', verification='VERIFIED', revenue_basis='NET_REVENUE',
      revenue_period='FY2021_MAR', valuation_basis='REVENUE'),

 dict(transaction_id='razorpay-2021-12', company_key='razorpay', company_name='Razorpay',
      date='Dec-21', date_iso='2021-12', round_type='Series F',
      capital_raised_musd='375.0', post_money_musd='7500.0', valuation_status='Disclosed',
      revenue_metric='Revenue from operations', revenue_musd='110.9',
      revenue_status='Filed accounts (MCA, via Inc42)',
      ev_revenue_x='67.6', subsector_as_supplied='Payment aggregator and neobanking',
      screening_category_as_supplied='Merchant Acquiring & PSP',
      lead_key_investors='Lone Pine Capital; Alkeon Capital; TCV; Tiger Global; Sequoia India; GIC',
      round_source_url='https://razorpay.com/blog/razorpay-secures-375-million-in-series-f-funding/',
      revenue_source_url='https://inc42.com/buzz/razorpays-fy22-profit-rises-20-to-inr-7-3-cr-operating-revenue-nears-inr-1500-cr-mark/',
      notes=('Revenue from operations Rs 841.2 Cr FY21, converted at about 75.85. Total income was '
             'Rs 844.6 Cr and is correctly excluded. GROSS BASIS IS INFERRED FROM THE AGGREGATOR '
             'MODEL, NOT FROM A QUOTED LINE: Razorpay collects the full merchant discount rate and '
             'pays interchange, scheme and acquiring-bank cost as an expense, but no "payment gateway '
             'cost" line was retrieved. Treat the 67.6x as a gross-revenue multiple. Staleness 8.7 '
             'months. Razorpay own blog says valuation "increases to $7.5 billion" and never says '
             'post-money.'),
      transaction_type='PRIMARY', denominator_basis='DISCLOSED_EXACT', bound='',
      in_medians='0', verification='VERIFIED', revenue_basis='GROSS_REVENUE',
      revenue_period='FY2021_MAR', valuation_basis='REVENUE'),

 dict(transaction_id='delhivery-2021-05', company_key='delhivery', company_name='Delhivery',
      date='May-21', date_iso='2021-05', round_type='Series H, pre-IPO',
      capital_raised_musd='277.4', post_money_musd='3000.0', valuation_status='Reported',
      revenue_metric='Revenue from operations', revenue_musd='502.3',
      revenue_status='Filed (DRHP)',
      ev_revenue_x='5.97', subsector_as_supplied='Third-party logistics and parcel',
      screening_category_as_supplied='Local Delivery & On-Demand',
      lead_key_investors='Fidelity; Baillie Gifford; Chimera; Steadview Capital',
      round_source_url='https://entrackr.com/2021/05/exclusive-ipo-bound-delhivery-raises-277-mn-led-by-fidelity/',
      revenue_source_url='https://entrackr.com/2021/11/delhivery-files-drhp-to-raise-rs-7460-cr-via-ipo/',
      notes=('Revenue from operations Rs 3,646.5 Cr FY21 from the DRHP, converted at about 72.6. '
             'GROSS: line-haul and carrier cost sits inside the revenue line, inferred from the 3PL '
             'principal P&L structure rather than a quoted DRHP item. Round of Rs 2,008.62 Cr / '
             '$277.4m in Series H preference shares, 30-May-2021. The $3bn was press-attributed at '
             'the time (Entrackr noted no filing had disclosed it) and Business Today describes it '
             'as post-money. DRHP filed Nov-2021, after pricing, but the FY2021 period closed '
             '31-Mar-2021, before it.'),
      transaction_type='PRIMARY', denominator_basis='DISCLOSED_EXACT', bound='',
      in_medians='0', verification='VERIFIED', revenue_basis='GROSS_REVENUE',
      revenue_period='FY2021_MAR', valuation_basis='REVENUE'),

 dict(transaction_id='xpressbees-2022-02', company_key='xpressbees', company_name='Xpressbees',
      date='Feb-22', date_iso='2022-02', round_type='Series F',
      capital_raised_musd='300.0', post_money_musd='1200.0', valuation_status='Reported',
      revenue_metric='Revenue from operations', revenue_musd='134.3',
      revenue_status='Filed accounts (MCA, via Entrackr)',
      ev_revenue_x='8.94', subsector_as_supplied='E-commerce logistics and parcel',
      screening_category_as_supplied='Local Delivery & On-Demand',
      lead_key_investors='Blackstone Growth; TPG Growth; ChrysCapital; Investcorp; Norwest',
      round_source_url='https://entrackr.com/2022/02/xpressbees-enters-unicorn-club-after-300-mn-series-f-round/',
      revenue_source_url='https://entrackr.com/2022/03/logistics-firm-xpressbees-crosses-rs-1000-cr-in-revenue-during-fy21/',
      notes=('Revenue from operations Rs 1,004.8 Cr FY21, up 32.7% from Rs 757.2 Cr, converted at '
             'about 74.8. An earlier working note used Rs 1,019.8 Cr, which is TOTAL INCOME. THE '
             'STALEST ROW IN THIS BATCH: the period closed 31-Mar-2021 and the round priced '
             '9-Feb-2022, 10.3 months later, against a business growing about 80% a year, and '
             'Entrackr noted FY21 accounts were still unfiled at pricing. Admissible under the '
             'at-pricing rule because the period had closed, but the denominator is materially '
             'behind the valuation. GROSS: carrier cost inside the revenue line, inferred.'),
      transaction_type='PRIMARY', denominator_basis='DISCLOSED_EXACT', bound='',
      in_medians='0', verification='VERIFIED', revenue_basis='GROSS_REVENUE',
      revenue_period='FY2021_MAR', valuation_basis='REVENUE'),

 dict(transaction_id='shiprocket-2022-08', company_key='shiprocket', company_name='Shiprocket',
      date='Aug-22', date_iso='2022-08', round_type='Series E2 extension',
      capital_raised_musd='32.6', post_money_musd='1230.0', valuation_status='Reported',
      revenue_metric='Revenue from operations', revenue_musd='76.7',
      revenue_status='Filed accounts (MCA, via Inc42)',
      ev_revenue_x='16.03', subsector_as_supplied='E-commerce shipping aggregation',
      screening_category_as_supplied='Local Delivery & On-Demand',
      lead_key_investors='Temasek; Lightrock India; McKinley Capital; March Capital',
      round_source_url='https://yourstory.com/2022/08/funding-shiprocket-temasek-march-capital-unicorn',
      revenue_source_url='https://inc42.com/buzz/logistics-unicorn-shiprocket-slips-into-the-red-reports-loss-of-inr-93-1-cr-in-fy22/',
      notes=('Operating revenue Rs 611.1 Cr FY22, converted at about 79.7. Total income Rs 634.4 Cr '
             'correctly excluded. GROSS BASIS IS EVIDENCED HERE RATHER THAN INFERRED: cost of '
             'materials consumed was Rs 518.9 Cr against Rs 611.1 Cr of revenue, so 85% of the '
             'revenue line is bought courier capacity. VALUATION CONFLICT: Entrackr gives $1.23bn '
             'post-allotment, giving 16.0x; YourStory gives "nearly $1.3bn", giving 17.0x. The '
             'lower, more specific figure is stored.'),
      transaction_type='PRIMARY', denominator_basis='DISCLOSED_EXACT', bound='',
      in_medians='0', verification='VERIFIED', revenue_basis='GROSS_REVENUE',
      revenue_period='FY2022_MAR', valuation_basis='REVENUE'),
]

TAGS_ROWS = [
 dict(company_key='better', company_name='Better.com', archetype='Lending & Credit',
      archetype_secondary='Vertical Software', industry='Real Estate & Construction',
      function='Finance & Payments', buyer='CONSUMER', gtm_motion='PAID_ACQUISITION',
      revenue_model='TRANSACTION_FEE', product_role='PLATFORM_SUITE', ai_stance='AI_NEUTRAL',
      product_tags='Digital Mortgage|Mortgage Origination|Home Lending|Title Insurance|Real Estate Services|Consumer Lending',
      tags_as_of='2021-05', screening_category_as_supplied='Lending & Credit',
      what_it_does='originates residential mortgages directly to consumers through its own platform, holding the loans briefly before sale'),
 dict(company_key='marqeta', company_name='Marqeta', archetype='Merchant Acquiring & PSP',
      archetype_secondary='Commerce & Payments Software', industry='Horizontal',
      function='Finance & Payments', buyer='ENTERPRISE', gtm_motion='ENT_SALES',
      revenue_model='TAKE_RATE', product_role='INFRA_LAYER', ai_stance='AI_NEUTRAL',
      product_tags='Card Issuing|Payment Processing|Virtual Cards|Programmable Payments|Embedded Finance|Card Programs',
      tags_as_of='2020-05', screening_category_as_supplied='Merchant Acquiring & PSP',
      what_it_does='issues and processes payment cards for other companies through an API, taking a share of interchange'),
 dict(company_key='dlocal', company_name='dLocal', archetype='Cross-Border & FX',
      archetype_secondary='Merchant Acquiring & PSP', industry='Horizontal',
      function='Finance & Payments', buyer='ENTERPRISE', gtm_motion='ENT_SALES',
      revenue_model='TAKE_RATE', product_role='INFRA_LAYER', ai_stance='AI_NEUTRAL',
      product_tags='Cross-Border Payments|Emerging Markets|Local Payment Methods|Payins and Payouts|Payment Gateway|FX',
      tags_as_of='2021-04', screening_category_as_supplied='Cross-Border & FX',
      what_it_does='collects and pays out money in emerging markets for global merchants, on local rails'),
 dict(company_key='zepz', company_name='Zepz', archetype='Cross-Border & FX',
      archetype_secondary='', industry='Horizontal', function='Finance & Payments',
      buyer='CONSUMER', gtm_motion='PAID_ACQUISITION', revenue_model='TRANSACTION_FEE',
      product_role='DESTINATION', ai_stance='AI_NEUTRAL',
      product_tags='Remittance|Cross-Border Payments|Money Transfer|Mobile Money|Diaspora Payments|FX',
      tags_as_of='2021-08', screening_category_as_supplied='Cross-Border & FX',
      what_it_does='sends consumer remittances across borders through WorldRemit and Sendwave'),
 dict(company_key='pinelabs', company_name='Pine Labs', archetype='Merchant Acquiring & PSP',
      archetype_secondary='Commerce & Payments Software', industry='Retail & Commerce',
      function='Finance & Payments', buyer='SMB', gtm_motion='ENT_SALES',
      revenue_model='TAKE_RATE', product_role='PLATFORM_SUITE', ai_stance='AI_NEUTRAL',
      product_tags='Merchant Payments|Point of Sale|Card Terminals|Buy Now Pay Later|Gift Cards|Merchant Commerce',
      tags_as_of='2021-05', screening_category_as_supplied='Merchant Acquiring & PSP',
      what_it_does='runs in-store payment terminals and merchant commerce software across India and southeast Asia'),
 dict(company_key='razorpay', company_name='Razorpay', archetype='Merchant Acquiring & PSP',
      archetype_secondary='Commerce & Payments Software', industry='Horizontal',
      function='Finance & Payments', buyer='SMB', gtm_motion='PLG',
      revenue_model='TAKE_RATE', product_role='PLATFORM_SUITE', ai_stance='AI_NEUTRAL',
      product_tags='Payment Gateway|Payment Aggregator|Online Payments|Payouts|Neobanking|Merchant Payments',
      tags_as_of='2021-12', screening_category_as_supplied='Merchant Acquiring & PSP',
      what_it_does='accepts online payments for Indian merchants and runs their business banking alongside it'),
 dict(company_key='delhivery', company_name='Delhivery', archetype='Local Delivery & On-Demand',
      archetype_secondary='Commerce Enablement & Fulfilment', industry='Logistics & Mobility',
      function='Operations', buyer='ENTERPRISE', gtm_motion='ENT_SALES',
      revenue_model='TRANSACTION_FEE', product_role='INFRA_LAYER', ai_stance='AI_NEUTRAL',
      product_tags='Third-Party Logistics|Parcel Delivery|E-commerce Logistics|Warehousing|Freight|Last Mile',
      tags_as_of='2021-05', screening_category_as_supplied='Local Delivery & On-Demand',
      what_it_does='runs a national parcel, freight and warehousing network for Indian e-commerce, on its own assets'),
 dict(company_key='xpressbees', company_name='Xpressbees', archetype='Local Delivery & On-Demand',
      archetype_secondary='Commerce Enablement & Fulfilment', industry='Logistics & Mobility',
      function='Operations', buyer='ENTERPRISE', gtm_motion='ENT_SALES',
      revenue_model='TRANSACTION_FEE', product_role='INFRA_LAYER', ai_stance='AI_NEUTRAL',
      product_tags='E-commerce Logistics|Parcel Delivery|Last Mile|Third-Party Logistics|Cross-Border Shipping|Reverse Logistics',
      tags_as_of='2022-02', screening_category_as_supplied='Local Delivery & On-Demand',
      what_it_does='carries e-commerce parcels across India end to end, on its own delivery network'),
 dict(company_key='shiprocket', company_name='Shiprocket', archetype='Commerce Enablement & Fulfilment',
      archetype_secondary='Local Delivery & On-Demand', industry='Retail & Commerce',
      function='Operations', buyer='SMB', gtm_motion='PLG',
      revenue_model='TRANSACTION_FEE', product_role='AGGREGATOR', ai_stance='AI_NEUTRAL',
      product_tags='Shipping Aggregation|E-commerce Logistics|Courier Aggregator|Fulfilment|Last Mile|Seller Tools',
      tags_as_of='2022-08', screening_category_as_supplied='Commerce Enablement & Fulfilment',
      what_it_does='resells courier capacity to small Indian online sellers through one shipping dashboard'),
]


def load(path):
    lines = open(path, encoding='utf-8').read().splitlines(True)
    head = [l for l in lines if l.startswith('#')]
    body = ''.join(l for l in lines if not l.startswith('#'))
    rd = csv.DictReader(io.StringIO(body))
    return head, rd.fieldnames, list(rd)


def append(path, new, key):
    head, cols, rows = load(path)
    have = {r[key] for r in rows}
    fresh = [r for r in new if r[key] not in have]
    if not fresh:
        print('nothing to add to %s, all %d already present' % (os.path.basename(path), len(new)))
        return 0
    for r in fresh:
        unknown = set(r) - set(cols)
        assert not unknown, ('unknown column', unknown)
    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=cols, lineterminator='\n')
    w.writeheader()
    for r in rows + [{c: r.get(c, '') for c in cols} for r in fresh]:
        w.writerow(r)
    open(path, 'w', encoding='utf-8').write(''.join(head) + out.getvalue())
    print('added %d rows to %s (now %d)' % (len(fresh), os.path.basename(path), len(rows) + len(fresh)))
    return len(fresh)


if __name__ == '__main__':
    n = append(ROUNDS, ROWS, 'transaction_id')
    m = append(TAGS, TAGS_ROWS, 'company_key')
    print('\nrounds +%d, tags +%d' % (n, m))
    print('Now run: python3 selector/golden.py   and read the diff before writing new fixtures.')
