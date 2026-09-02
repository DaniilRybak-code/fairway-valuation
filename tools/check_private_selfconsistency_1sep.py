import csv, io
_hl=[l for l in open('data/raw/2026-09-01_private-transactions-daniil.csv') if not l.startswith('#')]
his=list(csv.DictReader(io.StringIO(''.join(_hl))))
def f(x):
    try: return float(x)
    except: return None
bad=[]; ok=0; skip=0
for r in his:
    pm=f(r['post_money_m']); d=f(r['metric_value_m']); m=f(r['mult_reported'])
    if not (pm and d and m): skip+=1; continue
    calc=pm/d
    if abs(calc-m)/m > 0.02:
        bad.append((r['company'],r['txn_date'],pm,d,m,round(calc,2),r['metric_type'],r['denominator_basis']))
    else: ok+=1
print(f"his rows with all three numbers: {ok+len(bad)}   tie: {ok}   do NOT tie: {len(bad)}   incomplete: {skip}")
print()
for b in bad:
    print(f"  {b[0]:<20} {b[1]:<12} PM {b[2]:>9} / {b[3]:>9} = {b[5]:>8}   but his column shows {b[4]:>8}   [{b[6]}, {b[7][:30]}]")
