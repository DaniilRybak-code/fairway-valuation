import csv,re,io
def norm(n):
    n=re.sub(r'[^a-z0-9]','',(n or '').lower())
    for j in ('athleticgreens','luminati','cursor'): n=n.replace(j,'')
    return n
def load(p):
    lines=[l for l in open(p) if not l.startswith('#')]
    return list(csv.DictReader(io.StringIO(''.join(lines))))
ours=load('data/private-rounds.csv')+load('data/private-rounds-consumer.csv')
his=load('data/raw/2026-09-01_private-transactions-daniil.csv')
ourkeys={(norm(r['company_name']),(r['date_iso'] or '')[:7]) for r in ours}
ourco={norm(r['company_name']) for r in ours}
new_co=[]; new_round=[]
for r in his:
    k=(norm(r['company']),(r['txn_date'] or '')[:7])
    if k in ourkeys: continue
    (new_round if norm(r['company']) in ourco else new_co).append(r)
print(f"his rows we do not have: {len(new_co)+len(new_round)}")
print(f"  companies entirely new to us : {len(new_co)}")
print(f"  company known, round missing  : {len(new_round)}")
print("\n--- NEW COMPANIES ---")
for r in sorted(new_co,key=lambda r:r['company']):
    print(f"  {r['company']:<20} {r['txn_date']:<12} {r['mult_reported']:>8}x  {r['metric_type']:<17} {r['denominator_basis'][:34]}")
print("\n--- KNOWN COMPANY, MISSING ROUND ---")
for r in sorted(new_round,key=lambda r:r['company']):
    print(f"  {r['company']:<20} {r['txn_date']:<12} {r['mult_reported']:>8}x  {r['metric_type']:<17} {r['denominator_basis'][:34]}")
