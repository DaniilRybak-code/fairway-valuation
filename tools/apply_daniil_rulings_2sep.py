#!/usr/bin/env python3
"""
Applies Daniil's rulings of 2 September 2026 and the two fixes he asked for.

  1. ALL-STOCK ACQUISITIONS PRICE AT ANNOUNCEMENT, not at closing. His words:
     "need to use the price of Doordash AT ANNOUNCEMENT. This is what the seller was
     pricing when he was setting the price." Wolt moves from the audited $2,838m to the
     announced $8,100m. Glovo has the same exposure and its note is updated.
  2. Gorillas: our number was already right; the sources it was missing are added.
  3. Perplexity Jan-24: stored as the range TechCrunch actually reported.
  4. Anthropic: the May-2023 row loses its multiple because no revenue figure existed at
     that pricing. Three later rounds are inserted, each with a run-rate Anthropic itself
     disclosed at or before the pricing date.

Run from the repo root:  python3 tools/apply_daniil_rulings_2sep.py
"""
import csv, io, sys

MAIN = 'data/private-rounds.csv'
CONS = 'data/private-rounds-consumer.csv'

EDITS = {
 MAIN: {
  ('Wolt', '2021-11'): {
    'fields': {
      'post_money_musd': '8100.0',
      'ev_revenue_x': '23.5',
      'valuation_status': 'Disclosed (announced)',
      'round_source_url': 'https://ir.doordash.com/news/news-details/2021/DoorDash-Joins-Forces-with-Wolt/default.aspx',
    },
    'note': ("REPRICED 02-Sep-2026 FROM THE AUDITED CLOSE TO THE ANNOUNCED PRICE, ON DANIIL'S RULING. "
             "His words: use the price of DoorDash at announcement, because that is what the seller was "
             "pricing when the price was set. DoorDash's release of 09-Nov-2021 says 'Transaction is "
             "valued at approximately EUR 7.0 billion', with DoorDash equity struck at $206.45 a share "
             "on a 30-day VWAP; the press USD figure is $8.1bn. Wolt's own release of 25-Jan-2021 gives "
             "revenue in DOLLARS, 'tripling our revenue to a preliminary $345 million', so numerator and "
             "denominator are both USD and 8100/345 gives 23.5x, was 8.2x. The audited number stays on "
             "the record and in this note: DoorDash's 10-Q for the quarter ended 30-Jun-2022 gives "
             "consideration of $2,842m, 36m shares at the 31-May-2022 close plus $133m of replacement "
             "awards, about $75 a share against the $206.45 used to size the deal. The 65% gap is "
             "DoorDash's share price falling between signing and closing, which is a fact about DoorDash, "
             "not about Wolt. THIS IS NOW A STANDING RULE FOR EVERY ALL-STOCK DEAL."),
  },
  ('Perplexity', '2024-01'): {
    'fields': {
      'revenue_metric': 'ARR (reported range, 5 to 10)',
      'revenue_musd': '10.0',
      'revenue_status': 'Reported range (TechCrunch, sources familiar)',
      'ev_revenue_x': '52.0',
      'ev_revenue_low_x': '52.0',
      'ev_revenue_high_x': '104.0',
      'bound': '>=',
      'revenue_period': 'RUN_RATE',
      'revenue_basis': 'ARR',
      'denominator_basis': 'REPORTED_RANGE',
      'revenue_source_url': 'https://techcrunch.com/2024/01/04/ai-powered-search-engine-perplexity-ai-now-valued-at-520m-raises-70m/',
    },
    'note': ("PRICED AS A RANGE 02-Sep-2026, PREVIOUSLY UNPRICED ON 'SOURCES CONFLICT'. The sources do not "
             "conflict, they give a range. TechCrunch of 04-Jan-2024, the day of the round: 'Sources "
             "familiar with the matter tell TechCrunch Perplexity's annual recurring revenue is between "
             "$5 million and $10 million at the moment.' 520 over 10 gives 52.0x and 520 over 5 gives "
             "104.0x, so the row is stored as 52.0x to 104.0x with the headline at the conservative end "
             "and bound '>=' because the true multiple is at least 52.0x. Daniil's database carries 104.0x, "
             "which takes the bottom of the range as if it were the figure while showing 10 in the revenue "
             "cell; it is the top of the range, not a point."),
  },
  ('Anthropic', '2023-05'): {
    'fields': {
      'revenue_metric': 'no revenue figure was public at pricing',
      'revenue_musd': '',
      'revenue_status': 'Not public at pricing',
      'ev_revenue_x': '',
      'revenue_period': '',
      'revenue_basis': 'NONE',
      'denominator_basis': 'NONE',
      'display_gate': 'RECORD_ONLY',
      'in_medians': '0',
    },
    'note': ("MULTIPLE WITHDRAWN 02-Sep-2026. This was priced on a denominator that did not exist at the "
             "time. Our $87m is Anthropic's own statement of 26-Sep-2025 describing the START of 2024, "
             "eight months after this round. Daniil's database carries $100m, which is The Information's "
             "leak of 03-Oct-2023, five months after this round, and Anthropic's own later statement "
             "contradicts it. What WAS public in May 2023 was a forward projection, not a run rate: The "
             "Information of 27-Dec-2023 reported Anthropic expecting over $850m annualised by end-2024. "
             "Our standing rule says later figures are hindsight and notes only, so 46.0x was not a real "
             "multiple. Kept as a record of the round. Anthropic now has three later rounds in this file "
             "with run-rates the company disclosed at or before the pricing date, which is what should be "
             "used instead. Daniil's instruction, 02-Sep-2026: 'was a very early round for them in May "
             "2023, so we need to use a later one'."),
  },
  ('Anthropic', '2025-03'): {
    'fields': {
      'revenue_status': 'Reported (TechCrunch, day of round)',
      'revenue_source_url': 'https://techcrunch.com/2025/03/03/anthropic-raises-3-5b-to-fuel-its-ai-ambitions/',
    },
    'note': ("SOURCE UPGRADED 02-Sep-2026, FIGURE UNCHANGED. We were citing LinkedIn News relaying The "
             "Information. TechCrunch of 03-Mar-2025, the day of the round, carries the same figure: "
             "'The company's annual revenue run rate was reportedly around $1 billion last year.' "
             "Anthropic's own Series F release of 02-Sep-2025 confirms it retrospectively: 'At the "
             "beginning of 2025... Anthropic's run-rate revenue had grown to approximately $1 billion.'"),
  },
 },
}

NEW_ROWS = [
 {
  'transaction_id': 'anthropic-2025-09', 'company_key': 'anthropic', 'company_name': 'Anthropic',
  'date': 'Sep-25', 'date_iso': '2025-09', 'round_type': 'Series F',
  'capital_raised_musd': '13000.0', 'post_money_musd': '183000.0', 'valuation_status': 'Disclosed',
  'revenue_metric': 'Run-rate revenue (> threshold)', 'revenue_musd': '5000.0',
  'revenue_status': 'Disclosed (company)', 'ev_revenue_x': '36.6',
  'subsector_as_supplied': 'Foundation models / generative AI',
  'screening_category_as_supplied': 'Data, AI & Developer Tools',
  'lead_key_investors': 'ICONIQ (lead); Fidelity; Lightspeed; Altimeter; Baillie Gifford; BlackRock; Coatue; GIC; General Atlantic; General Catalyst; Insight; Jane Street; Ontario Teachers; Qatar Investment Authority; TPG; T. Rowe Price; WCM; XN',
  'round_source_url': 'https://www.anthropic.com/news/anthropic-raises-series-f-at-usd183b-post-money-valuation',
  'revenue_source_url': 'https://www.anthropic.com/news/anthropic-raises-series-f-at-usd183b-post-money-valuation',
  'transaction_type': 'PRIMARY', 'denominator_basis': 'DISCLOSED_THRESHOLD', 'bound': '<=',
  'in_medians': '0', 'verification': 'VERIFIED', 'revenue_basis': 'ARR_RUNRATE',
  'revenue_period': 'RUN_RATE', 'valuation_basis': 'REVENUE', 'revenue_basis_source': 'STATED',
  'growth_band': 'HYPER', 'growth_pct_at_round': '400', 'growth_band_basis': 'DERIVED',
  'notes': ("INSERTED 02-Sep-2026 at Daniil's instruction to replace the May-2023 round with a later one. "
            "The cleanest Anthropic row in the file: valuation and denominator both come from Anthropic's "
            "own release of 02-Sep-2025, and the denominator carries an 'as of' date a full month BEFORE "
            "the pricing rather than after it. 'Anthropic has completed a Series F fundraising of $13 "
            "billion led by ICONIQ. This financing values Anthropic at $183 billion post-money.' And: 'By "
            "August 2025, just eight months later, our run-rate revenue reached over $5 billion.' 'Over' "
            "makes the denominator a floor, so 36.6x is a CEILING and the row does not feed medians. "
            "GROWTH AT ROUND: the same release gives approximately $1bn at the beginning of 2025, so "
            "roughly 400% over eight months."),
 },
 {
  'transaction_id': 'anthropic-2026-02', 'company_key': 'anthropic', 'company_name': 'Anthropic',
  'date': 'Feb-26', 'date_iso': '2026-02', 'round_type': 'Series G',
  'capital_raised_musd': '30000.0', 'post_money_musd': '380000.0', 'valuation_status': 'Disclosed',
  'revenue_metric': 'Run-rate revenue', 'revenue_musd': '14000.0',
  'revenue_status': 'Disclosed (company)', 'ev_revenue_x': '27.1',
  'subsector_as_supplied': 'Foundation models / generative AI',
  'screening_category_as_supplied': 'Data, AI & Developer Tools',
  'lead_key_investors': 'GIC; Coatue (led); D. E. Shaw Ventures; Dragoneer; Founders Fund; ICONIQ; MGX (co-led)',
  'round_source_url': 'https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation',
  'revenue_source_url': 'https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation',
  'transaction_type': 'PRIMARY', 'denominator_basis': 'DISCLOSED_POINT', 'bound': '',
  'in_medians': '1', 'verification': 'VERIFIED', 'revenue_basis': 'ARR_RUNRATE',
  'revenue_period': 'RUN_RATE', 'valuation_basis': 'REVENUE', 'revenue_basis_source': 'STATED',
  'growth_band': 'HYPER', 'growth_pct_at_round': '180', 'growth_band_basis': 'DERIVED',
  'notes': ("INSERTED 02-Sep-2026. Anthropic's own release of 12-Feb-2026: 'We have raised $30 billion in "
            "Series G funding led by GIC and Coatue, valuing Anthropic at $380 billion post-money.' And, "
            "same document, same day: 'Today, our run-rate revenue is $14 billion.' A clean point, not a "
            "threshold, so this row DOES feed medians. 380000/14000 gives 27.1x. Press in January 2026 "
            "reported the round in negotiation at a $350bn pre-money; the price it actually closed at is "
            "the $380bn post-money above, and only the closed price is used."),
 },
 {
  'transaction_id': 'anthropic-2026-05', 'company_key': 'anthropic', 'company_name': 'Anthropic',
  'date': 'May-26', 'date_iso': '2026-05', 'round_type': 'Series H',
  'capital_raised_musd': '65000.0', 'post_money_musd': '965000.0', 'valuation_status': 'Disclosed',
  'revenue_metric': 'Run-rate revenue (> threshold)', 'revenue_musd': '47000.0',
  'revenue_status': 'Disclosed (company)', 'ev_revenue_x': '20.5',
  'subsector_as_supplied': 'Foundation models / generative AI',
  'screening_category_as_supplied': 'Data, AI & Developer Tools',
  'lead_key_investors': 'Altimeter Capital; Dragoneer; Greenoaks; Sequoia Capital (led)',
  'round_source_url': 'https://www.anthropic.com/news/series-h',
  'revenue_source_url': 'https://www.anthropic.com/news/series-h',
  'transaction_type': 'PRIMARY', 'denominator_basis': 'DISCLOSED_THRESHOLD', 'bound': '<=',
  'in_medians': '0', 'verification': 'VERIFIED', 'revenue_basis': 'ARR_RUNRATE',
  'revenue_period': 'RUN_RATE', 'valuation_basis': 'REVENUE', 'revenue_basis_source': 'STATED',
  'growth_band': 'HYPER', 'growth_pct_at_round': '236', 'growth_band_basis': 'DERIVED',
  'notes': ("INSERTED 02-Sep-2026. Anthropic's own release of 28-May-2026: 'Anthropic has raised $65 "
            "billion in Series H funding led by Altimeter Capital, Dragoneer, Greenoaks, and Sequoia "
            "Capital, valuing the company at $965 billion post-money', and 'our run-rate revenue crossed "
            "$47 billion earlier this month'. 'Crossed' makes the denominator a floor, so 20.5x is a "
            "CEILING and the row does not feed medians. NOT A ROUND, DELIBERATELY EXCLUDED: secondary "
            "shares reported changing hands around $1.2tn in July 2026 on Caplight. That is resale "
            "chatter, not a company-priced raise. Anthropic filed confidentially for an IPO in June 2026; "
            "nothing had priced beyond Series H as of 02-Sep-2026."),
 },
]

CONS_EDITS = {
  ('Gorillas', '2021-10'): {
    'fields': {
      'round_source_url': 'https://www.cnbc.com/2021/10/19/delivery-hero-leads-1-billion-investment-in-grocery-start-up-gorillas.html',
      'revenue_source_url': 'https://www.cnbc.com/2021/10/19/delivery-hero-leads-1-billion-investment-in-grocery-start-up-gorillas.html',
      'valuation_status': 'Disclosed (post-money)',
    },
    'note': ("SOURCES ADDED 02-Sep-2026, NUMBERS UNCHANGED AND CONFIRMED. This was the one row of the "
             "nineteen disagreements carrying no revenue source. Both figures come from CNBC of "
             "19-Oct-2021, the day of the round: 'Gorillas is now valued at $3.1 billion following the "
             "cash injection' and 'Gorillas says it now has a run rate of $300 million, meaning it "
             "expects to make that much revenue on an annual basis.' TechCrunch the same day gives the "
             "OTHER number: 'It's now being valued at $2.1 billion, pre-money.' Pre plus the close-to-$1bn "
             "raise reconciles to the $3.1bn post. Daniil's database shows post-money 3,100 in its "
             "valuation cell but a 7.0x multiple, which is 2,100 over 300, so the multiple there was "
             "computed off the pre-money. Ours is 3,100 over 300 and stands at 10.3x, a ceiling because "
             "Gorillas said MORE than $300m."),
  },
  ('Glovo', '2021-12'): {
    'fields': {},
    'note': ("STILL RECORD ONLY, BUT FOR A NARROWER REASON AFTER DANIIL'S 02-Sep-2026 RULING. The ruling "
             "that all-stock deals price at announcement removes the objection that killed Wolt's press "
             "number, so the announced EUR 2.3bn 100% fully-diluted valuation is now usable here too. "
             "What is still missing is a SOURCED denominator. Daniil's database carries roughly EUR 360m "
             "of 2020 revenue giving 6.39x, and 2300/360 reproduces CB Insights' published 6.4x exactly, "
             "which is why our own header note flagged it as read off a comps blog rather than sourced. "
             "One source for Glovo's 2020 revenue turns this row on."),
  },
}


def load(path):
    raw = open(path).read().split('\n')
    head = [l for l in raw if l.startswith('#')]
    body = '\n'.join([l for l in raw if not l.startswith('#') and l.strip()])
    rows = list(csv.DictReader(io.StringIO(body)))
    return head, rows, list(rows[0].keys())


def save(path, head, rows, cols):
    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=cols)
    w.writeheader()
    for r in rows:
        w.writerow({c: r.get(c, '') for c in cols})
    open(path, 'w').write('\n'.join(head) + '\n' + out.getvalue())


def apply_edits(path, edits, new_rows=None):
    head, rows, cols = load(path)
    hit = 0
    for r in rows:
        key = (r.get('company_name'), (r.get('date_iso') or '')[:7])
        if key in edits:
            e = edits[key]
            for k, v in e['fields'].items():
                if k not in cols:
                    print('ERROR: unknown column %r' % k); sys.exit(1)
                print('  %-12s %-8s %-20s %r -> %r' % (key[0], key[1], k, r.get(k), v))
            r.update(e['fields'])
            r['notes'] = e['note'] + ' || ' + (r.get('notes') or '')
            hit += 1
    if hit != len(edits):
        print('ERROR: matched %d of %d rows in %s' % (hit, len(edits), path)); sys.exit(1)
    if new_rows:
        existing = {r['transaction_id'] for r in rows}
        for nr in new_rows:
            if nr['transaction_id'] in existing:
                print('ERROR: %s already exists' % nr['transaction_id']); sys.exit(1)
            for k in nr:
                if k not in cols:
                    print('ERROR: unknown column %r' % k); sys.exit(1)
            rows.append({c: nr.get(c, '') for c in cols})
            print('  INSERTED %s  %s at %s post-money, %sx' % (
                nr['transaction_id'], nr['round_type'], nr['post_money_musd'], nr['ev_revenue_x']))
    save(path, head, rows, cols)
    return len(rows)


print('--- %s' % MAIN)
n1 = apply_edits(MAIN, EDITS[MAIN], NEW_ROWS)
print('--- %s' % CONS)
n2 = apply_edits(CONS, CONS_EDITS)
print('\n%s now %d rows, %s now %d rows' % (MAIN, n1, CONS, n2))
