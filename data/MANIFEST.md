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
| earlier | Listed consumer commerce | 71 | not recorded | `data/peers-ecommerce.csv` | yes |
| earlier | Private rounds, software and fintech | 99 | not recorded | `data/private-rounds.csv` | yes |
| earlier | Private rounds, consumer | 50 | not recorded | `data/private-rounds-consumer.csv` | yes |

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
