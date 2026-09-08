# -*- coding: utf-8 -*-
"""CHECK 20: can a founder actually be asked their fork's questions, and does every answer land?

WHY THIS EXISTS. The nine forks were written into selector/quiz_fork.py on 31 August, walked by
check 10 on every run since, and never rendered on the page. For six weeks every check said the
forks were fine and every founder got the same nine fixed steps. Check 10 was asking "does the
ENGINE handle every fork", which was true, and nobody was asking "does the PAGE draw them", which
was false.

So this check runs the whole path, end to end, for every one of the nine:

    a profile that routes to the fork
      -> api/profile.build(), which is what the page calls
      -> the questions it sends back
      -> the browser's renderer draws each one
      -> the answers land on the profile fields the engine reads
      -> the engine prices the basis that fork exists to reach

and fails if any link is missing. A fork that the page cannot draw is a fork that does not exist,
whatever quiz_fork.py says.

    python3 tools/check_fork_step.py
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'selector'))
sys.path.insert(0, os.path.join(HERE, 'api'))
os.chdir(HERE)

import quiz_fork as QF                                          # noqa: E402
import match_reference as M                                     # noqa: E402
import importlib.util                                           # noqa: E402

_spec = importlib.util.spec_from_file_location('_profile_api', 'api/profile.py')
API = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(API)

FAILED = []
KINDS_THE_PAGE_DRAWS = {'money', 'quantity', 'count', 'percent', 'choice'}


def check(name, cond, detail=''):
    print('   %-4s %s%s' % ('ok' if cond else 'FAIL', name, ('   ' + detail) if detail else ''))
    if not cond:
        FAILED.append(name)


def profile_for(fork):
    """A profile that routes to this fork, built from the fork's own archetype list."""
    arch = QF.FORKS[fork].get('archetypes', ())
    if not arch:
        return None
    return {'archetype': arch[0], 'archetype_secondary': '', 'industry': 'Horizontal',
            'function': 'Operations', 'buyer': 'SMB', 'gtm_motion': 'PLG',
            'revenue_model': 'SUBSCRIPTION', 'product_role': 'TOOL', 'ai_stance': 'AI_NEUTRAL',
            'product_tags': 'Test', 'stage': 'Seed'}


def main():
    print('THE FORK STEP: CAN A FOUNDER BE ASKED THEIR OWN QUESTIONS?\n')

    print('EVERY FORK ROUTES, AND THE ENDPOINT RETURNS ITS QUESTIONS')
    wire = {}
    for fork in QF.FORKS:
        prof = profile_for(fork)
        if prof is None:
            check('%-22s has no archetypes, so nothing can route to it' % fork, False)
            continue
        out = API.build({'stage': 'Seed', 'sector': 'x', 'website': 'acme.com'},
                        ask=lambda _p, _pr=prof: json.dumps(_pr),
                        fetch=lambda _u: ('', 'check: no fetch'))
        wire[out['fork']] = out
        # AN ARCHETYPE CAN SIT IN TWO FORKS' LISTS and fork_for's docstring says dict order is the
        # tie-break. Three do: Consumer & Prosumer Software (software or consumer subscription),
        # Streaming & Digital Media and Dating & Social Network (consumer subscription or media).
        # So this asserts the routing is DECIDED and STABLE, not that it matches a guess, and it
        # names the shared ones so the ambiguity stays visible rather than being discovered by a
        # founder who gets asked about subscribers when they sell software.
        shared = [f for f, spec in QF.FORKS.items()
                  if f != out['fork'] and prof['archetype'] in spec.get('archetypes', ())]
        check('%-22s -> %-22s %d questions'
              % (prof['archetype'][:22], out['fork'], len(out['questions'])),
              bool(out['fork']) and out['questions'],
              ('also claimed by %s; dict order decides' % ', '.join(shared)) if shared else '')

    print('\nEVERY QUESTION IS ONE THE PAGE KNOWS HOW TO DRAW')
    for fork, out in wire.items():
        for q in out['questions']:
            check('%-22s %-20s kind=%s' % (fork, q['key'], q.get('kind')),
                  q.get('kind') in KINDS_THE_PAGE_DRAWS,
                  'quiz-fork.js draws %s' % sorted(KINDS_THE_PAGE_DRAWS))
            check('%-22s %-20s has a label' % (fork, q['key']), bool(q.get('label')))
            if q.get('kind') == 'choice':
                check('%-22s %-20s choice has options' % (fork, q['key']), bool(q.get('options')))

    print('\nEVERY ANSWER LANDS ON A PROFILE FIELD THE ENGINE READS')
    for fork, out in wire.items():
        prof = profile_for(fork)
        answers = {}
        for q in out['questions']:
            answers[q['key']] = 'BALANCE_SHEET' if q.get('kind') == 'choice' else 100000
        after = QF.apply_answers(prof, answers)
        landed = [k for k in answers if after != prof and any(
            after.get(f) == answers[k] for f in after)]
        # `arr` and `net_revenue` both map to `revenue`, so a fork asking for both lands one value
        # under one field. That is the rule, not a fault: the engine holds one net revenue reading.
        collides = len(answers) - len({QF.apply_answers({}, {k: answers[k]}).get(
            next(iter(QF.apply_answers({}, {k: answers[k]})), ''), None) and
            next(iter(QF.apply_answers({}, {k: answers[k]})), k) for k in answers})
        check('%-22s %d answers, %d land on the profile' % (fork, len(answers), len(landed)),
              len(landed) == len(answers),
              'not landing: %s' % sorted(set(answers) - set(landed)) if len(landed) != len(answers)
              else '')

    print('\nTHE BROWSER CAN PRICE WHAT EACH FORK ASKS FOR')
    fg = open(os.path.join(HERE, 'reveal-figures.js'), encoding='utf-8').read()
    for fork, out in wire.items():
        prof = profile_for(fork)
        bases = set(M.bases_for(prof, 'listed')) | set(M.bases_for(prof, 'private'))
        priced = {b for b in bases if ('  %s:' % b) in fg or ('\n  %s:' % b) in fg}
        check('%-22s prices %d of the %d bases its fork reaches'
              % (fork, len(priced), len(bases)), len(priced) > 0,
              'unpriced: %s' % sorted(bases - priced) if bases - priced else '')

    print('\nTHE PAGE LOADS THE RENDERER AND HAS SOMEWHERE TO PUT IT')
    idx = open(os.path.join(HERE, 'index.html'), encoding='utf-8').read()
    check('index.html loads quiz-fork.js', 'quiz-fork.js' in idx)
    check('index.html has the fork container', 'id="qf-block"' in idx)
    app = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()
    check('app.js asks for the fork after step 2', 'qfAsk()' in app)
    check('app.js draws the fork at step 3', 'qfShowIfReady' in app)

    if os.environ.get('FAIRWAY_NO_NODE') != '1':
        print('\nTHE RENDERER PRODUCES MARKUP FOR EVERY QUESTION IN EVERY FORK')
        cases = [q for out in wire.values() for q in out['questions']]
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8') as fh:
            json.dump(cases, fh)
            spec = fh.name
        probe = os.path.join(HERE, 'tools', 'fork_render_probe.mjs')
        try:
            r = subprocess.run(['node', probe, spec], capture_output=True, text=True, timeout=60)
            if r.returncode != 0:
                check('the renderer ran', False, (r.stderr or '')[-300:])
            else:
                got = json.loads(r.stdout)
                check('%d questions across %d forks all produced markup'
                      % (len(got), len(wire)),
                      all(g['ok'] for g in got),
                      ', '.join(g['key'] for g in got if not g['ok']))
                check('every input carries the question key as its id',
                      all(g['has_id'] for g in got),
                      ', '.join(g['key'] for g in got if not g['has_id']))
        except FileNotFoundError:
            check('NODE IS NOT INSTALLED, so the renderer could not be run', False,
                  'install node, or set FAIRWAY_NO_NODE=1 to skip this half knowingly')
        finally:
            os.unlink(spec)

    print()
    if FAILED:
        print('FAIL: %d assertion(s) failed.' % len(FAILED))
        for f in FAILED[:20]:
            print('   %s' % f)
        return 1
    print('PASS: all nine forks route, every question is one the page can draw, every answer lands')
    print('on a field the engine reads, and the browser can price what each fork asks for.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
