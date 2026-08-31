# Brief for Fable: know what every multiple IS, then match it to what the founder gives us

Written 31 August 2026 at Daniil's instruction. His words:

> "I want someone to go through the base and make sure we know what each multiple is (i.e. is the
> multiple on each particular transaction on net vs gross basis, is it forward looking vs. backwards
> looking. Then we need to make sure our machinery can MATCH the numbers given by a founder (net vs
> gross, fwd looking vs backwards) with what we have in our database)."

It makes sense and it is the right shape. It is two jobs, not one, and they fail differently: the
first is a data job that fails by being incomplete, the second is an engine job that fails silently.

## Why this matters more than it sounds

A multiple is a ratio, and a ratio is only meaningful when the numerator and denominator measure the
same thing on both sides of the comparison. We have been getting this wrong in two directions at
once and neither announced itself.

**Gross against net.** On a payments business the two differ by roughly an order of magnitude.
Razorpay sat in the fintech file at 67.6x on a gross denominator for four days, next to net-revenue
rows, because the only thing keeping them apart was somebody remembering to set a flag by hand when
the row went in.

**Forward against trailing.** Every listed multiple we hold is enterprise value over NEXT twelve
months revenue. Every quiz fork asked the founder for the LAST twelve months. For a founder growing
80 per cent that comparison is wrong by 80 per cent, and it was wrong for every founder who has ever
touched the engine.

## Where it stands tonight

**Private, basis: done.** All 71 rows that can feed a range carry one. NET_REVENUE 41, ARR 39,
ARR_RUNRATE 24, GROSS_REVENUE 12, BANK_NOI 2. The 45 marked NONE are book-priced lenders and rows
with no multiple, neither of which has a revenue denominator.

**Private, period: done, after a clean-up.** The field carried six spellings of four ideas, RUNRATE
and RUN_RATE side by side for the same thing plus four one-off fiscal-year labels. 62 normalised.
RUN_RATE 60, LTM 51, NTM 6, blank 46, and every blank is a row with no multiple.

**Listed, period: known by construction.** Every one of the 432 listed multiples is EV over NTM
revenue. There is no other kind in the file.

**Listed, basis: NOT DONE, and this is the job.** A listed row has no `revenue_basis` field at all.
Statutory revenue is net for a take-rate marketplace like Etsy and gross for a first-party retailer
like Ocado, and both sit in the same family with nothing recording which. That is the OLIPOP error
at the listed level, and it is live right now.

## Job one, the data: tag 513 listed rows

Add `revenue_basis` to every listed row. Mostly mechanical, and the archetype does most of the work:

| Archetype | Basis | Why |
|---|---|---|
| Owned-Inventory Retail, Consumer Brand | GROSS_REVENUE | the company buys and resells, so net sales already ARE the transaction value |
| Third-Party Marketplace, Freelance & Services Marketplace | NET_REVENUE | a take rate on somebody else's transaction |
| Merchant Acquiring & PSP | CHECK EACH ONE | some report gross of interchange, some net, and the gap is an order of magnitude |
| Vertical Software, Business Applications, Cybersecurity | NET_REVENUE | subscription revenue has nothing to pass through |
| Local Delivery & On-Demand | CHECK EACH ONE | a first-party dark store is gross, a commission marketplace is net, and they sit together |
| Lending & Credit, Digital Bank & Deposits | NONE | priced on book, no revenue denominator |

The two CHECK EACH ONE rows are where the work is. Do not let an archetype rule decide those: read
the revenue recognition note. Payments and delivery are exactly the two sectors where the same
archetype contains both kinds, and getting one wrong is a ten-times error in a founder's valuation.

**Do it the way we do everything else: source per row, wording verbatim, two independent agents on
anything a rule could not decide.** A basis assigned by guess is worse than a blank, because a blank
is honest and a wrong label prices somebody.

## Job two, the engine: make the machinery match

Half of this is built. Look at these three before writing anything:

- `basis_compatible(prof, row)` refuses a gross row for a net founder and the reverse. Guarded so it
  never fires on a lender, which has no revenue denominator; without the guard it silently emptied
  all four lender fixtures within minutes of being switched on.
- `basis_mult(prof, row)` handles a row that holds TWO readings of the same period. Zepz is the
  first: $338m gross from the round announcement at 14.8x, $238m net from the filed accounts at
  21.0x, same twelve months. A net founder sees 21.0x, a gross founder sees 14.8x.
- `with_forward_revenue(prof)` derives the founder's NTM revenue as trailing times one plus growth,
  and stamps how it got there so nothing downstream mistakes it for something the founder said.

**What is missing on the engine side:**

1. **The listed lane has no basis gate at all.** Once the tags exist, `basis_compatible` has to run
   on the listed side too. Today it runs only on private.
2. **The quiz cannot ask which basis the founder is giving.** The gate already understands NET,
   GROSS and BOTH on the profile. There is no question producing that value, so it defaults to net
   for everyone. Daniil wants the founder to be able to give either or both, and then be priced on
   like for like.
3. **A run rate is not a trailing year.** It annualises the latest month or quarter, so on a fast
   grower it sits between LTM and NTM. 60 of our private rows are run rates, our largest bucket, and
   they are currently treated as if they were trailing. Labelled, not resolved.

## How to check it is actually done

Not by reading the code. By these four numbers, each reproducible from a command:

1. Listed rows with a `revenue_basis`: target 513 of 513, today 0.
2. Priced private rows with both a basis and a period: today 71 of 71. Must stay there.
3. Fixtures where a gross row prices a net founder: must be 0. It is 0 today on private and
   UNMEASURABLE on listed, because the field does not exist.
4. Fixtures where a trailing founder figure meets a forward peer multiple: was 43 of 43 this
   morning. Should be 0 once `with_forward_revenue` is wired into the listed lane, which it is not
   yet.

Number 4 is the one to watch. The derivation exists; nothing calls it.

---

# ADDED 31 August, evening: this becomes one of Fable's standing checks

Daniil asked who audits the basis. **Fable does, at every handover, alongside the inventory and the
golden suite.** It goes in the evening handover from tonight.

## The check, in one command

```
python3 tools/audit_basis_period.py
```

It reads the metric wording on every private row that carries a multiple and reports where the
label contradicts it. It asserts nothing and changes nothing, because the wording is often genuinely
ambiguous and a script that guesses is how we got into this. A human decides.

## What the numbers should say

Tonight it prints **43 rows need a human to look at the label, 65 rows agree with their own words**,
out of 108 that carry a multiple. Three things must hold at every handover:

1. **Rows agreeing with their own words only ever goes UP.** If it falls, a row was edited without
   its label being revisited, and that is exactly how Razorpay's gross 67.6x sat in the fintech file
   for four days.
2. **Every row that feeds a range has both a period and a basis.** 71 of 71 tonight. A row that can
   price a founder and cannot say what it is measuring must not price a founder.
3. **`revenue_basis_source` says how we know.** 13 STATED, the rest INFERRED, and a handful marked
   INFERRED_HIGH_RISK. STATED should climb as the backlog is worked; INFERRED_HIGH_RISK should reach
   zero, because every one of those is a row that could be wrong by an order of magnitude.

## What "audited" actually means for a row

Not that the field is filled. That is the easy half and it is already done. Audited means somebody
read the source and can say WHICH of these the number is:

- **Basis.** Does the line contain money that belongs to somebody else? A freight broker's revenue
  holds the carrier's money, a staffing platform's holds the worker's wage, a marketplace commission
  does not, and a first-party retailer keeps the whole sale price so its revenue is NET in our sense
  even though it looks gross beside a commission. The test is ownership of the money, not the size
  of the number.
- **Period.** Trailing, or forward. Daniil's ruling of 31-Aug: a run rate and an ARR are FORWARD,
  because both annualise what the business is earning now rather than the year just finished. Two
  buckets, not three.
- **Entity.** The one that caught Flipkart. Whose revenue is it, and is it the same entity the
  valuation covers? Flipkart India Private Limited is the B2B wholesale arm at Rs 43,357 crore;
  Flipkart Internet Private Limited is the marketplace at Rs 8,115 crore. Same group, five times
  apart, 6.4x against 34.2x. Nobody had asked which one the number was.

## The backlog, worst first

The five INFERRED_HIGH_RISK rows are down to one after tonight. dLocal, Pine Labs, Flipkart twice
and StockX are all resolved from primary sources. What is left:

- **The 90 INFERRED rows.** Each is a basis somebody read off the business model rather than off the
  source. Most will be right. Work them down by sector, hardest first: payments and delivery are the
  two where the same archetype contains both gross and net reporters.
- **The 43 rows the audit still flags.** Mostly rows where the wording says only "FY2021 revenue"
  and the basis was assumed. That is not a defect, it is an unverified assumption, and the
  difference matters when somebody asks us to defend a number.
- **The listed side, deprioritised by Daniil on 31-Aug** but still real: 513 rows with no
  `revenue_basis` field at all.
