# Public pull, 4 September 2026: read and verdicts

16 rows received as a screenshot of `I_Public_Comps` rows 508 to 523.

**THERE WILL BE NO CSV.** The pull runs in a separate sandbox and cannot be exported, so a
transcription is the only record there will ever be. It is written down:
`data/raw/2026-09-04_public-pull-16-names.csv`, 16 rows, transcribed column by column at 21:45 UK on
4 September, with a MANIFEST row. This is a standing change to D1 for this pull route: where a
screenshot is the only possible delivery, the transcription IS the raw file, and it is written
before anything else happens.

**The transcription is not yet second-read.** Every figure needs checking against the screen before
it loads. The arithmetic has been checked and is internally consistent: AV equals market cap plus
bridge on all sixteen, and every AV/revenue and AV/gross-profit multiple recomputes from the columns
beside it, with two ties at the rounding boundary (Skillsoft 4.04 shown as 4.1, LivePerson 7.21
shown as 7.1, both consistent with the screen computing off unrounded inputs).

## Arithmetic: 16 of 16 internally consistent

Checked by hand: `AV = market cap + bridge` on all sixteen, and every AV/NTM revenue and AV/NTM
gross-profit multiple recomputed from the columns beside it. All agree to rounding. No transcription
fault visible.

## Seven issues, in order of what they cost us

### 1. LivePerson should not be in the file at all
NASDAQ:LPSN. I flagged before the pull that it is under a Nasdaq delisting notice. The numbers say
the same thing: market cap $37m, net income -$40m, revenue growth -17.8% next year and -35.9%
thereafter. A company shrinking a third a year under a delisting notice cannot price a founder.
**Verdict: exclude on load.**

### 2. Green Dot arrives unusable on both paths
NYSE:GDOT. Gross profit is 0 against revenue of $2,491m, which is missing rather than zero, so the
gross-profit multiple cannot be built. BVPS and P/BV are n.a., so the book path cannot be built
either. And it is a bank holding company, so AV/revenue of 0.3x is not a price, it is an artefact of
comparing a market cap to gross interest and fee income.
**Verdict: hold out of the load until BVPS and P/BV arrive. It belongs in `peers-lending.csv`, not a
revenue peers file.**

### 3. Pluxee and Edenred: the same business, priced 3.5x apart by the bridge
ENXTPA:PLX at 0.8x AV/revenue against ENXTPA:EDEN at 2.8x. The cause is the bridge: Edenred carries
+$2,146m of net debt, Pluxee -$1,390m of net cash. Both hold large customer float, and float is
client money, not shareholder cash. Pluxee's enterprise value is understated by roughly the float.
This is exactly the XP Inc and CAB Payments pattern ruled on earlier today.
**Daniil's ruling, 4-Sep: the bridge INCREASES by the customer funds**, because client money held
in cash is not shareholder cash and net debt should be higher. A different correction from the XP
and CAB ruling and the right one here: those had a bridge so corrupted it went negative and the
answer was to price on equity value; these have a bridge that is directionally sound and too small.

    AV = market cap + bridge + customer funds

**Figures read from the companies' own reporting, 4-Sep 21:55 UK, not estimated.**

| | Edenred (31-Dec-2025) | Pluxee (31-Aug-2025) |
|---|---|---|
| customer float, company's own label | "Vouchers in circulation (Float)" EUR 6,125m | "Float-related cash" EUR 2,736m |
| restricted cash | EUR 1,661m | EUR 854m (float-related) |
| reported net position | net debt EUR 1,241m | net cash EUR 1,163m |
| reported revenue | FY2025 EUR 2,961m | FY2025 EUR 1,287m |

Sources: [Edenred FY2025 press release](https://www.edenred.com/system/files/documents/2026-02-24-edenred-fy-2025-pr.pdf),
[Pluxee Fiscal 2025 press release](https://www.pluxeegroup.com/sites/g/files/jclxxe221/files/2025-10/Pluxee%20FY26_Press%20Release%20EN.pdf).

**The adjustment, at an assumed USD/EUR of 1.12:**

| | AV as pulled | AV/revenue | AV + full float | AV/revenue | AV + float less restricted | AV/revenue |
|---|---|---|---|---|---|---|
| Edenred | 10,173 | 2.8x | 17,033 | **4.7x** | 15,173 | **4.2x** |
| Pluxee | 1,156 | 0.8x | 4,220 | **2.8x** | 3,264 | **2.2x** |

The 3.5x gap between two direct competitors becomes 1.7x on the full-float reading and 1.9x on the
other, which is roughly the discount Pluxee has actually traded at since the spin. Both readings are
carried in the raw file rather than one being chosen, because two things are still open:

1. **The FX rate.** 1.12 is my assumption. The screen is in USD and the float is in EUR, and the
   rate the screen used is not on the screen. One number from you replaces it.
2. **Whether the screen's cash already excludes restricted cash.** If it does, adding the full float
   double counts the restricted portion, and the right column is the second one. That is a question
   about how the pull treats restricted cash, not about the companies.

**Paysign is left unadjusted.** It holds cardholder funds on the same principle, but does not
disclose a float at the level these two do, and its bridge is only -22, so the correction is small
and unsourceable. Flagged rather than guessed.

### 4. Claritev and Skillsoft are leverage, not price
NYSE:CTEV: market cap $667m, enterprise value $5,353m, so **88% of the enterprise value is debt**.
NYSE:SKIL: market cap $59m, enterprise value $525m, **89% debt**. Their AV/revenue multiples of 5.1x
and 1.5x describe balance sheets, not businesses. A founder shown 5.1x from Claritev is being
compared to a company whose equity is a twelfth of its enterprise value.
**Verdict: load them, and carry a flag. They may sit in a comp list as context; they should not set
the top or the bottom of a band. If we have no such flag today, that is the gap.**

### 5. Alignment Healthcare and Evolent Health do not have "revenue" in our sense
NASDAQ:ALHC at 0.5x and NYSE:EVH at 0.4x. Both carry premium or medical cost through the top line,
so revenue is an order of magnitude away from anything a software founder means by revenue. Their
gross-profit multiples (3.7x and 3.1x) are the comparable figures, and Alignment also carries
BVPS $2 and P/BV 7.3x, so it can price on book.
**Verdict: tag both so the gross-profit denominator is forced, exactly as `match_reference.denominator`
already does when margins diverge. Alignment is a licensed insurer and should carry the
balance-sheet fork.**

### 6. Two names have almost no analyst coverage
Skillsoft: 1 estimate. Crawford & Company: 2. Everything else runs 3 to 25.
**Verdict: load, but a one-broker forward number is a single opinion. If we ever add a coverage
floor, this is the evidence for it.**

### 7. A ticker changed under us
I asked for MultiPlan, NYSE:MPLN. The pull came back as **Claritev Corporation, NYSE:CTEV**. Same
company, renamed. Nothing is wrong with the row, and it is a reminder that a name in a request is
not a key: the request should carry the ticker and the ticker should be checked on arrival.

## What is clean and useful

Verisk (8.7x revenue, 12.4x gross profit, 18 estimates), ExlService (2.3x / 5.9x, 10), monday.com
(2.0x / 2.3x, 25), Progyny (1.2x / 4.6x, 11), CPI Card Group (1.0x / 3.0x, 4), Paysign (5.3x / 8.5x,
5), D2L (1.2x / 1.7x, 7), Crawford (0.6x / 2.1x). Eight rows that can price a founder as they stand.

## Next step

Send the CSV. On arrival: `check_raw_coverage`, then the tag rows (I write those), then
`FAIRWAY_NO_GIT=1 sh tools/check_all.sh`, then a golden diff read before anything is committed.
