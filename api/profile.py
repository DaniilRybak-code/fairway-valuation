# -*- coding: utf-8 -*-
"""/api/profile - which fork is this founder, and what should we ask them?

THE MISSING HALF OF THE QUIZ. selector/quiz_fork.py has held nine forks since 31 August: the
questions, their labels, which are required, which measure each answer lands on, and the routing
rule that picks a fork from the founder's archetype. Check 10 walks all nine on every run. NONE OF
IT HAS EVER REACHED THE PAGE. index.html asks the same nine fixed steps of everyone and collects
one figure, monthly revenue, so a lender is asked for revenue when the engine prices them on their
book, and the gross-revenue question Daniil ruled on 5 September reaches nobody.

Nothing was lost and nothing needs rebuilding. The specification is in the source, in code, tested.
What was missing is this: something the PAGE can ask "who is this founder, and which questions do
they get". That is all this endpoint does.

THE ORDER OF EVENTS, and it is why this is a separate endpoint rather than part of the reveal:

    step 1   what stage are you at
    step 2   what do you do, and your website
    -------> the page calls THIS, once
    step 3   the fork's own questions, rendered from what comes back
    step 4+  growth, profitability, the raise, the rest

The fork cannot be chosen before step 2, because it is chosen from the founder's ARCHETYPE and the
archetype comes from the profiler, which reads what they do and their website. And it must be
chosen before step 3, because step 3 IS the fork. So the call belongs here, in the middle.

WHAT CROSSES, AND IT IS THE SAME FIFTEEN NAMES AS EVERYWHERE ELSE. Labels and two percentages. No
amount, in either direction: this endpoint returns QUESTIONS, never figures, and the answers to
those questions are amounts, so they stay in the browser exactly like every other figure (rule E9).
tools/check_request_boundary.py holds this endpoint to the same allowlist as the other two.

THE WEBSITE IS FETCHED HERE, for the first time. selector/site_text.py does it: one request, three
seconds, public hosts only, markup stripped. If it fails the profiler still runs on the founder's
words alone and the response says the site could not be read, so the page can tell them rather than
quietly giving a thinner answer.

NO KEY IS HANDLED IN PLAIN TEXT. The model key is read from one environment variable inside
api/payload._ask and nowhere else; this endpoint borrows that function rather than reading it again.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'selector'))
sys.path.insert(0, os.path.join(HERE, 'api'))

import profiler as PR                                          # noqa: E402
import quiz_fork as QF                                         # noqa: E402
import site_text as ST                                         # noqa: E402

MAX_BODY = 64 * 1024

# The same allowlist as api/payload.py and reveal-request.js. Check 15 compares all three.
ALLOWED = ('stage', 'sector', 'sectors', 'sector_detail', 'website', 'company', 'country',
           'revenue_model', 'funding_model', 'volume_unit', 'revenue_basis',
           'growth', 'growth_yoy', 'growth_plan', 'gross_margin')

# WHAT A QUESTION LOOKS LIKE ON THE WIRE. A deliberate subset of the fork spec: everything the page
# needs to draw the question and nothing about how the engine uses the answer. `basis` and
# `peer_field` stay on the server, because they are the engine's business and putting them on the
# page would invite the page to start deciding what an answer means.
QUESTION_FIELDS = ('key', 'label', 'kind', 'required', 'why', 'unit', 'placeholder', 'help')


def question_wire(q):
    out = {}
    for f in QUESTION_FIELDS:
        v = q.get(f)
        if v not in (None, ''):
            out[f] = v
    out['required'] = bool(q.get('required'))
    # THE SPEC CALLS THEM `choices` AND THE PAGE CALLS THEM `options`, and the first version of this
    # endpoint sent neither: the two choice questions in the whole product, the exchange fork's unit
    # and the lending fork's funding model, arrived with no answers to pick from and could not be
    # drawn at all. Check 20 caught it on its first run. The rename happens here, once, rather than
    # either side learning the other's word.
    if q.get('kind') == 'choice':
        out['options'] = list(q.get('choices') or [])
    return out


def filtered(body):
    out = {}
    for k in ALLOWED:
        v = (body or {}).get(k)
        if v in (None, ''):
            continue
        if k == 'sectors' and isinstance(v, list):
            out[k] = [str(x)[:80] for x in v[:3]]
        elif isinstance(v, str):
            out[k] = v[:400]
        elif isinstance(v, (int, float)):
            out[k] = v
    return out


def build(body, ask=None, fetch=None):
    """The whole endpoint minus the HTTP, so a check can drive it without a socket."""
    req = filtered(body)
    text, site_note = (fetch or ST.fetch)(req.get('website') or '')
    try:
        prof = PR.profile_from(req, ask or _ask(), site_text=text)
    except Exception as exc:                                   # noqa: BLE001
        prof = PR.profile_from(req, lambda _p: '')
        site_note = site_note or ('the profiler failed (%s)' % type(exc).__name__)

    fork = QF.fork_for(prof)
    questions = [question_wire(q) for q in QF.FORKS[fork]['questions']]
    # THE AI-NATIVE EXTRA IS PART OF THE FORK AS FAR AS THE PAGE IS CONCERNED. questions_for()
    # already appends it for an AI_NATIVE company, and the page should not have to know that rule.
    extra = [question_wire(q) for q in QF.questions_for(prof)
             if q['key'] not in {x['key'] for x in questions}
             and q['key'] not in {c['key'] for c in QF.CORE}]
    return {
        'fork': fork,
        'questions': questions + extra,
        # What the founder is, in their own reading. Shown back to them so a wrong read is caught
        # by the person best placed to catch it, before they answer four questions on it.
        'read_as': {
            'archetype': prof.get('archetype', ''),
            'industry': prof.get('industry', ''),
            'sells': prof.get('product_tags', ''),
        },
        'site_read': not bool(site_note),
        'site_note': site_note,
        # Named so a bad profile is diagnosable rather than merely disappointing.
        'dropped': prof.get('_dropped', []),
    }


def _ask():
    """Borrowed from api/payload.py so the model key is read in exactly one place."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        '_fairway_payload_api', os.path.join(HERE, 'api', 'payload.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod._ask


try:                                                           # pragma: no cover
    from http.server import BaseHTTPRequestHandler

    class handler(BaseHTTPRequestHandler):                     # noqa: N801  (Vercel's contract)
        def _send(self, code, obj):
            raw = json.dumps(obj).encode('utf-8')
            self.send_response(code)
            self.send_header('content-type', 'application/json')
            self.send_header('content-length', str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self):                                      # noqa: N802
            self._send(405, {'error': 'method_not_allowed'})

        def do_POST(self):                                     # noqa: N802
            try:
                n = int(self.headers.get('content-length') or 0)
            except ValueError:
                n = 0
            if n <= 0 or n > MAX_BODY:
                self._send(413, {'error': 'body_size'})
                return
            try:
                body = json.loads(self.rfile.read(n).decode('utf-8'))
            except Exception:                                  # noqa: BLE001
                self._send(400, {'error': 'bad_json'})
                return
            try:
                self._send(200, build(body))
            except Exception:                                  # noqa: BLE001
                self._send(500, {'error': 'profile_failed'})

        def log_message(self, *_a):
            return
except ImportError:                                            # pragma: no cover
    pass
