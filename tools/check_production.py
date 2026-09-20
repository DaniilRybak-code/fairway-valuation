#!/usr/bin/env python3
"""Check 21: is the engine alive on the LIVE site.

Every other check in tools/check_all.sh runs in a clone. On 20 September 2026 all twenty of them were
green while /api/payload and /api/profile had answered 404 on production since the day they were
written (7 September), so every founder's field printed "in build" on its engine rows. A suite that
never touches the deployment cannot see that. This check does, and nothing else.

What it does, in order:
  1. GET  /api/health   and requires ANTHROPIC_API_KEY to be present (a boolean; the value is never
                        sent, printed or read by anything).
  2. POST /api/profile  with a fixture body and requires a fork and its questions back.
  3. POST /api/payload  with the same body and requires at least one lane with a priced range, and
                        the profiler's note to be empty (a note means it fell back to nothing).

The body carries labels and two percentages and no amount, exactly the shape reveal-request.js
sends (rule E9). It is the same allowlist api/payload.py filters against.

Which site: FAIRWAY_URL if set, else production. Skipping is explicit and printed:
    FAIRWAY_SKIP_PRODUCTION=1 python3 tools/check_production.py
A skip is for a machine with no network. It is not for a red result.

Exit 0 on pass, 1 on any failure, with the failing step named.
"""
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_URL = 'https://fairway-coverage-kit.vercel.app'
BODY = {
    'stage': 'Series A',
    'sector': 'HR tech / Future of work',
    'sectors': ['HR tech / Future of work'],
    'sector_detail': 'HR software: onboarding, people management and performance reviews for SMBs',
    'company': 'Fairway smoke test',
    'website': '',
    'growth_yoy': 70,
    'growth_plan': 145,
}


def call(base, path, body=None, timeout=75):
    url = base.rstrip('/') + path
    data = None if body is None else json.dumps(body).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST' if data else 'GET',
                                 headers={'content-type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode('utf-8'))
        except Exception:                                      # noqa: BLE001
            return e.code, None
    except Exception as e:                                     # noqa: BLE001
        return None, {'error': type(e).__name__}


def main():
    if os.environ.get('FAIRWAY_SKIP_PRODUCTION') == '1':
        print('CHECK 21 SKIPPED: FAIRWAY_SKIP_PRODUCTION=1. The live site was NOT checked.')
        return 0
    base = os.environ.get('FAIRWAY_URL', DEFAULT_URL)
    print('checking', base)
    bad = 0

    code, h = call(base, '/api/health')
    if code != 200 or not isinstance(h, dict):
        print('FAIL health: HTTP', code)
        return 1
    print('health: commit', (h.get('commit') or '')[:7], 'branch', h.get('branch'))
    key = (h.get('env_present') or {}).get('ANTHROPIC_API_KEY')
    if key is not True:
        print('FAIL health: ANTHROPIC_API_KEY is not set on this deployment, so the profiler '
              'cannot run and every engine row will print "in build".')
        bad = 1
    else:
        print('ok    health: model key present')

    code, p = call(base, '/api/profile', BODY)
    if code == 404:
        print('FAIL profile: 404. The Python function is not deployed at all.')
        bad = 1
    elif code != 200 or not isinstance(p, dict) or not p.get('fork'):
        print('FAIL profile: HTTP', code, 'body', str(p)[:200])
        bad = 1
    else:
        print('ok    profile: fork', p.get('fork'), 'with', len(p.get('questions') or []), 'questions')
        if p.get('profiler_error'):
            print('FAIL profile: the profiler reported', repr(p.get('profiler_error')))
            bad = 1
        elif not (p.get('read_as') or {}).get('archetype'):
            print('FAIL profile: no archetype came back; dropped', p.get('dropped'))
            bad = 1
        else:
            print('ok    profile: read as', (p.get('read_as') or {}).get('archetype'))

    code, out = call(base, '/api/payload', BODY)
    if code == 404:
        print('FAIL payload: 404. The Python function is not deployed at all.')
        bad = 1
    elif code != 200 or not isinstance(out, dict) or not out.get('payload'):
        print('FAIL payload: HTTP', code, 'body', str(out)[:200])
        bad = 1
    else:
        prof = out.get('profiler') or {}
        ranges = (out['payload'].get('ranges') or {})
        priced = [(lane, basis) for lane, bases in ranges.items() for basis, r in bases.items()
                  if isinstance(r, dict) and r.get('n')]
        if prof.get('note'):
            print('FAIL payload: profiler note', repr(prof.get('note')))
            print('      dropped by the vocabulary:', prof.get('dropped'))
            bad = 1
        if not priced:
            print('FAIL payload: no lane came back with comparables; the field would print "in build"')
            bad = 1
        if not bad:
            print('ok    payload: archetype', prof.get('archetype'), 'lanes', priced)

    print('CHECK 21', 'FAILED' if bad else 'PASSED')
    return bad


if __name__ == '__main__':
    sys.exit(main())
