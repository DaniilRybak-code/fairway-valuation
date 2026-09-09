# WORK ORDER: enrich the private rounds with growth, and change nothing else

**Written 9 September 2026 for a fresh, search-enabled session. Paste this whole document as the
first message. Repo: `~/fairway-valuation`, origin `main` at `b0396fb`.**

---

## The one sentence

**163 private rounds that price a founder's range carry no growth figure. Find the growth rate for
as many of them as have one on a readable page, write it into three columns that already exist, and
do not touch anything else in the file.**

---

## Why this matters, so you know what you are protecting

Fairway prices a founder against private rounds. When a founder is compared to a round, the engine
would like to say whether that round was for a company growing faster or slower than they are.
Today it usually cannot, because the growth column is empty on three quarters of the rounds that
price.

That gap is also making a founder-facing paragraph misleading. The fix list currently benchmarks a
founder's growth against **listed** companies, whose three-year CAGRs run minus 4 to 52 per cent a
year. Any real seed founder is above that, so almost every founder is told they are at the 100th
percentile. Private rounds are the right yardstick and they are mostly blank. This work order is
what unblocks fixing that.

---

## THE FENCE. Read this before you open a file.

**You are enriching, not editing.** Three columns get filled. Everything else in both files is
untouched, including rows you think are wrong.

1. **The only columns you may write are `growth_pct_at_round`, `growth_band` and
   `growth_band_basis`**, and only on rows where all three are currently empty. A row that already
   carries a growth figure is left exactly as it is, even if you find a better source. If you think
   an existing figure is wrong, write it in the findings document and change nothing.
2. **No other column is written, reordered, renamed, reformatted or re-quoted.** Not the multiple,
   not the revenue, not the notes, not `in_medians`, not the date. If your writer touches quoting or
   line endings on rows it did not change, that is a failed run: fix the writer, not the file.
3. **No row is added and no row is removed.** 320 rows in, 320 rows out, across the two files.
4. **Every figure comes from a page you read, and the page is quoted in the row.** A model is never
   the source of a number. If you cannot find it, that is a result and it gets recorded as one.
5. **Never run any git command in `~/fairway-valuation`.** Not `git status`, not `git diff`. Write
   the files and hand Daniil a paste-ready command at the end. He has lost a session to a lock file.
6. **Report count in, count out, and name what fell between.** If you cannot name what you dropped,
   you are not allowed to drop it.

---

## What "growth" means here, precisely

This is the trap in this job, so read it twice.

`growth_pct_at_round` is **the year-on-year revenue growth rate the company was running at the time
of that round**, expressed as a percentage (write `140` for 140 per cent, not `1.4` and not `2.4x`).

Two conditions, both required:

- **Same measure as the row already prices on.** Look at `revenue_metric` and `revenue_basis` on the
  row. If the row prices on ARR, the growth must be ARR growth. If the row prices on gross revenue,
  the growth must be gross. If the row prices on revenue and the only growth figure you find is for
  bookings, GMV or users, that is **not** a match: record it as not found and say what you saw.
- **Same time as the round.** A round dated March 2024 needs the growth the company was running into
  or at that round, from a source published around then. A 2026 article saying the company has since
  tripled is not the growth at the 2024 round. If the only figure you find is dated more than about
  nine months away from the round, record it with basis `THIRD_PARTY_DATED` and say the gap in the
  quote.

**If the row's revenue figure is a bound** (`bound` column is set, for example "more than $100m ARR"),
a growth rate derived from two bounds is not a rate. Record it as not found unless the source states
the growth rate directly.

---

## The three columns

**`growth_pct_at_round`** — the number, as a plain percentage. One decimal at most.

**`growth_band`** — one of exactly three words, computed from the percentage, not judged:

| band | rule |
|---|---|
| `MATURE` | below 65 per cent |
| `GROWING` | 65 to 162 per cent inclusive |
| `HYPER` | above 162 per cent |

These thresholds are in `selector/match_reference.py` (`BAND_LOW`, `BAND_HIGH`). Read them from the
code rather than trusting this table, and say in your write-up which you used.

**`growth_band_basis`** — one of exactly four words, and the file already uses all four:

| basis | when |
|---|---|
| `DISCLOSED` | the company or the round announcement states the growth rate itself |
| `DERIVED` | you computed it from two revenue figures the source gives, on the same measure, twelve months apart. Show the arithmetic in the quote. |
| `THIRD_PARTY_DATED` | a credible third party states it, or the figure is more than about nine months from the round date |
| `STATED` | a founder or executive states it in an interview without a filing behind it |

---

## Your input

**`docs/growth-enrichment-targets-9sep.csv`** is already in the repo, written 9 September. It is the
exact work list: **163 rows, 135 distinct companies**, every private round that (a) sits in the
medians, (b) carries a revenue multiple, and so prices a real founder's range, and (c) has no growth
figure today. Rounds run October 2014 to August 2026.

It carries, for each row: the source file, `transaction_id`, `company_key`, `company_name`,
`date_iso`, `round_type`, `revenue_metric`, `revenue_musd`, `revenue_basis`, `revenue_period`,
`ev_revenue_x` and the existing `revenue_source_url`, plus five empty columns for you to fill:
`growth_pct_at_round`, `growth_band`, `growth_band_basis`, `growth_source_url`, `growth_quote`, and
`not_found_reason`.

**Start with `revenue_source_url`.** The page that gave us the revenue figure very often gives the
growth rate in the same sentence, and it is already dated to the round. Roughly a third of these
should close without a new search.

---

## Order of work

1. **Read the fence above, then read `docs/RULES.md` sections C and D.** Rule D12 in particular:
   every supplied row is accounted for by name, and silence is never an outcome.
2. **Fill `docs/growth-enrichment-targets-9sep.csv` row by row.** For each row either the three
   growth columns plus `growth_source_url` and `growth_quote`, or `not_found_reason` in plain words
   ("only bookings growth published", "no figure within nine months of the round", "source paywalled",
   "company never disclosed revenue growth"). **Every one of the 163 rows ends with one or the other.
   None is left blank.**
3. **Write the raw file** as `data/raw/2026-09-XX_private-growth-enrichment.csv` (D1: nothing is
   received until it is a file in `data/`) and add its MANIFEST row (D2).
4. **Write one load script**, `tools/load_growth_enrichment_XXsep.py`, that reads the raw file and
   writes the three columns into `data/private-rounds.csv` and
   `data/private-rounds-consumer.csv`. It must:
   - be **idempotent**: running it twice changes nothing the second time
   - **refuse to overwrite** a row that already carries a growth figure, and print any it refused
   - print **count in, count out, count changed, and the name of every row it skipped and why**
   - assert that no column other than the three is different afterwards, and fail if one is
5. **Run the suite**: `FAIRWAY_NO_GIT=1 sh tools/check_all.sh`. Twenty checks, all must pass.
6. **Rebaseline golden if it moves, and attribute every move.** Growth is used for ranking and for
   the band, so some fixtures' picked sets or ordering may change. That is expected. What is not
   acceptable is a rebaseline without a written reason per fixture, in the shape of
   `docs/golden-attribution-9sep.txt`. If golden moves on a fixture you cannot explain, stop and
   report it rather than rebaselining.
7. **Re-run the gate** (`python3 tools/peer_universe_check.py`) and report the before and after.
   It is 124 of 142 today.
8. **Write up** `docs/growth-enrichment-XXsep.md`: how many of the 163 closed, the split across the
   four basis values, the band distribution, every row that did not close with its reason, anything
   you found that looks wrong and did not touch, and the gate and golden movement.
9. **Hand Daniil one paste-ready command** that stages, commits with `-m` messages and pushes, in one
   block, starting `cd ~/fairway-valuation && rm -f .git/index.lock && git add -A && git commit -m ...`
   and ending `&& git push`. Never a bare `git commit`. Never a hand-written file list. Say what
   success looks like on his screen.

---

## What success looks like

- 320 private rounds in, 320 out, across the two files.
- Every one of the 163 target rows either carries a growth figure with a URL and a quote, or a
  reason it does not.
- Coverage on rounds that price rises from 56 of 219 towards something usable. **Do not chase a
  target number.** A well-evidenced 110 is worth more than a padded 160, and a single invented figure
  is worse than an empty column.
- Twenty checks pass. Golden either does not move or every move is attributed.
- No column outside the three has changed on any row.

---

## Two things to flag rather than fix

- Any row where the growth figure you find contradicts the revenue figure we hold.
- Any row where the revenue basis looks mislabelled (a gross figure on a net row, or the reverse).
  These go in the write-up. The basis audit is a separate piece of work and this order does not
  touch it.
