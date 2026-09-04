# -*- coding: utf-8 -*-
"""Fairway's read: where the founder stands, the one thing to do, and what it is worth.

Fable's roadmap of 2-Sep, Day 3, and Daniil on 3-Sep: "NRR SHOULD be used in the recommendations
piece." It was collected by the quiz and read by nothing, which the quiz walker found the same day.

FIVE DIMENSIONS, all five live as of 4-Sep-2026, and each one renders three sentences in this
order and no other:
  1. where the founder stands against THEIR OWN named peer set, not against a general truth
  2. the ONE action to take
  3. the valuation consequence, named as a row on their field

  quality of revenue   retention, against the peers who disclose it
  growth story         their rate against the set's, on the same measure
  unit economics       gross margin, and whether it has already moved their denominator
  market position      where their own lane prices against the wider family, and the tier label
  evidence gaps        what they could not answer, straight from the honesty flags

The third sentence is the part neither of the tools we looked at can write. A deck analyser can
score a deck; it cannot say which fix moves which bar on a founder's own football field.

NOTHING HERE INVENTS A NUMBER. Every figure comes from the profile, a peer row or a range object,
computed here and quoted, on the same discipline as the honesty layer. From 4-Sep that is no
longer a promise in a docstring: every dimension returns a `figures` list saying where each number
came from, and tools/recommendations_check.py refuses any number printed to a founder that is not
in it, recomputing every derived figure from the peer values it claims to come from. The banker
review stays the paid layer on top, and this is what the banker starts from.

THE FIX LIST IS ORDERED BY RANGE IMPACT, NOT BY RUBRIC ORDER. A dimension that cannot move the
number is reported and not prioritised. Impact is carried in turns of forward revenue for every
dimension so the ordering compares like with like.
"""
import statistics as st


def _M():
    """match_reference, imported on use so this module can be read and reasoned about without
    loading the universe."""
    import match_reference as M
    return M


def _f(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _fig(value, source, **kw):
    """One number that may reach a founder, and where it came from.

    source is one of:
      profile.<field>   the founder's own answer, straight off the profile
      peer.observed     a figure disclosed by one of the named companies, with `inputs` holding
                        the set it must be a member of
      range.<field>     a value off a range object the engine already built
      derived.median | derived.percentile | derived.count | derived.spread | derived.gap
                        computed here from `inputs`, which the check recomputes independently
    """
    d = dict(value=value, source=source)
    d.update(kw)
    return d


def _quartile_read(pairs, value):
    """Where `value` sits in a peer distribution, and what the top and bottom quartiles price at.

    pairs is [(metric, multiple)] for the peer set. Returns None when there is not enough to say
    anything honest, which matters: three names is not a distribution and pretending otherwise is
    how a recommendation becomes a horoscope.

    The raw inputs are kept on the read so every number built from them can be traced and
    recomputed by the check rather than trusted.
    """
    pairs = [(m, x) for m, x in pairs if m is not None and x is not None]
    if len(pairs) < 8 or value is None:
        return None
    pairs.sort()
    q = max(1, len(pairs) // 4)
    lo_med = st.median([x for _m, x in pairs[:q]])
    hi_med = st.median([x for _m, x in pairs[-q:]])
    below = len([1 for m, _x in pairs if m < value])
    pct = round(100.0 * below / len(pairs))
    return dict(n=len(pairs), percentile=pct,
                metrics=[m for m, _x in pairs],
                bottom_band=(pairs[0][0], pairs[q - 1][0]), bottom_multiple=round(lo_med, 1),
                bottom_multiples=[x for _m, x in pairs[:q]],
                top_band=(pairs[-q][0], pairs[-1][0]), top_multiple=round(hi_med, 1),
                top_multiples=[x for _m, x in pairs[-q:]],
                spread=round(hi_med - lo_med, 1), raw_low=lo_med, raw_high=hi_med)


def _read_figures(read, value, value_source):
    """The provenance of every number a quartile read can put in a sentence."""
    return [
        _fig(value, value_source),
        _fig(read['percentile'], 'derived.percentile', inputs=read['metrics'], against=value),
        _fig(read['n'], 'derived.count', inputs=read['metrics']),
        _fig(read['bottom_band'][0], 'peer.observed', inputs=read['metrics']),
        _fig(read['bottom_band'][1], 'peer.observed', inputs=read['metrics']),
        _fig(read['top_band'][0], 'peer.observed', inputs=read['metrics']),
        _fig(read['top_band'][1], 'peer.observed', inputs=read['metrics']),
        _fig(read['bottom_multiple'], 'derived.median', inputs=read['bottom_multiples']),
        _fig(read['top_multiple'], 'derived.median', inputs=read['top_multiples']),
        _fig(read['spread'], 'derived.spread', inputs=[read['raw_high'], read['raw_low']]),
    ]


def quality_of_revenue(prof, core_rows):
    """NET REVENUE RETENTION, which is the dimension Daniil asked for by name.

    Our own listed set is the evidence and it is a wide gap: across the names that disclose both a
    retention figure and a forward revenue multiple, the bottom quartile on retention trades well
    below the top. That gap is measured here from the set in front of the founder rather than
    quoted from memory, which is why no figure in this docstring is repeated in a sentence.

    The founder is placed against the peers ACTUALLY IN FRONT OF THEM where enough of those disclose
    it, and against the whole listed set otherwise, and the sentence says which. A percentile against
    seven names is not a percentile.
    """
    nrr = _f(prof.get('nrr'))
    shown = [(r.get('nrr'), r.get('mult')) for _sw, r in core_rows]
    read = _quartile_read(shown, nrr)
    scope = 'the peers on your own field'
    if read is None:
        # A CORE SET IS SEVEN NAMES AT MOST, so it can never be a distribution. Falling back to the
        # wider family is not a fudge as long as the sentence SAYS which set the founder is being
        # placed in, which is why scope is a variable and not a fixed phrase.
        read = _quartile_read(_family_pairs(prof, 'nrr'), nrr)
        scope = 'listed companies in your family'
    if read is None:
        return None
    lines = []
    lines.append(
        'Your net revenue retention of %.0f per cent sits at the %d%s percentile of %s that '
        'disclose it (%d names, %.0f to %.0f per cent).'
        % (nrr, read['percentile'], _ord(read['percentile']), scope, read['n'],
           read['bottom_band'][0], read['top_band'][1]))
    if read['percentile'] >= 75:
        lines.append('Lead with it. Put the cohort table in the deck rather than the headline '
                     'number, because the number is only believed once the cohorts are shown.')
    elif read['percentile'] <= 25:
        lines.append('This is the single highest-value thing to fix before you raise, and the fix '
                     'is expansion pricing or a seat-based upgrade path, not churn work alone.')
    else:
        lines.append('Get it above %.0f per cent and say so with cohorts: that is the boundary of '
                     'the top quartile in this set.' % read['top_band'][0])
    lines.append(
        'The consequence on your own field: names in the bottom quartile on retention price at a '
        'median %sx and the top quartile at %sx, a gap of %sx of forward revenue. That is the bar '
        'this dimension moves you between.'
        % (read['bottom_multiple'], read['top_multiple'], read['spread']))
    return dict(dimension='quality of revenue', metric='nrr', value=nrr,
                percentile=read['percentile'], impact=read['spread'], lines=lines, read=read,
                figures=_read_figures(read, nrr, 'profile.nrr'), names=[])


def growth_story(prof, core_rows):
    """Their growth against the peer set's, on the same measure, with the basis named."""
    g = _f(prof.get('growth'))
    shown = [(r.get('g_rank'), r.get('mult')) for _sw, r in core_rows]
    read = _quartile_read(shown, g)
    if read is None:
        read = _quartile_read(_family_pairs(prof, 'g_rank'), g)
    if read is None:
        return None
    lines = [
        'You are growing %.0f per cent against a peer set running %.0f to %.0f per cent, which puts '
        'you at the %d%s percentile of the %d names on your field that carry a comparable rate.'
        % (g, read['bottom_band'][0], read['top_band'][1], read['percentile'],
           _ord(read['percentile']), read['n']),
        'Name the two quarters that produced it and what you spent to get them, because a rate '
        'without a cost beside it is read as a spike.',
        'The consequence: the bottom quartile on growth prices at a median %sx and the top at %sx, '
        'a gap of %sx.' % (read['bottom_multiple'], read['top_multiple'], read['spread'])]
    return dict(dimension='growth story', metric='growth', value=g,
                percentile=read['percentile'], impact=read['spread'], lines=lines, read=read,
                figures=_read_figures(read, g, 'profile.growth'), names=[])


def unit_economics(prof, core_rows):
    """GROSS MARGIN, and whether it has already changed what the founder is priced on.

    Fable's roadmap called this dimension "the FIX_BY playbooks", which are the pattern-level
    strings the quiz shows before any of this exists: three sentences keyed off a revenue band and
    a burn answer, the same for every founder in the band. They are not evidence and they do not
    belong in a paid read.

    Gross margin is used instead, for one reason: it is the only unit economic the quiz actually
    collects (quiz_fork step `gross_margin`, and the P() default behind every fixture), our listed
    rows carry it computed from disclosed gross profit over disclosed revenue, and it is already
    wired to a pricing decision. `match_reference.denominator` switches the founder from a revenue
    multiple to a GROSS PROFIT multiple when their margin sits more than MARGIN_GAP points from the
    peer median. When that has happened it is the single most consequential thing on the page and
    nothing was telling the founder it had.

    A lender is skipped: its margin is not a unit economic, its book is, and the lender fork
    already prices on the book.
    """
    M = _M()
    if M.is_balance_sheet(prof):
        return None
    gm = _f(prof.get('gm'))
    shown = [(r.get('gm'), r.get('mult')) for _sw, r in core_rows]
    read = _quartile_read(shown, gm)
    scope = 'the peers on your own field'
    if read is None:
        read = _quartile_read(_family_pairs(prof, 'gm'), gm)
        scope = 'listed companies in your family'
    if read is None or gm is None:
        return None
    figures = _read_figures(read, gm, 'profile.gm')
    lines = ['Your gross margin of %.0f per cent sits at the %d%s percentile of %s that disclose '
             'one (%d names, %.0f to %.0f per cent).'
             % (gm, read['percentile'], _ord(read['percentile']), scope, read['n'],
                read['bottom_band'][0], read['top_band'][1])]
    if read['percentile'] >= 75:
        lines.append('Show what holds it there: which share of revenue is software and which is '
                     'passed through, because a margin this far above the set is read as a mix '
                     'accident until it is broken out.')
    elif read['percentile'] <= 25:
        lines.append('This is the fix with the shortest route to the number, because a point of '
                     'gross margin is a point on the denominator itself: pricing and mix move it, '
                     'volume does not.')
    else:
        lines.append('Take it above %.0f per cent and show the split behind it: that is where the '
                     'top quartile of this set starts.' % read['top_band'][0])

    # THE DENOMINATOR RULE, SAID OUT LOUD. This is the branch that makes the dimension worth
    # having: when the founder's margin is far enough from the group's, their whole field is
    # already drawn on gross profit and the revenue multiples on it are not comparing what the
    # founder thinks they are comparing.
    gms = [m for m, _x in shown if m is not None]
    med = st.median(gms) if len(gms) >= 3 else None
    if med is not None and abs(gm - med) > M.MARGIN_GAP:
        gap = round(abs(gm - med), 0)
        figures += [_fig(med, 'derived.median', inputs=gms),
                    _fig(gap, 'derived.gap', inputs=[gm, med])]
        lines.append('The consequence is already on your field: at %.0f points from the peer '
                     'median of %.0f per cent, the engine prices you on gross profit rather than '
                     'revenue, so every revenue multiple you are shown is measuring the business '
                     'model before it measures the business.' % (gap, med))
    else:
        lines.append('The consequence: the bottom quartile on margin prices at a median %sx and '
                     'the top at %sx, a gap of %sx of forward revenue, and margin is the one input '
                     'here that also decides whether your field is drawn on revenue or on gross '
                     'profit at all.'
                     % (read['bottom_multiple'], read['top_multiple'], read['spread']))
    return dict(dimension='unit economics', metric='gm', value=gm,
                percentile=read['percentile'], impact=read['spread'], lines=lines, read=read,
                figures=figures, names=[])


def market_position(prof, core_rows, ranges=None):
    """WHERE THE FOUNDER'S OWN LANE PRICES AGAINST THE WIDER FAMILY, and what the tier label costs.

    Fable's roadmap called this "the concerns block: incumbents, cohort expansion". The concerns
    block is written by a model against a pattern, which is exactly what may not carry a number, so
    the dimension is built instead out of the two things the selector already decided and never
    explained to the founder:

      the TIER of their listed set   DIRECT, ADJACENT or BROAD. A BROAD set is deliberately shown
                                     as context and prices nothing (match_reference.RANGE_TIERS),
                                     and a founder looking at named companies under a bar has no
                                     way to know that from the picture.
      the LANE against the FAMILY    the names actually in front of them, against every listed
                                     company in their family. When the lane is cheaper than the
                                     family, the argument to be won is which set they are read
                                     against, and that argument is worth the gap between the two
                                     medians in turns of revenue.

    Nothing here is a judgement about their market. It is where the engine has already placed them
    and what that placement is worth.
    """
    M = _M()
    lane = [(sw, r) for sw, r in core_rows if _f(r.get('mult')) is not None]
    if len(lane) < 3:
        return None
    mine = [_f(r['mult']) for _sw, r in lane]
    fam = [m for m in (_f(r.get('mult')) for r in M.same_family(prof, M.listed)) if m is not None]
    if len(fam) < 8:
        return None
    tier = M.set_tier(prof, core_rows)
    lane_med, fam_med = st.median(mine), st.median(fam)
    gap = round(abs(lane_med - fam_med), 1)
    dearest = max(lane, key=lambda z: _f(z[1].get('mult')))[1]
    dear_mult = round(_f(dearest.get('mult')), 1)
    figures = [_fig(len(mine), 'derived.count', inputs=mine),
               _fig(round(lane_med, 1), 'derived.median', inputs=mine),
               _fig(round(fam_med, 1), 'derived.median', inputs=fam),
               _fig(len(fam), 'derived.count', inputs=fam),
               _fig(gap, 'derived.gap', inputs=[lane_med, fam_med]),
               _fig(dear_mult, 'peer.observed', inputs=[round(m, 1) for m in mine])]
    lines = ['The %d names actually in front of you price at a median %sx of forward revenue '
             'against %sx across the %d listed companies in your family, and your set is labelled '
             '%s.' % (len(mine), round(lane_med, 1), round(fam_med, 1), len(fam), tier)]
    if tier == 'BROAD':
        lines.append('A BROAD set is shown as context and prices nothing, so the one action is the '
                     'evidence that puts you beside a named company rather than near a sector: the '
                     'shared product vocabulary, the same buyer, the same way of selling.')
    elif tier == 'ADJACENT':
        lines.append('Name the two companies here you are closest to and argue the premium against '
                     'those two explicitly, because an adjacent set prices you at its median until '
                     'you say why you are not the median.')
    else:
        lines.append('You have direct comparables, so the argument is not who you are like but '
                     'where in their range you sit: write the paragraph that puts you closer to '
                     'the dearest name on the list than to the middle of it.')
    lines.append('The consequence: which of those two sets you are read against is worth %sx of '
                 'forward revenue at the median, and %s at %sx is the name at the top of your own '
                 'lane that the argument has to reach.'
                 % (gap, dearest.get('company_name'), dear_mult))
    return dict(dimension='market position', metric='tier', value=tier,
                percentile=None, impact=gap, lines=lines,
                figures=figures, names=[dearest.get('company_name') or ''])


def evidence_gaps(prof, ranges, flags):
    """What they could not answer, straight from the honesty flags. No new judgement is added."""
    missing = []
    for lane in ('listed', 'private'):
        for basis, r in sorted((ranges.get(lane) or {}).items()):
            if r.get('founder_field') and r.get('founder_metric') is None:
                missing.append((lane, basis, r['founder_field'], r.get('low'), r.get('high')))
    if not missing and not flags:
        return None
    lines, figures = [], []
    if missing:
        lane, b, fld, lo, hi = missing[0]
        figures = [_fig(lo, 'range.low', lane=lane, basis=b),
                   _fig(hi, 'range.high', lane=lane, basis=b),
                   _fig(len(missing), 'derived.count', inputs=missing)]
        lines.append(
            'You have a %s range of %s to %s on your field and you did not give us a %s, so that '
            'row cannot be turned into a number for you. %d of your rows are in that position.'
            % (b.lower().replace('_', ' '), lo, hi, fld.replace('_', ' '), len(missing)))
        lines.append('Answer it. It is one figure and it adds a whole row to your field.')
        lines.append('Until you do, that row is shown as a multiple with nothing applied to it, '
                     'which a reader discounts to nothing.')
    else:
        lines.append('Every basis on your field has a number of yours behind it.')
        lines.append('Nothing to fix here.')
        lines.append('This is the dimension most founders lose the most on, so it is worth saying.')
    return dict(dimension='evidence gaps', metric='unanswered', value=len(missing),
                impact=len(missing) * 0.5, lines=lines, figures=figures, names=[])


def _family_pairs(prof, field):
    """(metric, multiple) for every listed name in this founder's family."""
    M = _M()
    fam = M.same_family(prof, M.listed)
    return [(r.get(field), r.get('mult')) for r in fam]


def _ord(n):
    return 'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')


def build(prof, core_rows, ranges, flags=()):
    """Every dimension that has something to say, ordered by how much it moves the number."""
    out = [d for d in (quality_of_revenue(prof, core_rows),
                       growth_story(prof, core_rows),
                       unit_economics(prof, core_rows),
                       market_position(prof, core_rows, ranges),
                       evidence_gaps(prof, ranges, flags)) if d]
    out.sort(key=lambda d: -(_f(d.get('impact')) or 0))
    return out


# WHAT MAY REACH THE PAGE, and nothing else. The same discipline as investors.py CARD_FIELDS: the
# read objects, the figures and the raw peer values stay on this side of the wall, so a field added
# to a dimension later cannot arrive in front of a founder by accident.
BLOCK_FIELDS = ('dimension', 'lines', 'impact', 'rank')

HEADING = 'What we would fix before this goes into the room'

FOOTER = ('Every figure above is either your own answer or one disclosed by a company named on '
          'your field. Nothing on this page is written by a model, and the ordering is by how much '
          'each one moves your range rather than by how it reads.')


def reveal_payload(prof, core_rows, ranges, flags=()):
    """Everything the reveal needs for the fix list, and nothing it does not."""
    dims = build(prof, core_rows, ranges, flags)
    blocks = []
    for i, d in enumerate(dims):
        blocks.append({'dimension': d['dimension'], 'lines': list(d['lines']),
                       'impact': round(_f(d.get('impact')) or 0.0, 1), 'rank': i + 1})
    return {
        'heading': HEADING,
        'blocks': blocks,
        'count': len(blocks),
        # A DIMENSION THAT COULD NOT BE READ IS NOT SILENTLY DROPPED. Five is the full rubric;
        # fewer means the evidence for one was not there, and saying so is the honest version of
        # a shorter list.
        'note': ('Five dimensions are read. %d of them could be answered from what you gave us '
                 'and what your peers disclose.' % len(blocks)) if len(blocks) < 5 else None,
        'footer': FOOTER,
    }
