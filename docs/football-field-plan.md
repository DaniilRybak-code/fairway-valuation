# The reveal, rebuilt as a football field

**Status:** plan, not built. 20 Aug 2026.

The current reveal gives a single range and four reference points. The Juno page is better because it shows the *architecture* of the number: several independent lenses, each with the parameter it uses and the metric it is anchored to, converging on a band. A founder reading it understands where the number came from before they read the number.

We should copy the structure. We cannot copy the content, and being clear about why is the whole design problem.

## 1. Half of that page does not exist for a seed company

The Juno field runs on a public company in a live sale process. Row by row:

| Their row | Works for us? | Why |
|---|---|---|
| L1Y trading range | No | No share price. |
| Broker target prices | No | No analyst coverage of a company with $600k ARR. |
| Trading multiples vs listed peers | Partly | The multiples exist. Applying a listed multiple to a pre-Series-A private company needs an explicit size and illiquidity discount, stated out loud, or it is nonsense. |
| Regression, EBITDA multiple vs revenue CAGR | No | Needs a peer set with both metrics. Our companies mostly have neither positive EBITDA nor a credible CAGR. |
| DCF | No | A DCF on a company with eighteen months of history is an opinion with decimal places. Including it would be the single fastest way to lose a banker's respect. |
| LBO | No | Nobody is levering a seed company. |
| Precedent transactions | Partly | Private round valuations are mostly undisclosed. Real, but expensive and patchy. |

So the honest version is a football field with different rows, not a thinner copy of theirs. Anything we cannot source becomes a row we do not draw.

## 2. The rows that actually work, ranked by how defensible they are

**Row 1. Stage benchmark.** Median post-money for the stage, less the round. Reference metric: "Seed median post-money $24.0M, Q4 2025". Source: Carta, published, checkable. Fully computable today with zero new data.

**Row 2. Round size at market dilution.** A founder raising $3M who gives up the typical 15% to 25% is implying a $9M to $17M pre-money, whatever they think the company is worth. This is arithmetic on their own answer plus a published dilution band, it is exactly how an investor sanity-checks a number, and it frequently contradicts the founder's ask, which makes it the most useful row on the page. Computable today.

**Row 3. Revenue multiple.** ARR times a sector multiple derived from listed peers, with the discount stated. Needs a peer multiple table. Only draw it for companies with revenue.

**Row 4. Comparable rounds.** Actual recent rounds for similar companies at similar stage and sector. The row founders most want, and the hardest to source. This is the one that should stay locked longest.

**Row 5. Scorecard.** The standard angel method, weighted against the regional stage average. Honest because it is explicitly a method rather than a data point, and it is the row where the reviewer's judgement shows.

**Row 6. Reviewer band.** The banker's own view after reading everything. Not a method, the conclusion. This is the paid product and should never appear free.

## 3. What is free and what is locked

Rows 1 and 2 visible. Both are fully computed from verified data and the founder's own answers, so there is no hallucination surface at all on anything they can read. Rows 3 to 6 locked.

**The locked rows must not be drawn at their true positions.** If the bars are positionally accurate and only the labels are blurred, a founder with a ruler has the entire answer, and the convergence band, which is the actual deliverable, is visible for free. Locked rows render as a neutral redacted block at a fixed decorative position, with the method name legible and the numbers hidden. They see that four more lenses were run, and which lenses, and nothing else.

The vertical dashed convergence line, the crescendo of the Juno page, stays locked too. The free check gives you a range from two lenses. The report gives you six lenses and where they agree.

To stop the axis leaking the locked extremes, scale it from the visible rows plus 25% padding rather than from the full row set.

## 4. Hover, and the fact that half your traffic has no mouse

Each reference metric carries a source object: label, detail, vintage, optional URL. Desktop shows it on hover, mobile on tap, and the same element handles both. Implemented as a `<button>` with `aria-describedby` rather than a `title` attribute, so it works with a keyboard and a screen reader and does not wait 1.5 seconds to appear.

What the tooltip says depends on the row. For stage benchmark: the publication, the quarter and the figure. For comparable rounds, when we get there: the company, the round, the date, the source of the valuation, and whether it was disclosed or estimated. That last flag matters, because an estimated valuation presented as fact is the same credibility failure as an invented one.

## 5. The data ladder, which is the real project

The front end is a day. The data is the business.

**Tier 0, today, free.** Carta's published releases for stage medians and dilution bands, CB Insights for context. Manually refreshed each quarter into `data/comps.js`. Enough for rows 1 and 2, which is enough to ship.

**Tier 1, free and genuinely differentiating for UK companies.** Companies House filings are public and free through their API. An SH01 return of allotment of shares gives the number of shares issued and the amount paid per share, which with the confirmation statement gives you an implied post-money for a real UK private round. Nobody assembles this into a usable comp set because it is tedious. That is precisely why it is a moat, and it is the cheapest credible route to row 4 for the UK and to a real "recent rounds in your sector" claim. Estimated valuations must be labelled as derived from filings rather than disclosed.

**Tier 2, paid.** Dealroom, Crunchbase or PitchBook for round data outside the UK. Only worth it once the free check is converting, since it turns a zero marginal cost product into a per-lookup cost.

**Tier 3, proprietary and the only durable one.** The reviewer panel fills the sector multiple table, and every correction a banker makes in the 24 hour email gets logged in the leads sheet next to the inputs. After thirty or so corrections the table is being tuned against outcomes rather than against opinion. This is the asset that compounds, and it exists because a human is already in the loop for other reasons.

## 6. What changes in the engine

Today the model produces the range and the reference points. That is the wrong division of labour for this design.

**Visible rows are computed in code. The model writes language, never the numbers a founder can read.** Rows 1 and 2 come out of the deterministic engine from `data/comps.js` and the founder's answers. The model's job becomes: phrase the reference metric readably, choose which locked rows are worth naming for this company, write the basis sentence, and produce the concerns. Guard rails stay as they are, plus a new one: a row without a source object never renders, and a visible row that did not come from the computed set never renders at all.

Schema change on `/api/reveal`:

```
rows: [{
  method,              // "Stage benchmark"
  parameter,           // "Median post-money, less round"
  reference_metric,    // "Seed median post-money $24.0M"
  low, high,           // implied pre-money, GBP or USD
  source: { label, detail, vintage, url },
  locked: false,
  computed: true       // true means code produced the numbers
}]
```

## 7. Build order

**Phase 1, one day.** Football field component with rows 1 and 2 live, four redacted locked rows, tap and hover sources, mobile stacking. Ships on data we already have. This alone replaces the current reveal and is a large step up.

**Phase 2, half a day plus a data session.** Sector multiple table filled by the reviewers, which lights up row 3 for revenue-stage companies and makes the range sector-aware for the first time.

**Phase 3, the real work.** Companies House ingestion into a comps table, giving row 4 for UK companies with sourced, filing-derived valuations. Scoped separately because it is a data pipeline, not a page.

**Phase 4, ongoing.** Reviewer corrections logged from the leads sheet, feeding back into the table.

## 8. The thing to hold onto

The reason this design works is not that it looks like a banker's page. It is that a founder can check row 1 in ninety seconds, find it correct, and therefore believe row 4 is worth paying for. Every row we cannot source honestly costs more credibility than it buys attention. Four solid rows beat seven, and two solid rows beat four fabricated ones, which is why phase 1 ships with two.
