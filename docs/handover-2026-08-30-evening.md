# Handover to Fable, 30 August 2026, evening

## Where this sits against the pilot

The pilot is the week of 21 September. That is three weeks and a few days from tonight.

Data was the thing standing in the way, and after today it mostly is not. The engine now reads
513 listed companies and 149 private rounds with nothing untagged. What is standing in the way
now is testing and honesty copy, and one of those has a hard number attached: we agreed we
cannot launch on 21 golden fixtures. We have 43. The target is at least 100, each checked by two
independent agents. That is the single biggest schedule risk and it has not moved today.

Second risk, unchanged: the six honesty flags the engine attaches to every range still do not
reach a founder. The engine can still print a confident number built on a loose relationship and
say nothing about it.

## Read this part first: I lost data, and it was my fault

Daniil sent five separate data pulls over the past week as screenshots. I read them, reasoned
about them, quoted numbers back, and never wrote them to a file. The sessions then compacted and
the images were gone. Whole sectors went missing from the product and it looked like a git
problem, which it never was. Daniil pushed every time I asked. There was simply nothing there to
push.

This is not a tooling gap. It was me treating a screenshot as a place data can live.

The rule now, and please write it down somewhere it will be enforced rather than remembered:

1. Any figure that arrives as an image is written to a file in `data/raw/` in the SAME session,
   before anything is built on it. Not after the analysis. Before.
2. Every raw file is listed in `data/MANIFEST.md` with its row count and whether the engine
   reads it.
3. `python3 tools/data_inventory.py` is run at the end of every data session. It prints row
   counts, archetype coverage, and any file the loader does not read. That last list is DERIVED
   from the loader, never hardcoded, because a hand-kept list of wired files goes stale and then
   the check people trust starts lying. It did exactly that this morning.
4. Nothing counts as done until the inventory shows it.

Please treat any future session where I quote a number I have not first written down as a
defect, and say so.

## What landed today

Five pulls transcribed and merged: specialty finance on price to book (79 names), logistics,
services, consumer and payments (123), a private transaction master file (58 rounds), a software
refresh (167) and a fintech refresh (85), plus an ecommerce pull with GMV (74).

Two new files wired into the matcher, `peers-lending.csv` and `peers-logistics-services.csv`,
and 202 new listed names tagged so the matcher can see them.

The ticker join was normalised. Capital IQ writes the same company as `NASDAQ:OPRT` on one pull
and `NASDAQGS:OPRT` on another, and an exact-string join was silently dropping the row. That is
how 29 lenders vanished this morning before it was caught.

Company-disclosed recurring revenue is now on 80 listed names and retention on 83, all from the
company's own words. Twelve retention values were found corrupted, where a recurring-revenue
percentage had been written into the retention column. Shopify was sitting at 22% net revenue
retention. All twelve were cleared, eight re-sourced, four confirmed as not disclosed.

Tonight, two more pulls: a volume-metrics research sheet and the same logistics pull re-sent with
the ticker and GMV columns visible.

## Tonight's two pulls, and what they do and do not do

`data/volume-metrics.csv` is now the single overlay of volume the ISSUER itself publishes,
240 names: 51 with a figure, 112 that report revenue and unit counts but no monetary gross
figure, and 77 whose business model has none to publish. That last group is a conclusion, not a
gap, and those names should never come back onto the sourcing list. The overlay is read by the
loader; `gmv-disclosures.csv` is superseded and marked as such in code and in its own header.

Two things in it matter more than the numbers.

**GMV and payments volume are not the same thing and must never be pooled.** WEX turns over
$197bn to earn $2.9bn. GigaCloud turns over $2.0bn to earn $1.7bn. Both are gross transaction
values and averaging them would be meaningless. `metric_category` separates core marketplace GMV
from adjacent gross volume and nothing may cross that line.

**For a payments name the multiple has to be a percentage, not a turn.** Capital IQ's own
AV/NTM GMV column rounds to 0.0x for every payments business we hold, and is simply blank for
two of them. The same figure as a percentage of volume is the take rate the market is paying
for, so the loader now carries `volume_pct` alongside the turn and the payments lane must
display the percentage.

**What tonight's sheet did NOT do.** It covered the logistics, services, consumer and payments
universe, which sits next to our outstanding list rather than on it. Not one of the 154 names on
`docs/sourcing-volume-metrics.md` was answered by it. 95 are still open, 70 of those TPV for the
large payments names: Adyen, Block, Fiserv, Global Payments, Visa, Mastercard, PayPal, Shopify,
Toast, Shift4, Wise, StoneCo, dLocal, Marqeta, Payoneer, Remitly, Corpay, Euronet, Nexi,
Paysafe. That is still the largest hole we have and it is the one a payments founder walks into.

## Please check the numbers, not just the code

Do not go through every figure, we will run out of usage. Go at the riskiest pieces. In order:

**1. The payments volume denominators are not like for like, and this is the most dangerous
thing I built today.** The percentages come out as Cass 0.84%, Usio 0.76%, Priority 1.70%,
WEX 3.09%, Phreesia 14.28%, Nayax 18.89%. They look comparable and they are not. Cass's figure
is transportation dollar volume only and the issuer publishes no consolidated total, so its
separate $23.3bn facility-expense volume is excluded. WEX's figure includes purchases issued by
other people using a WEX platform. Priority's is the Merchant Solutions segment, not the group.
Read the `exact_wording` and `scope` columns on those three rows and tell me whether any of them
should be dropped rather than shown. My instinct is that Cass should be marked segment-only and
kept out of any median.

**2. The twelve GMV figures that tie exactly.** Every broker GMV in the Capital IQ pull matches
the company's own disclosure to within 0.01%. That is a good result and it is also exactly the
sort of thing that is too clean. Pull two of them, RB Global and Auction Technology, back to the
filings and confirm the fiscal periods line up with the pull date of 21 August.

**3. Nayax was filed under the wrong exchange.** We had `TASE:NYAX`; it is `NASDAQ:NYAX`. This
is the second time this class of error has appeared, after NICE. Three others were wrong too:
ZipRecruiter and Expeditors were filed on Nasdaq and are both NYSE, and Radiant was
`NYSEAMERICAN` against Capital IQ's `NYSEAM`. Ninety-four of ninety-eight hand-recovered tickers
were right, which is not good enough when a wrong one creates a duplicate company. Please check
whether any other file has a company under two exchanges.

**4. Meesho.** Daniil asked me to check it because one of its two multiples had to be wrong.
Neither is. The 2021 round priced at 45.8x on $107m of FY2021 net revenue and the 2024 round at
4.2x on $922m of FY2024 net revenue, and both denominators are filed accounts describing a year
that had already ended at the pricing date. Revenue grew 8.6 times while the valuation fell 20%.
The real defect is next door: seven companies carry more than one priced round, the selector
keeps one row per company, and because two rounds of one company always tie on business-nature
score, the DATE decides on its own. Eight priced rows, 13% of our priced private evidence, are
unreachable by any founder, including the two highest multiples we hold, Meesho at 45.8x and
Klarna at 37.6x. Written up in `docs/multi-round-companies-30aug.md`. Awaiting Daniil's call on
the replacement rule before I change anything.

**5. Three definitions of growth are live at once** and nothing reconciles them. 249 rows carry a
CY+0 to CY+2 CAGR, 72 carry a CY+1 to CY+3 CAGR, 192 still carry a single forward year. Every row
records which one it is in `g_basis`, so nothing is silently blended, but the founder is asked
for growth over the last twelve months and is being compared against a two-year forward rate.
That gap is open and it affects the regression method directly.

**6. `nursa` returns no range while holding three priced comparables** (Vinted 7.3x, Meesho 4.2x,
Flipkart 5.2x). That is a plain bug, not a data gap, and it is unfixed.

**7. Twelve disclosed figures cannot be converted to dollars** because the issuer reports in a
currency we have no dated rate for: Airtasker and Freelancer and Humm in Australian dollars,
Credit Saison and U-NEXT and Digital Garage and BASE in yen, Worldline in euro, PayPoint in
sterling, AvenuesAI in rupees, Avarda in krona, Fawry in Egyptian pounds. The local figures are
recorded and the dollar column is deliberately empty. I did not invent a rate. Daniil needs to
say which rate table we use.

## What moved in the fixtures

Nothing priced. Across all 43 golden profiles the only change was Nayax's ticker on one
secondary peer list, which is the correction itself showing up. Rebaselined.

## Still open, roughly in the order they matter

1. Fixtures from 43 to 100, checked by two independent agents. Schedule risk.
2. The six honesty flags still do not reach a founder.
3. The `nursa` bug.
4. The next-best-neighbour step. Daniil's position, and it is the right one: a founder in a young
   category is using us precisely because no clear precedent exists, so a blank is a trigger to
   apply judgement and find the nearest neighbour on business model, end market, revenue
   generation, growth profile and maturity. Never one comp. A handful, each with its own reason
   for making the list for that specific valuation.
5. `private-rounds-master-30aug.csv` is still unread by the engine. It needs source URLs, and six
   rows conflict with this morning's insert: Zepz at 14.8x against 21.0x, and Marqeta at a
   14.3x gross ceiling against 30.0x net.
6. The 70 payments TPV names.
7. The tokeniser leaks stopwords: "to" is surviving out of "direct to consumer".
8. Profitability and EBITDA are still asked for in the live quiz and used nowhere.
