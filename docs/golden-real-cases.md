# The golden set moved to real companies, 25 August 2026

## What changed

The golden suite was twelve profiles I invented. It is now twenty-one real companies, profiled
from their live websites: twenty Product Hunt launches from around August 2026 plus fyle.io.
The twelve invented profiles are retired, kept in `golden_profiles.py` as evidence rather than
deleted, because the contrast between them is the finding.

## The finding

Run against the same engine on the same day, against the best listed match:

| | best score | tag points | returned a comparable set |
|---|---|---|---|
| twelve invented | 22.8 to 41.3 | 7.3 to 12.0 | 12 of 12 |
| twenty-one real | 8.0 to 22.6 | 0.0 to 3.9 | **1 of 21** |

The invented profiles were never a test. Writing them I reached for the dataset's own tag
vocabulary without noticing, so every one matched by construction. They passed because the
answer had been written into the question. The real companies wrote their own tags, on their
own websites, and share almost nothing with our tag file.

Any weight tuning done before this point would have been tuning against a rigged sample.

## What the real cases forced

**A blank no longer matches a blank.** Only `asset_intensity` and `purchase_frequency` enforced
that. Everything else used plain equality, so two blanks matched and paid full points. Six of
the twenty-one publish no pricing at all, so `revenue_model` is genuinely empty for them, and
the first one to meet a peer row with the same gap would have been paid 3.5 points for the two
of them being equally silent.

**Growth and margin scoring tolerates an empty profile.** No website publishes either figure.
Previously the scorer raised TypeError on a profile with none, which is also what every
pre-revenue founder will look like.

**Anchoring replaced the bare tag floor.** The floor was calibrated on the invented profiles.
A match now anchors by either route: real product vocabulary in common, or a shared
non-Horizontal end market plus a shared archetype. Horizontal is not an end market and never
anchors.

Fyle is the case that proves the point. A nail-care brand scoring 0.1 tag points against FIGS,
blocked outright by the old floor, now correctly returns FIGS, e.l.f. Beauty, Warby Parker, On
Holding and ASOS from the listed set, and Quince, SKIMS, Vuori, Glossier and Harry's from the
private set. Context.dev, which shares only the archetype "Data, AI & Developer Tools" with
MongoDB, an archetype spanning everything from a database to a scraper, stays blocked.

**Anchoring is tested per member, not on the leader.** Anchoring only the top candidate let a
restaurant point-of-sale profile keep Clio and Vanta as private comparables, because Guesty
anchored the set on Hospitality and the relative floor carried the rest in behind it.

Result: listed sets go from 1 to 3 of 21, private from 2 to 6.

## The bigger finding: this is mostly a DATA problem

Fifteen of twenty-one still return nothing, and the reason is not the gates. Ignoring every
gate and asking what the closest thing we own is, eight of the twenty-one have nothing scoring
16 or better anywhere in 434 companies.

The fifteen sort almost exactly onto the four company-gap clusters the field test named on 24
August, before any of this was measured:

| cluster | companies | predicted by the field test |
|---|---|---|
| personal productivity | Goldfish, Upstream, Bond, Acti | yes, "4 of 21" |
| web scraping and crawling | BrowserAct, Context.dev | yes, "company gap, not just a tag gap" |
| agent ops, evals, orchestration | AgentX | yes |
| email deliverability | Mailwarm | yes |
| sales engagement | Fundraisly | yes |
| the rest | Publora, Elentaria, SellerClaw, Pazi, AnySearch, Honen | agentic categories, mostly new |

MCP is the one gap that closed: Skybridge now matches Anthropic, because MCP was added to
Anthropic's row in batch 2. That is the proof that filling a gap works.

**The private set is the primary universe for these founders, not the listed set.** Six of the
twenty-one get a private set against three listed, and the private matches are better ones:
OpenSEO to Semrush, Skybridge to Anthropic, InsForge to Databricks, Fyle to Quince and SKIMS.
That is consistent with the product thesis on the landing page: for a seed-stage founder, what
matters most is what companies like them raised at.

---

## 25 August, evening: what the batch did to the 21, and two defects it exposed

Ten private rows and two listed rows were added. Ten of the twenty-one profiles moved. Five of
those moves are the gap closing exactly as predicted, and two are regressions that are worth more
attention than the wins.

**Where it worked.** Oxylabs is now the leading private comparable for BrowserAct, Context.dev,
AnySearch and AgentX, and it is the only web-data company in the file with a clean, at-pricing,
point multiple. BrowserAct is the clearest case: it was being shown Sierra, Clay and Decagon, which
are AI customer-service and GTM companies with nothing to do with running scrapers, and its range
was 33.0x to 105.3x. It is now Oxylabs first at 10.3x with a 10.3x to 33.0x range. Similarweb
entered OpenSEO's listed set and ZoomInfo entered Fundraisly's core listed set, both on the first
pass, which is what the two names were bought for.

**Defect one: one narrow tag promotes a candidate past four better ones.** InsForge, a
backend-as-a-service for AI coding agents, previously drew a four-name private range from Lovable,
LangChain, Replit and Cursor. It now draws a single-name DIAMOND on Algolia at most 22.5x. The
reason is that Algolia and InsForge share exactly one product tag, "Vector Search", which is worth
3.0 points, which is exactly `FLOOR_TAG_EVIDENCE`. That single tag makes Algolia DIRECT, DIRECT
beats ADJACENT outright, and the ladder stops at the first tier that has any member at all. So one
coincidence evicts four reasonable comparables. Its listed set collapsed the same way, to Elastic
alone.

This is the same failure shape as the two gate defects already recorded above: an absolute
threshold crossed by a single low-information signal. The candidate fix is that the ladder should
FILL from the best tier downward until it has the names it wants, rather than STOP at the best tier
that has one, and the group should then be labelled by its WEAKEST member rather than its best.
InsForge would read: Algolia, Lovable, LangChain, Replit, Cursor, labelled ADJACENT. That is not
implemented, deliberately, because it changes the meaning of the tier label and that is a product
decision rather than a bug fix.

**Defect two: an ADJACENT set can carry no product-tag evidence at all.** Publora, a social
publishing API, draws five private names of which the best scores 0.3 on product tags and the other
four score 0.0. They qualify on archetype, buyer, go-to-market and revenue model: all five are
developer-facing, consumption-priced infrastructure. That is a real similarity and it is not
nothing, but it is not a product similarity, and the reveal will draw a range from it. This is
pre-existing rather than new; the batch only made it visible by putting Oxylabs at the top of a list
it does not belong at the top of. `FLOOR_TAG_EVIDENCE` guards the DIRECT label, not admission to
the set, so a set with zero tag overlap can still be shown as ADJACENT.

**Leave-one-out, measured on today's data.** Each tagged company is turned into a profile, removed
from its own universe, and we ask what share of the returned group carries its archetype. Listed 78
percent across 320 companies with 9 empty sets; private 83 percent across 127 companies with none.
On the looser test that also accepts a secondary-archetype match, 98 and 97 percent. The private
lane is now the stronger of the two, which was not true a week ago and is the right way round for
this product.

---

## 26 August: the ladder fills instead of stopping, and coverage goes from 6 of 21 to 20 of 21

Daniil ruled on both defects the same morning they were raised.

On defect one: *"One coincidence for sure should not evict four decent comps. The point is not to get
a comp that is 100% same business, close enough is good enough."*

On defect two: *"If nothing matches very closely, we need to broaden the set and triangulate between
most similar comps."*

Three changes follow, and they are one idea.

**The ladder fills, it does not stop.** The core group is now built by walking DIRECT and then
ADJACENT, taking anchored names first and topping up behind them, and it falls to BROAD only if
neither pricing tier produces anything at all. InsForge reads Databricks, Algolia, Oxylabs, Lovable
and LangChain instead of a single Algolia diamond.

**A mixed set is labelled by its weakest member.** `set_tier` returns the maximum rather than the
minimum on the tier order. One direct hit does not make four adjacent names direct, and claiming
otherwise would be the same overstatement the diamond rule was built to stop.

**Business nature leads and recency orders within it.** The widening 24-month window is gone. It had
quietly become a selection criterion: the first version of the filling ladder pushed Algolia, the
only anchored comparable InsForge has, out of its own set because five adjacent names happened to be
more recent. Candidates are now sorted by tier and then by date inside the tier, and `months` stopped
being an input the loop widens and became an output, the age of the oldest transaction actually
shown, so the reveal can caveat it.

### What that costs and what it buys

| | before | after |
|---|---|---|
| of 21 real profiles, listed core set returned | 3 | **21** |
| of 21, private set returned | 6 | **20** |
| of 21, private range printed | 6 | **19** |
| leave-one-out, listed, strict archetype | 78% | 74% |
| leave-one-out, private, strict archetype | 83% | 78% |
| leave-one-out, both, loose archetype | 98% / 97% | 98% / 97% |

Strict precision falls because we return more names and more of them sit one rung out. Loose
precision does not move at all, which says the extra names still share an archetype rather than
being noise. That is the trade Daniil asked for, stated in numbers.

### Two flags so the copy can tell the truth about what it is showing

Coverage is now close to total, and **18 of the 19 private ranges are triangulations**: not one
contributing company shares real product vocabulary with the founder. That is a fact the reveal owes
the founder, so every range now carries it.

- `tag_evidence` the best product-tag score among the rows that actually feed the number.
- `triangulated` True when that score is below `FLOOR_TAG_EVIDENCE`, meaning no contributing
  company shares product vocabulary with this founder. It is still the best answer we have; it is
  not the same claim as a comparable set, and the sentence underneath it should differ.
- `anchor_dropped` True when the set's own best-anchored name scores above the floor but the
  contributing rows do not, meaning **the closest comparable is named in the set and prices
  nothing.** OpenSEO is the case: Semrush matches at 12.0 tag points and leads the set, but its only
  transaction is the Adobe take-private, which is a control deal and can never sit in a median of
  minority financings. The number the founder sees is built from Clay at 50.0x and Klaviyo at 32.6x.
  Showing that without saying it would be the worst kind of quiet dishonesty, because the set looks
  authoritative precisely because of the name that is not in it.

## 26 August, later: a control deal prices, and nothing unrelated is shown

Two rulings from Daniil, and they pull in opposite directions on purpose.

*"Why are you excluding take private from the median? In the absence of clean comps, we should not
exclude data based on the fact that this was a controlled deal. We should have the respective note
(visible when someone hovers over the range), but we should not exclude this entirely."*

*"It is ok not to have 100% comparables. It is important NOT TO SHOW COMPARABLES THAT HAVE
ABSOLUTELY NOTHING TO DO WITH THE FOUNDER'S BUSINESS. And important to explain the selection."*

### Rule four: a control deal is a benchmark and it prices

Four control rows carrying a sound multiple now feed medians: Scale AI Jun-25 at 14.5x, Mailchimp
Sep-21 at 15.0x, Semrush Nov-25 at 4.3x, Salesloft/Vista Dec-21 at most 23.0x. The software median
moved from 24.8x on 30 rows to **22.8x on 34**.

OpenSEO is the case that forced it, and it is the same case that produced the `anchor_dropped` flag
the day before. Its best comparable by a distance is Semrush at 12.0 tag points, and Semrush's only
transaction is the Adobe take-private. Under the old rule the founder saw Semrush named at the top of
the set and a range built from Clay at 50.0x and Klaviyo at 32.6x, neither of which shares a tag with
them. **The exclusion made the answer both worse and less honest.** OpenSEO now reads 4.3x to 50.0x
with `tag_evidence` 12.0 and `triangulated` False, and `anchor_dropped` no longer fires.

What does not change: a buyer of the whole company pays for control, so these multiples sit above
what the same business would fetch in a minority round. Every range carries `control_n` and
`control_names`, and the reveal must surface them on the name rather than in a footnote.

### The relevance gate: something, or nothing

A candidate now reaches no tier at all, secondary included, unless it has one of two things:

- **any shared product vocabulary**, however weak. Not the 3.0 that anchors a DIRECT label, just
  more than nothing.
- **the same specific, non-Horizontal end market.** This is what keeps Rokt and Yotpo next to
  SellerClaw: no shared tag, but all three live in Retail & E-commerce and that is a real
  relationship. Horizontal never counts, because it is the absence of an end market rather than one.

It removed 28 of 97 private members across the 21. **Mailwarm is the case that shows what it buys.**
An email warm-up and deliverability product was being shown Sierra, Clay, Decagon and Semrush, four
companies with no connection to email whatsoever. It now reads Apollo.io ("both do Cold Email"),
Mailchimp and Klaviyo. Nothing was added to the data to achieve that; the noise was simply removed
and what was underneath it turned out to be right.

Publora falls from five names to a set led by Oxylabs and Anthropic ("both do MCP"), which is thinner
and true. Zero of the 87 remaining private members now have no relationship at all to their founder.

### One more route through axis B, because the two changes together went too far

The relevance gate emptied OpenSEO's listed core set. OpenSEO is Horizontal, so axis B demanded a
horizontal peer with the same END CUSTOMER, and Similarweb sells to a line of business while OpenSEO
sells to developers. Similarweb shares two exact product tags with it, Keyword Research and Rank
Tracking, and is plainly its closest listed comparable. Being told who someone sells to is a proxy
for what they do; sharing the product vocabulary is the thing itself, so it should not lose to its
own proxy. Anchored product evidence now satisfies axis B for a Horizontal profile. OpenSEO's listed
core is Similarweb, at tier DIRECT, reasoned "both do Keyword Research, SEO, Rank Tracking".

### Explaining the selection

Every member of every set now carries a `reason`, built from the score's own working, and it is
recorded in the fixtures so it is tested rather than decorative. Examples from tonight's run:

- Fyle to Glossier: "both do Beauty; same type of business; same end market; same business function"
- InsForge to Algolia: "both do Vector Search; related type of business; same business function"
- SellerClaw to Rokt: "related type of business; same end market"
- Publora to Anthropic: "both do MCP; same type of business; same kind of customer"

### Where it lands

| | before today | after |
|---|---|---|
| of 21, listed core set returned | 3 | **20** |
| of 21, private set returned | 6 | **20** |
| of 21, private range printed | 6 | **19** |
| private members with no relationship at all | 28 of 97 | **0 of 87** |
| ranges flagged `anchor_dropped` | 2 | 1 |
| ranges flagged `triangulated` | 18 of 19 | 17 of 19 |
| leave-one-out, listed / private, strict | 78% / 83% | 74% / 80% |
| leave-one-out, listed / private, loose | 98% / 97% | 98% / 97% |

The two profiles that return nothing are the honest ones. Goldfish, a local-first AI memory layer,
has no listed core set because personal productivity is still an empty cluster, and Honen has no
private set. Those are gap-log entries, not failures.

Seventeen of nineteen ranges are still triangulations. **That is now the single number to manage.**
We are not short of comparables any more; we are short of close ones, and every future data batch
should be judged on whether it moves the triangulation count down rather than the coverage count up.

## 26 August, last change of the day: the range is priced off the closest band only

Daniil, on OpenSEO: *"If the closest peer reads 4.3x, this is what needs to be shown (as a
diamond). THEN if some other peers (with lower relevance) trade higher, we could show them
separately at the end of the field with indication of their multiples, indicating that we can
position towards them with right arguments. We cannot take an average of 4.3x and 50x, this
discredits the whole range."*

He is right, and it is the flaw in the filling ladder as first built. Filling the SET was correct.
Letting the whole filled set compute ONE number was not.

OpenSEO's set is Semrush at 4.3x, which is almost exactly its business, plus Clay at 50.0x and
Klaviyo at 32.6x, which are adjacent at best. Blending them produced a midpoint of 32.6x. No banker
would sign that and no founder should be shown it.

So the range is now computed from the closest band that has a price, and nothing weaker joins it.
Everything priced in a weaker band becomes `positioning`: named, with its multiple, drawn at the end
of the field rather than inside the bar. That is not a demotion. A founder who can argue they belong
nearer Clay than Semrush has a real case, and the field should hand them the case instead of quietly
averaging it away.

OpenSEO now reads a diamond at 4.3x on Semrush, with Klaviyo at 32.6x and Clay at 50.0x listed as
positioning. InsForge reads a diamond at 22.5x on Algolia, with Oxylabs at 10.3x and Lovable at
33.0x as positioning.

**What this does not fix.** Banding only separates names that sit in different bands. Pazi still
reads 4.3x to 105.3x and Fundraisly 4.3x to 50.0x, because every one of their names is ADJACENT and
they genuinely span the market. Those ranges are flagged `triangulated`, which is true but is a
weaker warning than the range deserves. If a spread inside a single band is this wide, the honest
answer may be that we have no range at all, only a set of positions.
