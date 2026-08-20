# The valuation engine: rows, inputs, and where the data comes from

**Status:** plan. 20 Aug 2026. Supersedes the row set in `football-field-plan.md`; the front-end and blur design in that doc still stand.

## 1. Where the earlier plan was wrong

**Stage benchmark is not a valuation method.** Correct. Two companies at seed with the same sector can be worth 3x different amounts. What it *is* is the analogue of the L1Y trading range at the top of the Juno page: market context that frames the field without driving it. Keep the row, label it context, put it first, and never let it move the number.

**Comparable rounds must be filtered on revenue scale.** Correct, and it is the whole difficulty. A comp set of "seed fintech" is useless. A comp set of "seed fintech, $80k to $150k MRR, Europe, last 12 months" is the product. Any comp query needs sector, stage, revenue band, geography and vintage, and if fewer than about five transactions survive that filter we do not draw the row.

**Growth-adjusted range.** Right, and it should be the anchor row rather than an extra one. More on the build below.

**Two band answers cannot drive a multiple.** Correct, and this is the binding constraint on everything else. See section 3.

## 2. Where I would still argue: round size

You are right that it is not a valuation methodology. I think it belongs in the field anyway, for the same reason the LBO row belongs in Juno's.

The LBO row is an ability-to-pay analysis: what can this buyer pay and still clear a 17.5% to 22.5% IRR. It is not a view on intrinsic value, it is a view on what price the transaction structure permits. At seed there is an exact analogue, and it is arguably more binding than at large cap: **most seed funds have ownership targets**, typically 10% to 20% for a lead. A founder raising $3M from a fund that must own 15% is implying a $20M post-money, whatever anyone thinks the company is worth. Price gets set by the intersection of cheque size and ownership target far more often than by any multiple.

So I would keep it, rename it **Ownership-target implied valuation**, and label it as constraint-driven exactly as the LBO row is. It is frequently the row that contradicts the founder's ask, which makes it the most commercially useful thing on the page.

If you still disagree after that framing, it comes out of the field and becomes a standalone sanity-check box underneath. Your call, and I will build whichever.

## 3. The inputs problem, which is the real blocker

Today we collect a revenue band, a growth band and a profitability band. You cannot apply a multiple to a band. `$50k–$150k/mo` spans a 3x range in ARR before any multiple is applied, which alone makes the output wider than any method's dispersion.

To run the multiple rows we need actual numbers:

| Input | Needed for | Why |
|---|---|---|
| ARR or MRR, exact | Rows 3, 4, 5 | The multiplicand. Nothing works without it. |
| Revenue growth, exact, YoY and last 3 months | Row 4 | The independent variable in the regression. |
| Gross margin | Rows 3, 4 | A 40% margin business does not get a software multiple. |
| Net revenue retention | Row 4 | The single strongest driver of multiple dispersion in listed SaaS. |
| Net burn and runway months | Row 6, concerns | Burn multiple, and the deadline discount. |
| Country of incorporation | Rows 1, 3, 5 | US anchors need an explicit adjustment elsewhere. |
| Last round: date, amount, pre or cap | All rows | The strongest single anchor we could have, and free to ask for. |
| Headcount | Row 3 | Size proxy for the discount band. |

**Design resolution: two-tier intake.** Do not put eight numeric fields in a four-minute quiz.

- **Tier 1, the current nine questions.** Produces rows 1 and 2 only, both fully computable from bands. The range is wide and the page says why.
- **Tier 2, on the result screen.** "Add five numbers and two more rows unlock." ARR, growth, gross margin, last round, country. Computes rows 3 and 4 live, in front of them, and visibly narrows the field.

That mechanic is better than the current blur in three ways. Precision is bought with information rather than money, which feels fair. It qualifies hard, since founders who type real numbers are actually raising. And it produces exactly the data the reviewer needs before the 24 hour email, which currently arrives with nothing.

## 4. The revised row set, mapped to the Juno structure

| Juno row | Ours | Drives the number? |
|---|---|---|
| L1Y trading range | **1. Market context.** Stage, sector and geography valuation band | No, context only |
| LBO ability to pay | **2. Ownership-target implied.** Round size divided by typical lead ownership target | Yes, as a constraint |
| Trading multiples | **3. Revenue multiple, size-banded.** ARR times sector EV/Revenue, with size and private discounts stated | Yes |
| Regression, multiple vs CAGR | **4. Growth-adjusted multiple.** Fitted EV/Revenue at this company's growth rate, from a listed peer regression | Yes, the anchor |
| Precedent transactions | **5. Comparable private rounds.** Filtered on sector, stage, revenue band, geography, vintage | Yes, when we have the data |
| Broker target prices | **6. Reviewer band.** The banker's view after reading everything | Paid only |

Free after tier 2: rows 1 to 4. Locked: rows 5 and 6, plus the convergence line. That is a genuinely useful free output and still leaves the two things founders most want behind the paywall.

## 5. Row 4 in detail, because it is the one that makes this credible

Listed software multiples are not flat, they are a function of growth, and the relationship is strong enough to fit. The method:

1. Maintain a peer set per sector, roughly 20 to 40 listed names.
2. For each: EV, LTM and NTM revenue, revenue growth, gross margin.
3. Regress EV/Revenue on growth. Store slope, intercept, R squared, n, and date.
4. Read the fitted multiple at the founder's growth rate.
5. Apply the private-company discount stack, each component stated separately: size, illiquidity, stage.
6. Multiply by ARR. That is the row.

The tooltip then reads something like: *"Listed B2B software, 34 names, EV/Revenue regressed on revenue growth, R² 0.61, as at 31 Jul 2026. Fitted multiple at 60% growth: 8.4x. Less 45% size and illiquidity discount: 4.6x. Applied to $1.2M ARR."*

That is a sentence a founder can take to an investor, which is the entire point. And every element of it is either public data or a stated judgement.

The discount stack is where your reviewers earn their fee. It is the parameter no competitor can copy, it should be per sector and per size band, and it must always be shown rather than buried, because an unexplained 45% haircut is the fastest way to lose a numerate founder.

## 6. The data question, answered directly

**Rows 3 and 4 need no vendor at all.**

- Sector EV/Revenue: Damodaran's NYU dataset covers 104 industries across roughly 6,000 US firms with EV/Sales, price/sales and margins, updated January 2026, free to download, with global versions available. This is the standard reference for exactly this purpose and it is citable by name, which matters more than it sounds: "per Damodaran, January 2026" is a source a founder and an investor both recognise.
- The regression needs per-company data, which Damodaran does not provide. Building it means maintaining a peer list per sector and pulling EV, revenue and growth from any market data source. That is a modest quarterly job and we own the output outright.

**Row 1 can be cited but not queried.** Carta publishes stage medians and dilution bands in its quarterly releases. There is no third-party API to look up a comp. Citing the published figure with its vintage is legitimate and free. Querying their dataset is not available to us.

**Row 5 is the only one that needs money, and it is the row founders most want.** Two routes:

- **Companies House, free, UK only.** SH01 return of allotment gives shares issued and amount paid per share, which yields an implied post-money for a real UK private round. Public, redistributable, and nobody assembles it because it is tedious. That is why it is a moat.
- **Dealroom, PitchBook or CB Insights for everywhere else.** Before signing anything, check the **redistribution terms specifically**. Most of these licences let you use the data internally and restrict showing individual data points to your own end customers, which is precisely what row 5 does. That clause, not the subscription price, is the thing that decides whether this is viable, and it is worth asking the sales rep in writing before a trial.

**Never scrape a vendor.** It breaches terms, and for a business whose entire product is credibility it is an unrecoverable own goal.

**So: do we build our own database?** Partly, and deliberately. Own the listed peer sets and the derived multiples, because they are cheap, public and defensible. Own the discount stack and the sector judgement, because that is the actual product. Own the reviewer corrections, because they compound. Licence private round data when the free check is converting well enough to justify a per-lookup cost. Cite aggregate benchmarks and never pretend to query them.

## 7. Build order

1. **Numeric intake, tier 2 on the result screen.** Five fields. Nothing else works without it. Half a day.
2. **Damodaran sector table into `data/`.** Gives row 3 immediately, size and private discounts as stated parameters set by the reviewers. One day plus a data session.
3. **Peer sets and the regression for the top four sectors.** Gives row 4, the anchor. Two to three days including the refresh script.
4. **Football field front end**, per the earlier doc: rows live, locked rows redacted, sources on hover and tap.
5. **Companies House ingestion** for row 5 in the UK. Separate project, scoped after the above are live.

Rows 1 and 2 already work with what we have, so step 4 could come first if you want something on screen sooner. I would still do the intake first, because a football field built on bands will look precise and be wrong, which is the worst combination available.
