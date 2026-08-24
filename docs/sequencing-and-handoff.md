# Sequencing and handoff, 24 August 2026 (late)

Two sessions worked on Fairway today and neither could see the other's conversation. This is the
one place that reconciles them. It SUPERSEDES the seven-item sequencing list at the foot of
`claude/Fairway_profiler_website_test.md`, which is otherwise still accurate and still the best
account of the profiler field test.

---

## Status of the agreed seven items

| # | Item | Status |
|---|---|---|
| 1 | Batch 2 + at-pricing rule merged to main | **Done** (28b900a, other session) |
| 2 | E-commerce / D2C data + a new taxonomy branch | **Done for LISTED. Private transactions still outstanding.** |
| 3 | Wire the selector against the data + token weights | **Done**, `selector/match_reference.py` |
| 4 | Golden test: snapshot expected comps as fixtures before tuning | **Harness built, 12 fixtures frozen. The 21 website profiles are not in it yet, see below.** |
| 5 | Reveal copy: pre-revenue positioning mode, control-transaction labels | Not started |
| 6 | Batch 3: scraping APIs, email deliverability | Not started |
| 7 | Second random-20 profiler test on the broadened scope | Not started, now unblocked |

---

## What item 2 actually delivered, and how it differs from the plan

The plan expected a private transaction dump in the shape of batch 2. What arrived was a LISTED
screen: 74 consumer, commerce and marketplace names, rows 9 to 82 of two CapIQ screenshots. So the
family is a public-comps family today. `data/peers-ecommerce.csv` and
`data/peers-ecommerce-tags.csv` are the result and `docs/consumer-commerce-taxonomy.md` is the
full write-up.

The plan's guess at what the taxonomy would need was right on every count: physical and D2C
archetypes, a UNIT_SALES-type revenue model (it is called PRODUCT_SALES), and margin structure. The
margin structure turned out to be the load-bearing part and it needed a new FIELD, not a new value,
which is the first time a vocabulary change has required a matcher change.

**Still outstanding for this family:** the private consumer and D2C rounds. Without them the
consumer reveal can show a public range and no private range, which breaks the lead-with-private
design. Vinted, ThredUp, Depop, Faire, Whatnot, Gopuff, Getir, Oda, Glossier, Ro and Cider are the
obvious candidates.

---

## What item 4 froze, and what it deliberately did not

`selector/golden.py` snapshots core and secondary lists plus the chosen denominator and quartile
range for twelve frozen profiles, four consumer, three software, three fintech, two crossover.
`python selector/golden.py` prints a readable diff and exits non-zero when anything moves.

The 21 website profiles from the field test are NOT in the fixtures. That document's appendix gives
nine of the ten fields for each company but not `product_tags`, and `product_tags` is the heaviest
weight in the matcher at a cap of 12 points against 3 for archetype. Freezing them without it would
freeze a weak fixture that passes for the wrong reason. They should go in as soon as the profiler
run that produced them can supply the tags.

---

## An error found in a file already on main

`data/peers-fintech.csv` had MercadoLibre's NTM revenue as 46,939. Both source screens show 46,874.
Corrected, with the reason in the file header.

The instructive part is why nothing caught it. Both figures produce 2.2x after rounding, so the
ratio reconciliation passed on both. It surfaced only because MercadoLibre appears in two pulls and
every other field matched byte for byte. The consumer pull carries revenue FY+0 and FY+1, which the
software and fintech pulls do not, and those give a growth reconciliation that a wrong revenue
figure fails. **Ask for FY+0 and FY+1 on the next refresh of the other two screens.**

---

## Two things that need a decision, not a default

**1. The private set has diverged between the two sessions.**

`origin/main` carries the other session's version: 66 rows, 60 companies, the at-pricing rule
applied row by row, threshold markers, a primary URL for the round and one for the revenue on every
row. That is the more rigorous artifact and it should be the base.

This session's container holds a different version on the local branch `wip/private-merge-local`:
95 transactions across 71 companies, because it merged in 50 private FINTECH transactions that
`origin/main` does not have, plus an investor file at 184 houses against 145 with lead separated
from participant on all 93 rounds.

Neither is a superset of the other and they must not be merged by taking one wholesale. The right
move is to re-verify the 50 fintech rows against the at-pricing rule and add them to the 66, which
is a data job of a few hours, not a merge. **Nothing in this session has been pushed over the
other session's work, and nothing should be until that is done.**

**2. The selector is Python and the site is Node.**

`selector/match_reference.py` is an executable specification, not a shippable component. The reveal
runs in `api/reveal.js` on Vercel. Porting is mechanical and should be done against the golden
fixtures rather than by eye, so the port is correct by construction the moment
`selector/golden.py` passes from the JS side.

---

## Two findings worth acting on, neither of them acted on here

**AI stance is underweighted, and the education category proves it.** The `consumer-learning-app`
fixture returns Duolingo at 4.4x, Coursera at 0.4x and Chegg at 0.4x. Those three differ on almost
nothing in the tag grid except `ai_stance`, which carries 1.0 point out of roughly 35. An
eleven-fold multiple spread driven by a 1.0-point field is a weight that does not reflect what the
market is pricing. Chegg is the cleanest observed price of AI displacement anywhere in the three
sets: NTM revenue down 47%, enterprise value 0.4x revenue. This should be tuned deliberately
against the fixtures, and it has not been touched.

**Token weights had to be regenerated and that is now a standing rule.** Adding 298 consumer tags
moved 45 tokens into the generic band and pushed ten hard: "marketplace" from 6 carriers to 29,
"online" 16 to 44, "commerce" 10 to 31. Without regenerating, a B2B procurement founder whose site
says "supplier marketplace" starts pulling eBay into scoring range on one shared word. Any tag
change must be followed by `python selector/regenerate_token_weights.py` and then
`python selector/golden.py`.

---

## Still true, still blocked

`git push` to `DaniilRybak-code/fairway-valuation` is refused by the proxy in this session. The
error names the fix: the repository has to be added to the session's authorised sources. Read
access works, so the session can see main and diff against it; only writing is blocked. Until that
is set, files are delivered directly and applied by hand.
