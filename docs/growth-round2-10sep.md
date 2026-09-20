# Growth enrichment, round two, 10 September 2026

**Written by Opus on 10 September 2026 against origin `main` at `1e210b4`, which is Daniil's push
of the 9 September enrichment. Every number below reproduces from
`python3 tools/load_growth_round2_10sep.py` and from the raw file it reads,
`data/raw/2026-09-10_private-growth-round2.csv`.**

## What this pass was for

Three things. Daniil's three rulings of 10 September. The twenty-five rows the 9 September pass had
to close on direct page reads only, because its web-search allowance ran out mid-run. And three
questions he asked about the "flagged, not fixed" list.

## In one paragraph

Eleven more rounds now carry a year-on-year growth rate with the page read and the sentence quoted.
Seventeen still do not, and each carries a reason in plain words, two of which are held for a
ruling rather than for want of searching. Growth coverage on the private rounds goes from 170 rows
to 181. Only the three growth columns changed, on eleven rows: 320 rows in, 320 rows out, and the
diff was checked twice, once by the loader and once independently. Twenty checks pass, the gate is
124 of 142 before and after, and golden did not move (0 of 142), for the same reason as on
9 September: the test companies carry no growth rate, so growth does nothing until a founder
supplies one.

---

# Part one: the three questions

## 1. The thirty revenue numbers. What is the contradiction?

You are right, and the flag was badly named. **Growth does not depend on the currency** when both
figures are quoted in the same currency. Revolut's 190 per cent is 190 per cent whether you read it
in pounds or in dollars. Nothing on that list is a growth problem.

The list is about **the revenue figure itself, which is the denominator of the multiple**. It never
touched the growth work, which is why it was flagged and not fixed. There are two separate defects
on it and they got put under one heading, which is what made it unreadable.

**Defect one: the number is right in its own currency, but the column says dollars.** The row holds
636.0 and the column is `revenue_musd`, but the figure is £636m. The valuation is in dollars. So the
multiple is a dollar valuation divided by a pound figure being treated as dollars, and the revenue
is understated by the exchange rate, so the multiple is overstated by about the same. Rough scale,
using the year's average rate and for illustration only:

| row | figure held | what it actually is | multiple on the row | roughly, once converted |
|---|---|---|---|---|
| revolut-2021-07 | 636.0 | £636m | 51.9x | about 37.6x |
| starling-bank-2021-03 | 145.0 | £145m | 7.6x | about 5.5x |
| atombank-2023-11 | 76.0 | £76m, and it is net interest income, not gross revenue | 4.8x | about 3.9x |
| enpal-2023-01 | 400.0 | EUR400m | 5.5x | about 5.1x |
| doctolib-2022-03 | 181.3 | EUR181m | 32.0x | about 30.5x |

The fix is small and mechanical: these rows have `fx_ccy` and `fx_rate` columns and both are empty.
Fill them and convert. It is the basis audit's job, not this one's.

**Defect two: the figure contradicts its own source, or belongs to a different date or a different
length of period.** Deel, Mercury, Stripe, BlockFi, Devoted Health, Zepz, Klarna, Voodoo and the
rest. Same effect: the multiple is wrong, the growth is not.

**One real exception, and it is the one live case where currency does change growth.** If the two
figures being compared were each translated into dollars at a different year's exchange rate, then
the dollar growth rate and the local growth rate are genuinely different numbers. Nubank is that
case, and it is why Nubank is held for your ruling below.

## 2. BlockFi. Is this a mistake, and are there others?

**Yes, it is a mistake, and it is confirmed against BlockFi's own words.** BlockFi's press release of
11 March 2021, the day of the round, says:

> "Monthly revenue currently exceeds $50 million, and the company now boasts more than $15 billion in
> assets on its platform, with a 0% loss rate across its lending portfolio since inception."

TechCrunch of the same day says the same thing: "Bumped its monthly revenue to over $50 million, up
from $1.5 million a year prior." The row records that $50m as last-twelve-months gross revenue and
prices the round at 60x. Annualised it is over $600m and the multiple is about 5x.

**The growth figure on that row is fine.** It compares $50m monthly to $1.5m monthly, so both legs
are the same measure, and 3,233 per cent stands. Only the revenue level and the multiple are wrong.
This is the clean illustration of the point above: the same row has a broken denominator and a sound
growth rate.

**One caution before anyone "fixes" it by multiplying by twelve.** $600m is a run rate, not
last-twelve-months. Monthly revenue went from $1.5m to $50m across that year, so true LTM revenue
was far below $600m and nobody published it. The honest options are to relabel the row as a run rate
or to leave the denominator blank. Twelve times fifty is not an LTM figure.

**Are there others?** I swept all 249 priced rows in two ways. First, every row whose notes mention a
sub-annual period (monthly, quarterly, six-month, half-year, weekly, year-to-date). Second, every row
on a full-year period (LTM or FY) carrying a multiple above 15x, on the reasoning that a monthly
figure used as an annual one shows up as an impossible multiple, which is exactly how BlockFi
surfaced.

**One other case, and it is confirmed.** `devoted-health-2021-10`. MedCity News, October 2021:

> "Devoted Health generated $247.3 million in revenues during the first six months of 2021, a 128%
> jump over the same period in 2020."

Six months, recorded as LTM. Annualised, revenue is about $494.6m and the multiple falls from 51.4x
to roughly 25.5x. Again the growth is fine, because 128 per cent is first-half against first-half.
The same article also gives the valuation as $12.6bn where the row holds $12.7bn.

**No third case found.** Everything else the sweep raised was either a monthly *active user* count,
not revenue, or a run rate that had already been annualised correctly. Mercor is the clearest of
those: its $75m is explicitly "calculated by multiplying its latest monthly revenue by 12".

**What the sweep cannot do.** It can only catch what a row's notes record or what shows up as an
implausible multiple. A row whose notes say nothing and whose multiple looks ordinary would pass
through it. Catching those means re-reading every row's source, which is the basis audit. I would
call this a screen that found the two obvious cases, not proof there is no third.

## 3. Deel, Mercury, Turing and Stripe. What is the timing gap?

Your rule is that a few months is fine, because rounds are priced on expected revenue. That holds
for one of these four, breaks badly for another, and does not apply at all to the other two.

| row | round | figure the row uses | date the figure belongs to | gap | multiple on the row | multiple on the at-round figure |
|---|---|---|---|---|---|---|
| deel-2022-05 | May 2022 | $295m ARR | end December 2022, published 23 Jan 2023 | **7 months after** | 40.7x | about **120x** on the ~$100m Deel disclosed in April 2022 |
| mercury-2025-03 | March 2025 | $650m annualised | September 2025, published 5 Feb 2026 | **6 months after** | 5.4x | **7.0x** on the $500m Mercury published on the round date |
| turing-2025-03 | March 2025 | $167m ARR | Q3 2024, per Turing's own blog | **about 6 months before** | 13.2x | 7.3x on the $300m Turing announced on 28 Jan 2025 |
| stripe-2025-02 | February 2025 | $5.6bn net revenue | no traceable period at all | not measurable | 16.3x | unknown |

**Deel is the one that breaks the rule, and it breaks it because of growth.** A forward figure is
only harmless if revenue does not move much over the gap. Deel grew 417 per cent that year. Seven
months forward at that rate is nearly three times the revenue, so the multiple is understated by
about two thirds. TechCrunch, 23 January 2023: "Deel reached $295 million in annual recurring revenue
(ARR) by the end of 2022 ... That's up 417.5% from $57 million in ARR achieved at the end of 2021."
At the round itself, TechCrunch of 11 May 2022 said only that Deel "had crossed the $100 million ARR
threshold".

**So the tolerance cannot be a flat number of months. It has to scale with the growth rate.** The
thing that matters is gap times growth, which is roughly how far the revenue has drifted:

- six months at 40 per cent growth moves revenue about 18 per cent, which is tolerable
- seven months at 417 per cent growth moves it about 180 per cent, which is not

If you want a rule I can apply mechanically, I would suggest: accept a forward figure where the gap
times the growth rate implies less than about 15 per cent of drift, and otherwise use the at-round
figure. On today's file that keeps Mercury inside the line by a small margin and puts Deel well
outside it.

**Mercury is a six-month forward figure and is inside your rule, but only just.** It flatters the
multiple by 23 per cent. Mercury's own annual letter, published 5 February 2026, says "as of
September 2025, we hit $650M in annualized revenue". Mercury's Series D page restates the same
number as "$650M Annualized revenue, as of Q3 2025", which is most likely where it was lifted from,
because the Series D is a different round at a $5.2bn valuation. On the round date, 25 March 2025,
Mercury published "$500M in annual revenue in 2024".

**Turing is not the same problem and is arguably correct.** Its figure is six months *before* the
announcement, not after. Turing's own release says "The round was priced when the company reached
$167 million in annualized revenue run rate (ARR)", and TechCrunch corroborates it. So the row is
consistent with an at-pricing convention. What is worth knowing is that Turing had publicly
announced $300m of ARR on 28 January 2025, five weeks before the announcement, so the same round is
13.2x on one convention and 7.3x on the other. This is the clearest row in the file where "at
pricing" and "at announcement" give materially different answers, and the company published both.
Whichever you choose, it should be applied consistently across the file.

**Stripe is not a timing problem at all, and it is worse than one.** Stripe has never published a net
revenue figure, in any annual letter, in any year. All four letters were read in full. Every top-line
number in them is total payment volume: $817bn for 2022, $1 trillion for 2023, $1.4 trillion for
2024, $1.9 trillion for 2025. The three TechCrunch articles the rows cite carry no revenue figure
either. So neither $4.1bn nor $5.6bn can have come from the sources named against them, and the same
$5.6bn sits on both the February 2024 and February 2025 rounds with the same URL. Nor does
re-labelling it by a year repair it: The Information, via Axios in March 2025, puts 2024 revenue at
$5.1bn after 28 per cent growth, which implies 2023 was about $4.0bn. $5.6bn matches no year on
record. **The three Stripe rows need their denominators rebuilt from scratch or withdrawn.**

---

# Part two: the rulings, and what each one did

## Ruling 1. "Sacra accepted in the absence of a better source."

Applied to all five held-out rows. It changed one of them, and not in the way anyone expected.

| row | what happened |
|---|---|
| skims-2023-07 | **Now loaded at 50, and not on Sacra.** A better source exists: Retail Dive, 19 July 2023, the round week: "the brand is expected to reach net sales of $750 million in 2023, an increase from nearly $500 million last year." Business of Fashion says the same. Sacra was carrying the same two figures as an estimate. |
| suno-2025-11 | **Still not loaded.** Sacra's figure does not survive being read. Its table stamps the 404.4 per cent growth rate as 2025 and the $300m revenue as 2026, and its prose says $300m in February 2026 is "up 404% year-over-year from ~$227M at the end of 2025", which is 32 per cent, not 404. A number that disagrees with itself inside one sentence is not a source. |
| mercury-2025-03 | **Still not loaded.** Sacra's 96.5 per cent implies 2023 revenue of about $254m, and Mercury has never disclosed a 2023 revenue figure to anyone. The rate rests on a denominator that does not exist publicly. What Mercury did publish at the round is 40 per cent customer growth and 64 per cent transaction volume growth, neither of which is revenue. |
| betterup-2021-10 | **No change, and the existing 100 per cent floor is now better supported.** Sacra's 127 per cent rests on $125m of ARR at October 2021, which BetterUp's own October 2021 release contradicts: it says $100m of ARR, reached in July. The same Sacra page also calls it a "$339M Series E" when BetterUp's own release says $300m. A checkable error on the same page is fair grounds for discounting the estimate. |
| oura-2024-12 | **No change, and Sacra's 53 per cent is now contradicted outright.** It is no longer on the Sacra page at all, and Oura's own release of 22 September 2025 says "The company reported revenue over $500 million in 2024, more than double that of the prior year." The existing 100 per cent floor is right and 53 was wrong. |

**So the ruling was applied in full and the answer is: one row closes, and the Sacra precedent turned
out not to be the reason.** Where Sacra was the only thing available, the Sacra figure itself did not
hold up on inspection. That is worth knowing before the next pass leans on it.

**One thing to watch.** Every Sacra page fetched today carries 2026 figures, and two of the five
numbers the 9 September pass attributed to Sacra are no longer on the page. Sacra rewrites its pages
in place, with no version history and no "as of" date on the table rows, and its table year labels
routinely disagree with its own prose. It is a moving target, so a Sacra figure should always be
loaded with the sentence quoted, never with the URL alone.

## Ruling 2. "If there is no matching data on ARR, take revenue growth."

Applied. Two new rows are loaded on it: `sumup-2022-06` on the CFO's statement about revenue against
a row that prices on an ARR run rate, and `zopa-2021-10` on bank operating income, which is the
revenue line for a bank, against a row that also prices on a run rate.

The seventeen rows the 9 September pass loaded on the same reading stand, unchanged and unstruck.

**Two things this ruling does not settle, and I have not stretched it to cover them.** Your ruling is
about which *measure* to accept. It says nothing about a sentence that names no measure at all.
There were two such rows and now there are three. `jobandtalent-2021-12` and `mews-2026-01` were
loaded on the ordinary reading and stay loaded. `virta-health-2021-04` is new, and I did not load it,
because its wording points the wrong way. See the ruling list below.

## Ruling 3. "Rerun the growth bands."

**Done, and I have not applied the result, because the script's own test now says the result is not
usable.** This is the one place I have not simply carried out the instruction, and I want to be
explicit about it rather than let it pass silently.

Here is what the script prints after today's load:

```
n = 181 private rounds carrying a growth rate
KS D = 0.169 against 5% critical 0.101  ->  LOG-NORMAL REJECTED, do not use these boundaries
BOUNDARIES:  MATURE below 64%   GROWING 64% to 204%   HYPER above 204%
```

The script assumes growth rates follow a log-normal distribution and tests that assumption before
reporting. The test fails, and it fails worse than it did at 170 rows. The script itself then says,
in its own output, not to use the numbers it just produced.

**Why it fails, and it is not a mistake in the data.** Companies report growth in round numbers.
Twenty-two of the 181 rows sit at exactly 100 per cent, ten at exactly 200, and 103 of the 181 sit on
a value shared with at least one other row. That is 57 per cent of the file stacked on a handful of
values. No smooth distribution fits a set that looks like that, and adding more rows makes it worse,
not better, because most new rows land on the same round numbers.

**Your four options, with the cost of each in rows that change band:**

| option | boundaries | MATURE / GROWING / HYPER | rows that change band |
|---|---|---|---|
| leave the code as it is | 77 / 206 | 77 / 69 / 35 | 0 |
| take the refit output anyway | 64 / 204 | 61 / 85 / 35 | 16 |
| equal thirds, straight from the data | 62 / 134 | 59 / 62 / 60 | 43 |
| the 31/38/31 split the script intends, straight from the data | 61 / 160 | 56 / 69 / 56 | 42 |

The last two need no distribution assumption at all. They just cut the sorted list at the right
places, which is what the script was trying to approximate. They also change about a quarter of the
file, and they push a lot of rows into HYPER, because the file's real distribution has a long tail
that the log-normal model was smoothing away.

**My reading, for what it is worth.** The refit output of 64 / 204 is barely different from the 77 /
206 in the code, moves 16 rows, and rests on a model the script says is rejected. It is not worth a
change. If you want the bands to reflect the file, the honest version is a percentile cut with no
distribution behind it, and that is a bigger decision than an enrichment. Either way, the table in
the 9 September work order that says 65 and 162 is still wrong and should be deleted, because it
matches neither the code nor any refit.

**Nothing was changed in `selector/match_reference.py`. Bands on all 181 rows are still 77 and 206.**

---

# Part three: the eleven rows loaded

Bands are recomputed by the code, never judged. The full URL, the verbatim sentence, the arithmetic
and every figure seen but not used are in the raw file.

| round | growth % | band | basis | floor | where it came from |
|---|---|---|---|---|---|
| remote-2022-04 | 1200 | HYPER | DISCLOSED | yes | globenewswire.com (2022-04), the round release itself |
| zopa-2021-10 | 186 | GROWING | THIRD_PARTY_DATED | | alternativecreditinvestor.com (2022-07), off the Companies House accounts |
| wefox-2021-05 | 100 | GROWING | DISCLOSED | | businesswire.com (2021-05), the round release itself |
| quince-2026-03 | 100 | GROWING | DISCLOSED | yes | prnewswire.com (2026-03), the round release itself |
| roblox-2021-01 | 82 | GROWING | DISCLOSED | | sec.gov S-1/A Amendment No. 4 (2021-02) |
| wiz-2024-05 | 75 | MATURE | DERIVED | | cnbc.com (2023-05) and techcrunch.com (2024-10) |
| plaid-2021-04 | 70 | MATURE | DERIVED | | justice.gov DOJ complaint (2020-11) and forbes.com (2021-04) |
| stockx-2021-04 | 67 | MATURE | DERIVED | yes | prnewswire.com (2021-04) and frontofficesports.com (2021-02) |
| sumup-2022-06 | 60 | MATURE | STATED | | techcrunch.com (2022-06), the CFO in the round interview |
| skims-2023-07 | 50 | MATURE | THIRD_PARTY_DATED | | retaildive.com (2023-07), the round week |
| n26-2021-10 | 22 | MATURE | DISCLOSED | | n26.com (2022-02), the FY2020 results release |

Split: DISCLOSED 5, DERIVED 3, THIRD_PARTY_DATED 2, STATED 1. Bands: MATURE 6, GROWING 4, HYPER 1.
Four are floors.

**Three of these deserve a sentence of their own.**

`remote-2022-04` at 1,200 per cent is the largest figure in the file and it comes from the round
announcement: "more than 13-fold growth in annual recurring revenue in the past year". It is the
exact measure the row prices on, in the company's own release, for the twelve months to the round.
The alternative reading of "13-fold growth" as an increase *of* thirteen times, ending at fourteen,
is less standard. Either reading is HYPER.

`plaid-2021-04` is the weakest of the eleven and is the one to strike first if you want one gone. Its
2019 leg is a full financial year from the Department of Justice's antitrust complaint against Visa,
paragraph 21: "Plaid's revenues have been growing rapidly and were almost $100 million in 2019." Its
2020 leg is a December run rate annualised, which is the $170m the row already prices on. Those are
not the same kind of period, and comparing a year-end run rate to a prior full year flatters the
rate. Two biases run in opposite directions and neither is quantified, so I did not mark it a floor.

`n26-2021-10` is loaded at 22 per cent but the row's revenue figure does not match the period the
growth belongs to. The row holds $200m for FY2020. N26's own FY2020 gross income was EUR112.4m,
about $128m. EUR182.4m of FY2021 gross revenue, about $215m, is far closer to the $200m the row
holds, and the matching rate for that year is 50.3 per cent, not 22. Loading 22 keeps the growth on
the period the row claims, and leaves the level for the basis audit. It is one line to flip once the
audit decides what the $200m is.

# Part four: what still does not close, and why

Seventeen rows. Fifteen are genuine search failures with the reason recorded row by row in the raw
file. Two are held for a ruling and are described below rather than left as failures.

Not found, in short: `notion-2026-01` (Sacra contradicts itself, 52.5 against 82 for the same
series), `vercel-2024-05` (only a secondary aggregator, nine-month window, neither endpoint
footnoted), `cohere-2023-06`, `masterclass-2021-05` (the tidy 100 per cent circulating online traces
back to an algorithmic estimator through two aggregators, and should be blacklisted),
`mercor-2025-02`, `qonto-2022-01`, `voodoo-2021-08`, `restaurant365-2023-05`, `pleo-2021-12`,
`klaviyo-2021-05`, `stripe-2023-03`, `stripe-2024-02`, `skims-2025-11`, `suno-2025-11`,
`mercury-2025-03`.

## What needs your ruling

**1. `nubank-2021-06`, and it is the currency question from your first point.** Nubank's FY2021
Form 20-F gives total revenue in US dollars of $612.1m for 2019, $737.1m for 2020 and $1,698.0m for
2021. That makes FY2020 over FY2019 **20.4 per cent** and FY2021 over FY2020 **130.4 per cent**. The
row prices on an LTM to June 2021, which sits between the two, and Nubank files no interim revenue
periods, so the LTM rate cannot be built from the filings at all.

The complication is that those are dollar translations of Brazilian real revenue, and the real fell
sharply against the dollar across 2019 and 2020. In reais the same two years grew far more than 20
per cent. So the dollar rate and the local rate are different numbers, and this is the one row in the
file where that is true and material.

Three ways to go, and it is your call:

- **20.4 per cent**, the dollar rate for the last full year completed before the round. Consistent
  with a file whose valuations and revenues are all in dollars. Puts Nubank MATURE.
- **130.4 per cent**, the dollar rate for the year the round sits inside. Consistent with the row's
  own LTM-June-2021 framing, which straddles the two years. Puts Nubank GROWING.
- **The local-currency rate**, which is what the market actually saw. It is not in the 20-F and would
  have to be pulled from Nu's Brazilian statements. I have not computed it, because a figure I
  calculate from average exchange rates is not a real statistic and does not belong in this file.

I would take 20.4 for consistency with the rest of the file, and put the local-currency figure on the
basis audit's list. But I have not written anything, because it moves a band.

**2. `virta-health-2021-04`, and it is the third "measure not named" row.** Virta's own Series E
release says: "Organizations are eager to add reversal solutions to their benefits portfolios,
driving Virta's growth rate to nearly 200% year over year."

It never says what grew. The file already loads two rows on the ordinary reading that a company's
growth rate is its revenue growth (`jobandtalent-2021-12`, `mews-2026-01`), so consistency would say
load this one too. I did not, for two reasons. The sentences on either side of it are about customer
organizations signing up, which is a count and is barred, so reading it as revenue is an inference
rather than the source's statement. And it says "nearly" 200, which makes it a ceiling, and the file
has a floor convention but no ceiling one.

Say the word and it goes in at 200, GROWING, DISCLOSED, marked MEASURE NOT NAMED, the same as the
other two.

**Worth knowing on the other two of that class.** `jobandtalent-2021-12` reads well: the very next
sentence gives the revenue run rate, and the company's own later releases report growth on revenue.
`mews-2026-01` reads badly, and worse than the 9 September pass knew. Its 50 per cent comes from a
release of 4 March 2025 describing calendar 2024, thirteen months before the January 2026 round. The
actual January 2026 round release exists, states no revenue and no ARR, and its only growth figure is
"Accelerated SaaS gross profit growth of 55%", which is not revenue growth. So that row is standing
on a stale sentence of unnamed measure while a contemporaneous release says nothing usable. It is
already loaded and this pass does not clear loaded rows, so it needs a decision, not a rerun.

# Part five: new entries for the basis audit

Flagged, not fixed, and each sits in the `flags` column of the raw file against its row.

- **Stripe, all three rows.** Stripe has never published net revenue. $4.1bn and $5.6bn are not in
  the cited sources, $5.6bn sits on two rounds a year apart, and it matches no year on record.
- **`blockfi-2021-03`.** Monthly revenue priced as annual, confirmed against the company's release.
  60x should be about 5x, and the honest denominator is a run rate or nothing.
- **`devoted-health-2021-10`.** Six-month revenue priced as LTM, confirmed. 51.4x should be about
  25.5x. Valuation is $12.6bn in the source and $12.7bn on the row.
- **`deel-2022-05`.** End-2022 ARR on a May 2022 round. 40.7x should be about 120x.
- **`mercury-2025-03`.** September 2025 annualised revenue on a March 2025 round, and it appears to
  have been lifted from Mercury's Series D page. 5.4x should be 7.0x.
- **`oura-2024-12`.** The row prices a December 2024 round on $225m. Oura's own release of
  22 September 2025 says 2024 revenue was over $500m.
- **`cohere-2023-06`.** The row prices June 2023 on $22m of ARR at 95.5x, but the only sourced
  figures put Cohere at about $13m annualized at the *end* of 2023 and $35m at end-March 2024. The
  $22m appears to trace to a Wikipedia line that misstates the article it cites.
- **`n26-2021-10`.** $200m held against a FY2020 gross income of EUR112.4m.
- **`wefox-2021-05`.** The company's release says $143m for 2020; the row holds $140m from TechCrunch.
- **`voodoo-2021-08`.** $336.9m reconciles with nothing. 2019 revenue was EUR360m, so the row implies
  revenue fell. The EUR380m 2020 figure on Wikipedia cites a September 2019 article and is
  unsupported.
- **`restaurant365-2023-05`.** Labelled ARR. Every source, the company's own release included, says
  revenue.
- **`turing-2025-03`.** Not an error. A convention question: 13.2x at pricing against 7.3x at
  announcement, and the company published both.
- **`pleo-2021-12`.** The Danish filing entity reports DKK 131.4m of revenue for FY2022, about $18m,
  against the $100m ARR the row prices on, so that entity holds only part of group revenue.

# Part six: what changed, and the proof

Written: `data/raw/2026-09-10_private-growth-round2.csv` (28 rows), `tools/load_growth_round2_10sep.py`,
one line in `tools/check_intake.py` so check 1 reads the new raw file as INGESTED rather than
PARTIAL, this document, and the status document.

Changed in the data: the three growth columns on eight rows of `data/private-rounds.csv` and three
rows of `data/private-rounds-consumer.csv`. Nothing else, on any row.

Proof, in this order:

- The loader re-reads both files after writing and compares them line by line. 320 in, 320 out. The
  eleven loaded lines differ in those three columns only; the other 309 lines are byte for byte the
  same. It exits 1 if anything else moves.
- I also diffed the files independently of the loader, row by row and column by column, against
  copies taken before the run. Same answer: eleven rows moved, three columns each, header unchanged,
  row order unchanged.
- Run it a second time and it reports 0 loaded, 11 already loaded, 0 refused.
- Every one of the 28 raw rows is accounted for by name: 11 loaded, 17 not found, 0 refused, 0
  unmatched.

Checks: twenty checks pass. Gate 124 of 142 before and after, the same 18 failures for the same
reasons. Golden 0 of 142 moved, which is expected: `band_compatible` gates the private lane only
when the founder has a growth band, and the 142 test companies carry no growth rate, so growth does
nothing until a founder supplies one through the quiz.
