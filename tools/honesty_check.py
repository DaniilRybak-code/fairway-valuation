"""Print what every fixture would say, so the copy is read in situ before it ships.

  python tools/honesty_check.py          what shows inline, per fixture
  python tools/honesty_check.py --all    everything, including the disclosure
"""
import sys, os, collections
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'selector'))
import match_reference as M, honesty as H
from golden_profiles import PROFILES

show_all = '--all' in sys.argv
fired, blank = collections.Counter(), []
for key, label, prof in PROFILES:
    picked, months, tier = M.select_private(prof, M.private)
    r = M.private_range(prof, picked, tier) or {}
    cs = H.caveats(prof, r)
    for c in cs: fired[c['key']] += 1
    if not cs:
        blank.append(key); continue
    print('\n%s   %s' % (key.upper(), label))
    print('   range %s to %s, %s, %s' % (r.get('low'), r.get('high'), r.get('display'),
                                         r.get('basis_label') or 'enterprise value to revenue'))
    for c in cs:
        if c['inline']: print('   INLINE  %s' % c['text'])
        elif show_all:  print('   more    %s' % c['text'])
    if not show_all and len(cs) > H.INLINE_MAX:
        print('   more    %d further caveats behind the disclosure' % (len(cs) - H.INLINE_MAX))

print('\n\nFLAG FREQUENCY, %d fixtures' % len(PROFILES))
for k, v in fired.most_common(): print('   %-20s %d' % (k, v))
print('\nfixtures with no priced range, so nothing to caveat: %d  %s' % (len(blank), blank))
