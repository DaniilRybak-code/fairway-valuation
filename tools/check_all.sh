#!/bin/sh
# ONE COMMAND. Run this after every data drop and before every commit.
#
# Daniil, 3-Sep-2026: "I will be providing data updates on regular basis, so we need to make sure
# the updated numbers go into the database and start reaching the user as soon as received, without
# creating any conflicts."
#
# The checks are in the order a figure travels, so a failure tells you WHERE it stopped rather than
# only that something is wrong. That ordering is the point: on 3-Sep a whole 509-row refresh sat
# unused for two days while every check below stage 2 passed, because they all begin by reading
# data/ and it had never got there.
#
#   1  intake        did the supplied FILE reach the engine at all
#   2  raw coverage  is every supplied ROW accounted for
#   3  field reach   does every supplied FIGURE reach a row, and is every column read
#   4  cross pull    where one company sits in two files, do they agree
#   5  engine reach  does every row reach the matcher, and does nobody vote twice
#   6  golden        did any founder's answer move
#   7  honesty       is every range caveated
#   8  peer universe can we still narrow the world for 100 companies
#   9  period        does a founder's own revenue convert onto each comparable's basis
#  10  quiz walker   does every fork ask only what peers can answer, and does every answer land
#  11  investor rails no contact details, no incomplete cards, both layers labelled
set -e
cd "$(dirname "$0")/.."
fail=0
run() {
  printf '\n=== %s ===\n' "$1"
  shift
  "$@" || fail=1
}
run "1 INTAKE          did the supplied file reach the engine"        python3 tools/check_intake.py
run "2 RAW COVERAGE    is every supplied row accounted for"           python3 tools/check_raw_coverage.py
run "3 FIELD REACH     does every figure reach a row"                 python3 tools/check_field_reach.py
run "4 CROSS PULL      do two files agree about one company"          python3 tools/check_cross_pull.py
run "5 ENGINE REACH    does every row reach the matcher"              python3 tools/check_engine_reach.py
run "6 GOLDEN          did any founder's answer move"                 python3 selector/golden.py
run "7 HONESTY         is every range caveated"                       python3 tools/honesty_check.py
run "8 PEER UNIVERSE   can we narrow the world"                       python3 tools/peer_universe_check.py
printf '\n'
if [ "$fail" = "1" ]; then
  echo 'ONE OR MORE CHECKS FAILED. The stage that failed is where the data stopped.'
  exit 1
fi
echo 'ALL CHECKS PASSED.'
