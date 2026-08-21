# Growth, and how MRR becomes a forward revenue figure

## The question changed

It used to ask for month-on-month growth, averaged over three months. That is a
founder's estimate of an instantaneous rate, and compounding it for twelve months
is brutal: 8% a month is 152% a year, 10% is 214%, 15% is 435%. Almost nobody
holds that for a full year, so projecting at the raw rate systematically
overstated forward revenue and therefore any multiple applied to it.

It now asks for growth over the last twelve months. A trailing rate is a fact.

## Growth persistence

Persistence is the observed ratio of next year's growth rate to this year's. A
company that grew 100% then 75% has a persistence of 0.75.

Point Nine measured it across two samples: a median of 89% for public SaaS (75
companies, 218 data pairs, regression slope 0.775) and a median of **75% for
early-stage SaaS** (29 companies, 96 data pairs). Scale Venture Partners put it
at 80 to 85%. Fairway's users are the early-stage sample, so `GROWTH_PERSISTENCE`
is 0.75.

The important detail: persistence is a **year-over-year** measure. It says next
year's growth is 75% of this year's. It does not say this year's growth is 75% of
what a spot monthly rate implies. Those are different claims, and applying the
constant to a monthly rate, which an earlier build effectively did, was not
supported by the research. Asking year on year fixes it at the source.

## The two forward figures

Given MRR now and forward annual growth `f`:

- **NTM revenue** is the sum of the next twelve months. Build the twelve monthly
  figures at `(1+f)^(1/12) - 1` and add them up. Consensus forward revenue is a
  sum, so ours has to be a sum for the multiple to be comparable.
- **Month-twelve ARR** is `MRR x (1+f) x 12`. An exit run-rate.

They are not close. At 8% monthly growth they differ by about 47%; at 15% by 93%.
Using one where the other belongs moves a valuation by more than half.

Both appear on the result screen and both get a row in the football field, at the
same multiple range, because the multiple is the evidence and the denominator is
the choice. The month-twelve row values the company at a future date and says so
in its label rather than in a footnote. For a company with a high recurring share
the month-twelve basis is the more defensible of the two, and the copy says why.

## Fallbacks

A founder who will not give a figure can pick a band. `GROWTH_BAND_PROXY` maps
those to 0%, 50% and 150%, and the persistence haircut still applies. Those
reveals should be treated as lower confidence by the reviewer.
