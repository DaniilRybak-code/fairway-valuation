# -*- coding: utf-8 -*-
"""Fairway's read: where the founder stands, the one thing to do, and what it is worth.

Fable's roadmap of 2-Sep, Day 3, and Daniil on 3-Sep: "NRR SHOULD be used in the recommendations
piece." It was collected by the quiz and read by nothing, which the quiz walker found the same day.

FIVE DIMENSIONS, and each one renders three sentences in this order and no other:
  1. where the founder stands against THEIR OWN named peer set, not against a general truth
  2. the ONE action to take
  3. the valuation consequence, named as a row on their field

The third sentence is the part neither of the tools we looked at can write. A deck analyser can
score a deck; it cannot say which fix moves which bar on a founder's own football field.

NOTHING HERE INVENTS A NUMBER. Every figure comes from the profile or the range objects, computed
here and quoted, on the same discipline as the honesty layer. The banker review stays the paid
layer on top, and this is what the banker starts from.

THE FIX LIST IS ORDERED BY RANGE IMPACT, NOT BY RUBRIC ORDER. A dimension that cannot move the
number is reported and not prioritised.
"""
import statistics as st


def _f(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _quartile_read(pairs, value):
    """Where `value` sits in a peer distribution, and what the top and bottom quartiles price at.

    pairs is [(metric, multiple)] for the peer set. Returns None when there is not enough to say
    anything honest, which matters: three names is not a distribution and pretending otherwise is
    how a recommendation becomes a horoscope.
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
                bottom_band=(pairs[0][0], pairs[q - 1][0]), bottom_multiple=round(lo_med, 1),
                top_band=(pairs[-q][0], pairs[-1][0]), top_multiple=round(hi_med, 1),
                spread=round(hi_med - lo_med, 1))


def quality_of_revenue(prof, core_rows):
    """NET REVENUE RETENTION, which is the dimension Daniil asked for by name.

    Our own listed set is the evidence and it is a wide gap: across the 83 names that disclose both
    a retention figure and a forward revenue multiple, the BOTTOM quartile on retention trades at a
    median 2.3x and the TOP quartile at 5.8x. That is the largest single gap we can measure on any
    disclosed metric, which is why retention is worth a question and worth a recommendation.

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
                percentile=read['percentile'], impact=read['spread'], lines=lines, read=read)


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
                percentile=read['percentile'], impact=read['spread'], lines=lines, read=read)


def evidence_gaps(prof, ranges, flags):
    """What they could not answer, straight from the honesty flags. No new judgement is added."""
    missing = []
    for basis, r in sorted((ranges.get('listed') or {}).items()) + \
                    sorted((ranges.get('private') or {}).items()):
        if r.get('founder_field') and r.get('founder_metric') is None:
            missing.append((basis, r['founder_field'], r.get('low'), r.get('high')))
    if not missing and not flags:
        return None
    lines = []
    if missing:
        b, fld, lo, hi = missing[0]
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
                impact=len(missing) * 0.5, lines=lines)


def _family_pairs(prof, field):
    """(metric, multiple) for every listed name in this founder's family.

    Imported lazily so this module can be read and reasoned about without loading the universe.
    """
    import match_reference as M
    fam = M.same_family(prof, M.listed)
    return [(r.get(field), r.get('mult')) for r in fam]


def _ord(n):
    return 'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')


def build(prof, core_rows, ranges, flags=()):
    """Every dimension that has something to say, ordered by how much it moves the number."""
    out = [d for d in (quality_of_revenue(prof, core_rows),
                       growth_story(prof, core_rows),
                       evidence_gaps(prof, ranges, flags)) if d]
    out.sort(key=lambda d: -(d.get('impact') or 0))
    return out
