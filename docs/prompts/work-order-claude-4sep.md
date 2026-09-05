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

## Step 0, and do not skip it

Eighteen fixtures currently fail the gate for want of private evidence, but **not all of them are
sourcing gaps**. A private lane can be short for four different reasons and only two of them are
fixed by finding more rounds:

| reason | fixed by sourcing? |
|---|---|
| there are no rounds in the lane at all | yes |
| the rounds are there but none disclosed a revenue figure | yes |
| the rounds are there and priced, but the set is tiered BROAD, which prices nothing by design | no |
| the rounds are there and priced, but they are held out of the medians by a ruling | no |

Run these two first and read them together:

```
python3 tools/thin_lane_diagnosis.py
python3 tools/peer_universe_check.py
```

The diagnosis asks our own database for the next best comparable in each thin lane. Where it comes
back with a name we already hold, the lane is a matcher or tier question and sourcing will not fix
it. Work only the lanes it confirms as genuine gaps, and say in the handover which ones you skipped
and why.

## The eighteen, with what we already hold

Each row is a real company the engine was tested against. Find rounds for the business as described,
not for the sector word: the sector word already matched and was not enough.

| fixture | what it does | archetype | what its private lane already holds |
|---|---|---|---|
| `agentcard` | debit cards for AI agents | Card Issuing & BaaS | Stripe, Marqeta |
| `apollo-atomics` | compact nuclear microreactors | Owned-Inventory Retail / Design & Engineering | Octopus Energy, Enpal |
| `bizmark` | agentic supply chain optimisation | Commerce Enablement & Fulfilment | WayCool Foods, Ninjacart |
| `clera` | AI agent matching candidates to roles | Freelance & Services Marketplace | nothing at all |
| `finn` | all-inclusive car subscription on an owned fleet | Owned-Inventory Retail / Local Delivery | Quince, Enpal, AG1, Packable |
| `levelten` | marketplace for renewable power purchase agreements | Market Infrastructure & Exchange | Xpansiv, The Zebra |
| `manifold-robotics` | robots-as-a-service for warehouses | Commerce Enablement & Fulfilment | Shiprocket |
| `marble` | autonomous back-of-house for restaurants | Vertical Software | Mews, Guesty |
| `nursa` | per-diem nursing shift marketplace | Freelance & Services Marketplace | Incredible Health, Jobandtalent |
| `osseus` | development platform for robotics | Design & Engineering / Dev Tools | Replit, Writer, Vercel, Docker |
| `paymentkit` | billing that survives a processor shutdown | Commerce & Payments Software | MoonPay, Recharge |
| `payna` | AI licensing agent for regulated industries | Vertical Software | Harvey, Clio |
| `priori-legal` | marketplace of flexible legal talent | Freelance & Services Marketplace | Harvey, Clio, Loadsmart, Jobandtalent |
| `standout` | agentic hiring marketplace | Freelance & Services Marketplace | Jobandtalent |
| `tash` | investment platform for sports and trading cards | Wealth & Capital Markets Platform | Raisin, The Zebra |
| `tsenta` | AI career agent that applies on your behalf | Freelance & Services Marketplace | Shiprocket, upGrad |
| `ultrasonium` | metal additive manufacturing | Owned-Inventory Retail / Design & Engineering | nothing at all |
| `wispr-flow` | voice productivity for writing and meetings | Consumer & Prosumer Software | ElevenLabs, Perplexity, OpenAI, Discord |

Read that last column as the shape of the problem. `finn` holds four consumer rounds and none of
them is a car subscription; `osseus` holds four developer-tool rounds and none of them is robotics;
`priori-legal` holds legal software but no talent marketplace. The lanes are not empty, they are
filled with the nearest thing the engine could reach, which is exactly the failure the pull exists
to correct.

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
