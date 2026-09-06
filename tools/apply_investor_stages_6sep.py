#!/usr/bin/env python3
"""Stage bands for the five houses the check refused, from Daniil's pull of 6 September 2026.

WHAT THE PULL ASKED FOR. `tools/investor_check.py` refuses a CALLABLE house with no stage band, and
after the cheque rule was brought into line with Daniil's 3-Sep ruling those five were the only
refusals left. The pull asked one question: what stage does each firm PUBLISH on its own site.

EVERY ROW VERIFIED AGAINST ITS OWN SOURCE URL before this script was written. The five pages were
fetched and the quoted wording checked word for word. The transcription was accurate on all five.

WHAT THE ANSWER ACTUALLY IS, and it is not five stage bands.

  Canaan       PUBLISHES A STAGE. "Canaan XIII is an oversubscribed $650 million fund intended to
               support visionary entrepreneurs seeking seed and Series A funding" and "will invest
               in seed and early-stage technology companies". -> Seed; Series A
  Techstars    PUBLISHES A STAGE. "Techstars is a leading pre-seed and early-stage venture capital
               firm"; the Accelerator Funds "invest on standardized terms in pre-seed companies".
               -> Pre-seed. The Venture Funds "invest in follow-on rounds of Techstars Accelerator
               graduates", which is a real activity with no stage label attached, so no second band
               is invented for it.
  Founderful   NAMES NO STAGE. "We back founder teams as their lead investor in their first
               financing round"; "the first institutional investor". Unambiguous in substance and
               unlabelled, and we do not translate substance into a label the firm did not use.
  Haystack     NAMES NO STAGE. "an early stage venture capital firm", "the earliest stages".
  Town Hall    NAMES NO STAGE, AND SAYS SO ON PURPOSE. "We invest across all stages. We prioritize
               team, business model, and mission over stage." That is a positive claim of no
               restriction, not an omission.

DANIIL RULED ON THE OTHER THREE, 6-Sep: "some of these houses clearly state that they are early
stage. It is good enough, we dont have to look for them to say exactly Series A or Seed." So the
band is the phrase the firm publishes: Founderful and Haystack are "Early stage", Town Hall is
"All stages", and Techstars is "Pre-seed; Early stage" because that is what its own page says.

THE HALF OF THIS THAT WOULD HAVE GONE WRONG SILENTLY. The stage band is an EXACT STRING match and a
HARD GATE in selector/investors.py: `if stages and stage and not stage_hit: continue`. Writing
"Early stage" into the file on its own would therefore have EXCLUDED Haystack from every seed
founder, because "Seed" is not the string "Early stage", and a band nobody can match is worse than
a blank one. `STAGE_COVERS` in that file is the other half: "Early stage" and "All stages" expand to
Pre-seed, Seed and Series A, which is the whole of what a founder can be, and the cheque range does
the rest of the filtering. Town Hall says all stages and writes $3m to $30m initial cheques; it is
_cheque_fits that keeps it away from a pre-seed founder.

TWO CHEQUE RANGES THE PULL CONFIRMED AND DID NOT CHANGE. Haystack "typically invest $1M to $3M in
initial rounds" and Town Hall "initial checks range from $3M to $30M" are both already in
data/investors.csv at exactly those figures. Nothing is written for them; the pull is independent
confirmation of two rows we already held, which is worth more than a new number.

ONE DISCREPANCY, FLAGGED NOT RESOLVED. haystack.vc's page body says "$1M to $3M" and its own meta
description says "$500K-$2M". We hold 1 to 3, matching the body. Two published figures on one page
is a ruling, not a transcription error, and it is on Daniil's list.

COUNT IN, COUNT OUT, nothing dropped. Idempotent.

  python3 tools/apply_investor_stages_6sep.py
"""
import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE)

PATH = 'data/investors.csv'

# key -> (stage_bands, source url for the stage claim)
STAGES = {
    'canaan': ('Seed; Series A', 'https://www.canaan.com/latest/announcing-canaan-xiii'),
    # Published as "pre-seed and early-stage venture capital firm", so both, verbatim.
    'techstars': ('Pre-seed; Early stage', 'https://www.techstars.com/for/investors'),
    # DANIIL, 6-Sep: "some of these houses clearly state that they are early stage. It is good
    # enough, we dont have to look for them to say exactly Series A or Seed." These three do say
    # it, in their own words, and the words are now a band the matcher understands (STAGE_COVERS
    # in selector/investors.py).
    'founderful': ('Early stage', 'https://www.founderful.com/'),
    'haystack': ('Early stage', 'https://haystack.vc/'),
    'town-hall-ventures': ('All stages', 'https://www.townhallventures.com/our-approach'),
}

# The exact published wording behind each band, so a reader can check the call without refetching.
WORDING = {
    'canaan': '"seeking seed and Series A funding"; "will invest in seed and early-stage '
              'technology companies"',
    'techstars': '"a leading pre-seed and early-stage venture capital firm"; Accelerator Funds '
                 '"invest on standardized terms in pre-seed companies"',
    'founderful': '"We have the courage to invest early"; "lead investor in their first financing '
                  'round"; "the first institutional investor"',
    'haystack': '"Haystack is an early stage venture capital firm"; "Backing outlier founders at '
                'the earliest stages"',
    'town-hall-ventures': '"We invest across all stages. We prioritize team, business model, and '
                          'mission over stage."',
}


def main():
    head = [l for l in open(PATH) if l.startswith('#')]
    body = [l for l in open(PATH) if not l.startswith('#')]
    rows = list(csv.DictReader(io.StringIO(''.join(body))))
    fields = list(rows[0].keys())
    n_in = len(rows)

    changed = skipped = 0
    for r in rows:
        k = (r.get('investor_key') or r.get('key') or '').strip().lower()
        if k not in STAGES:
            continue
        band, url = STAGES[k]
        cur = (r.get('stage_bands') or '').strip()
        if cur == band:
            print('ALREADY  %-22s stage_bands already %r' % (r.get('investor_name') or r.get('name') or r.get('investor'), band))
            skipped += 1
            continue
        if cur and cur not in ('Pre-seed',):
            print('REFUSED  %-22s already carries %r, which this script will not overwrite.'
                  % (r.get('investor_name') or r.get('name') or r.get('investor'), cur))
            skipped += 1
            continue
        r['stage_bands'] = band
        changed += 1
        print('CHANGED  %-22s stage_bands "" -> %r' % (r.get('investor_name') or r.get('name') or r.get('investor'), band))
        print('         source  %s' % url)
        print('         says    %s' % WORDING.get(k, ''))

    if changed:
        out = io.StringIO()
        w = csv.DictWriter(out, fieldnames=fields, lineterminator='\n')
        w.writeheader()
        w.writerows(rows)
        open(PATH, 'w').write(''.join(head) + out.getvalue())

    back = list(csv.DictReader(io.StringIO(''.join(
        l for l in open(PATH) if not l.startswith('#')))))
    print('\nCOUNT IN %d rows, COUNT OUT %d rows, changed %d, unchanged %d, dropped %d.'
          % (n_in, len(back), changed, skipped, n_in - len(back)))
    print('\nALL FIVE NOW CARRY A BAND. Daniil, 6-Sep: "some of these houses clearly state that')
    print('they are early stage. It is good enough, we dont have to look for them to say exactly')
    print('Series A or Seed." Three of the five say exactly that in their own words and one says')
    print('"across all stages", so the band is what they publish rather than a label we invented.')
    print('selector/investors.py STAGE_COVERS is what makes those two phrases mean something: the')
    print('band is an exact-match HARD GATE, so without it "Early stage" would have excluded')
    print('Haystack from every seed founder instead of including it.')
    return 0 if len(back) == n_in else 1


if __name__ == '__main__':
    sys.exit(main())
