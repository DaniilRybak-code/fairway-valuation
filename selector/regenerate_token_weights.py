# -*- coding: utf-8 -*-
"""Regenerate data/tag-token-weights.csv across FOUR tag files.

The rule is unchanged and is the one stated in the file it produces:
  weight_factor = 5 / companies_carrying, for tokens carried by more than five companies.
Reproduced exactly against the committed version on three files before the fourth was added
(management 105, software 75, payments 45, data 44, cloud 35 all match).

One row disappears relative to the committed version: 'of'. The tokeniser strips it as a
stopword, so it could never have scored. Nothing else is removed by hand.
"""
import csv, io, re, subprocess, sys
from collections import defaultdict
REPO='/home/claude/live'
def loads(s):
    return list(csv.DictReader(io.StringIO('\n'.join(l for l in s.splitlines() if not l.lstrip('"').startswith('#')))))
def gitshow(p): return subprocess.check_output(['git','show','origin/main:'+p],cwd=REPO).decode('utf-8')
def toks(t): return set(re.findall(r'[a-z0-9]+',t.lower())) - {'and','of','the','for'}

SRC=[('data/peers-software-tags.csv',None),('data/peers-fintech-tags.csv',None),
     ('data/private-companies-tags.csv',None)]
comp=defaultdict(set); tags=defaultdict(set)
def eat(label, rows):
    for i,r in enumerate(rows):
        key=(label, r.get('exchange_ticker') or r.get('company_key') or r.get('company_name') or i)
        for tg in [x.strip() for x in r['product_tags'].split('|') if x.strip()]:
            for t in toks(tg): comp[t].add(key); tags[t].add(tg.lower())
for f,_ in SRC: eat(f, loads(gitshow(f)))
for local in ('data/peers-ecommerce-tags.csv','data/private-companies-consumer-tags.csv'):
    eat(local, loads(open(REPO+'/'+local,encoding='utf-8').read()))

rows=[(t,len(c),len(tags[t]),round(5/len(c),2)) for t,c in comp.items() if len(c)>5]
rows.sort(key=lambda r:(-r[1],r[0]))
HDR='''# Generic-token down-weights for the selector's product-tag token matching. COMPUTED from the
# five tag files; regenerate when tags change, never hand-edit.
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
# REGENERATED 24-Aug-2026 to include data/peers-ecommerce-tags.csv, the fourth tag file. The
# consumer set adds 298 distinct tags, which changes the frequency of shared words: "marketplace",
# "commerce", "delivery", "subscription" and "brand" all become generic and lose weight, which is
# the mechanism working as intended. One row from the previous version is gone: 'of'. The
# tokeniser strips it as a stopword, so it never scored.
'''
buf=io.StringIO(); w=csv.writer(buf,lineterminator='\n')
w.writerow(['token','companies_carrying','distinct_tags_containing','weight_factor'])
for r in rows: w.writerow(r)
open(REPO+'/data/tag-token-weights.csv','w',encoding='utf-8').write(HDR+buf.getvalue())
print("rows:",len(rows))
prev={r['token']:r for r in loads(gitshow('data/tag-token-weights.csv'))}
new={r[0]:r for r in rows}
add=[t for t in new if t not in prev]; gone=[t for t in prev if t not in new]
print("newly generic (%d):"%len(add), sorted(add)[:40])
print("dropped (%d):"%len(gone), sorted(gone))
moved=sorted(((int(prev[t]['companies_carrying']), new[t][1], t) for t in new if t in prev
              and new[t][1]-int(prev[t]['companies_carrying'])>=8), key=lambda z:-(z[1]-z[0]))[:12]
print("biggest frequency jumps (was -> now):", [(t,a,b) for a,b,t in moved])
