# Why those bugs survived, and the check that would have caught them

3 September 2026. Written because Daniil asked, after finding three real defects in one sitting
that our checks had been passing over for days.

## The bugs

| what | how long | how it was found |
|---|---|---|
| twelve neobanks lost their price-to-book and price-earnings entirely | since peers-lending.csv arrived, 30 Aug | Daniil: "NU for sure carried price to book value" |
| sixteen volume multiples reached nothing, including every EV/originations one | since the volume columns arrived, 30 Aug | chasing the first one |
| all 123 logistics and services companies arrived with no growth at all | since that file arrived | the new check, same evening |
| Marqeta priced payfacs as an acquiring comparable | since the vocabulary was written | Daniil: "Marqeta is not an acquirer" |
| a valuation over 121.5 megatonnes of CO2 produced a tidy 11.52x | since the volume fix, one hour | the new check |

**Not one was found by a check. Every one was found by a person looking at an output and saying
that cannot be right.** That is the finding, and it is worse than any individual bug.

## Why the checks were blind

They were not weak. They were measuring the wrong unit.

| check | what it asks | why it passed |
|---|---|---|
| `check_raw_coverage` | is every supplied ROW accounted for | a row with a blank field is still an accounted-for row |
| `check_engine_reach` | does every ROW reach the engine | same |
| `golden.py` | did the output MOVE | **a field that was always empty never moves.** Golden is a regression snapshot, so a defect present when the baseline was written is invisible to it forever, by construction |
| `honesty_check` | is the output caveated | a missing multiple produces fewer names, not a wrong caveat |

Rule D8 already says the right thing: a figure in the file but not in the engine is ABSENT, not
pending. **Nothing enforced D8 below the row.**

## The shape they share

Three things, and they compound.

**1. They lose a FIELD while the ROW arrives intact.** Every check we had counts rows.

**2. They live at silent choice points.** `if k in listed: continue`. `_f(r.get('ev_gmv_x'))`. A
default argument of `'mult'`. A cap of five. Each is one line where the code picks between two
things and the loser leaves no trace at all: no log, no count, no exception.

**3. Every one was correct for the file it was written against, and became wrong when a SECOND file
arrived with a different shape.** The ticker-skip was right while there was one peers file per
company. `ev_gmv_x` was right while there was one private file. The five peers pulls now spell the
same measures five different ways: `revenue_ntm_musd` against `revenue_fy0_musd`,
`equity_to_av_bridge_musd` against `eqv_ev_bridge_musd`, `ev_gmv_x` against `ev_volume_x`,
`revenue_growth_ntm_pct` against `revenue_growth_pct`. Each new pull is a fresh chance for the same
bug, and there will be more pulls.

That is the honest root cause. It is not carelessness in any one line. It is that **the loader is
the one place in the system where data can disappear without anything counting it, and it was the
one place with no check.**

## The check that closes it

`tools/check_field_reach.py`, with two halves, because one half is not enough and I only learned
that by planting a fault and watching the first half pass.

**Half one, the value test.** For every numeric column of every source file, take the rows that
have a value and ask whether that value reaches the loaded row. Catches a field lost because the
whole row was dropped. It caught the neobank bug when I planted it back: it named `p_bv_x`,
`p_e_x`, and Nu Holdings, SoFi, Klarna, Chime and Inter & Co by name.

**Half two, the static test.** Does any line of the loader MENTION this column name? Half one
cannot catch a column the loader never reads, because both loaders build their row as
`{**raw, **tags}`, so the raw string sits on the row whether anything interprets it or not. I
planted the `ev_volume_x` fault and half one passed. A populated numeric column that appears in a
data file and nowhere in the loader source is a column the engine cannot possibly be using.

Both halves distinguish three things that look identical on a report and need different work:
a row **shadowed** by an earlier peers file, a row **deliberately killed** (Daniil's
`LISTED_NOT_PRICING`, reason attached), and a field genuinely **absent**. A column may be silenced
only by an entry in `REASONED_UNREAD` carrying the reason, and an entry without a reason is not an
entry.

## What it found on its first run, beyond the bugs it was built for

- **The 12 recovered neobanks had the multiples and not the figures behind them.** Nu Holdings
  arrived with a 3.9x price to book and no book value per share, so nothing could ever show a
  founder what the 3.9x was a multiple OF. Fixed by widening the merge to the denominators.
- **All 123 logistics and services companies had no growth at all**, because that file calls the
  column `revenue_growth_pct`. Now read for DISPLAY and deliberately not given a `g_rank`: the file
  does not state the horizon, and the standing rule is that only a multi-year rate may rank a peer.
- **Net revenue retention for 83 listed software companies, and recurring revenue percentage for
  80, sit in the file unread.** Whether retention enters the quiz is an open decision from the
  29 August review. If it is kept, the peer data is already here.
- **MercadoLibre is 2.10x in the ecommerce pull and 2.20x in the fintech pull.** Two of Daniil's own
  pulls disagree by 5% about the same company on the same measure.
- **Three rows carry a physical quantity in a dollar column**: Xpansiv 121.5 MtCO2e, and Flo Health
  and Calm with millions of users. All three are now barred from pricing anything.

## Standing end-of-day check, for Fable

Run in this order. The first two are new; the rest already existed.

```
python3 tools/check_field_reach.py      # every FIGURE reaches the engine, every column is read
python3 tools/check_raw_coverage.py     # every supplied ROW is accounted for
python3 tools/check_engine_reach.py     # every row reaches the engine, no company votes twice
python3 selector/golden.py              # nothing moved that was not meant to
python3 tools/peer_universe_check.py    # the march gate
python3 tools/honesty_check.py          # every range is caveated
```

**What Fable should actually look at, rather than just running them.**

1. **Any new column in any data file since yesterday.** Every one is a chance for the same bug.
   `check_field_reach` will name it as unread; the question is whether it SHOULD be read.
2. **Any new file.** The five peers pulls already spell the same measures five ways. A sixth pull
   is the single highest-risk event in this repo.
3. **The shadowed-ticker lines.** Fifteen tickers appear in two peers files. The check says which
   file won. Ask whether the winner carries the measures the loser had, because that is precisely
   the neobank bug.
4. **Whether a range got THINNER anywhere.** Golden reports movement, not direction. A lane that
   loses a name is worth a look even when golden is happy to have been rebaselined.
5. **Anything that looks too tidy.** 11.52x on Xpansiv looked like a normal multiple. It was a
   price per tonne of carbon dioxide. A number that reads plausibly is not evidence.

**And the standing rule this all points at:** when a check passes and a human still finds a defect,
the bug to fix first is the check, not the defect.


---

# Part two, later the same day: is it architectural?

Daniil, after the fourth instance: "How is it possible, again, that I provide super large dataset, it
takes A LOT of time to create and paste it, and AGAIN it does not reach the user. What is the matter?
Is it architectural?"

**Yes. It is architectural, and part one of this document had not identified it.** Part one found
that our checks count rows while the bugs lose fields. That was true and it was not the whole
answer, because the failures kept coming from places a field-level check does not look.

## The chain a figure has to survive

A number Daniil supplies passes through seven stages before a founder sees it:

```
1  ARRIVES     a file lands in data/raw
2  INGESTED    a tool reads that file and writes it into data/
3  LOADED      match_reference reads the column into a row field
4  KEPT        the row survives dedup, kill lists and family gates
5  SELECTED    the matcher picks that row for this founder
6  PRICED      a basis exists that the row can answer on
7  SHOWN       the reveal renders it
```

Every failure found today is a different stage, and that is the finding:

| what was lost | stage | how it failed |
|---|---|---|
| the entire 1-Sep listed refresh, 509 rows | **1 to 2** | the ingest tool had no write path at all. The file sat in raw for two days |
| price to book for 12 neobanks | **3 to 4** | a ticker already seen in another file was skipped |
| 16 volume multiples | **3** | the column is spelled `ev_volume_x` here and `ev_gmv_x` there |
| growth for all 123 logistics rows | **3** | that file calls the column `revenue_growth_pct` |
| retention for 83 software rows | **3** | the loader never mentioned the column |
| Xpansiv's 121.5 MtCO2e | **6** | no basis existed that a physical volume could answer on |
| Flo Health and Calm's subscribers | **6** | no basis existed, and I then barred them on a bad rule |
| 13 companies dropped from the pull | **4** | a decision taken by OMISSION left no trace anywhere |

**There is no single accounting that follows a figure from stage 1 to stage 7.** Each stage has, at
best, a check of its own, and each check is satisfied by handing the problem to the next stage.
`check_raw_coverage` proves a row was accounted for at stage 2 and says nothing about stage 3.
`check_engine_reach` proves stage 3 to 4 and says nothing about stage 6. Golden watches stage 7 and
cannot see a value that has been absent since its baseline was written. **A figure can be lost at
any stage and every check will still pass**, which is exactly what a founder experiences as "the
data I sent is not in the answer".

## The second structural cause: a decision taken by omission

The 13 dropped companies are the clearest case and the one with no check anywhere near it. Daniil
made a real decision, correctly, by leaving names out of a pull. Nothing in the repo could see it.
Two of the fifteen had been written into `LISTED_NOT_PRICING` by hand weeks earlier; the other
thirteen kept pricing founders off superseded numbers.

**A decision expressed as an absence is invisible to every check that looks at what is present.**
That is why the fix is not another list to maintain: the newest `as_of` in the file now DEFINES the
current universe, and any row older than it is frozen with its reason. The next refresh enforces
the next set of kills without anybody remembering.

## The third: a schema that cannot express what the data says

Xpansiv, Flo Health and Calm were not lost by a loader. They were loaded, matched and shown, and
then found there was no denominator they could answer on, because the engine knew about revenue,
gross profit and book value and nothing else. A tonne of carbon and a paying subscriber had nowhere
to go, so they became either a fake x or a barred row.

**When a founder's data has no place in the schema, the honest failure is loud and ours was silent.**
The engine gave a number that looked normal (11.52x) or gave nothing at all, and in neither case
did it say "we hold this figure and cannot use it".

## What now exists

- `tools/check_field_reach.py` covers stages 3 and 4: every figure in a file reaches a row, and every
  populated column is at least read.
- `tools/apply_listed_refresh.py` covers stage 1 to 2 and, critically, EXISTS: the refresh now has a
  write path, matches across renamed tickers, and accounts for every row in both directions.
- `tools/check_cross_pull.py` covers the case of one company in two files.
- The `as_of` rule covers decisions taken by omission.
- Six bases now exist where three did (revenue, gross profit, book, earnings, ARR, originations,
  throughput, and the count family), so more of what Daniil sends has somewhere to go.

## What is still missing, and it is the one that matters

**Nothing yet reports, for a given supplied figure, WHERE IT STOPPED.** That is the check to build
next, and it is the only one that would have caught all eight of today's failures with one command:

> for every numeric cell in every file under `data/raw/`, say which of the seven stages it reached,
> and for anything that stopped before stage 6, say which stage and why.

Stage 6 is the right bar rather than stage 7, because a figure that can price SOMEBODY is doing its
job even if no current fixture needs it.

## For Fable, added to the end-of-day list

7. **Diff `data/raw/` against the loaded universe.** Any file added since yesterday that has not
   been ingested is the highest-severity finding available: that is a whole dataset Daniil spent
   time producing, sitting unused. The 1-Sep refresh sat for two days and no check looked.
8. **Ask what the newest `as_of` is, and how many rows are older.** A row left behind by a refresh
   is a decision somebody made; confirm it was deliberate.
9. **For any figure type newly appearing in a supplied file** (tonnes, subscribers, borrowers), ask
   whether a basis exists that can use it. If not, that is a schema gap and it should be raised as
   one, not absorbed silently.
