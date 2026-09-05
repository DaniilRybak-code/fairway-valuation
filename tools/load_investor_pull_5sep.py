#!/usr/bin/env python3
"""
Loads Claude's 5-Sep-2026 investor pull, data/raw/2026-09-05_investor-pull-claude.csv, into
data/investors.csv. Imported by tools/build_investors_table.py and applied AFTER the human
enrichment, so the table can be rebuilt from its sources at any time without losing these rows.
Not run on its own.

WHAT THE PULL IS. Nineteen houses for the two thin clusters, Consumer & Prosumer Software (14 to
47 callable houses, 16 of them from this pull) and Online Learning (3 to 12): seed specialists and accelerators with a named
first-cheque deal into a consumer app or consumer learning product dated Sep-2025 or later, each
read on the URL in its row. Two are EVIDENCE only, on their own words (Tiny VC does not lead) or
because the fund's site could not be read (Shine Capital).

MERGE RULE. A house already in the table (matched on investor_key, then on the same alias stem the
checker uses) keeps its generated counts and deal history; the pull's fields overwrite only where the
pull carries a value, and the layer gains CALLABLE if the pull says so. A new house is appended with
the pull's fields and empty generated fields. Nothing is dropped and the merge is printed.
"""
import csv, io, os, re

SRC = 'data/raw/2026-09-05_investor-pull-claude.csv'

PULL_FIELDS = ('house_type', 'layer', 'geographies', 'stage_bands', 'first_cheque_low_m',
               'first_cheque_high_m', 'cheque_currency', 'thesis_one_liner', 'screening_categories',
               'subsectors', 'recent_deal_1_company', 'recent_deal_1_date', 'recent_deal_1_source_url',
               'recent_deal_2_company', 'recent_deal_2_date', 'recent_deal_2_source_url',
               'cheque_range_source', 'geographies_source', 'last_verified', 'deal_note')


def _stem(n):
    n = (n or '').lower()
    changed = True
    while changed:
        changed = False
        for tail in (' capital partners', ' capital', ' ventures', ' partners', ' vc',
                     ' management', ' group', ' global', ' investments'):
            if n.endswith(tail) and len(n) > len(tail) + 2:
                n, changed = n[:-len(tail)], True
                break
    return re.sub(r'[^a-z0-9]', '', n)


def load():
    if not os.path.exists(SRC):
        return []
    lines = [l for l in open(SRC, encoding='utf-8') if not l.startswith('#')]
    return list(csv.DictReader(io.StringIO(''.join(lines))))


def apply_to(rows, aliases=None):
    pull = load()
    if not pull:
        print('investor pull 5-Sep: %s not present, nothing applied' % SRC)
        return rows
    by_key = {r['investor_key']: r for r in rows}
    by_stem = {}
    for r in rows:
        by_stem.setdefault(_stem(r['investor_name']), r)
    merged, added = 0, 0
    for p in pull:
        target = by_key.get(p['investor_key']) or by_stem.get(_stem(p['investor_name']))
        if target is not None:
            for f in PULL_FIELDS:
                v = (p.get(f) or '').strip()
                if not v or f == 'layer':
                    continue
                target[f] = v
            layers = set(x for x in (target.get('layer') or '').split('|') if x)
            layers |= set(x for x in (p.get('layer') or '').split('|') if x)
            target['layer'] = '|'.join(sorted(layers, key=lambda x: x != 'CALLABLE'))
            target['provenance'] = (p.get('provenance') or '') + ' || also: ' + (target.get('provenance') or '')
            merged += 1
            print('MERGED  %-22s into existing row %s' % (p['investor_name'], target['investor_key']))
        else:
            row = {c: '' for c in rows[0].keys()} if rows else {}
            row.update({f: (p.get(f) or '').strip() for f in PULL_FIELDS})
            row['investor_key'] = p['investor_key']
            row['investor_name'] = p['investor_name']
            row['provenance'] = p.get('provenance') or ''
            for c in ('rounds_in_set', 'companies_in_set'):
                row[c] = 0
            rows.append(row)
            by_key[row['investor_key']] = row
            added += 1
    print('investor pull 5-Sep: %d houses read, %d merged into existing rows, %d added' % (len(pull), merged, added))
    return rows
