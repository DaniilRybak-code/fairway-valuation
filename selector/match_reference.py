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
import csv, io, re, sys, math, collections, statistics as st
import consumer_vocabulary as CV

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
untagged = []

# TWO FILES ARE LOADED IN A SECOND PASS AND THE REASON IS NOT COSMETIC. Family is the matching
# GATE, and it is LEARNED further down from the archetypes that appear on these listed rows. If the
# lending file and the logistics file each declared a NEW family, every archetype they share with
# the original three would be re-counted and could silently flip: 'Merchant Acquiring & PSP' sits in
# fintech today, and twenty payments names arriving under a family called 'operations' could move
# it. That would change which companies every payments founder is compared against, with nothing in
# any diff to show why.
#
# So the three original files keep their families exactly as they were and are loaded FIRST. The two
# new files are then loaded with family assigned PER ROW from the map the first three produced, so a
# logistics name lands in consumer, a payments name lands in fintech, and no existing archetype is
# re-counted. The gate is unchanged; the universe is simply larger.
_PRIMARY = [('peers-software.csv',  'peers-software-tags.csv',  'software'),
            ('peers-ecommerce.csv', 'peers-ecommerce-tags.csv', 'consumer'),
            ('peers-fintech.csv',   'peers-fintech-tags.csv',   'fintech')]
_SECONDARY = [('peers-logistics-services.csv', 'peers-logistics-services-tags.csv'),
              ('peers-lending.csv',            'peers-lending-tags.csv')]


def _ingest(mfile, tfile, fam_for):
    # THE TAG LOOKUP IS NORMALISED, NOT EXACT, AND THAT IS DELIBERATE. Capital IQ writes the same
    # company as NASDAQ:OPRT on one pull and NASDAQGS:OPRT on another, and an exact-string join
    # silently drops the row: 29 lenders vanished this way on 30-Aug-2026 before this was fixed.
    # norm() already strips the exchange prefix for de-duplication, so the join uses the same key.
    # The exact spelling is still tried first, so a file that is internally consistent is unaffected.
    tags, ntags = {}, {}
    for r in load(D+tfile):
        tags[r['exchange_ticker']] = r
        ntags.setdefault(norm(r['exchange_ticker']), r)
    for m in load(D+mfile):
        tk = m.get('exchange_ticker', '')
        k = norm(tk)
        if not k or k in listed: continue
        t = tags.get(tk) or ntags.get(k)
        if t is None:
            # A market row with no tag row cannot be matched on anything, so it is skipped and
            # RECORDED. Silently dropping it is how a whole sector goes missing without anyone
            # noticing, which is exactly what happened on 30-Aug-2026.
            untagged.append((mfile, tk, m.get('company_name', '')))
            continue
        r = {**m, **t, 'family': fam_for(t)}
        r['ev']   = _f(m.get('enterprise_value_musd'))
        r['rev']  = _f(m.get('revenue_ntm_musd'))
        r['mult'] = _f(m.get('ev_ntm_revenue_x'))
        # GROWTH ON THE LISTED SIDE CHANGED DEFINITION ON 30-AUG-2026 AND THIS IS WHERE IT LANDS.
        # Daniil recalculated it as the CY+0 to CY+2 COMPOUND ANNUAL GROWTH RATE of revenue in
        # reported currency, replacing the single-year forward NTM growth the screen used to give.
        # A two-year CAGR is the better measure for our purpose: one forward year is mostly the
        # analyst's near-term estimate and moves with every quarter, while two years describes the
        # trajectory a founder is actually being compared against, and it is far less sensitive to
        # a single guided quarter.
        #
        # BOTH COLUMNS ARE KEPT AND THE CAGR WINS WHERE IT EXISTS. The old column stays in the file
        # so an older row is not silently reinterpreted, and so the change is auditable rather than
        # a number that quietly means something different than it did last week. Anything comparing
        # a founder's growth against r['g'] is now comparing against a two-year rate: the founder is
        # asked for growth over the last twelve months, so the two are NOT like for like, and
        # closing that gap is an open item, not something to paper over here.
        #
        # THE ECOMMERCE PULL USES A THIRD DEFINITION AGAIN and it is read here rather than blended.
        # That file carries four revenue years and its CAGR runs CY+1 to CY+3; the software and
        # fintech files carry two years and theirs runs CY+0 to CY+2. Both are two-year forward
        # CAGRs, anchored a year apart. They are close cousins and NOT the same measure, so g_basis
        # records which one every row is carrying and no comparison across them can be made blind.
        r['g'] = _f(m.get('revenue_growth_cagr_cy0_cy2_pct'))
        r['g_basis'] = 'CAGR_CY0_CY2'
        if r['g'] is None:
            r['g'] = _f(m.get('revenue_growth_cagr_cy1_cy3_pct'))
            r['g_basis'] = 'CAGR_CY1_CY3'
        if r['g'] is None:
            r['g'] = _f(m.get('revenue_growth_ntm_pct'))
            r['g_basis'] = 'NTM'

        # GMV, WHERE THE COMPANY REPORTS ONE. gmv_reported is the company's own figure and is the
        # only one that may be shown to a founder as reported. gmv (NTM) and gmv_mult are built on
        # Daniil's assumption that GMV grows with revenue, because brokers do not forecast GMV, so
        # anything derived from them carries that assumption and must say so.
        r['gmv_reported'] = _f(m.get('gmv_cy0_musd'))
        r['gmv']          = _f(m.get('gmv_ntm_musd'))
        r['gmv_mult']     = _f(m.get('ev_ntm_gmv_x'))
        r['gmv_basis']    = 'DERIVED_FROM_REVENUE_GROWTH' if r['gmv_mult'] is not None else ''
        gp        = _f(m.get('gross_profit_musd'))
        r['gp']   = gp
        r['gp_mult'] = _f(m.get('ev_ntm_gp_x'))
        r['pb_mult'] = _f(m.get('p_bv_x'))          # balance-sheet lenders only
        r['pe_mult'] = _f(m.get('p_e_x'))           # balance-sheet lenders only
        r['gm']   = 100*gp/r['rev'] if (gp and r['rev']) else None
        r['acv']  = _f(r.get('acv_usd_disclosed'))
        r['mix_note'] = r.get('mix_note','')
        # in_stats on the software file, in_medians on the consumer file. Same idea:
        # the row is visible to the founder and out of every median.
        flag = r.get('in_medians', r.get('in_stats', '1'))
        r['in_medians'] = str(flag).strip() not in ('0','')
        listed[k] = r


for _mf, _tf, _fam in _PRIMARY:
    _ingest(_mf, _tf, (lambda f: (lambda _t: f))(_fam))

# The family map produced by the three primary files, used to place every secondary row.
_SEED = {}
for _r in listed.values():
    _SEED.setdefault(_r['archetype'], collections.Counter())[_r['family']] += 1
_SEED = {a: c.most_common(1)[0][0] for a, c in _SEED.items()}


def _fam_from_archetype(t):
    # An archetype the primary files never carried falls back to consumer, which is where every
    # such archetype in these two files belongs (logistics, retail, fitness, media). It is a
    # fallback, not a guess dressed up as one: nothing here should reach it, and if something does
    # it will show up as a consumer-family name that looks out of place.
    return _SEED.get(t.get('archetype')) or _SEED.get(t.get('archetype_secondary')) or 'consumer'


for _mf, _tf in _SECONDARY:
    _ingest(_mf, _tf, _fam_from_archetype)


# ---------------------------------------------------------------------------
# COMPANY-DISCLOSED VOLUME, LAID OVER THE BROKER ESTIMATE.
#
# 30-Aug-2026. Two different things were both called GMV until today. The peers files carry a
# BROKER GMV forecast, which exists for twelve names and is n.a. everywhere else. volume-metrics.csv
# carries what the ISSUER ITSELF published, which is the only figure we may quote back to a founder
# as reported. Where we hold both, the issuer's number wins for display and the broker's stays for
# the forward multiple, and volume_status records which we are looking at.
#
# THE CATEGORY MATTERS MORE THAN THE NUMBER. A payments TPV and a marketplace GMV are both gross
# transaction values and they are NOT comparable: WEX turns over $197bn to earn $2.9bn while
# GigaCloud turns over $2.0bn to earn $1.7bn. volume_kind keeps them apart so nothing can average
# a take-rate business against a marketplace.
#
# AND FOR A PAYMENTS NAME THE MULTIPLE IS A PERCENTAGE, NOT A TURN. Capital IQ's AV/NTM GMV column
# rounds to 0.0x for every payments business in the file, which tells a founder nothing. The same
# number as a percentage of volume is the take rate the market is paying for, so it is carried both
# ways and the payments lane must display the percentage.
# _OVERLAYS is read by tools/data_inventory.py so an overlay file is never reported unread.
_OVERLAYS = ('volume-metrics.csv',)
# A file kept for audit but no longer read: its content has been merged into an overlay.
_SUPERSEDED = {'gmv-disclosures.csv': 'merged into volume-metrics.csv on 30-Aug-2026'}
#
# THE JOIN NEEDS A SECOND KEY, AND THIS IS THE THIRD TIME THAT LESSON HAS COST US. norm() folds the
# Nasdaq tiers, which fixed 29 lenders this morning. It does not help when two sources disagree on
# the EXCHANGE itself: ACV Auctions came through as NASDAQGS:ACVA on one sheet and NYSE:ACVA on
# another, Triumph Financial as NYSE:TFIN and NASDAQ:TFIN, Naked Wines as LSE:WINE and AIM:WINE,
# PAX Global as SEHK:0327 and SEHK:327. Two of those four carry a disclosed volume figure and both
# were silently lost. So the fallback key is the SYMBOL plus the normalised company name. Symbol
# alone would be reckless, because the same symbol on two exchanges is usually two companies; with
# the name attached it is safe. Every row joined on the fallback is recorded in _VOLUME_TICKER_
# CONFLICTS so the disagreement is visible rather than papered over, and one of the two spellings
# is wrong and needs a human to say which.
_VOLUME_STATUS, _VOLUME_KIND, _VOLUME_ALT = {}, {}, {}
_VOLUME_TICKER_CONFLICTS = []


def _sym_name(tk, name):
    _s = (tk or '').split(':')[-1].strip().lstrip('0').lower()
    return _s + '|' + re.sub(r'[^a-z0-9]', '', (name or '').lower())[:14]


try:
    for _v in load(D + 'volume-metrics.csv'):
        _k = norm(_v.get('exchange_ticker', ''))
        if not _k:
            continue
        _VOLUME_STATUS[_k] = _v
        _VOLUME_KIND[_k] = _v.get('metric_category', '')
        _VOLUME_ALT.setdefault(_sym_name(_v.get('exchange_ticker'), _v.get('company_name')), _v)
except FileNotFoundError:
    pass

for _r in listed.values():
    _v = _VOLUME_STATUS.get(norm(_r['exchange_ticker']))
    if _v is None:
        _v = _VOLUME_ALT.get(_sym_name(_r['exchange_ticker'], _r['company_name']))
        if _v is not None:
            _VOLUME_TICKER_CONFLICTS.append(
                (_r['company_name'], _r['exchange_ticker'], _v['exchange_ticker']))
    _r['volume_status'] = (_v or {}).get('status', 'NOT_RESEARCHED')
    _r['volume_kind'] = (_v or {}).get('metric_category', '')
    _r['volume_metric_name'] = (_v or {}).get('issuer_metric_name', '')
    _r['volume_period'] = (_v or {}).get('fiscal_period', '')
    _r['volume_source'] = (_v or {}).get('source_url', '')
    _disc = _f((_v or {}).get('value_usd_musd'))
    if _disc is not None:
        _r['gmv_reported'] = _disc
        _r['gmv_basis_reported'] = 'ISSUER_DISCLOSED'
    elif _r.get('gmv_reported') is not None:
        _r['gmv_basis_reported'] = 'BROKER_ESTIMATE'
    else:
        _r['gmv_basis_reported'] = ''
    # A turn is unreadable below about 0.1x, which is every payments name we hold.
    _r['volume_pct'] = (round(100.0 * _r['ev'] / _r['gmv'], 2)
                        if (_r.get('ev') and _r.get('gmv')) else None)

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
            row['mult_book'] = _f(r.get('ev_book_x'))
            row['mult_tbook'] = _f(r.get('ev_tangible_book_x'))
            row['in_medians'] = str(r.get('in_medians', '1')).strip() not in ('0', '')
            row['transaction_type'] = r.get('transaction_type', 'PRIMARY')
            row['denominator_basis'] = r.get('denominator_basis', '')
            row['bound'] = r.get('bound', '')
            row['growth_band'] = (r.get('growth_band') or '').strip().upper()
            row['target_was_listed'] = str(r.get('target_was_listed', '')).strip() == '1'
            row['revenue_basis'] = (r.get('revenue_basis') or '').strip().upper()
            row['revenue_period'] = (r.get('revenue_period') or '').strip().upper()
            row['display_gate'] = (r.get('display_gate') or '').strip().upper()
            row['mult_low'] = _f(r.get('ev_revenue_low_x'))
            row['mult_high'] = _f(r.get('ev_revenue_high_x'))
            private.append(row)
    except FileNotFoundError:
        pass

W = dict(tags_cap=12.0, arch=3.0, arch_soft=1.5, industry=3.0, function=2.0,
         buyer=2.5, acv=1.5, rev_model=2.5, gtm=2.0, role=1.0,
         asset=3.5, freq=2.0, growth=5.0, profitability=3.0, ai=1.0)

def _both(p, r, f):
    a, b = (p.get(f) or '').strip(), (r.get(f) or '').strip()
    return a and b and a == b

# A BLANK NEVER SCORES. Only asset_intensity and purchase_frequency used to enforce this, via
# _both(). Everything else compared with plain equality, so two blanks matched and paid full
# points. The tag files happen to be complete today, so nothing was scoring wrongly, but the
# rule has to live in the code rather than in the luck of the data: a real founder profile is
# routinely missing revenue_model (six of the twenty-one field-test companies publish no
# pricing at all), and the moment one of those met a peer row with a gap it would have been
# paid 3.5 points for the two of them being equally silent.
def _eq(p, r, f):
    a, b = (p.get(f) or '').strip(), (r.get(f) or '').strip()
    return a and b and a == b

def score(p, r, weights=W, use_fin=True):
    s = 0.0; why = []
    ta = tag_overlap(p['product_tags'], r['product_tags'])
    if ta: s += min(ta, weights['tags_cap']); why.append('tags %.1f' % min(ta, weights['tags_cap']))
    ra, rb = r['archetype'], r['archetype_secondary']
    if p['archetype'] and p['archetype'] == ra: s += weights['arch']; why.append('archetype')
    elif p['archetype'] and (p['archetype'] == rb or p.get('archetype_secondary') in (ra, rb) and p.get('archetype_secondary')):
        s += weights['arch_soft']; why.append('archetype~')
    if p['industry'] != 'Horizontal' and _eq(p, r, 'industry'):
        s += weights['industry']; why.append('end market')
    elif p['industry'] == 'Horizontal' and r['industry'] == 'Horizontal': s += 1.0
    if _eq(p, r, 'function'): s += weights['function']; why.append('function')
    if _eq(p, r, 'buyer'): s += weights['buyer']; why.append('end customer')
    if _eq(p, r, 'revenue_model'): s += weights['rev_model']; why.append('revenue model')
    if _eq(p, r, 'gtm_motion'): s += weights['gtm']; why.append('GTM')
    if _eq(p, r, 'product_role'): s += weights['role']
    # Consumer-family only. A blank on either side scores nothing, so these two never
    # give a uniform lift to the 250 rows that do not carry them.
    if _both(p, r, 'asset_intensity'):    s += weights['asset']; why.append('cost structure')
    if _both(p, r, 'purchase_frequency'): s += weights['freq'];  why.append('purchase frequency')
    if _eq(p, r, 'ai_stance'): s += weights['ai']; why.append('AI stance')
    if use_fin:
        # The profile side can be genuinely empty. A pre-revenue founder has no growth rate and
        # no gross margin, and neither does a company profiled from its website alone. Scoring
        # must degrade to the qualitative axes rather than raise TypeError on None.
        if r.get('g') is not None and p.get('growth') is not None:
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
#   ONE ARCHETYPE, ONE LISTED ROW, AND THE GATE FALLS OVER. Found 26-Aug-2026 the moment Baozun
#   was removed. Baozun was the ONLY listed company carrying the archetype "Commerce Enablement &
#   Fulfilment". With it gone, that archetype had no family, so family_of() returned blank for
#   SellerClaw, and same_family() fails OPEN on a blank family and handed back the entire universe.
#   SellerClaw, a merchant-account operator, was then shown Sierra, Clay, Decagon and Semrush.
#   Deleting one listed row silently disabled the first gate for a whole archetype.
#
#   Two fixes, both needed. The map is now seeded from the consumer vocabulary so that every
#   declared consumer archetype has a family whether or not a listed row happens to carry it, and
#   the private rows contribute to the learning as well as consuming it.
_FAMILY_OF = {a: 'consumer' for a in getattr(CV, 'ECOM_ARCHETYPES', {})}
_learned = {}
for _r in listed:
    _learned.setdefault(_r['archetype'], collections.Counter())[_r['family']] += 1
_FAMILY_OF.update({a: c.most_common(1)[0][0] for a, c in _learned.items()})

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
# A LENDER NEVER PRICES A NON-LENDER, AND THE REVERSE.
#
# Daniil, 28-Aug-2026, on Payabli being priced off Klarna: "Klarna is exposed to credit risk. In my
# view some embedded payments stuff works much better." He is right, and the gate that already
# existed was only half a gate. is_balance_sheet decided which METRIC a founder is priced on; it did
# not decide which COMPANIES were eligible to price them. So an embedded-payments company carrying
# no credit risk was compared against a consumer lender, on a lender's economics, because Klarna
# was the only priced payments-adjacent row that cleared the relevance gate.
#
# The two populations do not price each other in either direction. A lender's multiple carries its
# funding book and its credit losses; a payments company's does not.
def balance_sheet_compatible(prof, rows):
    want = is_balance_sheet(prof)
    return [r for r in rows if is_balance_sheet(r) == want]

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
# FLOOR_ABS LOWERED 8.0 -> 5.0, 25-Aug-2026. It was set when the only profiles were the twelve I
# invented, which scored 22 to 41 against their best match. Real companies profiled from their own
# websites score 8 to 22, so an absolute floor of 8.0 was cutting almost everything: Shopify at 7.9
# for SellerClaw, Yext at 7.5 for Honestly, HubSpot at 6.9 for Fundraisly, Coursera at 6.0 for Honen.
# Swept against both measures at once. Agreement with Daniil's own comp picks goes from 8 of 22 to
# 12, and core hits from 4 to 7, while leave-one-out precision across 217 listed companies stays
# flat at 81%. It plateaus at 5.0, which means below that the relative floor and the anchoring rule
# are already doing the work and the absolute floor is redundant. Free recall, no accuracy cost.
FLOOR_REL, FLOOR_ABS = 0.45, 5.0

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

# ANCHORING REPLACES THE BARE TAG FLOOR, 25 August 2026.
#
# The tag floor was calibrated against twelve profiles I had invented, whose tag scores ran
# 7.3 to 12.0 because I had unconsciously written them in the dataset's own vocabulary. Run
# against twenty-one real companies profiled from their own websites, tag scores run 0.0 to
# 3.9 and the floor blocked twenty of twenty-one. It was not measuring comparability; it was
# measuring how closely a founder's words happen to echo our tag file.
#
# What the real cases show is that there are TWO honest ways a match can be anchored in
# something specific about the business, and the tag floor only knew one of them:
#
#   Fyle, a nail-care brand, best-matches FIGS with 0.1 tag points and yet shares archetype
#   Consumer Brand, end market Apparel & Beauty, product role BRAND and asset intensity
#   OWN_PRODUCT. That is a real comparable and the tag floor killed it.
#
#   Context.dev best-matches MongoDB with 0.0 tag points and shares only the archetype
#   "Data, AI & Developer Tools", which spans everything from a database to a scraper. That
#   is not a comparable and it must stay blocked.
#
# The difference is a SPECIFIC end market. So a match qualifies on either route: real product
# vocabulary in common, or a shared non-Horizontal end market plus a shared archetype.
# Horizontal is not an end market and never anchors, which is what keeps Context.dev out.
#
# Both regression cases still fail, checked: Huel against a language-learning app (different
# end markets, 0.1 tag points) and consumer marketplaces against SMB payments (Horizontal).
FLOOR_TAG_EVIDENCE = 3.0

def _anchored(p, r, why):
    if _tag_points(why) >= FLOOR_TAG_EVIDENCE:
        return True
    return (p.get('industry') and p['industry'] != 'Horizontal'
            and _eq(p, r, 'industry')
            and (p['archetype'] == r['archetype'] or p['archetype'] == r.get('archetype_secondary')))

# ---------------------------------------------------------------------------
# THE COMPARABILITY LADDER
#
# Returning nothing is honest but it is not useful, and on the twenty-one real companies it was
# happening fifteen times. A banker with no direct comparable does not stop; they widen, and they
# say out loud how far they widened. So does this.
#
#   DIRECT    the peer shares real product vocabulary, or shares a specific end market AND an
#             archetype. This is a comparable in the ordinary sense.
#   ADJACENT  the peer does the same KIND of thing, sharing an archetype, but the products
#             themselves have nothing in common. An agent-evals company against a database
#             company: both developer infrastructure, different businesses.
#   BROAD     same family only. Software against software, consumer against consumer. This is
#             "how this corner of the market trades", not "here are your peers".
#
# THE LADDER FILLS, IT DOES NOT STOP. Changed 26-Aug-2026 on Daniil's instruction: "one
# coincidence should not evict four decent comps. The point is not to get a comp that is 100%
# the same business, close enough is good enough."
#
# The rule it replaces stopped at the best tier that had ANY member. InsForge, a
# backend-as-a-service for AI coding agents, shares exactly one product tag with Algolia,
# "Vector Search". One exact tag is worth 3.0 points and FLOOR_TAG_EVIDENCE is 3.0, so that
# single coincidence made Algolia DIRECT, DIRECT beat ADJACENT outright, and a four-name range
# built from Lovable, LangChain, Replit and Cursor collapsed to a one-name diamond on a search
# API. Third time an absolute threshold has been crossed by a single low-information signal.
#
# So the set now fills from DIRECT downward through ADJACENT until it has the names it wants,
# and only falls to BROAD if those two produce nothing at all. DIRECT names still come first,
# because being anchored on real shared vocabulary is information the ordering should carry.
#
# AND THE LABEL FOLLOWS THE WEAKEST MEMBER, not the best. A group of one DIRECT hit and four
# ADJACENT names is an ADJACENT group: that is what the founder is being shown, and claiming
# DIRECT for it would be the same overstatement in a different place.
#
# A miss is still a miss: if nothing in the family clears FLOOR_ABS the answer is still no set,
# and that event is what the gap log records.
_TIER_ORDER = {'DIRECT': 0, 'ADJACENT': 1, 'BROAD': 2}
PRICING_TIERS = ('DIRECT', 'ADJACENT')

def set_tier(prof, members):
    """A mixed set is labelled by its WEAKEST member. One direct hit does not make four
    adjacent names direct."""
    if not members: return 'NONE'
    return max((_tier(prof, r, why) for (sc, why), r in members), key=lambda t: _TIER_ORDER[t])

def _tier(p, r, why):
    if _anchored(p, r, why):
        return 'DIRECT'
    mine = {p.get('archetype'), p.get('archetype_secondary')} - {None, ''}
    theirs = {r.get('archetype'), r.get('archetype_secondary')} - {None, ''}
    if mine & theirs:
        return 'ADJACENT'
    return 'BROAD'

# NOTHING WITH ABSOLUTELY NOTHING TO DO WITH THE FOUNDER.
#
# Daniil, 26-Aug-2026: "It is ok not to have 100% comparables. It is important NOT TO SHOW
# COMPARABLES THAT HAVE ABSOLUTELY NOTHING TO DO WITH THE FOUNDER'S BUSINESS. And important to
# explain the selection."
#
# This is the counterweight to the filling ladder, and it was needed the same day. Filling took
# coverage from 6 of 21 to 20 of 21, and the way it got there was partly by handing Publora, a
# social-media publishing API, four private names scoring exactly 0.0 on product tags: Lovable,
# Semrush, LangChain and Perplexity. They qualified on being developer-facing, consumption-priced
# infrastructure. That is a real similarity and it is not a business relationship, and a founder
# looking at Perplexity in their own comp set would rightly stop believing the rest of the page.
#
# So a candidate must have SOMETHING, by either of two routes:
#   product vocabulary  any shared tag token at all, however weak. Not the 3.0 that ANCHORS a
#                       DIRECT label, just more than nothing.
#   the same end market  a shared, specific, non-Horizontal industry. This is what keeps Rokt and
#                       Yotpo next to SellerClaw: no shared tag, but all three live in
#                       Retail & E-commerce and that is a genuine relationship.
# Horizontal never counts, because it is the absence of an end market rather than one.
#
# Measured across the 21 real profiles this removes 28 of 97 private members. Publora and Mailwarm
# fall to a single name each, which is the honest answer for them: one loosely related company,
# drawn as a diamond and captioned as one.
def _relevant(p, r, why):
    if _tag_points(why) > 0: return True
    pi = (p.get('industry') or '').strip()
    return bool(pi) and pi != 'Horizontal' and pi == (r.get('industry') or '').strip()


# AND EXPLAIN THE SELECTION. `why` is already the score's own working; this turns it into the
# sentence the reveal shows when a founder asks why a name is there.
_WHY_LABEL = {'archetype': 'same type of business', 'archetype~': 'related type of business',
              'end market': 'same end market', 'function': 'same business function',
              'end customer': 'same kind of customer', 'revenue model': 'same revenue model',
              'GTM': 'sold the same way', 'cost structure': 'same cost structure',
              'purchase frequency': 'same purchase frequency', 'AI stance': 'same AI stance',
              'growth': 'similar growth', 'margin': 'similar gross margin'}

def why_text(prof, rec, why):
    """A short, honest reason this company is in the set. Shared product vocabulary is named
    explicitly, because it is the strongest thing we can say and the easiest to check."""
    parts = []
    shared = sorted(toks(prof.get('product_tags') or '') & toks(rec.get('product_tags') or ''))
    tp = _tag_points(why)
    if tp > 0:
        named = [t for t in (rec.get('product_tags') or '').split('|')
                 if toks(t) and toks(t) <= toks(prof.get('product_tags') or '')]
        if named: parts.append('both do ' + ', '.join(named[:3]))
        elif shared: parts.append('shares the language of ' + ', '.join(shared[:3]))
    for w in why:
        lab = _WHY_LABEL.get(str(w))
        if lab and lab not in parts: parts.append(lab)
    return '; '.join(parts[:4]) or 'same business family only'


def qualifying(scored, prof=None, gate=FLOOR_ADEQUATE, only=None):
    """Returns (rows, tier). tier is DIRECT, ADJACENT, BROAD or NONE.
    `only` restricts to one tier; otherwise the best tier with members wins."""
    if not scored: return [], 'NONE'
    if prof is None:
        cut = max(FLOOR_REL * scored[0][0][0], FLOOR_ABS)
        return [x for x in scored if x[0][0] >= cut], 'DIRECT'
    # The relevance gate runs before the tiers, so a candidate with no relationship to this
    # founder cannot reach any tier, secondary included.
    scored = [x for x in scored if _relevant(prof, x[1], x[0][1])]
    if not scored: return [], 'NONE'
    tiers = {}
    for x in scored:
        tiers.setdefault(_tier(prof, x[1], x[0][1]), []).append(x)
    if only == 'ADJACENT':   want = ('DIRECT', 'ADJACENT')   # a direct hit is also adjacent
    elif only == 'BROAD':    want = ('DIRECT', 'ADJACENT', 'BROAD')
    elif only:               want = (only,)
    else:                    want = ('DIRECT', 'ADJACENT', 'BROAD')
    for t in (want if only else ('DIRECT', 'ADJACENT', 'BROAD')):
        rows = [y for tt in (want if only else (t,)) for y in tiers.get(tt, [])] if only else list(tiers.get(t, []))
        # DIRECT must clear the adequacy gate. A widened tier only has to clear the absolute
        # floor, because its job is to be the next best thing rather than a peer.
        floor = gate if (only or t) == 'DIRECT' else FLOOR_ABS
        rows = sorted([x for x in rows if x[0][0] >= floor], key=lambda z: -z[0][0])
        if not rows: continue
        cut = max(FLOOR_REL * rows[0][0][0], FLOOR_ABS)
        return [x for x in rows if x[0][0] >= cut], (only or t)
    return [], 'NONE'

# MATURE AND HYPER DO NOT BELONG IN THE SAME PRIVATE COMPARISON.
#
# Daniil, 26-Aug-2026: "Tag peers as mature (<15% growth), growing (15-30%) and hyper growth (30%+).
# Then match the profile of the user company to the database and select the peers accordingly. It is
# ok to have growing and hyper growth peers together, same as mature and growth. It is somewhat not
# right to have mature and hyper growth in the same comparison. FOR PRIVATE ROUNDS ONLY, PUBLIC
# COMPS ARE WHAT THEY ARE, MOST OF THEM ARE MATURE. The growth discrepancy will be more directly
# resolved in growth-adjusted valuation ranges."
#
# So the gate is: adjacent bands may sit together, opposite ends may not. It applies to the private
# lane and NOWHERE ELSE, by design: peer_groups is untouched.
#
# AN UNKNOWN BAND NEVER EXCLUDES ANYTHING. Growth at the time of a private round is not routinely
# disclosed and we will not invent it. Sourcing across 39 rounds found a stated, dated growth rate
# for 23 and nothing for the rest, so a blank has to be a permissive value rather than a guess.
#
# WHAT THE SOURCING ACTUALLY SHOWED, and it is worth knowing before relying on this gate: the
# private file is almost entirely hyper-growth. Of 23 rounds with a published rate, 21 are above
# 30% and the only two that are not are Mailchimp at 20% and Semrush at 15%. The band gate is
# therefore a narrow instrument here. It will keep Semrush and Mailchimp away from a hyper-growth
# founder, and that is all it can do until more rows carry a rate.
# THE BOUNDARIES ARE FITTED, NOT CHOSEN. Refitted 27-Aug-2026.
#
# Daniil: "We need to reconsider the definitions, otherwise it does not make sense to have 90% of
# names in hyper. Let's apply Gaussian distribution and derive growth definitions from it."
#
# He is right and the diagnosis is precise: the original 15 / 30 cut-offs were not wrong, they were
# calibrated to the WRONG POPULATION. On the 323 listed companies we hold, the terciles of forward
# growth fall at 8% and 17%, so 15 and 30 describe public markets almost exactly. On private rounds
# the terciles fall at 60% and 124%. Applying a public-market ruler to venture rounds put 36 of 40
# rows in one bucket, which is not a classification, it is a constant.
#
# A GAUSSIAN ON THE RAW RATE IS THE WRONG MODEL and it is worth saying why rather than just fixing
# it. Growth is bounded below at -100% and unbounded above, so the distribution is heavily right
# skewed: on our data, skew +3.16 and excess kurtosis +11.77 against 0 and 0 for a normal. A mean
# and a standard deviation on that produce boundaries that no data sits near. Taking ln(1+g) pulls
# it to skew +1.22 and excess kurtosis +1.74, and a Kolmogorov-Smirnov test gives D = 0.160 against
# a 5% critical value of 0.215, so log-normality is not rejected. That is the Gaussian to fit.
#
# Fitted on the 40 private rounds that carry a dated growth rate: mu = 0.734, sd = 0.462 in log
# space, so the typical private round in this file grows 108% a year. Boundaries at plus and minus
# half a standard deviation, which splits a normal into roughly 31 / 38 / 31 per cent:
#
#     MATURE   below 65%          14 rows
#     GROWING  65% to 162%        15 rows
#     HYPER    above 162%         11 rows
#
# THESE BANDS ARE RELATIVE TO PRIVATE ROUNDS, and that is deliberate. A company growing 50% a year
# is not mature in any ordinary sense; it is slow FOR A VENTURE-BACKED COMPANY BEING PRICED AGAINST
# OTHER VENTURE-BACKED COMPANIES, which is the only comparison this gate governs. The founder is
# banded on the same scale for the same reason. Listed companies are never banded: public comps are
# what they are.
#
# The numbers below are OUTPUTS of tools/refit_growth_bands.py. Rerun it when growth coverage grows
# materially and update them from it rather than by taste. n = 40 is thin, and the sample is biased
# toward companies that chose to disclose a growth rate, which skews it high; expect the boundaries
# to fall as coverage widens.
GROWTH_BANDS = ('MATURE', 'GROWING', 'HYPER')
_BAND_ORDER = {b: i for i, b in enumerate(GROWTH_BANDS)}
BAND_FIT = dict(n=51, mu=0.845, sd=0.543, typical_pct=133, fitted='2026-08-27b',
                source='tools/refit_growth_bands.py')
BAND_LOW, BAND_HIGH = 77.0, 206.0
BAND_LABEL = {'MATURE':  'slower than most rounds in the set',
              'GROWING': 'in line with the set',
              'HYPER':   'faster than most rounds in the set'}

def band_of(growth_pct):
    """Band a growth rate against the PRIVATE-ROUND distribution. Empty for an unknown rate."""
    if growth_pct is None: return ''
    try: g = float(growth_pct)
    except (TypeError, ValueError): return ''
    return 'MATURE' if g < BAND_LOW else ('GROWING' if g <= BAND_HIGH else 'HYPER')

def band_compatible(prof_band, row_band):
    a, b = _BAND_ORDER.get(prof_band or ''), _BAND_ORDER.get(row_band or '')
    if a is None or b is None: return True          # unknown on either side never excludes
    return abs(a - b) < 2


def _neg_date(d):
    """Sort key that puts the most recent date first while the key beside it sorts ascending."""
    return tuple(-int(x) for x in (d[:4], d[5:7]))


# ---------------------------------------------------------------------------
# ONE COMPANY, ONE VOTE, AND WHICH ROUND GETS IT
#
# Daniil, 31-Aug-2026: "revenue scale should only be the first gate when we select between multiple
# rounds of the same company and when the multiple is an order of magnitude different. If multiples
# are similar across rounds, we should just use the latest."
#
# WHY THIS RULE AND NOT THE OLD ONE. Twelve companies carry more than one priced round. The old code
# kept the highest business-nature score and broke ties on date. Two rounds of one company carry
# identical tags, so the score ALWAYS tied and the date decided on its own, every time. Recency was
# selecting a comparable, which our own rules prohibit. Eight priced rounds, including the two
# highest multiples we hold, were unreachable by any founder.
#
# THE THRESHOLD IS SET WHERE THE DATA IS EMPTY, WHICH IS THE ONLY HONEST PLACE TO PUT ONE. Measured
# across the companies that carry more than one round, the spread between a company's own multiples
# is either under 1.5x (Mews 1.04, SKIMS 1.06, Vinted 1.15, AlphaSense 1.5, Scale AI 1.5) or over
# 7x (Klarna 7.4, Meesho 11.0). Nothing sits between. Any threshold in that gap gives the same
# answer today, so 3.0 is not a tuned parameter and must not be treated as one: if a future round
# lands inside the gap, this constant needs a fresh look rather than a nudge.
MULTI_ROUND_SPREAD = 3.0


def _round_pick_reason(rows, chosen, spread):
    # The wording has to survive the case where the other rounds carry no multiple at all, which is
    # most of them. Calling those 'priced rounds' would be a small lie in a sentence a founder reads.
    n = len(rows)
    if spread is None:
        return 'the latest of %d rounds we hold for this company; only one of them is priced' % n
    if spread < MULTI_ROUND_SPREAD:
        return ('the latest of %d rounds we hold; the priced ones sit within %.1fx of each other, '
                'so the choice between them barely moves the answer' % (n, spread))
    return ('%s, chosen because its revenue at pricing is closest to yours rather than because it '
            'is the most recent; this company repriced by %.1fx between rounds'
            % (chosen['date'], spread))


def _one_round_per_company(prof, scored):
    """Keep one row per company. WHICH row is the whole question, and it is decided per founder."""
    by = collections.OrderedDict()
    for (sc, why), r in scored:
        by.setdefault(r['company_key'], []).append(((sc, why), r))
    out = []
    for k, rows in by.items():
        top = max(z[0][0] for z in rows)
        tied = [z for z in rows if z[0][0] >= top - 1e-9]
        if len(tied) == 1:
            out.append(tied[0]); continue
        mults = [m for m in (_f(z[1].get('mult')) for z in tied) if m]
        spread = (max(mults) / min(mults)) if len(mults) > 1 and min(mults) > 0 else None
        if spread is None or spread < MULTI_ROUND_SPREAD:
            # SIMILAR MULTIPLES: the rounds agree, so the choice does not matter much and the later
            # one carries the fresher market. Daniil's rule, and it is also the cheap answer.
            pick = max(tied, key=lambda z: z[1]['date_iso'])
        else:
            # AN ORDER OF MAGNITUDE APART: the rounds disagree because the company was a different
            # business at each one, and scale is what changed. Scale therefore leads HERE and only
            # here; everywhere else size stays out of selection entirely.
            frev = _f(prof.get('revenue'))
            fg = _f(prof.get('growth'))
            def dist(z):
                r = z[1]
                rrev, rg = _f(r.get('rev')), _f(r.get('growth_pct_at_round'))
                a = abs(math.log10(max(rrev, 1e-6)) - math.log10(max(frev, 1e-6))) if (frev and rrev) else None
                b = abs(rg - fg) / 100.0 if (fg is not None and rg is not None) else None
                # Scale first, then growth, then maturity as the age of the round. A missing field
                # never excludes a row: it drops to the back of that one key.
                return (a if a is not None else 9.0,
                        b if b is not None else 9.0,
                        -_date_key(r['date_iso']))
            pick = min(tied, key=dist) if (frev or fg) else max(tied, key=lambda z: z[1]['date_iso'])
        r = dict(pick[1])
        r['round_choice'] = _round_pick_reason([z[1] for z in tied], r, spread)
        r['round_alternatives'] = [
            {'date': z[1]['date'], 'mult': z[1].get('mult'), 'revenue_musd': z[1].get('rev')}
            for z in tied if z[1]['transaction_id'] != r['transaction_id']]
        out.append((pick[0], r))
    return sorted(out, key=lambda z: -z[0][0])


def _date_key(iso):
    try: return int(iso[:4]) * 12 + int(iso[5:7])
    except Exception: return 0

def select_private(prof, priv, want=5, window_months=24, asof=(2026, 8)):
    priv = same_family(prof, priv)                   # same gate on the private side
    priv = balance_sheet_compatible(prof, priv)      # lenders and non-lenders never mix
    pband = (prof.get('growth_band') or band_of(prof.get('growth'))).upper()
    if pband:
        priv = [r for r in priv if band_compatible(pband, r.get('growth_band'))] or priv
    scored = sorted(((score(prof, r, WP, use_fin=False), r) for r in priv), key=lambda z: -z[0][0])
    # CLOSE_MATCH_ONLY. A row whose denominator is a range rather than a figure earns its place
    # only where the business nature is genuinely close, which here means the row shares real
    # product language with the founder rather than merely landing in the same tier. Without
    # this a 25x-to-50x band would drift into sets it has no business informing.
    scored = [(sw, r) for (sw, r) in scored if r.get('display_gate') != 'NO_FIELD']
    scored = [(sw, r) for (sw, r) in scored
              if r.get('display_gate') != 'CLOSE_MATCH_ONLY'
              or _tag_points(sw[1]) >= FLOOR_TAG_EVIDENCE]
    pool = _one_round_per_company(prof, scored)
    # FILL, DO NOT STOP. Same rule as peer_groups: walk DIRECT then ADJACENT, keeping the order
    # so anchored names lead, and only fall to BROAD if neither pricing tier returns anything.
    cands, seen = [], set()
    for t in PRICING_TIERS:
        rows, _t = qualifying(pool, prof, only=t)
        for x in rows:
            if id(x) in seen: continue
            seen.add(id(x)); cands.append(x)
    if not cands:
        cands, _t = qualifying(pool, prof, only='BROAD')
    # BUSINESS NATURE LEADS, RECENCY ORDERS WITHIN IT. The widening window this replaces started
    # at 24 months and reached back only when it could not fill. That was fine while the candidate
    # list held one name, and broke the moment the ladder started filling: InsForge's only
    # anchored comparable, Algolia at Jul-2021, was pushed out by five adjacent names from the
    # last two years. Recency had quietly become a selection criterion, which is the same mistake
    # as letting size be one.
    #
    # So the order is tier first, then date within tier. A DIRECT name is never displaced by a
    # more recent ADJACENT one. `months` is no longer an input the loop widens; it is an output,
    # the age of the OLDEST transaction actually shown, so the reveal can caveat it honestly.
    ordered = sorted(cands, key=lambda z: (_TIER_ORDER[_tier(prof, z[1], z[0][1])],
                                           _neg_date(z[1]['date_iso'])))[:want]
    if not ordered: return [], window_months, 'NONE'
    oldest = min(c[1]['date_iso'] for c in ordered)
    y, m = int(oldest[:4]), int(oldest[5:7])
    months = max(0, (asof[0] - y) * 12 + (asof[1] - m))
    return ordered, months, set_tier(prof, ordered)


# ---------------------------------------------------------------------------
# CORE AND SECONDARY PEER GROUPS
#   Axis A, WHAT IT DOES     archetype, function, product tags, revenue model
#   Axis B, WHO IT SELLS TO  end market and end customer
#   CORE      strong on both.   SECONDARY strong on A, different on B.
# ---------------------------------------------------------------------------
def peer_groups(prof, universe, scorer=None, want=5):
    scorer = scorer or (lambda p, r: score(p, r))
    universe = same_family(prof, universe)          # gate on business nature before ranking on detail
    universe = balance_sheet_compatible(prof, universe)   # same rule on the listed lane
    scored = sorted(((scorer(prof, r), r) for r in universe), key=lambda z: -z[0][0])

    # AXIS B, WHO IT SELLS TO. Corrected 25-Aug-2026 against Daniil's own comp picks.
    #
    # The old rule demanded exact industry equality, which meant a HORIZONTAL peer could never be
    # core for a vertical profile. That is what buried Sprout Social. It is the engine's own
    # top-scored name for Honestly at 12.4, ahead of everything actually shown, and it was forced
    # into secondary because Honestly is tagged Retail & E-commerce and Sprout Social is Horizontal.
    #
    # Horizontal is not a DIFFERENT end market. It is no particular one, so it serves this
    # founder's market along with every other. A horizontal peer therefore belongs in core when it
    # otherwise qualifies. The same reasoning already governs the family gate's end-market bridge.
    #
    # A HORIZONTAL profile keeps the stricter test, peer also horizontal and the same buyer,
    # because for a horizontal founder the end customer is the only thing narrowing the field.
    # ONE MORE ROUTE THROUGH AXIS B: REAL PRODUCT EVIDENCE. Added 26-Aug-2026 alongside the
    # relevance gate, because the two together emptied OpenSEO's listed core set. OpenSEO is
    # Horizontal, so axis B demanded a horizontal peer with the SAME END CUSTOMER, and Similarweb
    # sells to a line of business while OpenSEO sells to developers. Similarweb shares two exact
    # product tags with it, Keyword Research and Rank Tracking, and is plainly its closest listed
    # comparable. Being told who someone sells to is a proxy for what they do; sharing the product
    # vocabulary is the thing itself, so it should not lose to its own proxy.
    def axis_b(r, why=None):
        ri, pi = (r.get('industry') or '').strip(), (prof.get('industry') or '').strip()
        if pi == 'Horizontal':
            return ((ri == 'Horizontal' and _eq(prof, r, 'buyer'))
                    or _tag_points(why or []) >= FLOOR_TAG_EVIDENCE)
        return bool(ri) and (ri == pi or ri == 'Horizontal')

    def axis_a(r):
        a = {r['archetype'], r.get('archetype_secondary') or ''}
        mine = {prof['archetype'], prof.get('archetype_secondary') or ''} - {''}
        return bool(a & mine) or _eq(prof, r, 'function')

    # WIDEN ONLY AFTER THE CORE/SECONDARY SPLIT, not before. Deciding the tier first and then
    # splitting threw away real DIRECT hits: a social-listening profile lost Rezolve AI and Klaviyo
    # because the DIRECT tier's members happened to fail the end-market axis, leaving the core group
    # empty even though the tier was non-empty. So walk the tiers and FILL the core group, taking
    # DIRECT names first and topping up from ADJACENT, rather than stopping at the first tier that
    # produces a single name. See the note above set_tier for why.
    core, seen = [], set()
    for tier in PRICING_TIERS:
        rows, _got = qualifying(scored, prof, only=tier)
        for x in rows:
            if len(core) >= want: break
            if id(x) in seen: continue
            if axis_a(x[1]) and axis_b(x[1], x[0][1]):
                seen.add(id(x)); core.append(x)
        if len(core) >= want: break
    if not core:
        rows, _got = qualifying(scored, prof, only='BROAD')
        core = [x for x in rows if axis_a(x[1]) and axis_b(x[1], x[0][1])][:want]
    if core:
        # NOTHING THAT QUALIFIES MAY VANISH. The old split put a row in secondary only if it
        # passed axis_a, so a name failing axis_a appeared in NEITHER group and was dropped in
        # silence. Cloudflare scores 12.9 against InsForge, higher than the Elastic that was
        # returned, and appeared nowhere at all. A row that cleared the score floor AND the
        # anchoring test is related to this founder by construction; if it is not core it is
        # secondary. It never disappears.
        # SECONDARY IS THE WIDER RING AND MUST BE DRAWN WIDER. It was being taken from the same
        # tier as core, so when core came from the DIRECT tier the secondary group could only
        # contain other DIRECT names, and there are rarely any. That is why Honestly showed one
        # company: Yext, HubSpot, Braze and Zeta Global all scored well, all sit in the same
        # archetype, and all were unreachable because they are not DIRECT-anchored.
        #
        # A banker's comp set is a tight core and a looser ring around it. So core is filled from
        # the pricing tiers in order, and secondary is everything else in the family that clears
        # the floor. The tier label still describes CORE, which is what the range is computed from.
        picked = {id(x) for x in core}
        wide, _wt = qualifying(scored, prof, only='BROAD')
        secondary = [x for x in wide if id(x) not in picked][:want]
        return core, secondary, set_tier(prof, core)
    return [], [], 'NONE'


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

# ---------------------------------------------------------------------------
# BALANCE-SHEET COMPANIES ARE PRICED ON A DIFFERENT AXIS
#
# Daniil, 27-Aug-2026: wire price to book and price to earnings into the football field FOR
# LENDERS AND BALANCE-SHEET-DRIVEN COMPANIES ONLY. Ecommerce, marketplaces, payments and software
# do not trade on book value or on net income, and must never be fed these.
#
# The reason a lender needs its own axis: revenue contains interest earned on BORROWED money, so
# it scales with leverage rather than with value, and enterprise value adds back the debt that IS
# the product. Our own listed pull proves the damage. Multitude AG returns a NEGATIVE enterprise
# value and therefore a negative multiple; Japan Post minus $105bn. OSB Group shows a 2% gross
# margin and 168x EV/gross profit, Banca IFIS 262x, Cholamandalam 239x. All artefacts of a screen
# putting gross interest income on the revenue line and interest expense in cost of revenue.
#
# Book value rather than the loan book, because book value nets the funding off the assets. Two
# lenders with the same loan book and different leverage would read identically on a loan-book
# multiple and correctly differently on price to book.
BALANCE_SHEET_ARCHETYPES = ('Lending & Credit', 'Digital Bank & Deposits')

def is_balance_sheet(prof):
    """True when this company is priced on its balance sheet rather than its revenue."""
    a = {prof.get('archetype'), prof.get('archetype_secondary')} - {None, ''}
    return bool(a & set(BALANCE_SHEET_ARCHETYPES))

def basis_for(prof):
    return 'BOOK' if is_balance_sheet(prof) else 'REVENUE'

# private lane key, listed lane key, and what the reveal should call it
BASIS_KEYS = {'BOOK':    ('mult_book', 'pb_mult', 'price to book'),
              'REVENUE': ('mult',      'mult',    'enterprise value to revenue')}

def denominator(prof, group):
    """Return ('gp'|'rev', reason). Gross profit leads when the subject's margin
    sits more than MARGIN_GAP points from the peer group median, or when the group
    itself spans more than 30 points of margin."""
    if is_balance_sheet(prof):
        return 'rev', ('a lender is priced on its book rather than its revenue, because revenue '
                       'scales with how much it has borrowed')
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

# A BROAD SET IS CONTEXT, NEVER A NUMBER.
#
# Daniil, 25-Aug-2026: a BROAD set may be shown, but it must not reach the football field.
# The reason is not squeamishness about the label. A consumer language-learning app and Huel
# share a family and nothing else that governs a multiple: different business model, different
# gross margin, different scalability. Putting their multiples in the same bar would not be a
# wide range, it would be a meaningless one, and a founder cannot tell the difference by looking.
#
# So the ladder splits into two jobs. DIRECT and ADJACENT sets price. A BROAD set is shown as
# "how this corner of the market trades", named companies and all, and computes no range.
RANGE_TIERS = ('DIRECT', 'ADJACENT')

# ONE COMPANY IS A DIAMOND, NOT A BAR.
#
# Gating BROAD exposed the same deception one layer down. Nine of the twenty-one real profiles
# drew a football field from fewer than three names and six drew one from a SINGLE name: Honen's
# "4.4x to 4.4x" is Duolingo and nothing else; Honestly's "2.7x to 2.7x" is Rezolve AI. A bar
# implies a distribution. Drawn from one observation there is no distribution, and the picture
# beats any caption you put under it.
#
# Daniil, 25-Aug-2026: draw it as a DIAMOND rather than a range, name the single comparable, and
# caveat it. Resolve it over time with more data, better tags and live traffic rather than by
# hiding it. So the range carries its own display instruction:
#
#   display DIAMOND  exactly one priced comparable. Draw a point, name it, caveat it.
#   display RANGE    two or more. Draw a bar.
#   thin             fewer than three. True for a two-name bar as well, so the copy can hedge.
#
# `sole` names the single company so the reveal never has to reach back into the group to find it.
# TRIANGULATION IS AN ANSWER, BUT IT HAS TO SAY SO.
#
# Daniil, 26-Aug-2026: "If nothing matches very closely, we need to broaden the set and
# triangulate between most similar comps." Agreed, and the broadening is what the filling ladder
# above now does. The remaining job is to say which kind of answer the founder is looking at.
#
# Publora is the case. A social-media publishing API draws five private names of which the best
# scores 0.3 on product tags and the other four score 0.0. They qualify on archetype, buyer,
# go-to-market and revenue model: every one is developer-facing, consumption-priced
# infrastructure. That is a real similarity and it is not a product similarity, and a bar drawn
# from it is a triangulation rather than a comparable set.
#
# So every range carries two extra facts:
#   tag_evidence   the best product-tag score among the rows that actually feed the number
#   triangulated   True when that best score is below FLOOR_TAG_EVIDENCE, meaning NOT ONE
#                  contributing company shares real product vocabulary with this founder
#
# The copy owes the founder a different sentence in that case. It is still the best answer we
# have; it is not the same claim.
# AND ONE MORE THING THE FOUNDER HAS TO BE TOLD: WHEN THE CLOSEST NAME DOES NOT PRICE.
#
# OpenSEO is the case that forced this. Its best private comparable is Semrush at 12.0 tag points,
# a perfect match, and Semrush is named at the top of the set. But Semrush's only transaction is
# the Adobe take-private, which is a CONTROL deal and can never sit in a median of minority
# financings. So the number the founder sees is built from Clay at 50.0x and Klaviyo at 32.6x,
# neither of which shares a single product tag with them, while the one name they would recognise
# as their comparable contributes nothing. Showing that without saying it would be the worst kind
# of quiet dishonesty: the set looks authoritative precisely because of the name that is not in it.
# HOW CLOSE, NOT PASS OR FAIL. Reworked 27-Aug-2026.
#
# Daniil: "What do you mean no contributing company shares real vocabulary with the founder? Means
# no 100% coincidences? As I mentioned, this is ok, we need to look for CLOSEST peers possible, if
# 100% coincidence is not available."
#
# He is right and the old flag was mislabelling its own data. `triangulated` fired whenever no
# contributing row scored 3.0 on product tags, and 3.0 means one EXACT tag match. So BrowserAct was
# flagged the same way as Goldfish, even though BrowserAct's comparables share ten tokens with it
# (agent, ai, api, browser, code, proxy, scraper, scraping, web, no-code) and Goldfish's share
# exactly one, "ai". Calling both of those "no shared vocabulary" was wrong about the first and
# useless for telling them apart.
#
# So closeness is now GRADED on what the contributing rows actually share:
#
#   SHARED_PRODUCT   an exact product tag in common. openseo, bluerails, insforge.
#   STRONG_OVERLAP   four or more shared words. browseract, agentx, context-dev, elentaria, pazi.
#   PARTIAL_OVERLAP  two or three. anysearch, bond, fyle, upstream, publora, sellerclaw, skybridge.
#   THIN_OVERLAP     one or none, and usually a generic one like "ai". fundraisly, goldfish,
#                    mailwarm, honestly, acti. These are the sets that genuinely deserve a caveat.
#
# `triangulated` survives as an alias for THIN_OVERLAP only, so it now means what its name says.
CLOSENESS = ('SHARED_PRODUCT', 'STRONG_OVERLAP', 'PARTIAL_OVERLAP', 'THIN_OVERLAP')

def _shared_tokens(prof, rows):
    mine = toks(prof.get('product_tags') or '')
    out = set()
    for (_sw, r) in rows:
        out |= (mine & toks(r.get('product_tags') or ''))
    return out

def _closeness(points, shared_n):
    if points >= FLOOR_TAG_EVIDENCE: return 'SHARED_PRODUCT'
    if shared_n >= 4: return 'STRONG_OVERLAP'
    if shared_n >= 2: return 'PARTIAL_OVERLAP'
    return 'THIN_OVERLAP'

def _evidence(contributing, whole=None, prof=None):
    """Both arguments are lists of ((score, why), record).
    Returns (best tag points among the rows that feed the number, closeness, anchor_dropped,
    the shared words themselves)."""
    def best(rows): return max([_tag_points(why) for (_sc, why), _r in rows] or [0.0])
    b = best(contributing)
    w = best(whole) if whole is not None else b
    shared = sorted(_shared_tokens(prof, contributing)) if prof is not None else []
    return round(b, 1), _closeness(b, len(shared)), (b < FLOOR_TAG_EVIDENCE <= w), shared


# A CONTROL DEAL IS A BENCHMARK. IT IS ALSO A PREMIUM. BOTH FACTS TRAVEL.
#
# Daniil, 26-Aug-2026: "Why are you excluding take private from the median? In the absence of clean
# comps, we should not exclude data based on the fact that this was a controlled deal. We should
# have the respective note (visible when someone hovers over the range), but we should not exclude
# this entirely."
#
# Right, and it is the fourth instance of the same principle as the three rules settled the day
# before: replace an exclusion with a label. OpenSEO was the proof. Semrush is its best comparable
# by a distance, matching at 12.0 tag points, and Semrush's only transaction is the Adobe
# take-private. Under the old rule the founder saw Semrush named at the top of the set and a range
# built from Clay at 50.0x and Klaviyo at 32.6x, neither of which shares a tag with them. Excluding
# the one relevant data point made the answer worse AND less honest.
#
# What does not change: a buyer of the whole company pays for control, so a control multiple sits
# above what the same business would fetch in a minority round. The range therefore carries how
# many of its contributors are control deals and which they are, and the reveal must surface that
# on the name rather than bury it in a footnote.
# A BAR THAT SPANS 4x TO 105x IS NOT A RANGE. IT IS TWO ANSWERS.
#
# Daniil, 26-Aug-2026: "What drives such a huge delta in comps multiples? Are we 100% sure these
# are comparable? Was there differential in growth? Showing such a huge range is not an option
# really, defeats the whole purpose. For now as temporary fix, let's show separate diamonds with
# annotation, but we need to investigate the source of the discrepancy."
#
# The investigation, on Pazi: the band runs Semrush 4.3x, Notion 18.0x, Clay 50.0x, Sierra 105.3x,
# Decagon 150.0x. Product-tag evidence across the whole set is 0.1 to 0.8, meaning they share the
# token "AI" and almost nothing else. And the spread is a GROWTH spread, not a business-model
# spread: Semrush is a mature SEO suite taken private, Sierra and Decagon went from nothing to
# nine-figure ARR inside two years. On the listed side we can measure exactly this effect, and it
# is the largest single driver we have: the fastest quarter of 164 software names trades at 8.3x
# and the slowest at 2.3x.
#
# THE ROOT CAUSE IS THAT THE PRIVATE LANE IS BLIND TO GROWTH. `WP` sets growth=0 and
# profitability=0 and select_private calls score with use_fin=False, because the private rows
# carry no growth field at all. So the one variable that best explains the spread is the one
# variable the private matcher cannot see. Fixing that means adding growth to the private rows
# wherever it was disclosed, and it is the next real piece of work on this engine.
#
# UNTIL THEN, SAY IT RATHER THAN AVERAGE IT. Where the band's own high is more than DISPERSION_MAX
# times its low, we stop drawing a bar and draw each contributor as its own diamond, named, with
# its multiple. Measured across the 21 real profiles the spreads cluster between 1.7x and 4.9x;
# Pazi at 24.5x and Fundraisly at 11.6x are the only two outside that, so 6.0 separates the
# genuine ranges from the non-ranges without catching anything healthy.
DISPERSION_MAX = 6.0

def _control(rows):
    names = [r.get('company_name', '') for (_sw, r) in rows
             if (r.get('transaction_type') or '').strip() == 'CONTROL']
    return len(names), names


# A TAKE-PRIVATE OF A LISTED COMPANY IS A PUBLIC-MARKET PRICE.
#
# This is what actually explains Pazi, and growth does not. Pazi's band ran Semrush 4.3x against
# Sierra 105.3x and Decagon 150.0x. Semrush was growing 15% and the venture names 100% and more, so
# the growth gate labels them one band apart and correctly leaves them together. The real difference
# is that Semrush was NYSE-listed and Adobe bought it at the multiple the public market was already
# paying, while the others are private rounds negotiated with one investor. Those are different
# kinds of price, not fast and slow versions of the same kind.
#
# So the range carries how many of its contributors were listed targets, and the reveal must say it
# on the name. Not excluded: Daniil's rule is that a control deal is a benchmark and it prices.
# LIKE FOR LIKE, OR SAY SO.
#
# Daniil, 26-Aug-2026: "We should just be asking for the same metric we store in our database. We
# should be asking for a like for like one." Right, and the precondition is knowing what we store,
# which until today we did not: `revenue_metric` was free text and the basis lived in prose.
#
# Every private row now carries revenue_basis: ARR, ARR_RUNRATE, NET_REVENUE, GROSS_REVENUE,
# BANK_NOI or NONE. Across the 58 rows that actually price, 24 are contracted ARR, 6 are a run rate,
# 24 are net revenue, 2 are a bank revenue line before credit losses, and ONE is gross sales. That
# last one is OLIPOP, the only priced consumer row on a gross basis while every other one is net,
# and it is exactly the comparison this field exists to catch.
#
# So the range reports the mix of bases behind it. If a founder gives us ARR and the number they are
# shown was built from gross sales, the copy owes them that sentence.
def _basis_mix(rows):
    m = {}
    for (_sw, r) in rows:
        b = r.get('revenue_basis') or 'UNKNOWN'
        m[b] = m.get(b, 0) + 1
    return m

def _listed_targets(rows):
    names = [r.get('company_name', '') for (_sw, r) in rows if r.get('target_was_listed')]
    return len(names), names

# YOU CANNOT AVERAGE 4.3x AND 50x.
#
# Daniil, 26-Aug-2026, on OpenSEO: "If the closest peer reads 4.3x, this is what needs to be shown
# (as a diamond). THEN if some other peers (with lower relevance) trade higher, we could show them
# separately at the end of the field with indication of their multiples, indicating that we can
# position towards them with right arguments. We cannot take an average of 4.3x and 50x, this
# discredits the whole range."
#
# He is right and it is the flaw in the filling ladder as I first built it. Filling the SET was
# correct; letting the whole filled set compute ONE number was not. OpenSEO's set is Semrush at
# 4.3x, which is its business almost exactly, plus Clay at 50.0x, Klaviyo at 32.6x and Apollo.io
# at 16.0x, which are adjacent at best. Blending those gave a midpoint of 32.6x, a number no
# banker would put their name to and no founder should be shown.
#
# So the range is computed from the CLOSEST BAND THAT HAS A PRICE, and nothing weaker joins it.
# Everything priced in a weaker band becomes `positioning`: named, with its multiple, drawn at the
# end of the field rather than inside the bar. That is not a demotion, it is the real argument. A
# founder who can show why they belong nearer Clay than Semrush has a case to make, and the field
# should hand them the case rather than quietly average it away.
def _bands(prof, priced):
    """Split priced rows into the closest band that has any, and everything weaker.
    Returns (band_tier, headline_rows, positioning_rows)."""
    by = {}
    for (sw, r) in priced:
        by.setdefault(_tier(prof, r, sw[1]), []).append((sw, r))
    order = ('DIRECT', 'ADJACENT', 'BROAD')
    for i, t in enumerate(order):
        if by.get(t):
            weaker = [x for tt in order[i+1:] for x in by.get(tt, [])]
            return t, by[t], weaker
    return 'NONE', [], []

def _positioning(prof, rows, key):
    out = [{'company': r.get('company_name', ''), 'mult': r[key],
            'tier': _tier(prof, r, sw[1]),
            'transaction_type': r.get('transaction_type', ''),
            'reason': why_text(prof, r, sw[1])} for (sw, r) in rows if r.get(key) is not None]
    return sorted(out, key=lambda z: z['mult'])

def group_range(prof, group, which='rev', tier='DIRECT'):
    """Quartile range of the group, excluding rows flagged out of medians.
    Returns None for a BROAD group: it is context, not a price."""
    if tier not in RANGE_TIERS: return None
    key = BASIS_KEYS['BOOK'][1] if is_balance_sheet(prof) else ('mult' if which == 'rev' else 'gp_mult')
    allpriced = [(sw, r) for (sw, r) in group if r.get(key) is not None and r.get('in_medians', True)]
    if not allpriced: return None
    band, priced, weaker = _bands(prof, allpriced)
    v = sorted(r[key] for _sw, r in priced)
    n = len(v)
    ev, close, dropped, shared = _evidence(priced, group, prof)
    dispersed = n >= 2 and v[0] > 0 and (v[-1] / v[0]) > DISPERSION_MAX
    out = dict(n=n, low=v[max(0, (n-1)//4)], mid=st.median(v), high=v[min(n-1, (3*(n-1))//4 + 1)],
               display=('DIAMOND' if n == 1 else ('SCATTER' if dispersed else 'RANGE')),
               dispersed=dispersed, spread=round(v[-1] / v[0], 1) if v[0] else None,
               points=(_positioning(prof, priced, key) if dispersed else []), thin=n < 3,
               bounded=any((r.get('bound') or '').strip() == '<=' for _sw, r in priced),
               tag_evidence=ev, closeness=close, shared_words=shared,
               triangulated=(close == 'THIN_OVERLAP'), anchor_dropped=dropped,
               control_n=_control(priced)[0], control_names=_control(priced)[1],
               listed_target_n=_listed_targets(priced)[0], listed_target_names=_listed_targets(priced)[1],
               basis_mix=_basis_mix(priced),
               band=band, positioning=_positioning(prof, weaker, key))
    if n == 1:
        out['sole'] = priced[0][1].get('company_name', '')
    return out

def private_range(prof, picked, tier):
    """The same rule on the private lane, kept here rather than in the caller so the two cannot
    drift apart. BROAD returns nothing; a single priced round returns a diamond."""
    if tier not in RANGE_TIERS: return {}
    basis = basis_for(prof)
    key = BASIS_KEYS[basis][0]
    allpriced = [(sw, r) for (sw, r) in picked if r.get('in_medians') and r.get(key)]
    if not allpriced: return {}
    band, priced, weaker = _bands(prof, allpriced)
    v = sorted(r[key] for _sw, r in priced)
    n = len(v)
    ev, close, dropped, shared = _evidence(priced, picked, prof)
    # A CEILING DRAWN AS A POINT IS THE DIAMOND'S OWN VERSION OF THE BAR PROBLEM. After the
    # software verification pass, Mailwarm's private lane is a single diamond at 105.3x, which is
    # Sierra, whose ARR is a 'more than $150m' threshold three months stale at pricing. Drawing
    # that as a point is exactly the overstatement the ladder was built to stop, so the range
    # carries whether any contributing row is bounded and the copy must say "at most".
    dispersed = n >= 2 and v[0] > 0 and (v[-1] / v[0]) > DISPERSION_MAX
    out = dict(n=n, low=min(v), mid=v[n // 2], high=max(v),
               display=('DIAMOND' if n == 1 else ('SCATTER' if dispersed else 'RANGE')),
               dispersed=dispersed, spread=round(v[-1] / v[0], 1) if v[0] else None,
               points=(_positioning(prof, priced, key) if dispersed else []), thin=n < 3,
               bounded=any((r.get('bound') or '').strip() == '<=' for _sw, r in priced),
               tag_evidence=ev, closeness=close, shared_words=shared,
               triangulated=(close == 'THIN_OVERLAP'), anchor_dropped=dropped,
               control_n=_control(priced)[0], control_names=_control(priced)[1],
               listed_target_n=_listed_targets(priced)[0], listed_target_names=_listed_targets(priced)[1],
               basis_mix=_basis_mix(priced),
               basis=basis, basis_label=BASIS_KEYS[basis][2],
               band=band, positioning=_positioning(prof, weaker, key))
    if n == 1:
        out['sole'] = priced[0][1].get('company_name', '')
    return out


# ---------------------------------------------------------------------------
# REGRESSION ON GROWTH: THE METHOD THAT HANDLES A DIFFERENT GROWTH PROFILE
#
# Daniil, 26-Aug-2026: "Build a regression with larger than usual 5 set of peers (taking other
# close peers that did not make into 5), build regression of multiple vs growth, apply user's
# given annual growth +/-10%, and infer the range of multiples that way. Important to make sure
# R2 is above 50% at least for the regression we build."
#
# This is the honest answer to the problem the comp set cannot solve on its own. A founder growing
# 74% against peers growing 11% is not worth the peer median, and no amount of peer selection fixes
# that: the peers are the right businesses at the wrong speed. A regression prices the difference
# instead of arguing about it, which is exactly what a banker does with a scatter and a trendline.
#
# THE R2 BAR IS NOT A FORMALITY, IT IS THE POINT. Measured across the 21 real profiles:
#   whole listed software universe, EV/revenue on growth   R2 = 40%   FAILS
#   the same, trimmed of the top and bottom 5%             R2 = 27%   FAILS
#   by archetype: Business Applications 15%, Vertical 26%, Data/AI/Dev 85%
#   the founder's OWN top 15 relevant peers                clears 50% for 6 of the 21
# So a regression built on a broad "software" bucket is worthless, and a regression built on a
# tight, relevant set is often excellent. R2 therefore doubles as a TEST OF THE PEER SET: if the
# multiples of the companies we chose cannot be explained by their growth, we do not have a
# coherent set and we should not draw a line through it. Below the bar we return nothing and the
# reveal simply omits the row.
#
# The peer set is deliberately WIDER than the football field's five, because a regression needs
# points. It is the same ranking, taken further down.
REGRESSION_N = 15
REGRESSION_MIN_POINTS = 6
REGRESSION_MIN_R2 = 0.50
REGRESSION_GROWTH_SPAN = 0.10          # the founder's growth rate plus and minus a tenth of itself

# AND A LINE IS ONLY EVIDENCE INSIDE THE RANGE IT WAS FITTED ON.
#
# Found the moment the first version ran. A founder growing 74% against listed software peers whose
# fastest name grows about 26% produced implied multiples of 27x to 39x, because the fit was being
# extrapolated to nearly three times the highest growth rate any peer actually exhibits. The R2 was
# excellent and the answer was fiction. The banker's chart this method copies reads its range at
# 17% to 22% growth, comfortably inside a cloud of points spanning 3% to 30%; it does not run the
# line off the edge of the page.
#
# So the founder's growth must sit inside the peer set's own growth range, or no more than
# EXTRAPOLATION_LIMIT beyond its top. Outside that we return nothing, and the honest reason is
# worth showing the founder: at that growth rate there is no listed company to regress them
# against. That is a data gap with a name, not a failure of method, and the private lane is where
# it gets resolved once more rounds carry a growth rate.
EXTRAPOLATION_LIMIT = 0.25

def _ols(xs, ys):
    n = len(xs)
    if n < REGRESSION_MIN_POINTS: return None
    mx, my = sum(xs)/n, sum(ys)/n
    sxx = sum((x-mx)**2 for x in xs)
    sst = sum((y-my)**2 for y in ys)
    if sxx == 0 or sst == 0: return None
    b = sum((x-mx)*(y-my) for x, y in zip(xs, ys)) / sxx
    a = my - b*mx
    ssr = sum((y-(a+b*x))**2 for x, y in zip(xs, ys))
    return a, b, 1 - ssr/sst

def regression_range(prof, universe, which='rev', want=REGRESSION_N):
    """Fit EV/denominator against growth across the founder's own extended peer set, then read the
    range off the line at their growth rate. Returns None when the fit is too weak to publish."""
    growth = prof.get('growth')
    if growth is None: return None
    univ = same_family(prof, universe)
    scored = sorted(((score(prof, r), r) for r in univ), key=lambda z: -z[0][0])
    scored = [x for x in scored if _relevant(prof, x[1], x[0][1])][:want]
    key = 'mult' if which == 'rev' else 'gp_mult'
    pts = [(r['g'], r[key], r) for _s, r in scored if r.get('g') is not None and r.get(key) is not None]
    fit = _ols([p[0] for p in pts], [p[1] for p in pts])
    if not fit: return None
    a, b, r2 = fit
    if r2 < REGRESSION_MIN_R2: return None
    gs = [p[0] for p in pts]
    lo_g, hi_g = growth*(1-REGRESSION_GROWTH_SPAN), growth*(1+REGRESSION_GROWTH_SPAN)
    ceiling = max(gs) * (1 + EXTRAPOLATION_LIMIT)
    floor = min(gs) - abs(min(gs)) * EXTRAPOLATION_LIMIT - 5.0
    if hi_g > ceiling or lo_g < floor:
        return dict(refused='OUT_OF_RANGE', n=len(pts), r2=round(r2, 3), growth=growth,
                    peer_growth_low=round(min(gs), 1), peer_growth_high=round(max(gs), 1),
                    denominator=which)
    v = sorted([a + b*lo_g, a + b*hi_g])
    if v[1] <= 0: return None                      # a downward line can imply a negative multiple
    return dict(n=len(pts), r2=round(r2, 3), intercept=round(a, 3), slope=round(b, 4),
                denominator=which, growth=growth, growth_low=round(lo_g, 1), growth_high=round(hi_g, 1),
                low=round(max(0.0, v[0]), 1), mid=round((v[0]+v[1])/2, 1), high=round(v[1], 1),
                peers=[{'company': r['company_name'], 'ticker': r.get('exchange_ticker', ''),
                        'growth': r['g'], 'mult': r[key]} for _g, _m, r in pts])
