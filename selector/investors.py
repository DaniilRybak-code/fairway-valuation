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

# WHAT A CALLABLE ROW MUST CARRY TO RENDER. Fable's bar, unchanged.
REQUIRED = ('recent_deal_1_company', 'recent_deal_1_date', 'first_cheque_low_m', 'geographies')


def renderable(d):
    """(bool, missing fields). A row is not shown to a founder unless it is complete."""
    miss = [k for k in REQUIRED if not (d.get(k) or '').strip()]
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
        geos = [g.strip().lower() for g in (d.get('geographies') or '').split(';') if g.strip()]
        geo_hit = bool(geo) and any(geo in g or g in geo for g in geos)
        geo_any = (not geos) or any(g in ('global', 'any', 'worldwide') for g in geos)
        fits = _cheque_fits(d, raise_musd)
        if fits is False:
            continue
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
            recent_deal_url=d.get('recent_deal_1_source_url')))
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
            seen.setdefault(name, []).append((r['company_name'], r.get('date')))
    return [dict(investor=k, backed=[{'company': c, 'date': d} for c, d in v[:3]], n=len(v))
            for k, v in seen.items()]
