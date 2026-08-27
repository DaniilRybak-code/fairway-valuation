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

---

## 26 August, evening: a bar that spans 4x to 105x is not a range

Daniil on Pazi and Fundraisly: *"What drives such a huge delta in comps multiples? Are we 100% sure
these are comparable? Was there differential in growth? Showing such a huge range is not an option
really, defeats the whole purpose."*

**The investigation.** Pazi's band was Semrush 4.3x, Notion 18.0x, Clay 50.0x, Sierra 105.3x, Decagon
150.0x. Two things drive it and only one of them is fixable today.

First, the comps are barely comps. Product-tag evidence across the whole set runs 0.1 to 0.8 out of a
possible 12. They share the token "AI" and almost nothing else.

Second, and this is the real answer to the question: **the spread is a growth spread.** Semrush is a
mature SEO suite taken private by Adobe. Sierra and Decagon went from nothing to nine-figure ARR
inside two years. On the listed side we can measure this effect exactly, and it is the largest single
driver in the data: the fastest quarter of 164 software names trades at 8.3x forward revenue and the
slowest quarter at 2.3x.

**The root cause is that the private lane is blind to growth.** `WP` sets `growth=0` and
`profitability=0`, and `select_private` calls the scorer with `use_fin=False`, because the private
rows carry no growth field at all. The one variable that best explains the spread is the one variable
the private matcher cannot see. Fixing that means adding growth to the private rows wherever it was
disclosed, and it is the next real piece of work on this engine.

**The temporary fix Daniil asked for, built.** Where the band's own high is more than
`DISPERSION_MAX` times its low, we stop drawing a bar and draw each contributor as its own diamond,
named, with its multiple. Measured across the 21 real profiles the spreads cluster between 1.7x and
4.9x; Pazi at 24.5x and Fundraisly at 11.6x are the only two outside that, so 6.0 separates the
genuine ranges from the non-ranges without catching anything healthy.

## And a gate that fell over when one row was deleted

Baozun was removed the same day, and it broke SellerClaw.

Baozun was the **only** listed company carrying the archetype "Commerce Enablement & Fulfilment".
With it gone that archetype had no family, so `family_of()` returned blank for SellerClaw, and
`same_family()` **fails open on a blank family** and handed back the entire universe. A merchant
account operator was then shown Sierra, Clay, Decagon and Semrush. Deleting one row silently disabled
the first gate for a whole archetype.

The map is now seeded from the consumer vocabulary, so every declared consumer archetype has a family
whether or not a listed row happens to carry it. Worth remembering as a shape: **a lookup learned
from data fails open when the data thins out, and fail-open on a gate is the wrong default.**

Recording the Baozun reason precisely, because the instruction and the file's own rule pointed
different ways. Daniil asked for it out "given it is small", and size is not a criterion here. It is
out on the data: a minority interest of $268m against a $165m market cap means the enterprise-value
bridge cannot be defended, so the 0.2x it printed was never a number we could stand behind.

---

## 26 August, late: growth bands, and what they do and do not fix

Daniil: *"I do not think we can source growth for private rounds, this is not something that is
routinely disclosed. If not, we should simply tag peers as mature (<15%), growing (15-30%) and hyper
growth (30%+). It is ok to have growing and hyper growth peers together, same as mature and growth.
It is somewhat not right to have mature and hyper growth in the same comparison. FOR PRIVATE ROUNDS
ONLY."*

**He was right that it is not routinely disclosed.** Sourcing across 39 rounds found a stated, dated
growth rate for 23 and nothing for the other 16. Blanks are therefore permissive: an unknown band
never excludes a comparable. Inventing one would be worse than not having it.

**The finding underneath is more useful than the gate.** Of the 23 rounds with a published rate, **21
are above 30%**. The only two that are not are Mailchimp at 20% and Semrush at 15%. The private file
is a hyper-growth file, so the band gate is a narrow instrument: it keeps Mailchimp and Semrush away
from a hyper-growth founder and that is all it can currently do.

**And it does not fix Pazi.** Semrush at 15% is GROWING, one band from HYPER, so the rule correctly
leaves it in. The 4.3x-against-105.3x spread survives.

### What actually explains Pazi

**Semrush was NYSE-listed.** Adobe bought it at the multiple the public market was already paying.
Sierra and Decagon are private rounds negotiated with one investor. Those are different KINDS of
price, not fast and slow versions of the same kind, and growth explains almost none of the gap.

So rows now carry `target_was_listed`, and every range carries `listed_target_n` and
`listed_target_names`. Not excluded, because a control deal is a benchmark and it prices. Named, so
the reveal can say the one thing a founder needs to hear: this comparable was priced by the stock
market, the others were priced by a venture investor.

That is a better lever than the growth band for the case that prompted the growth band, and it cost
one column.

---

## 27 August: retention, gross margin, and a regression that knows when to stay quiet

### Net revenue retention: 24 names became 51, and the headline stat moved

Sourced NRR from filings and calls for 48 listed software names that had none. **27 disclose it, 21
do not.** The 21 are now marked `DOES_NOT_DISCLOSE` with what they publish instead, so nobody
re-sources them.

The stat on the landing page has to change with it. On 24 names the top quarter by NRR traded at
16.3x and the bottom at 3.9x. On 51 names it is **11.1x against 2.9x**. The direction holds and the
gap is still the largest driver we can measure, but the magnitude was overstated by a thin sample.
Restricting to company-wide definitions only (43 names) gives 8.4x against 3.4x.

**The definitions are not interchangeable and the file now says so.** `nrr_scope` marks RESTRICTED
where a company publishes a cohort rather than a company-wide figure: Intapp's is cloud-only,
Samsara's counts only customers above $25,000 ARR, BILL's only customers using both products,
DocuSign's only direct customers, Teradata's only cloud and last printed in Q4-2025. `nrr_source`
marks the ten that exist only in an earnings-call transcript and appear in no filing. Datadog and
Atlassian publish a band, never a number.

### Gross margin: we did have it, except where it matters most

Daniil asked whether we already held it. The honest answer is three-quarters yes:

| file | before | now |
|---|---|---|
| listed consumer and commerce | `gross_margin_pct` on all 71 | unchanged |
| listed fintech | on all 87 | unchanged |
| listed software | not as a column, but derivable | **derived and stored, 158 of 165** |
| private rounds, both files | **nothing** | still nothing, and this is the real gap |

We price the consumer family on gross profit because EV/revenue moves from 0.9x to 2.8x across
margin quartiles while EV/gross profit sits at 3.6x and 3.1x. We cannot do that on the private side
at all, for any company, because no private row carries a margin. That is the single most valuable
missing field in the database.

### The regression method, and the two things that stop it

Built as `regression_range`. It fits the multiple against growth across the founder's own extended
peer set, wider than the football field's five, and reads a range off the line at their growth rate
plus and minus a tenth. Two gates, and both of them refuse more often than they permit.

**R2 must clear 50%, and it doubles as a test of the peer set.** Measured: the whole listed software
universe fits at 40%, and 27% once trimmed. By archetype it ranges from 15% for Business
Applications to 85% for Data, AI and Developer Tools. On the founder's own top 15 relevant peers it
clears 50% for 12 of the 21 real profiles at a 74% growth rate. So a regression on a broad "software"
bucket is worthless and a regression on a tight set is often excellent. If the multiples of the
companies we picked cannot be explained by their growth, we do not have a coherent set and we should
not draw a line through it.

**A line is only evidence inside the range it was fitted on.** The first version produced implied
multiples of 27x to 39x for a founder growing 74%, by extrapolating a fit far past the fastest peer
in it. Excellent R2, fictional answer. The banker's chart this copies reads its range at 17% to 22%
growth inside a cloud spanning 3% to 30%; it does not run the line off the page. The method now
refuses when the founder's growth sits more than 25% beyond the peer set's own maximum, and returns
the reason so the reveal can say it: at that growth rate there is no listed company to regress
against. That is a data gap with a name.

---

## 27 August: the growth bands were measuring the wrong population

Daniil: *"We need to reconsider the definitions, otherwise it does not make sense to have 90% of
names in hyper. Let's apply Gaussian distribution and derive growth definitions from it."*

**The 15 / 30 cut-offs were not wrong. They were calibrated to public markets.** On the 323 listed
companies we hold, the terciles of forward revenue growth fall at **8% and 17%**, so 15 and 30
describe a stock market almost exactly. On private rounds the terciles fall at **60% and 124%**.
Applying a public-market ruler to venture rounds put 36 of 40 rows in one bucket, which is a
constant rather than a classification.

**And a Gaussian on the raw rate is the wrong model, which is worth stating rather than quietly
fixing.** Growth is bounded below at -100% and unbounded above, so it is heavily right-skewed: on our
data, skew +3.16 and excess kurtosis +11.77 against 0 and 0 for a normal. A mean and a standard
deviation on that produce boundaries no data sits near. Taking ln(1+g) pulls it to +1.22 and +1.74,
and a Kolmogorov-Smirnov test gives D = 0.160 against a 5% critical value of 0.215, so log-normality
is not rejected. **That is the Gaussian to fit.**

Fitted on the 40 private rounds carrying a dated growth rate: mu 0.734, sd 0.462 in log space, so the
typical private round in this file grew **108% a year**, with boundaries at 65% and 162% splitting
14 / 15 / 11.

**REFITTED 27-AUG-2026 AFTER THE TRIAGE VERIFICATION.** Sourcing the triage rows added eleven dated
growth rates, most of them company disclosures rather than derivations, and the sample went from 40
to 51. The distribution got better behaved as it grew: skew fell from +1.22 to +1.06 and excess
kurtosis from +1.74 to +0.78, and KS D = 0.159 against a 5% critical value of 0.190. mu 0.845,
sd 0.543, so the typical private round grows **133% a year**. Boundaries again at plus and minus
half a standard deviation:

| band | range | rows |
|---|---|---|
| MATURE | below 77% | 21 |
| GROWING | 77% to 206% | 19 |
| HYPER | above 206% | 11 |

The split is more even than the first fit's, which is what a larger and less skewed sample should
do. Twelve rows changed band. The direction of travel is that the old boundaries were too low: names
we had called HYPER at 200%, including Writer, Miro, Airwallex, Apollo.io and Decagon, are simply
in line with the set, and names at around 70%, including PayFit, Guesty, 1Password and TravelPerk,
are slower than the set rather than in line with it.

**These bands are relative to private rounds, deliberately.** A company growing 50% a year is not
mature in any ordinary sense. It is slow *for a venture-backed company being priced against other
venture-backed companies*, which is the only comparison this gate governs. The founder is banded on
the same scale for the same reason, and listed companies are never banded at all: public comps are
what they are. The reveal should use the display labels rather than the machine values, because
telling a founder growing 50% that they are "mature" is a fight nobody needs.

**The gate now does real work.** On the same profile: a founder at 40% growth loses Lovable, Replit
and Clay and picks up Invisible, Turing and Scale AI; a founder at 250% keeps the fast names and
loses Semrush. Before the refit the gate moved almost nothing, because almost everything was HYPER.

`tools/refit_growth_bands.py` recomputes the fit, reports the KS test, and prints the boundaries.
The constants in the selector are its outputs. **n = 40 is thin and biased toward companies that
chose to publish a growth rate, so expect the boundaries to fall as coverage widens.** Rerun the
tool; do not adjust by taste.

---

## 27 August: closeness is a grade, not a pass mark. And the sector fork is built.

### "No shared vocabulary" was wrong, and the flag was mislabelling its own data

Daniil: *"What do you mean no contributing company shares real vocabulary with the founder? Means no
100% coincidences? As I mentioned, this is ok, we need to look for CLOSEST peers possible, if 100%
coincidence is not available."*

He is right and I described it badly. `triangulated` fired whenever no contributing row scored 3.0 on
product tags, and 3.0 means one EXACT tag match. So BrowserAct was flagged identically to Goldfish,
even though BrowserAct's comparables share **ten words** with it (agent, ai, api, browser, code,
proxy, scraper, scraping, web, no-code) and Goldfish's share exactly one, "ai". Calling both "no
shared vocabulary" was wrong about the first and useless for separating them.

Closeness is now graded on what the contributing rows actually share, and `shared_words` travels with
it so the reveal can print the overlap rather than assert it:

| grade | test | profiles |
|---|---|---|
| SHARED_PRODUCT | an exact product tag in common | OpenSEO, Bluerails, InsForge |
| STRONG_OVERLAP | four or more shared words | BrowserAct, AgentX, Context.dev, Elentaria, Pazi |
| PARTIAL_OVERLAP | two or three | AnySearch, Bond, Fyle, Upstream, Publora, SellerClaw, Skybridge |
| THIN_OVERLAP | one or none, usually generic | Fundraisly, Goldfish, Mailwarm, Honestly, Acti |

3 / 5 / 7 / 5. `triangulated` survives as an alias for THIN_OVERLAP only, so it now means what its
name says, and the honest headline is that **five of twenty sets are thin**, not seventeen.

### The sector fork, built as `selector/quiz_fork.py`

One rule enforced in code: `unbacked()` returns every question asking for a metric with no peer field
to compare it against, and it must stay empty. It caught one on the first run.

Two answers do real work today. `growth_pct` places the founder in a growth band, which gates the
private comparables and decides whether the regression can run at all. `gross_margin` decides whether
the reveal leads on revenue or gross profit, which for a consumer founder moves the multiple from
0.9x to 2.8x. The rest are stored and shown beside the peer figure.

**AI-native is a modifier, not a fork, and the first version got that wrong.** Treating it as its own
branch sent 13 of the 21 profiles down a path that asked only for a run rate and a three-month growth
rate. OpenSEO and Context.dev are AI-native SaaS: losing the retention and margin questions for them
is a straight loss, and being AI-native says nothing about which yardstick applies. The archetype
picks the fork; AI-native adds one question.

Nine to ten questions in total, six or seven of them required, which fits the promise on the page.

**What is untested.** Of the 21 real profiles, 19 take the software fork and 2 take e-commerce.
Marketplace, payments, lending, subscription and delivery have never been exercised against a real
company, because the test set is 20 software businesses and one D2C brand. That is the strongest
argument yet for the 20 additional test cases, and they should be chosen to hit those five forks.

### And then cut against Daniil's own rule

*"Fields that do not impact valuation are not asked."* Applied literally, question by question, the
fork lost a third of its questions the same day it was built.

Gone because he said they do not move the range: seats versus usage pricing, take rate on both
marketplace and payments, cohort retention, originations, loss rate, ARPU, churn, content cost,
orders per customer, contribution margin per order, and total payment volume.

**Gross margin is now asked in one fork only, e-commerce.** He endorsed it there and it earns its
place: across the listed consumer set the revenue multiple moves 0.9x to 2.8x between the lowest and
highest margin quartile while the gross-profit multiple sits at 3.6x and 3.1x. For software the same
measurement gives 3.4x against 5.0x, a much smaller effect, and he said plainly that margin does not
enter the valuation for an AI-native company. It comes out of every other fork. Nothing is lost on
the peer side: the column stays populated everywhere, and `denominator()` still switches to gross
profit on a wide peer-group margin spread without the founder answering anything.

**Volume is a cross-check, never an input.** GMV and GTV are optional and labelled as such. TPV is
gone entirely on his instruction, with one dissent recorded and then dropped: a founder who says
"$40m revenue" when they mean $40m of processed volume is out by about a hundred times.

**One question in the set is mine rather than his.** He asked to enrich the retention data, not to
ask the founder for it. NRR stays as an optional question because it is the largest gap we can
measure, 11.1x against 2.9x across the 51 listed names that disclose it. It is flagged in the file as
a call to be overruled.

The fork is now eight to ten questions with six or seven required.
