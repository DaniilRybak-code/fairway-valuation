# Is "we searched the rest and found nothing" actually right?

Daniil asked, 1 September: the other model searched the remaining tickers in the public pull and
reported no volume metric, and he wanted that checked rather than accepted.

## What the new sheet covers

101 rows, 98 distinct tickers. 96 of them match a name in our listed universe. Two do not:
**TSE:8253 Credit Saison** and **ASX:EML EML Payments**. EML is the name we dropped from the
universe on 31 August for thin broker coverage, so it arriving in a new pull is worth a decision
rather than a silent re-entry.

Two companies appear twice under different exchange prefixes, same figure both times:
**GigaCloud** (NASDAQGM:GCT and NASDAQ:GCT) and **Freightos** (NASDAQCM:CRGO and NASDAQ:CRGO).
Harmless, but they must be deduplicated on the way in or they double-count.

## How I judged the absences

120 names in our universe sit in an archetype where a volume figure might be expected and are
absent from the new sheet. Most of those absences are correct **by rule, not by research**:
**lending and deposit-taking businesses price on book value** under our own rule, so a volume
metric is irrelevant to them, and the same goes for the freight forwarders and warehouse REITs
already marked EXCLUDED. Stripping those out leaves **34 names** where a volume figure is the norm
for the business and an absence is a claim that needs testing.

Of those 34: 13 are already EXCLUDED with a reason, 20 are marked NOT_DISCLOSED, and one is marked
DISCLOSED, which is a straight contradiction.

## The six that look wrong, and what I found

**1. Worldline (ENXTPA:WLN). A contradiction with our own file.** We record it as DISCLOSED with
the metric named "Acquiring Merchant Sales Value" and no value attached, and the new sheet does not
carry it at all. One of the two is wrong. Worldline is a top-five European acquirer sitting beside
Adyen, Nexi and Fiserv, all of which are in the sheet.

**2. Eternal Limited, formerly Zomato (NSEI:ETERNAL). A real miss, and instructive.** It is marked
NOT_DISCLOSED. It discloses volume every quarter. **The metric was renamed**: Eternal moved from
Gross Order Value to NET Order Value from Q4 FY25, reporting "NOV of our B2C businesses grew 53% YoY
to INR 17,440 crore in Q4FY25". A search for "gross order value" finds nothing recent, which is
exactly the shape of a false negative.

Two consequences. The obvious one is that we are missing the largest Indian food-delivery
comparable. The less obvious one matters more: **Swiggy is in the sheet on B2C GROSS Order Value
and Eternal reports NET.** They are direct competitors and their volume figures are on different
bases. Under rule B3 they must never sit in the same range, and nothing in the data would have
told us.

**3. Global Payments (NYSE:GPN). The absence is CORRECT, and I checked it rather than assumed.**
Its FY2025 results release carries no dated volume figure, only the marketing line "manages
trillions in payments volume", which under our own rule (a figure with no stated period is excluded
outright) is not a number. NOT_DISCLOSED stands.

**4, 5, 6. Still open, same shape as Eternal.** Trip.com (NASDAQGS:TCOM) sits beside Booking,
Expedia, Airbnb and MakeMyTrip, all of which are in. Full Truck Alliance (NYSE:YMM) is a freight
marketplace that has historically reported gross transaction value. Meituan (SEHK:3690) is the
largest local-delivery platform in the set. Each should be re-checked **by the metric the company
actually uses**, not by the metric we expect.

## The rule this suggests

A "not found" is only evidence when the search knew what to look for. Companies rename these
metrics: GOV becomes NOV, GMV becomes GTV, TPV becomes processed volume. **Before a name is marked
NOT_DISCLOSED it should be searched on at least two metric names, and the note should say which
were tried.** Otherwise the file records an absence of evidence as evidence of absence, which is
what happened to Eternal.
