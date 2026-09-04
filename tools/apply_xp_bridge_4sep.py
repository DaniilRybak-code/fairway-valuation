#!/usr/bin/env python3
"""Daniil's ruling of 4-Sep-2026: XP Inc's equity-to-AV bridge is zero.

XP Inc came through the screen at an enterprise value of -$15,902m, because the bridge carries
-$24,684m of net debt: for a broker, client balances and financing sit on the balance sheet and
net against the market capitalisation, so the standard bridge produces a negative aggregate value
and a -3.8x revenue multiple. The arithmetic is right and the answer is meaningless.

The ruling is to price XP on its equity value, which is what the bridge being zero means:
enterprise value becomes the market capitalisation and the multiples are rebuilt from it.

WHAT IS AND IS NOT TOUCHED. The three bridge components (net debt, minority interest, associates)
are LEFT EXACTLY AS SUPPLIED. They are what the source said and this is a pricing ruling, not a
correction of the source, so overwriting them would destroy the evidence for the ruling. The
consequence is that for this one row the components no longer sum to the bridge, which is why the
override is written into the file's own header block as well as into docs/rulings-applied-4sep.md.

Run once:  python3 tools/apply_xp_bridge_4sep.py
It reports before and after and refuses to run twice.
"""
import os
import sys

PATH = 'data/peers-fintech.csv'
TICKER = 'NASDAQ:XP'
NOTE = ('# RULING 4-Sep-2026 (Daniil): NASDAQ:XP equity_to_av_bridge_musd overridden to 0 and '
        'enterprise_value_musd set to market_cap_musd. The supplied bridge was -25402 '
        '(net debt -24684, associates 718), giving EV -15902 and a -3.8x revenue multiple: a '
        "broker's client balances net against its market cap. The three component columns are "
        'left as supplied and no longer sum to the bridge for this row alone. '
        'See docs/rulings-applied-4sep.md.')


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    src = open(PATH, encoding='utf-8').read().splitlines()
    if any(l.startswith('# RULING 4-Sep-2026 (Daniil): NASDAQ:XP') for l in src):
        print('ALREADY APPLIED. The ruling note is in the file header; nothing to do.')
        return 0

    header = None
    idx = None
    for i, l in enumerate(src):
        if l.startswith('#'):
            continue
        if header is None:
            header = l.split(',')
            continue
        if l.split(',')[2:3] == [TICKER]:
            idx = i
    if header is None or idx is None:
        print('FAILED: %s not found in %s' % (TICKER, PATH))
        return 1

    col = {c: n for n, c in enumerate(header)}
    f = src[idx].split(',')
    before = dict((c, f[col[c]]) for c in ('market_cap_musd', 'net_debt_musd', 'associates_musd',
                                           'equity_to_av_bridge_musd', 'enterprise_value_musd',
                                           'revenue_ntm_musd', 'gross_profit_musd',
                                           'ev_ntm_revenue_x', 'ev_ntm_gp_x'))
    mc = float(before['market_cap_musd'])
    rev = float(before['revenue_ntm_musd'])
    gp = float(before['gross_profit_musd'])
    f[col['equity_to_av_bridge_musd']] = '0'
    f[col['enterprise_value_musd']] = '%g' % mc
    f[col['ev_ntm_revenue_x']] = '%.1f' % (mc / rev)
    f[col['ev_ntm_gp_x']] = '%.1f' % (mc / gp)
    src[idx] = ','.join(f)

    # The note goes into the file's own comment block, where the refresh provenance already lives,
    # so the next person to open the file sees the override without needing the doc.
    last_comment = max(i for i, l in enumerate(src) if l.startswith('#') and i < 10)
    src.insert(last_comment + 1, NOTE)
    open(PATH, 'w', encoding='utf-8').write('\n'.join(src) + '\n')

    print('XP Inc, %s' % PATH)
    print('  %-28s %12s -> %s' % ('equity_to_av_bridge_musd', before['equity_to_av_bridge_musd'], '0'))
    print('  %-28s %12s -> %g' % ('enterprise_value_musd', before['enterprise_value_musd'], mc))
    print('  %-28s %12s -> %.1f  (%g / %g)' % ('ev_ntm_revenue_x', before['ev_ntm_revenue_x'],
                                               mc / rev, mc, rev))
    print('  %-28s %12s -> %.1f  (%g / %g)' % ('ev_ntm_gp_x', before['ev_ntm_gp_x'] or '(blank)',
                                               mc / gp, mc, gp))
    print('  left as supplied: net_debt_musd %s, associates_musd %s'
          % (before['net_debt_musd'], before['associates_musd']))
    print('1 row in, 1 row out, no other row touched.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
