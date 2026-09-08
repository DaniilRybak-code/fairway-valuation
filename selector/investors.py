# -*- coding: utf-8 -*-
"""Who to call, and who paid up for businesses like yours. Two layers, kept apart on purpose.

Fable's roadmap of 2-Sep, Day 2. The table was built on Day 1 and has sat unmatched since: nothing
turned 408 investor rows into a list for a founder, so the feature promised on the landing page had
a database behind it and no machinery.

TWO LAYERS, AND THE SEPARATION IS THE DESIGN DECISION.

  CALLABLE  "Writing first cheques in your sector right now." Curated, and every row must carry a
            dated deal, a cheque range, a sector in our own archetype vocabulary and a geography.
            A row missing any of those does not render, on the same discipline as a comparable with
            no source: it does not exist.
  EVIDENCE  "The houses behind your reference rounds." Generated from the founder's OWN selected
            comparables, so the investors arrive attached to the evidence that built the field.
            Nobody can copy this layer, because it falls out of the selector.

Fable: "vcconf's failure mode is stale investors; ours would be aspirational ones." So the evidence
layer is labelled as a map of who pays up for businesses like this, never as a call list, and the
two are never merged.

DEGRADATION IS LABELLED, NEVER SILENT. Exact stage, sector and geography first; then sector or
geography agnostic houses; then any two of the three. Each step carries its own label so a founder
can see how far we reached. And the list is NEVER PADDED to a fixed count: six good matches beat
twelve loose ones.
"""
import collections
import csv
import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(os.path.dirname(HERE), 'data') + os.sep


def _rows(path):
    return list(csv.DictReader([l for l in io.open(path, encoding='utf-8')
                                if not l.startswith('#')]))


def _f(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# ONE VOCABULARY, WRITTEN TWO WAYS, AND THE SECOND ONE WAS INVISIBLE.
#
# Daniil, 4-Sep-2026: fix the investor sector column, and do not break peer selection doing it.
#
# A house reaches a founder when the founder's ARCHETYPE appears in the house's
# screening_categories, matched as an exact string. The archetypes come from our tag files
# ("Insurance Technology", "Consumer & Prosumer Software"). The screening categories came partly
# from the same vocabulary and partly from the enrichment pulls, which wrote the market in their
# own words ("Insurance", "Personal Software / Productivity"). The two never meet, and no error is
# ever raised: the house simply never matches anybody. Nine houses are tagged Insurance and
# `florin`, an insurance carrier, was shown none of them. It is the geography substring bug of
# 3-Sep in a different costume, and the same lesson: a facet that silently scores nothing looks
# exactly like a thin database.
#
# THE TRANSLATION IS HERE AND NOT IN THE FILE, on purpose. Rewriting data/investors.csv would
# destroy the evidence of what each pull actually said, and the file is the audit trail. The
# original name is kept alongside the archetype it maps to, so an exact match that already worked
# still works and nothing that matched before can stop matching.
#
# THIS CANNOT TOUCH PEER SELECTION. screening_categories exists in exactly one module, this one:
# match_reference.py never reads it, has no import of investors.py, and its own archetypes come
# from the tag files. Comparable selection is unchanged by anything in this block, and the golden
# suite is the proof: the core, secondary and private lanes of all 102 fixtures must not move.
#
# An entry here is a judgement about our own taxonomy and is written down as one. A category with
# no honest archetype (Healthcare, Life Sciences, Climate & Energy: industries, not business
# models) is deliberately absent and reported by tools/investor_coverage.py rather than forced.
SECTOR_ALIASES = {
    'Insurance': ('Insurance Technology',),
    'Personal Software / Productivity': ('Consumer & Prosumer Software',),
    'Consumer subscription': ('Consumer & Prosumer Software',),
    'Enterprise Applications': ('Business Applications',),
    'Cloud & Infrastructure Software': ('Cloud & Infrastructure',),
    'Agent Ops': ('Data, AI & Developer Tools',),
    'Scraping / Data for AI': ('Data, AI & Developer Tools',),
    # HubSpot and Klaviyo are tagged Marketing & Customer Engagement in our own listed set, which
    # is where a sales-engagement fund's portfolio sits in our vocabulary.
    'Sales Engagement': ('Marketing & Customer Engagement',),
    'Communications & Customer Engagement': ('Communications & Collaboration',
                                             'Marketing & Customer Engagement'),
    # Shopify is Commerce & Payments Software here and BASE is Commerce Enablement & Fulfilment;
    # a fund that calls itself e-commerce enablement backs both, so it is offered to both.
    'E-commerce Enablement': ('Commerce Enablement & Fulfilment', 'Commerce & Payments Software'),
    # Added 8-Sep-2026 (Route A). The supply-chain software archetype was split out of the
    # operators; a fund that names logistics or supply chain backs both kinds, so it is offered
    # to both, and the E2open row's own category ("Connected supply chain software network")
    # lands on the software side.
    'Logistics / Supply chain': ('Commerce Enablement & Fulfilment', 'Local Delivery & On-Demand',
                                 'Supply Chain & Logistics Software'),
    'Delivery logistics and supply chain': ('Local Delivery & On-Demand', 'Commerce Enablement & Fulfilment',
                                            'Supply Chain & Logistics Software'),
    'Connected supply chain software network': ('Supply Chain & Logistics Software',),
    'D2C / Consumer Brand': ('Consumer Brand',),
    'D2C': ('Consumer Brand',),
    'Consumer Marketplace': ('Third-Party Marketplace',),
    'B2B Marketplace': ('Third-Party Marketplace',),
    'B2B marketplace': ('Third-Party Marketplace',),
    'Marketplace aggregator': ('Third-Party Marketplace',),
    'Real Estate Marketplace': ('Classifieds & Listings',),   # Zillow is Classifieds & Listings
    'Streaming & Creator': ('Streaming & Digital Media',),
    'Education': ('Online Learning',),
    'Financial Data': ('Financial Data & Index',),
    'Lending': ('Lending & Credit',),
    'Travel Booking': ('Travel Booking & OTA',),
}


def _sectors(cell):
    """"Sector(n); Sector(n)" where n is that house's DEAL COUNT in the sector, not part of the
    name. Splitting without stripping it produced one bucket per deal count on 3-Sep.

    The archetype each name maps to is added beside it, never instead of it, so an exact match
    that already worked cannot be lost. Deal counts carry across unchanged.
    """
    out = {}
    for c in (cell or '').split(';'):
        c = c.strip()
        if not c:
            continue
        m = re.match(r'^(.*?)\((\d+)\)$', c)
        name = (m.group(1) if m else c).strip()
        n = int(m.group(2)) if m else 0
        out[name] = n
        for a in SECTOR_ALIASES.get(name, ()):
            out[a] = max(out.get(a, 0), n)
    return out


def sector_vocabulary(archetypes):
    """Which screening categories reach a founder and which cannot, given our archetypes.

    Reported by tools/investor_coverage.py. A category that is neither an archetype nor aliased to
    one is a category no founder can ever match: today those are industries rather than business
    models, and forcing them into the taxonomy would be worse than naming them here.
    """
    seen, reach, dead = {}, {}, {}
    for d in INVESTORS:
        for c in (d.get('screening_categories') or '').split(';'):
            c = re.sub(r'\(\d+\)$', '', c.strip()).strip()
            if not c:
                continue
            seen[c] = seen.get(c, 0) + 1
    for c, n in seen.items():
        targets = (c,) if c in archetypes else SECTOR_ALIASES.get(c, ())
        hit = [t for t in targets if t in archetypes]
        (reach if hit else dead)[c] = (n, hit)
    return reach, dead


# THE SAME TOKENISER THE PEER MATCHER USES, imported rather than rewritten so "embedded payments"
# tokenises identically on both sides of the page. A second, subtly different one here is how the
# investor list and the comparables list would slowly stop agreeing about what a business is.
_STOP = {'and', 'of', 'the', 'for', 'a', 'in', 'to', 'with', 'we', 'our', 'is', 'that', 'from',
         'ventures', 'capital', 'partners', 'fund', 'funds', 'invest', 'invests', 'investing',
         'companies', 'company', 'founders', 'stage', 'early', 'seed', 'series'}


def _toks(t):
    return set(re.findall(r'[a-z0-9]+', (t or '').lower())) - _STOP


def _tag_overlap(prof, d):
    """How close is what this house has backed to what this founder is building?

    The founder side is their own product vocabulary, the same `product_tags` the peer matcher
    scores on. The house side is the SUBSECTORS OF THE ROUNDS IT ACTUALLY JOINED plus its own
    one-line thesis: "AI coding assistant / IDE", "Residential real-estate marketplace (iBuyer)".
    Not its sector list, which is coarse by design and already scored as the sector facet.

    Jaccard rather than a raw count, so a house with a long portfolio does not out-rank a focused
    one simply by having more words.
    """
    mine = _toks(prof.get('product_tags', '').replace('|', ' '))
    if not mine:
        return 0.0
    theirs = _toks(' '.join([d.get('subsectors') or '', d.get('thesis_one_liner') or '']))
    if not theirs:
        return 0.0
    return len(mine & theirs) / float(len(mine | theirs))


# ---------------------------------------------------------------------------
# GEOGRAPHY, and why a substring test was never going to work.
#
# The founder's country arrives as an edge header, so it is a two-letter code or a full country
# name. The house's geography is a free-text line a human wrote: "UK", "UK/Europe; backs European
# founders building globally", "Europe-focused, invests globally", "North America; Europe; Israel",
# "Australia and New Zealand; Israel; Southeast Asia". The old test asked whether one string
# contained the other, so a founder in "United Kingdom" did not match a fund in "UK" -- the letters
# u and k are both there and not next to each other -- and geography scored nothing for anybody.
#
# So: resolve the founder to a set of words for their country AND the regions that contain it,
# and intersect that with the words in the house's line. A fund saying "Europe" matches a German
# founder without anyone listing Germany, and a fund saying "invests globally" matches everyone,
# which is what it means.
_REGIONS = {
    'eu':   ('europe', 'european', 'emea', 'eea'),
    'na':   ('north america', 'north american', 'americas'),
    'apac': ('apac', 'asia', 'asia pacific', 'southeast asia', 'south east asia'),
    'latam': ('latin america', 'latam', 'south america'),
    'africa': ('africa', 'african', 'sub-saharan'),
    'mena': ('mena', 'middle east', 'gulf'),
}
# code -> (what the country is called, which regions contain it). Kept to the markets the pilot
# will actually see, and adding one is a one-line change rather than a rethink.
COUNTRIES = {
    'gb': (('uk', 'united kingdom', 'britain', 'british', 'england', 'scotland', 'wales'), ('eu',)),
    'ie': (('ireland', 'irish'), ('eu',)),
    'us': (('us', 'usa', 'united states', 'america', 'american'), ('na',)),
    'ca': (('canada', 'canadian'), ('na',)),
    'de': (('germany', 'german', 'dach'), ('eu',)),
    'fr': (('france', 'french'), ('eu',)),
    'es': (('spain', 'spanish', 'iberia'), ('eu',)),
    'it': (('italy', 'italian'), ('eu',)),
    'nl': (('netherlands', 'dutch', 'benelux'), ('eu',)),
    'be': (('belgium', 'benelux'), ('eu',)),
    'se': (('sweden', 'swedish', 'nordic', 'nordics'), ('eu',)),
    'no': (('norway', 'norwegian', 'nordic', 'nordics'), ('eu',)),
    'dk': (('denmark', 'danish', 'nordic', 'nordics'), ('eu',)),
    'fi': (('finland', 'finnish', 'nordic', 'nordics'), ('eu',)),
    'pl': (('poland', 'polish', 'cee'), ('eu',)),
    'ch': (('switzerland', 'swiss', 'dach'), ('eu',)),
    'at': (('austria', 'austrian', 'dach'), ('eu',)),
    'pt': (('portugal', 'portuguese', 'iberia'), ('eu',)),
    'il': (('israel', 'israeli'), ('mena',)),
    'ae': (('uae', 'emirates', 'dubai', 'abu dhabi'), ('mena',)),
    'in': (('india', 'indian'), ('apac',)),
    'sg': (('singapore', 'singaporean'), ('apac',)),
    'au': (('australia', 'australian', 'anz'), ('apac',)),
    'nz': (('new zealand', 'anz'), ('apac',)),
    'jp': (('japan', 'japanese'), ('apac',)),
    'ng': (('nigeria', 'nigerian'), ('africa',)),
    'ke': (('kenya', 'kenyan'), ('africa',)),
    'ug': (('uganda', 'ugandan'), ('africa',)),
    'za': (('south africa',), ('africa',)),
    'br': (('brazil', 'brazilian'), ('latam',)),
    'mx': (('mexico', 'mexican'), ('latam',)),
}
_BY_NAME = {}
for _c, (_names, _regs) in COUNTRIES.items():
    for _n in _names:
        _BY_NAME[_n] = _c
    _BY_NAME[_c] = _c

_ANYWHERE = ('global', 'globally', 'worldwide', 'anywhere', 'any geography', 'international')


def geo_words(country):
    """Everything a house could write that would mean this founder's country. None if unresolved."""
    c = _BY_NAME.get((country or '').strip().lower())
    if not c:
        return None
    names, regs = COUNTRIES[c]
    out = set(names) | {c}
    for r in regs:
        out |= set(_REGIONS[r])
    return out


def geo_match(country, cell):
    """(matched, house states no restriction). Word-level, because the house side is a sentence."""
    line = (cell or '').strip().lower()
    anywhere = any(a in line for a in _ANYWHERE) or not line
    words = geo_words(country)
    if words is None:
        return None, anywhere
    return (any(w in line for w in words) or anywhere), anywhere


INVESTORS = _rows(D + 'investors.csv')

# WHAT A CALLABLE ROW MUST CARRY TO RENDER.
#
# ONE HARD REQUIREMENT: a named deal with a date and the URL it was read from. That is the
# activity rule and it is the whole defence against vcconf's failure mode. Everything else is
# something we either publish or say we do not have.
#
# DANIIL, 3-Sep-2026: "We should definitely include Benchmark and Thrive. Reality is they can do
# pretty much anything from what I understand."
#
# He is right and the old gate had the logic backwards. It refused any house that had not
# published a first-cheque range or an investing geography, which does not describe an inactive
# fund; it describes a fund with a sparse website. benchmark.com carries two office addresses and
# no investment criteria. thrivecap.com is one sentence. Both led seed rounds this year, both
# raised new early-stage funds this year, and both were being withheld from every founder because
# their marketing pages are thin. Meanwhile the ABSENCE of a stated geography was being read as a
# failed geography test when the honest reading is the opposite: a fund that publishes no
# geographic restriction has not claimed one.
#
# So an unpublished cheque and an unstated geography no longer block. They are SHOWN AS
# UNPUBLISHED on the card ("First cheque not published", "No stated investing geography"), which
# is true, useful and the same discipline we hold a comparable to. What still holds the line is
# the stage band: a house that says where it comes in is believed and filtered on, and IVP saying
# "typically Series B, floor $15m" keeps it away from a pre-seed founder whether or not anything
# else is published.
REQUIRED = ('recent_deal_1_company', 'recent_deal_1_date', 'recent_deal_1_source_url')

# Shown, not required. A ceiling or a floor alone is a real published figure and reads on the card
# as "up to $5m" or "from $100k": Salesforce Ventures states "under $5M" at seed, Mercia "up to
# GBP 10m", Google's AI Futures Fund a $2m ceiling, Menlo Anthology and Square Peg a floor.
CHEQUE_EITHER_END = ('first_cheque_low_m', 'first_cheque_high_m')


def renderable(d):
    """(bool, missing fields). A row is not shown to a founder without a dated, sourced deal."""
    miss = [k for k in REQUIRED if not (d.get(k) or '').strip()]
    return (not miss), miss


def gaps(d):
    """What this house does not publish, for the card to say out loud rather than hide."""
    out = []
    if not any((d.get(k) or '').strip() for k in CHEQUE_EITHER_END):
        out.append('cheque')
    if not (d.get('geographies') or '').strip():
        out.append('geography')
    return out


# THE STAGE BANDS, IN THE WORDS THE INVESTOR TABLE USES. The founder's own answer to step 1 of the
# quiz is written in exactly these words, so it needs no translation, only recognising.
STAGE_NAMES = ('Pre-seed', 'Seed', 'Series A', 'Series B', 'Series C')


def _stage_for(prof, raise_musd=None):
    """The founder's stage. Their own answer first, then the raise, then revenue.

    THE FOUNDER'S ANSWER COMES FIRST, and until 6-Sep-2026 it was not read at all. Step 1 of the
    quiz asks "what stage are you at?" and this function derived the answer from the size of the
    round instead. Reading the answer is better on its own terms, and it is what lets the stage
    gate keep working once the amounts stop reaching the engine.

    MEASURED, 6-Sep-2026, across the 102 fixtures. With the raise and no stated stage the call list
    is 813 cards and every fixture gets houses. With neither it collapses to 44 cards and 92 of the
    102 fixtures get none, because a house that publishes a stage band can only be matched against
    a founder who has one. With the stated stage and no raise it is 813 cards at Seed, 724 at
    Pre-seed and 797 at Series A, and no fixture is left without a house.

    WHAT IS STILL LOST WITHOUT THE RAISE is `_cheque_fits`, which drops a house whose published
    first cheque cannot fund the round. At a $3m raise that excluded 3 of 156 callable houses. It
    returns None without a raise, which never excludes, so those 3 are now shown with their
    published cheque range on the card for the founder to judge.

    The raise is still used when it is given. The paid tiers have it, because the founder has
    consented to us reading their figures by then.
    """
    stated = (prof.get('stage') or '').strip()
    for name in STAGE_NAMES:
        if stated.lower() == name.lower():
            return name
    r = _f(raise_musd)
    if r is None:
        rev = _f(prof.get('revenue')) or _f(prof.get('arr'))
        r = None if rev is None else (0.5 if rev < 1 else 3.0 if rev < 5 else 12.0 if rev < 20 else 40.0)
    if r is None:
        return None
    return ('Pre-seed' if r < 1 else 'Seed' if r < 5 else 'Series A' if r < 20
            else 'Series B' if r < 60 else 'Series C')


# WHAT A HOUSE MEANS WHEN IT SAYS "EARLY STAGE".
#
# Daniil, 6-Sep-2026: "some of these houses clearly state that they are early stage. It is good
# enough, we dont have to look for them to say exactly Series A or Seed."
#
# He is right, and this map is what makes that safe rather than harmful. The stage band is an EXACT
# STRING match and a HARD GATE: `if stages and stage and not stage_hit: continue`. So writing
# "Early stage" into the file without this map would not loosen anything, it would EXCLUDE Haystack
# from every seed founder, because "Seed" is not the string "Early stage". A band nobody can match
# is worse than a blank one.
#
# The founder can only be Pre-seed, Seed or Series A: those are the three buttons in the quiz. So
# both of these phrases cover the whole of what a founder can be, and the filtering that still
# matters is done by the cheque. Town Hall says "we invest across all stages" and writes $3m to
# $30m initial cheques; it is _cheque_fits that keeps it away from a pre-seed founder raising
# $500k, which is the right instrument for it.
STAGE_COVERS = {
    'EARLY STAGE': ('Pre-seed', 'Seed', 'Series A'),
    'ALL STAGES': ('Pre-seed', 'Seed', 'Series A'),
}


def _stages_of(d):
    """The founder stages a house's published band actually covers.

    A band we recognise as a phrase expands to the stages it means; anything else is taken
    literally, which is how every band in the file behaved before this existed.
    """
    out = []
    for s in (d.get('stage_bands') or '').split(';'):
        s = s.strip()
        if not s:
            continue
        for x in STAGE_COVERS.get(s.upper(), (s,)):
            if x not in out:          # "Pre-seed; Early stage" would otherwise list Pre-seed twice
                out.append(x)
    return out


def _cheque_fits(d, raise_musd):
    """A house whose first cheque cannot fund this round is the wrong conversation."""
    r = _f(raise_musd)
    lo, hi = _f(d.get('first_cheque_low_m')), _f(d.get('first_cheque_high_m'))
    if r is None or lo is None:
        return None                      # unknown, never used to exclude
    return lo <= r * 1.5 and (hi is None or hi >= r * 0.05)


def match_callable(prof, raise_musd=None, want=8):
    """The call list, with every match labelled by how far we had to reach for it."""
    mine = {prof.get('archetype'), prof.get('archetype_secondary')} - {None, ''}
    geo = (prof.get('country') or '').strip().lower()
    stage = _stage_for(prof, raise_musd)
    pool = []
    for d in INVESTORS:
        if 'CALLABLE' not in (d.get('layer') or ''):
            continue
        ok, _miss = renderable(d)
        if not ok:
            continue
        secs = _sectors(d.get('screening_categories'))
        sector_hit = bool(mine & set(secs))
        sector_any = not secs
        stages = _stages_of(d)
        stage_hit = bool(stage) and stage in stages
        stage_any = not stages
        # A PUBLISHED STAGE BAND IS A HARD GATE, NOT ONE FACET OF THREE. The enrichment turned
        # this from a preference into a rule. IVP states its entry is typically Series B and its
        # floor is $15m; Insight led four Series A rounds in 2026 at $15m to $25m and publishes no
        # cheque at all. Under the old scoring, either could still reach a pre-seed founder as a
        # "two of three facets" match on sector and geography, and a seed founder told to call
        # Insight is exactly the aspirational-investor failure this list exists to avoid. A house
        # that says where it comes in is believed. A house that says nothing is still eligible,
        # because silence is not a claim.
        if stages and stage and not stage_hit:
            continue
        hit, geo_any = geo_match(geo, d.get('geographies'))
        geo_hit = bool(hit)
        # AN UNKNOWN COUNTRY IS NOT A MISS, and treating it as one emptied the list.
        #
        # The founder is never asked where they are based. It comes from Vercel's edge header at
        # boot (app.js sets responses.country from /api/geo, docs/lead-capture.md), which is the
        # right call: one fewer question for a fact the request already carries. But the header
        # can be absent, a VPN can make it wrong, and NONE OF THE 43 TEST FIXTURES CARRY ONE, so
        # geo_hit was false for every founder we test and geo_any true only for the handful of
        # houses saying "Global". Ten fixtures got fewer than three houses and four got none. It
        # read as a thin database; it was a three-valued question answered with a boolean, the
        # same mistake _cheque_fits already avoids by returning None for unknown.
        geo_known = geo_words(geo) is not None
        fits = _cheque_fits(d, raise_musd)
        if fits is False:
            continue
        if not geo_known:
            # Score on what we actually know, and SAY that geography was not part of it rather
            # than letting the founder read "exact fit" and assume we checked.
            if sector_hit and stage_hit:
                tier, label = 1, 'sector and stage; your location was not resolved'
            elif (sector_hit or sector_any) and (stage_hit or stage_any):
                tier, label = 2, 'broader fit; your location was not resolved'
            else:
                continue
        else:
            hits = sum([sector_hit, stage_hit, geo_hit])
            if sector_hit and stage_hit and geo_hit:
                tier, label = 0, 'exact fit on sector, stage and geography'
            elif sector_hit and stage_hit:
                tier, label = 1, 'sector and stage, wider geography'
            elif (sector_hit or sector_any) and (geo_hit or geo_any) and (stage_hit or stage_any):
                tier, label = 2, 'broader fit'
            elif hits >= 2:
                tier, label = 3, 'two of three facets'
            else:
                continue
        # Rank inside a tier by the house's DEAL COUNT in the founder's own sectors: activity in
        # this sector is the evidence that matters, and it is the number the table already holds.
        depth = sum(n for s, n in secs.items() if s in mine)
        # TAG OVERLAP, the second half of the roadmap's ranking rule and the half that was
        # missing. Deal count says how ACTIVE a house is in the founder's sector; tag overlap says
        # how close the businesses it backed are to this one. A payments house with four deals is
        # ranked above one with two, but between two houses with four deals each, the one whose
        # portfolio shares the founder's own product vocabulary goes first. Same tokeniser the
        # peer matcher uses, so "embedded payments" means the same thing on both sides of the page.
        overlap = _tag_overlap(prof, d)
        # A HOUSE THAT PUBLISHES ITS TERMS OUTRANKS ONE THAT DOES NOT, all else equal. Benchmark
        # belongs on the list; it does not belong above a house of equal fit whose cheque range a
        # founder can actually check themselves.
        # A STAGE SPECIALIST OUTRANKS A GENERALIST OF EQUAL FIT. Daniil, 6-Sep-2026: "Accel should
        # not be above funds that specialize on seed and Series A in my view." Inside a tier the
        # house whose published band covers FEWER stages goes first: a fund that only writes seed
        # cheques is a better call for a seed founder than a house that writes them from seed to
        # Series C, whatever its deal count. Deal count and tag overlap still order the houses that
        # cover the same number of stages. "All stages" expands to every stage and so ranks last.
        # NOTE THE DATA LIMIT: this ranks on the band the row carries. Accel's row carries
        # "Pre-seed; Seed" (a seed programme, not the house), so on 6-Sep this rule alone does not
        # move it; the band is flagged for a source check in the status document.
        breadth = len(_stages_of(d))
        pool.append((tier, len(gaps(d)), breadth, -depth, -overlap, d['investor_name'], d, label))
    pool.sort(key=lambda z: (z[0], z[1], z[2], z[3], z[4], z[5]))
    # NEVER PADDED. If only four houses clear tier 0 and 1, four is the answer.
    out = []
    for tier, _ngaps, _breadth, _negdepth, _overlap, _name, d, label in pool[:want]:
        if tier >= 3 and len([o for o in out if o['tier'] < 3]) >= 3:
            break                          # do not dilute a good list with two-of-three matches
        out.append(dict(
            investor=d['investor_name'], house_type=d.get('house_type'),
            thesis=d.get('thesis_one_liner'), tier=tier, why=label,
            cheque_low_m=_f(d.get('first_cheque_low_m')), cheque_high_m=_f(d.get('first_cheque_high_m')),
            geographies=d.get('geographies'), stage_bands=d.get('stage_bands'),
            recent_deal=d.get('recent_deal_1_company'), recent_deal_date=d.get('recent_deal_1_date'),
            recent_deal_url=d.get('recent_deal_1_source_url'),
            # THE TWO CAVEATS THAT MUST TRAVEL WITH THE CARD, not sit in the file being true.
            # cheque_figure_dated is set where the only published figure carries a date: Freestyle
            # Mar-2022, Square Peg Nov-2022, Sequoia's Arc programme Jan-2023. deal_note is set
            # where the deal is a regional-fund deployment with the house named as fund manager
            # rather than writing a balance-sheet venture cheque. Both change what "first cheque
            # $1.5m to $3m" and "recently backed X" mean to the person reading them.
            cheque_figure_dated=(d.get('cheque_figure_dated') or '').strip() or None,
            deal_note=(d.get('deal_note') or '').strip() or None,
            # WHAT THIS HOUSE DOES NOT PUBLISH, carried so the card can say it rather than leave a
            # blank the founder fills in with an assumption.
            not_published=gaps(d) or None))
    return out


def match_evidence(picked):
    """The houses behind the founder's OWN comparables, from the rounds the selector chose.

    Honestly labelled: this is a map of who pays up for businesses like yours, mostly growth stage
    and mostly US. It is not a call list for a seed round and must never be shown as one.
    """
    seen = collections.OrderedDict()
    for _sw, r in picked:
        for name in re.split(r'[;,]', r.get('lead_key_investors') or ''):
            name = re.sub(r'\((led|acquirer)\)', '', name, flags=re.I).strip()
            # THE CELL IS FREE TEXT AND SOME OF IT IS PROSE, NOT A NAME. "IFC identified for up to
            # $40m of additional primary capital" and "Chimera Abu Dhabi (> $200m for > 20%)" are
            # both in the file. A fragment carrying a figure, a comparison or more than five words
            # is a sentence about a deal, not a house, and putting it on a card would look like we
            # cannot read our own data.
            name = re.sub(r'\([^)]*[\d>%$][^)]*\)', '', name).strip(' .,')
            if len(name) < 3 or len(name.split()) > 5:
                continue
            if re.search(r'[\d$%]|\b(identified|additional|up to|for|of|primary|capital only)\b',
                         name, flags=re.I) and not re.match(r'^[A-Z]', name):
                continue
            if re.search(r'\b(identified|additional|up to)\b', name, flags=re.I):
                continue
            # REPAIR, THEN REFUSE. The same shapes tools/build_investors_table.py applies when it
            # builds the table, kept here because this layer reads the rounds file directly rather
            # than the table. "partners of DST Global" is DST Global with a preposition in front,
            # "Origin Energy participated" is a house with a verb stuck to it, and "Walmart and
            # Flipkart" is two houses in one cell: none of them is a reason to lose an investor.
            # A clause that names nobody is refused.
            name = re.sub(r'^(?:partners of|affiliates of|funds managed by)\s+', '', name,
                          flags=re.I).strip()
            name = re.sub(r'\s+(?:participated|invested|joined)\s*$', '', name,
                          flags=re.I).strip()
            if re.search(r'\b(?:did not|said|was oversubscribed|declined to)\b', name, flags=re.I):
                continue
            # OUR OWN PLACEHOLDER, NOT A HOUSE. "Not identified in any source" is what we write in
            # the investor cell when a round names no lead. It was reaching the evidence layer as
            # an investor chip against Perplexity.
            if name.lower().startswith('not identified'):
                continue
            pair = re.match(r'^([A-Z][\w.&-]*) and ([A-Z][\w.&-]*)$', name)
            names = [pair.group(1), pair.group(2)] if pair else [name]
            for name in names:
                if len(name) < 3:
                    continue
                seen.setdefault(name, []).append((r['company_name'], r.get('date')))
            continue
            seen.setdefault(name, []).append((r['company_name'], r.get('date')))
    return [dict(investor=k, backed=[{'company': c, 'date': d} for c, d in v[:3]], n=len(v))
            for k, v in seen.items()]


# ---------------------------------------------------------------------------
# THE REVEAL PAYLOAD, and the compliance rails that travel with it.
#
# Fable, 2-Sep: "public information only, no scraping behind logins, no contact details, no claim of
# introduction. The footer's 'a map, not an introduction, no affiliation or endorsement is implied'
# carries over to every rendering of both layers. Styled text wordmarks, no logos."
#
# Those rails are enforced HERE rather than trusted to the renderer, because the renderer is the
# last place a rule gets remembered. Nothing leaves this function carrying a person's name, an
# email, a phone number or a logo URL, and every card carries the label saying how far we reached
# for it.
FOOTER = ('A map, not an introduction. No affiliation or endorsement is implied, and no contact '
          'details are held or shown. Every name here is drawn from public announcements.')

# A field that may reach a founder. Anything not on this list is not passed through, so a column
# added to investors.csv later cannot leak into the page by accident.
CARD_FIELDS = ('investor', 'house_type', 'thesis', 'why', 'cheque_low_m', 'cheque_high_m',
               'geographies', 'stage_bands', 'recent_deal', 'recent_deal_date', 'recent_deal_url',
               'cheque_figure_dated', 'deal_note', 'not_published')
BANNED = ('email', 'phone', 'contact', 'partner_name', 'linkedin', 'twitter', 'logo')


def _clean(card):
    out = {k: card.get(k) for k in CARD_FIELDS}
    for k, v in list(out.items()):
        if isinstance(v, str) and any(b in v.lower() for b in ('@', 'linkedin.com', 'mailto:')):
            out[k] = None
    return out


def cheque_line(card):
    """How the cheque reads on the card. vcconf's own reasoning, and it is right: "a $25K angel and
    a $15M fund are different conversations, and knowing which one you are looking at saves you the
    email." An unknown range says so rather than being hidden."""
    lo, hi = card.get('cheque_low_m'), card.get('cheque_high_m')
    line = None
    if lo is None and hi is None:
        line = 'First cheque not published'
    elif lo is None:
        # CEILING ONLY, AND IT SAYS SO. "under $5M" is what Salesforce Ventures publishes and it is
        # a different statement from "$0m to $5m", which we would be inventing.
        line = 'First cheque up to $%sm' % ('%g' % hi)
    elif hi is None or hi == lo:
        line = 'First cheque from $%sm' % ('%g' % lo)
    else:
        line = 'First cheque $%sm to $%sm' % ('%g' % lo, '%g' % hi)
    when = card.get('cheque_figure_dated')
    if when and lo is not None or when and hi is not None:
        line += ' (the only figure they publish, dated %s)' % when
    return line


def geography_line(card):
    """Where they invest, or the fact that they do not say. An empty line on a card is read as an
    omission by us; "no stated investing geography" is read as a fact about the fund, which is
    what it is. Seven of the houses on this list publish no geography at all, Benchmark and
    Founders Fund among them, and that is not a reason to hide them."""
    g = (card.get('geographies') or '').strip()
    return g if g else 'No stated investing geography'


# HOW MANY EXTRA HOUSES TO SEND SO THE BROWSER CAN DO THE CHEQUE FILTER ITSELF.
#
# Daniil, 7-Sep-2026: "can we not do the work of refining the universe of potential investors
# without me actually seeing what amount they are raising? How is it possible we are able to build
# a football field for them without me seeing the revenue figure, but cannot figure out the
# investor universe without raise amount reaching me?"
#
# He is right, and the answer was in front of us: it is the SAME TRICK THE FOOTBALL FIELD USES.
# The field works because the server sends MULTIPLES and the browser multiplies them by a revenue
# figure that never leaves it. The investor list can work the same way. The server sends the
# candidate houses WITH THEIR PUBLISHED CHEQUE RANGES, which are our data and not the founder's,
# and the browser drops the ones that cannot fund the round it holds locally.
#
# So the choice was never "the raise leaves, or the filter dies". Both were wrong.
#
# THE ONLY COST IS SENDING A FEW MORE HOUSES THAN THE FOUNDER WILL SEE. If the page shows eight and
# the browser filters some out, the server must have sent more than eight or the list comes up
# short. Six extra is enough: measured across all 102 fixtures on 7 September, the cheque filter
# removes at most 3 houses from any one list at any raise between $250k and $10m.
#
# AND THE OVER-FETCH REVEALS NOTHING. Every house sent is one the founder's SECTOR and STAGE
# already qualified; which of them the browser then hides is decided on this side of the wall and
# never sent back. An observer on our side sees the same fifteen names for every seed fintech
# founder in the country.
CHEQUE_FILTER_OVERFETCH = 6


def reveal_payload(prof, picked, raise_musd=None, want=8):
    """Everything the reveal needs for both layers, and nothing it does not.

    WITH NO RAISE, THE FILTER MOVES TO THE BROWSER rather than being skipped. See
    CHEQUE_FILTER_OVERFETCH above: extra candidates go out, each carrying its published cheque
    range, and `cheque_filter` tells the page to finish the job with the figure it holds.
    """
    browser_filters = _f(raise_musd) is None
    fetch = want + CHEQUE_FILTER_OVERFETCH if browser_filters else want
    callable_rows = match_callable(prof, raise_musd=raise_musd, want=fetch)
    evidence_rows = match_evidence(picked)
    cards = []
    for c in callable_rows:
        d = _clean(c)
        d['cheque_line'] = cheque_line(c)
        d['geography_line'] = geography_line(c)
        d['reach'] = c.get('why')
        cards.append(d)
    return {
        'callable': {
            'heading': 'Writing first cheques in your sector right now',
            'cards': cards,
            'count': len(cards),
            # THE INSTRUCTION TO THE BROWSER, and the rule it must apply, sent as data rather than
            # assumed. `low <= raise * 1.5 and (high is None or high >= raise * 0.05)` is exactly
            # what _cheque_fits does on this side when a raise IS given, and check 15 asserts the
            # page's copy of it agrees with this one on every fixture, so the two cannot drift.
            'cheque_filter': ({
                'apply': True,
                'show': want,
                'low_multiple': 1.5,
                'high_multiple': 0.05,
                'note': ('Some of these may write cheques far larger or smaller than you are '
                         'raising. Your browser hides those; we never see the figure it used.'),
            } if browser_filters else None),
            # NEVER PADDED, and the page should say so rather than look thin by accident.
            'note': ('%d houses match. We do not pad the list: a shorter list of houses that write '
                     'your cheque is worth more than a longer one that does not.' % len(cards))
                    if len(cards) < want else None,
        },
        'evidence': {
            'heading': 'The houses behind your reference rounds',
            # THE HONEST LABEL, and it is the difference between our failure mode and theirs.
            'note': ('A map of who pays up for businesses like yours, drawn from the rounds on your '
                     'own field. Mostly growth stage and mostly US: this is not a call list for an '
                     'early round.'),
            'chips': [{'investor': e['investor'],
                       'backed': '%s, %s' % (e['backed'][0]['company'], e['backed'][0]['date'])
                       if e['backed'] else None,
                       'n': e['n']} for e in evidence_rows],
            'count': len(evidence_rows),
        },
        'footer': FOOTER,
    }
