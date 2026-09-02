# Rule A5, made procedural: how we find the next best neighbour

Written 1 September 2026 at Daniil's instruction. His words: *"A5 is important and we need to be
more elaborative, more stage-by-stage in terms of what the engine should be checking, on what next
best neighbour is. I expect this rule to be used very often and perhaps it must be prioritised."*

He is right that it will be used often. Of twenty companies triaged yesterday, seven could not be
priced on an exact match and needed a neighbour. This is not an edge case, it is the normal case,
and it is the thing a founder is paying us for: anyone can look up a direct comparable, and a
founder in a young category is using Fairway precisely because no direct comparable exists.

---

## The idea in one paragraph

Today the engine widens its search until it has enough names, which works but cannot explain
itself. What follows replaces that with a ladder: a fixed order of things we are willing to give
up, cheapest first, where each rung is labelled so the founder can see exactly what was relaxed and
decide whether they accept it. The order is not my opinion. It is measured against our own 429
listed multiples.

---

## First, the part that is not negotiable

**Two kinds of thing look alike in the code and must never be confused.**

**Correctness rules.** Break one and the number is WRONG, not merely less similar. These are never
relaxed, not on any rung, not to reach a count, not ever:

- gross revenue against net revenue
- forward numbers against trailing numbers
- a lender priced on book against anything priced on revenue
- a control deal blended into a minority range
- revenue from a different legal entity than the one being valued
- a figure that was not public when the round was priced

**Proximity dimensions.** Relax one and the comparable is less similar but still honest. These are
the ladder, and only these.

If a search ever has to choose between breaking a correctness rule and returning nothing, it
returns nothing. That is the one case where a blank is the right answer.

---

## The order, measured rather than assumed

For each dimension I asked our own data one question: if you know only this about a company, how
much of the spread in its multiple can you predict? Measured across the 429 listed rows that carry
a multiple, on log multiples.

| Dimension | How much of the multiple it explains |
|---|---|
| Archetype, the business model | **44%** |
| Revenue model | 25% |
| Family, the broad nature | 21% |
| Buyer, who it sells to | 17% |
| Growth rate | 16% |
| Industry, the vertical served | 14% |
| Country | 11% |

**The headline is that WHAT a company does explains three times more than WHO it serves.** Business
model at 44% dwarfs vertical at 14%. That is the empirical backing for a thing we have believed on
instinct: subscription software sold to dentists is well priced by subscription software sold to
restaurants, and badly priced by a dental insurance company.

So we give things up in reverse order of what they explain. Cheapest first.

---

## The ladder

Each rung has a name, and the name goes on screen next to the range.

**Rung 0. Direct.** Same archetype, same revenue model, same buyer, same vertical, same growth band.
If three to five names come back here, stop. This is the ideal and it is rare.

**Rung 1. Different country.** Everything else held. Costs us the least of anything we can give up,
and it is usually the difference between a thin set and a good one, because our data is
concentrated in the US and UK.
*On screen:* "priced against comparable businesses in other markets".

**Rung 2. Different vertical, same business model.** The single most valuable rung, because it is
cheap at 14% and it unlocks the most names. A vertical software company is compared with vertical
software companies serving other industries.
*On screen:* "same business model, serving a different industry".

**Rung 3. Different growth rate.** *Amended by Daniil, 1 Sep:* growth belongs on the ladder, but it
must never be a reason to throw a public company out. His point is right and it is structural: our
founders will grow far faster than almost any listed company, so a rule that drops public comps for
growing too slowly would drop the entire public universe for every founder we have.

So growth works differently from the other rungs. **It orders, it does not exclude.** Among
companies that already pass the business-model test, the ones closest in growth rank higher and get
shown first. A large growth gap is reported next to the range as a caveat the founder can read, in
the form "these companies grow at around 11 per cent a year and you told us you grow at 140 per
cent, which is why the range below is likely to understate you", not as a silent filter.
*On screen:* the growth gap, stated in numbers, next to the range.

**Rung 4. Different buyer.** Small business against mid-market, or mid-market against enterprise.
One step on that scale, never consumer against enterprise, which are different businesses wearing
the same software.
*On screen:* "same product, sold to somewhat larger or smaller customers".

**Rung 5. Adjacent revenue model.** Subscription against usage-based, take rate against transaction
fee. Only between models that behave alike. Never subscription against one-off licence, and never
anything against a take rate on somebody else's transaction, because that is a correctness question
in disguise.
*On screen:* "a different way of charging for a similar product".

**Rung 6. Sibling archetype inside the same family.** The most expensive rung and the last one that
prices. A third-party marketplace against a freelance and services marketplace: both take a cut of
somebody else's transaction, so the economics rhyme even though the archetypes differ.
*On screen:* "a related but not identical kind of business".

**Rung 7. Context only. Stop pricing.** Below rung 6 we name companies, show their multiples
individually, and refuse to build a range. The founder sees real evidence and an honest statement
that we could not assemble a comparable set.
*On screen:* "we could not find close enough comparables to build a range. These are the nearest
businesses we hold, shown individually."

---

## Four rules about how the ladder is walked

**One. Descend until you have three names, then stop.** Do not keep going to reach five. Three
names from rung 2 beat five names that reach down to rung 6, and the range should say which rung it
stopped on.

**Two. Never mix rungs more than one apart.** A set of three from rung 1 topped up with two from
rung 6 is not a peer group, it is two peer groups in a trenchcoat, and its range will be wide for a
reason the founder cannot see. Top up only from the next rung down.

**Three. Descending must only ever add.** Going down a rung must never remove a name or narrow a
range that already existed. We broke this once already: an early version of the top-up logic
dragged the tier down and deleted a range that was already working.

**Four. Report the deepest rung used, not the average.** If four names come from rung 1 and one from
rung 3, the set is a rung 3 set. Comparability is set by its weakest member, exactly as a chain is.

---

## Two things this design needs that we do not have

**Geography is not a field.** Rung 1 is the cheapest and most useful rung, and we cannot implement
it because no row records a country in a form the matcher reads. This should be built before the
rest of the ladder.

**Growth bands are miscalibrated for listed companies, and badly.** This is the mechanical reason
behind Daniil's point above. The bands are MATURE below 77
per cent, GROWING to 206 per cent, HYPER above. Those were fitted on private funding-round growth
rates, where the typical figure is 133 per cent. Listed companies grow at a median of 11 per cent.
The result: **318 of the 319 listed companies that carry a growth rate are classified MATURE**, one
is HYPER, and nothing is GROWING. Growth currently does no work at all when choosing a public
comparable.

This matters immediately because Daniil is about to supply 192 CAGRs to power a dimension that
today sorts everything into a single bucket. Recalibrated to listed reality, growth explains 16 per
cent of the spread, which is real and worth having. **The listed lane needs its own bands, fitted
on listed growth rates, and the private lane keeps the ones it has.** They are different
populations and one set of thresholds cannot serve both.

And per Daniil's amendment, the listed bands are for ORDERING and for the caveat sentence, never for
exclusion. A founder growing at 140 per cent is not badly served by being compared with public
companies growing at 20 per cent, as long as we say so out loud. They are badly served by being told
we have no comparables.

---

## What I would build, in order

1. Recalibrate the listed growth bands on listed rates. Half a day, and it repairs a dimension that
   is currently dead.
2. Add a country field to both lanes and implement rung 1.
3. Implement the ladder as an explicit sequence with a named rung on every range, replacing the
   current widen-until-enough behaviour.
4. Put the rung label into the founder-facing copy, so every range says what was relaxed.

Steps 1 and 2 are data work and can happen while the fixture march runs. Step 3 is the engine
change and it should not start until the manual test mode exists, because otherwise it is untested.
