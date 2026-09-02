# The 2 September rulings, applied
What you asked for, what changed, and the one thing you should look at before this goes further.

## 1. Anthropic: yes, there are later rounds, and three are now in

You were right that May 2023 was too early. Anthropic had essentially no revenue then. Anthropic's
own newsroom, in September 2025, put run-rate revenue at $87m at the START of 2024, and Contrary
Research citing Anthropic has them at zero in January 2023. There was nothing to divide by, and
both databases were dividing by a figure that had not happened yet.

**The May-2023 row is now record-only.** The round stays, the 46.0x is gone.

**Three later rounds inserted, all from anthropic.com/news, all with a run-rate Anthropic itself
disclosed at or before the pricing date.**

| Round | Date | Raised | Post-money | Run-rate | As of | Multiple | In medians |
|---|---|---|---|---|---|---|---|
| Series F | 2 Sep 2025 | $13bn | $183bn | over $5bn | August 2025 | 36.6x ceiling | no |
| Series G | 12 Feb 2026 | $30bn | $380bn | $14bn | same day | 27.1x point | **yes** |
| Series H | 28 May 2026 | $65bn | $965bn | over $47bn | May 2026 | 20.5x ceiling | no |

**Series F is the cleanest row of the three, and probably the cleanest Anthropic row we will ever
have.** The valuation and the denominator come from the same Anthropic document, and the
denominator carries an "as of" date a month BEFORE the pricing rather than after it: "By August
2025, just eight months later, our run-rate revenue reached over $5 billion." Series G and H are
also honest but their run-rates are disclosed the same day as the raise, which is simultaneous
rather than prior.

Only Series G feeds a median, because it is the only one stated as a point rather than as
"over" or "crossed". The other two are ceilings.

Two things I deliberately kept out. Secondary shares reportedly changing hands around $1.2tn in
July 2026 is resale chatter, not a company-priced round. And press reports in January 2026 of a
round at a $350bn pre-money were the negotiation, not the close; the close was $380bn post-money
and only the close is used.

Anthropic's March-2025 row keeps its $1bn but its source moved off LinkedIn News onto TechCrunch
of the day of the round, which carries the same figure.

## 2. Gorillas and Perplexity

**Gorillas: our numbers were already right, so nothing moved.** What was missing was the sources,
and I have added them. CNBC of 19 October 2021 carries both: "Gorillas is now valued at $3.1
billion following the cash injection" and "Gorillas says it now has a run rate of $300 million".
TechCrunch the same day carries the other number, "It's now being valued at $2.1 billion,
pre-money". Pre-money plus the close-to-$1bn raise reconciles to the $3.1bn post, so the two
reports agree rather than conflict. Ours stays at 10.3x, a ceiling because Gorillas said MORE
than $300m.

**Something structural turned up while doing this.** Gorillas was the one row of the nineteen with
no revenue source, and the reason was not the row. `data/private-rounds-consumer.csv` had no
`revenue_source_url` column at all, so not one of its 51 rows could record where its revenue came
from. I have added the column. It is populated on Gorillas and empty on the other 50, which now go
on the sourcing list.

**Perplexity January 2024 is now priced as the range it actually is.** TechCrunch on the day of
the round: "Sources familiar with the matter tell TechCrunch Perplexity's annual recurring revenue
is between $5 million and $10 million at the moment." $520m over $10m is 52.0x and over $5m is
104.0x. The row now carries 52.0x to 104.0x with the headline at the conservative end and a "at
least" bound. It was unpriced before, on a note that said "sources conflict"; the sources do not
conflict, they gave a range.

## 3. Wolt, and the standing rule

Applied as you ruled it. **All-stock acquisitions price at announcement.**

Wolt moves from DoorDash's audited $2,838m to the announced $8,100m. The denominator does not
move: Wolt's own release of 25 January 2021 gives revenue in dollars, "tripling our revenue to a
preliminary $345 million", so there is no currency mixing. **8.2x becomes 23.5x.** The audited
figure and the reason for the gap stay in the row note as the record.

I checked whether a fresher denominator exists, because FY2020 revenue against a November 2021
price is eleven months stale for a company that was tripling. It does not. DoorDash's merger
filing carries no Wolt financials and no FY2021 figure was public at announcement. So $345m is
genuinely the number investors had at pricing, which is what our rule asks for.

Glovo has the same exposure and your ruling unblocks the valuation side of it: the announced
EUR 2.3bn is a 100% fully-diluted figure and is now usable. It stays record-only for a different
reason, which is that its denominator is unsourced. Your file carries roughly EUR 360m of 2020
revenue giving 6.39x, and 2,300 over 360 reproduces CB Insights' published 6.4x exactly, which is
why our own note flagged it as read off a comps blog. **One source for Glovo's 2020 revenue turns
that row on.**

## 4. The thing to look at before this goes further

The Wolt ruling moves more than one row. Wolt was the LOW anchor of the delivery and logistics
peer sets at 8.2x. At 23.5x it is now near the top, and four fixtures moved:

| Fixture | Before | After |
|---|---|---|
| hived | private mid 10.3x | **23.5x** |
| oda | private mid 10.3x | **23.5x** |
| byrd | private high 10.3x | **23.5x** |
| 99minutos | private mid 8.94x, high 10.3x | **10.3x and 23.5x** |

That is your ruling working correctly, and I think the ruling is right. But it means a founder in
courier or rapid delivery now sees a range roughly twice as high as yesterday, off one row. The
delivery private set is thin enough that one comparable can do that. Worth knowing before the
pilot, and it is an argument for sourcing Glovo, Flink and the other delivery names that currently
carry no denominator.

Five AI fixtures also changed, but only in the NAMES they show: Anthropic May-26 now appears as a
peer where Anysphere used to. No range moved, because that row is out of medians. Separately worth
your eye: a $965bn frontier lab showing as a named comparable to a seed-stage scraping tool is
defensible on business nature and indefensible on common sense. Our rule says size never selects
or excludes, so the engine is doing what it was told. You may want a display rule rather than a
selection rule.

## What changed in the files

`data/private-rounds.csv` 112 to 115 rows, `data/private-rounds-consumer.csv` 55 to 56 columns.
Applied by `tools/apply_daniil_rulings_2sep.py`, `tools/apply_daniil_rulings_2sep_consumer.py` and
`tools/apply_glovo_note_2sep.py`, each change carrying its reason in `notes`. Golden deliberately
rebaselined, 11 of 43 moved, now 0 of 43. The basis and period audit is unchanged at 42 rows
flagged and 69 agreeing with their own words.

## Sources

Anthropic Series F https://www.anthropic.com/news/anthropic-raises-series-f-at-usd183b-post-money-valuation ·
Series G https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation ·
Series H https://www.anthropic.com/news/series-h ·
Anthropic Series E https://www.anthropic.com/news/anthropic-raises-series-e-at-usd61-5b-post-money-valuation and https://techcrunch.com/2025/03/03/anthropic-raises-3-5b-to-fuel-its-ai-ambitions/ ·
DoorDash announcement https://ir.doordash.com/news/news-details/2021/DoorDash-Joins-Forces-with-Wolt/default.aspx ·
DoorDash 10-Q https://www.sec.gov/Archives/edgar/data/1792789/000162828022021372/dash-20220630.htm ·
Wolt revenue https://press.wolt.com/en-WW/196005-wolt-closes-530-million-financing-round-to-continue-expanding-beyond-the-restaurant/ ·
Gorillas https://www.cnbc.com/2021/10/19/delivery-hero-leads-1-billion-investment-in-grocery-start-up-gorillas.html and https://techcrunch.com/2021/10/19/gorillas-grabs-close-to-1bn-series-c-values-the-on-demand-grocery-delivery-biz-at-2-1bn/ ·
Perplexity https://techcrunch.com/2024/01/04/ai-powered-search-engine-perplexity-ai-now-valued-at-520m-raises-70m/
