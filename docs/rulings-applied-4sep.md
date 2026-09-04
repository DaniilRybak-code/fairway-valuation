# Rulings applied, 4 September 2026

Daniil's rulings from the evening session, applied the same turn they were given, per the new
rule D14. Each one names what changed, what it cost and what it did not touch.

---

## 1. Negative multiples are not allowed. They are n.m.

**The ruling.** "Negative multiples are not allowed, they should be marked as n.m."

**Where it lives.** `selector/match_reference.py`, one sweep after the universe is built, next to
the stale-row sweep it is modelled on. Any of `mult`, `mult_alt`, `gp_mult`, `pb_mult`, `pe_mult`
or `gmv_mult` that is zero or below is moved to `nm_<field>` and set to None. `multiple_display()`
returns the figure, the string `n.m.`, or None, which are three different statements: a price, a
price that means nothing, and no data at all. Written into the rulebook as **B11**.

**What it caught, count in and count out.** 511 listed rows in, 511 out, nothing dropped. Four
figures on four companies are now n.m.:

| company | field | was |
|---|---|---|
| XP Inc. | mult | -3.8 (fixed separately below, now 2.3) |
| CAB Payments Holdings plc | mult | -2.3 |
| Autohome Inc. | mult and gp_mult | 0.0 |
| Fiverr International Ltd. | gmv_mult | 0.0 |

`tools/check_engine_reach.py` gained CHECK 3, which prints that table on every run. A company that
loses a multiple keeps its name, tags, revenue and growth and can still be shown as context.

**What it cost.** Three fixtures' listed ranges moved because CAB Payments left the priced set:

| fixture | core range was | now |
|---|---|---|
| trolley | 0.9x to 2.3x on 6 names | 1.8x to 6.1x on 5 |
| dots | 0.9x to 2.3x on 6 names | 1.8x to 2.6x on 5 |
| tash (secondary) | 0.7x to 2.3x on 5 names | 0.8x to 2.3x on 5, Digital Garage replacing CAB |

The trolley move is large and it is the honest direction: a -2.3x was sitting in the median band
and pulling the bottom of the range below anything a real buyer would pay.

## 2. XP Inc: the equity-to-AV bridge is zero

**The ruling.** "For XP Inc in particular, we just need to make their Eq value to AV bridge 0
instead of what it is now."

**Where it lives.** `tools/apply_xp_bridge_4sep.py`, run once, with the override recorded in the
header of `data/peers-fintech.csv` itself.

| field | was | now |
|---|---|---|
| equity_to_av_bridge_musd | -25,402 | 0 |
| enterprise_value_musd | -15,902 | 9,500 (the market capitalisation) |
| ev_ntm_revenue_x | -3.8 | 2.3 (9,500 / 4,194) |
| ev_ntm_gp_x | blank | 3.3 (9,500 / 2,858) |

`net_debt_musd` (-24,684) and `associates_musd` (718) are **left exactly as supplied**. They are
what the source said, and this is a pricing ruling rather than a correction of the source. For this
one row the components no longer sum to the bridge, which is why the override is written into the
file's own header as well as here.

## 2b. CAB Payments, the same ruling, applied 20:19 UK

Daniil: "Let's do same for CAB payments." `tools/apply_bridge_zero.py` now holds both rulings in one
table and is idempotent, so XP was skipped and only CAB changed.

| field | was | now |
|---|---|---|
| equity_to_av_bridge_musd | -685 | 0 |
| enterprise_value_musd | -399 | 286 (the market capitalisation) |
| ev_ntm_revenue_x | -2.3 | 1.6 |
| ev_ntm_gp_x | 26.3 | -19.1, which B11 then marks n.m. |
| ev_ntm_gmv_x | -0.00657 | 0.00471 |

Every EV-based multiple in the row is rebuilt, not just the revenue one, because leaving a stale
ev/gp behind would be a figure computed from an enterprise value the file no longer holds. The 26.3x
it used to carry was two negatives dividing into a plausible-looking positive.

**Worth a separate look: CAB's gross profit is negative**, -$15m on $177m of revenue, a margin of
-8.5%. That is why its gross-profit multiple is n.m. after the fix rather than sensible. A negative
margin also sits in the distribution the unit-economics recommendation reads.

## 3. The investor sector column, fixed without touching peer selection

**The ruling.** "Proceed with fixes to the investor sector column, make sure that the matching
mechanism for PEER SELECTION does not break as a result."

**The fault.** A house reaches a founder when the founder's archetype appears in the house's
`screening_categories` as an exact string. Our archetypes come from the tag files; the screening
categories came partly from the enrichment pulls, which wrote the market in their own words. Nine
houses were tagged `Insurance` and no founder is ever tagged `Insurance`: they are tagged
`Insurance Technology`. 24 of the 53 category names in the file could never match anybody.

**The fix.** `SECTOR_ALIASES` in `selector/investors.py`, applied inside `_sectors()` at read time.
The archetype is added **beside** the original name, never instead of it, so nothing that matched
before can stop matching, and `data/investors.csv` is untouched, so the record of what each pull
actually said survives. 22 aliases, each one a judgement about our own taxonomy with the reason in
the comment (Zillow is Classifieds & Listings, so Real Estate Marketplace maps there; HubSpot and
Klaviyo are Marketing & Customer Engagement, so Sales Engagement maps there).

**What it changed.** 48 of the 53 categories now reach a founder, up from 29.

| | before | after |
|---|---|---|
| callable cards across 102 fixtures | 738 | 813 |
| houses a founder gets on average | 7.2 | 8.0 |
| fixtures getting fewer than three houses | 7 | 0 |

The seven founders who were shown nobody (goldfish, acti, welltory, planeat, wondering, befreed,
florin) now get eight houses each, all at tier 1, which is a genuine sector and stage hit and not a
fallback. `florin` gets Mundi, Altai, Insurtech Gateway, Anthemis and five more, all of which were
in the file and invisible.

**Five categories still reach nobody, deliberately:** Healthcare (11 houses), Life Sciences (3),
Climate & Energy (2), and two M&A-precedent tags. They are industries, not business models, and our
archetypes are business models. Forcing them into the taxonomy would be worse than naming them
here. `tools/investor_coverage.py` prints the list.

**Peer selection is untouched, and here is the proof rather than the promise.**
`screening_categories` appears in exactly one module, `selector/investors.py`.
`selector/match_reference.py` does not read it and does not import investors. Across all 102 golden
fixtures, the keys that moved were: `investors_callable` on 59 fixtures, `core_range` on three
(trolley, dots, tash, all from the n.m. rule above), and `secondary` plus `secondary_range` on tash
alone. **No fixture's core lane membership changed. No fixture's private lane changed at all.**

## 4. Three service-shell decisions

- **Price: 750 USD.** The page must say USD explicitly, because the founder has already chosen a
  currency for their ranges and would otherwise read the price in it. The meta description still
  ends "Reviewed by former bulge bracket bankers. Free." and has to change the same day the price
  appears.
- **No entity.** Sole trader, so the disclaimer written for a company is replaced.
- **Address for service: 29 Westbourne Terrace, London W2 3UN.** This is Daniil's home address and
  it will be public on the site. He was told the £50-a-year alternative and chose this.

Disclaimer text, now complete except for the contact email:

> Fairway is a service of Daniil Rybak, trading as Fairway, 29 Westbourne Terrace, London W2 3UN.
> Contact [email].
