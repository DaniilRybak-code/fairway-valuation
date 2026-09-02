# The 19 disagreements, checked independently
2 September 2026. Every row below was checked against live sources, not against memory and not
against either database. Five research passes ran in parallel, each required to produce a URL and
the verbatim sentence containing the figure, and to answer NOT FOUND rather than guess. I then
re-fetched the sources that decided the widest gaps myself: AlphaSense, Replit, Turing, Notion,
Decagon, Klarna and PayFit.

## The result

**Our number is right in 16 of 19. Daniil's is right in 1. In 1 both are wrong. 1 needs a ruling.**

The pattern behind almost every disagreement is the same, and it runs one way: **Daniil's file
tends to carry the company's LATEST known revenue figure, applied backwards to an older round.**
That is hindsight, and our standing rule already excludes it: multiples use the revenue investors
had at pricing, never later actuals.

| Row | Right | The deciding fact |
|---|---|---|
| 1Password Jan-22 | **ours, 150** | His 120 is 1Password's July-2021 Series B figure, six months early |
| AlphaSense Sep-23 | **ours, 100** | His 200 is Fortune, 09-Apr-2024, describing end-2023, six months after pricing |
| Anthropic May-23 | **ours, 87**, but see below | Both figures post-date the round; ours is at least company-stated |
| Apollo.io Aug-23 | **ours, 96** | His 150 is Apollo's May-2025 figure, 21 months after pricing |
| Canva Aug-25 | **ours, 3,300** | His 4,000 is Feb-2026, six months after the tender |
| Clay Jan-26 | **ours, 100** | Clay's own tender announcement restates $100m ARR. His 150 is Sacra, May-2026 |
| Databricks Sep-23 | **ours, 1,500** | His 1,600 is actual FY revenue to 31-Jan-2024, a later period and a different metric |
| Decagon Jan-26 | **ours, 30** | His 100 is what Decagon told Newcomer in August 2026, seven months later |
| ElevenLabs Jan-25 | **ours, 90**, arguable | Both figures are in the same TechCrunch piece, Oct-24 and Nov-24 |
| Gorillas Oct-21 | **ours, 10.3x** | $2.1bn is pre-money (TechCrunch), $3.1bn is post-money (CNBC). His used pre |
| Guesty Apr-24 | **ours, 100** | His 164 is Latka's FY2024 estimate. Gross bookings were $4bn, not 164 |
| Jasper Oct-22 | **ours, 45** | The CEO said $45m to TechCrunch on the day. His 42.5 is Contrary Research, later |
| Klarna Jul-22 | **ours, 1,303.7** | Not a gross/net question at all. See below, I got this wrong first time |
| Notion Jan-26 | **NEITHER**, 600 | Ours was four months stale, his is six months of hindsight |
| PayFit Jan-22 | **ours** | Les Echos on the day of the round. His 100 is supported nowhere |
| **Replit Sep-25** | **HIS, 150** | **Our own cited source says 150. We misread it** |
| Snyk Dec-22 | **ours, 180** | His 150 is close to filed FY2022 revenue of $147m, but that is revenue, not ARR |
| Turing Mar-25 | **ours, 167** | The round announcement says the round was priced at $167m ARR |
| Wolt Nov-21 | **needs your ruling** | Both valuations are real and both are verified |

## The one we got wrong

**Replit, September 2025.** Our row cited replit.com/news/funding-announcement-series-c and read
$100m off it. I fetched that page myself. It says:

> "The funding comes on the heels of Replit growing annualized revenue from $2.8 million to
> $150 million in less than a year, a more than 50x increase"

TechCrunch of the same day carries the identical figure. Our $100m is Replit's June-2025 milestone,
three months before pricing. This was not a sourcing gap. We were citing the right document and
took the wrong number out of it. **Corrected: 30.0x becomes 20.0x.**

## The one where both files are wrong

**Notion, January 2026.** Our 500 came from CNBC of 18-Sep-2025, four months before the tender.
His 865 is Sacra's July-2026 estimate, six months after it. The figure current when the price was
set is in Forbes of 15-Dec-2025, the day Notion told employees about the tender: Notion "passed
$600M in ARR, half of it from AI products". itiger.com repeats it the next day and Sacra's own
independent series puts Notion at $610m at end-2025.

**Corrected: 22.0x becomes 18.3x**, and because "passed" makes the denominator a floor, that is a
ceiling.

## The two I described wrongly to you yesterday

**1. Klarna is not a gross versus net question.** I told you our 1,303.7 was bank net operating
income and yours was total revenue, and that our gross/net rule pointed at ours. That was a lazy
read. The real reason is in our own row note, which I had not read:

Klarna Holding AB's FY2021 annual report gives total net operating income of SEK 13,948m and
translates it itself at its disclosed 8.6 SEK/USD full-year average, which is USD 1.6bn. But the
$6.7bn post-money was struck in July 2022 at a spot rate of about 10.55. Dividing a July-2022 spot
valuation by a 2021-average translation mixes two exchange rates and understates the multiple.
We re-translated the SEK figure at the pricing-date rate, which is where 1,303.7 comes from, and
we recorded the reason. That is the right treatment and it was a deliberate decision, not an error.

Your 1,900 is Klarna's FY2022 revenue, published February 2023, seven months after the round, and
it is a different line item: Klarna's "Revenue" excludes commission expense, interest expense and
net result from financial transactions, so it sits SEK 2,633m above net operating income. **Ours
stands.**

**2. Five of the six rows I called "stale-sourced, yours probably wins" go the other way.**
I judged them by comparing our source dates to the round dates and never checked how old HIS
figures were. Only Notion was genuinely stale on our side, and even there his number is worse than
ours. Turing, Decagon, Apollo.io, Snyk and Clay all come out ours, and in four of those five his
figure post-dates the round by between four and twenty-one months. That was my error and it would
have moved five rows the wrong way if you had acted on it.

## Two sourcing defects found on our side, numbers unchanged

**AlphaSense.** We were citing the TechCrunch piece of 28-Sep-2023 for our $100m. I read that
article in full. It contains no AlphaSense revenue or ARR figure of any kind; its only business
numbers are 4,000 enterprise customers and 10,000 sources. The $100m actually comes from CNBC of
11-Apr-2023: "AlphaSense is much further along, having already surpassed $100 million in annual
recurring revenue in 2022." The number was right, the citation was not. **Fixed.**

**Clay.** We were citing Clay's $100m ARR milestone post of 08-Dec-2025. Clay's own tender
announcement of 28-Jan-2026 restates the same figure as the basis for the price: "Clay's revenue
grew more than 3.5x, reaching $100M in ARR in December." The round announcement is the stronger
source and now carries the row. **Fixed.**

## One row that breaks our own rule, flagged not changed

**Anthropic, May 2023.** Both candidate denominators post-date the round. Ours, $87m, is Anthropic's
own statement of 26-Sep-2025 describing the start of 2024, eight months after pricing. His, $100m,
is The Information's leak of 03-Oct-2023, five months after pricing, and the company's later
statement contradicts it. Contrary Research, citing Anthropic's own 2025 disclosure, says Anthropic
had $0 revenue in January 2023 and reached $100m around January 2024, which means at the May-2023
pricing there was very little revenue to divide by.

Our own row note records that the $87m was "used against the May-2023 price by instruction", so
this was your call and I have not touched it. But our standing rule says later figures are
hindsight and notes only. On that rule this row should be record-only, and 46.0x is not a real
multiple. **Your call to reopen or leave.**

## The one that still needs your ruling

**Wolt, November 2021.** Both figures are now verified against primary sources.

- DoorDash's own announcement of 09-Nov-2021: "Transaction is valued at approximately EUR 7.0
  billion", with DoorDash stock priced at $206.45 a share on a 30-day VWAP. TechCrunch the same day
  put that at $8.1bn.
- DoorDash's Form 10-Q for the quarter ended 30-Jun-2022: "The acquisition date fair value of the
  consideration transferred for Wolt was $2,842 million", being 36 million shares at the closing
  price on 31-May-2022 plus $133m of replacement awards. That is about $75 a share against the
  $206.45 used to size the deal.

The gap is 65% and it is entirely DoorDash's share price falling between signing and closing.
Nothing about Wolt changed. My view is unchanged: the announced price is what the market put on
Wolt on the day, and the closing figure is a fact about DoorDash. But it is a standing rule for
every all-stock deal and it also decides Glovo, so it is yours to set.

Note our row carries 2,838 and the 10-Q says 2,842. The difference is almost certainly a
measurement-period adjustment between the 10-Q and the 10-K we cite. Immaterial either way.

## Two rows in your file to fix

1. **Gorillas Oct-21.** TechCrunch on the day: "It's now being valued at $2.1 billion, pre-money".
   CNBC the same day: "Gorillas is now valued at $3.1 billion following the cash injection". Both
   are right, they are pre and post. Your 7.0x is on the pre-money. Post-money gives 10.3x, which
   is ours. Your $300m run-rate is confirmed by CNBC quoting Gorillas directly, so only the
   valuation needs the fix.

2. **Perplexity Jan-24.** Your multiple of 104x is taken at the bottom of a stated 5m to 10m range
   while your revenue cell shows the top. It should be a range, 52x to 104x.

## What changed in the data

Four rows in `data/private-rounds.csv`, applied by
`tools/apply_reconciliation_verdicts_2sep.py`, each with its reason written into `notes`:

| Row | Change |
|---|---|
| Replit Sep-25 | revenue 100 to 150, multiple 30.0x to 20.0x |
| Notion Jan-26 | revenue 500 to 600, multiple 22.0x to 18.3x, source to Forbes 15-Dec-2025 |
| AlphaSense Sep-23 | source only, TechCrunch to CNBC 11-Apr-2023 |
| Clay Jan-26 | source only, milestone post to the tender announcement |

The golden suite moved 8 of 43 profiles, of which 2 moved a range and 6 only re-ordered peers.
Both range moves are AI and agent fixtures where Replit and Notion sit in the peer set:
insforge mid 22.5x to 20.0x, skybridge mid 30.0x to 20.0x. Both fall because two multiples that
were too high came down. Deliberately rebaselined, now 0 of 43.

## Sources

Replit https://replit.com/news/funding-announcement-series-c ·
Turing https://www.businesswire.com/news/home/20250306942806/en/Turing-Gears-Up-to-Power-Next-Wave-of-AGI-with-$111-Million-in-Series-E ·
AlphaSense https://techcrunch.com/2023/09/28/alphasense-an-ai-based-market-intel-firm-snaps-up-150m-at-a-2-5b-valuation/ and https://www.cnbc.com/2023/04/11/alphabets-capitalg-leads-100-million-round-in-ai-startup-alphasense-.html ·
Notion https://www.techmeme.com/251215/p35 and https://www.itiger.com/news/1136424118 and https://sacra.com/c/notion/ ·
Decagon https://sacra.com/c/decagon/ ·
Klarna https://owp.klarna.com/legacy/assets/sites/15/2022/03/28054315/Klarna-Holding-AB-Annual-Report-2021-EN.pdf ·
PayFit https://techcrunch.com/2022/01/05/payroll-startup-payfit-is-frances-latest-unicorn-as-it-raises-289-million ·
1Password https://www.cnbc.com/2022/01/19/1password-valued-at-6point8-billion-by-investors.html ·
Jasper https://techcrunch.com/2022/10/18/ai-content-platform-jasper-raises-125m-at-a-1-7b-valuation/ ·
Snyk https://www.calcalistech.com/ctechnews/article/ryrrggdlt ·
Guesty https://techcrunch.com/2024/04/10/guesty-snaps-up-130m-at-900m-valuation-to-help-property-managers-list-on-airbnb-and-beyond/ ·
Wolt https://ir.doordash.com/news/news-details/2021/DoorDash-Joins-Forces-with-Wolt/default.aspx and https://www.sec.gov/Archives/edgar/data/1792789/000162828022021372/dash-20220630.htm ·
Gorillas https://techcrunch.com/2021/10/19/gorillas-grabs-close-to-1bn-series-c-values-the-on-demand-grocery-delivery-biz-at-2-1bn/ and https://www.cnbc.com/2021/10/19/delivery-hero-leads-1-billion-investment-in-grocery-start-up-gorillas.html ·
Clay https://www.businesswire.com/news/home/20260128514638/en/Clay-Announces-Second-Employee-Tender-Offer-in-Nine-Months-at-a-$5B-Valuation ·
Databricks https://www.databricks.com/company/newsroom/press-releases/databricks-raises-series-i-investment-43b-valuation ·
Canva https://www.capitalbrief.com/article/canva-revenue-climbs-50-in-just-over-a-year-amid-enterprise-growth-f8198e36-872a-449f-afec-4c94a8888664/
