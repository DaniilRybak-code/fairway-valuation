# -*- coding: utf-8 -*-
"""ONE PAYLOAD. Everything the reveal draws, assembled in one place, from the engine.

Started 5-Sep-2026. This is the first half of the wiring week's headline item: "engine to reveal
connected, ranges, honesty flags, recommendations and both investor layers as one payload". The
second half is the page reading it, which is not this file.

WHY ONE OBJECT AND NOT FOUR CALLS. Today `investors.js` and `recommendations.js` each expect their
own payload from their own builder, the football field is drawn from figures written into the HTML
by hand, and the honesty strings reach nobody at all. Four sources means four chances for the page
to show a range from one run and a caveat from another. The reveal is a single claim about a single
company and it should be built in one pass or not at all.

WHAT IS IN IT, and every part already exists and is checked on its own:

  ranges         every lane the founder's fork supports, on every basis, with the founder's own
                 figure for that basis carried beside it. This is where the 5-Sep gross reading
                 arrives: a founder who gave both figures gets two revenue rows, labelled, never
                 averaged (rule B3a).
  honesty        the caveats for the lane the reveal leads on, split into what shows inline and
                 what sits behind the disclosure. `honesty.py` has always produced these and
                 nothing has ever read them.
  recommendations the fix list, from `recommendations.reveal_payload`.
  investors      both layers, from `investors.reveal_payload`.
  comparables    the named rows behind each lane, because a range whose names are not visible is
                 an assertion rather than an argument.

WHAT IS DELIBERATELY NOT IN IT.

  NO PRICE. The payload carries multiples and the founder's own metric; it does not carry a
  valuation. Multiplying is the page's job and it is one line, and keeping it there means the
  arithmetic the founder is shown is the arithmetic the hover explains.

  NO NUMBER THE FOUNDER HAS NOT PAID FOR. Ruled by Daniil on 6-Sep-2026: the public lane is free
  and complete, everything non-public is blurred, and hovering a blurred range shows the comparable
  NAMES without their multiples. `build(prof, tier='free')` is that payload. The lock is a boundary
  in the data and not a class name on the page: a locked lane keeps its shape and its names and
  loses every figure, so there is nothing behind the blur to inspect. Rule E8, as amended.

  NOTHING FROM OUTSIDE THE ENGINE. Every figure traces to a row, a range or a profile field, which
  is the same discipline check 13 already enforces on the fix list.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import match_reference as M          # noqa: E402
import honesty as H                  # noqa: E402
import investors as I                # noqa: E402
import recommendations as R          # noqa: E402

# WHICH FIELDS OF A RANGE CROSS THE WALL. The same whitelist discipline recommendations.py uses:
# the range object carries working the page has no business rendering (positioning tables, band
# internals, the raw peer rows), and passing the whole object through would put them one typo away
# from the screen.
RANGE_FIELDS = ('n', 'low', 'mid', 'high', 'display', 'dispersed', 'spread', 'thin', 'bounded',
                'closeness', 'triangulated', 'basis', 'basis_label', 'founder_metric',
                'founder_field', 'founder_low', 'founder_high', 'sole', 'band')

# ONE LINE PER COMPARABLE, and the multiple is on it. A founder who cannot see which company
# carries which multiple cannot argue with either.
PEER_FIELDS = ('company', 'ticker', 'date', 'multiple', 'growth_pct', 'retention_pct')


def _range(rng):
    if not rng:
        return None
    return {k: rng.get(k) for k in RANGE_FIELDS if rng.get(k) is not None}


def _peers(rows):
    return [{k: r.get(k) for k in PEER_FIELDS if r.get(k) is not None} for r in (rows or [])]


# WHICH LANE IS FREE. Daniil, 6-Sep-2026: "Let's start with showing public fully free and blurring
# everything that is non-public. For non-public, we can show the list of similar comps (when he
# hovers over the blurred range), without the multiples."
FREE_LANES = ('listed',)

# WHAT A LOCKED LANE IS ALLOWED TO CARRY. Rule E8 as amended: its existence, its size, the KIND of
# evidence, and the NAMES. Never a multiple, never a low, mid or high, never a founder value.
#
# The names are the change of 6-Sep and the numbers are not. A blur over a figure that is sitting in
# the DOM is not a paywall, it is a dare, so the figures still never leave the engine. The blur the
# founder sees is drawn over nothing.
LOCKED_FIELDS = ('basis', 'basis_label', 'n', 'closeness', 'thin', 'display')
# A NAME AND A DATE ARE NOT A NUMBER THE FOUNDER HAS NOT PAID FOR. The date is what makes
# the name worth seeing: "Vanta, Jul-23" tells a founder the evidence is recent, and it
# reveals nothing about the multiple.
LOCKED_PEER_FIELDS = ('company', 'ticker', 'date')


def lanes(prof, listed_core, listed_tier, picked, private_tier, tier='paid'):
    """Every lane and every basis, keyed the way the page will render them.

    THE SHAPE IS lane -> basis -> range, not lane -> range, and that is the 5-Sep change. A lender
    has always had four readings and an exchange two; from 5-Sep every revenue fork can have two as
    well, net and gross. A page built on one range per lane would have to pick one and hide the
    other, which is how the gross rounds got lost in the first place.

    `tier` is the paywall and it is a boundary in the DATA, not a class name on the page. On the
    free tier a locked lane keeps its shape and its names and loses every number, so there is
    nothing behind the blur to inspect. See rule E8 and LOCKED_FIELDS above.
    """
    out = {}
    everything = M.all_ranges(prof, listed_core, listed_tier, picked, private_tier)
    for lane in ('listed', 'private'):
        got = {}
        for basis, rng in (everything.get(lane) or {}).items():
            r = _range(rng)
            if not r:
                continue
            if tier == 'free' and lane not in FREE_LANES:
                r = {k: r[k] for k in LOCKED_FIELDS if k in r}
                r['locked'] = True
                r['peers'] = [{k: c.get(k) for k in LOCKED_PEER_FIELDS if c.get(k) is not None}
                              for c in (rng.get('table') or [])]
            else:
                r['peers'] = _peers(rng.get('table'))
            got[basis] = r
        if got:
            out[lane] = got
    return out


# THE ORDER THE CHARTS ARE READ IN, and it is Daniil's own order (6-Sep-2026): public multiples
# first, then private net, then private gross, then private per user. Public first because it is the
# lane the free tier leaves open and the one a founder can check themselves.
CHART_ORDER = (('listed', 'REVENUE'), ('listed', 'BOOK'), ('listed', 'EARNINGS'),
               ('private', 'REVENUE'), ('private', 'REVENUE_GROSS'),
               ('private', 'ARR'), ('private', 'BOOK'), ('private', 'ORIGINATIONS'),
               ('private', 'THROUGHPUT'))


# ---------------------------------------------------------------------------
# HOW WIDE IS TOO WIDE FOR A PER-USER CHART? DANIIL'S RULING, AND IT IS NOT MADE YET.
#
# The question, from the status document's rulings list: a per-user chart compares dollars of
# enterprise value per customer across the comparables. Some of them run from a few hundred dollars
# to tens of thousands, and a chart that wide reads as noise rather than as evidence. Should it be
# drawn at all above some spread?
#
# NOTHING IS HIDDEN TODAY. None means today's behaviour exactly: every per-user chart is drawn, and
# a chart wider than DISPERSION_MAX is already drawn as separate points rather than as a bar, with
# the SCATTER caveat saying in words that the names are comparable to the founder and not to each
# other. So the honest description of the current state is not "we show noise"; it is "we show it
# and we say what it is".
#
# MEASURED 7-SEP-2026 ACROSS ALL 102 FIXTURES. 60 per-user charts exist. Setting this constant
# hides the ones whose high divided by low is above it:
#
#     1000   hides  3, keeps 57
#      500   hides  4, keeps 56
#      200   hides  6, keeps 54
#      100   hides 11, keeps 49        <- the recommendation in the status document
#       50   hides 16, keeps 44
#       25   hides 26, keeps 34
#       10   hides 32, keeps 28
#
# FOR SCALE, AND THIS IS THE NUMBER THAT DECIDES IT: the 245 revenue charts have a MEDIAN spread of
# 3.3x and a widest of 110x. A per-user chart at 1,034x is not a wide version of the same thing; it
# is a different kind of object. The three widest all run $19,333 to $20,000,000 per business
# customer, which is a chart saying one comparable is worth a thousand of another per customer.
#
# THE ARGUMENT FOR SHOWING THEM ANYWAY, since it is a real one: a founder who has typed nothing has
# only these charts, and hiding the widest takes the only per-user evidence away from the fixtures
# that have least. Eleven charts at the 100 setting sit on nine fixtures.
#
# SET THE NUMBER AND NOTHING ELSE CHANGES. Golden will move on the fixtures that lose a chart, and
# the reason is this constant, which is why it is a constant with the measurement beside it rather
# than a threshold buried in a condition.
#
# CLOSED 7-SEP-2026 WITHOUT A NUMBER, and this is the better outcome. Daniil's answer to the
# question was not a threshold: "I thought we decided to exclude the super high user-based
# multiples, given they are calculated for B2B clients and such businesses do not price on that
# basis." Removing those readings at source (PER_CUSTOMER_BUSINESS_MAX in match_reference.py) took
# the widest per-user chart from 1,034x to 97x, so there is nothing left for a width rule to hide.
# The lever stays, unset, because a width rule treats a symptom and the rule above treats the cause.
PER_USER_SPREAD_MAX = None


def charts(ranges):
    """The bar charts this founder can actually be shown, in reading order.

    Daniil, 6-Sep-2026: "what if the user does not want to give us the numbers at all? Then we
    should be able just to show the peers and how they trade. So in the reveal he would get 2-3 bar
    charts (to the extent available), with the (i) public peers multiples, (ii) private peers
    multiples (net), (iii) private peers multiples (gross), (iv) private peers multiples based on
    number of users."

    THIS IS THE WHOLE PRODUCT FOR A FOUNDER WHO TYPES NOTHING, so it is built as its own list rather
    than left for the page to assemble out of `ranges`. Each entry carries what a bar needs and
    nothing else: how many names are behind it, the low, mid and high, the label of the measure, and
    `priced`, which says whether the founder gave the figure that turns the multiple into a value.

    `priced` false is the normal case, not an error. The chart is still worth drawing: it is what
    investors paid for companies like theirs, which is the argument, and the founder can put their
    own number against it later.
    """
    out, seen = [], set()
    counts = [(lane, b) for lane in ('private',) for b in sorted((ranges.get(lane) or {}))
              if b in M.COUNT_BASES]
    for lane, basis in list(CHART_ORDER) + counts:
        r = (ranges.get(lane) or {}).get(basis)
        if not r or (lane, basis) in seen:
            continue
        seen.add((lane, basis))
        # The per-user width rule, off until Daniil names a number. A locked lane carries no
        # figures, so it cannot be measured and is never hidden by this: the lock already hides it.
        if (PER_USER_SPREAD_MAX and basis in M.COUNT_BASES
                and r.get('low') and r.get('high') and r['low'] > 0
                and (r['high'] / r['low']) > PER_USER_SPREAD_MAX):
            continue
        out.append({'lane': lane, 'basis': basis, 'label': r.get('basis_label'),
                    'n': r.get('n'), 'low': r.get('low'), 'mid': r.get('mid'),
                    'high': r.get('high'), 'display': r.get('display'),
                    'thin': r.get('thin'), 'closeness': r.get('closeness'),
                    'priced': r.get('founder_metric') is not None,
                    'locked': bool(r.get('locked')),
                    'founder_low': r.get('founder_low'), 'founder_high': r.get('founder_high')})
    return out


def lead_range(prof, picked, private_tier):
    """The lane the reveal leads on, and the one the honesty strings are written about.

    The private lane on its default basis, which is what `honesty.caveats` has always been driven
    with and what `tools/honesty_check.py` reports. Named here rather than assumed by the caller,
    so that when the lead changes it changes in one place.
    """
    return M.private_range(prof, picked, private_tier) or {}


def build(prof, raise_musd=None, want_investors=8, tier='paid'):
    """The whole reveal for one profile, in one pass over the engine.

    Every lane comes from ONE selection run. The alternative, letting each block select its own
    peers, is how a range and the investor list behind it end up describing different companies.
    """
    core, sec, listed_tier = M.peer_groups(prof, M.listed)
    picked, window_months, private_tier = M.select_private(prof, M.private)
    lead = lead_range(prof, picked, private_tier)

    # THE CAVEATS COME OFF THE LEAD RANGE, AND THE LEAD RANGE IS THE PRIVATE ONE, so on the free
    # tier they are written without the figures the lock is over. See the long note in
    # honesty.caveats(): two of the sentences printed the locked high in prose, one line under the
    # blur, and nothing caught it until the render harness drew the page.
    lead_locked = (tier == 'free' and 'private' not in FREE_LANES)
    caveats = H.caveats(prof, lead, redact=lead_locked)
    rngs = lanes(prof, core, listed_tier, picked, private_tier, tier=tier)
    return {
        'tier': tier,
        'ranges': rngs,
        # WHAT A FOUNDER WHO TYPED NOTHING SEES. Built here rather than left to the page, because it
        # is the whole reveal for that founder and it must not depend on the page guessing an order.
        'charts': charts(rngs),
        # THE LANE THE PAGE LEADS ON, named rather than inferred from dict order.
        # THE LEAD RANGE IS THE PRIVATE ONE AND THE PRIVATE LANE IS LOCKED ON THE FREE TIER, so on
        # that tier the lead carries no figures either. Missing this would hand the free payload the
        # exact numbers the lock is over, through a second door.
        'lead': {'lane': 'private', 'basis': M.basis_for(prof),
                 'range': (None if (tier == 'free' and 'private' not in FREE_LANES)
                           else _range(lead))},
        'proximity': {'listed': listed_tier, 'private': private_tier,
                      'private_window_months': window_months},
        # HONESTY REACHES A FOUNDER FOR THE FIRST TIME HERE. Two lists, not one with a flag,
        # because inline and behind-the-disclosure are two different places on the page and the
        # split is already decided by severity in honesty.py.
        'honesty': {
            'inline': [{'key': c['key'], 'text': c['text']} for c in caveats if c['inline']],
            'disclosure': [{'key': c['key'], 'text': c['text']} for c in caveats
                           if not c['inline']],
            'count': len(caveats),
        },
        'recommendations': R.reveal_payload(prof, core, lead,
                                            flags=tuple(c['key'] for c in caveats)),
        'investors': I.reveal_payload(prof, picked, raise_musd=raise_musd, want=want_investors),
    }
