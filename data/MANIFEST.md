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
