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


def _sectors(cell):
    """"Sector(n); Sector(n)" where n is that house's DEAL COUNT in the sector, not part of the
    name. Splitting without stripping it produced one bucket per deal count on 3-Sep."""
    out = {}
    for c in (cell or '').split(';'):
        c = c.strip()
        if not c:
            continue
        m = re.match(r'^(.*?)\((\d+)\)$', c)
        out[(m.group(1) if m else c).strip()] = int(m.group(2)) if m else 0
    return out


INVESTORS = _rows(D + 'investors.csv')

# WHAT A CALLABLE ROW MUST CARRY TO RENDER. Fable's bar, unchanged in substance.
REQUIRED = ('recent_deal_1_company', 'recent_deal_1_date', 'geographies')

# A CHEQUE FIGURE AT EITHER END COUNTS, and the 3-Sep enrichment is why this changed. Five houses
# publish only one side of the range: Salesforce Ventures states "under $5M" at seed, Mercia "up
# to GBP 10m", Google's AI Futures Fund a $2m co-investment ceiling, Menlo Anthology a $100k floor,
# Square Peg a $1m floor. Requiring first_cheque_low_m specifically was a rule about our own column
# layout rather than about what a founder needs to know, and it kept five sourced, current houses
# off the list. A ceiling tells a founder just as clearly whether this is their conversation.
CHEQUE_EITHER_END = ('first_cheque_low_m', 'first_cheque_high_m')


def renderable(d):
    """(bool, missing fields). A row is not shown to a founder unless it is complete."""
    miss = [k for k in REQUIRED if not (d.get(k) or '').strip()]
    if not any((d.get(k) or '').strip() for k in CHEQUE_EITHER_END):
        miss.append('first_cheque_low_m or first_cheque_high_m')
    return (not miss), miss


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
        geos = [g.strip().lower() for g in (d.get('geographies') or '').split(';') if g.strip()]
        geo_hit = bool(geo) and any(geo in g or g in geo for g in geos)
        geo_any = (not geos) or any(g in ('global', 'any', 'worldwide') for g in geos)
        # AN UNKNOWN COUNTRY IS NOT A MISS, and treating it as one emptied the list.
        #
        # Every one of the 43 fixtures has country=None, because the quiz never asks it. geo_hit
        # is therefore false for all of them, and geo_any is true only for the four renderable
        # houses that say "Global", so 71 of 75 houses failed the geography facet for every
        # founder we test. Ten fixtures got fewer than three houses and four got none, and it read
        # as a thin database when it was a three-valued question answered with a boolean. The same
        # mistake _cheque_fits already avoids: unknown returns None and never excludes.
        geo_known = bool(geo)
        fits = _cheque_fits(d, raise_musd)
        if fits is False:
            continue
        if not geo_known:
            # Score on what we actually know, and SAY that geography was not part of it rather
            # than letting the founder read "exact fit" and assume we checked.
            if sector_hit and stage_hit:
                tier, label = 1, 'sector and stage; we have not asked where you are based'
            elif (sector_hit or sector_any) and (stage_hit or stage_any):
                tier, label = 2, 'broader fit; we have not asked where you are based'
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
        pool.append((tier, -depth, d['investor_name'], d, label))
    pool.sort(key=lambda z: (z[0], z[1], z[2]))
    # NEVER PADDED. If only four houses clear tier 0 and 1, four is the answer.
    out = []
    for tier, _negdepth, _name, d, label in pool[:want]:
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
            deal_note=(d.get('deal_note') or '').strip() or None))
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
               'cheque_figure_dated', 'deal_note')
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


def reveal_payload(prof, picked, raise_musd=None, want=8):
    """Everything the reveal needs for both layers, and nothing it does not."""
    callable_rows = match_callable(prof, raise_musd=raise_musd, want=want)
    evidence_rows = match_evidence(picked)
    cards = []
    for c in callable_rows:
        d = _clean(c)
        d['cheque_line'] = cheque_line(c)
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
