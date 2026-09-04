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


def _stage_for(prof, raise_musd=None):
    """The founder's stage, from the raise if they gave one, else from revenue.

    The quiz already asks the raise amount and it is the strongest single facet: as vcconf put it,
    "a $25K angel and a $15M fund are different conversations, and knowing which one you are looking
    at saves you the email."
    """
    r = _f(raise_musd)
    if r is None:
        rev = _f(prof.get('revenue')) or _f(prof.get('arr'))
        r = None if rev is None else (0.5 if rev < 1 else 3.0 if rev < 5 else 12.0 if rev < 20 else 40.0)
    if r is None:
        return None
    return ('Pre-seed' if r < 1 else 'Seed' if r < 5 else 'Series A' if r < 20
            else 'Series B' if r < 60 else 'Series C')


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
        stages = [s.strip() for s in (d.get('stage_bands') or '').split(';') if s.strip()]
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
        pool.append((tier, len(gaps(d)), -depth, -overlap, d['investor_name'], d, label))
    pool.sort(key=lambda z: (z[0], z[1], z[2], z[3], z[4]))
    # NEVER PADDED. If only four houses clear tier 0 and 1, four is the answer.
    out = []
    for tier, _ngaps, _negdepth, _overlap, _name, d, label in pool[:want]:
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


def reveal_payload(prof, picked, raise_musd=None, want=8):
    """Everything the reveal needs for both layers, and nothing it does not."""
    callable_rows = match_callable(prof, raise_musd=raise_musd, want=want)
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
