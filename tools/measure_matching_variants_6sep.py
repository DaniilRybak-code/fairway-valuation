# -*- coding: utf-8 -*-
"""Measure a proposed matcher change on a SCRATCH copy of the engine, against the golden fixtures.

Fable, 6-Sep-2026. The repo's selector is never edited by this tool. It copies selector/ to a
scratch directory, applies one named text patch to that copy, points the copy at the real data/,
snapshots all 102 profiles exactly as golden.py does, and reports, fixture by fixture, whose peers
changed, what they gained, what they lost, and whether the peer-universe gate verdict moved.

    python3 tools/measure_matching_variants_6sep.py taxonomy
    python3 tools/measure_matching_variants_6sep.py family_primary
    python3 tools/measure_matching_variants_6sep.py family_both
    python3 tools/measure_matching_variants_6sep.py specific_word
    python3 tools/measure_matching_variants_6sep.py family_primary+taxonomy   (patches stack)
    python3 tools/measure_matching_variants_6sep.py none                      (control: must be 0 moved)

Every patch is a literal text replacement and the anchor must match exactly once, so a drifted
engine fails loudly instead of measuring the wrong thing. Count in and count out are printed.
"""
import importlib
import json
import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIX = os.path.join(ROOT, 'selector', 'golden')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
LANES = ('core', 'secondary', 'private')


# ---------------------------------------------------------------------------------------------
# THE PATCHES. Each is (anchor, replacement) pairs applied to selector/match_reference.py text.
# ---------------------------------------------------------------------------------------------

# (2) THE TAXONOMY PROPOSAL, docs/taxonomy-review-5sep.md: for the four catch-all archetypes an
# archetype match counts only when the industry field matches too. Applied everywhere the engine
# tests archetype equality: the score, the tier, the relevance fallback, axis A and axis B.
# _anchored already demands the industry AND the archetype, so it is unchanged.
TAXONOMY = [
    ("def score(p, r, weights=W, use_fin=True):",
     '''CATCH_ALL_ARCHETYPES = {'Vertical Software', 'Data, AI & Developer Tools',
                        'Business Applications', 'Cloud & Infrastructure'}


def _shared_archetypes(p, r):
    """The archetype slots founder and row share, AFTER the catch-all rule: a shared catch-all
    label counts only when the industry field matches too (Horizontal equals Horizontal)."""
    mine = {p.get('archetype'), p.get('archetype_secondary')} - {None, ''}
    theirs = {r.get('archetype'), r.get('archetype_secondary')} - {None, ''}
    shared = mine & theirs
    if shared & CATCH_ALL_ARCHETYPES:
        if (p.get('industry') or '').strip() != (r.get('industry') or '').strip():
            shared = shared - CATCH_ALL_ARCHETYPES
    return shared


def score(p, r, weights=W, use_fin=True):'''),
    ('''    if p['archetype'] and p['archetype'] == ra: s += weights['arch']; why.append('archetype')
    elif p['archetype'] and (p['archetype'] == rb or p.get('archetype_secondary') in (ra, rb) and p.get('archetype_secondary')):
        s += weights['arch_soft']; why.append('archetype~')''',
     '''    _sh = _shared_archetypes(p, r)
    if p['archetype'] and p['archetype'] == ra and ra in _sh: s += weights['arch']; why.append('archetype')
    elif p['archetype'] and _sh:
        s += weights['arch_soft']; why.append('archetype~')'''),
    ('''    mine = {p.get('archetype'), p.get('archetype_secondary')} - {None, ''}
    theirs = {r.get('archetype'), r.get('archetype_secondary')} - {None, ''}
    if mine & theirs:
        return 'ADJACENT'
    return 'BROAD\'''',
     '''    if _shared_archetypes(p, r):
        return 'ADJACENT'
    return 'BROAD\''''),
    ('''    mine = {p.get('archetype'), p.get('archetype_secondary')} - {None, ''}
    theirs = {r.get('archetype'), r.get('archetype_secondary')} - {None, ''}
    return 'ARCHETYPE FALLBACK' if (mine & theirs) else None''',
     '''    return 'ARCHETYPE FALLBACK' if _shared_archetypes(p, r) else None'''),
    ('''    if _ALLOW_ARCHETYPE_FALLBACK:
        mine = {p.get('archetype'), p.get('archetype_secondary')} - {None, ''}
        theirs = {r.get('archetype'), r.get('archetype_secondary')} - {None, ''}
        return bool(mine & theirs)''',
     '''    if _ALLOW_ARCHETYPE_FALLBACK:
        return bool(_shared_archetypes(p, r))'''),
    ('''        a = {r['archetype'], r.get('archetype_secondary') or ''}
        mine = {prof['archetype'], prof.get('archetype_secondary') or ''} - {''}
        return bool(a & mine) or _eq(prof, r, 'function')''',
     '''        return bool(_shared_archetypes(prof, r)) or _eq(prof, r, 'function')'''),
    ('''                    or _eq(prof, r, 'archetype')
                    or _tag_points(why or []) >= FLOOR_TAG_EVIDENCE)''',
     '''                    or (_eq(prof, r, 'archetype') and prof['archetype'] in _shared_archetypes(prof, r))
                    or _tag_points(why or []) >= FLOOR_TAG_EVIDENCE)'''),
]

# (1) THE FAMILY BRIDGE, variant A: the family gate never blocks a row that carries the founder's
# own PRIMARY archetype in either of its slots. Family is learned from archetype by majority vote,
# so an archetype that straddles two families (Commerce Enablement & Fulfilment: consumer;
# Design & Engineering: software) blocks the minority from the founders it was assigned to.
FAMILY_PRIMARY = [
    ('''    out = [r for r in universe
           if family_of(r) == f
           or (bridged and (r.get('industry') or '').strip() == ind)]
    return out or universe''',
     '''    pa = (prof.get('archetype') or '').strip()
    out = [r for r in universe
           if family_of(r) == f
           or (bridged and (r.get('industry') or '').strip() == ind)
           or (pa and pa in (r.get('archetype'), r.get('archetype_secondary')))]
    return out or universe'''),
]

# (1) THE FAMILY BRIDGE, variant B, narrower: the row must carry BOTH of the founder's archetype
# slots (in either order). Same kind of business twice over by our own taxonomy.
FAMILY_BOTH = [
    ('''    out = [r for r in universe
           if family_of(r) == f
           or (bridged and (r.get('industry') or '').strip() == ind)]
    return out or universe''',
     '''    mine = {prof.get('archetype'), prof.get('archetype_secondary')} - {None, ''}
    out = [r for r in universe
           if family_of(r) == f
           or (bridged and (r.get('industry') or '').strip() == ind)
           or (len(mine) == 2 and mine <= ({r.get('archetype'), r.get('archetype_secondary')} - {None, ''}))]
    return out or universe'''),
]

# (1) THE SPECIFIC-WORD GATE: the relevance gate's vocabulary route needs a shared word that the
# token-weight file does NOT call generic (carried by five companies or fewer, weight 1.0), or an
# exact whole tag. Today any shared token counts, so The Zebra reaches a power-purchase marketplace
# and a trading-card platform on the word "marketplace" alone, worth 0.07 points.
SPECIFIC_WORD = [
    ("def relevance_route(p, r, why):",
     '''def _specific_vocabulary(p, r):
    """A shared whole tag, or a shared token the weight file does not call generic."""
    A = [x.strip().lower() for x in (p.get('product_tags') or '').split('|') if x.strip()]
    B = [x.strip().lower() for x in (r.get('product_tags') or '').split('|') if x.strip()]
    if set(A) & set(B):
        return True
    return any(t not in TOKW for t in (toks(p.get('product_tags') or '') & toks(r.get('product_tags') or '')))


def relevance_route(p, r, why):'''),
    ('''    if _tag_points(why) > 0:
        return 'shared product vocabulary'
    pi = (p.get('industry') or '').strip()''',
     '''    if _tag_points(why) > 0 and _specific_vocabulary(p, r):
        return 'shared product vocabulary'
    pi = (p.get('industry') or '').strip()'''),
    ('''def _relevant(p, r, why):
    if _tag_points(why) > 0: return True''',
     '''def _relevant(p, r, why):
    if _tag_points(why) > 0 and _specific_vocabulary(p, r): return True'''),
]

# (1) THE DEEP TOP-UP, private lane: when the lane still cannot price two names after the existing
# top-up, reach for priced names that cleared the RELEVANCE gate and the ABSOLUTE floor but fell
# under the RELATIVE floor (45 per cent of the best score). One excellent comparable should not
# leave a founder priced off one name. Never through the archetype fallback, never below 5.0.
DEEP_TOPUP = [
    ('''    if not ordered: return [], window_months, 'NONE'
    oldest = min(c[1]['date_iso'] for c in ordered)''',
     '''    if sum(1 for z in ordered if _p(z)) < 2 and not _ALLOW_ARCHETYPE_FALLBACK:
        have = {z[1]['transaction_id'] for z in ordered}
        deep = sorted([z for z in pool
                       if z[1]['transaction_id'] not in have and _p(z)
                       and z[0][0] >= FLOOR_ABS and _relevant(prof, z[1], z[0][1])
                       and _tier(prof, z[1], z[0][1]) in PRICING_TIERS],
                      key=lambda z: -z[0][0])
        for z in deep:
            if sum(1 for y in ordered if _p(y)) >= 2:
                break
            r = dict(z[1]); r['topped_up'] = True; r['below_relative_floor'] = True
            ordered.append((z[0], r)); have.add(r['transaction_id'])
    if not ordered: return [], window_months, 'NONE'
    oldest = min(c[1]['date_iso'] for c in ordered)'''),
]

# (2) THE SAME RULE, but the archetype FALLBACK (A12's recorded rescue) keeps matching on the raw
# label. The rescue is already a recorded failure, so one reading of the proposal leaves it alone.
TAXONOMY_FALLBACK_RAW = [pp for pp in TAXONOMY if 'ARCHETYPE FALLBACK' not in pp[0]
                         and '_ALLOW_ARCHETYPE_FALLBACK:' not in pp[0]]

# (3) FIXTURE RE-TAGS, applied to a scratch copy of golden_profiles.py. Marked with the file name.
PROFILE = 'golden_profiles.py'
RETAG_ULTRASONIUM = [(PROFILE,
    '''  dict(archetype='Owned-Inventory Retail', archetype_secondary='Design & Engineering',
   industry='Horizontal', function='Operations', buyer='LOB', gtm_motion='ENT_SALES',
   revenue_model='PRODUCT_SALES', product_role='BRAND', asset_intensity='OWN_PRODUCT', purchase_frequency='EPISODIC',
   ai_stance='AI_NEUTRAL', growth=None, gm=None,
   product_tags='Additive Manufacturing''',
    '''  dict(archetype='Design & Engineering', archetype_secondary='',
   industry='Horizontal', function='Operations', buyer='LOB', gtm_motion='ENT_SALES',
   revenue_model='PRODUCT_SALES', product_role='BRAND', asset_intensity='OWN_PRODUCT', purchase_frequency='EPISODIC',
   ai_stance='AI_NEUTRAL', growth=None, gm=None,
   product_tags='Additive Manufacturing''')]
RETAG_APOLLO = [(PROFILE,
    '''  dict(archetype='Owned-Inventory Retail', archetype_secondary='Design & Engineering',
   industry='Energy & Utilities',''',
    '''  dict(archetype='Design & Engineering', archetype_secondary='',
   industry='Energy & Utilities',''')]

# (3) ROW RE-TAGS, applied at load time in the scratch engine so the data files are untouched.
ROW_RETAG_ANCHOR = "for _r in private:\n    _r['family'] = family_of(_r)"
def row_retag(company, **fields):
    body = ''.join("        _r[%r] = %r\n" % (k, v) for k, v in fields.items())
    return [(ROW_RETAG_ANCHOR,
             "for _r in private:\n    if _r['company_name'] == %r:\n%s" % (company, body)
             + ROW_RETAG_ANCHOR)]
OWNER_NO_SECONDARY = row_retag('Owner', archetype_secondary='')
AUDITBOARD_SWAP = row_retag('AuditBoard', archetype='Business Applications', archetype_secondary='Vertical Software')

# (3) THE STALE WEIGHT FILE: a variant that regenerates data/tag-token-weights.csv into a scratch
# copy of data/ from all seven tag files. Marked with the data flag; no patch text.
WEIGHTS = [('DATA:weights', '', '')]

# (3) FUNCTION WORDS ARE NOT PRODUCT VOCABULARY. Today only and/of/the/for are stopped, so "Quote
# To Cash" and "Buy Now Pay Later" hand out the tokens "to" and "now". Stopping the function words
# changes the tokeniser, so the weight file is regenerated in the same variant.
STOPWORDS = [("STOP = {'and','of','the','for'}",
              "STOP = {'and','of','the','for','to','a','an','as','in','on','at','by','with','from','per','vs','via','or'}"),
             ('DATA:weights', '', '')]

# (1)(3) A WORD IS EVIDENCE ONLY IF IT SEPARATES. The vocabulary route through the relevance gate
# needs a whole tag in common, or a shared word with weight at or above VOCAB_MIN_WEIGHT (weight is
# 5 / companies carrying, so 0.2 means carried by 25 or fewer, 0.5 by 10 or fewer). Score is
# untouched; only the yes/no of the gate changes. Measured on top of fresh weights and stopwords.
INNER_DEF = "VOCAB_MIN_WEIGHT = %s\n\n\ndef _specific_vocabulary(p, r):\n    # A shared whole tag, or a shared word carried by few enough companies to separate.\n    A = {x.strip().lower() for x in (p.get('product_tags') or '').split('|') if x.strip()}\n    B = {x.strip().lower() for x in (r.get('product_tags') or '').split('|') if x.strip()}\n    if A & B:\n        return True\n    shared = toks(p.get('product_tags') or '') & toks(r.get('product_tags') or '')\n    return any(TOKW.get(t, 1.0) >= VOCAB_MIN_WEIGHT for t in shared)\n\n\ndef relevance_route(p, r, why):"


def vocab_gate(min_weight):
    return STOPWORDS + [
        ("def relevance_route(p, r, why):", INNER_DEF % min_weight),
        ("""    if _tag_points(why) > 0:
        return 'shared product vocabulary'
    pi = (p.get('industry') or '').strip()""",
         """    if _tag_points(why) > 0 and _specific_vocabulary(p, r):
        return 'shared product vocabulary'
    pi = (p.get('industry') or '').strip()"""),
        ("""def _relevant(p, r, why):
    if _tag_points(why) > 0: return True""",
         """def _relevant(p, r, why):
    if _tag_points(why) > 0 and _specific_vocabulary(p, r): return True"""),
    ]

# (1) THE TOP-UP ASKS THE RANGE'S OWN QUESTION. Today `_p` tests the founder's lead basis only
# (net revenue, or the raw multiple for a lender), so a lender's lane counts Kriya's 0.6x gross
# revenue as a price and never reaches for a second ARR name, while the ARR range refuses Kriya.
# Here a row "can price" if it prices on ANY reading the lane offers, judged by _basis_row_ok.
LANE_TOPUP = [
    ("""    def _p(z):
        return _f(basis_mult(prof, z[1], _pk)) and z[1].get('in_medians', True)""",
     """    _bases = [b for b in bases_for(prof, 'private') if BASIS_KEYS[b][0]]

    def _p(z):
        r = z[1]
        if not r.get('in_medians', True) or r.get('pre_post') == 'PRE':
            return False
        for b in _bases:
            k = BASIS_KEYS[b][0]
            if r.get(k) and _basis_row_ok(b, r) and _f(basis_mult(prof, r, k, basis=b)):
                return True
        return False"""),
]

RETAG_ULTRASONIUM_INDUSTRY = [(PROFILE,
    """   product_tags='Additive Manufacturing|Metal Fabrication|Industrial Production|Contract Manufacturing|Advanced Materials')),""",
    """   product_tags='Additive Manufacturing|Metal Fabrication|Industrial Production|Contract Manufacturing|Advanced Materials')),""")]
# industry only: same archetype, industry Manufacturing instead of Horizontal
RETAG_ULTRASONIUM_INDUSTRY = [(PROFILE,
    """  dict(archetype='Owned-Inventory Retail', archetype_secondary='Design & Engineering',
   industry='Horizontal', function='Operations', buyer='LOB', gtm_motion='ENT_SALES',
   revenue_model='PRODUCT_SALES', product_role='BRAND', asset_intensity='OWN_PRODUCT', purchase_frequency='EPISODIC',
   ai_stance='AI_NEUTRAL', growth=None, gm=None,
   product_tags='Additive Manufacturing""",
    """  dict(archetype='Owned-Inventory Retail', archetype_secondary='Design & Engineering',
   industry='Manufacturing', function='Operations', buyer='LOB', gtm_motion='ENT_SALES',
   revenue_model='PRODUCT_SALES', product_role='BRAND', asset_intensity='OWN_PRODUCT', purchase_frequency='EPISODIC',
   ai_stance='AI_NEUTRAL', growth=None, gm=None,
   product_tags='Additive Manufacturing""")]
RETAG_ULTRASONIUM_BOTH = [(PROFILE,
    """  dict(archetype='Owned-Inventory Retail', archetype_secondary='Design & Engineering',
   industry='Horizontal', function='Operations', buyer='LOB', gtm_motion='ENT_SALES',
   revenue_model='PRODUCT_SALES', product_role='BRAND', asset_intensity='OWN_PRODUCT', purchase_frequency='EPISODIC',
   ai_stance='AI_NEUTRAL', growth=None, gm=None,
   product_tags='Additive Manufacturing""",
    """  dict(archetype='Design & Engineering', archetype_secondary='',
   industry='Manufacturing', function='Operations', buyer='LOB', gtm_motion='ENT_SALES',
   revenue_model='PRODUCT_SALES', product_role='BRAND', asset_intensity='OWN_PRODUCT', purchase_frequency='EPISODIC',
   ai_stance='AI_NEUTRAL', growth=None, gm=None,
   product_tags='Additive Manufacturing""")]

VARIANTS = {'retag_ultrasonium_industry': RETAG_ULTRASONIUM_INDUSTRY, 'retag_ultrasonium_both': RETAG_ULTRASONIUM_BOTH,
            'lane_topup': LANE_TOPUP, 'vocab25': vocab_gate(0.2), 'vocab10': vocab_gate(0.5), 'vocab50': vocab_gate(0.1),
            'taxonomy': TAXONOMY, 'taxonomy_fallback_raw': TAXONOMY_FALLBACK_RAW,
            'retag_ultrasonium': RETAG_ULTRASONIUM, 'retag_apollo': RETAG_APOLLO,
            'owner_no_secondary': OWNER_NO_SECONDARY, 'auditboard_swap': AUDITBOARD_SWAP,
            'weights': WEIGHTS, 'stopwords': STOPWORDS, 'family_primary': FAMILY_PRIMARY, 'family_both': FAMILY_BOTH,
            'specific_word': SPECIFIC_WORD, 'deep_topup': DEEP_TOPUP, 'none': []}


def patched_source(src, patches):
    for anchor, repl in patches:
        if anchor.startswith('DATA:'):
            continue
        n = src.count(anchor)
        if n != 1:
            raise SystemExit('anchor matched %d times, refusing to measure a drifted engine:\n%s'
                             % (n, anchor[:200]))
        src = src.replace(anchor, repl)
    return src


def build_scratch(patches):
    tmp = tempfile.mkdtemp(prefix='fairway-scratch-')
    shutil.copytree(os.path.join(ROOT, 'selector'), os.path.join(tmp, 'selector'),
                    ignore=shutil.ignore_patterns('golden', '__pycache__'))
    # Three kinds of patch: engine text (2-tuples), a named file in selector/ (3-tuples), and a
    # data regeneration (anchor 'DATA:weights'), which copies data/ rather than linking it.
    engine = [pp for pp in patches if len(pp) == 2 and not pp[0].startswith('DATA:')]
    files = [pp for pp in patches if len(pp) == 3 and not pp[0].startswith('DATA:')]
    data_flags = {pp[0] for pp in patches if pp[0].startswith('DATA:')}
    if data_flags:
        shutil.copytree(os.path.join(ROOT, 'data'), os.path.join(tmp, 'data'),
                        ignore=shutil.ignore_patterns('raw'))
    else:
        os.symlink(os.path.join(ROOT, 'data'), os.path.join(tmp, 'data'))
    p = os.path.join(tmp, 'selector', 'match_reference.py')
    src = open(p, encoding='utf-8').read()
    open(p, 'w', encoding='utf-8').write(patched_source(src, engine))
    for fname, anchor, repl in files:
        fp = os.path.join(tmp, 'selector', fname)
        fsrc = open(fp, encoding='utf-8').read()
        open(fp, 'w', encoding='utf-8').write(patched_source(fsrc, [(anchor, repl)]))
    if 'DATA:weights' in data_flags:
        # Regenerate with the SCRATCH tokeniser's stopword list, read off the patched engine.
        import regenerate_token_weights_6sep as RW
        import re as _re
        m = _re.search(r"STOP = (\{[^}]*\})", open(p, encoding='utf-8').read())
        RW.STOP = eval(m.group(1))
        rows, rows_in, nfiles = RW.compute(tmp)
        import csv as _csv, io as _io
        buf = _io.StringIO(); w = _csv.writer(buf, lineterminator='\n')
        w.writerow(['token', 'companies_carrying', 'distinct_tags_containing', 'weight_factor'])
        for r in rows: w.writerow(r)
        open(os.path.join(tmp, 'data', 'tag-token-weights.csv'), 'w', encoding='utf-8').write(RW.HDR + buf.getvalue())
        print('weights regenerated in scratch: %d tag rows in, %d generic tokens out, stopwords %s'
              % (rows_in, len(rows), sorted(RW.STOP)))
    return tmp


def names(e, lane):
    return [x['company'] for x in (e.get(lane) or [])]


def main():
    spec = sys.argv[1] if len(sys.argv) > 1 else 'none'
    patches = []
    for part in spec.split('+'):
        if part not in VARIANTS:
            raise SystemExit('unknown variant %s; choose from %s' % (part, sorted(VARIANTS)))
        patches += VARIANTS[part]
    tmp = build_scratch(patches)
    sys.path.insert(0, os.path.join(tmp, 'selector'))
    golden = importlib.import_module('golden')
    assert golden.M.__file__.startswith(tmp), golden.M.__file__
    puc = importlib.import_module('peer_universe_check')

    if '--weak-words' in sys.argv:
        # NAMES ADMITTED ON WORDS ALONE. For every fixture and lane, the members whose only route
        # through the relevance gate is shared vocabulary, with no whole tag in common and every
        # shared word carried by 25 or more companies (weight 0.2 or less). Descriptive, so Daniil
        # can see what "any shared token at all" admits before ruling on it.
        M = golden.M
        weak, total = [], 0
        for key, label, prof in golden.PROFILES:
            core, sec, _t = M.peer_groups(prof, M.listed)
            picked, _m, _t2 = M.select_private(prof, M.private)
            for lane, grp in (('core', core), ('private', picked)):
                for (sc, why), r in grp:
                    total += 1
                    if M.relevance_route(prof, r, why) != 'shared product vocabulary':
                        continue
                    A = {x.strip().lower() for x in (prof.get('product_tags') or '').split('|') if x.strip()}
                    B = {x.strip().lower() for x in (r.get('product_tags') or '').split('|') if x.strip()}
                    if A & B:
                        continue
                    shared = M.toks(prof.get('product_tags') or '') & M.toks(r.get('product_tags') or '')
                    wmax = max(M.TOKW.get(t, 1.0) for t in shared) if shared else 0
                    if wmax <= 0.2:
                        weak.append((key, lane, r['company_name'], round(sc, 1),
                                     ' '.join('%s(%.2f)' % (t, M.TOKW.get(t, 1.0)) for t in sorted(shared))))
        print('VARIANT %s: %d of %d core+private members are admitted on generic words alone' % (spec, len(weak), total))
        for row in weak:
            print('   %-18s %-8s %-26s %5s  %s' % row)
        shutil.rmtree(tmp)
        return 0
    if '--peers' in sys.argv:
        # THE HUMAN-VERIFIED PEER SETS, the instrument built on 2-Sep for judging matcher changes.
        print('VARIANT %s, scored against the frozen human peer sets:' % spec)
        golden.peer_coverage()
        shutil.rmtree(tmp)
        return 0
    files = sorted(f[:-5] for f in os.listdir(FIX) if f.endswith('.json'))
    print('VARIANT %s   scratch engine at %s' % (spec, tmp))
    print('%d fixtures in' % len(files))
    changed, gained, lost, verdict_moved = [], [], [], []
    before_pass = after_pass = 0
    seen = 0
    for key, label, prof in golden.PROFILES:
        want = json.load(open(os.path.join(FIX, key + '.json')))['expected']
        got = golden.snap(prof)
        seen += 1
        vb, fb, _fc, _w = puc.score(want)
        va, fa, _fc2, _w2 = puc.score(got)
        before_pass += vb == 'PASS'
        after_pass += va == 'PASS'
        diffs = []
        g = l = False
        for lane in LANES:
            a, b = names(want, lane), names(got, lane)
            if a != b:
                add = [x for x in b if x not in a]
                rem = [x for x in a if x not in b]
                g = g or bool(add)
                l = l or bool(rem)
                diffs.append('%s +%s -%s' % (lane, add or '', rem or ''))
            na, nb = puc.best_n(want, lane), puc.best_n(got, lane)
            if na != nb:
                diffs.append('%s priced %s->%s' % (lane, na, nb))
        if diffs:
            changed.append(key)
            if g: gained.append(key)
            if l: lost.append(key)
            print('  %-18s %s -> %s  %s' % (key, vb, va, ' | '.join(diffs)))
        if vb != va:
            verdict_moved.append((key, vb, va, '; '.join(fa)))
    print('\n%d fixtures in, %d snapshotted, 0 dropped' % (len(files), seen))
    print('CHANGED PEERS %d of %d: %s' % (len(changed), seen, ', '.join(changed) or 'none'))
    print('GAIN a name   %d: %s' % (len(gained), ', '.join(gained) or 'none'))
    print('LOSE a name   %d: %s' % (len(lost), ', '.join(lost) or 'none'))
    print('GATE %d of %d before -> %d of %d after' % (before_pass, seen, after_pass, seen))
    for k, vb, va, why in verdict_moved:
        print('   %-18s %s -> %s  %s' % (k, vb, va, why))
    # THE NO-COMPS LIST under the variant, so a rescue that starts or stops firing is visible.
    print('archetype fallback fired for %d lane(s) under this variant: %s'
          % (len({(l, s) for l, s, _n, _a in golden.M.archetype_fallbacks}),
             sorted({(l, s[:30]) for l, s, _n, _a in golden.M.archetype_fallbacks})))
    shutil.rmtree(tmp)
    return 0


if __name__ == '__main__':
    sys.exit(main())
