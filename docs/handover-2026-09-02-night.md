# Handover to Fable, 2 September 2026, night

Pilot launches the week of **21 September 2026**. Nineteen days. Repo
`DaniilRybak-code/fairway-valuation`.

This handover is written to be audited, not believed. Every number below names its file and
reproduces from a command you can run. Section 2 is the audit route. Read section 4 first if you
read nothing else.

---

## 1. What state this describes

**Last commit on `main`: `5bfedb40be43225a7da0ef48abc8ef4ed518ddab`**, 2 Sep 22:33 UTC,
"Sector screen fixed version transcribed and verified...".

**Five files are changed on Daniil's machine and are NOT in that commit.** Verified by hashing each
local file as a git blob and comparing to the tree at `main`, since no git command may be run on his
machine through the bridge:

| File | Local blob | In repo | State |
|---|---|---|---|
| `data/private-rounds.csv` | `d7c528d` | `36de694` | modified |
| `data/MANIFEST.md` | `f5f9419` | `ef51e89` | modified |
| `tools/check_raw_coverage.py` | `52e0ac7` | `5fde89b` | modified |
| `data/raw/2026-09-02_sector-screen-fixed.csv` | `9e0e16a` | `068bb1f` | modified, comment block only |
| `docs/sector-screen-rulings-2sep.md` | `36974d4` | absent | new |

So `5bfedb4` captures the sector screen transcription and the verdicts, but **not** Daniil's rulings
or the Alan and wefox corrections. Until this lands, the repo shows wefox and Alan held out of the
medians at 112 and the working tree has them back in at 114. Commit still owed:

```
git add -A
git commit -m "Apply Daniil's sector screen rulings; correct Alan Sep-24 to 500m ARR and fix its bound direction; release both D6 holds; medians back to 114"
git push
```

---

## 2. How to audit today's work

Run these four in order. Expected output is stated so a mismatch is obvious.

```
python3 tools/check_raw_coverage.py
```
Expect PASS, and two blocks: the 191-row private sheet at 189 loaded, 2 excluded, 0 unaccounted;
and the 49-row sector screen at 4 loaded, 45 excluded in writing, 0 unaccounted. **Every one of the
49 sector screen rows is named in `EXCLUSIONS` with the ruling that governs it.** Read those reasons
rather than the summary line; they are the audit trail for section 3.

```
python3 selector/golden.py
```
Expect `0 of 43 profiles moved`. This is a regression snapshot, not a coverage measure. It says no
edit today changed any fixture's answer. It does not say the data is unused, and it does not say the
data is good.

```
python3 tools/data_inventory.py
```
Expect 2,706 rows across 21 files, and the foot naming `investors.csv` (408 rows) and
`private-rounds-master-30aug.csv` (58 rows) as NOT READ BY THE ENGINE. Both are unchanged today.

Row-level checks on `data/private-rounds.csv`: 184 rows, 114 with `in_medians = 1`, post-money over
revenue equals the stored multiple within 2% on every row (0 failures), and no `in_medians = 1` row
lacking a multiple or either URL (0).

To audit the sector screen transcription itself, the six source screenshots are committed at
`data/raw/2026-09-02_sector-screen-p0*.jpg`. Every figure in
`data/raw/2026-09-02_sector-screen-fixed.csv` was read off those images. The arithmetic ties, which
is the strongest evidence the reading is right, but three cells were visibly truncated and the fx
source URLs were read from wrapped cells; all of these are marked in the `transcription_note` column.

---

## 3. Delivered today, and where to check each item

**The fixed sector screen, transcribed.** `data/raw/2026-09-02_sector-screen-fixed.csv`, 49 rows,
41 columns. The 51-row original is untouched; raw files are append-only. Row accounting under D12,
matched on company plus year and month, not on sheet position: **51 in, 2 dropped, 0 added, 49 out,
balances.** The two dropped rows are the duplicate Alan May-2022 and the duplicate BetterUp
Oct-2021, both named in the file header. Worth knowing: the first run of this match used the sheet's
own row numbers and gave a wrong answer, because deleting two rows renumbers everything below them.
Matching on the row rather than the position is the whole of D12.

**Verification of that file.** 47 multiples recompute with 0 mismatches. 14 currency conversions
recompute with 0 mismatches, each carrying a rate, a date and a source. The denominator is restated
into the valuation's currency on every row, never the reverse. The sheet's own header counts are all
true. Written up in `docs/sector-screen-fixed-verdicts-2sep.md`, six findings.

**Live source checks.** Confirmed against primary sources: Ninjacart INR 747.6 crore FY21 revenue
from operations; Roblox $923.89m FY2020; Fireblocks revenue "between $50 and $100 million" for 2021
with the CEO declining a figure; Discord's 2020 revenue at $130m. Found wrong: Dream Sports and
WayCool use total income where the same source states revenue from operations, and LEAD School's
INR 600m does not tie to the Rs 57.1 crore operating revenue in the RoC filings. Could not read:
the Forbes India page cited for LEAD School returns 403.

**Daniil's seven rulings, applied.** Recorded in `docs/sector-screen-rulings-2sep.md` with what each
one did. Two need Fable's attention because they were not applied as literally given:

- **Discord was not dropped.** His instruction to drop was conditional on there being no matching
  denominator. There is one. The round priced 15 September 2021, so the last completed year at
  pricing is FY2020 and $130m is correct; the $310m FY2021 figure is a later actual, which his own
  ruling 5 forbids. Loaded at 115.4x with the basis label corrected. He has been told and can still
  overrule.
- **Vegrow was held, not accepted.** He asked whether the personal blog belongs to founder or
  management. The author does appear to work at Vegrow, but the page claims no authority, cites a
  third-party aggregator, and gives its revenue figure with **no year attached**. The sheet pins it
  to FY2023 on no stated basis. Held until a dated source exists.

**Two engine rows corrected after the sector screen cross-checked them.** This is the part worth
copying into your own notes, because the sector screen turned out to be a check on the engine and
not only new evidence.

- **wefox Jul-22**: dispute resolved in the engine's favour. Unchanged at 14.06x on FY2021 revenue
  of $320m. The sector screen's four-month $200m stub is the weaker basis and is inconsistent with
  its own wefox Series C row.
- **Alan Sep-24**: dispute resolved against the engine. The engine carried USD 550m ARR, a figure
  that appears in no source. TechCrunch, cited by both sheets, says ARR is expected "to reach
  €450 million (around $500 million) this year". Corrected to 500, so 8.18x becomes **9.00x**. The
  `bound` also flipped from `<=` to `>=`: the denominator is a forward year-end expectation, not a
  "more than" threshold, so 9.00x is a floor and the old value was telling founders "at most 8.2x"
  when the true trailing multiple is higher. Wrong direction, now right.

**The row-accounting check now guards two supplied files instead of one.**
`tools/check_raw_coverage.py` gained the sector screen as a source, a date parser that handles the
three date shapes these sheets arrive in, and 49 named exclusion entries.

**Sector screen disposition: 44 cleared to load, 2 held, 3 out.** Cleared is not loaded. All 49 rows
are still only in the raw file. **The load into `data/private-rounds.csv` has not been started.**

---

## 4. Read this first: 58 priced rounds are in the file and not in the engine

Found late tonight while checking the numbers for this handover, not while looking for it.

`data/private-rounds.csv` holds 184 rows. **The engine loads 126 of them.** Fifty-eight rounds,
**44 of them carrying `in_medians = 1`**, never reach a founder.

The cause is a silent join. `selector/match_reference.py` joins `private-rounds.csv` to
`data/private-companies-tags.csv` on the company, and any round whose company has no tag row is
dropped without a word. The correlation is total, not partial:

- Of the 93 companies that DO reach the engine, **0** are missing from the tags file.
- Of the 41 companies that do NOT, **41** are missing from the tags file.

Reproduce:

```
python3 - <<'PY'
import sys, csv, io, re
sys.path.insert(0,'selector'); sys.path.insert(0,'.')
import match_reference as M
def ck(n): return re.sub(r'[^a-z0-9]','',(n or '').lower())
def load(p):
    return list(csv.DictReader(io.StringIO(''.join(l for l in open(p) if not l.startswith('#')))))
f = load('data/private-rounds.csv')
eng = {(ck(r['company_name']), r['date'].strip()) for r in M.private}
missing = [r for r in f if (ck(r['company_name']), r['date'].strip()) not in eng]
print('file %d | engine %d | missing %d | of those in_medians=1: %d'
      % (len(f), len(f)-len(missing), len(missing),
         sum(1 for r in missing if r['in_medians'].strip()=='1')))
PY
```

The 44 median-eligible rounds that are lost, by screening category:

| Category | Rounds lost |
|---|---|
| Digital Bank & Deposits | 10 |
| Merchant Acquiring & PSP | 8 |
| Vertical Software | 5 |
| Cybersecurity | 4 |
| Personal Software / Productivity | 3 |
| Financial Data | 3 |
| Cloud & Infrastructure Software | 2 |
| D2C / Consumer Brand | 2 |
| Insurance | 2 |
| Crypto & Digital Assets | 2 |
| Connected Hardware, Owned-Inventory Retail, Marketing | 1 each |

Names include Revolut (four rounds), Monzo, Chime (two), N26, Atom Bank, Mercury, Stripe (three),
Checkout.com, SumUp (two), Mollie (two), Rapyd (two), Plaid (two), Fireblocks (two), Chainalysis
(two), MoonPay, Blockchain.com, Brex (two), Carta, Calm (three), Alan and wefox.

**Three consequences, all of which change what was reported earlier today.**

1. **The lending fork revision was specced on a number the engine does not have.**
   `docs/lender-fork-revision-2sep.md` and this morning's handover both state that Digital Bank &
   Deposits "now holds 11 rounds with a median of 15.0x". `tools/data_inventory.py` shows the engine
   holding **4**. Ten median-eligible neobank rounds are among the 58. The vintage split that spec
   is built on cannot be computed from what the engine can see.

2. **Today's Alan and wefox corrections do not reach a founder.** Neither company has a tag row, so
   both rounds are in the 58. The work was right and it is inert until the tags exist.

3. **"114 median-eligible" is not what the product prices.** The engine prices **70** of those 114
   from this file, plus the consumer file. Every handover that has quoted the median-eligible count,
   including this morning's and my own earlier messages today, has been quoting the file rather than
   the engine. That is precisely what D8 exists to stop: a figure in the file but not in the engine
   is ABSENT, not pending.

**The fix is small and the check is smaller.** Add tag rows for the 41 companies, which is a data
job of a few hours and needs no ruling, then make the join loud: it must report count in, count out,
and name what it dropped, which is D12 generalised and is already the rule. I have not started
either, because it changes what every fixture sees and that belongs in one deliberate commit rather
than at the end of a long session.

---

## 5. The roadmap to launch: done, and remaining

Against the plan in `Fairway_roadmap_2026-08-31.md`. Nineteen days to the pilot week.

### Week 1, to Friday 5 September: clean data, working matcher, fixture march

| Item | Status |
|---|---|
| Quarantine the five disputed private rows | **DONE** 31 Aug, by ruling rather than quarantine |
| Matcher drop fix, 14 held versus 3 surfaced | **DONE** 31 Aug. No fixture returns an empty listed lane |
| TPV pull and volume overlay | **DONE** 31 Aug. 268 rows, 63 usable |
| Multi-round closeness selection | **DONE** 31 Aug, `MULTI_ROUND_SPREAD = 3.0` |
| Twelve FX-pending volume figures | **DONE** 31 Aug |
| Private set completed and reconciled | **DONE** 2 Aug morning. 184 rows from 116 |
| Rules D11, D12, D13 and the row-accounting check | **DONE** 2 Sep |
| Seed investor layer | **DONE** 2 Sep. 408 houses, 124 render |
| Sector screen transcribed, verified, adjudicated | **DONE** 2 Sep tonight. Not loaded |
| Wire the 58-round master file | **NOT DONE**, unchanged since 30 Aug, still missing 14 source URLs |
| **Fixtures 43 to 100** | **NOT DONE. Still 43.** Twenty triaged on 31 Aug, none double-verified |

Week 1 is otherwise complete. The fixture march has not moved in three days and is the gate.

### Week 2, 7 to 11 September: connect, then the service and the shell

| Item | Status |
|---|---|
| Engine to reveal wiring | **BLOCKED** on the 100-fixture gate (E6). Cannot start at 43 |
| Honesty copy placed, reveal field rebuilt with blur-reveal | Not started |
| Reviewer workflow, lead to banker review to commentary in 24h | **NOT SCOPED ANYWHERE.** This is the paid service |
| Legal entity, privacy, retention, terms | Not started |
| Pricing confirmed, payment wired | Not started |

### Week 3, 14 to 18 September: dress rehearsal

Five to ten friendly founders end to end with a real banker review on the clock. Not started, and
depends on every Week 2 item.

### Week 4, 21 to 24 September: pilot

### What actually stands between here and launch

1. **The 58 lost rounds.** New tonight. Cheap to fix, and everything downstream is measured on the
   wrong base until it is.
2. **Fixtures 43 to 100.** 57 to go, each double-verified by two independent agents. Ten working
   days. The pilot gate does not move without it, and it has not moved in three days.
3. **The reviewer workflow.** Still scoped nowhere. It is what a founder pays for.
4. **Geography.** No country field exists on rounds, company tags or investor files. 74 promoted
   investor houses render only in the broader-fit tier because of it, and the quiz region question
   is blocked.
5. **The lending fork revision.** Spec written, not implemented, blocked on listed price-to-book and
   EBITDA for banks which we hold none of, on the unresolved Klarna basis, and now on item 1.

---

## 6. Open decisions for Daniil

Carried from this morning, plus tonight's.

1. **Kriya Oct-25.** Post-money 7.5 against revenue 12.6 gives 0.60x. The post-money is probably in
   a different unit. Held out.
2. **Klarna's basis.** Two rows price on bank net operating income, which is neither revenue nor
   book. Flagged 1 September, still unresolved, still blocking the lending fork.
3. **Fourteen curated investor funds have no dated deal** and do not render. Fill or drop.
4. **NEW: the four Indian rows are inconsistent on basis.** On his ruling of tonight, Dream Sports,
   LEAD School and WayCool load on total income while Ninjacart loads on revenue from operations.
   For Dream Sports and WayCool the operating-revenue figure is stated in the very same source, so
   this is a choice rather than a constraint. He has been offered the like-for-like version, which
   moves Dream Sports to 23.4x and LEAD School to 142.2x. Awaiting a word.
5. **NEW: Vegrow.** Held for want of a dated FY2023 source. Agritech is thin and this row is wanted.
6. **NEW: Discord at 115.4x.** Loaded on the reasoning in section 3. He can still overrule.

## 7. Queued work, in order

1. **Add tag rows for the 41 companies** and make the join report what it drops. Section 4. No
   ruling needed, highest value per hour of anything on this page.
2. **Load the 44 cleared sector screen rows** into `data/private-rounds.csv`. They need screening
   category, subsector and growth band assigning, and each carries its basis note. Remove its
   `EXCLUSIONS` entry as each row lands, so the check stays honest.
3. **Fixtures 43 to 100.** The new 57 must cover fintech, banking, payments, crypto, insurance and
   consumer. Note that items 1 and 2 both add evidence in exactly those sectors, so doing them first
   makes the fixtures meaningful rather than the other way round. Add revenue, basis and period to
   the fixture schema before starting.
4. **Scope the reviewer workflow.** Nothing exists. It is the paid service.
5. **Geography.** No country field anywhere.
6. **Implement `docs/lender-fork-revision-2sep.md`** once items 1 and 2 and the Klarna basis clear.
7. Six older rows in the medians carry no screening category: Airwallex Dec-25, Loadsmart Feb-22 and
   Nov-20, Creditas Jan-22, Jobandtalent Dec-21, Fundbox Nov-21.
8. Three Creditas rows carry `fx_ccy = BRL` with no rate and no date. The USD figures are right, so
   no multiple depends on it, but the conversion is not reproducible from the file.

## 8. Process notes from today

**What the rules caught.** D12 worked twice. Once as intended, when the coverage check refused to go
green until all 49 sector screen rows were named. Once on me, when I ran the row accounting on the
sheet's own row numbers, got a wrong answer because two deletions had renumbered everything below
them, and had to redo it on company plus year and month. That is the exact failure D12 was written
for, made by the person applying D12.

**What D13 caught.** The `git add -A` commit at 18:01 recovered `tools/load_daniil_sheet_2sep.py`
and `docs/sector-screen-fix-prompt-2sep.md`, both of which a hand-written add list had dropped
earlier the same day. The rule paid for itself on its first run. The claim in this morning's
handover that those two files never reached the repo is now out of date and should not be carried
forward.

**What no rule caught.** The 58 lost rounds. They are in the file, in the manifest, tagged as
median-eligible, visible on every inventory run, and silently dropped by a join. D8 says a figure in
the file but not in the engine is reported as ABSENT. Nothing computes that comparison, so nobody
reported it. **The next check to build is the one that compares the file to the engine, row by row,
and fails loudly.** That is a better use of an hour than any other check on the list, and it is the
third of the three candidate checks named at the foot of `docs/RULES.md`.

**A caution on tonight's data.** Every figure in the sector screen file was read off a screenshot.
The arithmetic ties on all 47 multiples and all 14 conversions, which is strong evidence, but it is
not the same as having the file. Three truncated cells and the wrapped fx URLs are marked in
`transcription_note`.
