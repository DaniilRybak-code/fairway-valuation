#!/usr/bin/env python3
"""The equity-to-AV bridge set to zero, for the companies Daniil has ruled on.

WHY THIS CLASS OF RULING EXISTS. A broker, a payments company or a bank holds client money and
financing on its own balance sheet. The standard bridge nets that against the market
capitalisation, and for these companies it produces a NEGATIVE enterprise value and a negative
multiple. The arithmetic is right and the answer is meaningless (rulebook B11). Daniil's ruling is
to price these names on their equity value, which is what a zero bridge means.

THE COMPONENTS ARE NEVER OVERWRITTEN. net_debt_musd, minority_interest_musd and associates_musd
stay exactly as supplied, because they are what the source said and this is a pricing ruling, not
a correction of the source. For a ruled row the components no longer sum to the bridge, which is
why every ruling writes a note into the data file's own header as well as into
docs/rulings-applied-4sep.md.

EVERY EV-BASED MULTIPLE IN THE ROW IS REBUILT, not just the revenue one. Leaving a stale ev/gp or
ev/gmv behind would be a figure computed from an enterprise value the file no longer holds.

Idempotent: a ticker whose note is already in the header is skipped and said so.

  python3 tools/apply_bridge_zero.py
"""
import os
import sys

# ticker -> (file, why, date)
RULED = {
    'NASDAQ:XP': ('data/peers-fintech.csv',
                  "a broker's client balances net against its market cap", '4-Sep-2026'),
    'LSE:CABP': ('data/peers-fintech.csv',
                 'a cross-border payments company holding client and settlement balances', '4-Sep-2026'),
}

# The EV-based multiples this file computes, and the column each one divides by.
MULTIPLES = (('ev_ntm_revenue_x', 'revenue_ntm_musd'),
             ('ev_ntm_gp_x', 'gross_profit_musd'),
             ('ev_ntm_gmv_x', 'gmv_ntm_musd'))


def note_for(ticker, why, date):
    return ('# RULING %s (Daniil): %s equity_to_av_bridge_musd overridden to 0 and '
            'enterprise_value_musd set to market_cap_musd, because %s. The bridge components are '
            'left as supplied and no longer sum to the bridge for this row. Every EV-based '
            'multiple in the row is rebuilt from the new enterprise value. '
            'See docs/rulings-applied-4sep.md.' % (date, ticker, why))


def apply_one(path, ticker, why, date):
    src = open(path, encoding='utf-8').read().splitlines()
    stamp = '# RULING %s (Daniil): %s ' % (date, ticker)
    if any(l.startswith(stamp) for l in src):
        print('%-12s ALREADY APPLIED, note in the file header. Nothing done.' % ticker)
        return False
    header, idx = None, None
    for i, l in enumerate(src):
        if l.startswith('#'):
            continue
        if header is None:
            header = l.split(',')
            continue
        if l.split(',')[2:3] == [ticker]:
            idx = i
    if header is None or idx is None:
        print('%-12s NOT FOUND in %s' % (ticker, path))
        return False
    col = {c: n for n, c in enumerate(header)}
    f = src[idx].split(',')

    def val(c):
        try:
            return float(f[col[c]])
        except (KeyError, ValueError, IndexError):
            return None

    mc = val('market_cap_musd')
    if mc is None:
        print('%-12s NO market capitalisation in the row, cannot price on equity value' % ticker)
        return False
    print('%s  %s' % (ticker, f[col['company_name']]))
    print('   %-26s %12s -> 0' % ('equity_to_av_bridge_musd', f[col['equity_to_av_bridge_musd']]))
    print('   %-26s %12s -> %g' % ('enterprise_value_musd', f[col['enterprise_value_musd']], mc))
    f[col['equity_to_av_bridge_musd']] = '0'
    f[col['enterprise_value_musd']] = '%g' % mc
    for mult_col, den_col in MULTIPLES:
        if mult_col not in col or den_col not in col:
            continue
        den = val(den_col)
        was = f[col[mult_col]] or '(blank)'
        if den in (None, 0):
            continue
        new = mc / den
        f[col[mult_col]] = ('%.5f' % new) if abs(new) < 0.1 else ('%.1f' % new)
        flag = '   <- non-positive, so B11 marks it n.m. in the engine' if new <= 0 else ''
        print('   %-26s %12s -> %s  (%g / %g)%s' % (mult_col, was, f[col[mult_col]], mc, den, flag))
    print('   left as supplied: net_debt %s, minority %s, associates %s'
          % (f[col['net_debt_musd']], f[col['minority_interest_musd']], f[col['associates_musd']]))
    src[idx] = ','.join(f)
    last_comment = max(i for i, l in enumerate(src) if l.startswith('#') and i < 12)
    src.insert(last_comment + 1, note_for(ticker, why, date))
    open(path, 'w', encoding='utf-8').write('\n'.join(src) + '\n')
    return True


def main():
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    done = 0
    for ticker, (path, why, date) in sorted(RULED.items()):
        done += 1 if apply_one(path, ticker, why, date) else 0
    print('\n%d ruled ticker(s) in the table, %d changed by this run, no other row touched.'
          % (len(RULED), done))
    return 0


if __name__ == '__main__':
    sys.exit(main())
