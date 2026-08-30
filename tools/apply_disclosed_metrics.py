# -*- coding: utf-8 -*-
"""Write company-disclosed recurring revenue and retention into the software peer file.

    python3 tools/apply_disclosed_metrics.py

THE RULE THIS FILE ENFORCES. Daniil, 30-Aug-2026: recurring revenue and retention go in "only if
disclosed by the company itself". Every figure below came from an SEC filing, an annual report, a
company earnings release, a company investor presentation or a company earnings call. Nothing here
comes from an analyst, an estimate or a third-party database. Five independent research passes
produced it, each instructed to return an empty answer rather than a plausible one.

TWO STATUSES, AND THE DIFFERENCE MATTERS.
  DISCLOSED   the company stated the percentage itself, in its own words.
  CALCULATED  the company disclosed the numerator and the denominator as separate line items and
              the division is ours. Arithmetic on two disclosed figures, not an estimate, but it is
              not the company's own headline number and is marked so a reviewer can tell.

WHAT WAS DELIBERATELY LEFT OUT, because a number that means something else is worse than no number:
  Autodesk        discloses NRR only as a range, "100 to 110 percent". No point figure exists.
  Zscaler, NICE   both plainly still report a retention metric, but the value sits inside a chart
                  image that could not be read. Blank rather than guessed. WORTH PULLING BY HAND.
  GoDaddy         "customer retention rate" of 85% is a customer COUNT metric, not dollar-based.
                  It is not NRR or GRR and does not belong in the same column.
  PSI Software    publishes a "Customer-Loyalty-Index" of 91%. That is a self-defined
                  reference-willingness score, not revenue retention.
  Pinewood        publishes net customer churn, which is not a retention rate.
  Consensus Cloud 67% is recurring as a share of SUBSCRIPTION revenue, not of total revenue.
  Amdocs          "managed services revenue", 66%, is a category Amdocs does not itself call
                  recurring or subscription.
  Pegasystems     says NRR improved "about 150 basis points" and never gives the level.
  Fortinet        the product/service split is not labelled recurring by Fortinet, and service
                  revenue mixes subscription with non-recurring support.

SCOPE IS RECORDED WHERE IT IS NOT THE WHOLE COMPANY. A retention rate for one segment is not a
company retention rate and must not be read as one: Commvault's 122% covers SaaS ARR only, roughly
a third of its book; BlackBerry's 94% is Secure Communications only; Agora's 109% is the non-China
segment; GB Group's 101.1% covers Identity and Location but not Fraud; Appian's is cloud
subscriptions only. Dassault's 82% recurring is a share of SOFTWARE revenue, not total revenue.
"""
import csv, io, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(HERE, 'data', 'peers-software.csv')

NEW_COLS = ['recurring_revenue_pct', 'recurring_term', 'recurring_period', 'recurring_source',
            'recurring_status', 'recurring_scope', 'nrr_type']

# ticker: (recurring_pct, term, period, source, status, scope)
REC = {
 'ENXTPA:74SW': (75, 'Recurring revenue', 'Q1 2026', 'Q1 2026 revenue release', 'CALCULATED', 'Company states 90.9% of PRODUCT revenue; 75% is against total group revenue'),
 'NASDAQGS:ACIW': (68.8, 'Recurring revenue', 'FY2025', 'FY2025 earnings release', 'CALCULATED', ''),
 'OM:ANOD B': (63, 'Recurring revenue', 'FY2025', 'Annual Report 2025', 'DISCLOSED', ''),
 'NASDAQGS:AGYS': (64.5, 'Recurring revenue, subscription and maintenance', 'FY2026', 'FY2026 earnings release', 'DISCLOSED', ''),
 'NASDAQGS:ALRM': (67.2, 'SaaS and license revenue', 'FY2024', 'FY2024 earnings release', 'CALCULATED', ''),
 'LSE:ALFA': (33.9, 'Subscription revenue', 'H1 2025', '2025 Half Year Report', 'CALCULATED', ''),
 'NASDAQGM:APPN': (79.5, 'Subscriptions revenue', 'FY2024', 'FY2024 earnings release', 'CALCULATED', ''),
 'XTRA:AOF': (69, 'Recurring revenue', '9M 2025', 'Investor roadshow presentation, Nov-2025', 'DISCLOSED', ''),
 'NASDAQGS:ADSK': (97, 'Recurring revenue', 'FY2025', 'FY2025 earnings release', 'DISCLOSED', ''),
 'NASDAQGS:AVPT': (76.1, 'SaaS revenue', 'FY2025', 'FY2025 earnings release', 'CALCULATED', ''),
 'NASDAQGS:BSY': (92, 'Subscription revenue', 'Q3 2025', 'Q3 2025 earnings release', 'DISCLOSED', ''),
 'NASDAQGS:BLKB': (98.0, 'GAAP recurring revenue', 'FY2025', 'FY2025 results', 'DISCLOSED', ''),
 'TSX:BB': (80, 'Recurring Software Product Revenue Percentage', 'Q3 FY2025', 'Q3 FY2025 earnings release', 'DISCLOSED', 'LAST DISCLOSED, appears discontinued after the 2024 restructuring'),
 'NYSE:AI': (91, 'Subscription revenue', 'FY2026', 'FY2026 earnings release', 'DISCLOSED', ''),
 'AIM:CER': (35, 'Recurring revenue', 'FY2025', 'Annual Report 2025', 'DISCLOSED', ''),
 'NASDAQGS:CVLT': (64.9, 'Subscription revenue', 'FY2026', 'Q4 FY2026 earnings release', 'CALCULATED', ''),
 'TSX:CSU': (76.8, 'Maintenance and other recurring revenue', 'Q1 2026', 'Q1 2026 MD&A', 'CALCULATED', 'Q1 is seasonally the strongest quarter'),
 'NASDAQGS:CRWD': (95.2, 'Subscription revenue', 'H1 FY2027', 'Q2 FY2027 earnings release', 'CALCULATED', ''),
 'TSX:ENGH': (69.2, 'Recurring revenue, SaaS and maintenance', 'Q4 FY2025', 'Q4 FY2025 results release', 'DISCLOSED', ''),
 'ASX:FCL': (57.8, 'Subscription revenue', 'H1 FY2026', 'H1 FY2026 ASX results announcement', 'DISCLOSED', ''),
 'NYSE:GWRE': (66.2, 'Subscription and support revenue', '9M FY2026', 'Q3 FY2026 earnings release', 'CALCULATED', ''),
 'NASDAQGS:IIIV': (80, 'Recurring revenue', 'H1 FY2026', 'Q2 FY2026 investor materials', 'DISCLOSED', ''),
 'XTRA:IOS': (80, 'Recurring revenues', 'FY2023', 'Investor presentation, Jan-2025', 'DISCLOSED', 'STALE: FY2023 data, not refreshed since'),
 'TSX:KXS': (62.1, 'SaaS revenue', 'Q1 2026', 'Q1 2026 earnings release', 'CALCULATED', 'FY2025 full year was about 66%'),
 'ENXTPA:LSS': (75, 'Recurring revenues', 'FY2025', 'FY2025 results release', 'DISCLOSED', ''),
 'ASX:360': (75.4, 'Subscription revenue', 'FY2025', 'FY2025 earnings release', 'CALCULATED', ''),
 'TSX:LSPD': (30.2, 'Subscription revenue', 'FY2026', 'Q4 FY2026 earnings release', 'CALCULATED', 'Low because most revenue is transaction and payments, not a weak subscription book'),
 'NYSE:RAMP': (75.5, 'Subscription revenue', 'FY2026', 'Q4 FY2026 earnings release', 'CALCULATED', ''),
 'TSXV:LMN': (72.5, 'Maintenance and other recurring revenue', 'FY2024', 'FY2024 annual financial statements', 'CALCULATED', ''),
 'NASDAQGS:MANH': (37.7, 'Cloud subscriptions', 'FY2025', 'FY2025 earnings release', 'CALCULATED', 'Excludes maintenance revenue, also recurring, which Manhattan never combines into one figure'),
 'NASDAQCM:MITK': (48.5, 'SaaS revenue', 'Q3 FY2026', 'Q3 FY2026 earnings release', 'CALCULATED', ''),
 'NYSE:NABL': (99, 'Subscription revenue', 'FY2025', 'FY2025 earnings release', 'CALCULATED', ''),
 'NASDAQGS:NCNO': (87.9, 'Subscription revenues', 'FY2026', 'Q4 FY2026 earnings release', 'CALCULATED', ''),
 'XTRA:NEM': (92.2, 'Recurring revenues', 'FY2025', 'Annual Report 2025', 'DISCLOSED', 'Up from 86.5% in FY2024 on the subscription transition'),
 'NASDAQGS:NTNX': (95, 'Subscription revenue', 'FY2026', 'Q4 FY2026 earnings release', 'CALCULATED', ''),
 'NASDAQGS:OKTA': (97.8, 'Subscription revenue', 'FY2026', 'Q4 FY2026 earnings release', 'CALCULATED', ''),
 'NASDAQCM:OSPN': (64, 'Subscription revenue', 'FY2025', 'FY2025 earnings release', 'CALCULATED', ''),
 'NYSE:OOMA': (92, 'Subscription and services revenue', 'FY2026', 'Q4 FY2026 earnings release', 'DISCLOSED', ''),
 'NASDAQGS:OTEX': (78.3, 'Annual Recurring Revenues as % of Rev', 'Q4 FY2026', 'Q4 FY2026 investor presentation', 'DISCLOSED', ''),
 'NASDAQGS:PANW': (80, 'Subscription and support revenue', 'FY2025', 'FY2025 earnings release', 'CALCULATED', ''),
 'NYSE:PAR': (63.3, 'Subscription service revenue', 'Q1 2026', 'Q1 2026 earnings release', 'CALCULATED', ''),
 'NASDAQGS:PEGA': (57.9, 'Subscription services revenue', 'FY2025', 'FY2025 earnings release', 'CALCULATED', ''),
 'LSE:PINE': (83.2, 'Recurring revenue', 'FY2025', 'FY25 results presentation', 'DISCLOSED', 'FY24 comparator was an 11-month stub, so the fall from 86.5% is partly a period effect'),
 'ENXTPA:PLNW': (91, 'Recurring revenue', 'FY2025', 'FY2025 results release', 'DISCLOSED', ''),
 'XTRA:PSAN': (39.3, 'Annually recurring revenue', 'FY2025', 'Annual Report 2025', 'DISCLOSED', ''),
 'NASDAQGS:PTC': (95, 'Recurring', 'FY2025', 'FY2025 10-K', 'DISCLOSED', ''),
 'NASDAQGM:RPD': (96, 'Recurring revenue', 'FY2025', 'FY2025 10-K', 'DISCLOSED', ''),
 'NASDAQCM:RDVT': (77, 'Contractual revenue', 'Q2 2026', 'Q2 2026 earnings release', 'DISCLOSED', 'Red Violet own coinage: customers on a monthly fee plus overage. Not a standard subscription definition'),
 'NASDAQGS:SAIL': (94, 'Subscription revenue', 'Q1 FY2027', 'Q1 FY2027 earnings release', 'CALCULATED', ''),
 'NYSE:CRM': (95, 'Subscription and support revenue', 'Q2 FY2027', 'Q2 FY2027 earnings release', 'CALCULATED', ''),
 'XTRA:SAP': (63.6, 'Cloud revenue', 'Q2 2026', 'Q2 2026 quarterly statement', 'CALCULATED', 'Cloud only. Adding software support, also recurring, takes it to about 88%. SAP never labels a figure recurring'),
 'ENXTPA:ALBFR': (87, 'SaaS subscriptions', 'FY2025', 'FY2025 statutory report', 'DISCLOSED', ''),
 'NASDAQGS:SPSC': (96, 'Recurring revenues', 'FY2025', 'FY2025 10-K', 'DISCLOSED', ''),
 'NASDAQGS:SNPS': (78, 'Recurring Revenue as % of Total Revenue', 'FY2025', 'Q4 FY2025 financial supplement', 'DISCLOSED', ''),
 'LSE:SGE': (97, 'Recurring revenue', 'FY2025', 'FY2025 Annual Report', 'DISCLOSED', 'Subscription penetration specifically was 83%'),
 'OM:TRUE B': (45, 'Recurring revenues', 'FY2025', 'Year-end 2025 report', 'DISCLOSED', ''),
 'NYSE:TYL': (87.1, 'Recurring revenues', 'FY2025', 'Q4 2025 earnings release', 'DISCLOSED', ''),
 'NASDAQGS:VRNS': (91.8, 'SaaS plus term license subscription revenues', 'FY2025', 'FY2025 earnings release', 'CALCULATED', ''),
 'NASDAQGM:VERX': (85.5, 'Software subscription revenues', 'FY2025', 'FY2025 earnings release', 'CALCULATED', ''),
 'NASDAQGS:ZS': (98, 'Subscription and support revenue', 'Q1 FY2026', 'Q1 FY2026 10-Q', 'DISCLOSED', ''),
 'NYSE:VEEV': (84.0, 'Subscription revenues', 'FY2026', 'Q4 FY2026 earnings release', 'DISCLOSED', ''),
 'NASDAQGS:CHKP': (48.4, 'Security Subscriptions Revenues', 'Q1 2026', 'Q1 2026 results', 'CALCULATED', 'Subscriptions only. Software updates and maintenance, a further 35.1% and also recurring, is excluded. Check Point never uses the word recurring'),
 'NASDAQGS:NICE': (89, 'Recurring Revenue', 'FY2025', 'Q1 2026 investor presentation', 'DISCLOSED', ''),
 'ENXTPA:DSY': (82, 'Recurring revenue', 'FY2025', 'FY2025 results release', 'DISCLOSED', 'DENOMINATOR IS SOFTWARE REVENUE, NOT TOTAL REVENUE. Overstates the share of total'),
 'NASDAQGS:WIX': (71, 'Creative Subscriptions Revenue', 'FY2025', 'FY2025 6-K earnings release', 'CALCULATED', ''),
 'NASDAQGM:AIP': (90.5, 'Licensing, support and maintenance revenue', 'FY2025', 'FY2025 earnings release', 'CALCULATED', 'Remainder is variable royalties'),
 'XTRA:IVU': (48, 'Recurring sales', 'FY2025', 'Annual Report 2025', 'DISCLOSED', ''),
 'NASDAQGM:RMNI': (95.6, 'Subscription revenue', 'Q4 2025', 'Q4 2025 earnings release', 'DISCLOSED', ''),
}

# ticker: (pct, type, label, period, source, scope)
RET = {
 'NASDAQGS:API': (109, 'NRR', 'Dollar-Based Net Retention Rate', 'TTM to 31-Dec-2025', 'FY2025 earnings release', 'Agora segment only; Shengwang China segment is 89%'),
 'LSE:ALFA': (112, 'NRR', 'NRR', 'H1 2025', '2025 Half Year Report', ''),
 'NASDAQCM:AMPL': (105, 'NRR', 'Dollar-based Net Retention Rate', 'as of 31-Dec-2025', 'FY2025 earnings release', 'TTM basis is 104%'),
 'NASDAQGM:APPN': (116, 'NRR', 'Cloud Subscription Revenue Retention Rate', 'as of 31-Dec-2024', 'FY2024 earnings release', 'CLOUD SUBSCRIPTIONS ONLY, not total subscriptions'),
 'XTRA:AOF': (116, 'NRR', 'Net retention rate', 'Q3 2025', 'Investor roadshow presentation, Nov-2025', 'Excludes Crewmeister. Gross retention separately 96.1%'),
 'NASDAQGS:AVPT': (111, 'NRR', 'Dollar-based net retention rate', 'as of 31-Dec-2025', 'FY2025 earnings release', '110% FX-adjusted'),
 'NASDAQGS:BSY': (109, 'NRR', 'LTM recurring revenues dollar-based net retention rate', 'LTM to 31-Mar-2026', 'Q1 2026 earnings release', ''),
 'TSX:BB': (94, 'NRR', 'Dollar-Based Net Retention Rate', 'FY2026', 'Q4 FY2026 earnings slides', 'SECURE COMMUNICATIONS SEGMENT ONLY, no company-wide figure'),
 'NYSE:BOX': (102, 'NRR', 'net retention rate', 'Q4 FY2025', 'Q4 FY2025 prepared remarks', 'Last quantified figure. Q4 FY2026 describes improvement without a number'),
 'NASDAQGS:CCCS': (106, 'NRR', 'Net Dollar Retention', 'Q4 2025', 'Q4 2025 earnings call', 'Gross dollar retention separately 99%'),
 'NASDAQGS:CVLT': (122, 'NRR', 'SaaS net dollar retention rate', 'as of 31-Mar-2026', 'Q4 FY2026 earnings release', 'SAAS ARR ONLY, about $333m of $1,122m total ARR. Not a company retention rate'),
 'NASDAQGS:CRWD': (115, 'NRR', 'Dollar-based net retention rate', 'as of 31-Jan-2026', 'FY2026 10-K', ''),
 'NYSE:FIG': (136, 'NRR', 'Net Dollar Retention Rate', 'as of 30-Jun-2026', 'Q2 2026 earnings release', 'Paid customers above $10,000 ARR only. Was 139% in Q1 2026'),
 'NASDAQGS:FRSH': (104, 'NRR', 'net dollar retention rate', 'Q2 2026', 'Q2 2026 earnings release', 'Declining: 106% Q2 2025, 106% Q1 2026, 104% Q2 2026'),
 'LSE:GBG': (101.1, 'NRR', 'net revenue retention', 'FY25 to 31-Mar-2025', 'FY25 results', 'IDENTITY AND LOCATION DIVISIONS ONLY, excludes Fraud and the group'),
 'NYSE:RAMP': (107, 'NRR', 'Subscription net retention', 'FY2026', 'Q4 FY2026 earnings release', 'Platform net retention separately 108%'),
 'NYSE:NABL': (103, 'NRR', 'Dollar-based net revenue retention', 'TTM to Q4 2025', 'Q4 FY2025 earnings release', '102% constant currency'),
 'NASDAQGS:NCNO': (112, 'NRR', 'ACV Net Retention Rate', 'FY2026', 'Q4 FY2026 earnings release', ''),
 'NASDAQGS:NTSK': (118, 'NRR', 'dollar-based net retention rate', 'as of 31-Jul-2025', 'IPO prospectus, Sep-2025', 'Not restated in later releases'),
 'NASDAQGS:NTNX': (108, 'NRR', 'net dollar-based retention rate', 'as of 31-Jul-2025', 'Q4 FY2025 earnings call', 'Absent from the FY2026 release; possibly discontinued'),
 'NASDAQGS:OKTA': (107, 'NRR', 'net retention rate', 'Q4 FY2025', 'Q4 FY2025 earnings call', 'Not restated in the FY2026 release'),
 'NASDAQCM:OSPN': (104, 'NRR', 'Net Retention Rate', 'FY2025', 'FY2025 earnings release', ''),
 'NASDAQGS:OTEX': (94, 'NRR', 'Cloud Net Renewal Rate', 'FY2026', 'Q4 FY2026 investor presentation', 'Footnote confirms it captures expansion, so NRR not GRR. Customer support net renewal separately 93%'),
 'OB:PEXIP': (102, 'NRR', 'net retention', 'Q2 2026', 'Q2 2026 quarterly report', 'By segment: Secure and Custom 106%, Connected Spaces 99%'),
 'ENXTPA:PLNW': (110, 'NRR', 'Net Retention Rate', 'FY2025', 'FY2025 results release', 'Down from 117%. Planisware changed the calculation method in 2025, so the two years are not strictly like for like'),
 'NYSE:PCOR': (106, 'NRR', 'Net Revenue Retention', 'FY2025', 'FY2025 earnings release', 'Gross revenue retention separately disclosed at 95%'),
 'NASDAQGS:PRGS': (100, 'NRR', 'Net Retention', 'FY2025', 'FY2025 earnings release', ''),
 'NASDAQCM:RDVT': (95, 'GRR', 'Gross revenue retention', 'TTM Q2 2026', 'Q2 2026 earnings release', 'Excludes expansion revenue by definition. Excludes idiVERIFIED, under 3% of revenue'),
 'XTRA:TMV': (93, 'NRR', 'Net Retention Rate, constant currency', 'Q2 2026', 'Q2 2026 results release', 'Enterprise-only NRR separately 94%'),
 'LSE:SGE': (101, 'NRR', 'Renewal rate by value', 'FY2025', 'FY2025 Annual Report', 'Sage own term. Includes upsell and cross-sell of the existing base, so it behaves as NRR'),
 'NYSE:U': (106, 'NRR', 'dollar-based net expansion rate', 'Q2 2023', 'Q2 2023 shareholder letter', 'DISCONTINUED. Unity has not disclosed this since Q2 2023. Three years stale'),
 'NASDAQGM:VERX': (105, 'NRR', 'Net Revenue Retention', 'as of 31-Dec-2025', 'FY2025 earnings release', 'Gross revenue retention separately disclosed at 94%'),
 'NYSE:VIA': (120, 'NRR', 'Platform Net Revenue Retention Rate', 'FY2023 and FY2024', 'IPO prospectus, Sep-2025', 'A FLOOR: prospectus says averaged OVER 120%. Not repeated in the FY2025 10-K'),
 'NASDAQGM:RMNI': (88, 'NRR', 'Revenue Retention Rate', 'TTM to 31-Dec-2025', 'Q4 2025 earnings release', 'Rimini own term, not labelled NRR or GRR by the company. Classified NRR because the definition does not cap expansion'),
}


def main():
    lines = open(TARGET, encoding='utf-8').read().splitlines()
    head = [l for l in lines if l.lstrip('"').startswith('#')]
    body = '\n'.join(l for l in lines if not l.lstrip('"').startswith('#'))
    rd = csv.DictReader(io.StringIO(body))
    cols = list(rd.fieldnames)
    rows = list(rd)
    for c in NEW_COLS:
        if c not in cols:
            cols.append(c)

    by = {r['exchange_ticker']: r for r in rows}
    rec_hit = ret_hit = 0
    missing = []

    for t, (pct, term, period, src, status, scope) in REC.items():
        r = by.get(t)
        if r is None:
            missing.append(('recurring', t)); continue
        r['recurring_revenue_pct'] = pct
        r['recurring_term'] = term
        r['recurring_period'] = period
        r['recurring_source'] = src
        r['recurring_status'] = status
        r['recurring_scope'] = scope
        rec_hit += 1

    for t, (pct, typ, label, period, src, scope) in RET.items():
        r = by.get(t)
        if r is None:
            missing.append(('retention', t)); continue
        # never overwrite a retention figure already researched and stored
        if str(r.get('nrr_pct') or '').strip():
            continue
        r['nrr_pct'] = pct
        r['nrr_type'] = typ
        r['nrr_label'] = label
        r['nrr_period'] = period
        r['nrr_source'] = src
        r['nrr_scope'] = scope
        r['nrr_status'] = 'DISCLOSED'
        ret_hit += 1

    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=cols, lineterminator='\n', extrasaction='ignore')
    w.writeheader()
    for r in rows:
        w.writerow({c: r.get(c, '') for c in cols})
    open(TARGET, 'w', encoding='utf-8').write('\n'.join(head) + '\n' + out.getvalue())

    have_rec = sum(1 for r in rows if str(r.get('recurring_revenue_pct') or '').strip())
    have_ret = sum(1 for r in rows if str(r.get('nrr_pct') or '').strip())
    print('recurring written %d  | file now has %d of %d' % (rec_hit, have_rec, len(rows)))
    print('retention written %d  | file now has %d of %d' % (ret_hit, have_ret, len(rows)))
    if missing:
        print('\nTICKERS NOT IN THE FILE, nothing written for them:')
        for kind, t in missing:
            print('   %-10s %s' % (kind, t))
    return 0


if __name__ == '__main__':
    sys.exit(main())
