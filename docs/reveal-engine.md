# Making the reveal real

**Status:** the range currently shown on screen is a placeholder. This is the plan to replace it.
**Owner decision needed:** primary geography, and whether we seed v1 from published benchmarks or from our own deal knowledge.

---

## 1. What is wrong today

The number comes from this:

```
base = (stageBase + revenueBump) x growthMult x profitMult
low  = base x 0.85     high = base x 1.55
```

It is deterministic, so it never contradicts itself on reload. That was the first fix. But every coefficient in it was chosen by hand to look plausible, and none of them is traceable to a real round. Two consequences:

1. **It cannot be defended.** If a founder forwards the range to anyone who prices companies, the first question is "based on what?" and there is no answer. That kills the goodwill the free check exists to create.
2. **It cannot be improved.** There is nothing to calibrate against, so we would never learn whether the ranges were any good.

The output also has to survive being read by someone whose day job is pricing. A number with no provenance in front of that audience is worse than no number.

## 2. The reframe that makes this tractable

Do not try to make the instant on-screen number impressive. Make it **honest, narrow in claim, and explainable**, then move the moment of goodwill to the 24 hour reviewed email.

- **On screen:** a first-pass range, with one sentence stating exactly what it is derived from and how many comparable rounds sit behind it. Explicitly labelled unreviewed.
- **In the email, within 24 hours:** a human confirms or corrects it with one paragraph of reasoning specific to the company. That is the product. That is what makes someone pay $750.

This is also the only version that is operationally honest at low volume. A banker cannot personally originate a hundred ranges a day, but they can review a handful, and the review is what we are actually selling.

## 3. Target design for the range

### 3.1 The comp table

A JSON file in the repo, refreshed quarterly, keyed by `stage x sector x geography`:

```json
{
  "vintage": "2026-Q1",
  "geo": "UK-EU",
  "rows": [
    { "stage": "Seed", "sector": "Fintech", "n": 84,
      "pre_p25": 4.1, "pre_p50": 6.0, "pre_p75": 9.2,
      "arr_multiple_p50": 14.5 }
  ]
}
```

`n` matters as much as the percentiles: it is what we put on screen to justify the number, and it tells us when a cell is too thin to quote.

### 3.2 Two methods, blended

- **Stage benchmark.** Position the company inside the p25 to p75 band for its cell.
- **Revenue multiple.** Where monthly revenue is above zero, annualise and apply the sector ARR multiple.

Where both exist, blend, weighting revenue more heavily as revenue grows. Pre-revenue companies get the stage benchmark alone, which is the honest answer.

### 3.3 Adjustments, bounded

Growth, profitability and runway shift the position inside the band. Every adjustment is capped, and the total adjustment is capped at roughly plus or minus 20%, so no combination of answers can produce a number outside the observed distribution. Runway under 12 months is the one factor allowed to push below p25, because in practice it does.

### 3.4 Guard rails

- Never quote a cell with fewer than a set minimum of comparable rounds. Fall back to the sector-agnostic stage band and say so.
- Range width stays between about 1.4x and 2.2x low to high. Narrower is a false claim of precision, wider is useless.
- If the implied dilution falls outside roughly 8% to 40%, flag it in the copy rather than hiding it, because it usually means the raise and the range disagree and that is itself worth telling them.

### 3.5 The explainability line

This single sentence does more work than the number:

> Your range is the 25th to 75th percentile of 84 priced Seed rounds in Fintech across the UK and Europe in the four quarters to Q1 2026, adjusted up for growth above 15% a month and down for runway under twelve months.

Vintage and source get printed underneath. If we cannot write that sentence truthfully for a given founder, we should not show a number to that founder.

## 4. Where the data comes from

**v1, cheap and citable.** Published quarterly benchmarks: Carta's State of Private Markets for US medians by round, and Beauhurst or Dealroom for UK and European coverage. These are free to read, updated quarterly, and can be named on the page, which is itself part of the credibility. Coverage is coarse: strong by stage, weaker by sector, weakest at the sector-by-geography intersection.

**v1.5, our own edge.** The reviewing team has seen real rounds. Encoding that as a private overlay on the published table, cell by cell, is the thing no competitor can copy, and it costs nothing but an afternoon of arguing about numbers.

**v2, if volume justifies.** A licensed feed for real per-round data at the sector level.

Two things not to do: do not scrape a paid database, and do not quote a figure whose source we could not show to the founder who asks.

## 5. Everything on the reveal that is not the number

The range is one of four outputs, and the other three are easier to make genuinely personal.

- **Concerns.** Today these key off revenue, growth and profitability. Next: lead with the concerns the founder told us they have actually been hearing, then fill from the pattern set. Someone who typed "two funds said the market looks small outside the UK" should see that sentence reflected back before they see anything generic.
- **Investor list.** Today it filters on sector only. It should filter on sector **and** stage **and** cheque size against their raise band, so a founder raising $300k never sees a fund whose minimum is 1M. That is a data fix, not a modelling one, and it removes the most obvious way the list looks wrong.
- **The dilution maths.** Already computed from their own answers, already honest.
- **The reviewed email.** See below.

## 6. The operational spine

None of this matters if the 24 hour promise is not kept.

1. Lead lands in the spreadsheet (see `docs/lead-capture.md`).
2. The Apps Script emails an alert and **pre-drafts the reply in Gmail**, prefilled with the computed range, the concerns the founder reported, and marked blanks where judgement is required.
3. Reviewer edits the draft, changes the number if it is wrong, sends.
4. Reviewer sets `status` and `sent_at` in the sheet.

Editing a good draft takes a few minutes. Writing from a blank page takes twenty, which is how SLAs get missed. Every corrected range is also calibration data: when the reviewer moves a number, that is the signal the comp table was wrong for that cell, and after thirty of them we can tune it.

## 7. Sequence

| Step | Work | Effort |
|---|---|---|
| 1 | Lead capture into the sheet, alert plus draft email | done, needs deploying |
| 2 | Investor list filtered by stage and cheque size | small |
| 3 | Founder-stated concerns lead the concerns card | small |
| 4 | Comp table structure, guard rails, explainability line, wired to placeholder numbers | medium |
| 5 | Populate the table from published benchmarks, print vintage and source | medium, needs the geography decision |
| 6 | Private overlay from the team's own deal knowledge | a session with the reviewers |
| 7 | Calibration loop: log every reviewer correction, tune quarterly | ongoing |

Steps 1 to 4 can ship before any real data exists, because they are structure. Step 5 is the one that turns the reveal from plausible into defensible, and it is the one that needs a decision on primary geography first: a UK and Europe table and a US table are different pieces of work and the sector cells are populated by different sources.

## 8. Interim honesty

Until step 5 lands, the on-screen copy should say what the number actually is. Something like: *this is an indicative first pass from stage and sector patterns, not a comp-set output; the reviewed number arrives by email within 24 hours.* That costs a little drama on the result screen and buys the thing the business runs on.
