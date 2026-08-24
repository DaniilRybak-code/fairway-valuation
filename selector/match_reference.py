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
import csv, io, re, sys, statistics as st

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
        # in_stats on the software file, in_medians on the consumer file. Same idea:
        # the row is visible to the founder and out of every median.
        flag = r.get('in_medians', r.get('in_stats', '1'))
        r['in_medians'] = str(flag).strip() not in ('0','')
        listed[k] = r
listed = list(listed.values())

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

def size_note(a, b):
    if not a or not b: return ''
    x = b/a
    return '%.0fx smaller' % (1/x) if x < 1 else '%.0fx your size' % x

# A comparable that is not comparable is worse than a shorter list. Below this floor a name is
# not a peer, and the reveal shows three names rather than padding to five with noise.
FLOOR_REL, FLOOR_ABS = 0.45, 8.0

def qualifying(scored):
    if not scored: return []
    best = scored[0][0][0]
    cut = max(FLOOR_REL * best, FLOOR_ABS)
    return [x for x in scored if x[0][0] >= cut]

def select_private(prof, priv, want=5, window_months=24, asof=(2026, 8)):
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
# across the 62 usable rows the median EV/NTM revenue moves 4.4x between the
# lowest and highest gross margin buckets while the median EV/NTM gross profit
# moves 2.1x. Comparing a 25% margin business to a 90% margin business on revenue
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
