# The honesty copy. Every flag, and the sentence it owes the founder.

27 August. The engine attaches eleven facts to every range because a number would otherwise mislead.
None of them reaches a founder today. This is the deck of strings that closes that gap.

**Three rules the whole deck follows.**

1. **Say the fact, then say what to do with it.** A caveat that only warns makes the product look
   weaker. A caveat that tells the founder how to use the number makes it look expert.
2. **Never apologise for the data.** "Only two comparables" is an apology. "Two companies in the
   world have priced this business model recently, and here they are" is a finding.
3. **Show the working where we have it.** Where a flag has names or words behind it, print them.
   `shared_words`, `control_names`, `sole` and the regression scatter are all printable.

Counts below are how often each fires across the 21 real profiles, so you can see what is edge case
and what is the common path.

---

## 1. How the range is drawn: `display`

**RANGE, 13 of 20.** No extra sentence needed. This is the normal case.

**DIAMOND, 5 of 20.** One comparable priced this.
> One company matches you closely enough to price from: **{sole}**. A single point is not a range, so
> treat it as a marker rather than a spread. More rounds in this category will widen it.

**SCATTER, 2 of 20.** The spread is more than six times low to high.
> These companies are comparable to you but they are not comparable to each other: {low}x to {high}x.
> Averaging them would produce a number none of them supports, so they are shown as separate points.
> Where you land in that spread is the argument, and it is usually about growth.

---

## 2. How close the comparables are: `closeness` and `shared_words`

This is the one the founder cares about most, and it replaces the old pass-or-fail flag.

**SHARED_PRODUCT, 3 of 20.**
> These companies do what you do. Shared product language: {shared_words}.

**STRONG_OVERLAP, 5 of 20.**
> Close, on {n} shared descriptors: {shared_words}. Not identical businesses, which is normal.

**PARTIAL_OVERLAP, 7 of 20.**
> The nearest businesses we hold. They share {shared_words} with you and diverge elsewhere. Read the
> range as a starting point you can argue up or down, not as a verdict.

**THIN_OVERLAP, 5 of 20.**
> **We do not have a close comparable for you yet.** The nearest companies share little more than
> "{shared_words}" with you. The range below is the best available read, not a peer set, and we would
> not put our name to it without a conversation.

That last one should also trigger the consultation route and go into the gap log. It is the honest
"we don't know" and it is worth more to the brand than a confident wrong answer.

---

## 3. How much evidence is behind it: `thin` and `band`

**`thin`, 10 of 20.** Fewer than three priced comparables.
> Drawn from {n} priced rounds. Thin, and a fourth could move it.

**`band` is ADJACENT, 15 of 20.** The names pricing the number are adjacent rather than direct.
> Priced off businesses in your category rather than your exact niche.

---

## 4. What kind of number each contributor is

**`bounded`, 13 of 20.** This is the most common flag and the most important one, because it is
directional.
> **At most {high}x.** {n} of these rounds disclosed revenue as a threshold ("more than $100m")
> rather than a figure, so the true multiple is lower than shown, not higher. We would rather
> understate than flatter.

**`control_names`, 4 of 20.**
> {names} is a change of control. A buyer of the whole company pays for control, so that multiple
> sits above what the same business would fetch in a minority round.

**`listed_target_names`, 3 of 20.**
> {names} was a public company when it was bought, so its price was set by the stock market rather
> than negotiated with one investor. Different kind of price, not a slower version of the same kind.

**`anchor_dropped`, 1 of 20.**
> **The company you will recognise here is not in the number.** {closest} is your nearest
> comparable, but its only transaction cannot price a minority round, so the range is built from the
> others. Worth knowing before you quote it.

**`basis_mix` has more than one entry, 11 of 20.**
> These rounds were priced on different measures: {ARR / annualised run rate / net revenue}. We have
> matched you to the closest, and the mix is why the spread is wider than it looks.

And where the founder's own basis differs from every contributor:
> You gave us {founder_basis} and these rounds were priced on {their_basis}. Not the same measure.
> The comparison still holds directionally; the decimal place does not.

---

## 5. The regression row

**When it prints:**
> Your peers' multiples are explained by their growth with an R-squared of {r2}%. At your growth rate
> of {growth}%, that line implies {low}x to {high}x. The scatter is below: every point is a real
> company, and you can see where you sit.

**When R2 is below 50%:**
> We could not draw a defensible line through these companies: their multiples are not explained by
> their growth. That usually means the set is not homogeneous enough to regress, so we have left the
> row out rather than fit a line to noise.

**When the founder is off the end of the range, which is the common refusal:**
> No listed company in your category grows as fast as you do. The fastest is {peer_high}%, you are at
> {growth}%. We can fit a line to them but we cannot honestly read your value off the end of it, so
> this row is blank. **This is a gap in the data, not in your business**, and it is the reason the
> private rounds matter more for you than the public comparables do.

---

## 6. Two things the field itself should say

**On the unrefined row:**
> The broad sector average, before anyone looked at your business. Every method below narrows it.

**On the whole field, when the founder has answered the optional questions:**
> {n} of your answers narrowed this. Gross margin moved you from a revenue multiple to a gross-profit
> one; retention moved you within the range.

That second one is the argument for answering the optional questions, and it is better made by
showing the range tighten than by marking a field required.

---

## What I would check before this ships

The counts above say the common path is: a RANGE, drawn from ADJACENT names, PARTIAL or STRONG
overlap, BOUNDED, on a MIXED basis. So the sentences that will be read most are the bounded one and
the closeness one. Those two are worth more drafting attention than the rest put together.

And one warning. Eleven caveats on one screen is not honesty, it is noise. My recommendation: show
at most **two** inline, chosen by severity in this order, and put the rest behind a "how this was
built" disclosure that any founder can open:

1. THIN_OVERLAP or `anchor_dropped`, because both mean the number may not be about them at all
2. `bounded`, because it is directional and changes what the number means
3. everything else
