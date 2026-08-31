# For Fable to double check: four things I changed and three I could not settle

31 August 2026, late afternoon. Tasks 1 to 4 done. What follows is what I would want checked if
somebody else had done it.

## What changed

**1. Private basis and period labels audited against their own words.** New tool,
`tools/audit_basis_period.py`, reads the metric wording on every priced private row and reports
where the label contradicts it. It asserts nothing and fixes nothing, because the wording is often
genuinely ambiguous and a script that guesses is how we got here. First run flagged 52 of 108. After
the fixes below it flags 43, and 65 rows now agree with their own words.

**2. Nine period labels were simply wrong and are corrected.** Five denominators described as
"expected", "forecast" or "projection" were labelled trailing and are now NTM: Loadsmart Nov-20,
SKIMS twice, Liquid Death. Four described as annualised or run rate were labelled LTM and are now
RUN_RATE: Mews Mar-24, Creditas three times, Jobandtalent. The Creditas rows are a single quarter
multiplied by four, which is not a year by any reading.

**3. Forty-two rows carry a basis the source never stated, and the file now says so.** New column
`revenue_basis_source`: STATED where the source uses the words, INFERRED where somebody read it off
the business model. 13 STATED, 90 INFERRED, 5 INFERRED_HIGH_RISK. Usually the inference is right.
The test is not "is it a big number", it is whether the line contains money belonging to somebody
else. A freight broker's revenue holds the carrier's money and a staffing platform's holds the
worker's wage; a first-party retailer keeps the whole sale price, so its revenue is NET in our sense
even though it looks gross beside a commission.

**THE FIVE HIGH-RISK ONES NEED A HUMAN TO READ THE FILING**, because each could be wrong by an order
of magnitude and each is currently pricing founders:

| Row | Multiple | The question |
|---|---|---|
| Flipkart Jul-21 | 6.4x | Flipkart India Pvt Ltd is the WHOLESALE entity, not the marketplace entity. Its revenue is gross B2B sales, not commission. |
| Flipkart Jul-23 | 5.2x | Same entity question. |
| Pine Labs May-21 | 30.3x | Revenue from operations on an Indian payments company may include pass-through interchange. |
| StockX Apr-21 | 9.5x | StockX takes possession for authentication, which can push it into gross revenue recognition. |
| dLocal Apr-21 | 48.0x | Total revenues, before cost of services. Whether that is gross of network costs decides the basis. |

**4. A forward multiple now meets a forward number.** `founder_revenue_for(prof, period)` returns
the founder's own revenue on whichever basis a comparable was built on. A founder with $10m trailing
growing 80 per cent is $10m against an LTM comparable, $18m against an NTM one and $14m against a
run rate. Every listed multiple we hold is EV over NTM revenue, so until today every founder was
being priced by applying a forward multiple to a trailing number. Both lanes now carry `period_mix`
and `period_span` on the range. Purely additive: no priced range moved when it went in.

The run-rate figure is a MODELLING CHOICE, not a fact. It assumes a run rate leads a trailing year
by half a year of growth, and it returns `ESTIMATED_HALF_A_YEAR_OF_GROWTH` so nothing downstream can
present it as something the founder said. 60 of our private rows are run rates, our largest bucket,
so this assumption is doing real work and deserves a second opinion.

**5. The lender fence now follows the PRIMARY archetype only.** It used to fire on either slot, so
Payoneer and Wise were fenced out because they hold customer funds and carry a banking archetype in
the secondary slot, and Block because it owns Square Financial Services. All three are payments
businesses the market prices on revenue, and all three were being blocked from exactly the founders
who needed them. A genuine lender is unaffected: its primary still says Lending & Credit.

**6. The listed lane now sizes like the private lane.** Three to five names on a close match, five
to seven where the match is weak, per Daniil's rule. Adyen was being dropped from Payabli at a score
of 7.8 against a cut of 9.6, which is sixth place rather than a hidden name.

## What moved, and the one I am unsure about

Eight priced ranges moved, all on the listed lane, all because the fence stopped blocking real
payments names. `dots` went from NO listed range at all to a core diamond at 1.8x on Payoneer plus a
six-name secondary range. That is the fix working.

**PLEASE LOOK AT TROLLEY.** Its listed core went from one name at 6.4x to two names spanning 0.7x to
6.4x: EML Payments at 0.7x and Corpay at 6.4x. That is a nine-fold spread from two names, and a
range built like that is close to meaningless. Either EML is mis-tagged, or the two genuinely are
the closest listed comparables to a mass-payout business and the honest answer is that the listed
lane cannot price Trolley at all. I do not know which and I would rather you decided.

## Still open, and neither is mine to settle

**AG1.** New tab says Jan-22, $1,200m post over $600m revenue, 2.0x. Our file says $1,315m over
$150m, 8.8x. Four times apart on both numerator and denominator.

**Zopa.** New tab says 25.16x on GBP29.809m of FY2020 statutory revenue with the filed report
attached. Master file says 8.8x on GBP85m. The price-to-book of 5.6x is unaffected and is what
actually prices our lender fixtures, so this only matters for the revenue lane.

## What I deliberately did NOT do

Daniil ruled that gross-versus-net mapping on the PUBLIC peers is not the priority and the private
side is. So the 513 listed rows still have no `revenue_basis` field. That remains a real hole and it
is the OLIPOP error at the listed level, but it is now a known and deprioritised one rather than an
unnoticed one.
