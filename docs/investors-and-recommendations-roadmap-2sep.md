# Investors and recommendations: the pre-launch build

2 September 2026, Fable, at Daniil's instruction. A roadmap for Opus. Repo copy:
`docs/investors-and-recommendations-roadmap-2sep.md`; project copy under `claude/`.

Two features are promised on the landing page and neither is engineered yet: **recommendations**
("we tell you where we'd take the number into the room") and **the investors most likely to write
the cheque** ("you know who to call"). Daniil asked for a strategic look at two specialist tools
that do adjacent things, and the most efficient way to get close without pretending to be them.

---

## What the two tools actually do

**vcconf.com** is the matching tool attached to a virtual pitch event. A founder picks **one
stage, one region, and up to three sectors** (5 stages × 21 sectors × 11 regions), and gets a
ranked **top-20** out of a curated database of **293 active VCs, angels and family offices**. The
things that make it good are not machine learning — they are editorial discipline: **every
investor shown has done at least 2 deals in the last 12 months** (their explicit answer to the
scraped-list problem); every card carries **check size and thesis**, plus stage/sector/geo; and
matching degrades gracefully — exact stage+sector+geo first, then "most thesis-aligned", then
investors who invest agnostically or globally, then any 2-of-3 overlap. Their own line about why
check size is on the card: "A $25K angel and a $15M fund are different conversations, and knowing
which one you are looking at saves you the email."

**1752.ai** is a free AI pitch-deck analyzer from the 1752vc accelerator: upload a deck, get
"slide-by-slide pitch deck feedback and a prioritized fix list" in under 60 seconds, claiming
training on "25,000+ pitch decks… and real outcomes from investor meetings". Its rubric is worth
stealing even if the training claims are marketing: **clarity of problem framing, strength of
market sizing, defensibility of competitive positioning, rigor of financial projections, and the
overall arc of the story** — scored, then turned into a prioritized fix list.

The strategic reading: vcconf's moat is a small, current, well-tagged database plus honest facet
matching; 1752's moat is a rubric plus the confidence to rank the fixes. Neither is out of our
reach, because **we already hold the two hardest inputs**: a tagged evidence base and a
per-founder valuation read.

---

## What we already hold (checked against the repo tonight)

For investors: `data/private-round-investors.csv` is already an investor table — **145 houses,
one row each, with house_type, rounds and companies backed IN OUR SET, first_round and
last_round dates, and archetypes/industries/functions backed in our own vocabulary.** That is
the matching substrate vcconf charges $349 to touch: our archetype tags ARE the sector facets,
and last_round IS activity evidence. The consumer twin (`private-round-investors-consumer.csv`,
112 rows) carries the same story under a different schema and needs harmonising. On top of that,
`data-content.js` carries a hand-curated table of ~20 UK early-stage funds with cheque sizes and
theses in prose (Playfair, Episode 1, Seedcamp, SFC, Fuel, Octopus…), keyed by sector. And the
quiz **already asks the raise amount** (`responses.raise`, step 6) — the single strongest
matching facet, since check-size fit is what saves the founder the email.

For recommendations: the reveal already computes advocacy bullets, investor concerns, and the
`FIX_BY_REVENUE / FIX_BY_GROWTH / FIX_BY_PROFIT` playbooks; the honesty renderer produces
per-range caveats; and — our unfair advantage — every founder has a football field behind their
read, so a recommendation can be **quantified against the evidence** ("CAC payback by channel is
what decides whether your 74% growth prices off the regression row or the core band"). 1752 can
score a deck; it cannot tell a founder which fix moves which bar on their field.

---

## The design

### Feature ii — "who to call": a two-layer investor list

**Layer 1, the callable list: "Writing first cheques in your sector right now."** 8–12 curated
active early-stage investors matched to the founder. This is the vcconf emulation, and it must
copy their quality bar, not their scale: every investor on it carries **(a) at least one named,
dated deal from the last 12 months with a source URL, (b) a first-cheque range, (c) stage,
sector focus in our archetype vocabulary, and geography, (d) a one-line thesis.** An investor
row missing any of those does not render — same discipline as comps sourcing (a figure with no
source does not exist). Start from the ~20 funds already curated in `data-content.js`; grow to
~60–80 through Daniil's pull, ordered by where fixtures cluster (B2B software, payments,
marketplaces, D2C, delivery — the forks we actually serve).

**Layer 2, the evidence list: "The houses behind your reference rounds."** Drawn automatically
from the two investor files — the funds that backed the founder's own comparables, with the
round and date on each chip (Sequoia — Vanta, Jul-25). This layer nobody can copy, because it
is generated by the same selector that built the field: the investors arrive attached to the
evidence. It is honestly labelled as a map of who pays up for businesses like yours — mostly
growth-stage, mostly US — not a call list for a £600k-ARR seed round. Keeping the two layers
separate is the design decision that matters: **vcconf's failure mode is stale investors; ours
would be aspirational ones.**

**Matching, by reuse, not by new code.** Facets first: stage (from the raise amount and revenue
band the quiz holds), sector (archetype tags — scored by the same tokeniser that matches
comps), geography (founder country, already planned from IP). Then rank inside the facet
matches by tag-overlap score. Copy vcconf's degradation rules verbatim: not enough exact
matches → sector-agnostic/pan-geo investors → any 2-of-3 facet overlap, each step labelled on
the card ("broader fit") the way tiers are labelled on the field. Never pad to a fixed count:
six good matches beat twelve loose ones — our line, not theirs.

**The compliance rails (already partly written, now binding here too):** public information
only, no scraping behind logins, no contact details, no claim of introduction — the footer's
"a map, not an introduction — no affiliation or endorsement is implied" carries over to every
rendering of both layers. Styled text wordmarks, no logos.

### Feature i — recommendations: the "into the room" read

Not a deck analyzer — nothing is uploaded pre-launch. We systematise what the engine already
knows into 1752's best idea, **a scored rubric with a prioritized fix list**, on five dimensions
adapted to what we actually hold: **growth story** (their rate vs the peer set's), **quality of
revenue** (retention, recurring share, basis), **unit economics** (the FIX_BY playbooks),
**market position** (the concerns block — incumbents, cohort expansion), and **evidence gaps**
(what they could not answer, straight from the honesty flags). Each dimension renders three
sentences: where the founder stands against the named peer set, the ONE action to take, and —
the part neither tool can do — **the valuation consequence, named as a row on their field**
("this is the argument for pricing off precedents at 12.2–17.4x rather than the core band").
The fix list is ordered by range impact, not by rubric order. All strings go through the
`honesty_check` discipline: generated from the profile and range objects, no free-running LLM
inventing figures; the banker review remains the paid layer on top.

**Post-launch phase 2 (not before):** optional deck upload that feeds the 24-hour banker
review, with an LLM pre-read FOR THE REVIEWER (rubric-aligned notes, never shown raw to the
founder). That is the honest version of 1752's product — ours ends in a human.

---

## The build plan for Opus — ordered, ~4 days of build inside the 15

**Day 1 — the investor table.** One schema, one file: `data/investors.csv` — name, house_type,
layer (CALLABLE / EVIDENCE / both), stage bands, first_cheque_low/high, archetypes (our
vocabulary), geographies, thesis_one_liner, recent_deal_1/2 (name + date + source_url),
last_verified date. Generate the EVIDENCE layer mechanically from the two round-investor files
(harmonise the consumer schema while there); seed CALLABLE from the data-content.js table.
Manifest row, inventory-visible, durability protocol applies. Acceptance: `tools/data_inventory.py`
shows it; every CALLABLE row passes a `tools/investor_check.py` that refuses rows missing a
dated deal ≤12 months or a cheque range.

**Day 2 — matching and rendering.** Facet match + tag-overlap ranking (reuse the tokeniser),
degradation rules with tier labels, card rendering for both layers on the reveal (and the
Northsteer example on the landing updated to show the two-layer shape). Acceptance: an
investor-matching pass added to the golden suite — each of the 43 fixtures gets its investor
list snapshotted like ranges, so a data edit that flips a founder's list shows up in a diff;
spot-read by both agents during the fixture march (the Google-test habit extends: "seed
investors in [sector] UK" — names we miss go on the pull list).

**Day 3 — the recommendations renderer.** The five-dimension read over profile + ranges, fix
list ordered by range impact, strings through honesty_check, rendered into the reveal's
"Fairway's read" blocks (universe / advocacy / concerns / investors already have their spec —
this completes the fourth block's engine side). Acceptance: renders for all 43 fixtures with
zero invented figures (every number in a recommendation traces to a profile field or a range
object), read in full by Fable for the first ten.

**Day 4 — hardening and copy.** Degradation paths exercised on the 20-company triage batch
(the thin-set names are exactly where fallbacks fire); empty-state copy ("we do not have a
current list for your sector — the map below is the evidence layer"); legal copy carried onto
every card; Daniil reads ten investor lists and ten recommendation reads end to end.

**Daniil's inputs, alongside:** (1) the CALLABLE pull — active early-stage investors for the
five fork clusters, ~15 per cluster, each with a deal from the last 12 months and cheque range
(CSV into `data/raw/`, per the protocol — a screenshot is not a delivery); (2) a ruling on
list length (recommend 8–12 with a "fewer, current, checkable" line in the copy); (3) ten-list
read-through before connect.

**Sequencing against the launch:** this slots after the fixture-schema fix and runs parallel to
the fixture march — it does not touch the selector's pricing path, only consumes its outputs.
Week 2's engine→reveal wiring then connects ranges, honesty flags, recommendations and
investors as one payload. If the march slips, the CALLABLE layer ships at whatever size passed
`investor_check` — the activity rule is the feature; the count is not.

## What we deliberately do not do

No scraping of investor databases or anything behind a login; no contact emails; no
"warm intro" claims; no fixed top-20 padding; no deck upload before launch; no LLM-sourced
figures anywhere in either feature. And no imitation of the event mechanic (vcconf sells
meetings; we sell preparation — the honest framing is that our list tells you who to research,
their product sells you seven minutes).

Sources: [vcconf.com](https://vcconf.com/) · [VC Corner on the matching tool](https://www.thevccorner.com/p/free-vc-matching-tool-top-20-investors-2026) · [1752.ai](https://1752.ai/) · [1752vc launch release](https://www.abnewswire.com/pressreleases/1752vc-launches-multimodal-ai-pitch-deck-analyzer-trained-on-25000-decks-and-real-investor-decisions_802866.html)
