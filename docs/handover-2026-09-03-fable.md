# Handover to Fable, 3 September 2026

Pilot launches the week of **21 September 2026**. Eighteen days.

Two things are asked of you here, in this order:

1. **Audit the new data**, selectively. Section 3 names exactly what to check and what to leave
   alone. It is scoped to spare credits: roughly a dozen figures, not three hundred.
2. **Inspect what was built against the investors and recommendations roadmap**, and tell Daniil
   what is finished, what is half-finished, and what was never started. Section 4 has what I found;
   check it rather than trust it.

---

## 1. State, and how to reproduce it

Run these four. Any deviation is the story.

```
python3 tools/check_raw_coverage.py     # PASS, three supplied files, 0 unaccounted
python3 selector/golden.py              # 0 of 43 profiles moved
python3 tools/data_inventory.py         # engine loads: listed 511, private 289
python3 tools/investor_check.py         # curated vs renderable, by sector
```

| | |
|---|---|
| `data/private-rounds.csv` | **237 rows** |
| `data/private-rounds-consumer.csv` | 52 rows |
| Private rounds reaching the engine | **289, all of them** |
| Untagged | **0** |
| Median-eligible | **179** |
| `data/private-companies-tags.csv` | 176 rows |
| Companies under more than one key | 0 |
| Post-money over revenue vs stored multiple, 2% tolerance | 0 failures |
| `in_medians = 1` rows lacking a multiple or either URL | 0 |

Twenty-four hours ago the engine loaded 178 private rounds and could not see a third of the file.
The cause was a silent join to the tags file; 41 companies had no tag row. That is fixed, and
everything since has been loaded with a tag row in the same commit.

---

## 2. What arrived and what was done with it

**Sector screen** (`data/raw/2026-09-02_sector-screen-fixed.csv`, 49 rows). 40 loaded, 9 not, all
nine named. Agritech, energy retail, crypto, healthtech, edtech, consumer health, insurtech, gaming.
Verdicts in `docs/sector-screen-fixed-verdicts-2sep.md`, rulings in `docs/sector-screen-rulings-2sep.md`.

**Lending screen, revised** (`data/raw/2026-09-03_lending-screen-v2.csv`, 22 rows). The first pull
priced ten rows on cumulative-since-inception volumes, which are not multiples. Daniil re-ran it.
Every cumulative denominator is gone and the sheet now reconciles exactly to its own header: 17
bounded multiples, 2 NM, 3 NOT FOUND. 13 rows loaded, 3 previously unpriced engine rows priced on
periodic originations, 6 skipped as already held.

**The single most valuable row in either sheet: Atom Bank, February 2022, 3.17x on consolidated
total equity at 31-Mar-2021, from the filed annual report.** That is the second priced BOOK
comparable we hold. Zopa at 5.6x was the only one, and four fixtures have been pricing off it alone
since the lending fork was built.

---

## 3. The audit, scoped

Do not re-verify everything. Almost all of it reproduces arithmetically and the arithmetic has been
checked twice. What arithmetic cannot check is whether a figure means what its label says. That is
what you are for, and only these need you.

### 3a. High risk, check these first. Eight figures.

| # | Row | What to check | Why it is high risk |
|---|---|---|---|
| 1 | **LEAD School Jan-22, 135.3x** | Is INR 600m LEAD School's FY2021 figure, and is it total income or revenue from operations? | Highest multiple in the whole base. Entrackr reads operating revenue of Rs 57.1 crore from the RoC filings, which would make it 142.2x. The cited Forbes India URL returns 403 and could not be read at all |
| 2 | **Dream Sports Nov-21, 22.06x** | Total income Rs 2,705.56 crore was used; revenue from operations was Rs 2,551.59 crore | Loaded on Daniil's ruling to use what is available. 6% denominator difference, moves it to 23.4x |
| 3 | **Klarna, all three rounds** | Which SEK/USD rate, and on what date | The engine holds 1,212.1 and 1,303.7; the sheet says 1,087 and 1,600 for the same figures. Both are net operating income. **The entire gap is the exchange rate and neither file records it.** Multiples move 37.6x to 41.95x and 5.1x to 4.19x |
| 4 | **Atom Bank Feb-22, 3.17x book** | Is GBP 137.0m consolidated total equity at 31-Mar-2021, and is the GBP 435m valuation the same entity | It is about to become half of our entire book-multiple evidence. Verify against the annual report PDF, not the press |
| 5 | **Oura Dec-24, 23.1x** | Does any tier 1 to 3 source give Oura a 2023 revenue figure | The denominator rests on Sacra alone. The cited TechCrunch piece carries no revenue number at all |
| 6 | **Discord Sep-21, 115.4x** | Confirm $130m is 2020 and that no 2021 figure was public before 15 September 2021 | Loaded over Daniil's instinct to drop it. If a 2021 figure was public at pricing, the row is wrong and I argued the wrong way |
| 7 | **Konfio Sep-21, 39.23x** | MXN 680m at 0.04873 on 29-Sep-2021 | The rate implies 20.5 MXN per dollar; MXN traded nearer 20.0 that week. Second-highest multiple in the lending set |
| 8 | **Tala Oct-21, 13.33x** | Confirm the $60m is a monthly origination pace | A one-month denominator. Annualised it is about 1.11x. It is out of the medians and flagged, but if anyone reads 13.33x as annual it is wrong by twelve times |

### 3b. Do not spend credits on these

Everything else in both sheets reproduces exactly, carries two URLs, and was cross-checked against
the engine where a round already existed. Ninjacart, Roblox, Fireblocks, Discord's value, Octopus
and the whole Indian block were verified against primary sources on 2 September. Do not repeat that.

### 3c. Structural questions, no sources needed

- **Three rows are priced on a PRE-money valuation**: Starling Bank Mar-21, Upgrade Nov-21 and
  Aug-21. Every other multiple in the base is post-money. Starling's 7.59x is the lowest of the
  lending revenue multiples and is not like for like. Should pre-money rows carry a flag the honesty
  layer reads?
- **Four Indian rows are inconsistent on basis**: Ninjacart uses revenue from operations; Dream
  Sports, LEAD School and WayCool use total income. Daniil ruled to use what is available with a
  note. The notes are there. The inconsistency is still visible to a reviewer.
- **Three companies are loaded unpriced** (Zilch, Billie, Pipe) because the revised sheet marked
  them NOT FOUND. They appear in peer lists and contribute no multiple. Confirm that is what we want.

### 3d. The two checks that do not exist and should

Both were found the hard way in the last day.

1. **A file-versus-engine check.** Nothing compares what is in `data/private-rounds.csv` to what
   `match_reference.py` actually loads. 58 rounds were invisible for days. It is the third of the
   three candidate checks at the foot of `docs/RULES.md` and it is now the most overdue.
2. **A cross-file duplicate check.** AG1's January 2022 round was in the engine twice under two
   keys, and the sector screen would have made it three times. It was caught by reading a golden
   diff, not by any check. Match on company plus month plus post-money, not on name: the three
   spellings were "AG1", "AG1 (Athletic Greens)" and "Athletic Greens (AG1)".

---

## 4. The investors and recommendations roadmap: what is actually built

Checked against `docs/investors-and-recommendations-roadmap-2sep.md`. **Verify this rather than
trust it**, because it is the part of the handover I am least sure of.

### Built

- `data/investors.csv`, **408 houses, 32 columns**, generated by `tools/build_investors_table.py`
  and validated by `tools/investor_check.py`.
- The `layer` split the roadmap asked for exists: **59 CALLABLE, 81 CALLABLE and EVIDENCE, 268
  EVIDENCE**, so 140 houses are callable in principle.
- `tools/load_seed_screen.py` folds Daniil's seed screen in, and 52 funds arrived that way.

### Not built, and this is the headline

**Nothing reads `data/investors.csv`.** The only files that touch it are the tool that writes it and
the tool that checks it. `tools/data_inventory.py` has been printing `NOT READ BY THE ENGINE` next to
it since it was created. There is no renderer, no API surface, and no reveal integration. Both
features are promised on the landing page and neither reaches a founder.

### Two data problems in the layer that is built

1. **Layer 1's own quality bar is met by 52 of 408 houses, not the 124 previously reported.** The
   roadmap says a Layer 1 card must carry a dated deal with a source URL, a first-cheque range,
   stage, geography and a one-line thesis, and that a row missing any of those does not render.
   Counting rows that have all six gives 52. The binding gaps are **`first_cheque_low_m` blank on
   346 rows and `geographies` blank on 342**. Somebody should reconcile the 124 against this before
   it goes in a status report.
2. **`tools/investor_check.py` is emitting duplicate sector buckets with numeric suffixes**:
   "Lending & Credit(1)", "Vertical Software(1)", "Vertical Software(2)", "Sales Engagement(1)",
   "(2)", "(3)". That is a splitting bug, not a taxonomy. It makes the per-sector counts unreadable
   and may be masking real coverage.

### Suggested order

Fix the sector-suffix bug first, because every coverage number downstream is read through it. Then
reconcile the renderable count. Then decide whether Layer 2, the evidence list, ships first: it needs
no curation because it falls out of the selector, and it is the layer nobody can copy.

---

## 5. Standing constraints, unchanged

Read section 1 of `claude/Fairway_HANDOVER_2026-09-02.md` in full before touching anything. The ones
that bite most often: no git command on Daniil's machine through the bridge, ever, including
read-only. Screenshots are the only transfer route for his workbooks. `git add -A`, never a
hand-written list. Every supplied row accounted for by name, matched on the row and not the entity.
No em dashes.

## 6. Open decisions for Daniil

1. Kriya Oct-25, post-money 7.5 against revenue 12.6. Unit error, held out.
2. **Klarna's exchange rate**, which is now the only thing separating our figures from his. The
   basis question is settled: it is net operating income, confirmed from two independent pulls.
3. Fourteen curated investor funds have no dated deal and do not render.
4. Vegrow, held: the revenue source is a Vegrow employee's personal notes page, the figure carries no
   year, and it cites a third-party aggregator.
5. Fireblocks Jan-22 from the sector screen, not loaded: its $50m denominator is the July 2021
   round's ARR, which already prices its own row at 40.0x.
6. The four Indian rows and their gross-versus-net inconsistency.
