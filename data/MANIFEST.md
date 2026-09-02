# Data manifest

**Every drop of data gets a row here on the day it arrives, before anything is built on it.**

The rule this file exists to enforce, written 30 August 2026 after four separate pulls were sent as
screenshots, read on screen, and never written to disk:

> **NOTHING IS "RECEIVED" UNTIL IT IS A FILE IN `data/`.** Not when it is discussed, not when the
> numbers are quoted back, not when a conclusion is drawn from it. A screenshot is not a file. A
> figure that exists only in a conversation is lost the moment that conversation compacts.

## The intake sequence, in order, no steps skipped

1. **Land the raw file first.** Original, unedited, into `data/raw/` with the date in the name.
   Nothing is analysed, quoted or reasoned about until this has happened.
2. **Add a row to the table below**: what it is, when it arrived, how many rows, where it came from.
3. **Transcribe or convert into a working file** in `data/`, keeping the raw copy untouched so any
   later dispute can be settled against the original.
4. **Run `python3 tools/data_inventory.py`** and paste the row counts back to Daniil, so he can see
   the number that landed matches the number he sent.
5. **Wire it into the loader** (a tags file with an archetype per name) or record here that it is
   not wired yet. A file the engine does not read is not coverage.

## Why files beat screenshots, in one line each

- A CSV lands byte-exact. A screenshot lands as my reading of a screenshot.
- A CSV carries the source URLs. At screenshot resolution a URL wrong by one character is worse than
  no URL, and our own rule says every figure carries a named source.
- A CSV survives a session ending. An image in a conversation does not.
- A CSV can be diffed. A screenshot cannot be checked against anything.

Screenshots stay useful for one thing: showing me what something looks like so I can ask the right
question about it. They are not a transfer mechanism.

## How to send

Best: save the workbook tab as CSV straight into `~/fairway-valuation/data/raw/`. It is a connected
folder, so it reaches me the moment it is written, byte for byte, and it is in the repo the moment
you commit.

Also fine: attach the CSV or the .xlsx to the conversation.

## The log

| arrived | what | rows | raw file | working file | wired into engine |
|---|---|---|---|---|---|
| 2026-08-30 | Listed specialty finance and lending, P/E and P/BV | 79 | transcribed from screenshot, NO RAW | `data/peers-lending.csv` | **no**, needs tags |
| 2026-08-30 | Listed logistics, services marketplaces, consumer subscription, payments | 123 | transcribed from screenshot, NO RAW | `data/peers-logistics-services.csv` | **no**, needs tags |
| 2026-08-30 | Private financing transaction database, 58 valuation-backed rounds | 58 | transcribed from screenshot, NO RAW | `data/private-rounds-master-30aug.csv` | **no**, source URLs missing |
| 2026-08-30 | **Listed software, refreshed pull.** Growth redefined as CY+0 to CY+2 CAGR; recurring revenue % added | 167 | `data/raw/2026-08-30_capiq-listed-software.csv` | `data/peers-software.csv` | **yes** |
| earlier | Listed software, first pull, superseded above | 166 | not recorded | `data/peers-software.csv` | yes |
| 2026-08-30 | **Listed fintech, payments, exchanges, market data. Refreshed pull.** | 85 | `data/raw/2026-08-30_capiq-listed-fintech.csv` | `data/peers-fintech.csv` | **yes** |
| 2026-08-30 | **Company-disclosed recurring revenue and retention**, five research passes, software set | 68 recurring + 42 retention | no raw, sourced from filings | `data/peers-software.csv` | **yes** |
| earlier | Listed fintech, first pull, superseded above | 87 | not recorded | `data/peers-fintech.csv` | yes |
| 2026-08-30 | **Listed ecommerce, marketplaces, travel, classifieds, media, consumer brands. Refreshed pull, WITH GMV.** | 74 | `data/raw/2026-08-30_capiq-listed-ecommerce.csv` | `data/peers-ecommerce.csv` | **yes** |
| 2026-08-30 | **Company-reported GMV disclosures**, metric name, period, scope and caveat | 74 checked, 25 disclose | `data/raw/2026-08-30_gmv-disclosures.csv` | `data/gmv-disclosures.csv` | not wired, reference file |
| earlier | Listed consumer commerce, first pull, superseded above | 71 | not recorded | `data/peers-ecommerce.csv` | yes |
| earlier | Private rounds, software and fintech | 99 | not recorded | `data/private-rounds.csv` | yes |
| earlier | Private rounds, consumer | 50 | not recorded | `data/private-rounds-consumer.csv` | yes |

## Three growth definitions now live in the files, and none of them may be blended

Each pull has arrived with growth measured differently, and every row records which one it carries
in `g_basis` so a comparison across them can never be made blind:

| basis | which files | what it is |
|---|---|---|
| `CAGR_CY0_CY2` | software, fintech | two-year CAGR from CY+0 to CY+2 |
| `CAGR_CY1_CY3` | ecommerce | two-year CAGR from CY+1 to CY+3 |
| `NTM` | older rows not yet refreshed | one-year forward growth |

The first two are both forward two-year CAGRs anchored a year apart. Close cousins, not the same
measure. The third is a different animal entirely and is only still present on rows an updated pull
has not yet reached.

## GMV: what is reported and what is assumed

`data/gmv-disclosures.csv` holds the company-reported figure for all 74 ecommerce names: **25
disclose something, 49 do not.** It carries the metric name, the fiscal period, the currency, the FX
basis, the scope and the exact caveat. **It is the file to cite to a founder.**

Seventeen different metric names appear across those 25 companies, and they do not measure the same
thing: Gross Merchandise Volume, Gross Merchandise Sales, Marketplace GOV, Gross Bookings, Gross
Booking Value, Gross Transaction Value, Gross Order Value, Gross Services Volume, Bookings. Three
carry scope that changes their meaning outright: Sea reports Shopee only, Tripadvisor reports the
Viator segment only, ASOS reports an issuer-defined alternative performance measure. Roblox's
Bookings is a cash-value KPI the company does not call GMV at all.

**The forward GMV columns in `peers-ecommerce.csv` are Daniil's, not the brokers'.** Brokers do not
publish GMV estimates, so he assumed GMV grows with revenue in local currency and pro-rated to an
NTM figure. Any EV/GMV multiple therefore inherits that assumption, and every such row is stamped
`gmv_basis = DERIVED_FROM_REVENUE_GROWTH`. It must never be presented as a third-party forecast.

## A defect this found, and the rule that comes out of it

Enriching the retention column on 30 August exposed that **twelve retention values were not
retention at all**. Every one of the twelve software names that carried a recurring-revenue
percentage had the identical number sitting in `nrr_pct`: Adobe 96 and 96, MongoDB 97 and 97,
Shopify 22 and 22. Shopify is the proof, because no going concern retains 22% of its revenue.
The recurring share had been written into the retention column, and it had been feeding the
retention spread we quote to founders.

All twelve were cleared. Eight were then re-sourced from filings and are back with the real figure:
BlackLine 102, Five9 106, GitLab 118, MongoDB 121, Sprinklr 104, Tecsys 106 (its Elite product line
only, not the company), plus Q2 Holdings and RingCentral marked stale. Four were confirmed to
disclose nothing at all: Adobe, Shopify, Workday, and Vitec, whose own materials publish recurring
revenue as a share of sales, which is precisely the figure that got mistaken for retention.

**THE RULE. Every metric column carries its own status and source, and a value with neither is
marked UNSOURCED_NEEDS_VERIFICATION rather than trusted.** Twelve rows carry that mark today. They
sit in a plausible retention range and are probably right, but nothing records where they came from,
so they cannot be defended to a founder. They stay in the file with the warning rather than being
deleted, because deleting real data to tidy a column is worse than carrying it honestly.

Two statuses distinguish how a figure was arrived at, and the difference is not cosmetic:
`DISCLOSED` means the company stated the percentage itself; `CALCULATED` means it disclosed the
numerator and denominator separately and the division is ours.

## Refreshing a listed pull

Public comps move with share prices, so these files are refreshed, not written once. Daniil,
30 August: "public comps will be updated regularly due to share price movements."

    python3 tools/refresh_listed_pull.py data/raw/<new pull>.csv data/peers-<set>.csv

The tool exists because an overwrite would destroy work. A market-data file holds two kinds of
column and they must be treated differently:

- **Market columns** (market cap, enterprise value, revenue, gross profit, the multiples) move every
  time the market does and are replaced wholesale.
- **Analysis columns** (net revenue retention and its period, scope, source and status; paying
  users) were researched by hand, do not move with the share price, and are preserved. There are 51
  hand-researched retention figures in the software file alone.

The join key is `exchange_ticker`, never company name. Every row carries an `as_of` date, so a name
that drops out of a later pull keeps its old figures and is visibly stale rather than assumed fresh.

The tool reports, and never silently resolves, three things: names dropped from the new pull, names
added by it, and names with no tags row, which the engine cannot match however good the market data.

**The three rows marked NO RAW are the debt.** They were transcribed by eye from screenshots because
the originals never reached the machine. They should be replaced by the real export and the raw file
recorded here, at which point my transcription can be diffed against it and any reading error found.

## 30-Aug-2026, evening

| File | Rows | What it is | Read by the engine |
|---|---|---|---|
| `raw/2026-08-30_volume-metrics-disclosure-research.csv` | 166 | Company-reported GMV and transaction value across logistics, services, consumer and payments, with the issuer's exact words and a source URL per row. 26 disclosed, 63 not disclosed, 77 excluded by business model. | No, raw |
| `raw/2026-08-30_capiq-listed-gmv-block.csv` | 12 | The GMV and volume block from the 21-Aug Capital IQ pull, the only twelve names in it that carry a broker volume estimate. | No, raw |
| `raw/2026-08-30_capiq-tickers-as-supplied.csv` | 104 | Tickers as Capital IQ supplied them. This morning the same pull arrived with the ticker column hidden and 123 tickers were recovered by hand; this is what checked them. | No, raw |
| `volume-metrics.csv` | 240 | The merged overlay of company-disclosed volume. Supersedes `gmv-disclosures.csv`. | Yes, as an overlay |
| `gmv-disclosures.csv` | 74 | Superseded. Kept only so the ecommerce sheet's provenance stays auditable. | No, superseded |

## 31-Aug-2026, TPV

| File | Rows | What it is | Read by the engine |
|---|---|---|---|
| `raw/2026-08-31_tpv-disclosure-research.csv` | 28 | Issuer-reported payment volume with the exact metric name, scope, an audit note and a filing URL per row. 21 reported, 4 segment-only, 3 not disclosed. | No, raw |
| `raw/2026-08-31_capiq-tpv-block.csv` | 27 | The Capital IQ TPV block, CY+0 to NTM, with local-currency revenue carried so the growth applied can be checked rather than trusted. | No, raw |
| `volume-metrics.csv` | 268 | The overlay, now including TPV. 63 usable, 13 not. | Yes, as an overlay |

## 31-Aug-2026, outstanding pull recorded rather than remembered

| File | Rows | What it is | Read by the engine |
|---|---|---|---|
| `../docs/cagr-needed-pull-list.tsv` | 192 | The listed names that hold a single forward year and no CAGR, so they cannot rank on growth under Daniil's 31-Aug ruling. 105 consumer, 75 fintech, 12 software. Pastable into Excel. Owner: Daniil, promised with the next full dataset refresh. Full note in `docs/cagr-todo-31aug.md`. | Not applicable, it is a request |

## 01-Sep-2026, GMV and TPV combined sheet

| File | Rows | What it is | Read by the engine |
|---|---|---|---|
| `raw/2026-09-01_gmv-tpv-combined.csv` | 101 | Company-reported GMV and TPV, latest annual, with the issuer's own metric name, fiscal period, local-currency value, period-average FX and the USD figure. Transcribed from screenshots because the source workbook lives in another sandbox and cannot be exported. **Every row verified by `tools/check_gmv_tpv_transcription.py`: usd = local x fx holds on 101 of 101.** | Not yet, raw |
| `raw/2026-09-01_full-refresh-p01..p11.png` | 507 | The full listed refresh, as images. NOT transcribed. Held as the record of what was shown on 1-Sep pending a transfer route. | No |

## 01-Sep-2026, the full listed refresh

| File | Rows | What it is | Read by the engine |
|---|---|---|---|
| `raw/2026-09-01_listed-full-refresh.csv` | 509 | The complete listed pull, recalculated by Daniil from fiscal-year figures and calendarised by hand, with the CY+1/+3 revenue CAGR and the FY+1 broker estimate count both new. Transcribed from screenshots because the source workbook is in another sandbox and cannot be exported. Checked by `tools/check_listed_refresh.py`: 1,993 arithmetic identity checks, 44 flagged, 43 of them explained by the sheet rounding gross profit or net income to a whole number, 1 genuine and flagged (U-NEXT AV/gross profit). | Not yet, raw |
| `raw/2026-09-01_full-refresh-p01..p11.png` | - | The screenshots the above was read from, kept as the record. | No |

## 2026-09-01 — Daniil's realigned private transactions (comparison only, NOT wired)

- `data/raw/2026-09-01_private-transactions-daniil.csv` — 148 rows transcribed from 16 screenshots.
  Source has 191 transactions; the screenshots cover 2021-08-24 to 2026-07-09 sorted newest first,
  so 43 rows dated before 24 August 2021 are still outstanding.
- `data/raw/2026-09-01_private-transactions-p01.png` .. `p16.png` — the raw screenshots, untouched.
- Status: **NOT WIRED and must not be wired.** This file exists to be compared against
  `data/private-rounds.csv` and `data/private-rounds-consumer.csv`, not to replace them.
- Self-check: 146 of 148 rows tie post-money / revenue = multiple. The two that do not are
  Gorillas Oct-21 (multiple computed off pre-money) and Perplexity Jan-24 (multiple taken at the
  bottom of a stated 5m-10m range while the revenue cell shows the top).
- Result of the comparison: `docs/private-reconciliation-1sep.md`. 95 rows match on company and
  month, 55 agree outright, 19 disagree on a number (17 of them denominator only), 21 are rows he
  prices and we do not. 52 of his rows are new to us, 45 of them new companies. Eight decisions
  are open before anything merges.

## 2026-09-02 — the 19 disagreements checked against live sources

- `docs/private-verdicts-2sep.md` — per-row verdict with the URL and the verbatim sentence that
  decided each. Ours right in 16 of 19, Daniil's in 1 (Replit), neither in 1 (Notion), Wolt open.
- `tools/apply_reconciliation_verdicts_2sep.py` — applied four changes to `data/private-rounds.csv`:
  Replit Sep-25 revenue 100 to 150 and 30.0x to 20.0x (we misread our own cited source);
  Notion Jan-26 revenue 500 to 600 and 22.0x to 18.3x with the source moved to Forbes 15-Dec-2025;
  AlphaSense Sep-23 source only, from a TechCrunch piece that carries no revenue figure to the
  CNBC piece that does; Clay Jan-26 source only, from the milestone post to the tender announcement.
- Golden suite deliberately rebaselined: 8 of 43 moved, 2 of them a range (insforge 22.5x to 20.0x,
  skybridge 30.0x to 20.0x, both AI fixtures where Replit and Notion sit in the peer set), 6 only
  re-ordered peers. Now 0 of 43.
- Flagged, not changed: Anthropic May-23 prices on a denominator eight months after the round,
  which breaks our own hindsight rule. The row note says it was done by Daniil's instruction.

## 2026-09-02 — Daniil's rulings applied

- `tools/apply_daniil_rulings_2sep.py` and `..._consumer.py` and `apply_glovo_note_2sep.py`.
- **ALL-STOCK ACQUISITIONS NOW PRICE AT ANNOUNCEMENT.** Daniil's ruling: "need to use the price of
  Doordash AT ANNOUNCEMENT. This is what the seller was pricing when he was setting the price."
  Wolt Nov-21 moves from the audited $2,838m close to the announced $8,100m: 8.2x becomes 23.5x.
  Both numerator and denominator are USD, so no conversion is involved. Glovo has the same
  exposure and its note is updated; it stays record-only only because its denominator is unsourced.
- Perplexity Jan-24 priced as the range TechCrunch reported on the day, $5m to $10m ARR:
  52.0x to 104.0x, headline 52.0x with bound '>='. Was unpriced on "sources conflict".
- Gorillas Oct-21: numbers confirmed and unchanged, both sources added. Found while doing it:
  **`private-rounds-consumer.csv` had no `revenue_source_url` column at all**, so none of its 51
  rows could record where its revenue came from. Column added, empty on 50 rows, populated on
  Gorillas. Filling the other 50 goes on the sourcing list.
- Anthropic May-23 loses its multiple and becomes RECORD_ONLY: no revenue figure was public at
  that pricing, and both candidate denominators post-date the round. Three later rounds inserted,
  each with a run-rate Anthropic disclosed at or before pricing, all from anthropic.com/news:
  Series F Sep-25 $183bn post on over $5bn (Aug-25), 36.6x ceiling, out of medians;
  Series G Feb-26 $380bn post on $14bn, 27.1x point, IN medians;
  Series H May-26 $965bn post on over $47bn, 20.5x ceiling, out of medians.
  Anthropic Mar-25 keeps its $1bn, source upgraded from LinkedIn News to TechCrunch on the day.
- private-rounds.csv 112 to 115 rows.
- Golden deliberately rebaselined: 11 of 43 moved, now 0 of 43. Four delivery fixtures moved a
  range because Wolt is now their high anchor rather than their low: hived mid 10.3x to 23.5x,
  byrd high 10.3x to 23.5x, oda mid 10.3x to 23.5x, 99minutos high 10.3x to 23.5x. Five AI
  fixtures changed peer NAMES only, Anthropic May-26 displacing Anysphere; it is out of medians
  so no range moved.

## 2026-09-02 — the private sheet is COMPLETE at 191 transactions

- `data/raw/2026-09-02_private-transactions-p01..p12.png` — the second screenshot batch, rows 123
  to 195 of the sheet, archived untouched before anything was built on them.
- `data/raw/2026-09-01_private-transactions-daniil.csv` — now 191 rows, matching the sheet's own
  stated count. Rows 123 to 152 overlapped the first batch and EVERY ONE matched what was already
  transcribed. 43 rows were new, running from Carta Aug-2021 back to Buffer Oct-2014.
- Self-check: 189 of 191 rows tie post-money / metric = multiple. The two that do not are the
  already-ruled Gorillas (pre-money) and Perplexity Jan-24 (bottom of a range).
- `tools/check_denominator_monotonicity.py` — NEW, and it closes a to-do the header of
  private-rounds.csv opened on 31-Aug. Across sequential rounds of one company on one basis the
  denominator should not fall; a fall flags a figure attached to the wrong round. Ours: 1 flag
  (Creditas, a real BRL decline). Daniil's sheet: 1 flag, Upgrade Aug-21 160 falling to Nov-21 100,
  which is exactly the defect we had already found and fixed on our side.
- `tools/apply_batch2_verdicts_2sep.py` — four rows moved after independent checking:
  Salesloft Apr-19 priced at 12.0x display-only (was a round with neither valuation nor
  denominator); Trendyol Aug-21 volume multiple 1.65x filled from numbers we already held;
  GOAT Group Jun-21 rounding 1.9x to 1.85x; Anthropic Series D Jan-24 inserted at $18.4bn on the
  $87m run-rate Anthropic itself dates to the start of 2024, 211.5x, IN medians.
- Golden unchanged, 0 of 43.

## 2026-09-02 — data/investors.csv, day 1 of the investors build

- `data/investors.csv` — **368 houses.** 19 carry a CALLABLE layer, 349 an EVIDENCE layer.
  Built by `tools/build_investors_table.py`, gated by `tools/investor_check.py`.
- EVIDENCE layer generated from `private-rounds.csv` and `private-rounds-consumer.csv`: every
  house carries its rounds in our set, its two most recent deals with company, month and the
  round's OWN source URL, and its sector mix in our screening vocabulary. **349 of 349 render.**
- CALLABLE layer seeded from the 19 UK funds in `data-content.js` with cheque ranges parsed from
  their notes. **0 of 19 render**, and that is the design: none carries a dated deal with a
  source URL. The refusals are the pull list, `docs/investor-pull-list-2sep.tsv`.
- Found and fixed while building: **27 houses were split in two by spelling** across the two
  round files (Sequoia / Sequoia Capital, Tiger Global / Tiger Global Management), which
  understated the activity of every one of them. Names now merge on a repeated-suffix stem and
  the collision count is 0. Prose leaking out of the investor cells ("Buyers: Drive Capital,
  Stack Capital Group…") is filtered rather than treated as a house.
- Also fixed today, in `selector/match_reference.py`: `_basis_mix` read `revenue_basis` on rows
  priced on BOOK. Harmless with one lender comp, wrong with two: it would have told a founder
  "these rounds were priced on different measures" when both were priced on book.

## 2026-09-02 — the source columns that were dropped twice

- `data/raw/2026-09-01_private-transactions-daniil.csv` now carries `valuation_source_url` and
  `revenue_source_url` on **191 of 191 rows**, read off the two screenshot batches already in
  `data/raw/`. Applied by `tools/add_sheet_source_urls_2sep.py`, which carries the post-mortem.
- WHAT WENT WRONG, because it is a new failure mode. Daniil sent columns AA and AB twice, on
  1 and 2 September. Both times the multiples in column Y were transcribed off those same images
  and the two source columns beside them were not, because the transcription schema had no field
  to put them in. He was then asked for them a third time. The screenshots were fine and the
  reading was fine; there was nowhere for the data to land, and nothing flagged its absence.
- Rules 1 to 10 of the durability protocol all assume that what arrives is either written down or
  visibly missing. A column that was never in the schema is neither. Hence rule 11.
- The immediate effect: 70 rounds that could not be inserted for want of a source per figure now
  have one. The remaining work on them is ours, tagging each company into the screening
  vocabulary, not Daniil's.

## 2026-09-02 — the callable investor list, generated rather than curated

- Daniil: "Why are we focusing on the UK curated funds? Why only 19? We have a much larger
  database already available from the deal database we own, no?" Right for the stage our data
  covers. **75 EVIDENCE houses promoted to CALLABLE on the activity rule; 73 render.** Yesterday
  the callable list rendered nothing at all.
- A promoted house carries the SIZE OF ROUND IT JOINS rather than a first-cheque range, because a
  first cheque is not something our data knows and inventing one would be worse than omitting it.
  `tools/investor_check.py` accepts either.
- WHERE OUR DATA STOPS, measured rather than assumed: the median round a house in this file joins
  is $267m, p10 is $100m, and exactly 3 of 349 houses appear in any round below $25m, none of them
  currently active. The database is built from priced rounds with a disclosed revenue figure and
  small rounds do not disclose revenue, so seed never entered it. Callable now reads 47 growth and
  crossover, 26 Series B/C, 2 Series A/B, and nothing at seed, which is where our founders are.
- FOUND WHILE DOING IT: **we hold no country field anywhere** — not on the rounds, not on the
  company tags, not on the investor files. Geography is one of the three matching facets and it is
  missing entirely, so every promoted house renders in the broader-fit tier. Added to the pull; it
  also unblocks the region quiz question already queued.

## 2026-09-02 — Daniil's Active Seed & Series A Investor Screen

- `data/raw/2026-09-02_seed-investor-screen.csv` — **88 deal rows, 25 funds, 8 sectors**,
  transcribed from three photographs (`..._seed-investor-screen-p01..p03`). ALL TEN SOURCE
  COLUMNS are carried, per durability rule 11 adopted this morning.
- The screen's own gate, quoted from its Read Me, is stricter than ours: "Funds lacking a
  bounded, fund-stated initial-cheque range or two eligible announcements were excluded." A
  fund-STATED cheque range is exactly what our promoted growth houses cannot supply, so where a
  fund appears both here and in the data-content.js list, the screen wins.
- Loaded by `tools/load_seed_screen.py`. **Callable list goes 73 to 100 renderable houses**, and
  for the first time it has a seed end: 8 pre-seed/seed, 12 seed/Series A, 3 Series A.
- THREE THINGS RECORDED ABOUT THE STRUCTURE, none of them faults:
  1. The two deals are per FUND, not per sector — the Read Me says so. Seedcamp appears in six
     sectors carrying Embedd and EverSettled in all six. A deal proves the fund is ACTIVE; it does
     not prove the sector claim beside it. `deal_evidences_sector` is 0 on every screen row and
     the renderer must not say "recently backed a company like yours".
  2. 15 of 88 deal links point at an INDEX page rather than the announcement: Pale Blue Dot,
     Nina Capital, Heal Capital, FoodLabs, Project A, plus single rows for Skalar and Cordant.
     Usable, weaker than the rest, flagged `source_is_index`.
  3. Cheque size spans a hundredfold in one list: Playfair and FoodLabs from 100k, Eos from 7m,
     Dawn from 10m. Stage bands are derived from the LOW end, because the low end is what tells a
     founder whether the first cheque could be theirs.
- 15 of 88 URLs are marked `url_confidence = LOW`: they are long and small in a photograph of a
  screen. They need a check before they render to a founder.

## 2026-09-02 — the seed screen, version 2, sector-matched

- `data/raw/2026-09-02_seed-investor-screen-v2.csv` — **132 deal rows, 66 fund-sector pairs,
  52 funds, 8 sectors**, transcribed from `data/raw/2026-09-02_seed-screen-v2-p01..p03.jpg`.
  SUPERSEDES `2026-09-02_seed-investor-screen.csv`, which stays as the record of what v1 said.
  `tools/load_seed_screen.py` prefers v2 when present and falls back to v1.
- **THE ONE STRUCTURAL DEFECT IN v1 IS FIXED.** v1's two deals were per FUND, so Seedcamp carried
  Embedd and EverSettled in all six of its sectors and the deal proved activity, never the sector
  claim beside it. v2's gate is "exactly two announcements per fund IN THE NAMED SECTOR", and it
  holds: of the 9 funds appearing in more than one sector, **0 repeat the same deal pair**.
  Seedcamp's B2B row is Embedd and EverSettled, its payments row Nopan and Topograph, its
  delivery row Operent and Sunrise Robotics, its digital-banking row Wanwani and Porters.
  `deal_evidences_sector` is therefore **1** on every v2 row, where it was 0 on every v1 row, and
  the renderer may now say the fund has backed a company in this sector.
- Three structural rules stated in the sheet's own Read Me, all three checked and all three pass:
  fund-sector pairs not carrying exactly two deals **0 of 66**; pairs whose newest sector deal is
  older than 2 Sep 2025 **0 of 66**; cheque-range sources present **132 of 132**. Column K,
  "Initial Cheque Range Source", is new in v2 and is carried as `cheque_range_source`.
- Sector coverage is even: Marketplaces 18 rows, Healthcare 18, the other six 16 each.
- **Callable list goes 100 to 124 renderable houses.** 60 of the 140 callable rows now band at
  seed, 46 of those render, and every one of the eight forks has 6 to 8 seed-capable houses:
  B2B 6, payments 7, banking and lending 6, marketplaces 8, consumer brands 7, delivery 8,
  healthcare 8, insurance 8.
- TWO DATA-QUALITY ITEMS RECORDED, both smaller than v1's:
  1. **3 deal links point at a listing page rather than the announcement** (v1 had 15): QED for
     Skalar cites `skalar.de/presse`, Trucks for Maritime Fusion cites `maritimefusion.com/blog`,
     Nina for IO Health cites `nina.capital/2025-news`.
  2. **2 links are attributed to the wrong house.** Kfund's Pollen row cites
     `paleblue.vc/portfolio/pollen`, which is Pale Blue Dot's own portfolio page, and Felix
     Capital's Lasso row cites a balderton.com announcement. Either both funds were in the round
     and the citation is simply the other lead's page, or the row is wrong. Not resolvable from
     the photograph.
- **88 of 132 URLs are `url_confidence = LOW` and 19 company names could not be read**, because
  these are photographs of a screen at an angle. That is a transcription limit, not a fault in
  the pull. A pasted text version of columns H and J settles both at once.

## 2026-09-02 — the sector screen, area 3's data dump

- `data/raw/2026-09-02_sector-screen.csv` — **51 priced private rounds, 41 companies, 1 Jan 2021
  to 2 Sep 2026**, transcribed from four photographs kept beside it as
  `2026-09-02_sector-screen-p01..p04.jpg`. This is Daniil's answer to area 3 of
  `docs/data-pull-prompts-2sep.md`, the verticals a founder cannot be priced in at all.
  Read-back and checks in `docs/sector-screen-read-2sep.md`. NOT WIRED into the engine yet.
- All 27 source columns are carried, including the three that are empty on every row: pre-money,
  the whole transaction-value block, and **the implied multiple**, which is blank throughout even
  though the tab is named "with Multiples". Durability rule 11.
- Four fields are OURS and are labelled as such: `sector_block_inferred` (the blocks are the row
  order in the sheet, not a column), `url_confidence`, `transcription_note`, and `sheet_row`.
- WHAT PRICES: 32 of 51 give a multiple straight away; 11 more need FX first (five Indian rows
  USD-against-INR, five Octopus rows USD-against-GBP, Voodoo EUR-against-USD); **8 have no
  denominator at all**. Only **21 survive a strict gate** — denominator present, currencies
  already agree, not a floor, not forward, not a part-year figure.
- SIX THINGS RECORDED, none of them guesses:
  1. **Two rows are the same round twice.** Alan EUR 183m at EUR 2,700m post is rows 27 and 50,
     dated four days apart under two different blocks. BetterUp US$300m at US$4,700m post is rows
     37 and 40, the same date written two ways. Dedupe gives 49 distinct rounds.
  2. **Discord's denominator contradicts its own metric**: metric REVENUE 130.0 FY2020,
     denominator 310.0 FY2021. One is wrong or the choice is undocumented.
  3. **Fuse Energy carries a US$5,000m post-money on a US$70m Series B** and neither source is a
     valuation announcement (a Goodwin mandate note and a Sifted raise story). Not loaded.
  4. **eFishery is in the agri block** and its reported figures were later found to have been
     fabricated. Must never be used as a comparable.
  5. **The two emptiest verticals depend entirely on the FX work.** Agri has 6 rows, 5 needing
     INR conversion, and its only FX-free row is eFishery. Energy has 7 rows, 5 needing GBP
     conversion, and its FX-free rows are Enpal (a floor) and Fuse Energy. Both blocks are empty
     until FX is done at the right rate per fiscal year.
  6. **Six of the eight missing denominators look like omissions**, because the metric column
     next door holds a clean number: upGrad 165, LEAD School 80, EGYM 130, Roblox 923.9 (from the
     audited S-1), Epic Games 5,100, Dream Sports 27,060. Only Fireblocks (a reported range) and
     ConsenSys ("nine figures") are correctly blank.
- QUALIFIERS MATTER HERE: 19 of 51 rows carry one — 11 estimates, **7 floors (">"), which make
  the multiple a CEILING not a point**, 2 forward figures, 2 vague ranges. Four more price a
  part-year denominator against a full valuation (Devoted Health H1, wefox four months, MoonPay
  eleven months, BlockFi one month) and need annualising, which is our assumption not the sheet's.
- SOURCING: 22 of 51 rows use the same URL for both figures. Seven lean on tier-4 or worse —
  sacra.com (Virta, Ro), forgeglobal.com (MasterClass, both figures), a CB Insights company page
  (Ninjacart), a personal blog (Vegrow), a French filings aggregator (Doctolib), a press index
  (Restore), and a **staging subdomain** for Dream Sports. Two more are paywalled (The
  Information, both Epic Games rows).

## 2026-09-02 — four private rows held a local-currency denominator under a USD column name

Found while answering "are all the previous private rounds usable". `data/private-rounds.csv`
has a column named `revenue_musd`. Four rows held a figure in BRL or EUR while the stored
multiple had been computed off a USD figure that was never written into the row.

| Row | Was | Now | Where the correct number already was |
|---|---|---|---|
| Creditas Dec-25 | 592.1 BRL | 445.4 USD | Daniil's sheet: "Q3 2025 annualized x4 to USD", 445.4 |
| Creditas Jul-22 | 846.1 BRL | 304.0 USD | this row's OWN note: "US$4,800m / (~US$152m x 2)" |
| Creditas Dec-20 | 78.8 BRL (a QUARTERLY figure) | 56.0 USD | Daniil's sheet: "Q3 2020 revenue annualized x4 from BRL 78.8", 56.0 |
| Jobandtalent Dec-21 | 1,000.0 EUR | 1,130.0 USD | this row's OWN note: "CB Insights translated >EUR1.0bn as >US$1.13bn" |

- **THE SAME CLASS OF ERROR AS THE DROPPED AA/AB COLUMNS.** In three of the four the correct USD
  figure was sitting in Daniil's own sheet and we loaded the local-currency one beside it instead.
  Nothing was derived by us; every replacement is quoted from a file already in the repo.
- **The test is exact reconciliation**: post_money_musd / revenue_musd now equals the stored
  multiple to the second decimal on all four. Across the whole file, rows where the two disagree
  by more than 2%: **0 of 116**, from 4 before.
- Jobandtalent was **in_medians = 1**, so it was live. Its multiple was right, but any renderer
  showing `revenue_musd` would have printed EUR 1,000m labelled US$. The three Creditas rows are
  in_medians = 0, so nothing moved in a median.
- Jobandtalent now carries `fx_rate` 1.1300 and `fx_date` 2021-12-01. Daniil's sheet cites the
  rate source itself, xrates.eu for 1 December 2021.
- STILL OPEN: three Creditas rows carry `fx_ccy = BRL` with no rate and no date. The USD figures
  are now correct and sourced, so no multiple depends on the missing rate, but the conversion is
  not reproducible from the file.
- Applied by `tools/fix_fx_denominators_2sep.py`. Golden suite unchanged, 0 of 43 moved.

## 2026-09-02 — the 63 unloaded rows from Daniil's sheet are now in

WHOOP, Revolut, Stripe, Plaid, Monzo, Chime and 40 more. `tools/load_daniil_sheet_2sep.py`.

- **WHY THEY SAT UNLOADED, plainly: our step, not his data.** His sheet is complete on 191 of 191
  rows. It carries no screening category, and the matcher joins on that field, so every company
  had to be placed in our vocabulary before its round could be selected for anyone. That work was
  queued behind the investor build and the sector screen and should not have been.
- `data/private-rounds.csv` goes **116 to 179 rows, 88 to 134 companies. Median-eligible rows go
  59 to 91.**
- Loaded at `verification = SHEET_02SEP`, NOT VERIFIED. In this file VERIFIED means a human opened
  the source and checked the figure against the sentence in it. These have not had that. The
  figures, bases and both URLs are Daniil's; the categories, bounds and median flags are ours.
- Two new screening categories were needed: **Connected Hardware & Wearables** (WHOOP) and
  **Crypto & Digital Assets** (Blockchain.com, MoonPay). Four more that already existed in
  `tools/load_seed_screen.py` now appear in the rounds file for the first time: Digital Bank &
  Deposits, Insurance, D2C / Consumer Brand, Owned-Inventory Retail.
- **31 of the 63 are held out of the medians**, each with the reason written into its own row:
  13 volume-only metrics (LOANS_ORIGINATED, PAYMENT_VOLUME, OTHER_VOLUME) which produce no revenue
  multiple at all and load into the volume fields; 2 paid-subscriber counts (Calm, Flo Health)
  which load into `paying_users_k`; 10 deposit-taking banks and neobanks held under the standing
  rule that these price on BOOK, never on EV/revenue (Revolut x4, Monzo, Chime x2, N26, Atom Bank,
  Mercury, Qonto); 2 entity-proxy denominators (SumUp Dec-23 "entity proxy", Checkout.com "UK
  entity revenue"); 2 stated proxies (Cohere "ARR proxy", Coalition "annualized GWP / revenue
  proxy" — GWP is premium written, not revenue); and 2 with a basis doubt the sheet states itself
  (Rapyd Jan-21 "unclear whether closed", Tipalti Dec-21 "annual period not specified").
- **Kriya Oct-25 is loaded and held out**: post-money 7.5 against revenue 12.6 gives 0.60x. A
  US$7.5m post-money on a company with US$12.6m of revenue is unlikely; the post-money is probably
  in a different unit. Needs Daniil's confirmation.
- Arithmetic across all 179 rows: post-money over revenue disagrees with the stored multiple by
  more than 2% on **0 rows**. in_medians = 1 rows missing a multiple or a URL: **0**.
- **GOLDEN SUITE: 1 of 43 profiles moved**, the first movement in a long time, and it is a real
  improvement. "honestly" picked up Contentsquare as a fourth comparable; midpoint 14.0x to 28.0x,
  tag evidence 0.6 to 0.9, closeness THIN_OVERLAP to PARTIAL_OVERLAP. Snapshot regenerated
  deliberately with `selector/golden.py --write`.
- **Only 1 of 43 moved because our fixtures do not cover these verticals.** The 43 frozen profiles
  are seed-stage B2B software, delivery and marketplace companies; these 63 rows are fintech,
  banking, payments, crypto, insurance and consumer. The data is not unused, it lands where the
  fixture set does not test. That is another argument for the 43 to 100 fixture march.
- STILL OPEN: six older rows carry no screening category and are in the medians (Airwallex,
  Loadsmart x2, Creditas Jan-22, Jobandtalent, Fundbox), all at SOURCED_31AUG.

## 2026-09-02 (later) — 189 of Daniil's 191 rows are now in, and the two that are not are the same rounds

`tools/fix_load_gaps_2sep.py`. Two fixes.

**FIX 1, MY BUG.** `tools/load_daniil_sheet_2sep.py` deduplicated on COMPANY rather than on
company AND round, so any round belonging to a company we already held was silently skipped. Six
rounds were lost and are now inserted: Airwallex Nov-21 (Series E1, $5.5bn, run-rate 100, 55.0x),
Deel May-22 (Series D extension, $12bn, ARR 295, 40.68x), Perplexity Jul-25 ($18bn, run-rate 150,
120.0x), Ramp Jul-25 ($22.5bn, run-rate 700, 32.14x), Ramp Aug-21 (Series C, $3.9bn, run-rate 100,
39.0x), and Whatnot Jan-25 (Series E, $4.97bn, GMV 3,000, 1.66x) into the consumer file.

**THE ONLY TWO OF HIS 191 ROWS NOT PRESENT ARE THE SAME ROUNDS UNDER DIFFERENT DATES**, both
deliberate and both documented in the rows themselves:
- **Figma 16-May-2024** is our Jul-24 row. Same Axios URL. We re-dated from tender LAUNCH to tender
  CLOSE, which is the honest date for a tender. Same $12.5bn, same $700m ARR, same 17.9x.
- **Canva 23-May-2024** is our Apr-24 row. Same Forbes URL. We withdrew the multiple over two
  recorded defects: the $26bn secondary COMPLETED in early April 2024 and there is no May-2024
  Canva share sale, and the 2,300 denominator matches no published figure. Canva's own number is
  "more than US$2.2 billion in annualised revenue", published 24-May-2024, six weeks AFTER the sale
  closed; the A$3.3bn in the same sentence is the AUD translation of that US$2.2bn, which is where
  both the phantom 2,300 and 3,300 come from. **DANIIL'S CALL:** price it at 11.8x off the $2.2bn
  and accept a denominator published six weeks after closing, or leave the multiple withdrawn.

**FIX 2, DANIIL'S RULING.** "Even if this is a finance company, if the revenue or ARR was cited for
it in the press release, this is how the round was priced and this is what our data needs to
reflect." Fifteen rows I had held out on my own judgement go back in: the ten deposit-taking banks
and neobanks (Revolut x4, Monzo, Chime x2, N26, Atom Bank, Mercury, Qonto), the two entity-proxy
denominators (SumUp Dec-23, Checkout.com Dec-23), the stated ARR proxy (Cohere Jun-23), and the one
basis doubt (Rapyd Jan-21).

**NOTHING IS LOST BY THIS, and it does not contradict the lender rule.** `is_balance_sheet` in
`selector/match_reference.py` picks the pricing basis from the FOUNDER'S archetype, not the
comparable's. A lender founder is still priced on book. Revolut's revenue multiple simply becomes
available to the payments and fintech founders who are priced on revenue, which is what the round
itself was priced on.

**WHAT REMAINS OUT OF THE REVENUE MEDIANS IS ARITHMETIC, NOT JUDGEMENT:** 13 volume-only rows
(LOANS_ORIGINATED, PAYMENT_VOLUME, OTHER_VOLUME) which carry no revenue denominator and whose
multiple lives in `ev_volume_x`; 2 subscriber counts (Calm, Flo Health); Coalition Jul-22,
RECLASSIFIED to a volume multiple because annualised gross written premium is the volume flowing
through an insurer's book, the analogue of GMV, not the insurer's revenue; and Kriya Oct-25, held
pending Daniil because post-money 7.5 against revenue 12.6 gives 0.60x and the post-money is
probably in a different unit.

**State: 184 rows, 111 median-eligible** (59 this morning, 91 after the first load). Arithmetic
disagreements between post over revenue and the stored multiple: 0. Median rows missing a multiple
or a URL: 0. Golden suite 0 of 43 moved, because the fixtures still do not cover fintech, banking
or payments.

## 2026-09-02 (night) — three rulings, three new rules, one check that makes silence impossible

**RULE D12, THE ROW-ACCOUNTING CHECK.** `tools/check_raw_coverage.py`. Every row Daniil supplies is
now accounted for BY NAME: loaded, or listed in that tool's EXCLUSIONS with a reason a stranger
could audit. It matches on company PLUS year-month, never on company alone, because company-alone
matching is the exact bug it was written to catch. It must pass before any commit that touches a
data file. Current state: **supplied 191, loaded 189, excluded with a written reason 2,
UNACCOUNTED 0.** The rule generalises: any operation that reduces a supplied set, a dedup, filter,
join, merge or promotion pass, must report count in, count out, and name what fell between. If it
cannot name what it dropped, it is not allowed to drop it.

**RULE D11** (schema carries every source column) and **RULE D13** (commit with `git add -A`, never
a hand-written file list) written into `docs/RULES.md` alongside it. D13 exists because a commit
block was skipped and `tools/load_daniil_sheet_2sep.py` and `docs/sector-screen-fix-prompt-2sep.md`
never reached the repo even though the data they produced did.

**CANVA Apr-24, PRICED ON DANIIL'S RULING** to use the number the company itself published. Canva
said "more than US$2.2 billion in annualised revenue" on 24-May-2024. 26,000 / 2,200 = **11.8x**,
carried as a CEILING because "more than" makes the denominator a floor, with the six-week gap
between the April close and the May publication recorded in `denominator_basis`. The earlier
withdrawal stands corrected: the objection was to the phantom 2,300, which is the AUD translation
A$3.3bn from the same sentence, not to Canva's own US$2.2bn.

**TWO MORE OVER-CAUTIOUS HOLDS REVERSED.** Plaid Apr-25 (12.2x) and Alan Sep-24 (8.2x) were held out
of the medians only because their denominators are thresholds. A ceiling is usable and the `bound`
field already says so. Same error as the neobank holds.

**THE LENDER RULE IS BEING RECONSIDERED**, on Daniil's ruling that public banks trade on book with
an EBITDA cross-check while private neobanks are priced off ARR. Spec at
`docs/lender-fork-revision-2sep.md`. The evidence is stark: we hold **ONE** private book multiple
(Zopa 5.6x) against **16 median-eligible revenue or ARR multiples** in the finance archetypes. The
lending fork has therefore been pricing founders off a single comparable, which breaks our own rule
that we never price off one comp, and the reason was scarcity rather than judgement: until today
the neobank rows were not loaded. Digital Bank & Deposits now holds **11 rounds, median 15.0x,
range 4.7x to 51.9x**, and the spread is the rate cycle, 2021 vintage at 26x to 52x against 2023-25
at 4.7x to 20.5x, so the range must split by vintage rather than average across it.

**YESTERDAY'S RECONCILIATION VERDICTS ALL STILL HOLD.** The 19 disagreements were decided on one
principle, that a multiple uses the revenue investors had AT PRICING and never a later actual.
Nothing ruled since touches that principle. Ours stood in 16, Daniil's in 1 (Replit, 150), neither
in 1 (Notion, 600), and Wolt was settled by the announcement-price ruling.

**State: 184 rows, 114 median-eligible.** Arithmetic disagreements 0, median rows missing a source
0, golden suite 0 of 43 moved.

## 2026-09-02, evening: sector screen fixed version

- `data/raw/2026-09-02_sector-screen-fixed.csv` — 49 rows, 41 columns. Transcribed from six
  screenshots of Daniil's fixed "Priced Private Funding Rounds - Sector Screen". The 51-row original
  `2026-09-02_sector-screen.csv` is untouched and stays as the record of what arrived first.
  Row accounting: 51 in, 2 dropped (Alan May-2022 and BetterUp Oct-2021, each a duplicate of a row
  that survived), 0 added, 49 out. Balances.
  INCOMPLETE BY DESIGN: columns AC to AF of the source sheet were not visible in any screenshot and
  are not transcribed. The file's own header says so. Owner: Daniil to supply those four columns.
- NOT WIRED INTO THE ENGINE. All 49 rows are named in `EXCLUSIONS` in `tools/check_raw_coverage.py`
  with a written reason, so the file is inside the row-accounting guard rather than outside it.
  Remove an entry when its row is loaded.
- `docs/sector-screen-fixed-verdicts-2sep.md` — what was checked, what recomputed, and six findings.
- `data/private-rounds.csv` — wefox Jul-22 and Alan Sep-24 set to `in_medians = 0` under D6, because
  Daniil's two sheets disagree on their denominators. Median-eligible 114 to 112. Row count unchanged
  at 184. Reversible: set `in_medians` back to 1 and delete the note.

### 2026-09-02, later: Daniil's rulings applied

- `docs/sector-screen-rulings-2sep.md` — seven rulings and what each one did.
- `data/private-rounds.csv` — both D6 holds released. Wefox Jul-22 back in the medians unchanged at
  14.06x (dispute resolved in the engine's favour). Alan Sep-24 CORRECTED: revenue 550.000 to
  500.000, multiple 8.18 to 9.00, bound `<=` to `>=`, back in the medians. The USD 550m appeared in
  no source; TechCrunch, cited by both sheets, says ARR expected to reach EUR450m, around USD500m.
  Median-eligible 112 back to 114. Row count unchanged at 184.
- `tools/check_raw_coverage.py` — all 49 sector screen exclusion reasons rewritten to carry the
  ruling that now governs each row. 44 cleared to load, 2 held, 3 out.
- Columns AC to AF: Daniil confirms they are hidden deliberately and are not needed. D11 flag withdrawn.
