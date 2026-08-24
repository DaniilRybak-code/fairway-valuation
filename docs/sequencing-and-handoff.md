# Sequencing and status, 24 August 2026 (evening update)

Two sessions worked on Fairway today and neither could see the other's conversation. This is the one
place that reconciles them. It supersedes the seven-item list at the foot of
`claude/Fairway_profiler_website_test.md`, which remains the best account of the profiler field test.

---

## Status against the seven items

| # | Item | Status |
|---|---|---|
| 1 | Batch 2 plus the at-pricing rule merged to main | **Done** (28b900a, other session) |
| 2 | E-commerce and D2C data, plus a new taxonomy branch | **Done.** 72 listed names, 44 private transactions across 31 companies, and a third vocabulary family with two new fields |
| 3 | Wire the selector against the data and the token weights | **Done.** `selector/match_reference.py`, 318 listed and 110 private rows, token weights regenerated over five tag files |
| 4 | Golden test, fixtures before any tuning | **Done for 12 profiles.** Core, secondary AND private comps, denominators and ranges are snapshotted. It has already caught one real defect. The 21 website profiles are still not in it, for the reason below |
| 5 | Reveal copy: pre-revenue positioning mode, control-transaction labels | **Not started.** The private set now carries `transaction_type`, so the labelling that copy needs exists in the data |
| 6 | Batch 3: scraping APIs, email deliverability | **Not started** |
| 7 | Second random-20 profiler test on the broadened scope | **Not started, now unblocked** |

---

## Item 2: what landed, and the one thing that did not

The listed set is refreshed to 72 names. It now carries a ticker column, a revenue FY+2 column, and
growth restated as FY+2 over FY+1, which removes the currency-translation effect that made ASOS,
Autohome and Hemnet read as declining businesses. Hemnet goes from -14% to +24%.

The private set is 44 rows from 48 supplied, and it needed a rebuild rather than an import. Details
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
