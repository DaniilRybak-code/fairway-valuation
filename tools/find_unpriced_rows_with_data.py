import csv, io
def load(p):
    lines=[l for l in open(p) if not l.startswith('#')]
    return p, list(csv.DictReader(io.StringIO(''.join(lines))))
def f(x):
    try: return float(x)
    except: return None
tot=0
for p in ('data/private-rounds.csv','data/private-rounds-consumer.csv'):
    p,rows=load(p)
    print(f"--- {p} : {len(rows)} rows ---")
    for r in rows:
        pm=f(r.get('post_money_musd')); rev=f(r.get('revenue_musd')); x=f(r.get('ev_revenue_x'))
        if pm and rev and not x:
            tot+=1
            print(f"  {r.get('company_name'):<20} {r.get('date_iso'):<9} PM {pm:>9} rev {rev:>8}  = {round(pm/rev,1):>6}x  metric={(r.get('revenue_metric') or '')[:34]:<36} gate={r.get('display_gate','')} status={r.get('revenue_status','')[:14]}")
print(f"\nTOTAL rows with a valuation and a revenue but no multiple: {tot}")
