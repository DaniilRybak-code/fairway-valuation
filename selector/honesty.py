# -*- coding: utf-8 -*-
"""The honesty copy, as code.

docs/honesty-copy.md is the deck of sentences the engine owes a founder. This turns it into a
function so that the sentences are chosen the same way every time, and so the choosing can be
tested against every fixture before anything reaches a screen.

THE ONE DESIGN DECISION, and it is the reason this file exists rather than a template in the page:
eleven caveats on one screen is not honesty, it is noise. At most TWO are shown inline, ranked by
severity, and the rest sit behind a "how this was built" disclosure any founder can open. The
ranking is fixed here, not left to whoever writes the markup:

  1  the number may not be about this founder at all  (THIN_OVERLAP, anchor_dropped)
  2  the number is directional and means something other than it says  (bounded)
  3  everything else

Three rules the sentences follow, from the deck:
  say the fact then say what to do with it; never apologise for the data; print the working where
  we have it, because shared_words, control_names and sole are all printable.
"""

SEV_BASIS, SEV_IDENTITY, SEV_DIRECTION, SEV_CONTEXT = 0, 1, 2, 3
INLINE_MAX = 2


def _words(xs):
    xs = [x for x in (xs or []) if x]
    if not xs: return ''
    if len(xs) == 1: return xs[0]
    return ', '.join(xs[:-1]) + ' and ' + xs[-1]


def _x(v):
    if v is None: return ''
    return ('%g' % round(float(v), 1)) + 'x'


def caveats(prof, r, regression=None):
    """Return the caveats a range owes, most severe first.

    `r` is what private_range() or group_range() returns. `regression` is the regression result
    or None. Every entry is {key, severity, text}; the caller shows the first INLINE_MAX inline
    and puts the rest behind the disclosure.
    """
    out = []
    if not r or not r.get('n'):
        return out
    n = r.get('n')
    lo, hi = r.get('low'), r.get('high')
    basis = r.get('basis', 'REVENUE')

    # --- 1. the number may not be about this founder -----------------------
    if r.get('closeness') == 'THIN_OVERLAP':
        shared = _words(r.get('shared_words'))
        # NO SHARED WORDS AT ALL IS THE HONEST CASE, NOT AN EMPTY QUOTE. Honestly is the fixture
        # that caught this: it prints share little more than "" without the branch.
        out.append(dict(key='thin_overlap', severity=SEV_IDENTITY, text=(
            ('We do not have a close comparable for you yet. The nearest companies share little '
             'more than "%s" with you. ' % shared) if shared else
            ('We do not have a close comparable for you yet. Not one company in our set describes '
             'itself the way you describe yourself. ')) + (
            'The range below is the best available read, not a peer set, and we would not put our '
            'name to it without a conversation.')))
    if r.get('anchor_dropped'):
        out.append(dict(key='anchor_dropped', severity=SEV_IDENTITY, text=(
            'The company you will recognise here is not in the number. Its only transaction cannot '
            'price a minority round, so the range is built from the others. Worth knowing before '
            'you quote it.')))

    # --- 2. the number is directional --------------------------------------
    if r.get('bounded'):
        out.append(dict(key='bounded', severity=SEV_DIRECTION, text=(
            'At most %s. Some of these rounds disclosed revenue as a threshold, "more than $100m" '
            'rather than a figure, so the true multiple is lower than shown, not higher. We would '
            'rather understate than flatter.' % _x(hi))))

    # --- 3. everything else -------------------------------------------------
    if r.get('display') == 'DIAMOND':
        out.append(dict(key='sole', severity=SEV_CONTEXT, text=(
            'One company matches you closely enough to price from: %s. A single point is not a '
            'range, so treat it as a marker rather than a spread. More rounds in this category '
            'will widen it.' % (r.get('sole') or 'that company'))))
    if r.get('display') == 'SCATTER':
        out.append(dict(key='scatter', severity=SEV_CONTEXT, text=(
            'These companies are comparable to you but they are not comparable to each other: %s '
            'to %s. Averaging them would produce a number none of them supports, so they are shown '
            'as separate points. Where you land in that spread is the argument, and it is usually '
            'about growth.' % (_x(lo), _x(hi)))))
    if r.get('closeness') == 'SHARED_PRODUCT':
        out.append(dict(key='shared_product', severity=SEV_CONTEXT, text=(
            'These companies do what you do. Shared product language: %s.' % _words(r.get('shared_words')))))
    if r.get('closeness') == 'STRONG_OVERLAP':
        out.append(dict(key='strong_overlap', severity=SEV_CONTEXT, text=(
            'Close, on %d shared descriptors: %s. Not identical businesses, which is normal.'
            % (len(r.get('shared_words') or []), _words(r.get('shared_words')))))) 
    if r.get('closeness') == 'PARTIAL_OVERLAP':
        out.append(dict(key='partial_overlap', severity=SEV_CONTEXT, text=(
            'The nearest businesses we hold. They share %s with you and diverge elsewhere. Read the '
            'range as a starting point you can argue up or down, not as a verdict.'
            % _words(r.get('shared_words')))))
    if r.get('thin'):
        out.append(dict(key='thin', severity=SEV_CONTEXT, text=(
            'Drawn from %d priced rounds. Thin, and a fourth could move it.' % n)))
    if r.get('band') == 'ADJACENT':
        out.append(dict(key='adjacent', severity=SEV_CONTEXT, text=(
            'Priced off businesses in your category rather than your exact niche.')))
    if r.get('control_names'):
        out.append(dict(key='control', severity=SEV_CONTEXT, text=(
            '%s is a change of control. A buyer of the whole company pays for control, so that '
            'multiple sits above what the same business would fetch in a minority round.'
            % _words(r.get('control_names')))))
    if r.get('listed_target_names'):
        out.append(dict(key='listed_target', severity=SEV_CONTEXT, text=(
            '%s was a public company when it was bought, so its price was set by the stock market '
            'rather than negotiated with one investor. Different kind of price, not a slower '
            'version of the same kind.' % _words(r.get('listed_target_names')))))
    mix = r.get('basis_mix') or {}
    if len(mix) > 1:
        out.append(dict(key='basis_mix', severity=SEV_CONTEXT, text=(
            'These rounds were priced on different measures: %s. We have matched you to the '
            'closest, and the mix is why the spread is wider than it looks.'
            % _words([k.replace('_', ' ').lower() for k in sorted(mix)]))))

    # A LENDER IS ON A DIFFERENT AXIS AND MUST BE TOLD SO. Added 27-Aug-2026 with the book basis.
    if basis == 'BOOK':
        out.append(dict(key='book_basis', severity=SEV_BASIS, text=(
            'You are priced on %s, not on revenue. A lender\'s revenue is interest earned on '
            'borrowed money, so it grows with how much you have borrowed rather than with what the '
            'business is worth. Book value nets the funding off the assets, which is why every '
            'listed lender is valued this way.' % (r.get('basis_label') or 'price to book'))))

    if regression is not None:
        if regression.get('refused_extrapolation'):
            out.append(dict(key='regression_refused', severity=SEV_CONTEXT, text=(
                'No listed company in your category grows as fast as you do. We can fit a line to '
                'them but we cannot honestly read your value off the end of it, so this row is '
                'blank. This is a gap in the data, not in your business, and it is the reason the '
                'private rounds matter more for you than the public comparables do.')))
        elif regression.get('r2') is not None and not regression.get('ok'):
            out.append(dict(key='regression_weak', severity=SEV_CONTEXT, text=(
                'We could not draw a defensible line through these companies: their multiples are '
                'not explained by their growth. That usually means the set is not homogeneous '
                'enough to regress, so we have left the row out rather than fit a line to noise.')))

    out.sort(key=lambda c: c['severity'])
    for i, c in enumerate(out):
        c['inline'] = i < INLINE_MAX
    return out


def inline(prof, r, regression=None):
    return [c for c in caveats(prof, r, regression) if c['inline']]


def disclosure(prof, r, regression=None):
    return [c for c in caveats(prof, r, regression) if not c['inline']]
