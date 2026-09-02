# Private transactions: your database against ours

> **SUPERSEDED IN PART, 2 September 2026.** Section 1's guess at which side is right was checked
> against live sources and was wrong on five rows. The verified verdicts are in
> `docs/private-verdicts-2sep.md`. Short version: our number is right in 16 of 19, Daniil's in 1
> (Replit), neither in 1 (Notion), and Wolt still needs a ruling. Everything else in this file
> (the counts, the new rows, the rows only we have, the self-consistency checks) still holds.
1 September 2026. Compares the 148 rows transcribed from your 16 screenshots against the
163 rows in data/private-rounds.csv and data/private-rounds-consumer.csv.

Your source has 191 transactions. The screenshots cover 2021-08-24 through 2026-07-09,
sorted newest first. The remaining 43 rows are all dated before 24 August 2021 and have
not been sent yet.

## The headline

The two files are complementary, not competing. Where they overlap they mostly agree on
the valuation and disagree on the denominator. Where they do not overlap they cover
different parts of the market: yours is fintech and software, ours is ecommerce, consumer
and India.

- 95 rows match on company and month.
- 55 of those 95 agree outright.
- 19 disagree on a number. In 17 of the 19 the valuation is identical and only the
  revenue figure differs.
- 21 are rows where you carry a multiple and we do not.
- 52 rows in your file are genuinely new to us. 45 are companies we have never had.
- 12 priced rows inside your date window are ours alone. Another 21 priced rows of ours
  sit before your window and may be in the 43 you have not sent.

## 1. The 19 numeric disagreements

Seventeen of them are the same story: same post-money, different revenue. The valuation
is not in dispute anywhere except Wolt.

| Company | Month | Your post-money | Your revenue | Your x | Our revenue | Our x | Ratio |
|---|---|---|---|---|---|---|---|
| AlphaSense | Sep-23 | 2,500 | 200 | 12.5 | 100 | 25.0 | 2.00 |
| Decagon | Jan-26 | 4,500 | 100 | 45.0 | 30 | 150.0 | 3.33 |
| PayFit | Jan-22 | 2,100 | 100 | 21.0 | 45.3 | 45.5 | 2.21 |
| Turing | Mar-25 | 2,200 | 300 | 7.33 | 167 | 13.2 | 1.80 |
| Notion | Jan-26 | 11,000 | 865 | 12.72 | 500 | 22.0 | 1.73 |
| Guesty | Apr-24 | 900 | 164 | 5.49 | 100 | 9.0 | 1.64 |
| Apollo.io | Aug-23 | 1,600 | 150 | 10.67 | 96 | 16.7 | 1.56 |
| Clay | Jan-26 | 5,000 | 150 | 33.33 | 100 | 50.0 | 1.50 |
| Replit | Sep-25 | 3,000 | 150 | 20.0 | 100 | 30.0 | 1.50 |
| Klarna | Jul-22 | 6,700 | 1,900 | 3.53 | 1,303.7 | 5.1 | 1.46 |
| Canva | Aug-25 | 42,000 | 4,000 | 10.5 | 3,300 | 12.7 | 1.21 |
| Anthropic | May-23 | 4,000 | 100 | 40.0 | 87 | 46.0 | 1.15 |
| Databricks | Sep-23 | 43,000 | 1,600 | 26.88 | 1,500 | 28.7 | 1.07 |
| Jasper | Oct-22 | 1,500 | 42.5 | 35.29 | 45 | 33.3 | 0.94 |
| ElevenLabs | Jan-25 | 3,300 | 80 | 41.25 | 90 | 36.7 | 0.89 |
| Snyk | Dec-22 | 7,400 | 150 | 49.33 | 180 | 41.1 | 0.83 |
| 1Password | Jan-22 | 6,800 | 120 | 56.67 | 150 | 45.3 | 0.80 |

Your denominator is the higher one in 13 of 17. That is a systematic difference, not
noise, and it makes your multiples systematically lower.

### Which side is likely right, by our own rule

The rule we already agreed is that the denominator must be the one current at the round
date, and that the round announcement beats a later filing or an earlier third-party note.
Applying it to our source URLs:

**Our figure comes from a source that predates the round. Your figure probably wins.**

| Company | Round | Our source | Gap |
|---|---|---|---|
| Notion | Jan-26 | CNBC, September 2025 | 4 months stale |
| Turing | Mar-25 | Businesswire, 28 Jan 2025 | 2 months stale |
| Decagon | Jan-26 | Forbes, December 2025 | 1 month stale |
| Apollo.io | Aug-23 | Sacra research page, undated | third party, not the round |
| Snyk | Dec-22 | Sacra research page, undated | third party, not the round |
| Clay | Jan-26 | Clay's own "$100m ARR" blog post | milestone post, not the round |

**Our figure comes from the round announcement itself. We should not move without a
better source from you.**

1Password (1password.com newsroom), Anthropic (anthropic.com), Databricks and AlphaSense
and ElevenLabs (TechCrunch pieces dated the day of the round), Replit
(replit.com/news/funding-announcement-series-c), Canva (Yahoo Finance on the stock sale),
Jasper (TechCrunch, day of round).

AlphaSense is the one to look at hardest. Our source is the TechCrunch piece from the day
of the round and our note says "ARR in 2022", against a September 2023 round. Yours says
200. If TechCrunch carried both figures, yours is the right one and ours picked the
stale half of the sentence.

Replit is the same shape in reverse. Our source is Replit's own Series C announcement and
we read 100 from it. Yours says 150. One of us misread a primary source.

**Two are basis questions, not sourcing questions.**

- **Klarna Jul-22.** Yours is total revenue, 1,900. Ours is bank net operating income,
  1,303.7, from Klarna's own annual report. Klarna is a bank; net operating income is the
  net figure and our gross-versus-net rule points at ours. No change unless you overrule.
- **Guesty Apr-24.** Ours is tagged NET_REVENUE at 100. Yours is 164 and labelled
  "Revenue / ARR proxy". If your 164 is gross bookings we must not use it. Worth one look.

### The two that are not denominator differences

**Wolt, Nov-21. This is a valuation disagreement and it is a real ruling.**
Yours: 8,100 post-money over 345 revenue, 23.48x. That is the announced price, EUR 7.0bn,
quoted everywhere as $8.1bn.
Ours: 2,838 over the same 345, 8.2x. That is DoorDash's audited consideration in its 10-K.
It was an all-stock deal and DoorDash shares fell between signing and closing, so the
audited number is 65% below the announced one.

Both are real. They answer different questions. The announced price is what the market
put on Wolt on the day. The audited figure is what the acquirer's shares turned out to be
worth months later, which is a fact about DoorDash, not about Wolt. My read is that for
pricing a founder's business the announced value at signing is the right one and we should
switch, but this needs your call because it sets a standing rule for every all-stock deal.
Glovo has exactly the same exposure and is currently record-only for this reason.

**Gorillas, Oct-21. Your row does not tie to itself.**
Your file shows post-money 3,100, revenue 300, multiple 7.0. But 3,100 / 300 is 10.33.
7.0 is 2,100 / 300, which is the pre-money. Either the multiple was computed off pre-money
or the post-money cell is wrong. Ours shows 10.3x on the same 3,100 and 300.

## 2. The only other row in your file that does not tie to itself

I checked all 148 transcribed rows for post-money divided by revenue equalling your
multiple column. 146 tie. Two do not: Gorillas above, and:

**Perplexity, Jan-24.** Post-money 520, revenue shown as 10, multiple 104. 520 / 10 is 52.
104 is 520 / 5. Your basis note says "range 5m-10m", so the multiple was taken at the
bottom of the range while the revenue cell shows the top. Not wrong, but the row prices at
104x when the same data supports 52x to 104x. It should be stored as a range or it will
drag any median it lands in.

## 3. The 21 rows where you have a multiple and we do not

Four of these are rows where we hold the same denominator you do and deliberately did not
price them:

| Company | Round | Denominator | Why we withheld |
|---|---|---|---|
| Rokt | Jan-25 | 600, same as yours | our note says gross network revenue, so gross-versus-net gates it |
| Thrasio | Oct-21 | 1,000, same as yours | founder forecast, and post-money was never disclosed so we left it blank |
| Perplexity | Sep-25 | 200, same as yours | tagged "< threshold", so the multiple is a floor of 100x, not a point |
| Gong | Nov-25 | ours 300, yours 500 | ours tagged "> threshold", so ours is a ceiling of 15x, not a point |

Those four are our gates working, not our data missing. Yours prices them; ours will not
until the basis question is settled.

The other 17 are genuine gaps where your file has a figure and ours has nothing:
Celonis Aug-22, Cyera Apr-24, dbt Labs Feb-22, Faire Nov-21, Flink Sep-24, Glovo Dec-21,
GoCardless Feb-22, Hopper Feb-22, LangChain Oct-25, Liquid Death Mar-24, Perplexity Dec-24,
Perplexity Jan-24, Personio Jun-22, TravelPerk Jan-24, Upgrade Nov-21, Weights & Biases
Mar-25, Zopa Oct-21.

Several of those carry notes in our file saying the figure was never published. Your file
says otherwise, so each needs its source before it goes in.

## 4. Eight rows on our side that hold both numbers and never got a multiple

| Company | Round | Post-money | Revenue | Would be | Why it is blank |
|---|---|---|---|---|---|
| Gong | Nov-25 | 4,500 | 300 | 15.0x | "> threshold", ceiling not a point |
| Outreach | Jun-21 | 4,400 | 100 | 44.0x | "> threshold", ceiling not a point |
| Faire | Nov-25 | 5,200 | 500 | 10.4x | "> threshold", ceiling not a point |
| Perplexity | Sep-25 | 20,000 | 200 | 100.0x | "< threshold", floor not a point |
| Wiz | Mar-26 | 32,000 | 1,000 | 32.0x | reported estimate, not disclosed |
| Razorpay | Dec-21 | 7,500 | 110.9 | 67.6x | display gate NO_FIELD |
| Rokt | Jan-25 | 3,500 | 600 | 5.8x | gross network revenue |
| Thrasio | Jul-20 | 1,260 | 300 | 4.2x | pro forma of undisclosed composition |

Every one is deliberate. But four of them are bounded, and we have ev_revenue_low_x and
ev_revenue_high_x columns sitting empty. A bound is usable information for a founder. We
should populate the bounds rather than show nothing.

## 5. What your file adds

52 rows we do not have, 45 of them companies we have never carried. The concentration is
striking and it fills our worst hole:

**Payments and banking:** Stripe x3 (Mar-23, Feb-24, Feb-25), Revolut x3 (Nov-23, Aug-24,
Nov-25), Chime, Monzo, N26, Atom Bank, Raisin, Mercury, Plaid, Checkout.com, SumUp x2,
MoonPay, Airwallex Nov-21, Qonto, Brex x2, Spendesk, Pleo, Mambu, Tipalti.

**Crypto and infrastructure:** Chainalysis, Fireblocks, Blockchain.com, Supabase.

**Lending and working capital:** Stenn, Wayflyer, Tala, Kriya. All four price off loans
originated, which is a denominator we currently have almost nothing on.

**Insurance:** Wefox, Coalition, Alan. We have one priced insurtech round today.

**Consumer and health:** WHOOP Mar-26 (the Series G you sent me), Strava May-25, Flo
Health, Olive & June, Packable, Incredible Health, Whatnot, Xpansiv.

**Software:** Cohere, Contentsquare, Remote, Deel May-22, Canva May-24, Ramp Jul-25 and
Aug-21, Perplexity Jul-25.

One caution. Figma 2024-05-16 at 17.86x is the same transaction as our Figma 2024-07 at
17.9x. You date it at announcement, we date it at close. Same round, same numbers. We need
one convention. I suggest announcement date, because that is when the price was set, and
because it is the date a founder will recognise. Our row also has a small tidiness bug:
its id says figma-2024-05 while its date says 2024-07.

## 6. What our file keeps

Inside your date window, 12 priced rows are ours alone, and they are the ecommerce, India
and consumer side you do not cover:

Meesho Sep-21 and May-24, Flipkart Jul-23, SHEIN Jan-24, Vinted Apr-26, Shiprocket Aug-22,
Xpressbees Feb-22, Zepz Aug-21, Creditas Jul-22, Liquid Death Oct-22, Mailchimp Sep-21,
Semrush Nov-25.

A further 21 priced rows of ours sit before 24 August 2021, outside your screenshots:
Away, Glossier, Harry's, Savage X Fenty, Marqeta x2, Creditas Dec-20, Loadsmart, Calendly,
Klaviyo, Algolia, Yotpo, Patreon, Better.com, Gopuff, Pine Labs, dLocal, StockX,
Delhivery, Flipkart Jul-21, Thrasio Jul-20. Some of these may be in the 43 rows you have
not sent.

## 7. What I need from you

1. **Wolt, and every all-stock acquisition.** Announced price at signing, or audited
   consideration at closing? This is a standing rule, not one row. It also decides Glovo.
2. **Gorillas.** Confirm your 7.0x was computed off pre-money so I can leave ours at 10.3x.
3. **Perplexity Jan-24.** Confirm it should be stored as a range, 52x to 104x.
4. **Date convention.** Announcement or close, for Figma and for everything after it.
5. **The six stale-source rows** (Notion, Turing, Decagon, Apollo.io, Snyk, Clay). If your
   figures are sourced to the round, I will take yours over ours.
6. **AlphaSense and Replit.** Both our sources are the round announcement itself and we
   still differ by 2x and 1.5x. One of us misread. Worth a direct look at those two links.
7. **Guesty.** Is your 164 net revenue or gross bookings?
8. **The remaining 43 rows**, all dated before 24 August 2021.

Nothing has been changed in the data files. This is a reconciliation, not a merge.
