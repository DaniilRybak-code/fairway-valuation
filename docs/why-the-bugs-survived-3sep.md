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
