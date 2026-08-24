# The third vocabulary family: consumer, commerce and marketplace

Added 24 August 2026 with `data/peers-ecommerce.csv` (74 listed names) and
`data/peers-ecommerce-tags.csv`. This is step 2 of the sequencing agreed the same day, with one
difference from what was planned: the data supplied was a LISTED screen, not a set of private
transactions, so this is a public-comps family. The private consumer and D2C transaction dump is
still outstanding.

---

## Why the software vocabulary could not simply be extended

One measurement decides it.

    gross margin, listed software     24% to 98%, median 77%
    gross margin, this set             8% to 100%, and it is bimodal

In software, revenue means roughly the same thing from one company to the next, so EV/revenue is a
fair comparison. Here it is not. Across the 62 rows in this set that carry a usable gross profit
line and are not flagged out of medians:

| gross margin bucket | names | median EV / NTM revenue | median EV / NTM gross profit |
|---|---|---|---|
| under 30% | 8 | 0.7x | 2.8x |
| 30 to 50% | 13 | 2.2x | 5.0x |
| 50 to 70% | 14 | 1.8x | 3.0x |
| 70% and above | 28 | 3.2x | 3.6x |
| **spread, highest over lowest** | | **4.3x** | **1.8x** |

Most of the apparent valuation gap between Carvana at 1.7x and Rightmove at 7.9x is an accounting
difference, not a valuation one: one books the price of the car as revenue and the other books the
listing fee. Moving to gross profit halves the distortion. It does not remove it, and the doc
should not claim it does.

**The rule that follows.** For any subject tagged into this family, gross profit is the PRIMARY
denominator and revenue is the secondary one. The reveal shows both, and leads with gross profit
whenever the subject's gross margin sits more than 15 points from the peer group median, or the
group itself spans more than 30 points. `denominator()` in the selector implements exactly that.

---

## What the family contains

**Twelve archetypes**, each defined by the economic engine rather than the sector, on the same
discipline as the ten fintech archetypes:

| archetype | names | what makes it its own engine |
|---|---|---|
| Classifieds & Listings | 16 | the supply side pays to be listed; no transaction, no inventory |
| Third-Party Marketplace | 12 | take rate on volume it never funded |
| Owned-Inventory Retail | 11 | revenue is the full ticket price of goods it bought |
| Local Delivery & On-Demand | 7 | a physical fulfilment leg and city-level density |
| Consumer Brand | 7 | owns the brand; gross margin is a brand outcome |
| Travel Booking & OTA | 5 | commission on inventory it does not hold |
| Streaming & Digital Media | 5 | the content is an asset and a cost |
| Freelance & Services Marketplace | 3 | matches labour, and leaks off-platform |
| Dating & Social Network | 3 | monetises a graph with no supply side to pay |
| Online Learning | 3 | the category most directly exposed to generative AI |
| Commerce Enablement & Fulfilment | 1 | operates someone else's store for a fee |
| Gaming & Virtual Economy | 1 | earns on virtual goods inside a world it runs |

The last two have one member each and need a data batch before they can select anything.

**Four functions** describing the operating core, orthogonal to the archetype, which is what makes
the core/secondary split work: Commerce Operations (27), Marketplace Operations (18), Listings &
Discovery (17), Content & Community (12). A cars-classifieds founder and a jobs-classifieds
founder share the function and differ on the end market, so one lands in core and the other in
secondary. That is the mechanism, not a coincidence.

**Four new revenue models**: GMV_RETAIL, LISTING_FEE, SUBSCRIPTION_CONSUMER, PRODUCT_SALES.
TAKE_RATE, ADVERTISING and SERVICES_LED carry over unchanged. GMV_RETAIL versus TAKE_RATE is the
Carvana versus eBay distinction and it is worth roughly 3x of multiple on its own.

**Six new industry values**, used as the consumer category: Travel, Food & Grocery, Apparel &
Beauty, Education, Recruitment & Work, Dating & Relationships. Automotive, Real Estate, Media &
Gaming, Retail & E-commerce, Healthcare & Life Sciences, Home & Field Services, Financial Services
and Horizontal all carry over.

**Three new go-to-market motions**: PAID_ACQUISITION, ORGANIC_BRAND, NETWORK_EFFECT. ENT_SALES and
CHANNEL keep their software meaning where they are literally true.

**Three new product roles**: DESTINATION, AGGREGATOR, BRAND.

---

## Two new FIELDS, which is a first

Every previous vocabulary change was a new VALUE in an existing field, and the architecture doc's
guarantee held: no engine change. This set needed two new FIELDS, and that is a two-line matcher
change plus two weights. Recording it plainly because the guarantee is now qualified.

**`asset_intensity`**: RESALE_INVENTORY, OWN_PRODUCT, CONTENT, FLEET_OPS, NONE, MIXED. This is
what makes the margin bimodal, so it must be matched before almost anything else. Weight 3.5,
just above the end market.

The first cut of this field did not survive the data and was rebuilt. A single INVENTORY value put
Chewy and e.l.f. Beauty in the same bucket and produced a range from 8% to 74% gross margin, which
is no bucket at all. A retailer's cost of goods is the wholesale price it paid; a brand's is what
it cost to make. Split apart, both hold:

| value | names | median gross margin | median EV / revenue |
|---|---|---|---|
| NONE | 30 | 75% | 3.0x |
| OWN_PRODUCT | 7 | 63% | 2.3x |
| CONTENT | 3 | 48% | 4.2x |
| MIXED | 9 | 46% | 2.0x |
| FLEET_OPS | 3 | 40% | 2.6x |
| RESALE_INVENTORY | 10 | 30% | 0.7x |

**`purchase_frequency`**: SUBSCRIPTION, REPEAT_TRANSACTION, EPISODIC. Separates Rightmove from
eBay inside the same end market and Netflix from Carvana inside the same margin band. Weight 2.0.

**A field is only scored when BOTH sides carry a value.** A blank never scores. That is what stops
the two consumer-only fields from giving a uniform lift to the 250 software and fintech rows that
do not have them, and it is why no existing file needed editing.

---

## The buyer convention for two-sided businesses

`buyer` survives into this family unchanged, and it does real work, because it encodes who pays.

> **buyer is the side that bears the monetisation, not the side that clicks.**

eBay and Etsy are SMB, the seller pays. Booking and Expedia are SMB, the hotel pays. Airbnb is
CONSUMER, the guest pays the larger half. DoorDash is SMB, the restaurant commission is the larger
half. REA, Rightmove and SEEK are SMB. CoStar is LOB. Netflix, Match and YETI are CONSUMER.

---

## Token weights were regenerated, and had to be

`data/tag-token-weights.csv` is computed from the tag corpus, and adding 298 distinct consumer
tags changes which words are generic. Forty-five tokens became generic that were not before, and
ten jumped hard: "marketplace" went from 6 carriers to 29, so its token weight fell from 0.83 to
0.17; "online" 16 to 44; "commerce" 10 to 31; "retail" 8 to 26.

Without regenerating, a B2B procurement founder whose site says "supplier marketplace" would start
pulling eBay and Etsy into scoring range on one shared word. The regression fixture
`b2b-procurement` exists to catch exactly that, and it returns Kinaxis and Dassault.

---

## Seven rows are visible and out of every median

The row still shows to the founder. It comes out of the arithmetic. The reason is on each row.

| name | why |
|---|---|
| Baozun | entity name read from a pixelated Chinese string and inferred from the financial fingerprint; confirm before use |
| Opendoor | NTM revenue of 5,955 sits above both FY+0 of 4,229 and FY+1 of 3,933 |
| FuboTV | no FY+0, growth reads #DIV/0!, minority interest of 1,826 against a 309 market cap |
| Just Dial | enterprise value is negative |
| Autohome | enterprise value is 4% of revenue, a net-cash artefact |
| Fiverr | enterprise value is 8% of revenue, same |
| Info Edge | 24.2x revenue because the listed Zomato and PolicyBazaar stakes sit inside the enterprise value and the associates line reads zero |

---

## Known limitations, stated rather than hidden

**Segment contamination on the largest names.** Amazon's reported gross profit includes AWS,
Alibaba's includes cloud and logistics, Sea's includes Garena. They are tagged MIXED and kept in
the medians, because excluding every name with a segment would empty the set. A founder comparing
to Amazon should be told the multiple is not a pure commerce read, and `what_it_does` says so.

**Non-USD reporters have a translation effect in the growth column.** ASOS at -13%, Autohome at
-23% and Hemnet at -14% are FY+1 over FY+0 in USD. Hemnet in particular is a growing business
whose FY+0 and FY+1 in this pull do not reflect that. The NTM figure and all three ratios are
internally consistent, so the rows are usable; the growth column is the one to treat carefully for
those names.

**The education category is where the current weights are most obviously wrong.** The
`consumer-learning-app` fixture returns Duolingo at 4.4x, Coursera at 0.4x and Chegg at 0.4x, and
a median of 0.4x. Those three companies differ on almost nothing in the tag grid except AI stance,
which is weighted 1.0 out of roughly 35. An eleven-fold multiple spread driven by one 1.0-point
field is a weight that does not reflect what is being priced. This should be tuned, deliberately,
against the golden fixtures. It has NOT been changed here.

**Apparel resale has one listed comparable.** The `resale-marketplace` fixture returns a core group
of one, The RealReal, and correctly refuses to pad it. Vinted, ThredUp and Depop-class names would
fix it.

---

## No ticker column was supplied

The screens carry entity name and country and no ticker. Every `exchange_ticker` in
`peers-ecommerce.csv` is assigned by Fairway from the name. The US lines are safe. Confirm these
before the file is used as a join key: WSE:ALE, XTRA:ZAL, AIM:ASC, LSE:AUTO, LSE:RMV, XTRA:G24,
ASX:REA, OM:HEM, ASX:SEK, LSE:MONY, SEHK:3690, NSEI:ETERNAL, NSEI:SWIGGY, NSEI:NAUKRI,
NSEI:JUSTDIAL.

---

## The private consumer set, and what verification did to it

Added 24 August 2026 as `data/private-rounds-consumer.csv`, `data/private-companies-consumer-tags.csv`
and `data/private-round-investors-consumer.csv`. 48 transactions were supplied. 44 are kept, 4 were
deleted, and 40 of the 44 are marked CORRECTED.

**The funnel, because the row count is not the usable number.**

Revised 24 August 2026 after a second verification pass against a corrected sheet.

| stage | rows | companies |
|---|---|---|
| verified transaction records on file | 50 | 34 |
| of those, carrying a defensible REVENUE multiple (`in_medians=1`) | **16** | **13** |
| of those 16, point estimates rather than ceilings | 10 | |
| separately, carrying a defensible GMV multiple (`in_gmv_medians=1`) | 4 | 4 |

Median of the 16 revenue multiples is 7.8x. Median of the 10 point multiples is 6.3x. The four GMV
multiples are 1.9x, 2.1x, 2.5x and 12.4x, and they must never be pooled with the revenue multiples.

The thirty rows with no printed multiple are not junk and are not deleted. Date, round type, PRIMARY
or SECONDARY, capital raised, post-money and lead investor are all verified on them, and that is what
the tagging and the investor file are built from. What they lack is a denominator that survives the
at-pricing rule.

**The GMV lane.** Seven columns were added: `gmv_metric`, `gmv_period`, `gmv_musd`, `gmv_basis`,
`gmv_bound`, `ev_gmv_x`, `in_gmv_medians`. A marketplace that publishes volume and not revenue used to
sit in the file with `denominator_basis = GMV_ONLY` and nothing else, which threw away a real number.
It now carries its volume in its own lane. Two rules govern it. A GMV multiple never enters a revenue
median, because the two differ by a take rate that is usually undisclosed: StockX is the only name in
the set that published both sides, GAAP revenue over $400m on GMV of $1.8bn, an implied take rate of
about 22%, and Contrary Research openly borrows that 22% to estimate GOAT's revenue, which is exactly
the contamination to avoid. And a non-company measure is not GMV: Liquid Death's $263m is SPINS
register data relayed by the company, so it sits in the lane with no multiple printed at all.

**Six rows are marked CORRECTED-AGAIN, meaning the defect was in Fairway's own previous entry rather
than in the supplied sheet.** These matter more than the sheet's errors, because nobody else was going
to catch them.

| row | was | is | why |
|---|---|---|---|
| Vinted, May-21 | 20.4x on EUR 184m | no multiple | EUR 184m is not Vinted's FY2020 revenue and appears in no source; the filed figure is EUR 149.89m. FY2020 first became public on 30-Aug-2021, 111 days AFTER pricing, and on 12-May-2021 the company said it did not disclose its financials in detail. The only at-pricing figure is FY2019 at EUR 83.92m, which would make the round about 45x. Capital was also EUR 250m, not USD 303m. |
| AG1, Jan-22 | 8.8x | no multiple | the ">$150m run-rate" describes the period before the July 2021 round, not January 2022, and TechCrunch reported growth approaching 200% in between |
| SHEIN, May-23 | 2.9x on $23.0bn | no multiple, figure corrected to $22.7bn | a WSJ figure sourced to "people close to the company" and disclaimed by the company; $23.0bn is a rounding, and the row's own cited source says $22.7bn |
| Liquid Death, Mar-24 | 5.3x | moved to the GMV lane, no multiple | $263m is SPINS retail scan data, not company revenue, which has never been disclosed in any period |
| Rokt, Jan-25 | 5.8x | no multiple | Rokt says seven of every eight dollars go back to partners and has never reconciled that to the $600m; Wellington also belonged to the Dec-2021 Series E, not this one |
| Trendyol, Aug-21 | GMV proxy | recorded, no multiple | a USD-quoted lira forecast with no disclosed conversion rate, in the year USD/TRY went from 7.4 to 13.5 |

**Three rows were added and one was refused.** Away (May-19, 9.3x), Glossier (Mar-19, at most 12.0x,
upgraded from estimate to company disclosure) and Rent the Runway (Mar-19, record only) join the set,
along with both Thrasio rounds and the Faire November 2025 tender. Packable was refused: an announced
SPAC that was repriced from $1.55bn to $1.346bn, whose PIPE collapsed from $180m to $70m, that was
terminated on 24 March 2022 and followed by Chapter 11. Nothing cleared, so it is not a transaction.

**Every supplied multiple reconciled arithmetically. Most did not survive the at-pricing rule.** The
corrections run in one direction, because every error divided a fixed valuation by a later and larger
revenue figure:

| row | was | is | why |
|---|---|---|---|
| AG1, Jan-22 | 2.0x | 8.8x | the $600m is a December 2024 figure; the round saw a $150m run-rate |
| Meesho, Sep-21 | 9.8x | 45.8x | $500m matched no fiscal year; FY2021 actual was about $107m |
| Quince, Mar-26 | 5.1x | at most 10.1x | the $2bn was published four and a half months after pricing, and the round was $500m not $200m |
| Vinted, May-21 | 18.4x | 20.4x | the denominator was FY2021, reported thirteen months later; FY2020 was EUR 184m |
| Harry's, Mar-21 | 4.3x | 4.6x | FY2020 sales were $370m, not $400m |
| Huel, Nov-22 | 3.0x | 3.3x | the "$184m" is GBP 184.5m and it is the year to July 2023 |

**Six companies have never published net revenue in any period**: Faire, Back Market, GOAT Group,
Whatnot, Trendyol and Ankorstore. They publish GMV or volume, and the revenue figures in the supplied
sheet were those volumes haircut at an assumed take rate. Loop Returns has never published any
revenue figure at all, which is why the 72.3x, the highest multiple in the batch, had no denominator.

**Three fields were added to the private schema.**

`transaction_type` is PRIMARY, SECONDARY or MIXED. A secondary share sale is a mark, not a priced
round, and it must be labelled exactly as control transactions are in the software set. Both Vuori
rounds were secondary tenders with nothing reaching the balance sheet; both Rokt rounds are pure
secondaries; StockX was 76% secondary; Flipkart July 2023 was Walmart buying out Tiger Global. Ten of
the 44 rows are affected and the supplied sheet had several of them the wrong way round.

`denominator_basis` is DISCLOSED_ACTUAL, DISCLOSED_FORECAST, DISCLOSED_THRESHOLD, FILED_ACCOUNTS,
GMV_ONLY, THIRD_PARTY_ESTIMATE or NONE. This is the field that stops an analyst back-solve being
presented to a founder as a disclosure.

`bound` is `<=` where the denominator is a "more than" floor, so the multiple is a ceiling and must
be printed as "at most", and `>=` where the valuation itself is a floor.

**Seventeen rows across thirteen companies carry a denominator good enough for a median, and their
median is 7.3x.** The other twenty-seven stay visible with their valuation and, where that is all
that exists, their GMV.

---

## What the golden fixtures caught on their first day

Adding thirty-one private consumer companies broke private matching for any profile with no private
neighbours. A consumer language-learning app was returned Huel, AG1 and Harry's, all scoring 9.7 on
nothing but "sells a subscription to a consumer": end customer, revenue model and purchase frequency
coinciding, three low-information tags. A relative quality floor cannot catch that, because 45% of a
bad best score is a worse score.

`FLOOR_ADEQUATE = 12.0` now returns an EMPTY set rather than a bad one. Calibration is the observed
gap between profiles that have private neighbours and one that does not: skincare 40.5, quick
commerce 23.6, car marketplace 13.5, language learning 9.7. The fixture diff showed exactly one
profile changing, which is what the fixtures are for.
