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

def qualifying(scored, prof=None, gate=FLOOR_ADEQUATE, only=None):
    """Returns (rows, tier). tier is DIRECT, ADJACENT, BROAD or NONE.
    `only` restricts to one tier; otherwise the best tier with members wins."""
    if not scored: return [], 'NONE'
    if prof is None:
        cut = max(FLOOR_REL * scored[0][0][0], FLOOR_ABS)
        return [x for x in scored if x[0][0] >= cut], 'DIRECT'
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

def _neg_date(d):
    """Sort key that puts the most recent date first while the key beside it sorts ascending."""
    return tuple(-int(x) for x in (d[:4], d[5:7]))

def select_private(prof, priv, want=5, window_months=24, asof=(2026, 8)):
    priv = same_family(prof, priv)                   # same gate on the private side
    scored = sorted(((score(prof, r, WP, use_fin=False), r) for r in priv), key=lambda z: -z[0][0])
    best = {}
    for (sc, why), r in scored:
        k = r['company_key']
        if k not in best or r['date_iso'] > best[k][1]['date_iso']:
            if k not in best or sc >= best[k][0][0]: best[k] = ((sc, why), r)
    pool = sorted(best.values(), key=lambda z: -z[0][0])
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
    def axis_b(r):
        ri, pi = (r.get('industry') or '').strip(), (prof.get('industry') or '').strip()
        if pi == 'Horizontal':
            return ri == 'Horizontal' and _eq(prof, r, 'buyer')
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
            if axis_a(x[1]) and axis_b(x[1]):
                seen.add(id(x)); core.append(x)
        if len(core) >= want: break
    if not core:
        rows, _got = qualifying(scored, prof, only='BROAD')
        core = [x for x in rows if axis_a(x[1]) and axis_b(x[1])][:want]
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
def _evidence(contributing, whole=None):
    """Both arguments are lists of ((score, why), record).
    Returns (best tag points AMONG THE ROWS THAT FEED THE NUMBER, triangulated, anchor_dropped)."""
    def best(rows): return max([_tag_points(why) for (_sc, why), _r in rows] or [0.0])
    b = best(contributing)
    w = best(whole) if whole is not None else b
    return round(b, 1), b < FLOOR_TAG_EVIDENCE, (b < FLOOR_TAG_EVIDENCE <= w)

def group_range(group, which='rev', tier='DIRECT'):
    """Quartile range of the group, excluding rows flagged out of medians.
    Returns None for a BROAD group: it is context, not a price."""
    if tier not in RANGE_TIERS: return None
    key = 'mult' if which == 'rev' else 'gp_mult'
    priced = [(sw, r) for (sw, r) in group if r.get(key) is not None and r.get('in_medians', True)]
    if not priced: return None
    v = sorted(r[key] for _sw, r in priced)
    n = len(v)
    ev, tri, dropped = _evidence(priced, group)
    out = dict(n=n, low=v[max(0, (n-1)//4)], mid=st.median(v), high=v[min(n-1, (3*(n-1))//4 + 1)],
               display='DIAMOND' if n == 1 else 'RANGE', thin=n < 3,
               bounded=any((r.get('bound') or '').strip() == '<=' for _sw, r in priced),
               tag_evidence=ev, triangulated=tri, anchor_dropped=dropped)
    if n == 1:
        out['sole'] = priced[0][1].get('company_name', '')
    return out

def private_range(picked, tier):
    """The same rule on the private lane, kept here rather than in the caller so the two cannot
    drift apart. BROAD returns nothing; a single priced round returns a diamond."""
    if tier not in RANGE_TIERS: return {}
    priced = [(sw, r) for (sw, r) in picked if r.get('in_medians') and r.get('mult')]
    if not priced: return {}
    v = sorted(r['mult'] for _sw, r in priced)
    n = len(v)
    ev, tri, dropped = _evidence(priced, picked)
    # A CEILING DRAWN AS A POINT IS THE DIAMOND'S OWN VERSION OF THE BAR PROBLEM. After the
    # software verification pass, Mailwarm's private lane is a single diamond at 105.3x, which is
    # Sierra, whose ARR is a 'more than $150m' threshold three months stale at pricing. Drawing
    # that as a point is exactly the overstatement the ladder was built to stop, so the range
    # carries whether any contributing row is bounded and the copy must say "at most".
    out = dict(n=n, low=min(v), mid=v[n // 2], high=max(v),
               display='DIAMOND' if n == 1 else 'RANGE', thin=n < 3,
               bounded=any((r.get('bound') or '').strip() == '<=' for _sw, r in priced),
               tag_evidence=ev, triangulated=tri, anchor_dropped=dropped)
    if n == 1:
        out['sole'] = priced[0][1].get('company_name', '')
    return out
