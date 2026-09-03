# Fairway: the one roadmap, 3 September 2026

Fable, after auditing the 3-Sep handover. This MERGES the 31-Aug roadmap, the 2-Sep investors and
recommendations plan, and the new workstreams Daniil named (quiz branch testing, reveal testing,
maths testing, landing tweaks) into a single document. **Eighteen days to the pilot week of
21 September; thirteen working days.** Repo copy: `docs/roadmap-merged-3sep.md`.

---

## 1. Tonight's audit, in one block

The four state commands reproduce exactly: raw coverage PASS with 0 unaccounted, golden 0/43,
inventory 511 listed / 289 private, investor_check runs (with the bug below). The basis audit foot
moved to 117 agreeing / 101 needing a human — agreeing went UP (66 → 117), and the 101 is new-data
workload, not regression. The eight scoped figures, verified from primary sources:

**Six hold clean.** Dream Sports 22.06x (both figures confirmed verbatim from Tofler-sourced
filings). Atom Bank 3.17x (£137.023m consolidated total equity read from the annual report PDF
itself; £435m same entity; tag "pre/post unspecified"). Oura 23.1x (better-than-Sacra anchor
found: the CEO's own December-2024 statement that 2024 sales would double to ~$500m implies ~$250m
for 2023; note a FILED Finnish figure exists on a Sep-year-end — €163.6m to 30-Sep-2023, which
would be 29.7x — flag the basis, do not silently swap). Discord 115.4x (no 2021 figure was public
before 15-Sep-2021 — TechCrunch itself wrote "the revenue record runs dry"; Opus argued the right
way). Konfio 39.23x (the recorded rate is within 0.11% of the Banco de México FIX for 29-Sep-2021;
the worry's premise was wrong; worst defensible alternative moves it to 38.9x). Tala (Forbes
verbatim: "recover to its pre-pandemic level of $60 million per month" — a monthly pace, flag
correct, keep out of medians).

**Two need Daniil.** (1) **Klarna is a convention fight, not an error**: the engine converted at
pricing-date spot, the sheet carries Klarna's OWN press-release USD figures at calendar-average
rates ("1 USD equals approximately… 9.2 SEK for full year 2020", their footnote). Recommendation:
adopt **ECB spot at pricing date** as the standing FX convention — it is the only one that makes a
multiple currency-invariant, and it matches the at-pricing principle. The exact pins: 8.2730
SEK/USD on 10-Jun-2021 → $1,208.8m NOI → 37.7x; 10.5905 on 11-Jul-2022 → $1,298.8m → 5.16x
(Klarna Bank AB figures SEK 10,000.1m / 13,754.5m — the annual reports; record rate, date and
entity in the file, keep Klarna's $1,087m/$1.6bn as a memo column). (2) **LEAD School**: the
₹600m is not a printed figure — it is total income DERIVED as expenses minus loss; the PRINTED,
sourced figure is operating revenue ₹57.1 crore (Entrackr, from the RoC filings), which gives
142.2x. Under our own sourcing rule the printed figure should win. Ruling requested.

**Structural (3c), my answers:** pre-money rows (Starling, Upgrade ×2) — yes, add a
`valuation_basis` flag the honesty layer reads; never silently mixed. Indian total-income vs
ops-revenue — prefer the printed revenue-from-operations wherever it is published (LEAD 142.2x,
Dream Sports 23.4x are both available on that basis); consistency beats convenience. Zilch,
Billie, Pipe loaded unpriced — correct as is; named-never-displacing already covers it.

**Investors roadmap state (section 4) — verified, all three claims true**: 408 houses / 32
columns exist; 140 callable in principle but **52, not 124, pass the six-field render bar** (346
rows lack a cheque range, 342 lack geography); **nothing reads investors.csv** — only its own
build and check tools touch it; and investor_check's sector buckets split with numeric suffixes
("Vertical Software(1)/(2)", "Enterprise Applications(1)-(3)") — a splitting bug masking real
coverage. And the two 1-Sep engine items are still open: **0 of 43 fixtures carry revenue** (the
schema fix never happened — the last two days went into the data crisis), and the dead
`with_forward_revenue` is still in the file.

---

## 2. The critical path, named

Everything below serves one chain: **fixture schema → march restarts → 100-fixture gate → engine
connects to the reveal → dress rehearsal.** The march is 43 of 100 with thirteen working days
left; it has not moved in three days and cannot restart until fixtures carry revenue, basis and
period. Data loading is no longer the constraint — 289 rounds are in. The constraint is testing
and the founder-facing surface.

**A decision only Daniil can make, this week: the gate.** 57 fixtures at two agents each in ~8
usable days means a surge (four-plus verified per day, run as parallel agent pairs, which Opus can
orchestrate) — or a conscious re-scope (e.g. "gate = 75, with every live fork holding at least
five fixtures", written down as a decision, not a slip). Recommendation: surge now, decide at the
Friday-12-Sep checkpoint whether to re-scope. What is not acceptable is discovering on the 18th
that the gate cannot be met.

---

## 3. The workstreams, merged

**A. Engine data hygiene** (Opus, continuous). Apply tonight's verdicts once ruled (Klarna pins,
LEAD, pre-money flag). Build the two checks that earned their keep the hard way: file-versus-engine
reconciliation (rows in CSV vs rows loaded, per file, in data_inventory) and the cross-file
duplicate check (company + month + post-money, never name — AG1 had three spellings). Work the
101-row basis backlog INSIDE the march: every fixture batch audits the rows it touches, so the
backlog burns down where it matters first.

**B. The fixture march and the maths tests** (Opus builds, both agents march, Fable spot-audits).
Schema first — revenue, revenue_basis, revenue_period on the profile; delete
`with_forward_revenue`; re-run the 43 with real inputs so the basis gate and period machinery run
on real numbers for the first time; then march at 6-8/day with expected_peers + the Google test.
The maths test-set rides the same harness: extend the identity checks (post-money ÷ denominator =
stored multiple, already passing on 289 rounds) to the REVEAL arithmetic — midpoint maths, the
±band construction, dilution, bar geometry (a bar's left/width must reproduce from its low/high
against the axis scale), and the run-rate conversion caps. Property tests, not examples: they run
on every fixture automatically. That is what "testing the maths" means here, and it is nearly free
once written.

**C. Investors and recommendations** (Opus; the 2-Sep plan holds, re-sequenced by tonight's
findings). Order: (1) fix the sector-suffix bug — every coverage number is read through it;
(2) reconcile the renderable count and never report 124 again; (3) **ship Layer 2 first** — the
evidence list falls out of the selector with zero curation and is the layer nobody can copy; wire
it into the reveal payload now so investors reach a founder the day the reveal connects;
(4) Layer 1 renders only rows passing investor_check — at 52 that is already enough for the five
launch forks IF the coverage lands where fixtures cluster (the suffix fix tells us); Daniil's
enrichment pull (cheque range + geography for the 88 callable-but-blank rows, and dated deals for
the 14 undated funds) grows it without blocking anything; (5) the recommendations renderer (the
five-dimension read, fix list ordered by range impact) is still not started — it is two build
days and must land before the reveal connects, because "we tell you where we'd take the number"
is promised copy.

**D. Quiz testing across branches** (Opus builds once, machines run it forever). A headless
quiz-walker: enumerate every fork path (seven forks × the branch questions), drive the real quiz
in Playwright, assert every path reaches the reveal handoff with a well-formed payload and no
dead question, and diff the payload fields against what `quiz_fork`/the engine expects — the
live-quiz-versus-fork-spec gap becomes a nightly failing test instead of a to-do. Golden quiz
paths: one recorded input set per fork, snapshotted like fixtures. Cost: about a day to build;
after that, branch coverage is free and every quiz edit is regression-checked.

**E. Reveal testing** (Opus builds the harness, Fable reads the output). A fixture-driven render
harness: for all 43 (then 100) fixtures, render the reveal HTML headlessly, screenshot it, and
assert the honesty strings appear where their range objects say they should. Fable reviews the
screenshot batch the way the landing rounds work — a contact sheet, not forty tabs. Two copy
gaps close inside this workstream: the CONTEXT-tier sentence (still unwritten) and the six
honesty flags that still do not reach a founder.

**F. The landing** (Fable, batched). One weekly round: Daniil marks up screenshots in one sitting
(as v8.0-v8.6 worked), Fable ships one PR. Current queue: whatever the next markup carries, plus
the two-layer investor block once C ships, and the legal placeholders coming out (below). No
mid-week one-off landing edits — they cost a full session each.

**G. The service shell — the biggest unbuilt block, must start this week** (Daniil decides, Opus
builds). Reviewer workflow (lead → banker review → commentary inside 24h — the actual paid
product), the legal entity + privacy + retention placeholders still rendering on the live page,
pricing confirmation and a way to pay. None of it is scoped anywhere. One working session of
Daniil's decisions (entity name, retention period, price, payment rail — Stripe payment link is a
day, not a project) unblocks all of it; the build is mostly wiring.

**How this stays efficient with one human.** Daniil does only the three things only he can do:
**rulings** (one 20-minute batch a day, straight off the tracker's open-decisions list — never
scattered through the day), **pulls** (one CSV batch a day into data/raw, per the protocol), and
**eyeballing** (one screenshot contact-sheet or ten-list review per day). Everything else must be
an automated check or an agent's job. The tests in B, D and E all convert one-off human checking
into machines-run-nightly — that is the whole point of building them now, twelve days before
founders arrive.

---

## 4. The thirteen days

**Thu 4 – Fri 5 Sep.** Fixture schema + rerun 43 · the two new checks · suffix bug + renderable
reconciliation · audit verdicts applied after rulings · march restarts Friday · Daniil: rulings
batch, gate decision, enrichment pull, service-shell decisions session.

**Mon 8 – Fri 12 Sep.** March at 6-8/day with the basis backlog burning inside it · quiz-walker
built and green on all forks · reveal harness + CONTEXT copy + honesty flags to the founder ·
Layer 2 investors in the reveal payload; recommendations renderer built · engine→reveal wiring
started mid-week · reviewer workflow + legal + payment wired · **Friday checkpoint: gate
arithmetic reviewed — surge on, or re-scope, in writing.**

**Mon 15 – Thu 18 Sep.** Dress rehearsal: five to ten friendly founders end to end with a real
banker review on the clock · fix list only · final landing round (investor block, placeholders
gone) · analytics + cookie decision · outreach prep.

**Week of 21 Sep.** Pilot. Daily triage. Nothing new ships but fixes.

---

## 5. Tomorrow, 4 September — in order

**Daniil (one sitting, ~45 minutes, plus one pull):**
1. Rulings batch: Klarna FX convention (recommend ECB spot at pricing date; pins above) · LEAD
   School denominator (recommend the printed ₹57.1cr → 142.2x) · pre-money flag yes/no · the
   handover's open six (Kriya, Vegrz — Vegrow, Fireblocks Jan-22, the 14 undated funds, Indian
   basis convention, Zilch/Billie/Pipe as named-unpriced).
2. The gate decision: surge to 100, or re-scope in writing.
3. The investor enrichment pull: cheque range + geography for the 88 callable-but-blank rows,
   dated deals for the 14 — one CSV into data/raw.
4. Book the service-shell decision session (entity, retention, price, payment) this week.

**Opus (in order):**
1. **Fixture schema — revenue, basis, period — delete `with_forward_revenue`, re-run the 43.**
   Everything else queues behind this; it has been the top item for three days.
2. The two checks: file-versus-engine reconciliation, cross-file duplicate (company+month+value).
3. Investor sector-suffix bug, then reconcile and report the true renderable count.
4. Apply the audit verdicts as rulings land (Klarna pins + rate/date/entity columns, LEAD,
   pre-money flag, Oura source-upgrade note, Atom pre/post tag).
5. If the day allows: start the quiz-walker.

**Fable (next session):** verify the schema fix ran on real inputs (period spans no longer
NO_REVENUE_GIVEN) · verify the two checks catch a planted fault each · read the first
suffix-free coverage table · landing round when the markup arrives.
