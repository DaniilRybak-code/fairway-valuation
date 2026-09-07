# -*- coding: utf-8 -*-
"""/api/payload - the engine payload, served.

This is the endpoint api/reveal.js has been apologising for since 6 September. Its comment says
"selector/reveal_payload.py builds the whole reveal in one pass and it is Python; this endpoint is
a Node function", and answers `payload: null` with that as the reason. The answer is not to port
the engine to JavaScript. It is a second function, in Python, next to the first one: Vercel runs
both runtimes in the same project, and the engine stays the single source of every number.

WHAT IT DOES, in order:
  1. Refuses anything that is not a POST, and anything oversized, before reading a body.
  2. Filters the body against ALLOWED, which is the SAME allowlist reveal-request.js builds from.
     The page already sends only these. The server refuses the rest anyway, because a promise
     enforced at one end is a promise enforced nowhere: that is exactly the lesson of the two doors
     found on 6 September, where /api/lead was storing every figure while /api/reveal was clean.
  3. Builds a profile through selector/profiler.py, which is where the one model call lives and
     which can only emit values the tag files already carry.
  4. Calls selector/reveal_payload.build() and returns it.

THE TIER IS THE SERVER'S TO DECIDE AND THE CLIENT MAY NOT CLAIM IT. Rule E8: the free and paid
tiers are two different payload objects, and the private figures are simply absent from the free
one. If the browser could ask for tier='paid' then the lock would be a suggestion. So the tier is
'free' unless the request carries an entitlement the server can verify, and today nothing can
verify one, so it is always 'free'. Wiring the paid tier to whatever proves payment is a named
to-do and it is deliberately not a client field.

NO KEY IS HANDLED IN PLAIN TEXT ANYWHERE IN THIS FILE. The model key is read from one environment
variable at the moment of the call and is never assigned to a profile field, never written to a
file, never put in a response and never printed. There is no log line in this handler that takes a
variable at all. If the variable is missing the endpoint returns a payload built with an empty
profile and says so in `profiler` rather than failing silently or, worse, carrying on with a key
from somewhere else.

WHAT NEVER ARRIVES HERE. No revenue, no ARR, no raise, no profit, no user count, no free text. The
founder's figures stay in their browser and are multiplied there (rule E9, reveal-figures.js), and
tools/check_request_boundary.py asserts it against this endpoint as well as the other two.
"""
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                'selector'))

import profiler as PR                                          # noqa: E402
import reveal_payload as RP                                    # noqa: E402

# THE ALLOWLIST, and it is the same list as reveal-request.js. If the two ever disagree, check 15
# fails: it reads both and compares them name by name.
ALLOWED = (
    # company data
    'stage', 'sector', 'sectors', 'sector_detail', 'website', 'company', 'country',
    'revenue_model',
    # fork labels: which measure, which unit, how the book is funded. Words, never amounts.
    'funding_model', 'volume_unit', 'revenue_basis',
    # the two ratios plus growth in the three shapes the quiz collects it in
    'growth', 'growth_yoy', 'growth_plan', 'gross_margin',
)
MAX_BODY = 64 * 1024
MODEL_URL = 'https://api.anthropic.com/v1/messages'


def _ask(prompt):
    """One model call. The key is read here and nowhere else, and does not leave this function."""
    key = os.environ.get('ANTHROPIC_API_KEY')
    if not key:
        raise RuntimeError('no_model_key')
    body = json.dumps({
        'model': os.environ.get('ANTHROPIC_MODEL', 'claude-sonnet-4-5'),
        'max_tokens': 1200,
        'messages': [{'role': 'user', 'content': prompt}],
    }).encode('utf-8')
    req = urllib.request.Request(MODEL_URL, data=body, method='POST', headers={
        'content-type': 'application/json',
        'anthropic-version': '2023-06-01',
        'x-api-key': key,
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        out = json.loads(r.read().decode('utf-8'))
    return ''.join(b.get('text', '') for b in out.get('content', []))


def filtered(body):
    """Only the allowlisted names, and only scalars. A dict or a list here would be a place to hide
    a figure, and `sectors` is the one list the page sends, so it is allowed as a list of strings."""
    out = {}
    for k in ALLOWED:
        v = (body or {}).get(k)
        if v in (None, ''):
            continue
        if k == 'sectors' and isinstance(v, list):
            out[k] = [str(x)[:80] for x in v[:3]]
        elif isinstance(v, (str, int, float)):
            out[k] = v if isinstance(v, str) is False else v[:400]
    return out


def build(body, ask=None, site_text=''):
    """The whole endpoint minus the HTTP, so a check can drive it without a socket."""
    req = filtered(body)
    note = ''
    try:
        prof = PR.profile_from(req, ask or _ask, site_text=site_text)
    except Exception as exc:                                   # noqa: BLE001
        prof = PR.profile_from(req, lambda _p: '')
        note = type(exc).__name__
    if not prof.get('archetype'):
        note = note or 'no_archetype: the profiler returned nothing the vocabulary recognises'
    # TIER IS NOT A CLIENT FIELD. See the header.
    payload = RP.build(prof, raise_musd=None, tier='free')
    return {
        'payload': payload,
        'profiler': {
            'archetype': prof.get('archetype', ''),
            'product_tags': prof.get('product_tags', ''),
            'dropped': prof.get('_dropped', []),
            'note': note,
        },
    }


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
                # No variable is interpolated into anything that leaves this handler.
                self._send(500, {'error': 'payload_failed'})

        def log_message(self, *_a):
            """Silence the default access log. It prints the request line, and a request line is
            the one place a query string could carry something we promised not to keep."""
            return
except ImportError:                                            # pragma: no cover
    pass
