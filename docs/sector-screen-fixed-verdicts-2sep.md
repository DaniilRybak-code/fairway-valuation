# Sector screen, fixed version: what I checked and what I found

2 September 2026. Source: six screenshots of "Priced Private Funding Rounds - Sector Screen",
supplied by Daniil. Transcribed to `data/raw/2026-09-02_sector-screen-fixed.csv` (49 rows, 41 columns).
The 51-row original at `data/raw/2026-09-02_sector-screen.csv` is untouched, as raw files are append-only.

## The short answer

**42 of the 49 rows are usable now. 4 need your ruling. 3 are correctly out.**

The fix did what the prompt asked. Every multiple recomputes, every currency conversion recomputes,
the currency direction is right on all 14 converted rows, and the sheet's own header counts are all
true. The problems that remain are not arithmetic. Three rows use total income where the rest of the
set uses revenue from operations, and that is your gross-versus-net audit instruction landing in
live data.

## Row accounting, matched on company plus year and month

| | |
|---|---|
| Count in | 51 |
| Dropped | 2 |
| Added | 0 |
| Count out | 49 |

The two dropped rows, named:

- **Alan, May 2022.** Two rows four days apart, 05-May-2022 and 9-May-2022, both at a EUR 2,700m
  post-money. One round. The 05-May-2022 row survived.
- **BetterUp, October 2021.** Two rows for the same date written two ways, 2021-10-08 and
  08-Oct-2021, both at a USD 4,700m post-money. One round. The 2021-10-08 row survived.

Both deletions were instructed by rule 6 of `docs/sector-screen-fix-prompt-2sep.md`. Nothing else
left the set. 51 minus 2 plus 0 equals 49, and it balances.

I first ran this match on the sheet's own row numbers and got a wrong answer, because deleting two
rows renumbered everything below them. Matching on the row rather than on the position is the same
lesson as D12.

## What recomputes cleanly

- **47 multiples, 0 mismatches.** Post-money over denominator equals the stated multiple on every
  row that has one.
- **14 currency conversions, 0 mismatches.** Metric value times the stated rate equals the stated
  denominator on all 14. Every one carries a rate, a date and a source.
- **Currency direction, 0 mismatches.** The denominator is restated into the valuation's currency on
  every row, never the reverse. EGYM and Voodoo, the two rows that held a USD metric against a EUR
  valuation, both moved to EUR.
- **The sheet's own header counts are all true.** 49 transactions, 47 populated multiples, 46
  non-excluded, 8 ceilings, 2 NOT FOUND. The 8 ceilings all carry `bound = GTE`.
- **Target 48 was not padded, and the shortfall is named.** 46 usable, not 48, because Fuse Energy
  has no public valuation and Celsius is excluded for fraud. That is the honest answer, not a gap.

## Finding 1: three rows use total income, not revenue from operations

This is the one that matters. Your amendment 4 in `docs/RULES.md` asked for an audit of whether the
net numbers are net and the gross are gross. Three rows fail it, and the set is inconsistent with
itself: Ninjacart uses revenue from operations while WayCool, Dream Sports and LEAD School use total
income.

**Dream Sports, 24-Nov-2021. Material.** The sheet uses INR 27,060m. The company's own release says
total income was Rs 2,705.56 crore and revenue from operations was Rs 2,551.59 crore. The sheet is
using total income. On revenue from operations the multiple is **23.4x, not 22.1x**.

**LEAD School, 12-Jan-2022. Material.** The sheet uses INR 600m for FY2021. Entrackr, reading the
RoC filings, reports operating revenue of Rs 57.1 crore, which is INR 571m. The INR 600m looks like
total income rounded. On operating revenue the multiple is **142.2x, not 135.3x**. The Forbes India
page cited as the revenue source returns 403 and I could not read it, so this row's stated source
cannot be checked at all.

**WayCool Foods, 22-Jun-2022. Immaterial but wrong.** The sheet uses INR 9,306m. The cited Inc42
article says operating revenue was INR 926.9 crore and that INR 930.6 crore is "total revenue,
including interest income and other operating revenue". The sheet took the second. The multiple
stays at 5.9x either way, so nothing moves, but the basis label is wrong.

**Ninjacart, 13-Dec-2021. Correct, and it is the control.** The cited Inc42 article says "revenue
from operations grew 60% year-on-year to INR 747.6 Cr in FY21". The sheet's INR 7,476m is that
figure, converted correctly. This is what the other three should look like.

I have not changed any of these. They are your figures and the gross-versus-net call is the one you
asked to have audited rather than settled quietly.

## Finding 2: five rows label the denominator period differently from the metric period

| Row | Company | Metric period says | Denominator basis says |
|---|---|---|---|
| 34 | LEAD School | FY2021 | Entering academic year 2022-23 |
| 41 | Oura | FY2023 estimate | FY2024 expected |
| 42 | Athletic Greens | Early 2022 | Current annualised revenue run-rate |
| 49 | Roblox | FY2020 | blank |
| 52 | Discord | FY2020 | FY2021 |

**Discord is the one the fix prompt asked to resolve** and it was only half resolved. The prompt said
metric 130 for FY2020 against denominator 310 for FY2021, pick one and cite it. The value was
picked, 130, and it is right: multiple sources report Discord's 2020 revenue at $130m, up 189%. But
the denominator basis still reads FY2021. The number is correct and the label is wrong.

**Roblox is correct on the value.** $923.89m for FY2020, confirmed. The denominator basis cell is
simply empty.

Athletic Greens is a wording difference, not a contradiction. LEAD School and Oura are real.

## Finding 3: Oura's denominator rests on a tier 4 source alone

The TechCrunch article cited as Oura's valuation source contains no revenue figure at all. It says
only that "the company's member base and revenue has more than doubled over the past year". The
entire $225m denominator comes from Sacra, which is tier 4. Your standing rule allows tier 4 only
when tiers 1 to 3 are empty. Nobody has shown that they are. This row also carries the FY2023 versus
FY2024 label contradiction above, and the fix changed its metric from a 500 run-rate to a 225
estimate, which moved the multiple from 10.4x to 23.1x. It should not price anything until the
denominator has a better source or you accept the tier 4.

## Finding 4: four rows are tagged the wrong tier

Your rule names Sacra, Forge, CB Insights and personal blogs as tier 4.

| Row | Company | Tagged | Rests on | Should be |
|---|---|---|---|---|
| 6 | Ninjacart | 3 | cbinsights.com for the valuation | 4 |
| 7 | Vegrow | 3 | gokulnk.com, a personal blog, for the revenue | 4 |
| 35 | MasterClass | 3 | forgeglobal.com for both figures | 4 |
| 29 | Doctolib | 2 | scanfacture.fr, a filings aggregator | 3 at best, your call |

Ninjacart's underlying numbers are right, so this is a labelling fix, not a data fix. MasterClass
rests on Forge for both the valuation and the revenue, which under your rule makes the whole row
tier 4 evidence.

## Finding 5: I cannot see four of the sheet's columns

The screenshots run A to AB and then jump to AG. **Columns AC, AD, AE and AF were never visible.**
Under D11 a schema must carry every column the source has, so this transcription is explicitly
incomplete and says so in its header. Send those four columns and I will fill them in.

## What I checked against live sources

Confirmed correct: Ninjacart INR 747.6 crore FY21 revenue from operations; Roblox $923.89m FY2020;
Fireblocks revenue "between $50 and $100 million" for 2021 with the CEO declining a specific number,
which makes the $50m floor and the GTE bound exactly right; Octopus FY2021 revenue, where the press
release says "from £1.2bn to £2bn" against the sheet's £2,008.8m, close enough that the multiple does
not move but the precise figure comes from the annual report, not the release cited.

Found wrong: Dream Sports, LEAD School, WayCool as above. Could not read: Forbes India for LEAD
School, 403.

## Recommendation

Load the 42 clean rows. Hold these four until you rule:

1. **Dream Sports** and **LEAD School**: total income or revenue from operations. I would say revenue
   from operations, which makes them 23.4x and 142.2x.
2. **WayCool**: same question, no effect on the multiple, so this is just a label.
3. **Oura**: accept a tier 4 sole source for the denominator, or leave the row unpriced.

Correctly out and staying out: eFishery, fabricated figures. Celsius, bankruptcy and fraud. Fuse
Energy, no public valuation.

---

# Finding 6: the sector screen cross-checks four rows already in the medians, and three disagree

This was not in the brief and it is the most important thing on the page. Four of the 49 sector
screen rounds are already loaded in `data/private-rounds.csv`, all four from your 191-row private
transactions sheet. Two of your own sheets carry different numbers for the same four rounds.

| Round | Private sheet, in the engine | Sector screen | Verdict |
|---|---|---|---|
| MoonPay Nov-21 | 3,400 / 150 = 22.67x, basis GROSS_REVENUE, period LTM | 3,400 / 150 = 22.7x, 11-month, not annualised | Same number, engine label wrong |
| Fireblocks Jan-22 | 8,000 / 100 ARR = 80.0x | 8,000 / 50 = 160.0x, ceiling | **Sector screen is wrong** |
| wefox Jul-22 | 4,500 / 320 LTM = 14.06x | 4,500 / 200, four months of 2022 = 22.5x | Needs your ruling |
| Alan Sep-24 | USD 4,500 / USD 550 ARR = 8.18x | EUR 4,000 / EUR 450 ARR = 8.9x | Needs your ruling |

**Fireblocks resolves against the sector screen, with evidence.** The engine holds two Fireblocks
rounds: Jul-21 at 2,000 over 50 ARR, and Jan-22 at 8,000 over 100 ARR. So the $50m ARR is the July
2021 Series D figure, and it already prices its own row at 40.0x. The sector screen has taken that
same $50m as the January 2022 Series E denominator and produced 160.0x, which is double. Its own
denominator basis cell says "Prior year / FY2021", which is the admission. The TechCrunch source
says revenue "grew by 600% over the year, ending with a figure between $50 and $100 million" and
that the CEO declined to give a number, so $50m is where that year started, not where it ended.
The engine's 80.0x stands and sector screen row 23 should not be loaded as it is.

**MoonPay is the reverse: the sector screen is right and the engine label is wrong.** Both say
$150m, but the sector screen records it as an eleven-month year-to-date figure at November 2021,
while the engine carries it as `revenue_basis = GROSS_REVENUE`, `revenue_period = LTM`. An
eleven-month year-to-date number is not LTM. The multiple does not move, so nothing is mispriced
today, but the label is wrong and the basis audit should catch it.

**wefox and Alan are live disputes, so under D6 they are out of the medians as of now.**

I set `in_medians = 0` on both. Median-eligible went from **114 to 112**. Row count is unchanged at
184, the coverage check still passes, the 2% multiple check still passes, and `selector/golden.py`
still reports 0 of 43 moved. Each row carries a note in `notes` saying why it is held and that it
goes back when you rule. To reverse either one, set `in_medians` back to 1 and delete the note.

On wefox I lean to the engine: an LTM figure available at pricing is the revenue investors had, and
the sector screen's own forward column records the $600m FY2022 guidance, which is what the
four-month $200m annualises to. On Alan I have no view yet. The post-money reconciles across the two
currencies, EUR 4,000m against USD 4,500m at September 2024 rates, but the ARR does not: USD 550m is
about EUR 495m, not EUR 450m. One of the two sheets has the wrong ARR and I cannot tell which from
the sources cited.

## Revised recommendation

- **41 sector screen rows load clean.**
- **5 held for a ruling**: Dream Sports, LEAD School, WayCool (gross versus net), Oura (tier 4 sole
  source), Fireblocks (denominator belongs to the prior round).
- **3 stay out**: eFishery, Celsius, Fuse Energy.
- **2 engine rows held under D6**: wefox Jul-22, Alan Sep-24.
- **1 engine label to fix**: MoonPay Nov-21, eleven-month year-to-date is not LTM.
