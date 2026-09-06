# Public pull of 16 names: read and verdicts

**Date corrected 5 September 2026, in the audit of the day's log.** This document and the raw file
it describes were both written on **5 September**, not 4 September: they first exist in commit
`224ec60`, made at 21:28 UK on 5 September, and no earlier commit contains either of them. The file
name keeps `4sep` because the MANIFEST, check 1 and the status document all point at it by that
name; the date is corrected here rather than by renaming four references.

16 rows received as a screenshot of `I_Public_Comps` rows 508 to 523.

**THERE WILL BE NO CSV.** The pull runs in a separate sandbox and cannot be exported, so a
transcription is the only record there will ever be. It is written down:
`data/raw/2026-09-04_public-pull-16-names.csv`, 16 rows, transcribed column by column on
5 September, with a MANIFEST row. This is a standing change to D1 for this pull route: where a
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
**RULED, 5-Sep 21:50 UK: no adjustment. Daniil's figures stand.** "P/E multiples are more aligned to
them, so AV in my spreadsheet is ok." The reasoning holds: the earnings multiple is computed on
market capitalisation and is untouched by the bridge, and Edenred at 12.5x against Pluxee at 10.0x
is two companies priced sensibly against each other. The enterprise-value difference between them is
a real balance-sheet difference, not an artefact: Edenred carries net debt of 2,175, Pluxee net cash
of 1,365.

**Two useful things came out of the investigation and are kept.**

The **currency question on these two rows is answered**. Pluxee reports net cash excluding restricted
cash of EUR 1,270m, and its screen bridge is -1,365, so the screen is USD at **USD/EUR 1.0748**,
derived rather than assumed. Both Euronext rows are USD, like the rest of the file.

And **Edenred's reported net debt already excludes restricted cash**: its note 6.5 nets debt of
EUR 4,826m against cash and other financial assets of EUR 3,585m for net debt of EUR 1,241m, and the
EUR 1,661m of restricted cash is not in that 3,585m. So the bridge was already clean of float assets,
which is why the gross-float adjustment I proposed first was wrong.

**What survives the ruling, for whoever bands these two.** On the screen's own figures Edenred
prices at 2.8x revenue and Pluxee at 0.8x, while their earnings multiples are 12.5x and 10.0x. For
these two the earnings multiple is the comparable measure and the revenue multiple is not. Putting
both into one revenue band gives a 0.8x to 2.8x range out of two companies doing the same thing.
Flagged, not decided.

**Both rows were re-pulled on 5-Sep**: Edenred bridge 2,146 → 2,175, AV 10,173 → 10,203; Pluxee
-1,390 → -1,365, AV 1,156 → 1,181. The raw file carries the new figures and keeps the old.

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

---

## The growth definition, settled 6 September 2026

**This was the last thing blocking the load.** The raw file's header said: "This screen gives CY+1,
CY+2 and CY+3 year-on-year plus a CY+1 to CY+3 CAGR. The engine's existing listed column is a CY+0
to CY+2 CAGR. These are NOT the same measure and must not be loaded into the same column."

**Daniil, 6 September:** "CY+1 to CY+3 growth is a CAGR of CY+1 to CY+3. It is 2026, so in our case
it is 2026 to 2028."

So on the screens he pulls, **CY+1 is the current year**. CY+1 to CY+3 is then the current year plus
two, which is the same window as CY+0 to CY+2 on a screen that calls the current year CY+0. Two
naming conventions, one measure.

**The arithmetic agrees, and it was tested rather than assumed.** This pull carries the year-on-year
series and the CAGR side by side, so the window can be recovered from the numbers:

| what was compounded | reproduces the printed CAGR on |
|---|---|
| the CY+2 and CY+3 yearly rates (two years, starting from the CY+1 level) | **16 of 16 rows** |
| the CY+1, CY+2 and CY+3 yearly rates (three years) | 2 of 16 |
| the CY+1 and CY+2 yearly rates (two years, starting from the CY+0 level) | 2 of 16 |

Tolerance 0.35 of a percentage point, which is what rounding on the printed inputs allows. The
first row is exact on every name including the two that shrink (Skillsoft, LivePerson) and the one
that is flat (Claritev), so it is not an artefact of a narrow spread.

**CORRECTION, 6 September, and it is mine.** The paragraph above is right about THIS SCREEN and
the sentence that followed it was not. I wrote that the two CAGRs are therefore the same window
under two names. That assumed the software and fintech files' CY+0 is the same calendar year as
this screen's CY+1, and nothing supported it. Measured properly against the revenue LEVELS stored
in the same rows: the ecommerce file's CY1-CY3 CAGR reconciles with `revenue_local_cy1` to
`revenue_local_cy3` on 73 of 73 and with cy0 to cy2 on 10 of 74; the software file's CY0-CY2 CAGR
reconciles with `revenue_local_cy0` to `revenue_local_cy2` on 164 of 167 and fintech on 83 of 84;
and cy0 differs from cy1 on every row carrying both. **So in our own files the two columns are
anchored a year apart.** Which calendar year each screen calls CY+0 cannot be settled from inside
the data: only two companies sit in both files and neither carries the levels needed to line them
up. The load is still unblocked, because this pull's CAGR goes into the `cy1_cy3` column either
way; what is not settled is whether the software and fintech CAGRs are a year behind, and the
answer to that is Daniil's single-source reload.

**What this means for the load.** The CAGR goes into `revenue_growth_cagr_cy1_cy3_pct`, the column
the loader already reads and which 72 ecommerce rows already use. Those rows get `g_basis` of
`CAGR_CY1_CY3`, which is already accepted and already ranks a peer. No new column, no code change,
and the label still records which screen the number came from.

**One correction that follows.** The comment in `match_reference.py` describing the two CAGRs as
"anchored a year apart" and "NOT the same measure" was wrong, and it has been corrected with this
measurement written into it. Nothing downstream was broken by it: `g_rank` already accepted both.
