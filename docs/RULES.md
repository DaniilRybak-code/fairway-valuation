# The Fairway rulebook

Every rule we have agreed, in one place, in plain words. Written 1 September 2026 because the rules
were scattered across handovers and nobody could see the whole set at once.

**Three columns matter and only one of them is comfortable.** A rule can be AGREED (we said it),
BUILT (the code does it), or CHECKED (something fails loudly if it stops being true). Most of our
rules are agreed. Fewer are built. Almost none are checked, which is why a ruling can quietly stop
being true and nobody notices for four days. Where a rule is not built, the entry says so and says
what would have to happen.

Daniil owns every rule here. Edit this file directly; it is the source, and the code follows it.

---

## A. Choosing which companies to compare against

**A1. Business nature selects a comparable. Nothing else does.**
What the company actually does is the only thing that decides whether it belongs in the set.
*Built:* yes, `same_family()` gates on business nature before anything is ranked.

**A2. Size never selects, and never excludes. It may only TRIM.**
A company is not a better or worse comparable for being bigger, so size never decides who is in the
pool. **Amended by Daniil 1 Sep:** once the pool is chosen on business nature and it holds more
names than we show, size may rank the survivors, and we keep the ones closest in size to the
founder. Size decides which of the equally valid names get shown, never which are valid.
*Built:* the no-size-in-selection half, yes. **The trim-by-size half is NOT built** and is now on
the list.
*One live breach, deliberate:* two names, OFX and EML, are excluded by name for being micro caps
where broker forecasts are unreliable. That is a named list with a written reason each, not a size
rule, precisely so it cannot spread.

**A3. Recency never selects either, with one narrow exception.**
The exception is between two rounds of the SAME company. There:
- if the two multiples are similar, take the later round, because it is more relevant;
- if they are far apart (an order of magnitude), do not take either on date. Compare the founder's
  own scale and maturity and take the round that is evidence about a company like theirs.
**Amended by Daniil 1 Sep and rebuilt the same day.** The old test was a 3x spread, which I had set
to sit in a gap in our own data. His test is on the gap itself: **if the lower multiple is more than
30 per cent below the higher one, apply the closeness criteria.** Below that, take the latest.
*Built:* yes, `MULTI_ROUND_GAP = 0.70`.
*What it changed:* the closeness rule now fires on eight companies instead of four. It newly catches
AlphaSense (17.0 to 25.0), Scale AI (9.9 to 14.5), Zepz (6.3 to 14.8) and SHEIN (1.4 to 2.9), all
of which are genuine repricings where the older round is evidence about a smaller company. No test
case moved.

**A4. Never blend two rounds of the same company into an average.**
One company, one vote. The other round is context shown beside it, never half of a number.
*Built:* yes.

**A5. A blank is a trigger, never a conclusion.**
If no obvious comparable exists, find the next best neighbour and label how close it is. A founder in
a young category is using Fairway precisely because no clean precedent exists. Returning nothing is
the one answer that has no value.
*Built:* crudely. Bands widen until they hold at least three names, the core tops up from the wider
set, and a CONTEXT tier shows named companies with a disclaimer where the match is weak. It works
and it cannot explain itself.
**Daniil 1 Sep: this rule is used constantly and must be made procedural and prioritised.** A full
seven-rung specification, with the order measured against our own 429 listed multiples rather than
asserted, is now written up in `docs/next-best-neighbour-spec.md`. Headline finding: what a company
DOES explains 44 per cent of the spread in its multiple, while the vertical it serves explains only
14 per cent, so the vertical is the first thing we should be willing to give up and the business
model is close to the last.

**A6. A handful means 3 to 5 names on a close match, 5 to 7 where the match is weaker.**
Two names is not a range.
*Built:* yes, on both lanes.

**A7. Never price off one comparable.**
A single name is shown as one labelled point, never as a range.
*Built:* yes, a single priced name renders as a point, not a range.

**A8. Never show an unrelated comparable.** Three real names beat five padded ones.
*Built:* partly. The comparability label is on every range. The judgement of "unrelated" is still
human.

**A9. Listed and private evidence never combine into one number.**
Two separate lanes, shown separately, never averaged together.
*Built:* yes.

**A10. Lenders and deposit-taking banks price on book value, never on revenue.**
No other sector may touch the book path.
*Built:* yes, and the fence reads the PRIMARY business type only. It used to read either slot, which
wrongly fenced out Payoneer, Wise and Block for holding customer money.

**A12. Failing the relevance gate is a FAILURE, and the archetype fallback is how we serve the
founder anyway. Every use is recorded.**
*Added 5 Sep, Daniil: "Not satisfying this gate is a failure and should be flagged to us. BUT, as a
fallback, we can defer to archetypes... we need to get recording such failures and enrich the
database as we go, but we cannot keep spending time on this only."*

Three parts, and the third is the one that decays if nobody watches it:

1. **The gate is unchanged.** A comparable earns its place by shared product vocabulary or a shared
   specific end market. Sharing an archetype is a label, not evidence, and the labels are too coarse
   to carry it: `Vertical Software` holds 120 rows and contains stock exchanges and restaurant
   software (`docs/taxonomy-review-5sep.md`).
2. **The fallback is a RESCUE, not a loosening.** Stated as the code applies it, because the first
   wording of this rule was looser than the thing it described. The fallback opens for a lane
   holding FEWER THAN TWO priced comparables, and what it admits is KEPT ONLY IF IT ADDS A PRICED
   NAME. A lane that is already healthy never sees it, and a rescue that brings in five names and
   prices none of them is discarded rather than shown. Applied everywhere instead, it would hand a
   social publishing API the Perplexity round, which is the failure the gate was written to stop.
3. **Every rescue is named on every run** by `tools/peer_universe_check.py`, and it is named in the
   NO-COMPS LIST alongside the companies that got no comparables at all. Those were the two kinds of
   entry and they belong on one list: a founder served on a label and a founder served on nothing
   are both founders the database could not answer. **Two more kinds joined them.** On 6 Sep,
   companies served on a generic word or the end market alone (recorded, not removed). On 8 Sep,
   after march 1 showed Orca Aerospace, Constellation Space and Zymbly passing the gate on
   restaurant and hospitality rounds, Daniil: *"such companies should immediately go into the
   no-comps list."* So a fixture whose comparable set a person has read and struck carries the
   reason on its profile (`struck`), FAILS the gate whatever its lanes hold, and is printed as the
   fourth kind. The gate counts names found; it cannot judge whether they make sense, and a pass on
   nonsense is worse than a failure. `tools/fixture_comparables_table.py` writes every fixture
   beside the names it was shown, which is how the reading is done.

   **What we do about it, and this is the part that decays if nobody watches it.** Daniil, 5 Sep,
   23:10 UK: the pool is large enough, there will always be blind spots, and the pilot is the best
   way to find them. So **we do not chase comparables lane by lane as the list grows.** On 8, 11, 15
   and 18 September we run a MARCH, not a data pull: 30 to 40 new test companies each time, scored
   the way the 3-Sep march scored them, each march adding to the No-comps list. **The list is
   resolved in bulk once, after the 18 September march and before launch.** Between the marches the
   work is on the matching machine and the tagging, not on enlarging the pool. A proposal to pull
   data outside that one bulk pass is this rule telling you to stop.

**A11. Hardware is filed under what it sells, not under a hardware archetype.**
We have no hardware archetype and we are not adding one, because the taxonomy sorts businesses by
what they do commercially rather than by whether the thing they ship is physical. A company that
makes a physical product and sells it to consumers is Owned-Inventory Retail; one that engineers it
to order is Design & Engineering. That is where both hardware fixtures sit today.
*Live consequence, and it is not comfortable:* `ultrasonium`, a metal manufacturer, carries
Owned-Inventory Retail, and on that label the archetype fallback offered it Moove, Quince, Olive &
June and Flink. It fails the gate anyway, so nothing wrong reaches a founder, but the rule is doing
worse work here than it does elsewhere and the tagging review has it.

---

## B. What a multiple actually means

**B1. Use the revenue the investor had at the time of pricing, never later actuals.**
The period matters, not the publication date. Later figures are hindsight and are notes only.
*Built:* yes.

**B2. A round announcement beats filed accounts for the same period.**
It is the primary source and it is what the investor priced against. Keep the filed figure as a note.
*Agreed 31 Aug. Built:* yes, applied to Zepz and standing for everything after.

**B3. Gross and net revenue never sit in the same range.**
The test is ownership, not size: does the line contain money that belongs to somebody else? A
freight broker's revenue holds the carrier's money. A staffing platform's holds the worker's wage. A
first-party retailer keeps the whole sale price, so its revenue is NET in our sense even though it
looks large next to a commission.
*Built:* on private rows only. **NOT built on listed rows, because listed rows carry no basis field
at all.** 511 listed rows have nothing recording whether their revenue is gross or net. This is the
single biggest known hole in the rulebook.
**Daniil 1 Sep: filling the field is not the job. Fable must AUDIT whether the rows labelled net are
genuinely net and the rows labelled gross are genuinely gross.** A label nobody checked is not
evidence. 100 private rows currently carry a basis somebody read off the business model rather than
off the source document.

**B3a. The quiz asks the founder for BOTH figures, and the engine keeps both.**
*Added 5 Sep, Daniil, 23:35 UK.* Until then the quiz asked for net revenue only, and that single
default threw away every round priced on a gross figure: 66 of our 320 private rounds hold a usable
gross multiple, sitting in the right archetype next to founders who could not reach them. Six of the
twelve fixtures failing the peer-universe gate failed for that reason and no other.

So the founder is asked for net revenue and for gross revenue, with the difference explained beside
the question in plain words: gross is everything that passes through the business before the money
that was never theirs goes back out, net is the part they keep. **A founder who gives one figure is
served on that one.** Neither question blocks them.

**This does not loosen B3; it is what makes B3 affordable.** Gross still never bands with net. The
founder's net figure is compared only against rounds priced on net, the gross figure only against
rounds priced on gross, and the two produce TWO SEPARATE RANGES, each labelled with the measure it
is built on. Mixing them was the only thing the net-only default protected against, and it protected
by throwing the evidence away.
*Built:* yes, on the private lane. **Not on the listed lane, and deliberately:** listed rows carry no
basis field at all (see B3 above), so a listed gross range would mean relabelling 513 rows nobody has
read. Until that hole is filled, a founder's gross figure meets private rounds only.

**B4. Forward and trailing numbers never sit in the same comparison.**
Run rate and ARR are FORWARD, because both annualise what the business is earning now rather than
the year just finished. Two buckets, forward and trailing, not three.
*Built:* the machinery exists and every range carries the founder's revenue on the right basis.
**Nothing consumes it yet.** Daniil asked why, on 1 Sep, and the answer is exactly what he guessed:
no founder revenue has ever been fed in, because the reveal is not connected and the test cases
carry no revenue figure. The fix is not more data, it is a manual test mode where a revenue number
can be typed in and the whole path exercised. That is being built.

**B5. A disclosed threshold produces a ceiling, not a point.**
"More than $300m of revenue" gives a multiple that is at most X, and it must display as at most X.
*Built:* yes, the bound is carried and displayed.

**B6. A control deal prices, but carries its label.**
A takeover price includes a control premium that a minority round never gets. Semrush-class M&A
anchors mark the field as labelled diamonds; they do not feed the range.
*Built:* yes.

**B7. Volume multiples (GMV, TPV) may price only when the valuation and the volume describe the
same thing.**
That excludes a lender whose balance sheet is the business, and any segment volume set against a
whole-group valuation.
*Built:* yes, 63 of 268 volume rows are usable and 13 are explicitly not, each with a reason.

**B8. GMV, ARR and revenue are not interchangeable. Equity value and enterprise value are not
interchangeable.**
Volume enters the field as its own row when a founder gives it, never blended into a revenue range.
*Built:* the data side is done. The football field wiring is not.

**B9. Growth ranking uses the multi-year CAGR only.**
Single forward years exist to estimate volume, never to sort peers into growth bands.
*Agreed 31 Aug. Built:* yes. Cost today: 319 of 511 listed rows can rank on growth, 192 cannot,
because they carry only one forward year.

**B11. A multiple that is negative or zero is not a price. It is n.m.**
*Added 4 Sep, Daniil: "Negative multiples are not allowed, they should be marked as n.m."* A
negative enterprise value is arithmetic, not evidence: a broker or a payments company holding client
balances nets its own cash against its market capitalisation and comes out below zero. The company
is not dropped. It keeps its name, its tags, its revenue and its growth and can be shown as context;
it simply carries no meaningful multiple, so it cannot enter a range, a median or a quartile, and
the page prints `n.m.` rather than a blank, because a blank says we hold nothing when we hold a
fact. The original figure stays on the row under `nm_<field>`, and every row this touches is named
by `tools/check_engine_reach.py`, count in and count out.
*Built:* yes, in the loader, one sweep after the universe is built. Four figures on four companies
today.

**B10. Entity matters as much as period.**
Whose revenue is it, and does it belong to the thing being valued? Flipkart India Private Limited is
the wholesale arm; Flipkart Internet Private Limited is the marketplace. Same group, five times
apart, 6.4x against 34.2x.
*Built:* no. This is a human check and it caught us once already.

---

## C. Where numbers may come from

**C1. Every figure carries a named source with a date.** No source, no publication to a founder.
*Built:* yes on the main private file (111 of 112 rows carry a round source URL).
*Not true of the consumer private file:* only 3 of 51 rows carry one.

**C2. An LLM is never the source of a transaction record or any figure.**
*Built:* no code can enforce this. It is a discipline.

**C3. Statistics in product copy must be real. Never invented, never illustrative.**

**C4. Estimator sites are a last resort.**
Usable only when better sources are empty, tagged as such. A figure with no stated period is
excluded outright.
*Built:* **no.** This rule exists on paper only; nothing in the code marks or ranks source tiers.

**C5. Never scrape a vendor. Check redistribution terms in writing before signing any data licence.**

**C7. A listed comparable has to still be listed, and the agent proposing it has to have checked.**
*Added 4 Sep*, after I put four companies on a ticker request that no longer trade: Sapiens
International (Advent, $2.5bn), Learning Technologies Group (General Atlantic, about $1bn), Udemy
(into Coursera) and Accolade (Transcarent, $621m). None was in our data, so nothing we hold went
stale, but all four would have wasted a Capital IQ pull and one of them would have been priced off a
dead quote if the screen had returned one. Two consequences: check before proposing, and treat the
delisting itself as evidence, because a take-private is a priced control transaction under B6 and
belongs in the private file. Whole sectors are disappearing from the listed side this way, corporate
learning first among them.

**C6. Test only on real companies. Never invent one.**

---

## D. Not losing data (the durability protocol)

**D1. Nothing is received until it is a file in `data/`.** A screenshot is a preview, never a
transfer. Any transcription is written to a file in the same session, before analysis touches it.

**D2. Every drop gets a row in `data/MANIFEST.md`.**

**D3. Every data session opens and closes with the inventory, and the closing run goes into the
handover verbatim, including the "not read by the engine" line.**

**D4. Every number in a handover names its file and reproduces from a command a reader can run.**

**D5. No file sits unwired past one session without a manifest line saying why and who owns it.**

**D6. A disputed row stops feeding the engine the moment the dispute is known**, not when the
ruling lands.

**D7. Every session that touches data ends with commit and push, and the handover quotes the SHA.**

**D8. A figure that is in the file but not in the engine is reported as ABSENT, not as pending.**
*Added 31 Aug.* Twelve currency figures sat correctly filed and entered no valuation at all, and it
was reported as a decision waiting on Daniil rather than as data not being used.

**D9. A ruling that lives only in a conversation is not in the product.**
*Added 31 Aug*, after OFX was found still pricing days after it was killed, and after our own note
about Flipkart's wholesale entity sat unread while the wrong multiples fed live ranges. Every ruling
ends the session written into code or into a file, and the handover names which.

**D10. Nobody runs any git command on Daniil's machine through the bridge, including read-only
ones.** Files and patches in; commands for him to run.

**D11. A transcription schema must carry every column the source has.**
*Added 2 Sep*, after source URL columns AA and AB were dropped twice from the same sheet. D1 to D10
all assume that what arrives is either written down or visibly missing. A column that was never in
the target schema is neither: the data has nowhere to land and nothing counts its absence. Before
transcribing, list the source's columns and give every one a field, even the ones that look empty
or useless today.

**D12. EVERY SUPPLIED ROW IS ACCOUNTED FOR BY NAME. Silence is never an outcome.**
*Added 2 Sep*, after a loader deduplicated on COMPANY rather than on company AND round and silently
skipped six of Daniil's rounds, for companies we already held.

Three parts, and all three are mandatory:

1. **Match on the row, never on the entity.** A load that decides "we already have this company"
   is broken by construction. The comparison key is company plus year and month, always. The same
   applies to funds, tickers and investors: match the ROW, not the name.
2. **`python3 tools/check_raw_coverage.py` must PASS before any commit that touches a data file.**
   It reads every supplied file, matches every row against the loaded files, and exits 1 with the
   company and date of anything unaccounted for. It is deliberately dumb because the bug it exists
   to catch was clever.
3. **A row that is not loaded is EXCLUDED IN WRITING or it is a failure.** Add it to `EXCLUSIONS`
   in that tool with a reason a stranger could audit. Never make the check pass by editing a raw
   file: raw files are the record of what Daniil sent and are append-only.

The rule generalises past loading. Any operation that reduces a supplied set, a dedup, a filter, a
join, a merge, a promotion pass, must report the count in and the count out, and name what fell
between them. **If it cannot name what it dropped, it is not allowed to drop it.**

**D13. Commit with `git add -A`, never with a hand-written file list.**
*Added 2 Sep*, after a commit block was skipped and `tools/load_daniil_sheet_2sep.py` and
`docs/sector-screen-fix-prompt-2sep.md` never reached the repo, even though the data they produced
did. A hand-written `git add` list is a second place for work to be silently lost: it fails when a
file is forgotten, and it fails again when a whole block is skipped. Every commit instruction handed
to Daniil is `git add -A`, and every handover names the SHA that the state was verified against.

**D14. A ruling, a rule change or a data pull is committed the moment it lands, not at the end of
the day.**
*Added 4 Sep, Daniil: "as soon as we make some decision regarding rules, data, or when we get the
new data pull, we commit it immediately or at least make a note of it to be committed. We do not
want to lose any work."* D7 says a session ends with a commit and D9 says a ruling that lives only
in a conversation is not in the product. D14 is the tighter version of both, because a session can
end unexpectedly: an agent hits its context limit, a laptop sleeps, a chat is closed. The unit is
the decision, not the day.

Three parts:

1. **The moment a decision is made, it is written into code or a file in the same turn**, and
   committed at the next natural break rather than held for a handover.
2. **A data pull is committed on arrival**, before it is loaded, analysed or argued about. The raw
   file is the record of what was sent (D1, D12), and an unpushed raw file is a pull that can
   disappear without anyone knowing it existed.
3. **When a commit genuinely cannot happen now**, the decision goes on the TO COMMIT list at the
   foot of the status document in the same turn, with the file it lives in. An item on that list
   is unfinished work, not finished work.

---

## E. The product and what it may claim

**E1. The word "calculator" never appears in product copy.**
*Checked:* it appears nowhere in the site today.

**E2. No copy may imply we are a 409A provider or a chartered valuer.**
Use-case copy frames Fairway as preparation for a regulated valuation, never a substitute.

**E3. Pre-revenue founders get comparables and precedent rounds, never a computed number.**
The consultation offer is framed as a data constraint, not a sales step.

**E4. Plain language everywhere.** Handovers, this file, and product copy. No naming conventions a
reader has to decode. No em dashes.

**E5. Daniil's name and LinkedIn stay off the site** until he says otherwise.

**E6. The engine connects to the reveal only after 100 double-verified test cases.**

**E7. Every comment Daniil makes gets reflected in the product, and anything that cannot be is
flagged to him immediately.**

**E8. A number the founder has not paid for is ABSENT FROM THE PAYLOAD, never merely blurred in
the page.**
*Added 4 Sep. Amended by Daniil 6 Sep, and the amendment is the reason the wording above changed
from "a lane" to "a number".*

**What the three tiers are** (Daniil, 6 Sep, settling the apparent contradiction on the live page):
the **free** tier is the reveal plus a banker reading every set of answers by hand within 24 hours
to confirm the comparables make sense; **$250** unblocks the full football field, private tiers and
DCF included; **$750** is a full valuation presentation. The free review is not a contradiction of
the $250 tier: one checks that the comparable set is sane, the other hands over the field.

**What the free tier shows.** The PUBLIC lane in full and free. Everything non-public blurred, and
on hovering a blurred range **the list of comparable companies, without their multiples**.

**Which half of the old rule survives, and it is the important half.** A CSS blur over a number
sitting in the DOM is not a paywall, it is a dare: inspect the element and read it. So the FIGURES
behind the lock still never reach the browser. The free payload carries, for a locked lane: that it
exists, how many comparables stand behind it, what kind of evidence they are, and now their NAMES.
It carries no multiple, no low, mid or high, and no founder value. The blur the founder sees is
drawn over nothing; there is nothing behind it to inspect.

**What changed, plainly:** names used to be withheld with the numbers, and Daniil has ruled they
should be shown. That is a good trade. A founder who can see that we hold Vanta, Personio and Miro
for them knows the lock is over real work, which is a better argument for paying than a grey box.
*Built:* `reveal_payload.build(prof, tier='free')` and check 14, which asserts that no multiple and
no range endpoint appears anywhere outside the listed lane of a free payload.

**E9. A founder's own figures stay in their browser until they press a button that says so.**
*Added 6 Sep, on Daniil's instruction: "we only take a record of the company data (profile,
website), without storing the numbers... if the user wants to have his numbers and ff reviewed, he
presses a button and it comes through to us, in which case he would specifically agree for us to
see it."*

**What may leave the browser on the free path.** The company profile (stage, sector chips, the
sector written in their own words, website, company name, country, how they charge, and the fork
labels: how a lender funds its book, what unit a volume is in, which measure a revenue figure is
on), the growth rate, and the gross margin. Every one of those is either a label or a percentage.
None of them says how big the business is.

**What does not.** Revenue in any form, ARR, gross revenue, book value, net income, originations,
volume, every user count, EBITDA, the last round, whether they are profitable, the size of the round
they are raising, and the free-text boxes, which is where a founder writes a figure when no box has
asked for one.

**Two things cross and the copy says so.** The growth rate gates which private rounds a founder is
compared against and ranks the peers; the gross margin decides whether the reveal leads on revenue
or on gross profit. They are needed and they are ratios. The sentence on the page says exactly that
rather than claiming we receive nothing.

**Why it costs nothing.** Selection needs those two ratios. Pricing is one multiplication and it
happens in the browser. The proof is the gate: all 102 test fixtures carry no revenue, no growth
rate and no margin, and 95 of them pass.

**Both ends, not one.** `reveal-request.js` is the only place in the product that builds a request
body and it builds every one by looping over the allowlist. `api/lead.js` blanks every figure column
unless the body carries `consent.figures === true`, and `api/reveal.js` reads only the allowlisted
fields, so a page that starts leaking again still writes nothing and sends nothing to a model.

**The button.** One request, triggered by the founder, wording that names what is being sent and to
whom, and the wording itself stored beside the figures. It buys the free 24-hour banker read.

*Built and checked:* check 15, `tools/check_request_boundary.py`. It runs the request builders with
a sentinel value in every figure the quiz collects and looks for those values in every request body,
in the Vercel log line and in the prompt that goes to the model; it handles `api/lead.js` twice,
with and without consent; and it compares the browser's multiplication against `round(v * low, 2)`,
which is the sum `match_reference.py` does and check 14 recomputes.

---

## What this table says about us

Of the 40 rules above, roughly two thirds are built into the code and about five are actively
checked by something that fails loudly. The gap between AGREED and BUILT is where every problem of
the last week has come from: the basis rule existed for four days before anything enforced it, the
OFX ruling existed for a day before anything enforced it, and the estimator-tier rule has existed
since the start and has never been enforced at all.

**The fix is not more rules. It is a check per rule.** The three that exist (the inventory, the
basis audit, the golden suite) are the reason we catch anything. The candidates for the next three
checks, in order: a listed-side basis gate once the tags exist (B3), a source-tier check (C4), and
a test that every named ruling has a corresponding line of code or data (D9).

---

## FOR FABLE: Daniil's amendments of 1 September, to be checked today

Five comments on this rulebook, recorded verbatim so nothing is lost in paraphrase. Three are rule
changes, two are audit instructions.

**1. On A2, size.** *"true BUT, if we have an alternative of multiple comps and we need to trim down
the selection to the usual 5-7, then we need to rank by size and select those which are closer by
size."* Rule amended above. Not yet built; the trim currently drops on score alone.

**2. On A3, the multi-round threshold.** *"I would not hardcode 3x, I would say that if the lower
multiple is more than 30% below the higher multiple, then we need to apply size criteria."* Built
the same day. Check the change moved the right four companies and nothing else.

**3. On A5, next best neighbour.** *"is important and we need to be more elaborative, more
stage-by-stage... I expect this rule to be used very often and perhaps it must be prioritised."*
Specification written at `docs/next-best-neighbour-spec.md`. **Fable to review the ladder order
before any of it is built**, particularly the claim that vertical is cheap to give up and business
model is not, which is measured but measured only on the listed set.

**4. On B3, gross and net. THIS IS THE AUDIT INSTRUCTION.** *"we need to ask Fable to AUDIT, if the
net numbers in the base are indeed net and gross are indeed gross."* This is not the same as
checking the field is populated, which is already done. It means reading the source document for
each row and confirming the label. 100 private rows carry an inferred basis. Start with payments and
delivery, the two sectors where the same kind of business reports both ways.

**5. On B4, forward and trailing.** Confirmed that nothing consumes the matching because no revenue
has ever been supplied. Daniil accepts this, on condition that the manual test mode gets built so he
can supply one himself and test it.

### Two findings from measuring the rules rather than reading them

**Growth does nothing on the listed lane.** The growth bands are MATURE below 77 per cent, GROWING
to 206, HYPER above, fitted on private funding rounds where the typical rate is 133 per cent. Listed
companies grow at a median of 11 per cent. So **318 of the 319 listed companies carrying a growth
rate are classified MATURE**, one is HYPER, and none is GROWING. Growth currently plays no part in
choosing a public comparable. This needs fixing before the 192 CAGRs arrive, or they will feed a
dimension that sorts everything into one bucket.

**37 of 108 priced private rounds are excluded from every range.** A third of our private evidence
does not price anybody. Some exclusions are certainly right. Nobody has checked that all of them are.
