# 3 September 2026, evening: rulings applied, two silent loader drops found, lender fork rebuilt

Daniil pushed back on three things and every one of them was right.

## 1. "Marqeta is not an acquirer. Marqeta is an issuing business."

Correct, and the fault was our vocabulary, not the matcher. Our archetype list had no entry for
issuing at all, so the only pure card-issuing business in the listed file sat in the merchant
acquiring bucket and was reachable as a core comparable for every payfac, gateway and PSP.

An issuer earns interchange on cards it puts into the market. An acquirer earns a merchant discount
on cards it accepts. Same industry, opposite side of the transaction, different economics.

New archetype `Card Issuing & BaaS`, applied to Marqeta in both the listed and the private tag
files, with Merchant Acquiring & PSP kept in the secondary slot so it still appears as context for
a payments founder and can no longer price one. I audited all 25 names in the acquiring bucket:
Marqeta was the only one misplaced. Fiserv, Global Payments, Nexi and Worldline do issuer
processing as one line of a broader acquiring business, which is a different thing.

Payabli's listed core is now Repay, Tyro, Usio, PayPoint, Fawry, dLocal and Nexi, and its private
lane leads with Stripe. Marqeta sits in secondary.

## 2. "It is ok if we cannot find an EXACT match"

Also a real bug. The rule from 31 August is three to five names on an almost perfect match, five to
seven where the match is weaker. That has been enforced on the private lane since. The listed core
was hard-capped at five whatever the quality, so on a WEAK match it stopped at five and left the
obvious names out. Payabli stopped at Fawry, an Egyptian bill-payment network, while dLocal, Nexi
and GMO Payment Gateway waited in sixth to eighth place.

A weaker match is exactly when a founder needs more names, not fewer. **51 listed names gained
across the fixtures, 6 displaced.** Trolley's core went from Corpay, Repay and Usio to Western
Union, Corpay, CAB Payments, Al Ansari, Payoneer, Flywire and Remitly.

## 3. "NU for sure carried price to book value"

It does, and we had transcribed it correctly. **The loader threw it away.**

Twelve companies sit in both `peers-fintech.csv` and `peers-lending.csv`, because a neobank is both
a fintech and a lender. The loader skipped any ticker it had already seen, so for all twelve the
lending row was dropped in silence, and the fintech file has no price-to-book or price-earnings
column at all.

| lost | recovered |
|---|---|
| Nu Holdings | P/BV 3.9x, P/E 14.7x |
| Klarna | P/BV 1.9x, P/E 35.9x |
| SoFi | P/BV 2.0x |
| Inter & Co | P/BV 1.0x, P/E 6.2x |
| American Express | P/BV 6.0x, P/E 18.5x |
| Block, Chime, Enova, Upstart | P/BV 1.9x, 6.2x, 2.8x, 2.8x |
| Affirm, Zip, LendingClub, Pathward, Cass | P/E 19.4x, 18.1x, 9.4x, 9.2x, 16.6x |

Those are the exact names that came back unpriced in every lender fixture yesterday. Listed
price-to-book coverage 47 to 57 rows, price-earnings 64 to 76.

A second file may now FILL a field the first one left empty. It may never overwrite one, only
touches a whitelist of measures, never a tag or a family, and records `filled_from` on the row.

### And a second drop of the same kind

The two private files spell the same column differently: the consumer file writes `ev_gmv_x`, the
fintech file writes `ev_volume_x` with a `volume_metric` naming what the volume is. Only the first
was read, so **16 volume multiples reached nothing, including every EV/originations multiple we
hold.** Both spellings are read now, the metric is carried and normalised so originations, payment
volume and GMV can never be averaged together, and a since-inception period is barred from pricing.

Private volume multiples 6 to 22 rows. Four are periodic originations: Wayflyer 3.20x, Clearco
2.00x, Tala 0.80x, Upgrade 0.75x.

## The lender fork now shows every reading it can support

> "public peers are priced off book value or net income. Private peers very often (but not always)
> are priced off ARR. So when we ask the question to the user, we need to ask all of these."

Done, and each one is backed by multiples we actually hold, which is the rule the fork is built on.

| lane | basis | evidence we hold |
|---|---|---|
| listed | price to book | 57 rows |
| listed | price to earnings | 76 rows |
| private | EV / book | 2 rounds: Zopa 5.6x, Atom Bank 3.17x |
| private | EV / ARR | **12 rounds**, from Starling 7.6x to Qonto 41.7x |
| private | EV / originations | 4 periodic rounds, 0.75x to 3.20x |

ARR is the largest private lender basis we have and the fork was not asking for it. Book value stays
the only required question; ARR, net income and originations are asked and optional, so a founder is
never blocked and each answer adds a whole range rather than refining an existing one.

Perenna now gets four readings instead of one. Mondu, which had no priced range at all, now has
three.

## The rulings, applied

| ruling | effect |
|---|---|
| Klarna, spot rate at pricing date | Mar-21 28.52x to 26.11x, Jun-21 37.6x to 37.72x, Jul-22 5.1x to 5.16x. Rate, date and entity (Klarna Bank AB) recorded on each row. |
| Klarna volume metric | **Yes, one was disclosed.** GMV of $53bn for 2020, public 24-Feb-2021, so current when both 2021 rounds were priced. Loaded as EV/GMV 0.585x and 0.860x. FY2021 not loaded: the only figure I could verify is "42% year on year". |
| LEAD School, printed number | 135.30x to 142.17x on Rs 57.1 crore operating revenue. |
| Indian rows, revenue from operations | Dream Sports 22.06x to 23.40x. WayCool basis label fixed, 5.88x to 5.91x. Ninjacart was already right and is the control. |
| pre-money column | Added, three values, derived only where the row's own text settles it: 54 POST, 1 PRE, 182 UNSPECIFIED. A PRE row can no longer join a post-money range, and every range records how many of its names are stated post-money rather than assumed. |
| Vegrow, keep with a note | Loaded at 6.68x. The note is on the row: tier-4 source, no year attached to the figure at source, used because tiers 1 to 3 are empty for FY2023. |
| Kriya | Checked. 12.6 is turnover from the filed accounts, not a volume. The odd number is the numerator: GBP7.5m is Allica Bank's accounting purchase consideration on acquiring Kriya, not a valuation. Typed CONTROL_ACQUISITION, out of medians. |
| Fireblocks | No fix needed. Our two rounds carry their own dated ARR, $50m at Jul-21 and $100m at Jan-22. The stale denominator was in the supplied sector screen and that row was never loaded. |
| the fourteen funds | All fourteen now have dated deals, thirteen with two. Every one confirmed on a page naming the fund and the round. |

## State

```
listed 511 | private rounds 290 | median-eligible 180
raw coverage        PASS
engine reach        PASS   290 rows, 290 loaded, no double vote
golden              0 of 43 after rebaseline
peer universe       36 of 43
funds with no dated deal   0, was 14
```
