# The six conflicts, and the four other decisions waiting on you

31 August 2026. Everything here is a ruling only you can give. Facts first, my view second, clearly
separated.

---

## A. The private transactions workbook: nothing was lost

You have not lost any transaction and you do not need to re-upload the data.

All 58 rounds are in `data/private-rounds-master-30aug.csv` with every analytical field intact:
company, date, round type, capital raised, the valuation wording verbatim, the revenue wording and
its timing, whether the metric was public at pricing, the evidence status, the multiple with its
inequality preserved, the investors, the source tier and the caveat. That file is committed.

**One column is missing: the source URL.** In the screenshots the URLs were too small to read
character by character, and a URL wrong by one character is worse than no URL, so all 58 say
`NEEDS_WORKBOOK` rather than a guess.

**And only 14 of the 58 actually need one.** 25 rows are marked "found, not usable" and 19 are
"not found", so they will never be shown to a founder and never need a citation. The 14 that will
be shown are:

| Company | Date | Multiple as your workbook states it |
|---|---|---|
| Airwallex | Nov-21 | <55.0x |
| dLocal | Apr-21 | 48.0x |
| Zepz (WorldRemit) | Aug-21 | 14.8x, flagged |
| Marqeta | May-20 | <14.3x gross revenue, flagged |
| Jobandtalent | Dec-21 | <2.08x |
| Loadsmart | Feb-22 | <5.2x |
| Zopa | Oct-21 | 8.8x |
| Creditas | Jan-22 | 24.0x |
| Fundbox | Nov-21 | <11.0x |
| Gorillas | Oct-21 | <10.3x |
| Gopuff | Jul-21 | about 44.1x |
| Savage X Fenty | Feb-21 | >6.7x |
| AG1 / Athletic Greens | Jan-22 | about 8.8x |
| Patreon | Apr-21 | <40.0x |

So the ask is 14 URLs, not a workbook. Paste those 14 rows, or just the URL column, in any form.
If the workbook is easier to export whole, that works too, but it is not required.

---

## B. The six conflicts. What each one actually is

Each is a disagreement between what I inserted this morning and what your workbook says. In every
case both numbers are real; the question is which denominator is the right one.

### 1. Loadsmart. Not a conflict, I was wrong. Insert it.

I dropped it because I could not find a stated period for the revenue. Your workbook has one:
gross revenue "north of $250 million in 2021", from contemporaneous VentureBeat, marked usable at
under 5.2x. My exclusion was the error. **Nothing for you to rule on: I will insert it.**

### 2. Gorillas. Same shape. Insert it.

I dropped it. Your workbook marks it usable at under 10.3x post-money against a run rate above
$300m, Tier 1 on both the transaction and the metric, and calls it the strongest logistics pricing
comparable in the set. **Nothing to rule on: I will insert it.**

### 3. Jobandtalent. Same. Insert it.

I dropped it. Workbook marks it usable at under 2.08x on the revenue run rate. **I will insert it.**

### 4. Zepz. 14.8x or 21.0x. YOUR CALL.

Both figures are Zepz's own and both are defensible.

- **I used $238m** and got 21.0x. That is the revenue figure in the later filed accounts.
- **Your workbook uses $338m** and gets 14.8x. That is the figure quoted in the round announcement
  itself.

The at-pricing rule says the denominator must describe a period public on or before the pricing
date. The round-announcement figure passes that test by construction, because it was published
with the round. The filed-accounts figure is more reliable but describes the same period from a
later vantage point, and our rule cares about the period, not the publication date, so it also
passes. The two are not measuring the same thing: the $338m is very likely gross and the $238m
net, which is the recurring killer in this dataset.

**My view: take 14.8x** and mark the row as needing a basis check, because a round-announcement
figure is what the investor actually priced against. But if you know the $338m is gross, then
14.8x is a gross multiple sitting in a net-revenue median and the row should be excluded from
ranges entirely rather than shown at either number. **Ruling needed: 14.8x, 21.0x, or exclude.**

### 5. Marqeta. 30.0x or under 14.3x gross. YOUR CALL.

- **I used FY2019 net revenue from the S-1** and got 30.0x.
- **Your workbook uses contemporaneous Forbes reporting** of "above $300 million" 2019 GROSS
  revenue and gets under 14.3x, flagged, "retain only as valuation over gross".

The S-1 was published in 2021, well after the May-2020 round. It describes FY2019, so it passes
the period test, but nobody pricing that round in May 2020 had seen it. Your figure is what was
knowable at the time. It is also gross, and "above $300 million" is a threshold, which makes 14.3x
a ceiling, not a point.

**My view: your workbook is stricter and right on the evidence, and its number is not usable in a
net-revenue range.** So Marqeta should be visible to a founder as context with the label "at most
14.3x on gross revenue" and be out of every median. **Ruling needed: use 30.0x net, use the
capped gross figure as context only, or drop.**

### 6. Pine Labs and Razorpay. Your workbook says neither is usable. YOUR CALL.

I inserted both as usable, at 30.3x and 67.6x.

- **Pine Labs.** The FY2021 statutory operating revenue is ₹726 crore, about $99m at the rate on
  the pricing date. Another cited figure puts net revenue at about $107m or ₹800 crore, which is a
  different definition. Your workbook says the two conflict and marks it not usable.
- **Razorpay.** FY2022 revenue of ₹1,485.7 crore was not available at the December 2021 pricing.
  FY2021 at ₹844.6 crore was available, about $111m, giving 67.6x, but your workbook says that is
  the wrong side of the gross-versus-net question.

Razorpay at 67.6x on a gross basis is the single number most likely to distort a fintech founder's
range. **My view: follow your workbook and mark both not usable.** **Ruling needed: keep or drop.**

### 7. Better.com. A seventh that was not on the list.

Your workbook covers the April-2021 SECONDARY and marks it not usable. My insert used the
May-2021 SPAC transaction, which your workbook does not cover, at 8.79x. These are two different
transactions, so neither of us is contradicting the other. **Ruling needed: is the May-2021 SPAC
a transaction we want to price off at all, given a SPAC valuation is negotiated rather than
market-cleared?**

---

## C. Why the disputed rows matter, even though we never show a global median

You are right that we do not show a median of the whole set anywhere, and a median of 149 rounds
would be meaningless. That is not what is happening.

The range a founder sees is the median of **his own handful**, and that handful is usually three
names. Right now five of our payments test companies get a handful in which two of the three rows
are disputed:

| Test company | Its private range today | Built from |
|---|---|---|
| payabli | 30.0x to 48.0x, middle 30.3x | Pine Labs 30.3x, Marqeta 30.0x, dLocal 48.0x |
| rainforest | 30.0x to 48.0x, middle 30.3x | the same three |
| moov | 30.0x to 48.0x, middle 30.3x | the same three |
| trolley | 21.0x to 48.0x, middle 30.0x | Zepz 21.0x, Marqeta 30.0x, dLocal 48.0x |
| dots | 21.0x to 48.0x, middle 30.3x | Zepz 21.0x, Pine Labs 30.3x, dLocal 48.0x |

If the disputed rows stop feeding the ranges, every one of those five collapses to a single point
at dLocal 48.0x. The founder goes from being told roughly 30x to being told 48x, on the same
business, with no new information. That is a 60 per cent move driven entirely by which rows we
trust.

So the answer to "why does this matter" is: **not because of a global median, but because with
three rows in a handful, one disputed row is a third of the evidence, and two are most of it.**

It also shows quarantining alone makes things worse rather than better. The real fix is your
workbook's usable rows going in, which turns a handful of three into a handful of six or seven.
That is why the 14 URLs matter more than the quarantine.

---

## D. FX: you are mostly right, and the ask is smaller than it looked

Your instinct is correct. We price everything in USD and the Capital IQ pull is already in USD, so
for the multiples there is no FX question at all.

The twelve rows are a different thing. They are not multiples. They are the volume figure **as the
company itself published it**, and eleven companies publish it in their own currency: Airtasker in
Australian dollars, Credit Saison in yen, Worldline in euro, PayPoint in sterling, AvenuesAI in
rupees, Fawry in Egyptian pounds. There is no USD version to take, because the company never
published one.

Two ways out, and the second is probably what you want:

1. **Give me a rate table** and I convert. This is the only route if we want to show a founder
   "Worldline processes 500 billion euro, which is about $X".
2. **Do not convert at all.** Keep the local figure with its currency, show it in its own currency
   where we show it, and never put it in a dollar comparison. Only the ratio matters for
   valuation work, and a ratio of a company's own enterprise value to its own volume is
   currency-free.

**My recommendation is 2.** It removes the FX question entirely and loses nothing we actually use.
Then no rate table is needed and the twelve rows stop being a blocker.

---

## E. Your multi-round rule, implemented

Reading your rule back so you can correct it if I have it wrong:

- Between two rounds of the SAME company, revenue scale is the first gate **only when the
  multiples are an order of magnitude apart.** When they are similar, take the latest.
- Everywhere else in comparable selection, revenue scale matters less and growth and maturity
  matter more. Size stays out of selection, exactly as it always has.

Built and in the repo. The threshold sits at 3.0x, and it is placed where the data is empty rather
than tuned: measured across the companies that carry more than one round, the spread between a
company's own multiples is either under 1.5x (Mews 1.04, SKIMS 1.06, Vinted 1.15, AlphaSense 1.5,
Scale AI 1.5) or over 7x (Klarna 7.4, Meesho 11.0). Nothing sits between, so any threshold in that
gap gives the same answer today. If a future round lands inside the gap, the constant needs a fresh
look rather than a nudge.

What it does, tested on a real fixture with Meesho's own verified revenue figures:

| Founder revenue | Which Meesho round they now see |
|---|---|
| $20m growing 180% | Sep-21 at 45.8x |
| $107m growing 124% | Sep-21 at 45.8x |
| $400m growing 60% | May-24 at 4.2x |
| $922m growing 40% | May-24 at 4.2x |
| $2,000m growing 20% | May-24 at 4.2x |

Meesho-2021 at 45.8x was unreachable by anyone yesterday. It is now reachable by the founder it is
actually evidence about. Every chosen round carries a plain-language sentence explaining why that
round and not the other one.

Nothing moved in the 43 fixtures, because they carry no revenue or growth and so fall back to the
old behaviour. The rule only bites when a founder answers the quiz, which is the live path.

---

## F. The nursa "bug" is not a bug, and I was wrong to call it one

I reported that nursa holds three priced comparables and returns no range, and called it a plain
code defect. It is not. Traced tonight:

nursa's five private comparables are Whatnot, Vinted, Faire, Meesho and Flipkart. All five land in
the BROAD tier, and `private_range` deliberately returns nothing for BROAD, because a BROAD name is
context rather than a price. The code is doing what it was told.

The reason they are all BROAD is that a per-diem healthcare shift marketplace shares a business
model with a fashion resale marketplace and shares nothing else: not the end market, not the
customer, not the buying occasion.

So this is not a bug to fix. It is exactly the case you described: a founder in a category with no
clear precedent, where a blank should be a trigger to apply judgement rather than a conclusion.
The fix is the next-best-neighbour step, which needs your three open answers:

1. May a neighbour cross business families, or must a marketplace only ever be priced off
   marketplaces?
2. May a gross-revenue neighbour price a net-revenue founder if the label says so loudly?
3. How far down maturity do we reach before a name becomes context rather than price?

## G. SEO tools: yes, you gave them, and here is exactly what came back

Semrush is in, as a private round at Nov-25 and 4.3x, and it feeds ranges. Similarweb is in as a
listed name at 2.1x. Ahrefs went out on the 226-company list you ran, and came back with no
multiple, which is right: it has never raised, so there is no priced round to find. Ubersuggest,
Screpy, Wope and Keyword Insights were on the same list and came back blank for the same reason.

For openseo the matcher surfaced Semrush and held nothing else back. The gap there is real market
scarcity, not lost data.
