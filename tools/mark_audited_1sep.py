# -*- coding: utf-8 -*-
"""Record that a human read the source for these rows, so the work is in the data and not only in a
markdown file. Rule D9: a ruling that lives only in a conversation is not in the product.

The basis audit tool's count does NOT move when a label is corrected, because it measures whether
the SOURCE WORDING asserts a basis, which corrections do not change. The progress metric is this
field. AUDITED_1SEP means somebody opened the source and decided.
"""
import csv, io, os, sys
WRITE = '--write' in sys.argv
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AUDITED = {
 ('dLocal','Apr-21'),('Pine Labs','May-21'),('Marqeta','May-20'),('Zepz','Aug-21'),
 ('Delhivery','May-21'),('Xpressbees','Feb-22'),('Shiprocket','Aug-22'),('Jobandtalent','Dec-21'),
 ('Loadsmart','Nov-20'),('Loadsmart','Feb-22'),('Calendly','Jan-21'),('Invisible Technologies','Sep-25'),
 ('Scale AI','Jun-25'),('Mailchimp','Sep-21'),('Semrush','Nov-25'),('Jasper','Oct-22'),
 ('Klaviyo','May-21'),('OLIPOP','Feb-25'),('Huel','Nov-22'),('Liquid Death','Oct-22'),
 ("Harry's",'Mar-21'),('Savage X Fenty','Feb-21'),('Away','May-19'),('Glossier','Mar-19'),
 ('Quince','Mar-26'),('StockX','Apr-21'),('Wolt','Nov-21'),('Gopuff','Jul-21'),
 ('Vinted','Apr-26'),('Vinted','Oct-24'),('Meesho','May-24'),('Meesho','Sep-21'),
 ('SHEIN','Jan-24'),('SHEIN','May-23'),('Marqeta','May-19'),('Zepz','Oct-24'),
 ('Creditas','Dec-25'),('Creditas','Jul-22'),('Creditas','Dec-20'),
 ('Flipkart','Jul-23'),('Flipkart','Jul-21'),
}
# Read, but left open on purpose. These keep a flag so nobody records them as settled.
OPEN = {('Mews','Jan-26'): 'CANNOT_TELL_NEEDS_FY2024_REVENUE_NOTE',
        ('Scale AI','Jun-25'): 'AUDITED_1SEP_OPEN_STAFFING_RULING',
        ('Invisible Technologies','Sep-25'): 'AUDITED_1SEP_OPEN_STAFFING_RULING',
        ('Zepz','Aug-21'): 'AUDITED_1SEP_OPEN_DENOMINATOR_RULING'}

n=0
for path in ('data/private-rounds.csv','data/private-rounds-consumer.csv'):
    p=os.path.join(HERE,path)
    raw=open(p).read().splitlines(True)
    head=[l for l in raw if l.lstrip().lstrip('"').startswith('#')]
    body=[l for l in raw if not l.lstrip().lstrip('"').startswith('#')]
    rdr=csv.DictReader(io.StringIO(''.join(body))); cols=rdr.fieldnames; rows=list(rdr)
    if 'revenue_basis_source' not in cols: continue
    hit=False
    for r in rows:
        k=((r.get('company_name') or '').strip(),(r.get('date') or '').strip())
        if k in OPEN: r['revenue_basis_source']=OPEN[k]; hit=True; n+=1
        elif k in AUDITED: r['revenue_basis_source']='AUDITED_1SEP'; hit=True; n+=1
    if hit and WRITE:
        with open(p,'w',newline='') as f:
            f.writelines(head); w=csv.DictWriter(f,fieldnames=cols); w.writeheader()
            for r in rows: w.writerow({c:r.get(c,'') for c in cols})
print('%d rows %s' % (n,'WRITTEN' if WRITE else 'would be marked (dry run)'))
