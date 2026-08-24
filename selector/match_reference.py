# -*- coding: utf-8 -*-
# REFERENCE IMPLEMENTATION, NOT THE PRODUCTION PATH.
#
# The site runs on Vercel and the reveal is Node (api/reveal.js), so the selector that ships has to
# be JavaScript. This file is the executable specification: it is what the JS port must reproduce,
# and it is what the golden tests are generated from. Keeping it in Python was the fastest way to
# get the doctrine right against the real CSVs; porting it is mechanical and should be done against
# the golden fixtures, not by eye.
#
# It reads the CSVs in data/ directly and needs no arguments.
# -*- coding: utf-8 -*-
"""Fairway selector. Business nature selects, recency only orders.

  1. Select on BUSINESS NATURE. No time filter, no size filter.
  2. Then take the MOST RECENT transactions among the names selected.
  3. If a similar business has not traded in the last 24 months, EXTEND the window
     until there are enough comparables. Never drop a good comparable to keep the window.

The window is a presentation rule applied AFTER selection, never a selection criterion.
That is the same mistake as the size gate, and it is avoided the same way.

THREE VOCABULARY FAMILIES now feed one universe:
  software    163 names   archetypes describe what kind of software it is
  fintech      87 names   archetypes describe the economic engine
  consumer     74 names   archetypes describe the consumer engine, and two extra
                          fields, asset_intensity and purchase_frequency, carry
                          the margin structure that the other two families do not need
A field is only scored when BOTH sides have a value for it. A blank never scores,
so the two consumer-only fields cannot quietly inflate every software row.
"""
import csv, io, re, sys, collections, statistics as st

def load(p):
    return list(csv.DictReader(io.StringIO('\n'.join(
      l for l in open(p,encoding='utf-8').read().splitlines() if not l.lstrip('"').startswith('#')))))
import os
D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data') + os.sep

# ---------------------------------------------------------------------------
# PRODUCT-TAG MATCHING
# An exact whole-tag match is worth 3.0 and is never down-weighted. A shared
# TOKEN is worth 0.6 scaled by how generic the token is, read from
# data/tag-token-weights.csv, which is computed from the tag files themselves.
# Frequency, not a hand-maintained stop list: a word carried by thirty companies
# separates nothing. Adding the consumer set took "marketplace" from six carriers
# to twenty-nine, and its token weight from 0.83 to 0.17, without anyone editing
# a list.
# ---------------------------------------------------------------------------
STOP = {'and','of','the','for'}
def toks(t): return set(re.findall(r'[a-z0-9]+', t.lower())) - STOP

TOKW = {r['token']: float(r['weight_factor']) for r in load(D+'tag-token-weights.csv')}

def tag_overlap(a, b):
    A = [x.strip() for x in (a or '').split('|') if x.strip()]
    B = [x.strip() for x in (b or '').split('|') if x.strip()]
    if not A or not B: return 0.0
    exact = len({x.lower() for x in A} & {x.lower() for x in B})
    ta = set(); tb = set()
    for x in A: ta |= toks(x)
    for x in B: tb |= toks(x)
    shared = 0.6 * sum(TOKW.get(t, 1.0) for t in (ta & tb))
    return 3.0*exact + shared

def norm(t):
    ex, sym = t.split(':', 1)
    return re.sub(r'^NASDAQ(GS|GM|CM)$','NASDAQ',ex) + ':' + sym.strip()

def _f(v):
    try: return float(v)
    except (TypeError, ValueError): return None

# Load order decides which tag row wins for a name that appears in two pulls.
# software before consumer before fintech, because:
#   BILL, nCino and Q2 sell software to financial institutions and must keep the
#   software archetypes (documented in the fintech vocabulary).
#   MercadoLibre is a marketplace with a payments business attached, not the reverse,
#   so it must keep the consumer archetypes.
listed = {}
for mfile, tfile, fam in [('peers-software.csv','peers-software-tags.csv','software'),
                          ('peers-ecommerce.csv','peers-ecommerce-tags.csv','consumer'),
                          ('peers-fintech.csv','peers-fintech-tags.csv','fintech')]:
    tags = {r['exchange_ticker']: r for r in load(D+tfile)}
    for m in load(D+mfile):
        k = norm(m['exchange_ticker'])
        if k in listed: continue
        r = {**m, **tags[m['exchange_ticker']], 'family': fam}
        r['ev']   = _f(m['enterprise_value_musd'])
        r['rev']  = _f(m['revenue_ntm_musd'])
        r['mult'] = _f(m['ev_ntm_revenue_x'])
        r['g']    = _f(m['revenue_growth_ntm_pct'])
        gp        = _f(m.get('gross_profit_musd'))
        r['gp']   = gp
        r['gp_mult'] = _f(m.get('ev_ntm_gp_x'))
        r['gm']   = 100*gp/r['rev'] if (gp and r['rev']) else None
        r['acv']  = _f(r.get('acv_usd_disclosed'))
        r['mix_note'] = r.get('mix_note','')
        # in_stats on the software file, in_medians on the consumer file. Same idea:
        # the row is visible to the founder and out of every median.
        flag = r.get('in_medians', r.get('in_stats', '1'))
        r['in_medians'] = str(flag).strip() not in ('0','')
        listed[k] = r
listed = list(listed.values())

# ---------------------------------------------------------------------------
# PRIVATE UNIVERSE
# Two files today: the software rounds and the consumer rounds. They share a schema.
# A round is only eligible for a RANGE if in_medians is 1; every other row stays visible
# and is shown as context with its valuation and, where that is all that exists, its GMV.
# transaction_type must reach the reveal: a SECONDARY is a mark, not a priced round.
# ---------------------------------------------------------------------------
private = []
for rfile, tfile in [('private-rounds.csv','private-companies-tags.csv'),
                     ('private-rounds-consumer.csv','private-companies-consumer-tags.csv')]:
    try:
        ptags = {r['company_key']: r for r in load(D+tfile)}
        for r in load(D+rfile):
            t = ptags.get(r['company_key'])
            if not t: continue
            row = {**t, **r}
            row['post'] = _f(r.get('post_money_musd'))
            row['rev']  = _f(r.get('revenue_musd'))
            row['mult'] = _f(r.get('ev_revenue_x'))
            row['in_medians'] = str(r.get('in_medians', '1')).strip() not in ('0', '')
            row['transaction_type'] = r.get('transaction_type', 'PRIMARY')
            row['denominator_basis'] = r.get('denominator_basis', '')
            row['bound'] = r.get('bound', '')
            private.append(row)
    except FileNotFoundError:
        pass

W = dict(tags_cap=12.0, arch=3.0, arch_soft=1.5, industry=3.0, function=2.0,
         buyer=2.5, acv=1.5, rev_model=2.5, gtm=2.0, role=1.0,
         asset=3.5, freq=2.0, growth=5.0, profitability=3.0, ai=1.0)

def _both(p, r, f):
    a, b = (p.get(f) or '').strip(), (r.get(f) or '').strip()
    return a and b and a == b

def score(p, r, weights=W, use_fin=True):
    s = 0.0; why = []
    ta = tag_overlap(p['product_tags'], r['product_tags'])
    if ta: s += min(ta, weights['tags_cap']); why.append('tags %.1f' % min(ta, weights['tags_cap']))
    ra, rb = r['archetype'], r['archetype_secondary']
    if p['archetype'] == ra: s += weights['arch']; why.append('archetype')
    elif p['archetype'] == rb or p.get('archetype_secondary') in (ra, rb):
        s += weights['arch_soft']; why.append('archetype~')
    if p['industry'] != 'Horizontal' and p['industry'] == r['industry']:
        s += weights['industry']; why.append('end market')
    elif p['industry'] == 'Horizontal' and r['industry'] == 'Horizontal': s += 1.0
    if p['function'] == r['function']: s += weights['function']; why.append('function')
    if p['buyer'] == r['buyer']: s += weights['buyer']; why.append('end customer')
    if p['revenue_model'] == r['revenue_model']: s += weights['rev_model']; why.append('revenue model')
    if p['gtm_motion'] == r['gtm_motion']: s += weights['gtm']; why.append('GTM')
    if p['product_role'] == r['product_role']: s += weights['role']
    # Consumer-family only. A blank on either side scores nothing, so these two never
    # give a uniform lift to the 250 rows that do not carry them.
    if _both(p, r, 'asset_intensity'):    s += weights['asset']; why.append('cost structure')
    if _both(p, r, 'purchase_frequency'): s += weights['freq'];  why.append('purchase frequency')
    if p['ai_stance'] == r['ai_stance']: s += weights['ai']; why.append('AI stance')
    if use_fin:
        if r.get('g') is not None:
            v = max(0, weights['growth']*(1 - abs(p['growth']-r['g'])/60.0)); s += v
            if v > weights['growth']*0.5: why.append('growth')
        if r.get('gm') is not None and p.get('gm') is not None:
            v = max(0, weights['profitability']*(1 - abs(p['gm']-r['gm'])/30.0)); s += v
            if v > weights['profitability']*0.5: why.append('margin')
    return s, why

WP = dict(tags_cap=12.0, arch=4.0, arch_soft=2.0, industry=4.0, function=3.0,
          buyer=3.5, acv=0.0, rev_model=3.5, gtm=3.0, role=1.5,
          asset=4.5, freq=2.5, growth=0, profitability=0, ai=2.0)

# ---------------------------------------------------------------------------
# FAMILY, THE FIRST GATE
#   Compare like with like BEFORE comparing detail. A D2C nutrition brand and a
#   language-learning app can share "sells a subscription to consumers" and score on it,
#   but one buys, makes and ships physical goods and the other does not, and no amount of
#   product-tag work fixes that. So family decides WHETHER two things may be compared, and
#   tags decide HOW WELL they compare. Ordering matters: gate first, then rank.
#
#   Family is not guessed. It is learned from the 318 listed rows, where family is already
#   assigned, by taking the family each archetype sits in. Every private archetype has a
#   listed counterpart, so the mapping is complete. Only "Vertical Software" is mixed
#   (38 software, 9 fintech) and takes the majority.
#
#   Deliberately NOT a hard gate on archetype itself. Measured across the twelve golden
#   profiles, gating on exact archetype equality costs real peers: a consumer neobank drops
#   from 5 listed peers to 3, a B2B procurement profile from 2 to 0. Archetype already
#   carries 4.0 points in the score, which is the right weight for a strong signal that is
#   sometimes too narrow. Family is the level where the gate belongs.
_FAMILY_OF = {}
for _r in listed:
    _FAMILY_OF.setdefault(_r['archetype'], collections.Counter())[_r['family']] += 1
_FAMILY_OF = {a: c.most_common(1)[0][0] for a, c in _FAMILY_OF.items()}

def family_of(x):
    return x.get('family') or _FAMILY_OF.get(x.get('archetype'), '')

for _r in private:
    _r['family'] = family_of(_r)

#   FAMILY IS THE GATE, END MARKET IS THE BRIDGE. A pure family gate is too blunt in one
#   direction. Toast sits in fintech because most of its revenue is card processing, while a
#   restaurant point-of-sale profile sits in software, so family alone shuts Toast out of a
#   set it obviously belongs in. What connects them is the end market: both sell to
#   restaurants, and Toast's industry is already tagged Hospitality. So a candidate passes
#   the gate if it shares the family OR shares a SPECIFIC end market.
#
#   "Specific" is doing real work. Horizontal is not an end market, it is the absence of one,
#   so it never bridges: otherwise every horizontal fintech would qualify as a peer for every
#   horizontal software company and the gate would dissolve.
#
#   Note what this gate does NOT do, because it matters for calibration. Huel and a
#   language-learning app are BOTH consumer family, so no family gate was ever going to
#   separate them. FLOOR_TAG_EVIDENCE is what separates those two, by requiring shared product
#   vocabulary. The two mechanisms catch different failures and both are needed: the gate stops
#   an SMB payments profile being shown consumer marketplaces, and the tag floor stops a
#   nutrition brand being shown to an edtech company inside the same family.
def same_family(prof, universe):
    f, ind = family_of(prof), (prof.get('industry') or '').strip()
    if not f: return universe
    bridged = ind and ind != 'Horizontal'
    out = [r for r in universe
           if family_of(r) == f
           or (bridged and (r.get('industry') or '').strip() == ind)]
    return out or universe


def size_note(a, b):
    if not a or not b: return ''
    x = b/a
    return '%.0fx smaller' % (1/x) if x < 1 else '%.0fx your size' % x

# A comparable that is not comparable is worse than a shorter list. Below this floor a name is
# not a peer, and the reveal shows three names rather than padding to five with noise.
FLOOR_REL, FLOOR_ABS = 0.45, 8.0

# AND AN ADEQUACY GATE, added 24-Aug-2026 after the golden fixtures caught the failure it fixes.
# A relative floor is useless when the BEST match is itself bad: 45% of a bad score is a worse score.
# Once the private universe gained 31 consumer companies, a consumer language-learning profile
# returned Huel, AG1 and Harry's as its private comparables, all scoring 9.7 on nothing but "sells a
# subscription to a consumer" - end customer plus revenue model plus purchase frequency, three
# low-information tags coinciding. That is the Perplexity-at-142.9x failure in a new costume.
#
# Calibration is the observed gap between a profile that HAS private neighbours and one that does not:
#   direct-to-consumer skincare   best 40.5   Glossier, Quince, SKIMS, Vuori. Real.
#   grocery quick commerce        best 23.6   SHEIN, Trendyol. Real, if imperfect.
#   UK car marketplace            best 13.5   Faire, Back Market. Marketplaces, wrong end market.
#   consumer language learning    best  9.7   nothing. There is no private edtech in the set.
# Anything below the gate means THERE IS NO COMPARABLE SET, and the reveal must say so rather than
# show five names. This is the same rule as "three names rather than padding to five", taken to zero.
FLOOR_ADEQUATE = 12.0

# A SUM IS NOT EVIDENCE. FLOOR_ADEQUATE alone was defeated the first time the tag corpus grew.
# Adding Rent the Runway to the private set gave a consumer language-learning profile a best match of
# 14.11, clearing the 12.0 gate, on end customer + revenue model + GTM + purchase frequency, that is,
# "sells a subscription to consumers and acquires them organically". Product tags contributed 0.1 of a
# possible 12.0. Huel, AG1 and Harry's had scored 9.69 on three of those four coincidences; Rent the
# Runway simply hit a fourth. Nothing about the match got better, the sum just got longer.
#
# So adequacy needs a second, orthogonal condition: the heaviest and most specific axis, what the
# product actually IS, must carry real weight. Measured across the twelve golden profiles, the best
# private match scores on product tags as follows:
#
#   d2c-skincare        12.0 Glossier      resale-marketplace  10.5 StockX
#   design-tool         11.1 Figma         b2b-procurement      7.2 Spendesk
#   consumer-neobank     3.8 Qonto         smb-payments         3.3 Qonto
#   ---------------------------------------- gap ----------------------------------------
#   quick-commerce       0.1 SHEIN         online-pet-retail    0.1 SHEIN
#   consumer-learning    0.1 Rent the Rway core-banking         0.1 CommerceIQ
#   car-marketplace-uk   0.0 Faire         restaurant-pos       0.0 Guesty
#
# The gap between 3.3 and 0.1 is an order of magnitude and it falls exactly where the categories we
# know are missing from the private set fall: edtech, quick commerce, auto and property marketplaces,
# pet retail, restaurant technology, core banking. The floor is set inside that gap.
FLOOR_TAG_EVIDENCE = 3.0

def _tag_points(why):
    for w in why:
        m = re.match(r'tags ([\d.]+)', str(w))
        if m: return float(m.group(1))
    return 0.0

def qualifying(scored, gate=FLOOR_ADEQUATE, tag_gate=FLOOR_TAG_EVIDENCE):
    if not scored: return []
    (best, why) = scored[0][0]
    if best < gate: return []                    # no comparable set exists; say so, do not pad
    if _tag_points(why) < tag_gate: return []    # coincidence without product commonality is not a set
    cut = max(FLOOR_REL * best, FLOOR_ABS)
    return [x for x in scored if x[0][0] >= cut]

def select_private(prof, priv, want=5, window_months=24, asof=(2026, 8)):
    priv = same_family(prof, priv)                   # same gate on the private side
    scored = sorted(((score(prof, r, WP, use_fin=False), r) for r in priv), key=lambda z: -z[0][0])
    best = {}
    for (sc, why), r in scored:
        k = r['company_key']
        if k not in best or r['date_iso'] > best[k][1]['date_iso']:
            if k not in best or sc >= best[k][0][0]: best[k] = ((sc, why), r)
    cands = qualifying(sorted(best.values(), key=lambda z: -z[0][0]))
    months = window_months
    while months <= 120:
        cut = '%04d-%02d' % (asof[0] - months//12, asof[1])
        inwin = sorted([c for c in cands if c[1]['date_iso'] >= cut],
                       key=lambda z: z[1]['date_iso'], reverse=True)
        if len(inwin) >= min(want, len(cands)): return inwin[:want], months
        months += 12
    return cands[:want], months


# ---------------------------------------------------------------------------
# CORE AND SECONDARY PEER GROUPS
#   Axis A, WHAT IT DOES     archetype, function, product tags, revenue model
#   Axis B, WHO IT SELLS TO  end market and end customer
#   CORE      strong on both.   SECONDARY strong on A, different on B.
# ---------------------------------------------------------------------------
def peer_groups(prof, universe, scorer=None, want=5):
    scorer = scorer or (lambda p, r: score(p, r))
    universe = same_family(prof, universe)          # gate on business nature before ranking on detail
    ranked = qualifying(sorted(((scorer(prof, r), r) for r in universe), key=lambda z: -z[0][0]))

    def axis_b(r):
        if prof['industry'] == 'Horizontal':
            return r['industry'] == 'Horizontal' and r['buyer'] == prof['buyer']
        return r['industry'] == prof['industry']

    def axis_a(r):
        a = {r['archetype'], r.get('archetype_secondary') or ''}
        mine = {prof['archetype'], prof.get('archetype_secondary') or ''} - {''}
        return bool(a & mine) or r['function'] == prof['function']

    core = [x for x in ranked if axis_a(x[1]) and axis_b(x[1])][:want]
    secondary = [x for x in ranked if axis_a(x[1]) and not axis_b(x[1])][:want]
    return core, secondary


# ---------------------------------------------------------------------------
# WHICH DENOMINATOR THE REVEAL LEADS WITH
#
# For software this never came up: gross margin runs 24-98% with a median of 77%,
# so revenue means roughly the same thing from one name to the next. In the
# consumer set it runs 8-100% and it is bimodal, and the consequence is measured:
# across the 63 usable rows the median EV/NTM revenue moves 4.3x between the
# lowest and highest gross margin buckets while the median EV/NTM gross profit
# moves 1.8x. Comparing a 25% margin business to a 90% margin business on revenue
# is not a valuation, it is an accounting artefact.
# ---------------------------------------------------------------------------
MARGIN_GAP = 15.0

def denominator(prof, group):
    """Return ('gp'|'rev', reason). Gross profit leads when the subject's margin
    sits more than MARGIN_GAP points from the peer group median, or when the group
    itself spans more than 30 points of margin."""
    gms = [r['gm'] for (_s, r) in group if r.get('gm') is not None]
    if not gms or prof.get('gm') is None:
        return 'rev', 'no usable gross margin on the subject or the group'
    med = st.median(gms)
    spread = max(gms) - min(gms)
    if abs(prof['gm'] - med) > MARGIN_GAP:
        return 'gp', ('your gross margin is %.0f%% against a peer median of %.0f%%, so the revenue '
                      'multiple is measuring the business model rather than the business'
                      % (prof['gm'], med))
    if spread > 30:
        return 'gp', ('gross margin across these peers runs %.0f%% to %.0f%%, too wide for a revenue '
                      'multiple to mean the same thing twice' % (min(gms), max(gms)))
    return 'rev', 'gross margin is close enough across the group for revenue to be comparable'

def group_range(group, which='rev'):
    """Quartile range of the group, excluding rows flagged out of medians."""
    key = 'mult' if which == 'rev' else 'gp_mult'
    v = sorted(r[key] for (_s, r) in group if r.get(key) is not None and r.get('in_medians', True))
    if not v: return None
    n = len(v)
    return dict(n=n, low=v[max(0, (n-1)//4)], mid=st.median(v), high=v[min(n-1, (3*(n-1))//4 + 1)])
