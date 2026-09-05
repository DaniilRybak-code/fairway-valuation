# Work order for Claude, 4 September 2026. Private rounds and investor houses.

**Read this first.** Daniil set the division of labour on 4 September:

- **Private rounds are Claude's own work.** Not a prompt handed to another model. Find the rounds,
  read the announcements, write the file.
- **Public companies: Claude selects the NAMES, Daniil pulls the data.** Claude never touches
  Capital IQ and never sources a listed company's enterprise value, market cap or multiple from
  anywhere else. If a lane needs listed comparables, the names go into
  `Fairway_ticker_request_4Sep.md` and Daniil pulls them.
- **Investor houses are Claude's own work too.** Fund websites and deal announcements are public
  web pages, not a market-data terminal.

Everything below is executable by a Claude session with the repo open. It needs no other model.

---

## Before anything: the standing rules that decide whether the work counts

1. **A figure with no source does not exist** (rulebook C1). Every number carries the URL of the
   page it appears on. A company's own release, a filed account, a regulator's page, or a named
   publication reporting the round. Crunchbase and PitchBook profile pages do not count as the
   source.
2. **Never estimate.** If a round did not disclose revenue, the row does not go in the file. A round
   we cannot price is not a comparable, and an invented revenue is the one error a founder cannot
   detect.
3. **Say what the number is** (rulebook B-series). `revenue_basis` is NET_REVENUE, GROSS_REVENUE,
   ARR, GMV, or REVENUE_FROM_OPERATIONS for Indian filers. `revenue_period` is LTM, FY2025,
   ANNUALISED_Q4 or RUN_RATE, and NOT STATED where the source does not say. Do not normalise
   anything yourself.
4. **The schema is the file's, not yours** (D11). Open `data/private-rounds.csv`, copy its header
   verbatim, and fill every column you can. A column with no value is left empty; a column is never
   dropped because it looked useless.
5. **Raw first** (D1, D2, D3). The output is a new file under `data/raw/` named
   `YYYY-MM-DD_<what-it-is>.csv`, a row in `data/MANIFEST.md`, and the inventory run at the end.
6. **Commit on arrival** (D14). The raw file is committed before it is loaded, analysed or argued
   about. Hand Daniil a `git add -A` block; never run git on his machine.
7. **Count in, count out** (D12). Report how many rounds were examined, how many made the file, and
   name what fell out and why.

---

# Part 1. Private rounds

## The diagnosis is already run. Read it before sourcing anything.

Eighteen fixtures fail the gate for want of private evidence. They do NOT all fail for the same
reason, and one of those reasons is not fixed by finding more rounds. Run at 20:45 UK on
4 September against the current file; re-run if the data has moved:

```
python3 tools/thin_lane_diagnosis.py
python3 tools/peer_universe_check.py
```

### (a) The basis trap, four fixtures. This is the finding that matters most.

`bizmark`, `nursa`, `paymentkit` and `apollo-atomics` each hold two private rounds, both in the
medians, both priced, both tier-compatible, and their private range is still empty. The reason is
`basis_mult`: **a round whose disclosed figure is GROSS revenue cannot price a founder who answers
on NET.** Gross never bands with net, and a fixture carries no revenue answer so it defaults to
NET_REVENUE. WayCool Foods, Ninjacart, Incredible Health, Jobandtalent, MoonPay, Octopus Energy and
Enpal are all gross rows, so for these four founders the lane is full and prices nothing.

Across the file: **71 of 290 private rounds are on a gross basis, and 151 of the 219 priced rounds
are usable by a net-basis founder.**

> **Prioritise rounds where the disclosed figure is NET revenue or ARR.** A gross-revenue round is
> still worth having, because it prices a founder who answers gross, but it will not move any of
> these four fixtures, and adding more of them looks like progress while changing nothing.

Record the basis honestly whichever it is. Never relabel a gross figure as net to make it price.

### (b) Nothing in the lane at all, two fixtures

`clera` (AI candidate matching) and `ultrasonium` (metal additive manufacturing). `ultrasonium` is
marked OUT_OF_MARKET and is not worth hunting; `clera` is.

### (c) The set is too far away to price, one fixture

`tsenta` is tiered BROAD, which prices nothing by design. Only a genuinely closer round raises the
tier, so a loosely related round does not help.

### (d) One usable round where two are needed, eleven fixtures

`agentcard`, `finn`, `levelten`, `manifold-robotics`, `marble`, `osseus`, `payna`, `priori-legal`,
`standout`, `tash`, `wispr-flow`. Each draws a diamond rather than a range. One or two good rounds
each closes the group, and this is where the pull pays best. Check `osseus` first: it holds four
rounds and three are held out of the medians by an earlier ruling.

## Control transactions, added 4 September on Daniil's suggestion

Six companies I proposed as listed comparables turned out to have been taken private or acquired.
That makes them useless as listed peers and valuable as something else: each is a priced control
transaction in a sector where our private lane is thin.

**Rulebook B6 already governs this.** "A control deal prices, but carries its label. A takeover
price includes a control premium that a minority round never gets. M&A anchors mark the field as
labelled diamonds; they do not feed the range." The file already carries `transaction_type` with
nine CONTROL rows and one CONTROL_ACQUISITION, so nothing new has to be built: these load as
labelled anchors, not into the range.

| target | acquirer | value | what it prices | which fixtures it helps |
|---|---|---|---|---|
| Sapiens International | Advent International | $2.5bn, $43.50 a share | insurance software | `evergrove`, `insurf`, `florin`, `denta` |
| Learning Technologies Group | General Atlantic | about $1bn | corporate learning | `honen`, `bloomy` |
| Udemy | Coursera | delisted from Nasdaq, value to confirm | consumer and enterprise learning | `honen`, `wondering`, `befreed` |
| Accolade | Transcarent | $621m | payer-facing care navigation | `insurf`, `evergrove` |
| Confluent | IBM | $11bn, $31 a share, completed 17 Mar 2026 | real-time data infrastructure sold to developers | `projectx`, `osseus`, `orchids` |
| Verint Systems | Thoma Bravo (via Calabrio) | $2bn all-cash, completed | conversation and voice analytics | `wispr-flow`, `dograh`, `akkari` |

**What is still needed for each, and it is the part that makes them usable.** The announced
consideration is the easy half. The row does not price until it carries the target's revenue at the
announcement date, on a named basis, from the target's own last filing before the deal, with the URL.
Do not take a revenue figure from the press release summary unless the release states it.

Set `transaction_type` to CONTROL, and never let one of these feed a range: B6 is a rule, not a
preference, and a control premium quietly inside a founder's range is exactly the overstatement the
honesty layer exists to prevent.

While you are there: **listed corporate learning is being taken private one company at a time**
(LTG, Udemy, and Instructure and PowerSchool before them). That is why `honen`'s listed lane is thin
and it will not get better. Control transactions are the honest answer for that lane.

## What a good row looks like

- **A round announced 2023 or later.** Older rounds price a different market.
- **Revenue or ARR disclosed at announcement**, by the company or in the announcement coverage, with
  the post-money valuation. Both figures from the same date, or the pair is not a multiple.
- **Four to six rounds per gap.** Three good ones beat eight loose ones, and a round that fails any
  rule above is worth less than no round at all.
- **A secondary sale is a mark, not a priced round.** Record `transaction_type` honestly; the engine
  treats the two differently.
- **Watch the entity.** Whose revenue is it, and does it belong to the thing being valued? Flipkart
  India Private Limited and Flipkart Internet Private Limited are five times apart (rulebook B10).

## Output

`data/raw/2026-09-05_private-rounds-claude.csv`, header copied verbatim from
`data/private-rounds.csv`, plus a companion note in the handover naming: rounds examined, rounds
written, and every candidate rejected with the reason (no disclosed revenue, no source, pre-2023,
wrong entity). Then the tag rows for any company we do not already hold, into the matching
`data/private-companies-tags.csv` schema, or the load will drop them in silence.

---

# Part 2. Investor houses

## What is actually missing

The vocabulary fix of 4 September translated the file's sector names into our own, which took
callable cards from 738 to 813 and left no founder with fewer than three houses. What is left is a
narrower gap, and it is real:

| our sector name | callable houses that reach it | what they are |
|---|---|---|
| Consumer & Prosumer Software | 14 | mostly generalists: Accel, Sequoia, Andreessen Horowitz, Index, Dawn, Notion, South Park Commons, Uncork |
| Online Learning | 3 | Founders Factory, Mercia Ventures, SFC Capital |

Three houses is not a call list. A consumer AI app founder handed four multi-stage generalists is
being told something they already knew. **Fifteen specialists per cluster, thirty in total, and a
house we already hold does not count towards the fifteen.**

The founders behind this: `goldfish` (local-first AI memory), `acti` (agentic mobile keyboard),
`welltory` (heart-rate variability tracking), `planeat` (meal planning), `wondering` (gamified
consumer learning), `befreed` (audio learning).

## The bar, and it decides whether a row renders at all

1. **Question zero: does this house write FIRST cheques?** These founders raise roughly $0.5m to
   $20m. Write `CALLABLE` in `layer` only if the fund leads or co-leads pre-seed, seed or Series A
   today. A real but growth-stage house is `EVIDENCE`: it stays in the database and comes off the
   call list. A seed founder told to call Benchmark is worse served than one shown six houses that
   actually write their cheque.
2. **A named, dated deal from the last twelve months with the URL it was read on.** Both
   `recent_deal_1_*` columns are required, dated `YYYY-MM`. Activity is the feature.
3. **`screening_categories` uses OUR sector names, spelled exactly**: `Consumer & Prosumer Software`
   and `Online Learning` for this pull. There is now an alias table in `selector/investors.py`, so a
   near-miss may still translate, but do not rely on it: an unrecognised name still reaches nobody.
   Several can be separated by `; `.
4. **The cheque range is what they publish, never what you estimate.** `first_cheque_low_m` /
   `first_cheque_high_m` in millions with `cheque_currency`, and the page in `cheque_range_source`.
   If they publish nothing, leave both empty and write `NOT PUBLISHED`. The card then says "first
   cheque not published", which is a fact about the fund and reads as one.
5. **`stage_bands` is a hard gate.** Only what the fund states, from `Pre-seed; Seed; Series A;
   Series B`. If it states nothing, leave it empty: silence is not a claim, and an empty cell keeps
   the house eligible while a wrong band removes it.
6. **No contact details of any kind.** No email, phone, partner name, LinkedIn or logo URL. The
   compliance check refuses the row.
7. **The test is a named portfolio company, not a stated interest.** A fund whose site says it likes
   consumer does not qualify; a fund that led a seed round into a named consumer app in the last
   twelve months does.

Education funds that only back schools and universities belong in `EVIDENCE`, not on a call list for
a consumer app: these founders sell subscriptions to individuals.

## Output

`data/raw/2026-09-05_investor-pull-claude.csv`, columns copied verbatim from `data/investors.csv`
(the ones a human pull can fill: investor_key, investor_name, house_type, layer, geographies,
stage_bands, first_cheque_low_m, first_cheque_high_m, cheque_currency, thesis_one_liner,
screening_categories, subsectors, recent_deal_1_company, recent_deal_1_date,
recent_deal_1_source_url, recent_deal_2_*, cheque_range_source, geographies_source, last_verified,
provenance). Then run `python3 tools/investor_check.py` and `python3 tools/investor_coverage.py` and
put both outputs in the handover: the first says which rows can render, the second says whether any
founder is better off.

---

## When both parts are done

```
python3 tools/check_raw_coverage.py
FAIRWAY_NO_GIT=1 sh tools/check_all.sh
```

Then hand Daniil the `git add -A` block. Do not run git on his machine (D10), and do not leave the
work uncommitted overnight (D14).
