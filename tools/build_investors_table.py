#!/usr/bin/env python3
"""
DAY 1 of the investors-and-recommendations build (Fable's roadmap, docs/investors-and-
recommendations-roadmap-2sep.md). Builds data/investors.csv, one row per investor house.

TWO LAYERS, kept separate on purpose. Fable's line: vcconf's failure mode is stale investors;
ours would be aspirational ones.

  EVIDENCE  generated mechanically from our own rounds. These are the houses behind a founder's
            reference rounds. Every deal on the card carries the company, the round month and the
            round's own source URL, because it comes out of the same file the field comes from.
            Nobody can copy this layer: the investors arrive attached to the evidence.

  CALLABLE  funds writing first cheques in the founder's sector right now. Seeded from the 19
            UK funds already curated in data-content.js. These rows are DELIBERATELY INCOMPLETE:
            they carry a cheque range and a thesis and NO dated deal, so tools/investor_check.py
            refuses to render them. That refusal IS the pull list.

Rebuild:  python3 tools/build_investors_table.py
Check:    python3 tools/investor_check.py
"""
import csv, io, re, os, sys, json
from datetime import date

OUT = 'data/investors.csv'

# ---------------------------------------------------------------- helpers
def load(path):
    lines = [l for l in open(path) if not l.startswith('#')]
    return list(csv.DictReader(io.StringIO(''.join(lines))))

ROLE = re.compile(r'\s*\((?:lead|co-lead|co-led|led|acquirer|participating|existing|new)[^)]*\)\s*$', re.I)
JUNK = {'existing investors', 'existing', 'undisclosed', 'others', 'other investors', 'n/a', '',
        'named buyers, no lead stated', 'undisclosed investors', 'unnamed u.s. institutional investor',
        'tender participants', 'pipe investors', 'secondary buyers', 'not disclosed'}

# Prose that leaked out of the investor cells on the first build. These are sentences, not
# houses: "Buyers: Drive Capital, Stack Capital Group...", "sellers included Horizons Ventures".
# A house name is short and does not contain a colon or a verb.
NOT_A_HOUSE = ('buyer', 'seller', 'undisclosed', 'existing', 'unnamed', 'named buyers',
               'strategic partners', 'not fully disclosed', 'other investors', 'buying',
               'participants', 'syndicate members')

def split_investors(cell):
    if not cell:
        return []
    out = []
    for part in re.split(r'[;|]', cell):
        p = ROLE.sub('', part).strip().strip('.,')
        p = re.sub(r'\s*\((?:lead|co-lead|co-led|led)\)\s*', '', p, flags=re.I).strip()
        low = p.lower()
        if not p or low in JUNK or len(p) < 3:
            continue
        if any(t in low for t in NOT_A_HOUSE):
            continue
        if ':' in p or len(p) > 45 or low in ('founders', 'others', 'investors'):
            continue
        out.append(p)
    return out

# ONE HOUSE, ONE ROW. The two round files spell the same firm two ways ("Sequoia" in the consumer
# file, "Sequoia Capital" in the software file), which split 27 houses in two on the first build
# and understated the activity of every one of them. The canonical name is the longer, formal one.
ALIAS_TAILS = (' capital partners', ' capital', ' ventures', ' partners', ' management',
               ' group', ' global', ' investments')

def _stem(name):
    # Strip REPEATEDLY, not once. "Tiger Global Management" needs two passes to meet
    # "Tiger Global", and one pass left them as two houses.
    n = name.lower()
    changed = True
    while changed:
        changed = False
        for t in ALIAS_TAILS:
            if n.endswith(t) and len(n) > len(t) + 2:
                n, changed = n[:-len(t)], True
                break
    return re.sub(r'[^a-z0-9]', '', n)

def key_of(name):
    return _stem(name) or re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def _months_since(ym):
    from datetime import date
    if not re.match(r'^\d{4}-\d{2}$', ym or ''):
        return None
    t = date.today()
    return (t.year - int(ym[:4])) * 12 + (t.month - int(ym[5:7]))

MONTHS = {m: i for i, m in enumerate(
    ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'], 1)}

def iso_of(r):
    d = (r.get('date_iso') or '').strip()
    if re.match(r'^\d{4}-\d{2}', d):
        return d[:7]
    d2 = (r.get('date') or '').strip()          # 'Jan-22'
    m = re.match(r'^([A-Za-z]{3})-(\d{2})$', d2)
    if m:
        return '20%s-%02d' % (m.group(2), MONTHS[m.group(1).lower()])
    return ''

# ---------------------------------------------------------------- EVIDENCE layer
def evidence_rows():
    houses = {}
    files = [('data/private-rounds.csv', ['lead_key_investors']),
             ('data/private-rounds-consumer.csv', ['lead_investor', 'other_named_investors'])]
    for path, cols in files:
        if not os.path.exists(path):
            continue
        for r in load(path):
            iso = iso_of(r)
            company = (r.get('company_name') or '').strip()
            url = (r.get('round_source_url') or '').strip()
            arche = (r.get('screening_category_as_supplied') or r.get('category_as_supplied') or '').strip()
            sub = (r.get('subsector_as_supplied') or '').strip()
            for col in cols:
                for inv in split_investors(r.get(col)):
                    h = houses.setdefault(key_of(inv), dict(
                        name=inv, aliases=set(), deals=[], cats={}, subs={}, posts=[], cheques=[]))
                    h['aliases'].add(inv)
                    if len(inv) > len(h['name']):
                        h['name'] = inv
                    h['deals'].append((iso, company, url))
                    if arche:
                        h['cats'][arche] = h['cats'].get(arche, 0) + 1
                    if sub:
                        h['subs'][sub] = h['subs'].get(sub, 0) + 1
                    try: h['posts'].append(float(r.get('post_money_musd')))
                    except (TypeError, ValueError): pass
                    try: h['cheques'].append(float(r.get('capital_raised_musd')))
                    except (TypeError, ValueError): pass
    return houses

# ---------------------------------------------------------------- CALLABLE layer
def callable_seed():
    """The 19 UK funds curated in data-content.js, parsed rather than retyped."""
    s = open('data-content.js').read()
    m = re.search(r'const INVESTORS = \{(.*?)\n\};', s, re.S)
    if not m:
        print('WARNING: could not find the INVESTORS table in data-content.js')
        return {}
    funds = {}
    for sector, body in re.findall(r"'([^']+)':\s*\[(.*?)\]", m.group(1), re.S):
        for name, note in re.findall(r"\{\s*name:\s*'([^']+)',\s*note:\s*'([^']*)'\s*\}", body):
            f = funds.setdefault(key_of(name), dict(name=name, sectors=[], notes=set()))
            f['sectors'].append(sector)
            f['notes'].add(note)
    return funds

MONEY = re.compile(r'([£$€])\s*([\d.]+)\s*([kKmM])')

def parse_cheque(note):
    """'First cheques £100k to £1.5M.' -> (0.1, 1.5, 'GBP'). Returns (None, None, '') when absent."""
    hits = MONEY.findall(note or '')
    if not hits:
        return None, None, ''
    ccy = {'£': 'GBP', '$': 'USD', '€': 'EUR'}[hits[0][0]]
    vals = []
    for _sym, num, unit in hits:
        v = float(num)
        vals.append(v / 1000.0 if unit in 'kK' else v)
    return min(vals), max(vals), ccy

# The quiz sector keys are not our archetype vocabulary. This is the bridge, and it is the one
# piece of judgement in the file, so it lives here in the open rather than inside a loop.
SECTOR_TO_CATEGORY = {
    'SaaS / B2B software':        'Business Applications; Vertical Software',
    'AI / ML':                    'Data, AI & Developer Tools',
    'Fintech':                    'Merchant Acquiring & PSP; Digital Bank & Deposits; Commerce & Payments Software',
    'Insurtech':                  'Insurance',
    'Healthtech / Digital health':'Healthcare',
    'Biotech / Life sciences':    'Life Sciences',
    'Consumer / D2C':             'Consumer Brand; Owned-Inventory Retail',
    'Marketplaces':               'Third-Party Marketplace; Freelance & Services Marketplace',
    'Climate / Energy':           'Climate & Energy',
    'Deeptech / Hardware':        'Cloud & Infrastructure',
    'Cybersecurity':              'Cybersecurity',
    'Logistics / Supply chain':   'Commerce Enablement & Fulfilment; Local Delivery & On-Demand',
    'Proptech':                   'Vertical Software',
    'Edtech':                     'Education',
    'Other':                      '',
}

COLS = ['investor_key', 'investor_name', 'house_type', 'layer', 'geographies', 'stage_bands',
        'first_cheque_low_m', 'first_cheque_high_m', 'cheque_currency',
        'round_size_low_m', 'round_size_high_m', 'thesis_one_liner',
        'screening_categories', 'subsectors', 'recent_deal_1_company', 'recent_deal_1_date',
        'recent_deal_1_source_url', 'recent_deal_2_company', 'recent_deal_2_date',
        'recent_deal_2_source_url', 'rounds_in_set', 'companies_in_set', 'companies_backed',
        'first_round', 'last_round', 'median_round_size_m', 'median_postmoney_m',
        'last_verified', 'provenance']


def build():
    today = date.today().isoformat()
    rows = []

    ev = evidence_rows()
    for k, h in ev.items():
        deals = sorted([d for d in h['deals'] if d[0]], reverse=True)
        companies = sorted({c for _d, c, _u in h['deals'] if c})
        cats = '; '.join('%s(%d)' % (c, n) for c, n in sorted(h['cats'].items(), key=lambda x: -x[1])[:6])
        subs = '; '.join('%s(%d)' % (c, n) for c, n in sorted(h['subs'].items(), key=lambda x: -x[1])[:4])
        med = lambda xs: (sorted(xs)[len(xs)//2] if xs else '')
        rows.append({
            'investor_key': k, 'investor_name': h['name'], 'house_type': '', 'layer': 'EVIDENCE',
            'geographies': '', 'stage_bands': '',
            'first_cheque_low_m': '', 'first_cheque_high_m': '', 'cheque_currency': '',
            'thesis_one_liner': '', 'screening_categories': cats, 'subsectors': subs,
            'recent_deal_1_company': deals[0][1] if len(deals) > 0 else '',
            'recent_deal_1_date':    deals[0][0] if len(deals) > 0 else '',
            'recent_deal_1_source_url': deals[0][2] if len(deals) > 0 else '',
            'recent_deal_2_company': deals[1][1] if len(deals) > 1 else '',
            'recent_deal_2_date':    deals[1][0] if len(deals) > 1 else '',
            'recent_deal_2_source_url': deals[1][2] if len(deals) > 1 else '',
            'rounds_in_set': len(h['deals']), 'companies_in_set': len(companies),
            'companies_backed': '|'.join(companies),
            'first_round': deals[-1][0] if deals else '', 'last_round': deals[0][0] if deals else '',
            'median_round_size_m': med(h['cheques']), 'median_postmoney_m': med(h['posts']),
            '_round_sizes': [x for x in h['posts'] if x],
            'round_size_low_m': '', 'round_size_high_m': '',
            'last_verified': today,
            'provenance': ('GENERATED from data/private-rounds.csv and data/private-rounds-consumer.csv'
                           + ('. Spellings merged: ' + ' / '.join(sorted(h['aliases']))
                              if len(h['aliases']) > 1 else '')),
        })

    for k, f in callable_seed().items():
        note = sorted(f['notes'], key=len, reverse=True)[0]
        lo, hi, ccy = parse_cheque(' '.join(f['notes']))
        cats = sorted({c for s in set(f['sectors']) for c in SECTOR_TO_CATEGORY.get(s, '').split('; ') if c})
        existing = next((r for r in rows if r['investor_key'] == k), None)
        if existing:                       # a house that is BOTH a curated fund and in our rounds
            existing['layer'] = 'CALLABLE|EVIDENCE'
            existing['thesis_one_liner'] = note
            existing['first_cheque_low_m'] = lo if lo is not None else ''
            existing['first_cheque_high_m'] = hi if hi is not None else ''
            existing['cheque_currency'] = ccy
            existing['geographies'] = 'UK'
            existing['stage_bands'] = 'Pre-seed; Seed; Series A'
            existing['provenance'] += ' + data-content.js curated table'
            continue
        rows.append({
            'investor_key': k, 'investor_name': f['name'], 'house_type': 'Venture',
            'layer': 'CALLABLE', 'geographies': 'UK', 'stage_bands': 'Pre-seed; Seed; Series A',
            'first_cheque_low_m': lo if lo is not None else '',
            'first_cheque_high_m': hi if hi is not None else '', 'cheque_currency': ccy,
            'thesis_one_liner': note, 'screening_categories': '; '.join(cats),
            'subsectors': '; '.join(sorted(set(f['sectors']))),
            'round_size_low_m': '', 'round_size_high_m': '',
            'recent_deal_1_company': '', 'recent_deal_1_date': '', 'recent_deal_1_source_url': '',
            'recent_deal_2_company': '', 'recent_deal_2_date': '', 'recent_deal_2_source_url': '',
            'rounds_in_set': 0, 'companies_in_set': 0, 'companies_backed': '',
            'first_round': '', 'last_round': '', 'median_round_size_m': '', 'median_postmoney_m': '',
            'last_verified': '',
            'provenance': 'SEEDED from data-content.js. Needs two dated deals with source URLs.',
        })

    # ------------------------------------------------------------------ promotion
    # DANIIL, 02-Sep-2026: "Why are we focusing on the UK curated funds? Why only 19? We have a
    # much larger database already available from the deal database we own, no?"
    #
    # Right on both counts for the stage our own data covers, and the numbers settle where the
    # line falls. Of 349 houses, 80 have a deal inside 12 months and every one of them already
    # carries that deal with its date and its source URL. Those 80 are a current, sourced call
    # list and they were being withheld from founders because the CALLABLE layer had been
    # hand-typed rather than generated.
    #
    # What our data CANNOT do is the seed end, and this is a fact about the database rather than
    # a curation choice: it is built from priced rounds with a disclosed revenue figure, and small
    # rounds do not disclose revenue, so they never entered it. The median round a house in this
    # file joins is $267m; the 10th percentile is $100m; exactly THREE houses of 349 appear in any
    # round below $25m and none of the three is currently active. A founder raising GBP 600k
    # cannot call Coatue.
    #
    # So the layer is promoted where the evidence supports it and left to a pull where it does not.
    # A promoted house carries the size of ROUND it joins rather than a first-cheque range, because
    # a first cheque is not something our data knows and inventing one would be worse than leaving
    # it out. That is the honest equivalent: it tells a founder whether this is their conversation,
    # which is the whole point of putting a number on the card.
    def _stage_of(m):
        if m is None:                  return ''
        if m < 25:                     return 'Seed; Series A'
        if m < 100:                    return 'Series A; Series B'
        if m < 300:                    return 'Series B; Series C'
        return 'Growth; Late stage; Crossover'

    promoted = 0
    for r in rows:
        if r['layer'] != 'EVIDENCE':
            continue
        age = _months_since(r['last_round'])
        if age is None or age > 12:
            continue
        sizes = r.pop('_round_sizes', None) or []
        m = r.get('median_round_size_m')
        m = float(m) if m not in (None, '') else None
        if m is None:
            continue
        r['layer'] = 'CALLABLE|EVIDENCE'
        r['stage_bands'] = _stage_of(m)
        r['round_size_low_m'] = round(min(sizes), 1) if sizes else round(m, 1)
        r['round_size_high_m'] = round(max(sizes), 1) if sizes else round(m, 1)
        r['cheque_currency'] = 'USD'
        r['thesis_one_liner'] = ('Joins rounds of $%.0fm to $%.0fm in %s. Generated from the rounds '
                                 'in our own set, not from a curated list.'
                                 % (r['round_size_low_m'], r['round_size_high_m'],
                                    (r['screening_categories'] or 'our tracked sectors').split('(')[0].strip()))
        promoted += 1
    print('%d EVIDENCE houses promoted to CALLABLE on the activity rule (a deal inside 12 months).'
          % promoted)

    rows.sort(key=lambda r: (r['layer'] == 'EVIDENCE', -int(r['rounds_in_set'] or 0), r['investor_name']))

    header = """# Fairway investor table. One row per house. Built by tools/build_investors_table.py.
# Checked by tools/investor_check.py, which is the gate on what may render.
#
# TWO LAYERS AND THEY MUST NOT BE BLENDED.
#   EVIDENCE  the houses behind a founder's own reference rounds, generated from the same files
#             the football field comes from. Every deal carries company, month and the round's own
#             source URL. Honest label: a map of who pays up for businesses like yours, mostly
#             growth-stage and mostly US. NOT a call list for a seed round.
#   CALLABLE  funds writing first cheques in the founder's sector now. Seeded from the 19 UK funds
#             curated in data-content.js and DELIBERATELY INCOMPLETE: no dated deal, no source URL,
#             so the checker refuses them. That refusal is the pull list, not a bug.
#
# THE ACTIVITY RULE, taken from vcconf and binding here: a CALLABLE investor renders only with at
# least one named, dated deal inside 12 months WITH a source URL, a first-cheque range, a stage,
# a sector in our vocabulary, a geography and a one-line thesis. A row missing any of those does
# not render. Same discipline as comps sourcing: a figure with no source does not exist.
#
# COMPLIANCE, binding on every rendering of both layers: public information only, nothing behind
# a login, no contact details, no claim of introduction. The footer line carries onto every card:
# a map, not an introduction; no affiliation or endorsement is implied. Styled text wordmarks,
# never logos.
#
# Never pad to a fixed count. Six good matches beat twelve loose ones.
"""
    out = io.StringIO()
    w = csv.DictWriter(out, fieldnames=COLS)
    w.writeheader()
    for r in rows:
        w.writerow({c: r.get(c, '') for c in COLS})
    open(OUT, 'w').write(header + out.getvalue())

    nc = sum(1 for r in rows if 'CALLABLE' in r['layer'])
    ne = sum(1 for r in rows if 'EVIDENCE' in r['layer'])
    print('%s written: %d houses, %d carry a CALLABLE layer, %d carry an EVIDENCE layer'
          % (OUT, len(rows), nc, ne))
    return rows

if __name__ == '__main__':
    build()
