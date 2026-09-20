# -*- coding: utf-8 -*-
"""THE GROWTH REGRESSION, read at the founder's FORWARD growth.

One row on the football field: EV to NTM revenue fitted against growth across the founder's own
extended listed peer set (the same ranking the peer sets use, taken REGRESSION_N deep), then read
off the line at the founder's growth rate, a tenth either side (REGRESSION_GROWTH_SPAN).

RULED BY DANIIL, 20-Sep-2026, after the D2C run, and this file is those rulings:

  "The regression is built on peers' forecasted growth and the user's FORWARD growth should be
   applied to build it." Every listed peer's `g` is a forecast (CAGR CY1 to CY3, with the
   fallbacks named on the listed sheet). Until today the line was read at the founder's TRAILING
   rate (`prof['growth']`, step 4's "over the last twelve months"): a forward line read at a
   backward number. Now it is read at the plan they gave at step 4 (`growth_plan`, typed as a rate
   or back-calculated from a revenue target) and, only when they gave no plan, at the trailing
   rate as a stand-in. The result says which (`growth_basis`), so the page can say it too.

  "When R2 for public peers regression is below 0.4, we should disclaim that with a callout to
   that range on FF." The 4-Sep gate hid the row below R2 0.50. Now the fitted range is published
   whenever a line can be drawn and read inside the peers' own growth range, and `weak_fit` is
   True below REGRESSION_WEAK_R2 so the field draws the callout beside the bar.

  UNCHANGED, pending his ruling: the extrapolation refusal. A founder whose growth sits outside
   the peers' own range (more than EXTRAPOLATION_LIMIT beyond the fastest of them) is still not
   read off the line, because a line is only evidence inside the range it was fitted on. The
   refusal carries the numbers (their growth, the peers' low and high, the count, the fit) so the
   field can say why in a sentence rather than an adjective.

WHY A NEW FILE. match_reference.regression_range() (4-Sep) is the function this replaces, and it
is the only caller-facing change. It could not be rewritten in place today: match_reference.py
cannot be written from the session that made this change (no folder attached, and a 189 KB file
is not retyped through the GitHub API by hand). It stays in match_reference.py, unreferenced,
until that file is next written, and then it is deleted. NOTHING HERE IS A COPY: the peer
selection is the engine's own, imported (same_family, score, _relevant, _ols and the constants),
so the fifteen names fitted are the fifteen the engine would pick.

The founder's rates and the peers' `g` are both percentages (47 means 47%), as the profiler and
the listed sheet carry them.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import match_reference as M          # noqa: E402

# Below this the row is drawn WITH A CALLOUT (Daniil, 20-Sep-2026: "when R2 is below 0.4, we should
# disclaim that"). It replaces REGRESSION_MIN_R2 = 0.50, which hid the row instead.
REGRESSION_WEAK_R2 = 0.40


def founder_growth(prof):
    """The rate the line is read at, and where it came from.

    ('plan') when step 4's plan was given, ('trailing') when only the last twelve months were,
    (None, None) when neither. The plan wins because the peers' rates are forecasts.
    """
    for key, basis in (('growth_plan', 'plan'), ('growth', 'trailing')):
        v = prof.get(key)
        if v is None:
            continue
        try:
            return float(v), basis
        except (TypeError, ValueError):
            continue
    return None, None


def regression_range(prof, universe, which='rev', want=M.REGRESSION_N):
    """Fit EV/denominator against growth across the founder's extended peer set and read the range
    off the line at their forward growth.

    Returns None when no growth rate was given at all. Otherwise always a dict, and it is one of:

      the fitted range      low / mid / high, r2, n, weak_fit, growth, growth_basis, the peers
      a refusal             refused = 'TOO_FEW' (fewer than REGRESSION_MIN_POINTS usable peers),
                            'OUT_OF_RANGE' (their growth outside the peers' range, see above), or
                            'NEGATIVE' (the line implies a multiple at or below zero there)

    A refusal publishes no range and no line; it carries the numbers the field needs to say why.
    """
    growth, basis = founder_growth(prof)
    if growth is None:
        return None
    univ = M.same_family(prof, universe)
    scored = sorted(((M.score(prof, r), r) for r in univ), key=lambda z: -z[0][0])
    scored = [x for x in scored if M._relevant(prof, x[1], x[0][1])][:want]
    key = 'mult' if which == 'rev' else 'gp_mult'
    pts = [(r['g'], r[key], r) for _s, r in scored
           if r.get('g') is not None and r.get(key) is not None]
    out = dict(n=len(pts), growth=growth, growth_basis=basis, denominator=which)
    fit = M._ols([p[0] for p in pts], [p[1] for p in pts])
    if not fit:
        out['refused'] = 'TOO_FEW'
        return out
    a, b, r2 = fit
    gs = [p[0] for p in pts]
    out.update(r2=round(r2, 3), weak_fit=(r2 < REGRESSION_WEAK_R2),
               peer_growth_low=round(min(gs), 1), peer_growth_high=round(max(gs), 1))
    # A tenth either side of the founder's rate. Sorted, because a negative rate flips the ends.
    lo_g, hi_g = sorted([growth * (1 - M.REGRESSION_GROWTH_SPAN), growth * (1 + M.REGRESSION_GROWTH_SPAN)])
    ceiling = max(gs) * (1 + M.EXTRAPOLATION_LIMIT)
    floor = min(gs) - abs(min(gs)) * M.EXTRAPOLATION_LIMIT - 5.0
    if hi_g > ceiling or lo_g < floor:
        out.update(refused='OUT_OF_RANGE', out_of_range=True)
        return out
    v = sorted([a + b * lo_g, a + b * hi_g])
    if v[1] <= 0:                                  # a downward line can imply a negative multiple
        out['refused'] = 'NEGATIVE'
        return out
    out.update(intercept=round(a, 3), slope=round(b, 4),
               growth_low=round(lo_g, 1), growth_high=round(hi_g, 1),
               low=round(max(0.0, v[0]), 1), mid=round((v[0] + v[1]) / 2, 1), high=round(v[1], 1),
               peers=[{'company': r['company_name'], 'ticker': r.get('exchange_ticker', ''),
                       'growth': r['g'], 'mult': r[key]} for _g, _m, r in pts])
    return out
