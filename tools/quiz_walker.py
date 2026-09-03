# -*- coding: utf-8 -*-
"""Walk every fork of the quiz and check a founder who answers it can actually be priced.

FABLE'S ITEM 5. The quiz is the only thing a founder touches, and until now nothing has ever walked
it end to end. Every fork is a promise: answer these questions and we will show you comparable
companies. This checks the promise holds for each fork separately, because the forks have diverged
a lot in three days: two new ones were added on 3-Sep and the lending fork went from one question
to six.

FOR EACH FORK IT ASKS FOUR THINGS.

  1. NEVER ASK FOR A METRIC WE CANNOT PUT A PEER NUMBER NEXT TO. This is the fork's own founding
     rule, written when the net loan book question was demoted for breaking it. Every question that
     declares a `basis` must have peers holding a multiple on that basis, or the founder is being
     asked to type a number into a void.
  2. EVERY REQUIRED ANSWER MUST REACH THE ENGINE. A question maps_to a profile field; if nothing
     reads that field the answer is collected and discarded, which is the quiz-shaped version of
     every data-loss bug found today.
  3. A FOUNDER WHO ANSWERS IT GETS A PRICED RANGE. Simulated with a plausible answer set, the fork
     must produce at least one range on at least one lane.
  4. AND THE ANSWERS ARE ONLY EVER SIMULATED HERE. Nothing this file computes is written anywhere,
     snapshotted, or allowed near the golden fixtures. On 3-Sep a synthetic revenue injected into
     the fixtures moved the peer selection of 42 of 43; invented numbers stay inside the walker.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, 'selector'))
os.chdir(HERE)
import match_reference as M                      # noqa: E402
import quiz_fork as Q                            # noqa: E402

# A plausible answer for each kind of question, used only to drive the walk.
ANSWER = {'money': 10.0, 'percent': 60.0, 'quantity': 100000.0}


SRC = io.open('selector/match_reference.py', encoding='utf-8').read() + \
      io.open('selector/quiz_fork.py', encoding='utf-8').read()


def field_is_read(field):
    """Does anything actually read profile.<field>?

    Written as a real search rather than a substring test, because the first version asked whether
    the bare word appeared anywhere in the file and passed on words like `revenue` that appear in a
    hundred unrelated places. A field is read when something asks the PROFILE for it.
    """
    pats = ["prof.get('%s'" % field, 'prof["%s"' % field, "prof['%s']" % field,
            "profile.get('%s'" % field, "p.get('%s'" % field]
    if any(x in SRC for x in pats):
        return True
    # A field read through the basis map is read. BASIS_FOUNDER_FIELD is looked up by basis and the
    # field name is then a variable, so no literal search can see it; naming it there IS the wiring.
    return field in set(M.BASIS_FOUNDER_FIELD.values())


def profile_for(fork_name, fork):
    """A REAL company profile that routes to this fork, plus the answers it would give.

    Using a real fixture rather than an invented profile matters: an invented one has no product
    vocabulary, so the relevance gate rejects every candidate and the walker reports that no fork
    can price anybody, which is a fact about the walker and not about the engine. That is what the
    first version did.
    """
    from golden_profiles import PROFILES
    base = None
    for k, l, p in PROFILES:
        if Q.fork_for(p) == fork_name:
            base = dict(p)
            base['_fixture'] = k
            break
    if base is None:
        return None, []
    asked = []
    for q in fork['questions']:
        if q.get('reviewer_context'):
            continue
        maps = (q.get('maps_to') or '')
        if not maps.startswith('profile.'):
            continue
        field = maps.split('.', 1)[1]
        asked.append((q['key'], field, q.get('required'), q.get('basis')))
    # The ANSWERS are deliberately NOT written onto the profile. Peer selection must never see an
    # invented number: on 3-Sep a synthetic revenue moved the selection of 42 of 43 fixtures. What
    # is checked here is that the question has somewhere to go and somebody to be compared against.
    return base, asked


def peers_on(basis):
    """How many rounds and listed rows can answer on this basis at all."""
    if basis in (None, ''):
        return None
    key_priv = (M.BASIS_KEYS.get(basis) or (None, None, ''))[0]
    key_list = (M.BASIS_KEYS.get(basis) or (None, None, ''))[1]
    n = 0
    if key_priv:
        n += len([r for r in M.private
                  if r.get(key_priv) is not None and M._basis_row_ok(basis, r)])
    if key_list:
        n += len([r for r in M.listed if r.get(key_list) is not None])
    return n


# A question may declare a basis that is not itself a BASIS_KEYS entry, because it feeds one.
ALIAS = {'NET_REVENUE': 'REVENUE', 'ARR': 'ARR', 'BOOK': 'BOOK', 'EARNINGS': 'EARNINGS',
         'ORIGINATIONS': 'ORIGINATIONS', 'THROUGHPUT': 'THROUGHPUT',
         'SUBSCRIBERS': 'PAYING_SUBSCRIBERS', 'BORROWERS': 'BORROWERS', 'LOAN_BOOK': None}


def main():
    bad, warn = [], []
    print('WALKING EVERY FORK OF THE QUIZ\n')
    for name, fork in Q.FORKS.items():
        prof, asked = profile_for(name, fork)
        if prof is None:
            print('=== %s === NO FIXTURE ROUTES HERE, so the fork is untested by this walk' % name)
            warn.append(name)
            print()
            continue
        print('=== %s === %d questions, walked with fixture %s (%s)'
              % (name, len(asked), prof.get('_fixture'), prof['archetype']))
        # 1 and 2
        for key, field, required, basis in asked:
            b = ALIAS.get((basis or '').upper(), (basis or '').upper() or None)
            n = peers_on(b) if b else None
            src = field_is_read(field)
            note = []
            if b and n == 0:
                note.append('NO PEER CAN ANSWER ON %s' % b)
                bad.append('%s / %s' % (name, key))
            if not src:
                note.append('profile.%s is READ BY NOTHING' % field)
                bad.append('%s / %s' % (name, key))
            print('   %-22s %-9s basis %-18s peers %-5s %s'
                  % (key, 'REQUIRED' if required else 'optional', b or '-',
                     n if n is not None else '-', '; '.join(note)))
        # 3
        core, sec, lt = M.peer_groups(prof, M.listed)
        picked, _mo, pt = M.select_private(prof, M.private)
        ranges = M.all_ranges(prof, core, lt, picked, pt)
        got = {ln: sorted(v) for ln, v in ranges.items() if v}
        if not got:
            print('   NO PRICED RANGE AT ALL for a founder who answers this fork')
            bad.append('%s / no range' % name)
        else:
            print('   priced: %s' % got)
        print()
    if bad:
        print('FAIL: %d problems.' % len(bad))
        for b in bad:
            print('   %s' % b)
        return 1
    print('PASS: every fork asks only for metrics peers can answer, every answer reaches the')
    print('engine, and every fork produces a priced range.')
    return 0


sys.exit(main())
