# Handover to Fable, 3 September 2026, end of day

All twelve checks pass. `sh tools/check_all.sh` is the one command.

## The headline: the march is done

**102 fixtures, 90 refine the peer universe.** The gate was 100 and we are past it.

Daniil, tonight: "March should be done to 100, without revenue numbers, just checking that we have
sufficient depth and breadth of data lake. Take product hunt and YC companies randomly."

So it was scored on the peer universe alone, which needs no revenue on any fixture, and it went
from 43 to 102 in one evening rather than the 8.1 a day the roadmap was asking for.

| | |
|---|---|
| fixtures | 43 to **102** |
| refine the peer universe | 39 of 43 to **90 of 102** |
| distinct archetypes exercised | 18 to **26** |
| new archetypes now tested | Card Issuing & BaaS, Commerce & Payments Software, Crypto & Digital Assets, Cybersecurity, Design & Engineering, Financial Data & Index, Insurance Technology, Wealth & Capital Markets Platform |

**Every one is a real company.** 44 read off its own `ycombinator.com/companies` page (Summer,
Spring, Winter and Fall 2026 batches), 13 off its own Product Hunt page. The one-line description
is the company's own published tagline, not a paraphrase. Five candidates were rejected during
sourcing because the slug resolved to an older company: short common-word slugs get reused, which
is the failure mode to watch if you extend this.

**Random means random.** Three are outside the market this product is aimed at, and they are kept
rather than quietly dropped: Hop Aero (rocket cargo), Ultrasonium (metal manufacturing), Apollo
Atomics (compact nuclear reactors). `OUT_OF_MARKET` in `golden_profiles.py` names them so the
score reads both ways. **In-market: 99 fixtures, 89 pass, 90%.** A fixture set curated down to
what we already cover would have scored better and told us nothing.

## What the march found, which is the point of running it

Ten in-market failures, and **eight of them are the same failure**: a lane holding exactly one
usable name, so there is no range. `tools/thin_lane_diagnosis.py` checked our own database for the
next best comparable in each case and **all seventeen thin lanes are genuine sourcing requests**.
The data lake is deep on the listed side and thin on the private side for specific profiles.

The pull is written and ready for Daniil's next batch:
`docs/prompts/peer-sourcing-4sep.md`, 17 gaps across 15 companies, all needing a revenue-carrying
comparable. The hardest four are named in it: agent payments and stablecoin rails (our card
issuing set is three names), fractional collectibles (the engine reached for neobanks), consumer
voice productivity (it reached for enterprise conversation intelligence), and vertical software
for single trades.

Nine fixtures now pass **with an empty lane**: acti, blindspot, clera, evergrove, goldfish, honen,
insurf, orchids, projectx. **Daniil has still not ruled on whether an empty lane should fail.** It
was three fixtures this morning and it is nine now, so the question is getting louder.

## Investors: Day 2 is finished

The three missing pieces from Fable's Day 2 are built: tag-overlap ranking on the shared
tokeniser, `investors.js` rendering both layers, and the two-layer shape on the Northsteer landing
example. **92 of 92 callable houses render**, up from 62 of 140 this morning.

Two things worth your verification pass:

- **A check now bites on the Python-to-JS seam.** `check_investor_compliance.py` parses
  `investors.js` for every field it reads off a card and fails if the payload has no such field. I
  broke it on purpose to confirm it bites. That seam is where a field goes missing silently, and
  it is the same shape as the 509-row refresh that sat unused for two days.
- **Geography was scored on nothing.** The matcher compared the founder's country to the fund's
  line with a substring test, so "United Kingdom" never matched a fund saying "UK". No fixture
  carries a country, so nothing caught it. There is now a country table and a test that two
  founders differing only by country must get different lists.

**Daniil's ruling tonight:** an unpublished cheque range or geography no longer blocks a house.
Sixteen active houses were withheld because their websites are thin, Benchmark and Thrive among
them. The card says "First cheque not published" rather than leaving a blank. Stage bands stay a
hard gate, and a house that publishes its terms outranks one that does not.

7 of 102 fixtures get fewer than three investor houses. All seven are consumer software, consumer
health or consumer learning, which is the same gap `docs/investor-sourcing-gaps.md` already names:
the seed screen has eight coarse sectors and neither consumer software nor edtech is one of them.

## The service shell: three of four answered

`docs/service-shell-decisions-3sep.md` has the full working. Short version:

- **Entity.** Nothing registered. The pilot can run as a sole trader, but the disclaimer is
  written for a company that does not exist and needs a real name and an address for service.
  Replacement text is drafted and waiting on his word.
- **Retention.** He asked 14 or 30 days. Both are lead-capture numbers for what is a paid
  professional engagement. Recommended three clocks: 90 days for a non-buyer, six years from
  delivery for a paid file (the contract limitation period), and de-identified calibration data
  kept, with a caution that revenue plus sector plus month can re-identify a startup.
- **Price.** Flat 750. **Currency not stated, and that is the one thing blocking the page.** Also:
  the meta description still ends "Free", which has to change the day a price appears.
- **Stripe.** Later, agreed. Nothing blocks; a pilot of five to ten can invoice by email.

**The item ahead of all of them:** he is an MD in fintech coverage under SM&CR and this is an
outside business interest close to what he covers. That answer gates whether he can take the first
£750, and it is not in his gift. Flagged to him plainly.

## Where to look first tomorrow

1. **Verify the march.** Spot-audit ten of the 59 new fixtures with the Google test. The tagging
   is my reading of each company's own tagline, and the archetype field is what drives peer
   selection, so a mis-tag is the failure mode. `alloovium`, `tash`, `agentcard`, `wispr-flow` and
   `marble` are the ones I am least sure of.
2. **Confirm the thin-lane diagnosis is honest.** Seventeen lanes said to be sourcing requests
   rather than matcher faults is a strong claim. Plant a comparable that should have been found
   and check it is.
3. **The empty-lane question.** Nine fixtures now. Worth a recommendation from you rather than
   waiting for it to reach twenty.
4. **The landing round** when his next markup arrives: the two-layer investor block is in, and the
   legal placeholders are ready to come out the moment the entity and currency land.

## Open, unchanged

- `asset_intensity` withdrawn from the ecommerce fork: only question in the quiz with no `why`,
  and nothing read the answer. Worth wiring, not deleting.
- Day 3 remainder: unit economics and market position dimensions of the recommendations rubric,
  and the recommendations renderer into the reveal.
- Consumer software and edtech have no fund in the investor screen and thin private comparables.
  The same gap shows up in both workstreams, which suggests one pull fixes both.
