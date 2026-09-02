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
hk={(norm(r['company']),(r['txn_date'] or '')[:7]) for r in his}
inwin=[];pre=[]
for o in ours:
    d=(o.get('date_iso') or '')[:7]
    if (norm(o['company_name']),d) in hk: continue
    (inwin if d>='2021-08' else pre).append(o)
def f(x):
    try: return float(x)
    except: return None
priced=[r for r in inwin if f(r.get('ev_revenue_x'))]
print(f"our rows he does not have, DATED 2021-08 OR LATER (his window): {len(inwin)}   of which priced: {len(priced)}")
print(f"our rows dated before his window (not a gap, just not covered yet): {len(pre)}   of which priced: {len([r for r in pre if f(r.get('ev_revenue_x'))])}")
print("\n--- PRICED, IN HIS WINDOW, ONLY WE HAVE ---")
for r in sorted(priced,key=lambda r:r['company_name']):
    print(f"  {r['company_name']:<20} {r.get('date_iso'):<9} {f(r['ev_revenue_x']):>7}x  {(r.get('revenue_metric') or '')[:38]}")
