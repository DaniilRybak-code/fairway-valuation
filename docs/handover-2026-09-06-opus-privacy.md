# The no-storage reveal: built, checked, and what is still open

**6 September 2026, 12:30 UK. Opus.** Built in a fresh clone of origin at `fb260b2`, then merged
onto the working tree on Daniil's laptop, which held a parallel session's uncommitted work. No git
command ran on his laptop, read-only or otherwise (rule D10). See section 10 for what that merge
found.

Daniil's instruction, in his own words:

> "Is there a way to do all the same for the founder WITHOUT storing his financials? So we say
> transparently, we only take a record of the company data (profile, website), without storing the
> numbers. Then he gets the reveal based on the numbers he put in (we still do not see any
> financials at that point). Then if the user wants to have his numbers and ff reviewed, he presses
> a button and it comes through to us, in which case he would specifically agree for us to see it."

---

## 1. The thing worth reading first: the prompt named one door and there were two

The brief said `reveal-client.js` posts the figures to `/api/reveal`. It does, and that is the
smaller of the two leaks.

`submitLead()` in `app.js` posted `Object.assign({}, responses, { computed: result })`, which is
**the entire answer set plus every number `computeResult` had just worked out**, to `/api/lead`,
which writes it into named columns in a Google Sheet and `console.log`s the whole record. It fired
at the email step, **before the founder had seen anything at all**.

So a promise that covered only `/api/reveal` would have been false the moment anyone typed their
email. Both doors are closed, and both are closed at both ends: the page does not send, and the
server does not store.

---

## 2. The request body, before and after

**Before, to `/api/reveal`** (16 fields, six of them amounts):

```
stage, sector, sector_detail, website, currency,
revenue, revenue_exact, arr_exact, recurring_pct, revenue_model,
growth, growth_yoy, growth_detail,
profit, raise, timing, concerns, concern_notes
```

**After** (15 allowed, and only the ones the founder answered are sent):

```
stage, sector, sectors, sector_detail, website, company, country, revenue_model,
funding_model, volume_unit, revenue_basis,
growth, growth_yoy, growth_plan, gross_margin
```

**Removed by name:** `revenue` (a band is an amount written as a range), `revenue_exact`,
`arr_exact`, `recurring_pct`, `profit`, `raise`, `timing`, `growth_detail`, `concern_notes`,
`currency`. Three of those are free text, which is where a founder writes a figure when no box has
asked for one: "we went from 40k to 90k MRR" is a revenue disclosure in a growth box.

**Before, to `/api/lead`:** every field above plus `email`, `company`, `phone`, `ebitda_ltm`,
`last_round_amount`, `last_round_value`, `last_round_type`, `last_round_date`, `context_link`, and
the computed `ntmM`, `exitArrM` and `runRateM`.

**After:** the 15 allowed fields, plus `email`, `phone`, `concerns`, `variant`, `utm_source`,
`currency`, `type` and the consent block. Nothing else.

**Everything on the allowlist is a label or a percentage.** Nothing on it says how big the business
is.

**Two things still cross and the page says so rather than claiming we receive nothing.** The growth
rate gates which private rounds a founder is compared against (`band_compatible`) and ranks the
peers (`g_rank`). The gross margin decides whether the reveal leads on revenue or on gross profit
(`denominator`). Both are ratios.

---

## 3. Why this is nearly free, measured rather than assumed

**All 102 test fixtures carry no revenue, no growth rate and no margin, and 95 of them pass the
peer-universe gate.** The engine has been running on the private architecture since before anyone
asked for it. That is the whole argument, and it was already in the repo.

Revenue touches selection in exactly one place, `_one_round_per_company`, as a tie-break between two
rounds of the same company an order of magnitude apart. It degrades to growth-only when the figure
is absent, and since no fixture carries a revenue figure, it has been degrading that way for the
whole gate.

**The brief missed one thing, and it mattered.** `investors._stage_for` derived the founder's stage
from the size of the round they are raising, and the stage band is a hard gate on the investor list.
Without the raise the call list collapsed:

Measured against the merged working tree, which is where all five of those houses now carry a
published stage band:

| | callable cards across 102 fixtures | fixtures with no houses |
|---|---|---|
| raise $3m, stage not read (before) | 813 | 0 |
| no raise, stage not read | **0** | **102** |
| no raise, stage read (now) | 813 at Seed, 724 at Pre-seed, 797 at Series A | 0 |

(Against origin, before the parallel session filled those five bands in, the middle row was 44 cards
and 92 empty fixtures. Filling the bands in made the gate bite harder, so the fix below carries more
weight now than it did this morning, not less.)

That turned out to be a bug rather than a price. **The founder tells us their stage in step 1 of the
quiz and the engine was deriving it from an amount instead of reading the answer.** `_stage_for` now
reads the stated stage first, and the list is whole again with no amount anywhere near it.

**What is genuinely lost:** `_cheque_fits`, which drops a house whose published first cheque cannot
fund the round. At a $3m raise it excluded **3 of 156** callable houses. Those three are now shown,
with their published cheque range printed on the card, which is the thing a founder can check.

---

## 4. What was built

**`reveal-request.js` (new).** The only place in the product that builds a request body. Three
builders, each a loop over a named list, none of them containing a field name of its own. The
allowlist is three arrays with a comment on every entry saying why it may leave the browser.

**`reveal-figures.js` (new).** The founder's figures in one variable in one closure, and the
multiplication. No `localStorage`, no `sessionStorage`, no IndexedDB, no cookie. The arithmetic is
`round(figure * low, 2)`, which is what `match_reference.py` does and what check 14 recomputes.

**`reveal-client.js` (rewritten).** Posts the allowlisted body, holds the figures, and reads the
engine payload: the peer charts, the honesty caveats, the fix list and both investor layers, all
from one selection run. Before today `renderRecommendations` and `renderInvestors` existed and
nothing called them, and the honesty strings had been correct and unread since 26 August.

**Two things the payload wiring found on the way.** The chart entries carry no peer names, because
the names live in `ranges`, so each bar is joined back to its own lane and basis for them. And the
engine has always said whether a reading is a `RANGE`, a `SCATTER` or a `DIAMOND`, and nothing read
it: a one-name reading is now drawn as a point and labelled "one name is not a range" (rule A7)
rather than as a bar of no width. The axis is grouped by unit, because 3.0x to 4.4x and $2,700 a
subscriber are not the same measure and one scale for both makes the first one a dot.

**`api/lead.js`.** `FIGURE_COLUMNS` is blanked unless the body carries `consent.figures === true`.
Three columns added at the end of the row, so an existing sheet keeps every column where it is:
`figures_consent`, `consent_at`, `consent_wording`. The log line is written after the gate, so an
unconsented figure does not reach a log either, and a separate warning names how many fields were
refused.

**`api/reveal.js`.** The `answers` object is the server-side allowlist. `RAISE_MIDPOINT` is deleted
rather than moved: the endpoint used to subtract the midpoint of the raise from the stage median,
and `field.js` has always done that same subtraction in the browser, so the deduction moved to the
side of the wall that already had the number. Nothing the founder sees changes.

**The consent button.** Beside the 24-hour promise, because that read is what it buys. The wording
names the founder's own answers one by one ("your monthly revenue, your gross margin, your last
twelve months of EBITDA, your last round...") rather than saying "your data", and the exact wording
clicked is stored beside the figures.

**The copy.** One plain sentence before the quiz, on the hero and again at the top of the quiz
screen, because a `/?hook=` link lands a founder on the quiz without the hero ever being on their
page. The data disclaimer is rewritten in both places: it used to say the commentary service
"receives the business figures alone", which is now false, because it receives no figure at all.

**Rulebook E9.** Written, with the allowlist, the two things that cross, and what holds it up.

---

## 5. Check 15, and what it asserts

`tools/check_request_boundary.py`, wired into `tools/check_all.sh` as check 15. It is half a reader
and half a runner, because a boundary you can only read is a boundary you are trusting.

**What it reads.** The allowlist in `reveal-request.js` against its own copy in the check, in both
directions, so adding a field to the page means writing down in the check why it may leave the
browser. That nothing on the allowlist is a figure or a free-text box, judged against the check's
own independent list of 31 figure names and 5 free-text fields. That the builders contain no field
name of their own. That no `fetch()` in `app.js` or `reveal-client.js` posts a hand-made body. That
`api/reveal.js`'s `answers` object keeps no figure and `api/lead.js` still has its gate. That the
sentence before the quiz is on the page twice and the old disclaimer line is gone. That
`COUNT_BASES` and the basis names agree between `reveal-figures.js` and `match_reference.py`, which
is one fact written in two languages. That the three reveal files contain no browser storage.

**What it runs**, through `tools/request_boundary_probe.mjs`:

- The three builders, against a `responses` object holding every field the live quiz collects, with
  a **sentinel value in every figure** that appears nowhere else in the repo. It then looks for
  those values in every request body.
- `api/lead.js`, handled three times: the page's own body, a body with every figure forced back in,
  and a consented body. It asserts 14 figure fields are refused on the second, that none of them
  reaches the log line, and that they ARE stored on the third, so the button is not decorative.
- `api/reveal.js`, handled with every figure in the body and **the outbound call to the model
  intercepted**, so what would have reached the model is read rather than assumed. Zero sentinels
  reach it.
- **1,176 multiplications** of the browser's arithmetic against `round(v * low, 2)`, over the real
  charts of all 102 fixtures built by the real engine, at four probe values spanning four orders of
  magnitude. The multiplication moved into the browser, so there are two implementations of one sum,
  and this is what finds out on the day they diverge rather than a month later.

**The check was tested by breaking the boundary.** Adding `revenue_exact` to the allowlist makes it
fail in nine independent ways. Renaming a basis on one side makes it fail in three.

**It needs node.** Seven of its ten assertions can only be established by running the code, and node
is already a hard dependency: `api/lead.js` and `api/reveal.js` are Node functions on Vercel. If
node is missing the check fails and says so, rather than quietly testing half as much. Say if you
would rather it warned.

---

## 6. The suite, before and after

Both runs in the same fresh clone, `FAIRWAY_NO_GIT=1 sh tools/check_all.sh`.

| | before | after |
|---|---|---|
| checks | 15 (0 to 14) | 16 (0 to 15) |
| red | check 1 only, by design (public pull unloaded) | check 1 only, by design |
| golden | 0 of 102 profiles moved | 0 of 102 profiles moved |
| gate | 95 of 102 | 95 of 102 |
| callable cards | 813 | 813 |
| payload | 102 of 102 build, 96 caveated, 101 fix lists, 102 callable houses | identical |
| free tier | 102 free payloads, no figure outside the public lane | identical |
| investor cards | 813 across 102 fixtures | 813 |
| new | | check 15: 15 allowed fields, 14 figure fields refused by the server, 0 sentinels in the model prompt, 1,176 multiplications agreeing |

**Checks 0 to 14 are byte-identical between the two runs.** `diff` on the first 1,125 lines of the
two outputs returns nothing. Golden did not move, so nothing needs a reason written down.

**It was also run in a real browser.** Chromium loads `index.html`, the scripts load in order with
no page errors, the actual POST to `/api/reveal` carries eleven fields and no amount, the paid
payload renders the charts, the caveats, the fix list and eight investor cards, the free payload
renders the private lanes blurred with names and dates and no figures anywhere in the DOM, and the
consent POST fires only after the click and carries the figures with the consent block. Screenshot
delivered separately.

---

## 7. What is NOT done, named rather than left to be discovered

**1. The engine payload is not served yet, and the response says so.** `selector/reveal_payload.py`
is Python and `/api/reveal` is a Node function on Vercel. The endpoint returns `payload: null` with
`payload_reason: 'engine_not_served'`, and every block reads nothing rather than something wrong.
This is the remaining half of the wiring week and **it does not change the boundary**: that request
carries the same allowlisted body this one does. It is the next piece of work and it is a real
piece: a Python function on Vercel has to reach the CSVs in `data/`.

**2. The page can price one basis today, and the reason is a quiz question that does not exist.**
The live quiz asks for current monthly revenue and nothing else. Monthly times twelve is a run rate,
which prices the `ARR` basis. The engine's `REVENUE` basis is a **trailing twelve-month** figure
(`founder_revenue_for` treats it as trailing, and check 9 tests exactly that), and the quiz never
asks for one. Using a run rate against a trailing multiple would overstate the founder, so the page
does not. **This is a ruling for you** and it is in the box below. Every other basis (gross revenue,
book value, net income, originations, volume, every user count) is asked by a fork in
`selector/quiz_fork.py` that is not on the live page yet, which is the quiz testing that has not
started.

**3. The football field is still drawn by `field.js` from its own rows.** The peer charts render in
their own block under it. `field.js` draws nine METHOD rows (the last-round marker, the stage
anchor, the unrefined range, NTM, ARR, DCF and the paid rows) and the payload carries PEER EVIDENCE
per lane per basis. Deciding which of those nine rows survives contact with the engine is a product
decision, not a privacy one, and bundling it into this change would have put a product rewrite
inside a boundary change. Named as the next piece.

**4. Eleven em dashes on the live page, against rule E4.** All pre-existing, none of them mine, all
in copy you wrote: the three hero stat cards, the section lede, the comparison table, the driver
list. One at line 69 is a legitimate empty-cell marker in the football field. Not touched, because
changing eleven lines of your landing copy is not mine to do quietly.

---

## 8. For the open decisions box

- **Does monthly revenue times twelve stand in for the trailing figure?** The engine prices its
  `REVENUE` basis on a trailing twelve-month number and the quiz asks for a current month. Either
  the quiz gains a trailing question, or you rule that the run rate stands in, or the revenue lanes
  stay unpriced and the founder sees the peer multiples without a value beside them. My
  recommendation: add the question, because check 9 already tests the conversion in both directions
  and the machinery is waiting for an input it has never had.
- **Does the raise band go back on the free path?** I took it off, because it is an amount and the
  brief said no absolute figure. It costs 3 of 156 investor houses no longer being filtered on
  cheque size. If you would rather have that filter, the raise band is a defensible exception: it is
  the ask, not a figure from your accounts. One line either way and check 15 changes with it.
- **Should check 15 fail or warn when node is missing?** It fails today.

---

## 9. What the merge onto Daniil's laptop found

Before writing anything I compared his working tree against origin, file by file, by checksum,
without running git. **His tree held a second session's uncommitted work**, stamped 13:00 UK: the
"Early stage is a stage band" change. Writing my files over his would have destroyed it and
`git add -A` would have committed the loss silently. So my changes were merged onto his versions
rather than the other way round, and every number in this document was re-measured against the
merged tree.

What was uncommitted: `selector/investors.py` (`STAGE_COVERS` and `_stages_of`),
`data/investors.csv` (5 rows against origin), `docs/STATUS-2026-09.md`, six golden fixtures, and two
new files (`tools/apply_investor_stages_6sep.py`, `data/raw/2026-09-06_investor-stage-gap-5houses.csv`).
`selector/investors.py` is the one file both sessions touched, and the two changes are in different
functions, so the merge is clean: his `_stages_of` expands the band, my `_stage_for` reads the
founder's stated stage.

**Two things in that work that need saying, neither of them mine to fix:**

**1. Golden moved and the log entry does not say so.** Six fixtures changed: acti, befreed, bloomy,
honen, welltory, wondering. The reason is sound and is the intended consequence: Haystack now
carries a band, so it enters those six founders' call lists at tier 1. It still needs writing down,
because "golden must not move without the reason written down" is the rule that catches the ones
that were not intended. Added to the status document.

**2. Five `deal_note` fields still say STAGE BAND LEFT EMPTY, and `investors.js` prints `deal_note`
on the founder's card** (line 66, `invCallableCard`). Canaan, Founderful, Haystack, Techstars and
Town Hall Ventures each carry a band now and a note beside it saying the band was left empty. That
is a false sentence on a card a founder reads. Left alone because it is that session's work in
flight and the wording is Daniil's ruling, but it should not reach the pilot.

---

## 10. Files changed

```
new     reveal-request.js                     the allowlist and the three request builders
new     reveal-figures.js                     the figures, in one variable, and the multiplication
new     tools/check_request_boundary.py       check 15
new     tools/request_boundary_probe.mjs      the half of check 15 that runs the code
new     docs/handover-2026-09-06-opus-privacy.md
edit    reveal-client.js                      posts the allowlist, reads the payload, consent button
edit    app.js                                submitLead posts buildLeadRecord, keeps the lead id
edit    api/lead.js                           figure columns blanked without consent, 3 new columns
edit    api/reveal.js                         answers is the server allowlist, RAISE_MIDPOINT gone
edit    selector/investors.py                 _stage_for reads the founder's stated stage first
edit    index.html                            the sentence before the quiz, three mounts, the
                                              consent block, both disclaimers, two script tags
edit    docs/RULES.md                         rule E9
edit    docs/lead-capture.md                  what a row holds now, and the consent columns
edit    tools/check_all.sh                    check 15
edit    docs/STATUS-2026-09.md                session log and TO COMMIT, merged onto the
                                              parallel session's version
```

**Also in this commit, from the parallel session and not from this one:** `selector/investors.py`
(`STAGE_COVERS`), `data/investors.csv` (5 rows), six golden fixtures,
`tools/apply_investor_stages_6sep.py`, `data/raw/2026-09-06_investor-stage-gap-5houses.csv` and
`docs/prompts/privacy-architecture-6sep.md`.

**Counts in, counts out.** This session touched no data file. 102 fixtures in, 102 out. 532
investor houses in, 532 out. 268 private rounds in, 268 out. On the merged tree: golden 0 of 102
moved, gate 95 of 102, 813 callable cards, 1,557 evidence chips. Nothing was dropped, and the
parallel session's nine changed files and two new files are all still there.
