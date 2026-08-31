# Handover, evening of 31 August 2026, Opus to Fable

**Three weeks to the pilot. It goes live the week of 21 September, which is 15 working days away.**

Read this against `Fairway_roadmap_2026-08-31.md`, which I have marked up item by item tonight.
Every number below names the file it comes from and the command that reproduces it. Where I got
something wrong today, it is written down as wrong rather than smoothed over.

---

## The one-paragraph version

The data side of the plan is effectively finished, four days ahead of the week-one schedule.
Daniil ruled on all five disputed private rounds, supplied the twelve missing FX conversions, and
landed a 28-name TPV pull that ties to the issuers' own filings to the dollar. The matcher drops
are fixed and no fixture returns an empty peer list any more. Multi-round selection is built under
his ordering. Against that, two findings from checking my own work tonight, and both point the same
way. **No fixture carries a revenue figure**, so today's basis and period machinery has never once
run on real input and the gross branch of the basis gate has never been exercised. And on twenty
companies the engine had never seen, **7 of 20 get no listed range and 13 of 20 get no clean private
range**. The 43 fixtures flatter us twice over: data existed for them, and they only ever tested
peer selection. The pilot risk is no longer data quality. It is that the fixture march is about to
do 57 more of a test that covers half the engine.

---

## Inventory foot, run at close, verbatim (the protocol requires this)

```
WHAT THE ENGINE ACTUALLY LOADS
  listed  511
  private 163

FILES PRESENT BUT NOT WIRED INTO THE LOADER
    private-rounds-master-30aug.csv                 58 rows  NOT READ BY THE ENGINE
```

Private moved from 149 to 163 on the day. Listed moved 513 to 511, because OFX and EML were
dropped tonight for the reason in finding 5 below. The 58-row master file is the only unwired file and it
ends the day exactly where it started, which I flag rather than bury: it still lacks 14 source URLs
and under our own sourcing rule none of its rounds may be shown to a founder until they exist.

Golden suite: `python3 -m selector.golden` gives **0 of 43 profiles moved**. Two things about that
number tonight. It held at 0 across every change made for the rulings, which answers your
rebaselining worry from last night directly: no fixture was leaning on a disputed number, so the old
baseline was honest. It was then **deliberately rebaselined once**, at the end of the day, for the
OFX and EML removal in finding 5. Three fixtures moved, all three named and explained below, and the
0 above is against the new baseline.

---

## What was completed today

Against your own six build items, four are done, one is started, one is blocked on the same input
it was blocked on last night. Against the five things you asked of Daniil, four are done and one is
part done. The marked-up roadmap has the item-by-item detail. The short version:

**The five disputed rows are resolved, not quarantined.** Your instruction was to quarantine first
and ask later, which was right. In the event the rulings arrived the same morning, so the rows were
corrected in place. Zepz takes the round-announcement figure. Marqeta takes contemporaneous Forbes.
Razorpay is out entirely, because we do not hold its denominator at the time of pricing, which
removes a 67.6x gross-revenue number that was dragging the fintech median. Pine Labs keeps one
denominator, the most-cited, with the reason recorded. Better.com keeps the SPAC valuation with its
comment. Loadsmart, Gorillas and Jobandtalent are in.

**Two rulings from today are now standing rules and should be treated as such.** First: a round
announcement beats filed accounts for the same period, because it is the primary source and it is
what the investor actually priced against. Second: revenue scale is the first gate between two
rounds of one company **only** when the multiples are an order of magnitude apart; where the
multiples are similar, take the latest. Everywhere else size stays out of selection. That second
one is narrower than your recommendation and I think it is better, because it keeps the standing
"size never selects" rule intact instead of carving an exception into it.

**Like-for-like basis is wired for the first time.** This is the finding I would most want you to
check. `revenue_basis` has existed on private rows since 27 August and **nothing ever enforced it**.
Razorpay's gross 67.6x sat in the fintech file for four days next to net multiples. There is now a
`basis_compatible()` gate, net-equivalent and gross-equivalent sets, and dual-basis rows carry both.
The gross/net test we settled on is ownership, not size: does the line contain money belonging to
somebody else? A first-party retailer keeps the whole sale price, so its revenue is net in our
sense.

**Period matching is built, and I want to be careful about the word wired, because when I went to
check it tonight it is less finished than I said this afternoon.** The problem is real: every listed
multiple in our files is EV over NTM revenue, every quiz fork asks the founder for a trailing number,
and we were applying a forward multiple to a trailing denominator everywhere, silently. What now
exists is `founder_revenue_for(prof, period)`, which returns the founder's own revenue on whichever
basis a comparable was built on, and every range on both lanes carries `period_mix` and
`period_span` so the reveal can multiply row by row instead of applying one median to one number.
**What does not exist is anything consuming it**, because the reveal is not connected to the engine
yet, and that is by design. See finding 1 below for the part that genuinely worries me.

**The matcher drops are fixed, by three separate changes.** Bands widen until they hold at least
three names and record how far they widened. The listed core tops up from the wide set until it has
three priceable names. A new CONTEXT tier returns the wide set with a disclaimer where the match is
genuinely weak. Five fixtures that previously returned no listed peers at all now return some. One
bug I caught and fixed inside this: the first version of the top-up dragged the tier to BROAD and
**removed** sellerclaw's existing range. Topping up must only ever add evidence, never take it away.

**Volume metrics are usable and fenced.** The overlay is 268 rows, 63 usable and 13 not. A gross
volume may price only where the enterprise value and the volume describe the same thing, which
excludes balance-sheet lenders and any segment volume set against a group valuation. I found and
fixed a hole where the usability flag blocked one door and not the other, so U-NEXT and Digital
Garage were still producing percentages through the back way.

**Hygiene, both items.** Lending market rows and tag rows now agree on the raw ticker string, 79 to
79, so a future naive join will not re-drop the lenders. `nursa` returns a listed range again, 0.7
to 1.2x on three names, as a side effect of the band widening.

---

## Key findings, in the order I would want them read

### 1. The 43 fixtures carry no revenue, so the basis and period work is completely untested

I found this checking my own claim before sending this, and it is the most important thing in the
handover. **Not one of the 43 golden profiles carries a revenue figure.** The key is not even in the
schema they use: a fixture profile has archetype, industry, function, buyer, growth, gross margin,
revenue model and tags, and no revenue.

Reproduce:

```
cd selector && python3 -c "from golden_profiles import PROFILES; \
  print(sum(1 for i in PROFILES if [x for x in i if isinstance(x,dict)][0].get('revenue')), 'of', len(PROFILES))"
```

It prints 0 of 43. Three consequences, and each one bites:

**The period machinery has never run on real input.** Across all 43 fixtures there are 75
`period_span` entries and **every single one says `NO_REVENUE_GIVEN`**. The derivation is correct as
far as I can read it, and it has never once produced a number.

**The basis gate has only ever been exercised on one branch.** `basis_compatible` reads
`prof.get('revenue_basis') or 'NET_REVENUE'`, so with no fixture supplying it, every founder in
every test is net. The gross branch, which is the one that would have caught Razorpay, is untested.

**There is a second, dead derivation of the same number.** `with_forward_revenue(prof)` exists at
line 1093 and has **zero callers anywhere in the repo**. It duplicates what `founder_revenue_for`
does. Two derivations of one number is how they drift apart, and one of them being dead is how
nobody notices. It should be deleted or made the single path, and that is a decision I would rather
you took than I did at this hour.

**What this means for the pilot gate, which is the part Daniil should see.** The gate is 100
double-verified fixtures. Fixtures of the current shape test peer SELECTION and nothing else. They
do not test that a founder's number meets a comparable on the same basis, or on the same period, or
that the multiple applied to it is the right one. **Reaching 100 fixtures of this shape would
certify half the engine and read as though it certified all of it.** I do not think that changes
the gate, but the fixture schema has to grow a revenue figure, a revenue basis and a period before
the march goes much further, or we will do 57 more of the wrong test. Six a day for ten days is a
lot of work to spend on the wrong shape.

Fable, your own check number 4 in the basis brief was "fixtures where a trailing founder figure
meets a forward peer multiple: was 43 of 43, should be 0". The honest answer tonight is that it is
**unanswerable**, not zero. The number the check needs is on the range object now. Nothing supplies
the input that would make it non-null.

### 2. Fresh companies do much worse than our fixtures, and we should say so out loud

I triaged twenty real companies taken from Product Hunt's July, June and May 2026 monthly
leaderboards. Real names, nothing invented, per the standing rule. `tools/triage_20_31aug.py`
reproduces all of it.

What comes back, counted by what the founder would actually see:

| | RANGE | SCATTER | single point | nothing |
|---|---|---|---|---|
| listed lane | 10 | 2 | 1 | 7 |
| private lane | 7 | 7 | 4 | 2 |

So **7 of 20 get no listed range and 13 of 20 get no clean private range.** Two get nothing at all
on either lane, wispr-flow and naptick. Nine build a range on fewer than three names.

The listed sevens are all CONTEXT tier. That is working as designed: the founder sees named context
companies with a disclaimer rather than an empty box, and a weak match correctly refuses to price.
But I want to be precise about what today's fix did and did not do, because it would be easy to
overclaim. It removed the empty peer list. It did not turn those into priced ranges, and it should
not have.

The private sevens that scatter are the more interesting failure. On velo, the set that comes back
is Sierra at 105.3x, Clay at 50.0x, Semrush at 4.3x and Apollo.io at 16.7x. Those are not
comparables, they are a genre. The engine is honest about it, it returns SCATTER rather than a
range, so a founder sees points and no number. But a founder who gets points and no number twice
has not been served, and the honest reading is that our private software set is thin enough that
band widening reaches straight past the useful neighbours into whatever is left.

**The limitation of this batch, stated plainly: Product Hunt is almost entirely software.** All
twenty are software. This tells us nothing about the ecommerce, payments, lending or delivery forks,
which is exactly where the volume-metrics and TPV work landed today. The next triage batch has to
come from somewhere else.

### 3. Twenty different spellings of the same field

`denominator_basis` on the 108 priced private rows carries **20 distinct values**, of which nine are
free-text sentences rather than labels: "Q3 results released on financing close date; closed
quarter", "Reported around round", "Estimate around financing". Alongside them sit
DISCLOSED_ACTUAL, DISCLOSED_EXACT and "Disclosed at pricing", which as far as I can tell mean the
same thing three ways.

Reproduce with:

```
cd selector && python3 -c "import match_reference as M; from collections import Counter; \
  print(Counter((r.get('denominator_basis') or 'BLANK') for r in M.private if r.get('mult') is not None))"
```

Nothing can filter reliably on a field spelled twenty ways. The notes are worth keeping, but they
belong in a notes column, not in the field the engine reads. This wants a controlled vocabulary and
a one-time migration, and it should happen before the fixture march scales, not after.

### 4. Twelve figures were in the file, correctly tagged, and in no valuation at all

This is my failure and it deserves its own heading. Twelve non-USD volume figures sat in
`volume-metrics.csv`, manifested and visible, and never entered a single valuation because nothing
converted them. I reported this as "waiting on an FX ruling". Daniil's response was the correct one:
he needed it flagged as an absence, not filed as a pending decision.

Then, converting them, three of my own figures were wrong by 1,000x or 1,000,000x on the scale
(U-NEXT, Digital Garage, AvenuesAI) and he caught all three.

**The durability protocol as written does not catch this class of failure.** It catches data that
never arrives. It does not catch data that arrives, is recorded correctly, and then silently fails
to be used. I have proposed a ninth rule in the marked-up roadmap: a figure that is in the file but
not in the engine is reported as absent, not as pending, and every data session states by count
which rows entered a valuation and which did not. Adopt it or redraft it, but it needs to exist.

### 5. OFX and EML were killed in conversation and were still pricing an hour ago

I went to confirm this as a carry-over rather than assume it, and found the decision had never
reached the code. Daniil killed both on 31 August ("these are micro stocks, doubt anyone wants to be
compared to them"), and had said of EML the week before, "would simply drop this peer". EML had been
stopped from pricing. **OFX had not, and was sitting in medians with `in_medians` true and
`pricing_eligible` true.**

Worse, the fix that existed for EML was the wrong shape. It stopped the name pricing but still
printed it beside a founder's company as a named peer, and being compared to them is precisely what
Daniil objected to. Both are now dropped from the universe outright, with the reason string kept
against each so no name ever goes silently. Listed count moves 513 to 511.

Three fixtures moved as a result, and all three moved the right way:

- **trolley**, which is the fixture that started this. Its listed core was EML at 0.7x and Corpay at
  6.4x, a ninefold spread from two names. The core is now Corpay, Repay and Usio, and the secondary
  range lifts off the distress multiple from 0.5 to 0.9x, up to 0.7 to 2.1x.
- **dots**. OFX gone from the core, Marqeta in, and the low end lifts from 0.5x to 1.3x.
- **moov**. EML out of the secondary, Nexi in.

Golden rebaselined deliberately after this and back to 0 of 43. **Please check this one, because I
changed a baseline at the end of the day**: the diff is in the repo, the three moves above are the
whole of it, and every one is a low end coming off a micro cap that should not have been there.

The general point is the one Daniil keeps making and I keep proving: a ruling that lives only in a
conversation is not in the product. Everything he ruled on today is written into code or into a
file, and this handover names the file for each.

### 6. Flipkart was wrong in a way our own notes already knew

Our notes said the denominator was the B2B wholesale entity. Nobody acted on it. The result was
6.4x and 5.2x sitting in the ranges when the marketplace entity prices at 34.2x, a factor of six.
Both Flipkart rows are now out of the ranges. The general lesson is worth writing down: a note
recording a problem is not the same as the problem being handled, and we have at least one more of
these in the file (the 42 rows the basis audit flags below).

### 7. Two more things I got wrong today, recorded

My explanation of Wise's negative growth was wrong. I attributed it to interest income decoupling.
The real cause was that Wise reports in USD from FY2026, so a sterling year sat next to a dollar
year and printed as a 10.9% decline. And I asked Daniil for a ruling on Marqeta that his own
workbook had already given, with the Forbes source named in it.

---

## The ask: what Fable audits, all of it in one place

Everything we flagged for you today, gathered here so it is one list rather than four documents. The
source documents stay where they are and go deeper: `docs/brief-for-fable-basis-and-period.md`,
`docs/issues-for-fable-31aug-pm.md`, `docs/basis-and-period-audit-31aug.md` and
`docs/tpv-check-31aug.md`. Items 1 to 3 are standing checks that repeat at every handover from now
on. Items 4 to 11 are this batch.

### The standing checks, at every handover

**1. Run `python3 tools/audit_basis_period.py` and read the foot.** Tonight: **42 rows need a human,
66 agree with their own words**, out of 108 that carry a multiple. Three things must hold each time:

- **The agreeing number only ever goes UP.** If it falls, a row was edited without its label being
  revisited, which is exactly how Razorpay's gross 67.6x sat in the fintech file for four days.
- **Every row that can feed a range carries both a period and a basis.** **108 of 108 tonight**, and
  it must stay there. A row that can price a founder and cannot say what it is measuring must not
  price a founder.
- **`revenue_basis_source` says how we know.** Tonight: **18 STATED, 100 INFERRED, 0
  INFERRED_HIGH_RISK, 45 blank** (book-priced lenders and rows with no multiple). STATED should
  climb. **INFERRED_HIGH_RISK is at zero for the first time**: all five are resolved from primary
  sources, which was the dLocal, Pine Labs, StockX and Flipkart-twice investigation Daniil ordered.

**2. Run `python3 tools/data_inventory.py` and paste the foot into the handover**, including the NOT
READ BY THE ENGINE line. Plus the new ninth protocol rule: state by count which rows entered a
valuation and which did not, so a figure that is in the file but not in the engine is reported as
absent rather than as pending.

**3. Run the golden suite and check that no ruling from the day ended only in a conversation.** That
is the tenth protocol rule, added tonight after OFX.

### This batch

**4. The fixture schema, and I would do this one first.** Finding 1 above: no fixture carries a
revenue figure, so all 43 period spans read `NO_REVENUE_GIVEN`, the basis gate has only ever run on
its net branch, and `with_forward_revenue` is dead code with zero callers. Decide whether that
function is deleted or becomes the single path, and decide what a fixture profile has to carry
before the march to 100 continues. This gates the other 57.

**5. The 100 INFERRED basis rows.** Each is a basis somebody read off the business model rather than
off the source. Most will be right. Work them by sector, hardest first: **payments and delivery are
the two where the same archetype contains both gross and net reporters**, so an archetype rule must
not decide them. The test is ownership, not size: does the line contain money belonging to somebody
else? A freight broker's revenue holds the carrier's money, a staffing platform's holds the worker's
wage, and a first-party retailer keeps the whole sale price so its revenue is net in our sense even
though it looks gross beside a commission.

**6. The run-rate modelling assumption, which is doing more work than anything else on the list.**
`founder_revenue_for` assumes a run rate leads a trailing year by half a year of growth, and returns
`ESTIMATED_HALF_A_YEAR_OF_GROWTH` so nothing downstream can present it as something the founder
said. **66 private rows are run rates or ARR, our largest single bucket.** That is a modelling
choice, not a fact, and it deserves a second opinion before it prices anyone.

**7. The TPV arithmetic, on the riskiest rows rather than all 28.** Every CY+0 figure ties exactly to
the issuer's disclosure, which I checked. The forward series are the risk, because they are grown at
the local-currency revenue growth rate and four inherited a broken revenue series before I fixed it
across three revisions. Two manual overrides are in the file and both will become permanent if
nobody writes them down, so they are written down here, in `docs/tpv-check-31aug.md` and in the
manifest: **Fiserv carries a hand-entered 1% growth assumption for 2026** because Capital IQ was
returning something wrong, and **Nu's historical revenue was manually corrected** by Daniil. Both
must be replaced when the real numbers exist.

**8. The basis gate's permissiveness.** When first switched on it emptied all four lender fixtures,
because lenders carry no revenue basis and the gate read blank as incompatible. It is now guarded on
`is_balance_sheet()` and treats blank, NONE and UNKNOWN as unknown rather than as a mismatch. That is
the right fix and it is a permissive one: **check that no non-lender is passing the gate on a blank.**

**9. The lender fence, which I narrowed today.** It used to fire on either archetype slot, so
Payoneer and Wise were fenced out for holding customer funds and Block for owning Square Financial
Services. All three are payments businesses the market prices on revenue, and all three were blocked
from exactly the founders who needed them. It now reads the PRIMARY archetype only. Check that no
genuine lender slipped through the narrowing.

**10. Trolley, which you asked about and which has changed since.** Its listed core was EML at 0.7x
and Corpay at 6.4x, a ninefold spread from two names, and you asked whether EML was mis-tagged or
whether the honest answer was that the listed lane cannot price Trolley at all. Daniil decided it:
EML is dropped. The core is now Corpay, Repay and Usio, and the secondary range moves from 0.5-0.9x
to 0.7-2.1x. **Worth a look at whether that reads as a real range or as three names that happen to
be left**, because the original worry has not fully gone away.

**11. Whether the CONTEXT tier is honest on screen.** It is new today and it is the thing standing
between a founder and an empty box. Seven of the twenty new names land on it. The disclaimer copy
has never been read in situ. If the label does not make it obvious that these are context and not
comparables, we have replaced an honest empty box with a dishonest full one, which is worse.

### Known and deliberately deprioritised, so it is not rediscovered as a surprise

**The 513 listed rows still have no `revenue_basis` field at all**, and the listed lane therefore has
no basis gate. Statutory revenue is net for a take-rate marketplace like Etsy and gross for a
first-party retailer like Ocado, and both sit in the same family with nothing recording which. That
is the OLIPOP error at the listed level and it is live. Daniil ruled on 31 August that private names
matter more here, which I think is right, so this is a known hole rather than an unnoticed one. The
tagging table by archetype is in `docs/brief-for-fable-basis-and-period.md`, including the two
archetypes that must be read one by one rather than ruled on.

**The quiz cannot ask which basis the founder is giving.** `basis_compatible` already understands
NET, GROSS and BOTH on the profile, and no question produces that value, so it defaults to net for
everyone. Daniil wants the founder to be able to give either or both and then be priced like for
like. The gate is built and the input does not exist.

---

## Carry-overs and open items

**The 58-round master file, unchanged.** Still unwired, still missing 14 source URLs. Same position
as last night.

**The CAGR refresh, new tonight and written down so it survives compaction.** Daniil's ruling today:
growth ranking uses the CAGR only, and single forward years exist to estimate volume, not to
categorise peers. That is wired, via a separate `g_rank` field that only populates on a CAGR basis.
The cost until the refresh lands is exact: **321 of 513 listed rows can rank on growth, 192 cannot**
(105 consumer, 75 fintech, 12 software). Those 192 still price and still match on business nature,
they are simply invisible to the growth dimension. Daniil will supply the CAGRs with the next full
dataset refresh. The pull list is `docs/cagr-needed-pull-list.tsv`, 192 rows pastable into Excel,
and the full note with the reproduction command is `docs/cagr-todo-31aug.md`. When it lands, the
growth bands must be refit and fixtures will move, deliberately.

**The fixture march is now the only thing between us and the gate.** 43 verified, 57 to go, 15
working days. Today's 20 are triaged but not double-verified, so the number does not move. At two
independent agents per company that is roughly six companies a day and it needs to start Monday.

**Still unresolved from before today:** the six honesty flags do not reach a founder; volume
multiples are not yet on the football field although today's work unblocks them; 100 private rows carry an
INFERRED basis that nobody has verified; and Nexi's local-currency CY+0 cell is still blank.

---

## Commits

I do not run git on Daniil's machine, including read-only commands, per the standing rule. Everything
up to and including the OFX and EML removal is on origin at **`61c8032`**, pushed at his terminal:
eight files, three of them new (`docs/cagr-todo-31aug.md`, `docs/handover-2026-08-31-evening.md`,
`tools/triage_20_31aug.py`), plus `selector/match_reference.py`, `data/MANIFEST.md` and exactly the
three golden fixtures that moved. Eight is the number it should have been, which also confirms the
fixture writer is deterministic: a rewrite of all 43 produced diffs on only the three that changed,
so the suite is doing what it claims.

This handover was then extended after `61c8032` with finding 1, which I found while checking my own
claim about period matching, and with the consolidated audit list. One more push:

```
git add -A && git commit -m "Handover extended: fixture schema gap, consolidated Fable audit list" && git push
```

Fable, verify tonight's claims against `61c8032` plus that push.
