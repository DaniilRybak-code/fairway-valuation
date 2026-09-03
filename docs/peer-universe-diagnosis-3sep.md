# Why Payabli had no listed comparables, and what that turned out to be

3 September 2026. Written after Daniil asked how a payments company could come back with no peers.

## The short answer

Payabli was never short of peers. It had seven listed payments names and seven private ones, and a
priced private range of 16.3x to 48.0x. What it had was an empty CORE lane, and my scoreboard
printed a column headed "core" with a zero in it, which reads as "we found nothing". That was my
reporting, not the engine.

The empty core was real though, and it was worth chasing. Four fixes came out of it and the
peer-universe score went from 33 of 43 to 36 of 43.

## Why the core was empty

Payabli is tagged Horizontal and sells to developers. The rule for a horizontal founder demanded a
listed peer that is BOTH horizontal AND developer-facing, because for a horizontal company the end
customer is the only thing that narrows the field. No listed acquirer is both. Marqeta sells to
developers but is tagged Financial Services; Adyen and dLocal are horizontal but sell to enterprises.

The second route through that rule is shared product vocabulary, and it could not fire either,
because our founder tags and our listed tags were written in different words for the same thing:

| Payabli says | Marqeta says | scored |
|---|---|---|
| Embedded Payments | Embedded Finance | |
| Payment Infrastructure API | Card API | |
| Unified Payments API | Issuer Processing | 0.7 out of a required 3.0 |

So an empty core out of 84 eligible names, 25 of them merchant acquirers.

**Fix 1.** A third route: sharing the exact PRIMARY archetype. That is narrower evidence than either
existing route, not looser. Axis A already accepts an overlap on either archetype slot; this asks the
primary slots to be identical. Payabli and Marqeta are both Merchant Acquiring & PSP. Trolley and
Western Union are both Cross-Border & FX.

Effect: 23 listed names gained, 2 displaced, across 16 fixtures. Payabli, moov and rainforest each go
from an empty core to five acquirers. Trolley goes from Repay and Usio to Western Union, CAB
Payments, Payoneer and Corpay, which is what a global payouts business should be shown.

## Then the same class of bug three more times

Chasing Payabli turned up three more places where the engine held the answer and picked something
else. All three are the same mistake: **the code asked "is there a number in the cell" when the
question is "can this name price THIS founder".**

**Fix 2, which round of a company to use.** Atom Bank is in the file twice: Nov-23 with a revenue
multiple and Feb-22 with the BOOK multiple of 3.17x that we loaded on 2 September precisely because
the lender fork had been pricing off one comparable. Both rounds score identically, so the tie went
to the later date and the book round lost. Perenna, a mortgage lender, was still being shown a book
range of one name. Now the tie drops rounds that cannot price this founder before anything else is
considered. Perenna's book range: 3.17x to 5.6x, two names.

**Fix 3, the listed top-up was measuring the wrong field.** There is a rule that a core which cannot
price three names is not a core, and it tops up from the wider ring. It asked every candidate for
`mult`, enterprise value to revenue. A lender has no revenue multiple, so for every lender fixture
the answer was "none of these price", the top-up ran to its ceiling, and it still measured nothing.
Perenna's core was SoFi, LendingClub, Nu Holdings and Inter & Co, four names with no price-to-book in
the file, while 39 listed lenders that carry one sat unshown in the same family. **A lane that is
full and empty at the same time is worse than an empty one, because it looks answered.**

**Fix 4, and the top-up has to reach for names that price.** Having fixed what "price" means, it
still walked the wider ring in score order and appended whatever came next. Tienda-Pago filled to
seven with six unpriced names while 33 priced lenders sat in the same pool, three of them scoring
above the two that were taken. Score still orders the names that price; it no longer decides whether
the top-up is any use.

**Fix 5, the private lane, same rule.** A private lane that cannot price two names now reaches for
one that can, and "can price" means on the founder's own basis, through `basis_mult`, not the raw
cell. Sellerclaw held four multiples and priced off one, because Packable, WayCool and ElasticRun are
gross-revenue rows and the founder is asked for net. Counting the raw cell made the lane look
answered, so the top-up never fired.

## Score

| | before | after |
|---|---|---|
| fixtures whose peer universe is defensible | 33 of 43 | **36 of 43** |
| fixtures with no priced range at all | 4 | **2** (nursa, mondu) |
| golden movement | | rebaselined, 0 of 43 after |

Human-verified peer surfacing did not move (14 of the 29 we hold). That measure asks a different
question: which specific companies a human named. It is unaffected by any of this.

## The scoreboard had two faults of its own

**It rewarded an empty answer over a thin one.** It failed a lane holding one priced name and said
nothing about a lane holding none, so numida passed with a book range built on no comparable and then
"failed" the moment a real one arrived and made it one. A check that scores zero above one is worse
than no check. Fixed: fewer than two priced names fails, and zero is reported separately.

**It re-raised a settled ruling as an open question.** It flagged moov, payabli and rainforest as
"passing with an empty lane, Daniil has not ruled on this". He had, on 31 August: show the wider names
as context with a disclaimer rather than showing nothing. The warning is gone, and so is the condition
that produced it.

## Where the remaining seven actually stand

`tools/thin_lane_diagnosis.py` answers Daniil's question directly: is the next best peer in our
database or not. It separates three causes that look identical on a report.

Six thin lanes remain. **All six are genuine sourcing requests.** In every one, the only related
names left that price on the founder's basis are BROAD tier, which the no-unrelated-comparable rule
bars, or they sit under the lane's own score cut.

| fixture | lane | what is missing |
|---|---|---|
| acti, goldfish | listed core | Consumer & Prosumer Software holds six listed names and only Truecaller reaches these two. An AI keyboard and a local-first memory layer have no priced listed comparable that is not BROAD. |
| finn | private | Car subscription on an owned fleet. The names that price are Savage X Fenty, Huel, Harry's, all BROAD. Putting Huel next to a car subscription business would fill the lane and break the rule the lane exists to keep. |
| honen | listed secondary | Its CORE is fine: Duolingo, Docebo, Nerdy, Coursera, Chegg. Only the wider context ring is thin, and the one name in it, JustSystems, carries no multiple. This may not deserve to fail at all. |
| levelten | private | Xpansiv is held, matched, and carries no multiple. One valuation and one denominator fixes this fixture. |
| priori-legal | private | Legal talent marketplace. Clio prices; Harvey is out of the medians; the rest are BROAD retail marketplaces. |

Nothing here asks for a new sector. The cheapest four are named figures for companies we already
hold: **Xpansiv's valuation and denominator, JustSystems' multiple**, and the net-revenue reading for
the gross-only Indian rows.
