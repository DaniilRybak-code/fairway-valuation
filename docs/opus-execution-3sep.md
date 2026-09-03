# Opus list, 3 September 2026: what was executed

Source: `claude/Fairway_roadmap_MERGED_3Sep.md` and `claude/Fairway_tracker.md`, both by Fable.
One item was rescoped by Daniil on the morning of 3 Sep and is marked as such.

---

## 1. March to 100, RESCOPED and now running

Daniil, 3 Sep: "this needs to be done without revenue figures. We just need to make sure that for
100 random names we are able to refine the peer universe. Applying revenue (or ARR or GMV or book
value) number to the respective multiples is more mechanical and hopefully can be tested afterwards."

That removes the blocker the roadmap recorded. The march was waiting on a fixture schema that
carried a revenue figure per company. It no longer needs one.

New tool: `tools/peer_universe_check.py`. It scores each fixture on the comparable set alone. The
bar is not invented; it is four of Daniil's own standing rules turned into assertions.

1. Never price off one comparable. A lane holding exactly one name fails.
2. Three real names beat five padded ones. Fewer than three distinct names fails.
3. Never show an unrelated comparable. If every lane is THIN_OVERLAP, the set rests on a shared
   word and fails.
4. A blank is a trigger, never a conclusion. No peers at all is the loudest failure.

**Result: 43 fixtures, 33 pass, 10 fail.**

The ten: acti, finn, fundraisly, goldfish, honen, levelten, perenna, priori-legal, sellerclaw,
tienda-pago. Nine of the ten fail for the same reason, a lane priced off ONE name.

Three more (moov, payabli, rainforest) pass with an entire lane empty. That is reported as a
warning, not a failure, because no ruling exists on whether an empty lane should fail. It needs one.

### The finding that matters more than the score

`selector/golden.py --peers` compares our output against the human-verified peer lists.

- 255 human-named peers across the 43 fixtures.
- **Only 29 of those 255 exist anywhere in our data. That is 11%.**
- Of the 29 we hold, 14 were surfaced.

The matcher finds roughly half of what it is physically able to find. The other 89% of the human
answer is not in the building. So marching from 43 fixtures to 100 will document the gap in more
places. It will not close it. **The constraint is sourcing, not matching.**

## 2. Engine reach checks, BUILT and wired to fail a build

New tool: `tools/check_engine_reach.py`, the two checks Fable asked for.

- Check 1: every row of `data/private-rounds.csv` reaches the engine, or the check names the ones
  that do not. It imports `selector/match_reference.py` instead of reimplementing the loader, so it
  cannot drift from the thing it checks. This is the check that would have caught the 58 lost rounds
  on the day they were lost rather than two weeks later.
- Check 2: no company votes twice in one median under two keys.

Both were run against a planted fault before being trusted. Both faults found a real bug in the
check. Check 2 used exact token-set equality and let the planted duplicate walk straight through,
because "AG1" and "AG1 (Athletic Greens)" produce unequal token sets. It now buckets on month plus
post-money and groups by token overlap. It then over-fired on the known managed AG1 duplicate, so
only a genuine double vote (more than one copy inside the medians) fails the build.

Clean state: 289 file rows, 289 loaded, one managed duplicate reported as a warning.

## 3. Investor table, sector suffix bug FIXED

`screening_categories` holds `Sector(n); Sector(n)` where n is that house's deal count in the
sector. The splitter kept the suffix, producing one bucket per deal count: "Vertical Software(1)",
"(2)", "(3)". Every coverage number in the table was unreadable and real concentration was hidden.

Fixed. Top sectors now read Agent Ops 11 of 11 target sectors covered, Lending and Credit 11,
Merchant Acquiring and PSP 13.

### The two renderable counts reconciled

Both numbers in circulation are correct. They measure different bars.

- 408 houses in the table, 140 marked CALLABLE.
- **124** clear `investor_check`'s bar.
- **52** clear the roadmap's stricter six-field bar.

What separates them, precisely: **78 callable rows have no `first_cheque_low_m`, 74 have no
`geographies`.** Those two fields are the whole gap. Filling them moves the renderable count from
52 toward 124 without sourcing a single new house.

## 4. Dead code removed

`with_forward_revenue()` deleted from `selector/match_reference.py`. Zero callers since 31 Aug. A
note in its place records what it did and why it went, so the reasoning survives the code. Golden
unmoved at 0 of 43.

## 5. Quiz walker

Not started. The roadmap marked it "if the day allows".

---

## Standing checks, all green after the above

```
check_raw_coverage    PASS   every supplied row accounted for across 3 guarded files
check_engine_reach    PASS   289 rows, 289 loaded, no double vote
golden.py             0 of 43 profiles moved
honesty_check         4 fixtures with no priced range, nothing to caveat
```
