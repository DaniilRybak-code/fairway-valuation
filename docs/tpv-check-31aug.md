# The TPV batch, checked

31 August 2026. Your method was: take TPV for the last reported year, convert at the average FX for
that period, then grow it at the same rate as revenue in local currency. Three checks, one per step.

## Step 1: does CY+0 tie to what the company actually published? YES, all 28

Every CY+0 figure in the Capital IQ block matches the issuer's own disclosure to the dollar. Not
approximately: exactly, on all 28, including the awkward conversions. Adyen at EUR1,394.3bn,
GMO Payment Gateway at JPY21.8tn, Paytm at INR23.8 lakh crore, StoneCo at R$560.9bn. That is the
cleanest tie we have had on any batch.

## Step 2: is the growth applied as stated? YES on 23 of 25, and the two misses matter

The TPV forward series grows at exactly the local-currency revenue rate on 23 rows. Two do not:

**Fiserv.** TPV FALLS 7.6 per cent while local-currency revenue RISES 28.1 per cent. This is the
only row where the two genuinely disagree. The CY+0 is the Investor Day $4.6tn figure and the
forward series looks grown off a different base.

**CAB Payments.** 657.5 per cent against 681.2 per cent. Both are nonsense for the reason below.

## Step 3: is the RATE ITSELF sensible? NO on four rows, and this is the real finding

The method is applied faithfully, which means it faithfully inherits a broken input. Four rows have
a units or scope break in the CY+0 local-currency revenue, and the TPV inherited it exactly:

| Company | TPV growth CY+0 to CY+1 | Why |
|---|---|---|
| StoneCo | +343% | Local-currency revenue runs 3,382 then 14,987. That is a CURRENCY break: CY+0 looks like USD and CY+1 onward like BRL. |
| PagSeguro | +160% | Local-currency revenue runs 8,159 then 21,185. PagSeguro earned around R$19bn in FY2024, so CY+0 is not the same measure. |
| Nexi | -42% | Local-currency revenue falls from EUR6,273m to EUR3,646m. A definition break, not a forecast. |
| CAB Payments | +658% | Local-currency revenue runs 16 then 125 on a company earning around GBP130m, so CY+0 is mis-scaled. |

For all four the CY+0 volume is right and only the forward series is wrong, so the forward figures
are cleared and the reported year is kept. Fiserv is cleared for the same reason. **Please re-pull
the local-currency revenue series for those five**; the volume itself needs no rework.

## The take-rate test, which caught three more

Revenue over volume should sit roughly between 0.1 and 3 per cent for a payments business. Four sit
outside it and every one is a scope mismatch rather than a data error:

- **Euronet at 5.5 per cent.** Group revenue against the Money Transfer segment's volume only.
- **Western Union at 3.8 per cent.** Revenue covers all company flows; the principal is consumer
  cross-border only.
- **Toast at 3.2 per cent.** Revenue includes software subscriptions; the volume is payments only.
- **CAB Payments at 0.04 per cent.** FX turnover is a wholesale flow, not payments.

## Thirteen names cannot price, and here is each reason

**Not disclosed, correctly blank (3).** Al Ansari publishes transaction growth and mix but no
monetary principal. EVERTEC's "more than 10 billion" is transactions, not dollars. Global Payments
has no standalone FY2025 figure, and the $3.7tn is combined pro forma volume after the January 2026
Worldpay acquisition.

**Segment volume against a group enterprise value (4).** Corpay is Corporate Payments only, Euronet
is Money Transfer only, Fiserv is merchant volume against a group that includes the banking
platform, Nexi is Merchant Solutions only. Same error shape as U-NEXT: the numerator covers the
whole company and the denominator covers a part of it.

**CAB Payments, on three counts.** Negative enterprise value of minus $399m, which makes any EV
multiple meaningless on its own, plus a broken forward series and an FX-turnover metric that is not
payments volume.

Plus the six already excluded from the earlier batch.

## One category rule that must survive into the reveal

The research sheet separates four things and they are NOT interchangeable:

- **CONSOLIDATED_TPV** (16 names): the whole company's payment volume.
- **SEGMENT_ONLY_PAYMENT_VOLUME** (4): one segment, priced against the group. Excluded.
- **FX_TURNOVER** (2, CAB and OFX): wholesale and customer FX flow.
- **REMITTANCE_PRINCIPAL** (3, Wise, Remitly, Western Union): money actually sent, net of
  cancellations and excluding fees.

The last two are real analogues and comparable to each other. Neither is merchant-acquiring TPV and
neither may be pooled with it.

## Where that leaves the payments lane

28 names now carry a volume multiple, and the payments-type band runs from Marqeta at 0.21 per cent
of volume to dLocal at 5.2 per cent, with a median around 2.8 per cent. All five payments fixtures
that had nothing three days ago now see five to seven comparables carrying one: payabli sees
Marqeta, Tyro, Usio, PayPoint and Fawry; dots sees Payoneer, OFX, Wise, Marqeta, Western Union and
Remitly.

Nothing priced moved on the 43 fixtures, because volume multiples are not yet wired into the
football field. That is the next build.

---

# Revision 2, checked. Five of five fixed, one still open

Your corrected sheet is in. Re-running the same three checks.

## The five broken forward series are all fixed

| Company | Was | Now | Local-currency revenue growth | Agrees |
|---|---|---|---|---|
| StoneCo | +343% | +11.8% | +11.8% | yes |
| PagSeguro | +160% | +7.3% | +7.3% | yes |
| CAB Payments | +658% | +5.0% | +5.0% | yes |
| Fiserv | -7.6% against +28.1% revenue | -7.6% | -7.6% | yes |
| Adyen, Wise, Tyro, EML, OFX | small revisions | | | yes |

Every one of the 24 rows with a TPV now grows at exactly its own local-currency revenue rate. The
largest remaining gap is 0.32 percentage points on OFX, which is rounding.

## One row cannot be verified

**Nexi.** Its local-currency CY+0 revenue cell is a red error in the sheet, so there is nothing to
check the 1.8 per cent volume growth against. The CY+0 volume of $982.7bn is right and ties to the
annual report. The forward series is loaded as blank rather than as an unverified number, and Nexi
is excluded from pricing anyway because its metric is Merchant Solutions only against a group
enterprise value. **Please refill that cell on the next pull.**

## Two things the corrections surfaced that are not errors

**Wise's volume is now forecast to FALL 11 per cent, and that is the method meeting a real problem.**
Wise's revenue includes interest income on customer balances, which falls when rates fall. Its
cross-border VOLUME is not falling. Growing volume at the revenue rate therefore points the wrong
way for any business whose revenue has a large interest component: Wise most of all, Payoneer and
Paysafe to a lesser degree. Same shape on OFX at minus 8.5 per cent, EML at minus 2.0 per cent and
Fiserv at minus 7.6 per cent. **Volume and revenue are decoupled for these names and the assumption
that they move together does not hold.** Worth a decision: either forecast volume separately for
interest-earning businesses, or show only their reported year and no forward figure.

**PagSeguro's take rate moved to 4.03 per cent**, above the payments band, once the revenue series
was corrected. That is not a data error: PagSeguro's revenue includes banking and credit income
alongside acquiring, so its revenue covers more than the volume does. Same shape as Toast at 3.15
per cent and Western Union at 3.77 per cent. Scope mismatch, now labelled.

**Nu Holdings has the same revenue-series break the other five had**: local currency runs 6,991 then
22,793, a 226 per cent step. Nu has no TPV so no volume is affected, but that growth rate feeds the
band filter that decides which founders see Nu as a comparable. **It needs the same fix.**

## Where it stands

58 listed names carry a usable volume multiple. The payments-type band runs from Marqeta at 0.21 per
cent of volume to dLocal at 5.2 per cent, median 2.89 per cent, across 30 names. Nothing priced
moved on the 43 fixtures, because volume multiples are still not wired into the football field.

---

# Revision 3. Wise is fixed and the cause is now visible

**Wise: minus 10.9 per cent becomes plus 21.4 per cent, matching its own revenue exactly.** And the
cause of the earlier figure is now readable in the data rather than a hypothesis. Wise reports in
US dollars from FY2026, so its local-currency column IS the dollar column. In revision 2 the CY+0
cell held 2,389 and the CY+1 cell held 2,128, which is a sterling figure sitting next to a dollar
one. Nothing about interest income was involved. My earlier explanation was wrong and this one is
checkable: Wise's implied take rate now comes out at 0.95 per cent, which is what a cross-border
transfer business should look like.

**Payoneer and Paysafe needed nothing.** Both were already internally consistent at plus 6.6 per
cent across all three revisions, and both report in dollars already. My flag on them was about the
concept rather than the data, and at plus 6.6 per cent there is no artefact to correct.

**Three negatives survive and all three are real.** Fiserv at minus 7.6 per cent, OFX at minus 8.5
per cent and EML at minus 2.0 per cent each match a genuinely declining revenue line in their own
reporting currency. EML in particular is a company whose equity has fallen 69 per cent in a year;
a shrinking volume forecast is the correct answer, not a broken one.

## The full progression

| Company | v1 | v2 | v3 | Its revenue |
|---|---|---|---|---|
| CAB Payments | +658% | +5.0% | +5.0% | +5.0% |
| StoneCo | +343% | +11.8% | +11.8% | +11.8% |
| PagSeguro | +160% | +7.3% | +7.3% | +7.3% |
| Wise | +18.7% | -10.9% | **+21.4%** | +21.4% |
| Nexi | -42% | +1.8% | +1.8% | cell still blank |
| Fiserv | -7.6% vs +28% revenue | -7.6% | -7.6% | -7.6% |

**Twenty-four of twenty-five rows now grow at exactly their own local-currency revenue rate.** The
largest gap is 0.32 percentage points on OFX, which is rounding.

## Two cells left, and neither blocks anything

**Nexi.** The local-currency CY+0 cell is still blank in the sheet, so its 1.8 per cent volume
growth cannot be checked against anything. The CY+0 volume of $982.7bn is right and ties to the
annual report, so that is loaded and the forward series is held blank rather than carried
unverified. Nexi is excluded from pricing regardless, because its metric is Merchant Solutions only
against a group enterprise value.

**Nu Holdings.** Local-currency revenue still runs 6,991 then 22,793, a 226 per cent step, which is
the same break the other five had. Nu has no TPV so no volume is affected, but that growth rate
feeds the band filter that decides which founders ever see Nu as a comparable, so it is a live
defect on the matching side rather than the pricing side.

## Where the volume lane now stands

58 listed names carry a usable volume multiple, 30 of them payments-type, and the payments band runs
from Marqeta at 0.21 per cent of volume to dLocal at 5.2 per cent with a median of 2.75 per cent.
Nothing priced moved on the 43 fixtures, because volume multiples are still not drawn on the
football field. That is the next build and it is now unblocked.

---

# Revision 4, and the growth ruling

## Two manual overrides, recorded so they are not lost in the next refresh

**Fiserv.** Capital IQ is returning something wrong on the forward revenue, so the volume could not
be grown off it. You assumed 1 per cent for calendar 2026 by hand. That is an ASSUMPTION, not a
forecast, and it is written into the file header in those words. CY+2 and NTM are left blank rather
than extrapolated from an assumption, so Fiserv carries no volume multiple at all. It is excluded
from pricing anyway, because its volume is merchant-segment only against a group enterprise value,
so nothing is lost. **Replace it the moment Capital IQ is fixed.**

**Nu Holdings.** Your corrected cell renders red in the screenshot, so its value could not be read.
The growth column now shows 44 per cent for CY+1, which implies a CY+0 of about 15,828. That figure
is DERIVED FROM THE STATED GROWTH RATE, not transcribed, and is marked as such in the file. The
226 per cent break is gone.

**OFX and EML removed**, on your instruction. EML still appeared in the screenshot when this was
written, so it was removed on what you said rather than on what the sheet showed. Worth confirming.

## The exchanges are not a mistake, and here is what they are actually doing

You asked why S&P Global, Nasdaq, MarketAxess, Tradeweb and Cboe are in the dataset. 28 names sit in
that cluster and they serve two different founders:

**The DATA names are comparables for a data-subscription business.** S&P Global, Moody's, MSCI,
FactSet, Morningstar and CRISIL are all shown to `fundraisly`, which sells investor matching as a
data product. Your guess was right for that half.

**The EXCHANGE names are comparables for a two-sided marketplace where the traded thing is a
contract.** CME, Deutsche Boerse, Intercontinental Exchange, Multi Commodity Exchange and Indian
Energy Exchange are all shown to `levelten`, a marketplace for renewable power purchase agreements.
That is genuinely the closest listed comparison a PPA marketplace has: a venue matching buyers and
sellers of a commodity contract and earning a fee per trade.

**Nasdaq, Cboe, MarketAxess and Tradeweb reach no fixture at all today.** They are carried for the
archetype rather than used. That is not waste, it is inventory: the founder who needs them has not
walked in yet.

## The growth ruling, implemented

Daniil, 31-Aug-2026: "for growth we need to take longer-term numbers to rank the peers (i.e. the
CAGR). Year 1 and 2 numbers are only there to estimate the TPV / GMV, where available, but should
not be used to categorise the peers."

`g_rank` is now a separate field from `g`. `g` keeps whatever we hold, because the volume forecast
is built off the near-term series and the reveal shows what exists. `g_rank` is what the MATCHER may
see, and it is EMPTY unless we hold a real CAGR.

Fiserv is the argument for the rule in one line: its CY+1 revenue is down 7.6 per cent while its
two-year trajectory is up. Ranking a founder's comparables on that single year would sort Fiserv
next to a shrinking business, which it is not.

**321 of 513 listed names can now rank on growth. 192 cannot, because they carry only a single
forward year and no CAGR at all:** 105 consumer, 75 fintech, 12 software. Those rows are not
excluded and not penalised. They simply compete on business nature alone, and `band_compatible`
already lets an unknown growth pass rather than filtering on it. That is the honest treatment: we do
not know their trajectory, so we do not pretend to.

**The fix is a data pull, not code.** `docs/cagr-needed-pull-list.tsv` lists all 192 with what is
needed: revenue CAGR over CY+0 to CY+2 in local currency. Until that lands, roughly two in five of
our listed names are invisible to the growth dimension of the match.

Nothing moved on the 43 fixtures, because the fixtures carry no founder growth rate, so the growth
term never fires on them. It fires on every live founder, which is where it matters.
