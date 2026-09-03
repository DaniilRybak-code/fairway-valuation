# What the call list cannot cover, 3-Sep-2026

The founder-facing list is headed "writing first cheques in your sector right now". A house
reaches it only with a named deal carrying a date and the URL we read it on. This file is what we
still cannot answer, so the next pull is aimed rather than general.

## Where we are

| | |
|---|---|
| houses in the table | 445 |
| carry a CALLABLE layer | 92 |
| can render to a founder | 92 |
| test founders getting fewer than three houses | 2 of 43 |

The 92 is down from 140 and that is the enrichment working, not a loss: 47 houses were moved to
the EVIDENCE layer because a human read each one against the heading and said no. Coatue,
BlackRock, Baillie Gifford, T. Rowe Price and 43 others were on a first-cheque list because an
automated rule promoted anything with a deal inside twelve months.

## The gate, and the ruling that changed it

DANIIL, 3-Sep-2026: "We should definitely include Benchmark and Thrive. Reality is they can do
pretty much anything from what I understand."

The old gate refused any house that had not published a first-cheque range or an investing
geography. That does not describe an inactive fund; it describes a fund with a sparse website.
benchmark.com carries two office addresses and no investment criteria. thrivecap.com is one
sentence. Both led seed rounds this year and both raised new early-stage funds this year, and
both were invisible to every founder.

Sixteen houses were being withheld on that rule: Amplify, Atomico, Acrew, Bain Capital Ventures,
Battery, Benchmark, Bessemer, Founders Fund, Freestyle, Greycroft, HOF Capital, Index, Insight,
Lightspeed, Ribbit, Thrive. All sixteen now render.

**What is shown instead of a blank.** "First cheque not published" and "No stated investing
geography" are facts about the fund. An empty line is read as our omission, which is worse and is
also untrue. **What still holds the line** is the stage band: a house that says where it comes in
is believed and filtered on, so IVP's "typically Series B, floor $15m" keeps it away from a
pre-seed founder whether or not anything else is published. And a house that publishes its terms
outranks one that does not, all else equal, because the founder can check the first for themselves.

## Gap 1: two archetypes have no fund at all

The seed screen has eight coarse sectors. These founder archetypes fall outside all of them, so
the two fixtures tagged the first get an empty list:

- **Consumer & Prosumer Software** (acti, goldfish). A consumer app is not a D2C brand and mapping
  it to "consumer brands and D2C" would be inventing coverage.
- **Online Learning.** There is no edtech sector in the screen at all.

**The pull that closes this:** seed and Series A funds that state a cheque range and publish
recent dated deals in consumer software and consumer subscription apps, and in edtech. Ten to
fifteen of each takes the two remaining empty fixtures to a full list.

## Gap 2: geography was scored on nothing until tonight

The founder is never asked where they are based. It comes from Vercel's edge header at boot
(`app.js` reads `/api/geo`, and `docs/lead-capture.md` records that no IP is ever stored). That is
the right call: one fewer question for a fact the request already carries.

But the matcher compared the header value to the fund's own line with a substring test, so a
founder in "United Kingdom" did not match a fund in "UK", the letters not being adjacent. **The
facet scored nothing for anybody**, and none of the 43 test fixtures carries a country, so nothing
caught it. Geography now resolves through a country table to the names and regions a fund could
write, and `tools/investor_coverage.py` runs two synthetic founders identical but for the country
and fails if they get the same list.

**Still open:** the header can be absent and a VPN can make it wrong. Those founders get cards
labelled "your location was not resolved" rather than a silent "exact fit". Whether that is worth
one confirmation question on the results screen is a product call, not a data one.

## Gap 3: three published cheque figures are years old

Freestyle VC's is a TechCrunch line dated 31 Mar 2022, Square Peg's a blog post dated 21 Nov 2022,
Sequoia's the Jan 2023 Arc announcement. Each is the only figure that house publishes anywhere.
They render with the date on the card: "First cheque $1.5m to $3m (the only figure they publish,
dated 31 Mar 2022)". Better than hiding them and better than presenting them as current.

## Gap 4: Greycroft, and what we refused to use

A $500K to $50m range for Greycroft circulates on aggregator profiles and appears on no
first-party page. It is not in the file. Greycroft renders anyway now, saying no cheque range is
published, which is the honest version of the same card.

## Open decision: `asset_intensity`

"Do you hold your own stock?" was withdrawn from the ecommerce fork. It was the only question in
the quiz with no `why`, and nothing read the answer. Worth wiring rather than deleting:
own-inventory retail and dropship are priced differently and the archetype vocabulary already
separates them. The restore line is in `selector/quiz_fork.py`.
