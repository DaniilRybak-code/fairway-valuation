# 31 August, afternoon: rulings applied, and four things that need you

## 1. Nothing was lost, and the new data is in

All 23 rounds from the three tabs you sent are transcribed to
`data/raw/2026-08-31_private-rounds-with-sources.csv` with source URLs on every row. 113 of our 163
private rows now carry a source URL, against zero on those companies yesterday.

Fourteen rounds went into the engine. Five companies had to be TAGGED first, and this is worth
knowing: a private round whose company has no row in the tags file is skipped by the loader
silently. Creditas, Fundbox, Gorillas, Jobandtalent and Loadsmart were all in that state, so
inserting the rounds alone would have changed nothing at all. They are tagged now.

Private set: 149 rows to 163. Priced rows feeding ranges: 63 to 71, from 62 companies.

## 2. Marqeta: you are right and my question was unnecessary

Your workbook named the Forbes article, gave its date, and said the S-1 figure conflicts and is not
back-applied. That is a ruling, not a conflict, and I should have applied it rather than asked.
Applied: 14.3x on the contemporaneous Forbes figure, marked as a CEILING because "more than $300m"
is a threshold, and out of every range because the basis is gross.

## 3. SKIMS is safely saved

Two rounds, both feeding ranges: Nov-25 at 5.0x and Jul-23 at 5.3x.

## 4. The rulings, applied

**Zepz.** 14.8x on the $338m round-announcement figure. Your rule is now recorded in the file as a
GENERAL rule, in your words: where a round announcement and later filed accounts describe the same
period, the announcement wins, because it is the primary source and it is what the investor priced
against. The $238m accounts figure is kept in the note, not discarded. One flag: the two differ by
42 per cent, which is the size of a gross-versus-net gap on a remittance business. If $338m is
gross, the row has to leave the net range.

**Marqeta.** Contemporaneous Forbes. Done, above.

**Razorpay.** Dropped. The multiple is cleared, the row is kept for audit and cannot reach a
founder.

**Pine Labs.** One denominator chosen and the reason recorded. We use the FY2021 statutory total
revenue of Rs 726.16 crore, about $99.08m at Rs 73.27 on the pricing date, giving 30.3x. Three
reasons: it is a defined and auditable line for a period that closed before the 17-May-2021
pricing; the rival "$107m" figure states neither definition nor period, so we would not know what
we were dividing by; and Rs 726.16 crore is the figure the market actually cites. And the choice
barely matters, which is the argument for keeping the row rather than dropping it: $3,000m over
$99.08m is 30.3x, over $107m is 28.0x, an eight per cent difference. Source: Entrackr, 5-Jul-2022.

**Better.com.** Kept with the comment: a SPAC valuation is negotiated between sponsor and target,
not cleared by competing buyers, so it is weaker evidence than a priced venture round.

## 5. TWO CONFLICTS I WILL NOT RESOLVE MYSELF

**AG1.** The new e-commerce tab says Jan-22, $1,200m post, $600m revenue, 2.0x. Our file says
$1,315m post, $150m revenue, 8.8x. Both numerator and denominator disagree and the multiple differs
by four times. Which is right?

**Zopa.** The new blue tab says $750m post over GBP29.809m of FY2020 statutory revenue, 25.16x,
citing the filed annual report. Our master file said 8.8x on GBP85m. GBP29.809m is the exact
statutory line quoted verbatim with the filed report attached, so I lean to it, but 25.16x for a
lender is a striking number and I would rather you looked. Zopa's price-to-book of 5.6x is
unaffected and is what actually prices our lender fixtures.

## 6. GMV: I need you to repaste

You are right that the ratio should use the USD figure against USD enterprise value. Checking my
records honestly: in the file I wrote from your screenshots, the USD column is EMPTY for the twelve
non-USD rows, which is why I flagged them. Either the column was blank in the part of the sheet I
could see, or I misread it. I cannot verify either way now, because the images are gone.

Please repaste those twelve rows: Airtasker, Freelancer, Humm, Credit Saison, U-NEXT, Digital
Garage, BASE, Worldline, PayPoint, AvenuesAI, Avarda, Fawry. Nothing else from that sheet is
needed.

## 7. Gross versus net is now a RULE, not a habit

You asked whether the like-for-like logic is wired. It was not. Every private row has carried
`revenue_basis` since 27-Aug and the range reported the mix, but nothing stopped a gross-revenue row
pricing a founder who was asked for net. The only thing keeping them apart was somebody remembering
to set a flag by hand when the row went in. That is how Razorpay's 67.6x on a gross denominator sat
in the fintech file for four days.

It is a gate now. Ten rows carry GROSS_REVENUE and none of them can enter a net founder's range.
They stay visible as context with the basis on the label, because a founder shown only net
comparables cannot tell that the gross ones exist.

The quiz asks every fork for NET revenue and says so in the label, so a founder's basis is net
unless they say otherwise. Your optionality idea is half built: the gate already reads a
`revenue_basis` on the profile and handles NET, GROSS and BOTH. What is missing is the quiz
question that lets a founder say which they are giving. That is a quiz change, not an engine one.

## 8. How many names, and why the payments handful was thin

Your rule is built. Three to five names when the match is almost perfect, five to seven when it is
weaker. The band that builds the range also widens now until it holds at least three names: it used
to stop at the first tier that held anything, which on a thin set meant a one-name diamond. Hived
had Gorillas as a direct comparable and Wolt as an adjacent one, and the old rule threw Wolt out and
drew a range off Gorillas alone.

Across the 43 fixtures the handful is now three or more on 37 of them, and seven on 19.

## 9. The eleven are not hidden. Something worse is happening

You asked why we hide the eleven peers we hold. We do not hide them. Three different things are
going on and only one of them is about those eleven.

**Five of our 43 test companies get NO listed peers at all.** goldfish, payabli, rainforest, moov
and dots. Not a thin set: zero, from an eligible pool of 74 to 179 names that pass the family and
balance-sheet gates. So Adyen is not being hidden from payabli; nothing at all is being shown.
This is the real defect and it is bigger than the peer-coverage number suggested.

**Where names are shown, the held ones lose on score.** PayPal scores 4.6 for Trolley while the
lowest name actually shown scores 8.4. That is a weighting question, not a bug: PayPal is a
plausible comparable that our tag overlap does not reward.

**Two are fenced out on purpose, wrongly.** Wise and Block are tagged into lender or bank
archetypes, and `balance_sheet_compatible` fences lenders off from non-lenders in both directions.
The fence is right; the tags are wrong. Wise and Block are payments businesses first.

Fixing the empty-lane defect is the next thing I do.
