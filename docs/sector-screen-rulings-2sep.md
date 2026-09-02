# Sector screen: Daniil's rulings of 2 September 2026, and what each one did

Follows `docs/sector-screen-fixed-verdicts-2sep.md`. Seven rulings, all applied. Where a ruling was
conditional and the condition turned out not to hold, that is said plainly rather than worked around.

## Ruling 1, gross versus net: "ok to use whatever is available, with the respective note"

Applied. Dream Sports, LEAD School and WayCool keep the total income figures they carry and will
load with `revenue_basis = TOTAL_INCOME` and a note naming the alternative.

| Row | Loads at | Basis | Also available |
|---|---|---|---|
| Dream Sports 24-Nov-2021 | 22.1x | Total income, Rs 2,705.56 crore | Revenue from operations Rs 2,551.59 crore, which would give 23.4x |
| LEAD School 12-Jan-2022 | 135.3x | Total income, INR 600m | Operating revenue Rs 57.1 crore per the RoC filings, which would give 142.2x |
| WayCool 22-Jun-2022 | 5.9x | Total revenue incl. interest, INR 9,306m | Operating revenue INR 926.9 crore. Multiple is 5.9x either way |

One thing to know that the ruling did not cover. For Dream Sports and WayCool the revenue from
operations figure is stated in the very same source, so it is not a case of taking what we can get.
Ninjacart, the fourth Indian row, uses revenue from operations. So the set will be internally
inconsistent on basis, which is visible in the notes and is the thing a reviewer would pick at. Say
the word and I will move all four to revenue from operations for the like-for-like version.

## Ruling 2, Discord: "if this is the case, we need to drop"

**The condition does not hold, so I have not dropped it.** Your reading was that we need a 2021
denominator and only have 2020. It is the other way round.

The round priced on 15 September 2021. At that date the last completed year was 2020, and Discord's
2020 revenue was about $130m. That is the revenue investors had at pricing. The $310m figure is the
FY2021 outturn, which nobody knew in September 2021, and using it would be pricing the round on
information that did not exist yet. That is the same principle you applied across all 19
reconciliation verdicts: a multiple uses the revenue investors had at pricing, never a later actual.

So $130m is not a fallback, it is the correct denominator. The only thing wrong with the row is the
basis label, which says FY2021 and should say FY2020. Loading at **115.4x** with the label fixed.

It is a high multiple. It is also a real one for a September 2021 round, and the honesty layer will
carry it as an outlier rather than hide it. If you still want it out after reading this, say so and
it goes, but I did not want to drop a correct row on a premise that was inverted.

## Ruling 3, Oura: "ok, with respective note for the user"

Applied. Loads at 23.1x with `source_tier = 4` and a user-facing note saying the denominator comes
from an estimator rather than the company or the press. Also fixing the sheet's internal
contradiction: the denominator basis cell says FY2024 expected while the metric period says FY2023
estimate. FY2023 is right, because the roughly $500m forward figure already sits in `forward_metric`.

## Ruling 4, Vegrow: "whose personal blog is that? if founder or management, ok to accept"

**Answered, and it does not clear the bar. Held.**

The author is Gokul NK and his LinkedIn does show him at Vegrow, so on the narrow question you asked
the answer is yes, he appears to be staff. But the page itself does not clear your condition:

- It makes no claim of authority. It does not say he works there or that these are company figures.
- It reads as personal research notes and cites **thekredible**, a third-party aggregator, for its
  numbers. So it is not a company disclosure, it is a summary of someone else's estimate.
- Most importantly, the page gives "Gross Revenue 100 cr and 361 cr" with **no year attached to
  either**. The sheet assigns the 361 crore to the year ended 31 March 2023 on no stated basis.

Inc42 has Vegrow at Rs 407.9 crore for FY24 and Rs 554.9 crore for FY25 but publishes nothing for
FY23, and FY24 closed after the December 2023 round so it cannot be used anyway.

An undated number pinned to a specific financial year is the one thing your rules do not bend on.
Held until there is a dated FY2023 source. Agritech is thin and I would like this row, but not on
this evidence.

## Ruling 5, columns AC to AF: "hidden for a reason, not important"

Noted. The D11 flag is withdrawn and the transcription is recorded as complete for our purposes,
with a line in the raw file saying those four columns were hidden deliberately and are not needed.

## wefox: dispute resolved in the engine's favour

The TechCrunch Series D piece carries all three figures: revenues "doubled to $320 million last
year", "$200 million in the first four months of 2022", and a $600m full-year target. FY2021 is the
last completed year at pricing and the like-for-like annual basis. The sector screen picked the
four-month stub, which is also inconsistent with its own wefox Series C row, priced on FY2020.

**Back in the medians, unchanged at 14.06x.** The sector screen's version is not loaded.

## Alan: dispute resolved in the sector screen's favour, and the engine was wrong

The TechCrunch article cited by **both** sheets says: "It expects its annual recurring revenue to
reach €450 million (around $500 million) this year."

The engine carried USD 550m. That figure appears in no source. Corrected:

| | Was | Now |
|---|---|---|
| revenue_musd | 550.000 | 500.000 |
| ev_revenue_x | 8.18 | 9.00 |
| bound | `<=` | `>=` |
| in_medians | 0 | 1 |

9.00x now ties to the sector screen's EUR 4,000m over EUR 450m at 8.9x, the small gap being the
article's own rounding of €450m to "around $500 million".

The bound change matters more than the number. `<=` in this file means the denominator is a "more
than" floor, so the multiple is a ceiling and the honesty layer tells a founder "at most". Alan's
denominator is a forward year-end expectation, so trailing ARR at pricing was **below** it, which
makes 9.00x a floor, not a ceiling. The old `<=` was telling founders "at most 8.2x" when the true
trailing multiple is higher than 9.0x. That was backwards and is now right.

## State after all of this

- `data/private-rounds.csv`: 184 rows, **median-eligible back to 114**, both D6 holds released.
- `python3 tools/check_raw_coverage.py`: PASS, 191 of 191 and 49 of 49 accounted for.
- The 2% multiple check: 0 failures. `selector/golden.py`: 0 of 43 moved.
- Sector screen: **44 rows cleared to load**, 2 held (Vegrow, and Fireblocks which is not loaded
  because the engine already has the better version), 3 stay out (eFishery, Celsius, Fuse Energy).
- Not yet done: the load itself. These 44 rows are cleared but are still only in the raw file. That
  is the next job.
