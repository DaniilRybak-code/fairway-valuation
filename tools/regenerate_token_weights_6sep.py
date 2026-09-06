# -*- coding: utf-8 -*-
"""Regenerate data/tag-token-weights.csv from ALL SEVEN tag files in the working tree.

Fable, 6-Sep-2026. The file's own header says it is COMPUTED and must be regenerated when the tags
change, never hand-edited. It was last regenerated on 24-Aug-2026 from five tag files, through
selector/regenerate_token_weights.py, which reads three of them out of `git show origin/main` at a
path (/home/claude/live) that no longer exists. Since then the lending and logistics files were
added and the private set grew from 90 to 320 rounds, and the file was never re-run. Measured on
6-Sep: 400 tokens are generic by the file's own rule (carried by more than five companies), the
file lists 207, and 193 generic words carry full weight, so a founder and a row can clear the
relevance gate on "own", "health", "warehouse" or "freight" as if those were product vocabulary.

The RULE IS UNCHANGED: weight_factor = 5 / companies_carrying for tokens carried by more than five
companies; everything else keeps 1.0 by being absent. Only the inputs are brought up to date.

    python3 tools/regenerate_token_weights_6sep.py            writes the file, prints in/out
    python3 tools/regenerate_token_weights_6sep.py --dry-run  prints what would change, writes nothing
    python3 tools/regenerate_token_weights_6sep.py --out PATH writes elsewhere (used by the measurer)
"""
import csv
import glob
import io
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STOP = {'and', 'of', 'the', 'for'}          # must match match_reference.toks exactly


def loads(p):
    return list(csv.DictReader(io.StringIO('\n'.join(
        l for l in open(p, encoding='utf-8').read().splitlines() if not l.lstrip('"').startswith('#')))))


def toks(t):
    return set(re.findall(r'[a-z0-9]+', t.lower())) - STOP


def tag_files(root):
    return (sorted(glob.glob(os.path.join(root, 'data', 'peers-*-tags.csv')))
            + [os.path.join(root, 'data', 'private-companies-tags.csv'),
               os.path.join(root, 'data', 'private-companies-consumer-tags.csv')])


def compute(root):
    comp, tags = defaultdict(set), defaultdict(set)
    rows_in = 0
    for f in tag_files(root):
        rows = loads(f)
        rows_in += len(rows)
        for i, r in enumerate(rows):
            key = (os.path.basename(f), r.get('exchange_ticker') or r.get('company_key')
                   or r.get('company_name') or i)
            for tg in [x.strip() for x in (r.get('product_tags') or '').split('|') if x.strip()]:
                for t in toks(tg):
                    comp[t].add(key)
                    tags[t].add(tg.lower())
    out = [(t, len(c), len(tags[t]), round(5.0 / len(c), 2)) for t, c in comp.items() if len(c) > 5]
    out.sort(key=lambda r: (-r[1], r[0]))
    return out, rows_in, len(tag_files(root))


HDR = '''# Generic-token down-weights for the selector's product-tag token matching. COMPUTED from the
# seven tag files; regenerate when tags change, never hand-edit.
#
# WHY. Token-level matching (0.6 per shared token) pulls false comps on generic words: "Agent
# Network" (Western Union, human money-transfer agents) shares a token with every AI-agent
# startup, "Local AI" with "Local Payment Methods". The fix is frequency, not a hand list: a
# token carried by many companies separates nothing and scores little.
#
# RULE. token_score = 0.6 * weight_factor. Tokens absent from this file (carried by 5 or fewer
# companies) keep weight_factor 1.0. Listed tokens use weight_factor = 5 / companies_carrying.
# EXACT full-tag matches (3.0 points) are NEVER down-weighted - "AI Agents" as a whole tag is a
# real category; only its loose tokens are cheap.
#
# REGENERATED 6-Sep-2026 by tools/regenerate_token_weights_6sep.py from all seven tag files
# (software, ecommerce, fintech, logistics-services, lending, private, private-consumer). The
# previous version dated from 24-Aug-2026 and five files; 193 words that had become generic since
# then were carrying full weight.
'''


def main():
    dry = '--dry-run' in sys.argv
    out_path = os.path.join(ROOT, 'data', 'tag-token-weights.csv')
    if '--out' in sys.argv:
        out_path = sys.argv[sys.argv.index('--out') + 1]
    rows, rows_in, nfiles = compute(ROOT)
    prev_path = os.path.join(ROOT, 'data', 'tag-token-weights.csv')
    prev = {r['token']: r for r in loads(prev_path)} if os.path.exists(prev_path) else {}
    new = {r[0]: r for r in rows}
    added = sorted(t for t in new if t not in prev)
    gone = sorted(t for t in prev if t not in new)
    print('%d tag files, %d tag rows in' % (nfiles, rows_in))
    print('%d generic tokens in the committed file, %d in the regenerated one' % (len(prev), len(new)))
    print('%d newly generic (absent before, carried full weight): %s%s'
          % (len(added), ', '.join(added[:30]), ' ...' if len(added) > 30 else ''))
    print('%d dropped (no longer carried by more than five): %s' % (len(gone), ', '.join(gone) or 'none'))
    moved = [(t, prev[t]['weight_factor'], new[t][3]) for t in new if t in prev
             and abs(float(prev[t]['weight_factor']) - new[t][3]) >= 0.05]
    print('%d tokens whose weight moved by 0.05 or more' % len(moved))
    if dry:
        print('dry run, nothing written')
        return 0
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator='\n')
    w.writerow(['token', 'companies_carrying', 'distinct_tags_containing', 'weight_factor'])
    for r in rows:
        w.writerow(r)
    open(out_path, 'w', encoding='utf-8').write(HDR + buf.getvalue())
    print('wrote %s: %d rows out' % (out_path, len(rows)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
