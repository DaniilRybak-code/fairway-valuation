# What changed, and why

21 August 2026.

## The indicative range is gone

There were two of them. `computeResult()` in `app.js` built one from a chain of
coefficients: a stage base, a revenue bump on a hand-drawn curve, then multipliers
for growth, recurring share, gross margin and profitability, then a 0.85 to 1.55
spread. `/api/reveal` built a second one from a different anchor and overwrote the
first. Neither was reconciled with the other, and neither was derived from the
football field the founder was looking at.

Every coefficient was chosen by us and sourced from nothing. Both are deleted
rather than improved. The valuation is now implied by the rows of the field, and
the reviewer gives the read on where inside them a company sits.

## The illiquidity discount is gone

It existed to bridge a listed industry aggregate to a private company. That is
work a properly selected peer set should do, and the discount was a number we
invented. The Damodaran aggregate stays on the page as market context and is
never converted into a valuation of anybody.

## Growth is asked year on year

A trailing rate is a fact. A spot monthly rate is a founder's estimate, and
compounding one for twelve months produced 435% annual growth at the top of the
old slider.

Forward growth is the trailing rate multiplied by a growth persistence factor of
0.75: the median Point Nine measured across 29 early-stage SaaS companies and 96
data pairs, against 89% for public SaaS and Scale Venture Partners' 80 to 85%.
Persistence is a year-over-year measure, so it is applied to a year-over-year
figure. Applying it to a spot monthly rate, which the old build effectively did,
was a different claim than the one the research supports.

## NTM revenue and month-twelve ARR are different numbers

NTM revenue is the **sum of the next twelve months**. Consensus forward revenue
is a sum, so ours has to be a sum. Month-twelve ARR is an **exit run-rate** and
is larger: at 8% monthly growth the two differ by about 47%, at 15% by 93%.

Both appear on the result screen and both get a row in the field, at the same
multiple range, because the multiple is the evidence and the denominator is the
choice. The month-twelve row values the company at a future date and says so in
its label, not in a footnote.

## The field

Public: last round as a diamond, NTM revenue multiple, ARR multiple at month
twelve, growth-adjusted, DCF, NTM EBITDA. Private: comparable precedents,
growth-adjusted precedents. Plus two market-context rows that are explicitly not
applied to the company.

The private row carries a **multiple, never a valuation**. Another company's
post-money tells a founder nothing without the revenue underneath it.

DCF is locked with the business plan as its unlock, and its cost of capital is
built from the same peer set's beta, so it is consistent with the rest of the
page rather than a parameter from nowhere.

The concluding "Indicative range" row and `ffTotalMetrics` are gone. That row was
the headline range in another costume.

## Still to come

The two revenue rows show the metric they will price and say plainly that the
multiple is being wired to live comparable-company data. They do not pretend to
be a paywall. See `Fairway_engine_diagnosis_and_comps_plan.md` in the project for
the peer engine and the private rounds plan.
