import csv, re, io

def norm(n):
    n = re.sub(r'[^a-z0-9]','',(n or '').lower())
    for junk in ('athleticgreens','luminati','cursor'):
        n = n.replace(junk,'')
    return n

def load_ours():
    rows=[]
    for path in ('data/private-rounds.csv','data/private-rounds-consumer.csv'):
        with open(path) as f:
            lines=[l for l in f if not l.startswith('#')]
        for r in csv.DictReader(io.StringIO(''.join(lines))):
            rows.append(r)
    return rows

ours = load_ours()
_hl=[l for l in open('data/raw/2026-09-01_private-transactions-daniil.csv') if not l.startswith('#')]
his = list(csv.DictReader(io.StringIO(''.join(_hl))))

targets = """1Password 2022-01
AlphaSense 2023-09
Anthropic 2023-05
Apollo.io 2023-08
Canva 2025-08
Clay 2026-01
Databricks 2023-09
Decagon 2026-01
ElevenLabs 2025-01
Gorillas 2021-10
Guesty 2024-04
Jasper 2022-10
Klarna 2022-07
Notion 2026-01
PayFit 2022-01
Replit 2025-09
Snyk 2022-12
Turing 2025-03
Wolt 2021-11""".strip().split('\n')

def f(x):
    try: return float(x)
    except: return None

print(f"{'company':<14}{'month':<9}| {'his PM':>8} {'his den':>9} {'his x':>7} {'basis':<16}| {'our PM':>8} {'our den':>9} {'our x':>7} {'implied':>8}  our metric")
print('-'*130)
for t in targets:
    name, month = t.rsplit(' ',1)
    hn = norm(name)
    hrow = [r for r in his if norm(r['company'])==hn and (r['txn_date'] or '').startswith(month)]
    orow = [r for r in ours if norm(r['company_name'])==hn and (r['date_iso'] or '').startswith(month)]
    h = hrow[0] if hrow else {}
    o = orow[0] if orow else {}
    hpm=f(h.get('post_money_m')); hden=f(h.get('metric_value_m')); hx=f(h.get('mult_reported'))
    opm=f(o.get('post_money_musd')); oden=f(o.get('revenue_musd')); ox=f(o.get('ev_revenue_x'))
    implied = (opm/ox) if (opm and ox) else None
    print(f"{name:<14}{month:<9}| {hpm if hpm else '':>8} {hden if hden else '':>9} {hx if hx else '':>7} {(h.get('denominator_basis') or '')[:15]:<16}| {opm if opm else '':>8} {oden if oden else '':>9} {ox if ox else '':>7} {round(implied,1) if implied else '':>8}  {(o.get('revenue_metric') or '')[:28]}")
