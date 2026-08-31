# The consistency audit you asked for

31 August 2026. Three questions, answered from the data rather than from memory.

---

## Q1. Public comps are priced on NTM. Do we ask the founder for NTM revenue?

**No, and it was wrong.** Every listed multiple in the file is enterprise value over NEXT twelve
months revenue: 432 of 513 rows carry one and there is no other kind. Every quiz fork asks the
founder for the LAST twelve months and says so in the label.

So we were applying a forward multiple to a trailing number. That is not conservative and not
aggressive, it is a different measure, and for a founder growing 80 per cent it is wrong by 80 per
cent.

**Fixed, by derivation rather than another question.** We already ask for growth, so
`with_forward_revenue()` computes NTM as trailing times one plus growth and stamps
`revenue_ntm_basis = DERIVED_FROM_TRAILING_AND_GROWTH`. Where growth is missing the trailing figure
is used unchanged and the flag says `TRAILING_USED_UNCHANGED_NO_GROWTH_GIVEN`, because a made-up
growth rate is worse than a labelled mismatch. Nothing downstream can mistake a derived number for
something the founder said.

## Q2. Do private comps distinguish NTM from LTM?

**Yes, and it was a mess until this afternoon.** The field existed but carried six different
spellings of four ideas: RUNRATE and RUN_RATE side by side for the same thing, plus four one-off
fiscal-year labels (FY2020, FY2019, FY2021_MAR, FY2022_MAR) that all mean trailing.

62 labels normalised. The private set now reads:

| Period | Rows |
|---|---|
| RUN_RATE | 60 |
| LTM | 51 |
| NTM | 6 |
| blank | 46 |

**Every one of the 71 rows that can feed a range now has a period.** The 46 blanks are all rows
with no multiple, so they cannot reach a founder.

The remaining gap is that a run rate is not the same as a trailing year: a run rate annualises the
most recent month or quarter, so on a fast-growing company it sits between LTM and NTM. 60 of our
rows are run rates, which is the largest single bucket. Worth a decision, but it is a smaller error
than the one above and it is at least labelled.

## Q3. Do we have the machinery to keep gross multiples on gross metrics?

**Now yes. This morning, no.** The field had existed since 27 August and the range even reported
the mix, but nothing stopped a gross row pricing a founder asked for net. The only thing keeping
them apart was somebody remembering to set a flag by hand when the row went in.

Three pieces built today:

1. **A gate.** `basis_compatible()` refuses a gross row for a net founder and the reverse. It is
   guarded so it never fires on a lender, which is priced on book and has no revenue denominator at
   all; without the guard it silently emptied all four lender fixtures.
2. **Dual-basis rows.** `basis_mult()` lets a row hold two readings of the SAME period, one gross
   and one net, and hands back the one matching what the founder was asked for. Zepz is the first:
   $338m gross from the round announcement at 14.8x, $238m net from the filed accounts at 21.0x,
   same twelve months. A net founder now sees 21.0x and a gross founder sees 14.8x. Before this the
   row could only carry one number, so whichever we chose was wrong for half the founders.
3. **Labels everywhere.** The private set now reads NET_REVENUE 41, ARR 39, ARR_RUNRATE 24,
   GROSS_REVENUE 12, BANK_NOI 2, NONE 45. **All 71 rows that can price carry a basis.** The 45
   NONE rows are book-priced lenders and rows with no multiple.

**THE HOLE THAT REMAINS, AND IT IS THE BIGGEST ONE LEFT.** A listed row has no `revenue_basis`
field at all. Statutory revenue means net for a marketplace like Etsy and gross for a first-party
retailer like Ocado, and we hold both in the same family with nothing recording which. That is the
OLIPOP error at the listed level and it is not yet fixed. It needs a basis tag per listed name,
which is a data job of about 500 rows, mostly mechanical: an owned-inventory retailer is gross, a
take-rate marketplace is net, a subscription business is net.

---

## The volume metrics, and your four challenges

You were right on all four, and the rule underneath them is now in the code rather than in
somebody's judgement. **A gross volume may price a company only when the enterprise value and the
volume describe the same thing.** Two ways they do not:

**A balance-sheet lender.** Avarda IS a bank. Its value sits in a loan book and it prices on price
to book, so enterprise value over transaction volume is not a multiple of anything. Same for Credit
Saison, a card issuer and consumer lender, and Humm. The disclosures stay as facts; they may not
price.

**A segment volume against a group enterprise value.** U-NEXT is a streaming business whose cashless
arm has a GMV, and dividing group value by segment volume gave 341.6x, which is how the error
announced itself. Digital Garage is an incubation and marketing group that owns a payments arm.
Also caught by the same rule: Cass (transportation only, no consolidated total), Priority (Merchant
Solutions segment) and WEX (Corporate Payments, and the figure includes volume issued by others).

**AvenuesAI is the one you should keep.** CCAvenue is a payment aggregator, which is exactly the
business a TPV describes. It looked wrong only because of the scale error: at the corrected
$57.1bn its enterprise value is 0.50 per cent of volume, which is a sensible take-rate multiple.
Seven names are now marked unusable and 38 carry a volume multiple.

## The scale errors: you were right, and this is on me to catch

Three rows were out by a thousand or a million times, because the reported figure was in billions or
trillions of local currency and the conversion multiplied by the rate without normalising to
millions. U-NEXT, Digital Garage and AvenuesAI. Your corrected figures are in.

**And the deeper failure is that they never reached the engine at all and I did not tell you.** The
twelve non-USD rows had an empty USD column, so the loader read nothing, so they were absent from
every valuation while sitting in the file looking present. I flagged them as "needing FX" in a list
rather than saying plainly: THESE TWELVE COMPANIES ARE NOT IN ANY VALUATION. That is the flag you
should have had and did not.

## Public comps: threshold lowered, with the disclaimer

Five of our 43 test companies were getting NO listed peers at all, out of eligible pools of 74 to
179 names. Not a thin set: zero. The founder saw nothing, which reads as "we have no data" when we
hold hundreds of names in their family.

The floor now drops for DISPLAY only. Where nothing clears the bar for core, the neighbourhood comes
back in the secondary group with the tier reported as `CONTEXT`, and CONTEXT is not a pricing tier,
so nothing there can ever price a founder. What the five now see:

| Fixture | Shown as context |
|---|---|
| payabli | Repay, Marqeta, Tyro, Usio, PayPoint |
| rainforest | Marqeta, Repay, Tyro, PayPoint, Usio |
| moov | Marqeta, Repay, Usio, PayPoint, PayPal |
| dots | OFX, Al Ansari, Marqeta, Western Union, Remitly |
| goldfish | Truecaller |

Those are the right neighbours. No priced range moved on any of the 43 fixtures.
