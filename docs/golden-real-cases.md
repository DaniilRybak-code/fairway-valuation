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
