# Sequencing and status, 24 August 2026 (evening update)

Two sessions worked on Fairway today and neither could see the other's conversation. This is the one
place that reconciles them. It supersedes the seven-item list at the foot of
`claude/Fairway_profiler_website_test.md`, which remains the best account of the profiler field test.

---

## Status against the seven items

| # | Item | Status |
|---|---|---|
| 1 | Batch 2 plus the at-pricing rule merged to main | **Done** (28b900a, other session) |
| 2 | E-commerce and D2C data, plus a new taxonomy branch | **Done, second pass complete.** 72 listed names; 50 verified private transaction records across 34 companies, of which **16 rows across 13 companies carry a defensible REVENUE multiple** and 4 carry a GMV multiple in a separate lane; and a third vocabulary family with two new fields |
| 3 | Wire the selector against the data and the token weights | **Done.** `selector/match_reference.py`, 318 listed and 110 private rows, token weights regenerated over five tag files |
| 4 | Golden test, fixtures before any tuning | **Done for 12 profiles, and it has now caught two real defects.** Core, secondary AND private comps, denominators and ranges are snapshotted. It has already caught one real defect. The 21 website profiles are still not in it, for the reason below |
| 5 | Reveal copy: pre-revenue positioning mode, control-transaction labels | **Not started.** The private set now carries `transaction_type`, so the labelling that copy needs exists in the data |
| 6 | Batch 3: scraping APIs, email deliverability | **Not started** |
| 7 | Second random-20 profiler test on the broadened scope | **Not started, now unblocked** |

---

## Item 2: what landed, and the one thing that did not

The listed set is refreshed to 72 names. It now carries a ticker column, a revenue FY+2 column, and
growth restated as FY+2 over FY+1, which removes the currency-translation effect that made ASOS,
Autohome and Hemnet read as declining businesses. Hemnet goes from -14% to +24%.

The private set is 44 rows from 48 supplied, and it needed a rebuild rather than an import. **The
number that matters is not 44.** 44 is the count of verified transaction *records*. Only 17 rows
across 13 companies carry a multiple defensible enough to price against, and 5 of those 17 are
ceilings rather than point estimates, so 12 are point multiples. The other 27 rows are real,
verified transactions kept for their date, structure and investor record, with no printed multiple.
Median of the 17 is 7.3x; of the 12 point multiples, 6.3x. Details
are in `docs/consumer-commerce-taxonomy.md`. The short version: every supplied multiple reconciled
arithmetically and most did not survive the at-pricing rule.

**Still outstanding for this family:** private consumer rounds in the categories the 44 do not reach.
There is no private edtech, no private food delivery or quick commerce, no private travel, and no
private auto or property marketplace. The golden fixtures show the consequence directly: a consumer
language-learning profile now correctly returns NO private comparable set, because there is nothing
to return.

---

## Item 4: what the fixtures caught on day one

Adding 31 private consumer companies broke private matching for any profile with no private
neighbours. A consumer language-learning app was returned Huel, AG1 and Harry's, each scoring 9.7 on
nothing but "sells a subscription to a consumer": end customer, revenue model and purchase frequency
coinciding, three low-information tags. A relative quality floor cannot catch this, because 45% of a
bad best score is a worse score.

`FLOOR_ADEQUATE = 12.0` now returns an empty set rather than a bad one, calibrated on the observed
gap between profiles that have private neighbours and one that does not: skincare 40.5, quick
commerce 23.6, car marketplace 13.5, language learning 9.7. The fixture diff showed exactly one
profile changing.

The 21 website profiles from the field test still are not in the fixtures. That document's appendix
gives nine of the ten fields for each company but not `product_tags`, which is the heaviest weight in
the matcher at a cap of 12 points against 3 for archetype. Freezing them without it would freeze a
fixture that passes for the wrong reason.

---

## Two errors found in files already on main

**MercadoLibre.** `data/peers-fintech.csv` had NTM revenue as 46,939; both source screens say 46,874.
Corrected. Both figures round to 2.2x, so no ratio check could have caught it; the duplicate name
across two pulls did.

**Autohome minority interest, not changed, needs your eye.** The screen carries +179. The company
reports a noncontrolling interest deficit of US$(148)m at 30 June 2026. That is a 327 swing against a
29 enterprise value and would put the aggregate value at roughly -298. It has been left alone in case
the screen is picking up a redeemable or mezzanine interest the summary balance sheet does not
separate.

---

## Two things that still need a decision

**1. The private software set has diverged between the two sessions.** `origin/main` carries the
other session's 66 rows across 60 companies with the at-pricing rule applied row by row. This
session's container holds a different branch, `wip/private-merge-local`, with 95 transactions
including 50 private FINTECH rows that main does not have, and an investor file at 184 houses against
145. Neither is a superset. The right move is to re-verify the 50 fintech rows under the at-pricing
rule and add them to the 66. Nothing has been pushed over the other session's work. The golden
fixtures are deliberately generated against the data on MAIN so they reproduce for anyone else.

**2. The selector is Python and the site is Node.** `selector/match_reference.py` is an executable
specification, not a shippable component. The port should be done against the fixtures rather than by
eye, so it is correct by construction the moment `selector/golden.py` passes from the JS side.

---

## Data quality: what this batch changed about how the reveal must behave

Three rules came out of the verification and are now enforced in the data rather than in copy.

**A secondary is a mark, not a priced round.** Ten of the 44 private rows are secondary or mixed, and
the supplied sheet had several of them the wrong way round. `transaction_type` carries it.

**A "more than" figure makes the multiple a ceiling.** `bound` carries it, and the reveal must print
"at most" where it is set.

**An analyst back-solve is not a disclosure.** `denominator_basis` carries it. Six of the companies in
this batch have never published net revenue in any period; what circulates as their revenue is GMV
haircut at an assumed take rate.

And one that applies to the listed set: `mix_note` is a display requirement, not a comment. Amazon's
multiple is not a commerce multiple while a third of its gross profit is AWS, and a founder comparing
themselves to it has to be told so on the same line.

---

## Still blocked

`git push` to `DaniilRybak-code/fairway-valuation` is refused by the proxy in this session. The error
names the fix: the repository has to be added to the session's authorised sources. Read access works,
so the session can diff against main; only writing is blocked. Until that is set, work is delivered as
a patch that applies cleanly on top of `origin/main`.


---

## What the second verification pass changed, 24 August 2026

A revised sheet was supplied covering 23 e-commerce transactions. Every one of the 23 reconciled
arithmetically, as before. Nine were verified against primary sources by parallel agents, and the
work found more in Fairway's own file than in the sheet.

**The sheet's own errors.** OLIPOP was given a 2024 sales RANGE of $400m to $450m producing 4.1x to
4.6x. Nothing anywhere supports $450m: every contemporaneous account says sales "surpassed $400
million". The likely origin is splitting the difference between a Bloomberg story that the company
"eyes $500 million" and the $400m actually delivered, a target it missed. The 4.1x end was invented,
and presenting it as a range disguised that the only real figure is a floor. Investor lists were also
wrong on five rows in the same way each time, names imported from a different round of the same
company: Wellington into Rokt's 2025 secondary from its 2021 Series E, Tiger Global and Whale Rock
into StockX's April 2021 round from its December 2020 one, Founders Fund and Sequoia into Faire's
November 2021 round from its May 2022 extension.

**What the sheet got right that we had missed.** It separated GMV from revenue into its own columns
with an explicit proxy label. That was the right idea and the file now carries it as a full lane. It
also surfaced Away, Rent the Runway and both Thrasio rounds, three of which are keepers.

**What the sheet dropped that should not have been.** The revision covered 21 companies against the
44 rows already on the branch. Klaviyo and Meesho both price and both were verified, Klaviyo against
its S-1. They have been retained rather than dropped, along with twelve other companies the revision
does not reach.

---

## Item 4, the second defect the fixtures caught

`FLOOR_ADEQUATE = 12.0` was defeated the first time the tag corpus grew. Adding Rent the Runway gave
the consumer language-learning profile a best private match of 14.11, clearing the gate, on end
customer plus revenue model plus GTM plus purchase frequency: "sells a subscription to consumers and
acquires them organically". Product tags contributed 0.1 of a possible 12.0. Huel, AG1 and Harry's had
scored 9.69 on three of those four coincidences. Rent the Runway simply hit a fourth. Nothing about
the match got better; the sum just got longer.

The lesson is that a sum is not evidence, and an absolute gate on a sum of independent low-information
coincidences will always be crossed eventually. `FLOOR_TAG_EVIDENCE = 3.0` adds an orthogonal
condition: the heaviest and most specific axis, what the product actually IS, must carry real weight.

Freezing the fixtures is what exposed something worse. Four profiles had been passing for the wrong
reason all along. A restaurant point-of-sale profile was being shown Clio, Vanta, Guesty, Rippling and
Spendesk as its private comparables, with zero product-tag overlap against any of them. A core banking
profile was being shown CommerceIQ, Wiz and Celonis, all scoring between 12.00 and 12.07, right on the
gate. A UK car marketplace was being shown Faire. Those sets are now empty, which is the correct
answer.

Seven of the twelve profiles now return no private comparable set: language learning, quick commerce,
online pet retail, restaurant technology, core banking, consumer neobanking and car marketplaces. That
is not a regression. It is the honest map of what the private set covers, which today is D2C brands,
resale marketplaces, B2B procurement software, design tools and SMB payments, and nothing else. No
listed core group was emptied, because listed peers have real product-tag overlap.


---

## The private software and fintech set, which had never had this pass run on it

The consumer file has now been through full primary-source verification twice. `private-rounds.csv`,
which is the larger of the two at 66 rows across 60 companies, had never had it run at all. It had no
`in_medians`, no `bound`, no `denominator_basis` and no `transaction_type` column, so **every one of
its 66 rows fed medians as an unbounded point multiple from a primary round.** It has now been
triaged against its own labels, which is a floor rather than a verification.

What the file itself already admitted, once someone read the `revenue_status` column:

| what the row says about its own denominator | rows | now |
|---|---|---|
| Disclosed, or Reported contemporaneously | 32 | stay in medians |
| Third-party estimate | 28 | demoted |
| Estimated or reported proxy, range midpoint, at-round construction | 6 | demoted |

The median falls from **27.8x to 19.9x**, and the top of the range from 150.0x to 105.3x. The three
highest multiples in the whole set were all estimates: Decagon at 150.0x on a reported estimate,
Perplexity at 142.9x on a third-party estimate, Cohere at 95.5x on a third-party estimate. One row was
an explicit range midpoint, which is the same defect as the fabricated $450m on OLIPOP.

Two more structural fixes in the same pass. **18 rows carry "(> threshold)" in the metric and were
printing as point multiples**, because there was no bound column to carry the ceiling; they are now
bound `<=`. **10 rows are secondaries or tenders** identifiable only from free text in `round_type`,
including Canva, Figma, Notion, Gong and Clay; they are now labelled `SECONDARY` or `MIXED`. They stay
in medians, because a secondary can be a perfectly good mark and two of the consumer set's cleanest
rows are Vinted secondaries, but the reveal has to say which is which.

Every row in that file is now marked `STATUS-TRIAGE`, which means exactly what it says: the rule has
been applied to the file's own labels and not to primary sources. Until those 32 surviving rows are
checked the way the 23 consumer rows were, they are weaker than the consumer multiples no matter what
`in_medians` says. That is the next batch and it is the largest remaining data risk in the product.

**One thing the range maths still does not do.** `group_range` treats a bounded multiple as a point.
A row marked `<=` contributes its ceiling to the low, mid and high as though it were a value. With 18
bounded rows in the software set and 6 in the consumer set, roughly a fifth of the private universe is
a ceiling being read as a price. Fixing that is reveal work rather than data work and belongs with
item 5, but it should not be forgotten: the honest statement is "at most 14.0x", not "14.0x".

---

## Family as the first gate, and what it exposed

Daniil's rule: do not compare product tags until you have established the two things are the same
kind of business in the first place. Gate first, then rank. That is now how the selector works.

**The gate is family, not archetype.** Family is learned from the 318 listed rows, where it is already
assigned, by taking the family each archetype sits in. Every private archetype has a listed
counterpart, so the mapping is complete; only Vertical Software is mixed, 38 software against 9
fintech, and takes the majority. Archetype itself is deliberately NOT a hard gate. Measured across the
twelve profiles, gating on exact archetype equality costs real peers: a consumer neobank drops from 5
listed peers to 3, and a B2B procurement profile from 2 to 0. Archetype already carries 4.0 points in
the score, which is the right weight for a strong signal that is sometimes too narrow.

**What the gate found.** The measurement is more interesting than the gate.

*A core banking profile was being priced off payment processors.* Its listed core set was nCino, Jack
Henry, FIS, Temenos and EVERTEC. FIS and EVERTEC are payment processors, in the set only because they
share the fintech family and score on adjacent tags. The set is now nCino, Temenos, 74Software, Q2
Holdings and Blend Labs, which are actually core banking and digital banking software. The range moves
from 5.7x to 10.2x gross profit down to 2.3x to 5.9x revenue, so this was not a cosmetic change.

*An SMB payments profile was being shown consumer marketplaces as private comparables.* Whatnot,
Faire and Meesho were three of its five. That is precisely the failure Daniil described, and it was
happening in the shipped fixtures. It now returns nothing, which is correct, because the private
fintech set contains three companies.

*Three private companies were filed in the wrong family.* Airwallex, GoCardless and Qonto all carried
the archetype "Commerce & Payments Software", which maps to software. They are cross-border FX, bank
payments and digital business banking respectively. Retagged, the private fintech set goes from zero
companies to three, and a consumer neobank profile gains Qonto as its first private comparable. This
was the real bug; the gate is what made it visible.

**The honest caveat: the gate itself changes very little on its own.** Once the three retags are made,
the family gate alters exactly one listed set, and that one is a judgement call rather than a clear
win. A restaurant point-of-sale profile loses Toast, because Toast is classified fintech, which is
defensible given how much of its revenue is payment processing, but a reader might well want Toast in
a restaurant POS set. **Daniil should decide that one.** Everything else the gate would have caught,
the scoring was already catching. Its value is that it makes the guarantee explicit instead of
emergent, so it cannot quietly stop holding the next time the tag corpus grows, which is exactly how
`FLOOR_ADEQUATE` failed.

---

## Software and fintech private set, first verification batch

Eight of the highest-risk rows checked against primary sources. Five needed changing.

**Three rows are control transactions sitting inside a minority-financing median.** Semrush November
2025 is Adobe taking the whole company private at $12.00 a share. Mailchimp September 2021 is Intuit
buying 100%. And Scale AI June 2025, which was coded as a "strategic investment", is Meta paying about
$14.3bn for 49% of the equity, with the proceeds distributed straight out to existing shareholders
rather than retained, and the founder-CEO leaving to run Meta's superintelligence effort. A large part
of that consideration is talent, not enterprise value for the data-labelling business. All three are
now `CONTROL` and out of the medians.

**Two rows failed at-pricing on dates.** Figma's ">$700m ARR" was first published on 17 July 2024 at
the tender's close, two months after the 16 May pricing, and is sourced to people with knowledge
rather than to Figma, which declined to confirm. Canva's May 2024 row is wrong twice: the secondary
actually completed in early April 2024, and the $2,300m denominator matches no published figure. The
real number is "more than US$2.2 billion", published 24 May 2024, six weeks after the sale closed, and
the A$3.3bn in that same sentence is the AUD translation of it, which is where both the phantom 2,300
and 3,300 came from.

**Semrush also carried an equity-versus-enterprise error.** The $1,900m is equity value. Net cash was
about $262m, so enterprise value is about $1,638m and the comparable M&A multiple is roughly 3.7x, not
4.3x. That is the same class of error as the Trendyol row on the consumer side.

Also worth recording for the reveal: the denominators in this file are not interchangeable. Semrush is
guided GAAP revenue, Mailchimp a press estimate, both Scale rows are forward ARR forecasts, Canva and
Ramp are annualised run-rate, Figma is ARR. Only Semrush is anything close to trailing GAAP revenue.
Figma's own IPO filing shows Q1 2024 GAAP revenue of $156.2m, about $625m annualised, against the
">$700m" ARR, so an ARR multiple and a revenue multiple on the same company differ by about a tenth.

24 of the 32 in-medians rows in this file are still unverified. That is the next batch.
