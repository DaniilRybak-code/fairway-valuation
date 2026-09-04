#!/bin/sh
# IS ANYTHING OF YOURS ONLY ON THIS LAPTOP.
#
# Daniil, 4-Sep-2026: "WHY only Fable discovers that something had not been committed?"
#
# Because nothing was looking. Twelve checks read the data and the engine and none of them read the
# repository, so "committed and ready to push" could sit in a handover for a day and every check
# would stay green. The two agents that write the code cannot look either: neither of them may run
# git on this machine, by your own standing rule, after a read-only call through the bridge left an
# index.lock you could not clear. So the only way it was ever found was a person reading a file list
# and noticing.
#
# This is the loop closed, and it runs where git is meant to run: in your own shell, not through the
# bridge. It REPORTS and never fails, because a dirty tree in the middle of an afternoon is normal
# and a check that cries wolf gets ignored. What is not normal is a dirty tree at the end of a day,
# or a laptop three commits behind origin while a handover says the push is done.
#
#   sh tools/check_pushed.sh
set +e
cd "$(dirname "$0")/.." || exit 0

if [ "$FAIRWAY_NO_GIT" = "1" ]; then
  echo 'SKIPPED   FAIRWAY_NO_GIT=1. This check runs git, and D10 says no git runs on the laptop'
  echo '          through the bridge. Run it yourself in your own terminal.'
  exit 0
fi
if [ ! -d .git ]; then echo 'not a git working tree, nothing to report'; exit 0; fi
if [ -f .git/index.lock ]; then
  echo "LOCK      .git/index.lock exists ($(ls -l .git/index.lock 2>/dev/null | awk '{print $6, $7, $8}'))."
  echo "          Git will refuse to commit until it is deleted: rm .git/index.lock"
fi

BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
HEAD_SHA=$(git rev-parse --short HEAD 2>/dev/null)
echo "BRANCH    $BRANCH at $HEAD_SHA"

DIRTY=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
if [ "$DIRTY" != "0" ]; then
  echo "LOCAL     $DIRTY file(s) exist only on this laptop:"
  git status --porcelain 2>/dev/null | head -20 | sed 's/^/          /'
  if [ "$DIRTY" -gt 20 ]; then echo "          ... and $((DIRTY - 20)) more"; fi
else
  echo 'LOCAL     working tree clean'
fi

# WITHOUT A FETCH THIS ANSWERS FROM A STALE REMOTE REF, which is exactly how a laptop ends up
# pushing onto a branch that moved under it. Quiet, and ignored when there is no network.
git fetch --quiet 2>/dev/null
UP=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null)
if [ -n "$UP" ]; then
  AHEAD=$(git rev-list --count "$UP"..HEAD 2>/dev/null)
  BEHIND=$(git rev-list --count HEAD.."$UP" 2>/dev/null)
  echo "ORIGIN    $UP: $AHEAD commit(s) ahead, $BEHIND behind"
  if [ "$BEHIND" != "0" ] && [ -n "$BEHIND" ]; then
    echo '          A plain git push will be REJECTED. Commit first, then git pull --rebase, then push.'
  fi
  if [ "$AHEAD" != "0" ] && [ -n "$AHEAD" ]; then
    echo '          Commits exist here that nobody else can see. Push them or say so in the handover.'
  fi
else
  echo 'ORIGIN    this branch tracks nothing, so nothing can be said about what is pushed'
fi
exit 0
