# -*- coding: utf-8 -*-
"""CHECK 16: is the token-weight file what the tag files say it should be?

Fable, 6-Sep-2026, on Daniil's question of why the file could sit stale for two weeks while new
companies joined the data. The answer was that nothing checked it: the file is computed from the tag
files by a rule (5 divided by the number of companies carrying a word, for words carried by more
than five), and the only thing that re-ran the rule was a script somebody had to remember to run.
Between 24 August and 6 September two tag files were added and the private set more than tripled,
193 words became generic, and every one of them kept full weight. This check recomputes the file
from the seven tag files on every run and fails if the committed file differs.

The fix when it fails is one command, and the check prints it. No hand edits.

  python3 tools/check_token_weights.py
"""
import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'tools'))
import regenerate_token_weights_6sep as RW      # noqa: E402

PATH = os.path.join(HERE, 'data', 'tag-token-weights.csv')


def main():
    rows, rows_in, nfiles = RW.compute(HERE)
    want = {r[0]: (r[1], r[3]) for r in rows}
    have = {r['token']: (int(r['companies_carrying']), float(r['weight_factor']))
            for r in RW.loads(PATH)}
    print('TOKEN WEIGHTS: %d tag files, %d tag rows read; %d generic words expected, %d in the file'
          % (nfiles, rows_in, len(want), len(have)))
    missing = sorted(t for t in want if t not in have)
    extra = sorted(t for t in have if t not in want)
    moved = sorted(t for t in want if t in have and (want[t][0] != have[t][0]
                                                     or abs(want[t][1] - have[t][1]) > 0.005))
    if not (missing or extra or moved):
        print('PASS: data/tag-token-weights.csv is exactly what the seven tag files produce today.')
        return 0
    if missing:
        print('   %d generic words ABSENT from the file, so they score at full weight: %s%s'
              % (len(missing), ', '.join(missing[:20]), ' ...' if len(missing) > 20 else ''))
    if extra:
        print('   %d words in the file that are no longer generic: %s' % (len(extra), ', '.join(extra[:20])))
    if moved:
        print('   %d words whose carrier count or weight has drifted: %s%s'
              % (len(moved), ', '.join('%s (%d -> %d)' % (t, have[t][0], want[t][0]) for t in moved[:12]),
                 ' ...' if len(moved) > 12 else ''))
    print('FAIL: the weight file is stale. Tags changed and the rule was not re-run. Regenerate it:')
    print('   python3 tools/regenerate_token_weights_6sep.py && python3 selector/golden.py --write')
    print('   then write the reason golden moved into the status document (it will move: every')
    print('   shared word is worth a different amount).')
    return 1


if __name__ == '__main__':
    sys.exit(main())
