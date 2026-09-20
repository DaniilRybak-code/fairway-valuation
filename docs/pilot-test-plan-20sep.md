# Fairway: the test-run plan before the pilot

**Written by Fable, Sunday 20 September 2026, 21:30 UK.** Daniil merged batch 2 (`main` at `453a013`) and asked what comes next and how to test without doing it blindly. This is the plan. It uses the same test companies the engine is checked against on every run of the suite (the 142 fixtures in `selector/golden_profiles.py`), so every run has an expected answer to compare with.

**Two terms.** A *fork* is the set of extra questions a founder gets at step 3, chosen from what the website says the company is: a lender is asked for its book, a marketplace for what passes through it. A *fixture* is one of the 142 real companies the engine is tested on; each has hand-written tags and a known result.

---

## 1. What "ready for the pilot" means

The launch gate (`Fairway_launch_gate_20Sep.md`, section 7) has seven items. Where they stand tonight:

| gate | what it is | status |
|---|---|---|
| G1 | the engine answers on the live site | passed (`344323e`) |
| G2 | a production smoke test in the suite (check 21) | passed |
| G3 | the field rebuilt and approved | passed (`e143d18`, then batch 2 at `453a013`) |
| G4 | live reveals read by hand on production | **this plan** |
| G5 | dress rehearsal: five to ten friendly founders end to end | after G4 |
| G6 | the fix list decision applied and read with real numbers | needs a ruling (section 5 of this document) |
| G7 | the page's edges: contact email in, legal placeholders off, invoice path | not started |

So the answer to "keep doing test runs?" is yes, but as G4, with a fixed set of companies, fixed inputs and one scorecard, so that each run is judged the same way and written down. Two rounds: round one finds the defects, fixes go in, round two confirms them. Then G5.

---

## 2. The test set: ten companies, one per kind of business

Every company below is a fixture. The expected columns come from tonight's run of check 8 (the peer-universe check) on the hand-written tags: how many listed peers the engine finds in the core set and how many private rounds carry a usable multiple. The live site reads the website with the profiler instead of using the hand tags, so a different count is itself a finding (section 4, check 1).

Use each company's own website at step 2 (search the name; fyle.io is the one already used today). From batch 3 the website comes first and the sector is filled in from the read; change it only if it is wrong, and write down when you did.

| run | company | what it is | fork it should get | expected read (archetype) | listed core | private rounds | why it is in the set |
|---|---|---|---|---|---|---|---|
| 1 | Elentaria | software running commercial operations, B2B | software | Business Applications | 7 | 7 | the strong case: every row should draw |
| 2 | Fundraisly | investor matching run as an agency | software | Marketing & Customer Engagement | 3 | 3 | the thin case: three names each side; the field must say so |
| 3 | Oda | online grocery on its own stock | e-commerce | Owned-Inventory Retail | 7 | 7 | a D2C run that is not fyle; GMV question and row |
| 4 | Bokksu | subscription box of Japanese snacks | e-commerce | Consumer Brand | 4 | 4 | subscription billing on a consumer brand |
| 5 | Inato | marketplace for clinical trial sites | marketplace | Third-Party Marketplace | 7 | 7 | GMV asked separately from revenue |
| 6 | Nursa | per-diem nursing shift marketplace | marketplace | Freelance & Services Marketplace | 3 | 2 | thin private lane: two rounds |
| 7 | Numida | working-capital loans to African small businesses | lending | Lending & Credit | 7 | 7 | a lender: asked for book, not revenue |
| 8 | Payabli | embedded payments for software platforms | payments | Merchant Acquiring & PSP | 4 | 5 | gross before interchange |
| 9 | Hived | electric parcel delivery on its own couriers | delivery | Local Delivery & On-Demand | 7 | 5 | the basket asked separately |
| 10 | Supercritical | marketplace for carbon removal | exchange | Market Infrastructure & Exchange | 3 | 1 | **expected to fail the peer gate**: one priced round, no private lane; the field must say why, not draw a sliver |

Two more, not fixtures, chosen by Daniil:

| run | pick | why |
|---|---|---|
| 11 | a dating app or a streaming or podcast company | the consumer fork (subscribers and users) has no fixture and is untested by the walker |
| 12 | an insurer (Denta is the fixture: AI-native dental insurance) | insurers route to the lending fork and are asked for a book; check that the questions make sense to an insurer |

---

## 3. The inputs: the same figures every time

Use these unless you know the company's real figures, in which case use those and write them down. Fixed figures make the runs comparable and make the arithmetic checkable by hand.

| step | Seed run | Series A run |
|---|---|---|
| 1 stage | Seed | Series A |
| 3 revenue | $600,000 a year | $3,000,000 a year |
| 3 fork extras | give the gross figure (GMV, basket, or gross revenue) at 1.5 times revenue; a lender: book $2,000,000; a marketplace: GMV at 10 times revenue | same rule |
| 3 gross margin | software 80%; e-commerce 45%; marketplace 70%; payments 40%; delivery 25% | same |
| 4 growth, last twelve months | 74% | 120% |
| 4 plan | **two runs per company where time allows**: plan 20% (inside the peers' range, so the regression row draws, with or without the callout) and plan 100% (outside it, so the row is refused with the numbers) | same |
| 5 raise | $1M to $2.5M | $5M to $10M |
| 5 last round | $4,000,000 cap, SAFE, March 2025, $750,000 raised | $12,000,000 pre-money, priced, June 2025, $3,000,000 raised |
| 6 email | your own | your own |

Run the ten companies at Seed first. Then runs 1, 5 and 7 again at Series A (software, marketplace, lender), which is the G4 minimum of three at each stage.

---

## 4. The scorecard: nine checks per run

Answer each one yes or no, and where it is no, one sentence and a screenshot. The screenshot name is the run number and the check number (`run7-check4.png`).

| # | screen | check | what "yes" looks like |
|---|---|---|---|
| 1 | step 2 | the read is right | "We read your site as ..." lands under the website box within fifteen seconds and names what the company sells; the sector it fills in is the one you would have picked; on the field, "Compared as" shows the expected archetype from the table in section 2. If it differs, write both down: this is the profiler disagreeing with the hand tag, and it decides which peers the founder gets |
| 2 | step 3 | the right questions | the extra questions match the fork column in section 2 (a lender is asked for its book; a marketplace for GMV; a brand for GMV and margin). Every "i" opens with "Used for:" and you can tell which figure feeds which row |
| 3 | step 4 | the plan note reads right | the line leads with the annual figure, names the plan or the trailing rate, and the number matches: revenue times (1 + growth) is the run-rate; the twelve-month sum is a little below it |
| 4 | field | the rows that should draw, draw | the core peer set on revenue, the gross-profit row where a margin was given, the private row, the gross or per-unit row where the figure was given; the "Not drawn" line under the field names every missing row with a reason you accept |
| 5 | field | every bar is its own arithmetic | pick one bar: the metric beside it times the multiple beside it equals the ends of the bar (hover the bar; it says the sum). One bar per run is enough |
| 6 | field | the peers are the right names | hover each multiple: would you put these names in front of an investor for this company? Write down any name that does not belong, with the reason. The count should be close to the "listed core" and "private rounds" columns. On the private row every round is a mark; the hollow marks are the rounds set aside (take-privates at seed, the highest and the lowest), and the bar runs between the rest |
| 7 | field | the regression behaves | plan 20%: the row draws, reads "read at your 20% planned growth", says how many names were set aside to improve the fit and what R² was with and without them, and shows the weak-fit callout when R² is still under 0.40. Plan 100%: no row, and the "Not drawn" line says your growth sits outside the peers' range, with the range. Hover the multiple: three columns, peer, forecast growth, multiple, and the names set aside under their own heading |
| 8 | below the field | caveats, fix list, investors | the honesty lines say something true about this set; the fix list names this company's own numbers; the investor table fits the sector and stage, the last column says why each house is there, and no card says your location was not resolved (it is read from where you are). The peer charts are drawn only for a founder who gave no figures |
| 9 | the whole page | would you show this to the founder? | yes or no. If no, the one thing that stops you. This is the check that matters; the other eight explain it |

---

## 5. What is not a test-run finding, and needs a ruling instead

These will show up in the runs but no amount of testing settles them. Each is Daniil's to decide, before the dress rehearsal.

1. **The fix list reads the same for two companies.** It is built from templates: the numbers are the company's own and the peers', the sentences are fixed. See the note sent with this plan for how it works and the proposal (the engine keeps every number, a model writes the sentences from them, with a check that no number appears that the engine did not supply).
2. **Everything is unlocked.** `SERVED_TIER` is `paid` for the test phase (one constant in `api/payload.py`). Before the pilot: which rows are free and which are behind the review. The record says the private lane locks (6 September); Daniil said on 20 September he thought it should be visible. Unresolved.
3. **The private pool is growth rounds.** A seed founder's private row is priced off Series D and later rounds (launch gate, section 4). The SAFE sentence and the marker say so, but the honest fix is a pull of Series A and B rounds with disclosed ARR, which is a bulk-pass decision under rule A12.
4. **Series B has no stage median** (Carta publishes seed and Series A in its text; the Series B figure sits in an interactive page that could not be read). No figure until one is read from the source.
5. **Two open engine questions from batch 2:** a listed EV-to-GMV row (55 listed names carry the multiple); whether an out-of-range regression is drawn with a callout or left off (recommendation: left off).
6. **G7:** the contact email, the legal placeholders in the footer, the invoice path.

---

## 6. How to record a run

Copy the block below into `docs/pilot-test-log.md` once per run (the file is created with this plan), fill it in, and put the screenshots in `docs/test-shots/`. One block per run keeps the record readable and lets the next session act on it without asking.

```
## Run <n>: <company>, <stage>, <date and time>
Inputs: <anything different from section 3>
Read: expected <archetype> / got <archetype>
Listed core: expected <n> / got <n>. Private: expected <n> / got <n>.
Checks: 1 y/n, 2 y/n, 3 y/n, 4 y/n, 5 y/n, 6 y/n, 7 y/n, 8 y/n, 9 y/n
Where no: <check number>: <one sentence>. Screenshot: run<n>-check<k>.png
Names that do not belong: <name: reason>
```

---

## 7. Order of work from here

1. Round one: the ten Seed runs (about four minutes each on the page, ten with the scorecard).
2. The log goes to the session; the defects are fixed in one batch, screenshots for approval, one merge block.
3. Round two: the three Series A runs plus any Seed run that failed check 9.
4. The rulings in section 5.
5. G5, the dress rehearsal, with five to ten friendly founders and the banker read on the clock.
