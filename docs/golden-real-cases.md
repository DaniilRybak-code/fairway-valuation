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
