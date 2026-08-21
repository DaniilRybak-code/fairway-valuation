# The valuation engine: rows, inputs, and where the data comes from

**Status:** plan, v3. 20 Aug 2026. Revised after the competitive scan. Supersedes the row set in `football-field-plan.md`; the front-end and blur design in that doc still stand, with one change noted in section 4.

## 1. Where the earlier plan was wrong

**Stage benchmark is not a valuation method.** Correct. Two companies at seed in the same sector can be worth 3x different amounts. What it *is* is the analogue of the L1Y trading range at the top of the Juno page: market context that frames the field without driving it. Keep the row, label it context, put it first, and never let it move the number.

**Comparable rounds must be filtered on revenue scale.** Correct, and it is the whole difficulty. A comp set of "seed fintech" is useless. A comp set of "seed fintech, $80k to $150k MRR, Europe, last 12 months" is the product. Any comp query needs sector, stage, revenue band, geography and vintage, and if fewer than about five transactions survive that filter we do not draw the row.

**Growth-adjusted range.** Right, and it is the anchor row rather than an extra one.

**Two band answers cannot drive a multiple.** Correct, and this was the binding constraint on everything else. Now fixed: see section 3.

## 2. Round size: kept, but moved behind the paywall

Not a valuation methodology, agreed. It belongs in the field anyway, for the same reason the LBO row belongs in Juno's.

The LBO row is an ability-to-pay analysis: what can this buyer pay and still clear a 17.5% to 22.5% IRR. It is not a view on intrinsic value, it is a view on what price the transaction structure permits. At seed there is an exact analogue, and it binds harder than at large cap: **most seed leads have ownership targets**, typically 10% to 20%. A founder raising $3M from a fund that must own 15% is implying a $20M post-money, whatever anyone thinks the company is worth. Price gets set by the intersection of cheque size and ownership target far more often than by any multiple.

So it stays, renamed **Ownership-target implied valuation**, labelled constraint-driven exactly as the LBO row is. It is frequently the row that contradicts the founder's ask, which makes it the most commercially useful thing on the page, which in turn is why it now sits in the locked set rather than the free one.

## 3. The inputs problem, now solved

We used to collect a revenue band, a growth band and a profitability band. You cannot apply a multiple to a band: `$50k-$150k/mo` spans a 3x range in ARR before any multiple is applied, which alone made the output wider than any method's dispersion.

The quiz now collects exact figures:

| Input | Needed for | Status |
|---|---|---|
| Monthly revenue, exact, in the founder's own currency | A1, A2, B1 | **Collected** |
| Reporting currency | Display, and the US anchor caveat | **Inferred from the edge, not asked** |
| Recurring share of revenue | A1, A2 | **Collected**, and only asked where the revenue model makes it meaningful |
| Revenue model | Which multiple set applies at all | **Collected** |
| Revenue growth, exact, per month | A2 | **Collected** |
| Gross margin | A1, A2 | **Collected**, optional, on the result screen |
| Net revenue retention | A2 | Not yet. Next field to add to the result screen. |
| Net burn and runway months | Concerns, and the deadline discount | Band only |
| Country | A1, B1 | Inferred from the edge header |
| Last round: date, amount, pre or cap | All rows | **Collected**, optional, on the result screen |

Both revenue and growth keep a band fallback for anyone who would rather not give a figure, so nothing in the quiz is mandatory. A founder who takes the fallback is told what the band costs them in precision rather than being quietly treated as pre-revenue.

Everything optional lives on the **result screen**, not in the quiz, and every field says on screen that it is optional and that it narrows the range. Precision is bought with information rather than money, which is the direct answer to the mandatory-form problem every competitor has. It also qualifies hard, because founders who type real numbers are actually raising, and it produces exactly what the reviewer needs before the 48 hour email. Adding gross margin and a last round currently takes the range about 30% tighter relative to its mid-point, and the page says by how much.

## 4. Two blocks, two convergence lines

Revised after the competitive review. The finding that drives it: every competitor produces a single range with nothing behind it, and the two that attempt an explanation do it generically. The differentiator is not the number, it is that each row names its method, shows its reference metric, and reveals the source on hover.

The field splits into two blocks, and the gap between them is the insight nobody else can show.

**Block A, public market.** Always computable, any geography, no vendor licence.

| Row | Visible free? |
|---|---|
| **A1. Revenue multiple.** ARR times sector EV/Revenue, size and illiquidity discounts stated separately | Yes |
| **A2. Growth adjusted.** Fitted EV/Revenue at this company's growth rate, from a listed peer regression | Yes |

Both rows are **revenue based, never EBITDA**. Our companies mostly do not have positive EBITDA, and a regression on a metric half the peer set lacks is a decoration rather than a method. A2 is the anchor: A1 says what the market pays for revenue in this sector, A2 says what it pays for revenue *growing at this rate*, and the gap between them is the argument the founder will have in the room. "The sector trades at 4.1x, but at our growth rate the fitted multiple is 7.8x, and here is the regression."

**Block B, private market.** Thin outside the US and UK, and this is where the money goes.

| Row | Visible free? |
|---|---|
| **B1. Comparable private rounds.** One cut, filtered on sector, stage, revenue band, geography, vintage | **Yes, one row** |
| B2. Further private round cuts, on different filters | Locked |
| B3. **Ownership-target implied.** Round size divided by typical lead ownership target | Locked |
| B4. **Reviewer band.** The banker's view after reading everything | Locked |

Block B is not entirely blurred. One private-round cut is open, because it is the row founders most want and the one competitors cannot produce, so giving one away is what makes the rest credible.

**The two convergence lines are the product.** Block B above block A means the private market is paying a premium to fundamentals, so raise now. Block B below block A means you are being discounted relative to what your own numbers support, and here is what closes it. Either way the founder leaves with a sentence they can use in a room, and no calculator on the internet can produce it.

**Sequencing caveat.** B1 needs the private data pipeline. Until Companies House ingestion exists it renders locked by necessity, not by design, and the copy should say which of the two it is. A locked row that is locked because we do not have the data yet must never be presented as a paywall.

## 5. Row A2 in detail, because it is the one that makes this credible

1. Maintain a peer set per sector, roughly 20 to 40 listed names.
2. For each: enterprise value, LTM revenue, revenue growth, gross margin.
3. Regress EV/Revenue on revenue growth. Store slope, intercept, R squared, n, and date.
4. Read the fitted multiple at the founder's growth rate.
5. Apply the private-company discount stack, each component stated separately: size, illiquidity, stage.
6. Multiply by ARR. That is the row.

Tooltip: *"Listed B2B software, 34 names, EV/Revenue regressed on revenue growth, R squared 0.61, as at 31 Jul 2026. Fitted multiple at 60% growth: 8.4x. Less 45% size and illiquidity discount: 4.6x. Applied to $1.2M ARR."*

That is a sentence a founder can take to an investor. Every element is either public data or a stated judgement.

The discount stack is where the reviewers earn their fee. It is the parameter no competitor can copy, it should be per sector and per size band, and it must always be shown rather than buried. An unexplained 45% haircut is the fastest way to lose a numerate founder.

## 6. The data question, answered directly

**Block A needs no vendor for the fundamentals.**

- Sector EV/Revenue: Damodaran's NYU dataset covers 104 industries across roughly 6,000 US firms with EV/Sales, price/sales and margins, updated January 2026, free, with global versions. Citable by name, which matters: "per Damodaran, January 2026" is a source both a founder and an investor recognise.
- Per-company fundamentals for the regression: **SEC EDGAR**. The company facts and frames APIs are free, need no key, and return every XBRL fact a US filer reports, including revenue and cost of revenue. Public domain, no licence, no redistribution clause. The only requirements are a declared User-Agent with a contact address and staying under 10 requests per second, which for a quarterly refresh of 40 tickers is not a constraint.

### Why we would pay anything at all: the share price question

Fair challenge, and you are right that nothing here needs to be live. Enterprise value needs a price, and a price from last Friday is fine for a quarterly regression. Three routes:

1. **Do not hit an API at all.** The regression is refreshed by a reviewer once a quarter. They can pull the peer set from any terminal or screen they already have and paste it into `data/`. Zero cost, zero licence exposure, and roughly an hour of work per sector per quarter. This is the honest default and it is what I would ship first.
2. **Yahoo Finance or Google.** Neither is licensable for this. Yahoo has no public API; the endpoints everyone uses are undocumented, break without notice, and their terms do not permit redistributing the data in a commercial product. Google Finance has had no API since 2012, and `GOOGLEFINANCE()` only exists inside a Google Sheet with its own display restrictions. Both are fine for you to look something up personally. Neither survives the question "where did this number come from" from a founder's investor, which is the only question our product exists to answer. I would not build on either.
3. **Pay the $29.** Polygon.io is now Massive. Its free tier is 5 calls a minute, end of day only, financials excluded, and explicitly individual use, so it is not usable for us. The Starter tier at roughly $29 a month gives unlimited calls and delayed data, which is more than enough. If we ever want it automated, that is the price, and it is a rounding error.

**The licence point that actually matters, and it applies to all three.** We publish a *derived statistic*: a fitted multiple, a median, a regression coefficient, with the peer set named and the method stated. We do not publish a table of each peer's individual multiple. That distinction is what keeps us clear of redistribution restrictions, and it happens to be exactly how a banker's page presents it anyway. Keep it that way even when the data is free.

**FX.** Reporting currency is inferred from the edge rather than asked, and all the maths runs in the founder's own currency, because a multiple is a ratio and does not need converting. The only cross-currency comparison is against the US market anchors, and that gets stated in the copy rather than silently converted at a rate nobody can check. If the reviewers later want real conversion, it needs a sourced rate with a date, from the ECB daily reference rates or the Fed H.10, both free and both public.

**Block B, private rounds, is the only part that needs money.**

- **Companies House, free, UK only.** SH01 return of allotment gives shares issued and amount paid per share, which yields an implied post-money for a real UK private round. Public, redistributable, and nobody assembles it because it is tedious. That is why it is a moat.
- **Dealroom, PitchBook or CB Insights elsewhere.** Before signing, check the **redistribution terms specifically**. Most of these licences permit internal use and restrict showing individual data points to your own end customers, which is precisely what B1 does. That clause, not the price, decides whether it is viable. Get it in writing before a trial.

**Never scrape a vendor.** For a business whose entire product is credibility it is an unrecoverable own goal.

**So: do we build our own database?** Partly, and deliberately. Own the listed peer sets and the derived multiples, because they are free from EDGAR and Damodaran and defensible. Own the discount stack and the sector judgement, because that is the actual product. Own the reviewer corrections, because they compound. Licence private round data only when the free check converts well enough to justify a per-lookup cost. Cite aggregate benchmarks such as Carta and never pretend to query them.

## 7. Content: what moves valuation must be tailored

The competitive scan found two sites that explain valuation drivers and both do it generically, which is why neither is persuasive. Our version is generated per respondent from sector, stage, size, growth, recurring share and revenue model, and every driver either quotes the founder's own number back or comes from a sector-specific table. Where a driver cannot be tailored, it does not render.

That content lives in `drivers.js`, deliberately separated from the funnel mechanics, because it is the file the reviewers will maintain.

Rules for this section:

- No paragraph that would read identically for two different founders.
- The sector line names the metric that sector is actually indexed on, plus what pays and what cuts. Net revenue retention for B2B software, gross margin after inference cost for AI, net revenue rather than GMV for marketplaces, loss ratio for insurtech, and so on.
- Biotech and medtech get told plainly that revenue multiples do not apply to them, rather than being shown one.
- Under twelve months of runway overrides everything else and says so.
- It stays open, not blurred. This section is what buys the credibility that makes the locked rows worth paying for.

## 8. Build order

1. **Exact numeric intake.** Done. Revenue, recurring share, revenue model, growth, gross margin and last round are collected, with currency inferred rather than asked, and all of it flows to the lead sheet and the reveal engine.
2. **Damodaran sector table into `data/`.** Gives row A1. One day plus a data session with the reviewers to set the discount stack.
3. **Peer sets and the regression** for the top four sectors, from EDGAR plus a quarterly reviewer price pull. Gives row A2, the anchor.
4. **Football field front end.** Block A live with sources on hover and tap, block B redacted at a decorative position rather than its true one, and the two convergence lines.
5. **Companies House ingestion** for B1 in the UK. Separate project.
