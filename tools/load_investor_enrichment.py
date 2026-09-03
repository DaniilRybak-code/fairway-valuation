#!/usr/bin/env python3
"""The human-researched investor enrichment, read as a SOURCE rather than patched in once.

DANIIL, 3-Sep-2026: "You need to fix this architectural problem with different data sets. I will
be providing data updates on regular basis, so we need to make sure the updated numbers go into
the database and start reaching the user as soon as received, without creating any conflicts."

That is why this is a loader the builder calls, not a one-off script. data/investors.csv is
GENERATED: tools/build_investors_table.py rebuilds it from the rounds files, the seed screen and
data-content.js. A patch applied to the output would survive exactly until the next rebuild and
then vanish without a word, which is the failure that cost two days on 3-Sep with the 1-Sep public
refresh. So the enrichment file sits in data/raw, the builder reads it as its LAST stage, and
re-running the builder re-applies it.

IT RUNS LAST BECAUSE IT OVERRIDES THE MACHINE. The promotion rule in the builder turns any house
with a deal inside twelve months into a CALLABLE row. That rule put Benchmark, Coatue, BlackRock,
Baillie Gifford and 44 others on a list headed "writing first cheques in your sector right now".
The verdict column here is a human reading each house against that heading and saying no. A
machine cannot make that call and should not be trusted to.

WHAT IT MAY AND MAY NOT DO
  may   fill a cheque range, a geography, a stage band, a thesis and the URL each came from
  may   move a house off the CALLABLE layer (verdict evidence_only), which never removes it from
        the EVIDENCE layer: it stays behind the founder's own comparables where it belongs
  may   drop a row that is not an investor at all, by name, reported
  never blank a figure we already hold. An empty cell in the enrichment means NOT RESEARCHED, and
        NOT RESEARCHED is not the same as NOT PUBLISHED. Where the researcher meant "no figure is
        published anywhere", the source column says NOT STATED and that is recorded as such.
"""
import csv, io, os, re

SRC = 'data/raw/2026-09-03_investor-enrichment-complete.csv'

# Columns this file adds to data/investors.csv.
NEW_COLS = ['geographies_source', 'dormant_note', 'enrichment_verdict', 'cheque_figure_dated']

# Columns it may write into, and which enrichment column feeds each.
MAP = {
    'first_cheque_low_m':  'first_cheque_low_m',
    'first_cheque_high_m': 'first_cheque_high_m',
    'cheque_currency':     'cheque_currency',
    'geographies':         'geographies',
    'stage_bands':         'stage_bands',
    'thesis_one_liner':    'thesis_one_liner',
    'cheque_range_source': 'cheque_range_source',
    'geographies_source':  'geographies_source',
    'dormant_note':        'dormant_note',
}

# A CHEQUE FIGURE WITH A DATE ON IT IS A DIFFERENT THING FROM A CURRENT ONE, and the founder is
# the one who needs to know. Three of the sixteen published figures are years old: Freestyle's is
# a Mar-2022 TechCrunch line, Square Peg's a Nov-2022 blog post, Sequoia's the Jan-2023 Arc
# announcement. The researcher wrote the date into the source cell in each case; this reads it
# back out rather than us remembering. Nothing is inferred: no date in the text, no flag.
DATED = re.compile(r'\b(?:dated|published|post dated|posted)\s+((?:\d{1,2}\s+)?'
                   r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+20\d\d)', re.I)


def _dated_figure(row):
    for cell in (row.get('cheque_range_source'), row.get('dormant_note')):
        m = DATED.search(cell or '')
        if m:
            return m.group(1)
    return ''


def load(path=SRC):
    """[{investor_key, verdict, ...}] straight off the supplied file, nothing dropped."""
    if not os.path.exists(path):
        return []
    lines = [l for l in io.open(path, encoding='utf-8') if not l.startswith('#')]
    rows = list(csv.DictReader(io.StringIO(''.join(lines))))
    for r in rows:
        r['cheque_figure_dated'] = _dated_figure(r)
    return rows


def apply_to(rows, path=SRC, log=print, aliases=None, dropped=None):
    """Join onto the built table on investor_key. Two-way accounting, every row named.

    Returns (applied, unmatched_keys). Prints the count in, the count out and what moved, because
    D12 says every supplied row is accounted for BY NAME and a merge that only reports a total is
    the same as no report at all.
    """
    supplied = load(path)
    if not supplied:
        log('INVESTOR ENRICHMENT: %s not present, skipped.' % path)
        return 0, []
    by_key = {}
    for r in rows:
        by_key.setdefault(r['investor_key'], r)
    # A SUPPLIED KEY THAT WENT SOMEWHERE ON PURPOSE IS NOT A MISS. Two of the 78 are handled
    # before this stage runs: a16z is merged into andreessenhorowitz by NAME_ALIASES, and the
    # unattributed-participant placeholder is dropped by DROP_KEYS. Without being told, this
    # loader would report both as lost research and the report would cry wolf on every run.
    aliases = aliases or {}
    dropped = dropped or {}

    stats = {'callable_kept': [], 'demoted': [], 'filled_cheque': [], 'filled_geo': [],
             'dated_figure': [], 'unmatched': [], 'merged': [], 'dropped': []}
    for s in supplied:
        k = s['investor_key'].strip()
        d = by_key.get(k)
        if d is None and k in aliases:
            d = by_key.get(aliases[k])
            if d is not None:
                stats['merged'].append('%s -> %s' % (k, d['investor_name']))
        if d is None and k in dropped:
            stats['dropped'].append('%s (%s)' % (s['investor_name'], dropped[k]))
            continue
        if d is None:
            stats['unmatched'].append(k)
            continue
        had_cheque = bool((d.get('first_cheque_low_m') or '').strip()
                          or (d.get('first_cheque_high_m') or '').strip())
        had_geo = bool((d.get('geographies') or '').strip())
        for dest, src in MAP.items():
            v = (s.get(src) or '').strip()
            if v:                       # NEVER BLANK WHAT WE ALREADY HOLD
                d[dest] = v
        d['enrichment_verdict'] = s['verdict']
        if s.get('cheque_figure_dated'):
            d['cheque_figure_dated'] = s['cheque_figure_dated']
            stats['dated_figure'].append('%s (%s)' % (d['investor_name'], s['cheque_figure_dated']))
        if s['verdict'] == 'evidence_only':
            # OFF THE CALL LIST, NOT OUT OF THE DATABASE. It keeps every round it is attached to.
            d['layer'] = 'EVIDENCE'
            stats['demoted'].append(d['investor_name'])
        else:
            stats['callable_kept'].append(d['investor_name'])
            if not had_cheque and ((s.get('first_cheque_low_m') or '').strip()
                                   or (s.get('first_cheque_high_m') or '').strip()):
                stats['filled_cheque'].append(d['investor_name'])
            if not had_geo and (s.get('geographies') or '').strip():
                stats['filled_geo'].append(d['investor_name'])

    log('')
    log('INVESTOR ENRICHMENT, %s' % path)
    log('  supplied           %d rows' % len(supplied))
    log('  matched on key     %d' % (len(supplied) - len(stats['unmatched'])
                                       - len(stats['dropped'])))
    for line in stats['merged']:
        log('  merged spelling    %s' % line)
    for line in stats['dropped']:
        log('  dropped upstream   %s' % line)
    log('  kept CALLABLE      %d' % len(stats['callable_kept']))
    log('  moved to EVIDENCE  %d' % len(stats['demoted']))
    log('  cheque range now held where it was not: %d' % len(stats['filled_cheque']))
    log('  geography now held where it was not:    %d' % len(stats['filled_geo']))
    if stats['dated_figure']:
        log('  cheque figure carries a date and is flagged to the founder:')
        for n in sorted(stats['dated_figure']):
            log('      %s' % n)
    if stats['unmatched']:
        log('  UNMATCHED, AND THAT IS A FAILURE. These keys are in the supplied file and not in')
        log('  the table, so the research on them reaches nobody:')
        for k in stats['unmatched']:
            log('      %s' % k)
    log('  moved to EVIDENCE, by name:')
    log('      ' + ', '.join(sorted(stats['demoted'])))
    log('')
    return len(supplied) - len(stats['unmatched']), stats['unmatched']


if __name__ == '__main__':
    rows = load()
    print('%d rows in %s' % (len(rows), SRC))
    for r in rows:
        if r['cheque_figure_dated']:
            print('  dated figure: %-22s %s' % (r['investor_key'], r['cheque_figure_dated']))
