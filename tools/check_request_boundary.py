# -*- coding: utf-8 -*-
"""CHECK 15. Does a founder's figure leave the browser?

WHY THIS CHECK EXISTS. Daniil, 6-Sep-2026: "we only take a record of the company data (profile,
website), without storing the numbers. Then he gets the reveal based on the numbers he put in (we
still do not see any financials at that point). Then if the user wants to have his numbers and ff
reviewed, he presses a button and it comes through to us, in which case he would specifically agree
for us to see it."

That is a promise printed on the landing page before the quiz. A promise in copy with nothing
holding it up is a promise that lasts until the next hurried edit, which is the lesson of the two
days before it: the honesty strings were correct and unread for eleven days, the gross rounds sat
in the right archetype for a fortnight, and both survived because every check passed.

WHAT IT ASSERTS, and every line is a thing that would break the promise rather than crash the page:

  1. THE ALLOWLIST IS WHAT IT SAYS IT IS. reveal-request.js declares the fields that may leave the
     browser on the free path. Every one of them is named below with a reason. A field added on one
     side and not the other fails here, in both directions.
  2. NOTHING ON THE ALLOWLIST IS A FIGURE. This file holds its own list of figure names and refuses
     to take reveal-request.js's word for anything.
  3. THE BUILDERS CONTAIN NO FIELD NAME OF THEIR OWN. They loop over the allowlist. A hand-written
     assignment is how a boundary grows a hole.
  4. EVERY REQUEST IN THE PRODUCT IS BUILT BY ONE OF THEM. A fetch() anywhere in the page with a
     hand-made body is a second door.
  5. THE BUILDERS ACTUALLY BEHAVE. Run, not read: a responses object carrying every field the quiz
     collects, with a sentinel value in every figure, goes in and the output is inspected.
  6. THE SERVER REFUSES WHAT THE PAGE SHOULD NOT HAVE SENT. api/lead.js is handled twice, with and
     without a consent block, and the figure columns are checked in the response and the log.
  7. NO FIGURE REACHES THE MODEL. api/reveal.js is handled with every figure in the body and the
     outbound call is intercepted, so what would have gone to the model is read rather than assumed.
  8. THE PAGE'S ARITHMETIC IS THE ENGINE'S ARITHMETIC. The multiplication moved into the browser,
     so there are two implementations of one sum. Real payload rows from the real engine go through
     reveal-figures.js and the answers are compared with round(v * low, 2), which is what
     match_reference.py computes and what check 14 recomputes.
  9. NO BROWSER STORAGE. A figure written to disk survives the promise. localStorage,
     sessionStorage, IndexedDB and document.cookie appear in none of the three reveal files.
 10. THE COPY AND THE CODE AGREE. The sentence before the quiz is on the page, and the old
     disclaimer line that said the commentary service "receives the business figures alone" is gone,
     because it now receives no figure at all.

IT NEEDS NODE. Half of what is above can only be established by running the code, and node is
already a hard dependency of this product: api/lead.js and api/reveal.js are Node functions on
Vercel. If node is missing this check fails and says so rather than quietly testing half as much.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'selector'))
os.chdir(HERE)

PROBE = os.path.join(HERE, 'tools', 'request_boundary_probe.mjs')

# ---------------------------------------------------------------------------
# 1. THE ALLOWLIST, WITH A REASON BESIDE EVERY FIELD.
#
# This is the check's own copy and it is deliberately a second copy. reveal-request.js is what the
# browser runs; this is what a person agreed to. They are compared in both directions, so adding a
# field to the page means writing down here why it may leave the browser.
# ---------------------------------------------------------------------------
ALLOWED = {
    # Company data. Daniil's words: "we only take a record of the company data (profile, website)".
    'stage':          'Pre-seed, Seed or Series A. The founder\'s own answer to step 1, and the '
                      'investor stage gate reads it.',
    'sector':         'the leading sector chip, which starts the archetype match',
    'sectors':        'up to three sector chips in the order picked',
    'sector_detail':  '"in your own words" when the sector is Other. A description, not an amount.',
    'website':        'the heaviest input the matcher has. See docs/engine-architecture.md.',
    'company':        'the company name. Company data, not a figure.',
    'country':        'resolved from the edge header at boot, never asked. Geography scores the '
                      'investor list.',
    'revenue_model':  'HOW they charge (subscription, transaction fee), never HOW MUCH',
    # Fork labels. Words, not amounts.
    'funding_model':  'balance sheet, marketplace or forward-flow. Decides whether a lender may be '
                      'priced on revenue at all.',
    'volume_unit':    'tonnes, transactions, USD. The unit, never the quantity.',
    'revenue_basis':  'net, gross or both. WHICH measure the founder\'s figure is on, never how '
                      'much of it. Rule B3a.',
    # The two ratios, and the growth rate in the shapes the quiz collects it in.
    'growth':         'the growth band label. band_compatible gates the private lane on it.',
    'growth_yoy':     'the trailing growth rate, a percentage. g_rank ranks peers on it.',
    'growth_plan':    'the planned growth rate, a percentage',
    'gross_margin':   'a percentage. denominator() decides on it whether the reveal leads on '
                      'revenue or on gross profit.',
}

# ---------------------------------------------------------------------------
# 2. THE FIGURES. The check's own list, and it never reads reveal-request.js to build it.
# ---------------------------------------------------------------------------
FIGURE_NAMES = (
    'revenue', 'revenue_exact', 'revenue_gross', 'arr', 'arr_exact', 'mrr',
    'ebitda', 'ebitda_ltm', 'net_income', 'book_value', 'originations', 'volume',
    'last_round_amount', 'last_round_value', 'raise', 'profit', 'valuation',
    'subscribers', 'borrowers', 'members', 'customers', 'business_customers',
    'merchants', 'active_users', 'registered_users',
    'ntmM', 'exitArrM', 'runRateM', 'markerM', 'ebitdaM', 'computed',
)

# FREE TEXT IS A FIGURE FIELD IN PRACTICE. A founder asked "anything else about your growth?" writes
# "we went from 40k to 90k MRR". A box that does not ask for a number still collects them.
FREE_TEXT_NAMES = ('growth_detail', 'concern_notes', 'context_link', 'notes', 'link')

# The lead carries these on top of the allowlist, and each one is a deliberate decision.
LEAD_EXTRA = {
    'email':      'the whole point of the lead is a person emailing the founder back',
    'phone':      'the same, and it is optional on the page',
    'concerns':   'the worry chips. Labels we wrote, never the founder\'s own prose.',
    'variant':    'which hook they arrived on. Analytics.',
    'utm_source': 'analytics',
    'currency':   'a label. Which currency the founder thinks in, never an amount in it.',
    'type':       'lead, partial, enrichment or figures. The sheet already sorts on it.',
    'consent':    'the consent block itself, which is what opens the figure columns.',
}

# Probe values for assertion 8. THESE ARE NOT DATA AND THEY DESCRIBE NO COMPANY. They are inputs to
# a multiplication, chosen to span four orders of magnitude, exactly as check_period_conversion.py
# uses known inputs with known answers to test the period conversion.
ARITHMETIC_PROBES = (0.6, 12.5, 250.0, 0.017)


def read(path):
    with open(os.path.join(HERE, path), encoding='utf-8') as fh:
        return fh.read()


def strip_comments(src):
    """The code with every comment blanked and the line count kept.

    Every file in this repo carries more prose than code, on purpose, and the prose says the word
    localStorage in the sentence that promises not to use it. A check that reads the comments finds
    the promise and reports it as the breach.
    """
    out, i, n = [], 0, len(src)
    while i < n:
        two = src[i:i + 2]
        if two == '/*':
            j = src.find('*/', i + 2)
            j = n if j == -1 else j + 2
            out.append(re.sub(r'[^\n]', ' ', src[i:j]))
            i = j
        elif two == '//':
            j = src.find('\n', i)
            j = n if j == -1 else j
            out.append(' ' * (j - i))
            i = j
        else:
            out.append(src[i])
            i += 1
    return ''.join(out)


def array_literal(src, name):
    """The entries of `var NAME = [ 'a', 'b' ];` in order, or None if it is not there.

    Read from the comment-stripped source, because every entry in those arrays carries a comment
    explaining itself and an apostrophe in one of them would otherwise read as a field name.
    """
    code = strip_comments(src)
    m = re.search(r'var\s+' + re.escape(name) + r'\s*=\s*\[(.*?)\]\s*;', code, re.S)
    if not m:
        return None
    return re.findall(r"'([^']+)'", m.group(1))


def function_body(src, name):
    """The text of `function NAME(...) { ... }`, matched by brace depth."""
    m = re.search(r'function\s+' + re.escape(name) + r'\s*\([^)]*\)\s*\{', src)
    if not m:
        return None
    i, depth = m.end(), 1
    while i < len(src) and depth:
        if src[i] == '{':
            depth += 1
        elif src[i] == '}':
            depth -= 1
        i += 1
    return src[m.end():i - 1]


def close(a, b):
    """The same tolerance check 14 uses, for the same reason: two languages round differently at
    the half and the difference is never a difference a founder can see."""
    if a is None or b is None:
        return a is None and b is None
    return abs(a - b) <= max(0.01, abs(b) * 0.005)


def main():                                                     # noqa: C901
    bad = []
    notes = []

    rq = read('reveal-request.js')
    fg = read('reveal-figures.js')
    rc = read('reveal-client.js')
    app = read('app.js')
    lead_js = read('api/lead.js')
    reveal_js = read('api/reveal.js')
    html = read('index.html')

    # ---- 1. the allowlist, both directions ----
    groups = ['REVEAL_PROFILE_FIELDS', 'REVEAL_FORK_LABELS', 'REVEAL_RATIOS']
    declared = []
    for g in groups:
        got = array_literal(rq, g)
        if got is None:
            bad.append('reveal-request.js: %s is not a flat array literal, so this check cannot '
                       'read the boundary at all' % g)
        else:
            declared.extend(got)
    for f in declared:
        if f not in ALLOWED:
            bad.append('reveal-request.js sends "%s" and tools/check_request_boundary.py does not '
                       'allow it. Add it to ALLOWED with the reason it may leave the browser, or '
                       'take it out of the page.' % f)
    for f in ALLOWED:
        if f not in declared:
            bad.append('ALLOWED names "%s" and reveal-request.js does not send it. One of the two '
                       'is out of date.' % f)

    # ---- 2. nothing on the allowlist is a figure ----
    for f in declared:
        if f in FIGURE_NAMES:
            bad.append('"%s" is a figure and it is on the allowlist' % f)
        if f in FREE_TEXT_NAMES:
            bad.append('"%s" is free text the founder writes, which is where figures end up when '
                       'no box asks for one, and it is on the allowlist' % f)

    # ---- 3. the builders contain no field name of their own ----
    rq_code = strip_comments(rq)
    for fn in ('buildRevealRequest', 'buildLeadRecord'):
        body = function_body(rq_code, fn)
        if body is None:
            bad.append('reveal-request.js: %s is missing' % fn)
            continue
        for name in FIGURE_NAMES + FREE_TEXT_NAMES:
            if re.search(r"['\"]" + re.escape(name) + r"['\"]", body):
                bad.append('%s names "%s" in its own body. The builders loop over the allowlist and '
                           'nothing else.' % (fn, name))

    # ---- 4. every request in the product is built by one of them ----
    BUILDERS = ('buildRevealRequest', 'buildLeadRecord', 'buildReviewRequest')
    for path, src in (('app.js', strip_comments(app)), ('reveal-client.js', strip_comments(rc))):
        for m in re.finditer(r'body:\s*([^\n]+)', src):
            line = m.group(1)
            if 'JSON.stringify' not in line:
                continue
            if not any(b in line for b in BUILDERS) and 'body)' not in line:
                bad.append('%s posts a hand-made request body: %s' % (path, line.strip()[:90]))
    for path, src in (('app.js', app), ('reveal-client.js', rc)):
        if 'Object.assign({}, responses' in src:
            bad.append('%s still posts the whole responses object, which is every figure the '
                       'founder typed' % path)

    # ---- the two lists that are one fact in two languages ----
    js_counts = array_literal(fg, 'COUNT_BASES')
    try:
        import match_reference as M                              # noqa: E402
        py_counts = list(M.COUNT_BASES)
        py_bases = set(M.BASIS_FOUNDER_FIELD)
    except Exception as exc:                                     # noqa: BLE001
        py_counts, py_bases = None, None
        bad.append('could not read the engine to compare the basis lists: %s' % exc)
    if js_counts is None:
        bad.append('reveal-figures.js: COUNT_BASES is not a flat array literal')
    elif py_counts is not None and js_counts != py_counts:
        bad.append('COUNT_BASES differs between reveal-figures.js and match_reference.py. The page '
                   'groups the axis on it and the engine opens a basis on it, so they are one '
                   'fact. Page: %s. Engine: %s.' % (js_counts, py_counts))
    if py_bases is not None:
        js_priced = set(array_literal(fg, 'FIGURE_SOURCES') or [])
        # FIGURE_SOURCES is an object, not an array, so read its keys directly.
        js_priced = set(re.findall(r'^  ([A-Z_]+):\s*\{', strip_comments(fg), re.M))
        js_absent = set(re.findall(r'^  ([A-Z_]+):\s', strip_comments(fg), re.M)) - js_priced
        stray = (js_priced | js_absent) - py_bases
        if stray:
            bad.append('reveal-figures.js names %s, which is not a basis the engine knows. A basis '
                       'renamed on one side prices nothing on the other.' % ', '.join(sorted(stray)))
            
        missing = py_bases - (js_priced | js_absent)
        if missing:
            bad.append('reveal-figures.js says nothing about %s, so a founder whose lane uses it '
                       'gets a blank rather than a reason' % ', '.join(sorted(missing)))

    # ---- 9. no browser storage ----
    for path, src in (('reveal-request.js', rq), ('reveal-figures.js', fg),
                      ('reveal-client.js', rc)):
        code = strip_comments(src)
        for token in ('localStorage', 'sessionStorage', 'indexedDB', 'document.cookie'):
            if token in code:
                bad.append('%s: %s appears in code, not in a comment. A figure written to disk '
                           'outlives the promise on the page.' % (path, token))

    # ---- 10. the copy and the code agree ----
    if html.count('We do not receive your revenue figures.') < 2:
        bad.append('index.html: the sentence before the quiz is missing from the hero or from the '
                   'quiz screen. Both need it: a /?hook= link lands a founder on the quiz without '
                   'ever showing them the hero.')
    if 'receives the business figures alone' in html:
        bad.append('index.html: the disclaimer still says the commentary service receives the '
                   'business figures. It receives no figure at all. The disclaimer has to match '
                   'what the code does, not the other way round.')
    if 'Send my figures for the banker review' not in rc:
        bad.append('reveal-client.js: the consent button wording is gone')
    for mount in ('consent-block', 'peer-charts', 'honesty-block'):
        if 'id="%s"' % mount not in html:
            bad.append('index.html: the %s mount is missing, so reveal-client.js draws nothing '
                       'into it' % mount)

    # ---- the server files, read before they are run ----
    m = re.search(r'const\s+answers\s*=\s*\{(.*?)\n  \};', strip_comments(reveal_js), re.S)
    if not m:
        bad.append('api/reveal.js: the answers object could not be found, so this check cannot '
                   'read what the endpoint keeps')
    else:
        for name in FIGURE_NAMES + FREE_TEXT_NAMES:
            if re.search(r'\ba\.' + re.escape(name) + r'\b', m.group(1)):
                bad.append('api/reveal.js keeps a.%s. Nothing that is an amount, or that a founder '
                           'writes prose into, is read by this endpoint.' % name)
    if 'FIGURE_COLUMNS' not in lead_js or 'hasFigureConsent' not in lead_js:
        bad.append('api/lead.js: the consent gate is gone. The page holding its end is half a '
                   'boundary.')
    if 'c.figures === true' not in lead_js:
        bad.append('api/lead.js: consent is not tested with ===. A truthy value is not a decision.')

    # ---- 6, 7, 8 and the behaviour of the builders: run it ----
    engine_rows = []
    try:
        import reveal_payload as RP                              # noqa: E402
        from golden_profiles import PROFILES                     # noqa: E402
        for key, _label, prof in PROFILES:
            for c in RP.build(prof, raise_musd=3.0).get('charts') or []:
                if isinstance(c.get('low'), (int, float)) and isinstance(c.get('high'), (int, float)):
                    engine_rows.append({'fixture': key, 'basis': c['basis'],
                                        'low': c['low'], 'mid': c.get('mid'), 'high': c['high']})
    except Exception as exc:                                     # noqa: BLE001
        bad.append('could not build the engine payloads to test the arithmetic against: %s: %s'
                   % (type(exc).__name__, exc))

    spec_path = None
    if engine_rows:
        fh = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8')
        json.dump({'rows': engine_rows, 'probes': list(ARITHMETIC_PROBES)}, fh)
        fh.close()
        spec_path = fh.name

    probe = None
    try:
        cmd = ['node', PROBE] + ([spec_path] if spec_path else [])
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if out.returncode != 0:
            bad.append('the node probe failed: %s' % (out.stderr or '')[-500:])
        else:
            probe = json.loads(out.stdout)
    except FileNotFoundError:
        bad.append('NODE IS NOT INSTALLED, so seven of the ten assertions above could not run. '
                   'This product already needs node: api/lead.js and api/reveal.js are Node '
                   'functions. Install it and run the suite again rather than trusting the half '
                   'of this check that reads the files without running them.')
    except Exception as exc:                                     # noqa: BLE001
        bad.append('the node probe did not return usable JSON: %s: %s' % (type(exc).__name__, exc))
    finally:
        if spec_path and os.path.exists(spec_path):
            os.unlink(spec_path)

    sent_ok = 0
    if probe:
        sent = probe['sentinels']
        req = probe['requests']

        # 5. the default request body, run rather than read
        extra = [k for k in req['reveal_keys'] if k not in ALLOWED]
        if extra:
            bad.append('the default request body carries %s, which is outside the allowlist'
                       % ', '.join(extra))
        for k, v in sent.items():
            if str(v) in req['reveal_json']:
                bad.append('the sentinel value of "%s" is in the default request body' % k)
            if str(v) in req['lead_json']:
                bad.append('the sentinel value of "%s" is in the lead body' % k)
        lead_extra = [k for k in req['lead_keys'] if k not in ALLOWED and k not in LEAD_EXTRA]
        if lead_extra:
            bad.append('the lead body carries %s, which is neither on the allowlist nor a named '
                       'lead field' % ', '.join(lead_extra))
        # The consent request is the one that MUST carry them, or the button does nothing.
        if 'revenue_exact' not in req['review_keys']:
            bad.append('the consent request carries no figure, so the button sends nothing')
        if '"figures":true' not in req['review_json'].replace(' ', ''):
            bad.append('the consent request carries no consent block, so api/lead.js will refuse it')
        sent_ok = len(sent)

        # 6. the server gate
        L = probe['lead']
        if L['clean']['response'].get('figures_refused'):
            bad.append('the page\'s own lead body contained a figure for the server to refuse')
        if L['clean']['response'].get('figures_stored'):
            bad.append('the server stored figures for a lead body that carried no consent')
        if not L['leaked']['response'].get('figures_refused'):
            bad.append('a body carrying every figure was accepted by api/lead.js with no consent '
                       'block. The server-side half of the boundary is not holding.')
        for k, v in sent.items():
            if str(v) in L['leaked']['log']:
                bad.append('api/lead.js wrote the "%s" figure to its log with no consent' % k)
        if not L['consented']['response'].get('figures_stored'):
            bad.append('the server refused the figures on a request that DID carry consent, so the '
                       'button does not work')

        # 7. what reaches the model
        outbound = ' '.join(c['body'] for c in probe['model']['outbound'])
        for k, v in sent.items():
            if str(v) in outbound:
                bad.append('the "%s" figure reached the model prompt' % k)
        if not probe['model']['outbound']:
            bad.append('the probe intercepted no outbound call, so nothing was checked about what '
                       'reaches the model')

        # 8. the arithmetic
        checked = 0
        if 'arithmetic' in probe and engine_rows:
            want = {}
            for row in engine_rows:
                for v in ARITHMETIC_PROBES:
                    want[(row['basis'], v, row['low'], row['high'])] = (
                        round(v * row['low'], 2), round(v * row['high'], 2))
            seen = 0
            for row, got in zip([(r, v) for r in engine_rows for v in ARITHMETIC_PROBES],
                                probe['arithmetic']):
                r, v = row
                lo, hi = round(v * r['low'], 2), round(v * r['high'], 2)
                if not close(got['low'], lo) or not close(got['high'], hi):
                    bad.append('%s / %s: the browser makes %s times the range %s to %s into %s to '
                               '%s, and the engine makes it %s to %s'
                               % (r['fixture'], r['basis'], v, r['low'], r['high'],
                                  got['low'], got['high'], lo, hi))
                seen += 1
            checked = seen
        notes.append(('ARITHMETIC', '%d multiplications compared against round(v * low, 2), the '
                                    'sum match_reference.py does and check 14 recomputes' % checked))

        # what the page can price today, reported rather than asserted
        f = probe['figures']
        notes.append(('PRICEABLE', '%d of %d bases can be priced from the live quiz: %s'
                      % (len(f['sources']), len(f['sources']) + len(f['not_priced']),
                         ', '.join(f['sources']))))

    # ---- the report ----
    print('THE BOUNDARY: DOES A FOUNDER\'S FIGURE LEAVE THE BROWSER?\n')
    print('ALLOWLIST %d fields may leave on the free path, every one a label or a percentage'
          % len(declared))
    print('          %s' % ', '.join(declared))
    print('REFUSED   %d figure names and %d free-text fields are named as things that never leave '
          'without a click' % (len(FIGURE_NAMES), len(FREE_TEXT_NAMES)))
    if sent_ok:
        print('SENTINELS %d figures given values that appear nowhere else in the repo, then looked '
              'for in every body, every log line and the model prompt' % sent_ok)
    if probe:
        L = probe['lead']['leaked']['response']
        print('SERVER    api/lead.js refused %d figure fields on a body with no consent block, and '
              'stored them on one with it' % L.get('figures_refused', 0))
    for label, text in notes:
        print('%-9s %s' % (label, text))
    print()
    if bad:
        print('FAIL: %d problems.' % len(bad))
        for b in bad[:40]:
            print('   %s' % b)
        if len(bad) > 40:
            print('   ... and %d more' % (len(bad) - 40))
        return 1
    print('PASS: the default request carries the profile and two ratios and no amount, the server')
    print('refuses a figure that arrives without consent, no figure reaches the model, and the')
    print('browser multiplies exactly as the engine would have.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
