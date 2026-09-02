# The second private batch: written down, checked, and ruled
2 September 2026. The 12 screenshots are archived at
`data/raw/2026-09-02_private-transactions-p01..p12.png` and were saved before anything was built
on them. The transcription is `data/raw/2026-09-01_private-transactions-daniil.csv`, now **191
rows, which matches the count your sheet states.** Nothing is lost.

## What arrived

Rows 123 to 195, running from Creditas Jan-2022 back to Buffer Oct-2014.

- Rows 123 to 152 overlapped the first batch. **Every one matched what was already transcribed.**
- 43 rows were new, all dated before 24 August 2021.
- Self-check: 189 of 191 rows tie post-money divided by metric to the multiple column. The two that
  do not are the ones already ruled: Gorillas (computed off pre-money) and Perplexity Jan-24
  (bottom of a range).

## Anthropic, done as you asked

You were right that the early rounds matter and that a seed founder should not be meeting the
Series F. I went looking for every priced Anthropic round with a denominator.

**Inserted: Series D, January 2024, $18.4bn post-money, $87m run-rate, 211.5x, and it feeds
medians.** Forbes of 11 January 2024: "$750 million in new funding that would nearly quadruple its
valuation to $18.4 billion." Forbes said the round was still in progress that day; TechCrunch of
23 June 2026, writing up Menlo's next fund, confirms it closed and that the round "quadrupled the
startup's valuation to $18 billion." The denominator is Anthropic's own: "our run-rate revenue has
grown from $87 million at the start of 2024 to over $5 billion in August 2025." That figure was
published later but it DESCRIBES this moment, which is what the hindsight rule asks for. It is the
same shape as a filed account.

**The Anthropic ladder now reads across stages, which is exactly what you wanted:**

| Round | Date | Post-money | Run-rate | Multiple |
|---|---|---|---|---|
| Series D | Jan 2024 | $18.4bn | $87m | **211.5x** |
| Series E | Mar 2025 | $61.5bn | $1.0bn | 61.5x |
| Series F | Sep 2025 | $183bn | over $5bn | 36.6x ceiling |
| Series G | Feb 2026 | $380bn | $14bn | 27.1x |
| Series H | May 2026 | $965bn | over $47bn | 20.5x ceiling |

**The rounds that still cannot be priced, and why.** The Series B of April 2022 and Google's $300m
of February 2023 have no valuation Anthropic ever disclosed. The Series C of May 2023 has no
revenue figure describing it; Anthropic itself declined to give a valuation and the press range
was $4.1bn to $5bn. And Amazon's money in 2023 and 2024 went in as **convertible notes with no
stated valuation**, confirmed from Amazon's own 10-Q, so none of it is a priced round no matter
what the aggregators say. One aggregator shows a "$2.8bn Series D in November 2024"; no primary
source supports it and it looks like a mis-dated duplicate of the Menlo round.

## The new tool this batch forced

`tools/check_denominator_monotonicity.py`. Across sequential rounds of one company on one basis,
the denominator should not fall. A fall is a flag, not a verdict, because companies do shrink, but
it catches a figure attached to the wrong round. Our own file header asked for this check on
31 August and it did not exist until today.

- **Our files: 1 flag.** Creditas, revenue falling from R$846m at Jul-2022 to R$592m at Dec-2025.
  That is a real decline, not an error.
- **Your sheet: 1 flag, and it is a genuine defect.** Upgrade, run-rate 160 in August 2021 falling
  to 100 in November 2021, with the multiple going 21.44x to 62.80x. See below.

## The disagreements, checked one by one

### Where your sheet is right and ours moved

**Trendyol Aug-21.** We held a $16.5bn post-money and $10bn of FY2021E GMV and printed no
multiple, so the row displayed nothing. 16,500 over 10,000 is 1.65x, which is what your sheet
carries. **Filled from numbers we already had.** Revenue was never published for Trendyol, so this
row prices on volume or not at all.

**GOAT Group Jun-21.** Ours carried 1.9x, yours 1.85x. 3,700 over 2,000 is 1.85 exactly. **Ours
was a rounding, now corrected.**

**Salesloft Apr-19.** We had a round with neither a valuation nor a denominator. Your 12.0x turns
out to be supportable, though only as display: TechCrunch of 25 April 2019 says "This round gives
it a valuation of $600 million, according to TechCrunch, although the company is declining to
comment on that", and CEO Kyle Porter is on the record saying "we're sitting around the 50 million
mark" three months after the round, with a March-2019 post seven weeks BEFORE the round already
reporting Salesloft crossing $50m ARR. The figure brackets the pricing date on both sides.
**Priced at 12.0x, out of medians because neither leg is company-confirmed.**

### Where your sheet has a defect

**Upgrade, both rows.** Your Aug-21 uses a $160m run-rate and your Nov-21 uses $100m. A consumer
lender's run-rate does not fall 38% in three months. I checked: the $100m figure belongs to
**Upgrade's Series D of June 2020**, seventeen months earlier, where TechCrunch reported "it is
currently on a $100 million run rate". No Q3-2021 figure of $100m exists anywhere. Upgrade's own
Series F release of November 2021 discloses no revenue at all; the only metric it gives is credit
volume.

So your 62.80x on the November round is built on a figure from eighteen months before it. This is
the same defect our own file header recorded on 31 August, where two figures from a single
TechCrunch piece had been attached to two rounds in the wrong order. We caught it and left both
rows unpriced. **Both our Upgrade rows stay unpriced**, and there is a second reason: Upgrade is
classified Lending & Credit, and our standing rule is that lenders price on book, never on
EV/revenue. What that row needs is a book value, not a revenue figure.

**Zopa Oct-21, same rule.** Your 25.16x is on FY2020 statutory revenue. Ours prices Zopa at 5.6x
book, which is where a lender belongs. Not a conflict about a number, a conflict about a method,
and our own rule settles it.

### Where ours is right and yours is not supported

**Calendly Jan-21. Ours, 42.9x.** Your 30.0x uses $100m ARR described as above a threshold. I
could not find that figure anywhere in day-of coverage. TechCrunch on the day of the round says
"The company last year made about $70 million annually in subscription revenues from its
SaaS-based business model." Even Sacra's own independent estimate for early 2021 is about $85m,
closer to our $70m than to your $100m. 3,000 over 70 gives 42.9x. **No change.**

**Rent the Runway Mar-19. Both of us right to leave it unpriced, and your 10.0x should come out.**
No day-of source discloses any revenue: I checked TechCrunch, Fashionista, PitchBook, Refinery29
and Forbes. The $100m traces to a 2016 Forbes headline and a 2017 Inc. piece, two to three years
stale. And the S-1 later showed fiscal 2019 revenue of $256.9m, so $100m was not just stale, it
was wrong by a factor of two and a half. Your 10.0x would be roughly 2.6x too high.

**Gong Jun-21. Ours right to leave it unpriced.** Your 72.5x uses $100m ARR "at transaction". Gong
disclosed no dollar figure. Its own release says only "Increased ARR 2.3X between Q1 of 2020 and
Q1 of 2021", and TechCrunch records the CEO explicitly declining: "While he wasn't ready to
discuss specific numbers, he did say that ARR grew 2.3x".

**Loft Mar-21. Ours right to leave it unpriced.** Your $150m run-rate is a stale prior-year
disclosure. On the day, the co-founder said only that revenue and GMV "increased significantly" in
2020 and declined to give specifics. The $150m appears a month LATER in a follow-up piece, quoting
something Loft had said the previous year about its first full year of operation.

**Klarna Jun-21. Ours, 37.6x. Your 32.57x uses a figure that does not exist.** Your denominator is
$1,400m of "annual revenue". Klarna's FY2020 statutory reports were checked in full, Holding AB
and Bank AB and the February 2021 statement release, and **there is no "Revenue" or "Total
revenue" line anywhere in them.** Klarna is a licensed bank and reported one top line: total net
operating income, SEK 10,000m for the Bank and SEK 10,094m for Holding.

Ours is that SEK figure restated at the pricing-date exchange rate rather than at Klarna's
full-year-2020 average of 9.2, and this is worth stating plainly because it is the same question
as the July-2022 row. The numerator is a June-2021 spot valuation. Translating a SEK flow at a
year-old average rate and dividing a spot USD valuation by it credits an FX move to Klarna as
multiple compression. Computing in krona throughout gives 37.8x, which is what our 37.6x is. This
is the same discipline that makes the PayFit row right, where the multiple is computed in euros
on both legs.

**One inconsistency on our own side, flagged not changed.** Zopa and Upgrade are both Lending &
Credit and neither prices on revenue. Klarna is also Lending & Credit and prices on net operating
income. Our rule says lenders and deposit-taking banks price on book. Either Klarna is an
exception worth writing down, or it should move to book like the other two. **Your call**, and it
matters because Klarna is one of the few large fintech comparables we have.

## What your sheet adds that we still do not have

**70 rows, 62 of them companies we have never carried.** The concentration has not changed and it
is still the hole in our coverage:

**Payments and banking:** Stripe x3, Revolut x4 (including Jul-2021), Chime x2, Monzo, N26, Atom
Bank, Raisin, Mercury, Plaid x2, Checkout.com, SumUp x2, MoonPay, Qonto, Brex x2, Spendesk, Pleo,
Mambu, Tipalti, Rapyd x2, Mollie x2, Carta.

**Crypto:** Chainalysis x2, Fireblocks x2, Blockchain.com, Supabase.

**Lending and working capital:** Clearco x2, Stenn, Wayflyer, Tala x2, Kriya. Six rows on loans
originated, a denominator we have almost nothing on.

**Insurance:** Wefox, Coalition, Alan.

**Consumer and health:** WHOOP, Strava, Flo Health, Calm x3, Olive & June, Packable, Whatnot,
Incredible Health, Xpansiv, Buffer.

**Software:** Cohere, Contentsquare, Remote, Deel, Canva May-24, Ramp x2, Perplexity Jul-25,
Airwallex Nov-21, Figma May-24.

Each needs its source URL before it goes in, which your sheet has in columns AA and AB. Those two
columns are the ones I still cannot read from the screenshots at full width, so when you next send
a batch, the source columns are the ones worth capturing.

## What changed in the files

`data/private-rounds.csv` 115 to 116 rows, `data/private-rounds-consumer.csv` two multiples
filled. Applied by `tools/apply_batch2_verdicts_2sep.py`, each change carrying its reason in
`notes`. Golden unchanged at 0 of 43.

## Sources

Calendly https://techcrunch.com/2021/01/26/how-atlantas-calendly-turned-a-scheduling-nightmare-into-a-3b-startup/ ·
Upgrade Series D https://techcrunch.com/2020/06/17/credit-focused-fintech-startup-upgrade-raises-40m-after-reaching-100m-run-rate/ ·
Upgrade Series E https://upgrade.com/press/upgrade-closes-105-million-series-e-round-at-3-325-billion-valuation ·
Upgrade Series F https://techcrunch.com/2021/11/16/credit-focused-company-upgrade-raises-280-million-at-6-billion-valuation/ ·
Gong https://www.gong.io/press/gong-raises-250-million-in-series-e-funding-at-7-25-billion-valuation ·
Loft https://techcrunch.com/2021/03/23/real-estate-platform-loft-raises-425m-at-a-2-2b-valuation-in-one-of-brazils-largest-venture-rounds ·
Rent the Runway S-1 https://www.sec.gov/Archives/edgar/data/1468327/000119312521291103/d194411ds1.htm ·
Salesloft https://techcrunch.com/2019/04/25/salesloft-funding/ ·
Klarna FY2020 https://owp.klarna.com/legacy/assets/2021/03/30041745/Annual-Report-Klarna-Holding-AB-2020-210329.pdf ·
Anthropic Series D https://www.forbes.com/sites/alexkonrad/2024/01/11/anthropic-750million-funding-round-menlo-ventures/ and https://techcrunch.com/2026/06/23/after-betting-the-firm-on-anthropic-menlo-ventures-raises-victorious-3b-fund/ ·
Anthropic run-rate https://www.anthropic.com/news/anthropic-expands-global-leadership-in-enterprise-ai-naming-chris-ciauri-as-managing-director-of ·
Amazon convertible notes https://www.sec.gov/Archives/edgar/data/1018724/000101872425000036/amzn-20250331.htm
