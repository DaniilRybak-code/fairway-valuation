# What still needs pulling, and a prompt for each
2 September 2026. Nine areas, ordered by what blocks the pilot. Each has a self-contained prompt
you can paste into your other LLM without any of the surrounding text.

Every prompt carries the same four rules, because every one of our data failures has come from
dropping one of them: a figure needs a URL and the sentence it came from; NOT FOUND is a valid
answer; the figure must be the one that was public AT the round; and estimator sites are a last
resort and must be labelled.

---

## 1. Seed investors — LANDED, with three small things left

Daniil's Active Seed & Series A Investor Screen arrived on 2 September: **88 deal rows, 25 funds,
8 sectors**, written to `data/raw/2026-09-02_seed-investor-screen.csv` with all ten of its source
columns. Its own gate is stricter than ours and is quoted in the file.

**The callable list now renders 97 houses and for the first time it has a seed end:** 8 pre-seed
and seed, 12 seed and Series A, 3 Series A, alongside 47 growth and crossover and 26 at Series B
and C. Every fork we serve now has someone a founder can call.

Three small things remain, none of them a new pull of any size.

**a. Fourteen of the original curated funds still have no dated deal** and are therefore still
refused: Ada Ventures, Backed VC, Concept Ventures, Founders Factory, Fuel Ventures, Future
Planet Capital, LocalGlobe / Latitude, MMC Ventures, Maven Capital Partners, Mercia Ventures,
Octopus Ventures, Passion Capital, SFC Capital, SyndicateRoom. Five of the original nineteen were
superseded by the screen. If any of the fourteen matter, they need the same two columns the
screen has; if they do not, say so and I will drop them, since an unrenderable row is clutter.

**b. Project A is in the screen but its latest deal is June 2025, fifteen months old.** The
screen's own window runs from January 2023 so it passes there, but it fails our twelve-month
activity rule and does not render. Two recent deals would bring it in.

**c. Fifteen of the eighty-eight URLs are marked low confidence** because they are long and small
in a photograph of a screen, and fifteen deal links point at an index page rather than the
announcement (Pale Blue Dot, Nina Capital, Heal Capital, FoodLabs, Project A, and single rows for
Skalar and Cordant). Both lists are in the raw file. A pasted text version of column J alone
would settle the first; the second needs the deal page rather than the blog index.

**The geography gap is still open and it is the bigger one.** We hold no country field anywhere:
not on the rounds, not on the company tags, not on our own investor files. The screen fixes this
for its own 25 funds, which now carry a real Region. The other 75 promoted houses still render in
the broader-fit tier because we cannot match them to a founder's country.

> For each investor in the attached list, state the countries or regions it invests in, with the
> page that says so. Where a fund says "global" or "sector agnostic", say that rather than
> guessing a list.

## 2. Source URLs for the 70 rounds — CLOSED, 2 September

**This was never a pull.** The URLs were already in the two screenshot batches Daniil sent on
1 and 2 September, in columns AA and AB, and they were dropped twice at transcription because
the target schema had no field for them. They are now in:
`data/raw/2026-09-01_private-transactions-daniil.csv` carries `valuation_source_url` and
`revenue_source_url` on **191 of 191 rows**.

Nothing is owed here. What remains is our own work: 70 rounds are now insertable with a source
per figure, and the only thing standing between them and the file is tagging each company into
our screening vocabulary.

## 3. The verticals a founder cannot be priced in at all

**Why it blocks.** A founder in one of these arrives, answers the quiz, and gets no private range.
Healthcare has 1 priced private round, gaming 1, insurtech 1. Education, fitness, climate, crypto
and agriculture have none.

> Find priced private funding rounds, 2021 to today, for companies in the eight sectors below.
> For each round I need: company name, transaction date, round name, amount raised, the
> post-money valuation, AND a revenue, ARR or annualised run-rate figure that was reported AT THE
> TIME of that round, with the period it covers.
>
> Sectors, and I want 6 to 10 rounds in each: digital health and healthcare software; video games
> and interactive entertainment; insurance and insurtech; education technology; fitness and
> wellness; climate and energy transition software; crypto and digital assets; agriculture
> technology.
>
> Rules. A round only counts if BOTH the valuation and a revenue-type figure were public. If a
> round has a valuation but no revenue figure, skip it, do not estimate. Say clearly whether the
> figure is ARR, annualised run-rate, or a full financial year, and which year. Give the URL and
> the exact sentence for the valuation and for the revenue figure separately, since they are
> often in different articles. Prefer the company's own announcement, then press published the
> day of the round. Label anything from Sacra, Getlatka, Growjo or Contrary Research as an
> estimate.
>
> Return: company | date | round | raised | post-money | metric type | metric value | period |
> valuation source URL | revenue source URL | the two quoted sentences.

---

## 4. The lender fork has one priced comparable in the world

**Why it blocks.** Zopa at 5.6x book is the only priced lender we hold. Four fixtures already
price off it alone, which means one row is setting the number for every lending founder. Lenders
price on book, so revenue figures do not help here.

> Find priced private funding rounds, 2021 to today, for lending and credit businesses: consumer
> lenders, SME lenders, digital banks with a loan book, buy-now-pay-later, revenue-based finance,
> invoice and working-capital finance.
>
> For each I need: company, date, round, amount raised, post-money valuation, and then AT LEAST
> ONE of these balance-sheet measures with the date it was struck: net loan book or gross loans
> outstanding; total equity or net asset value; loans originated in the last twelve months;
> customer deposits.
>
> Names to start with, and add any others you find: Zopa, Starling, Monzo, Atom Bank, OakNorth,
> Tandem, Allica, iwoca, Capital on Tap, YouLend, Liberis, Funding Circle, Lendable, Abound,
> Zilch, Klarna, Zopa Bank, Tala, Branch, Konfio, Creditas, Nubank pre-IPO rounds, MoneyLion,
> Upgrade, Avant, Best Egg, Happy Money.
>
> Rules. Balance-sheet figures usually come from filed accounts, so give me the filing and its
> date as well as any press coverage. Say clearly which measure each number is; do not convert
> between them. If a company reports in a currency other than dollars, give me the original
> currency figure and the exchange rate the source itself states, not one you calculate.
>
> Return: company | date | post-money | measure | value | currency | as-of date | source URL |
> quoted sentence.

---

## 5. The delivery and courier set is one row deep

**Why it blocks.** After the announcement-price ruling, Wolt at 23.5x is the top of the delivery
range and four fixtures moved with it. The set is thin enough that one comparable moves everyone.
Glovo sits in the file record-only for want of a single revenue figure.

> Two jobs.
>
> First, one figure: Glovo's revenue for the financial year 2020, in euros. Delivery Hero acquired
> control of Glovo on 31 December 2021 at a valuation of approximately EUR 2.3 billion, and I need
> the revenue figure that was public at that date. Look at Glovo's filed accounts in Spain,
> Delivery Hero's own reporting on Glovo, and Spanish press. Give me the figure, the exact
> sentence and the URL. If the only figures available are estimates, say so and label them.
>
> Second, priced private rounds 2021 to today for rapid grocery delivery, food delivery, and
> parcel and courier companies, with a revenue or GMV figure public at the round. Start with:
> Getir, Gorillas, Flink, Zapp, Weezy, Dija, Jokr, Rappi, iFood, Delivery Hero minority stakes,
> Bolt Food, Wolt, Deliveroo pre-IPO rounds, Gopuff, Instacart pre-IPO rounds, Picnic, Oda,
> Packfleet, Gophr, Fin Mile, Peak, DeliveryApp, Shutl, Stuart, Evri, Yodel, InPost pre-IPO,
> Xpressbees, Delhivery pre-IPO, Shiprocket, Loadsmart, Hived, Byrd, 99minutos.
>
> Rules as before: the figure must be the one public at the round, GMV and revenue must be
> labelled separately and never merged, and a figure with no stated period does not count.

---

## 6. Revenue CAGR for 192 listed names

**Why it blocks.** Growth is one of the seven dimensions the matcher scores on and 192 of 511
listed rows are invisible to it, because growth ranks on CAGR only. Pull list is
`docs/cagr-needed-pull-list.tsv`, pastable into Excel.

> For each ticker in the attached list, give me revenue for calendar year CY+0 and calendar year
> CY+2, both in the company's OWN REPORTING CURRENCY, together with the implied two-year compound
> annual growth rate.
>
> Two things matter more than anything else here. First, local currency: a growth rate must not
> have a currency movement inside it, and the last pull printed Wise as a 10.9% decline purely
> because of sterling. Second, calendarised: where a company's fiscal year does not end in
> December, calendarise it the way you did for the last listed refresh rather than using the
> fiscal year as reported.
>
> Also state the number of broker estimates behind the CY+1 figure, as you did last time, so I can
> see how well covered each name is.
>
> Two specific holes to close while you are in there: Fiserv's 2026 growth, where our file carries
> a manual 1% assumption because Capital IQ returned something wrong; and Nexi's CY+0 in local
> currency, which is blank.

---

## 7. Gross margin on the private rows

**Why it blocks.** We can tell a founder what multiple their peers priced at and nothing about the
quality of the revenue underneath it. Gross margin is the single field that separates a software
comparable from a reseller, and no private row has it.

> For each company and round in the attached list, find the gross margin or gross profit
> percentage that was public at the time of that round, or the nearest reported figure with its
> date.
>
> Rules. Say whether the figure is gross margin or contribution margin, and what it deducts:
> these are not the same and marketplaces in particular report both. If a company reports a
> "take rate" instead, give me that and label it as a take rate, not a margin. Where the only
> figure available comes from a later filing or an S-1, give it to me but mark it clearly as a
> later disclosure with its date.
>
> Return: company | round date | measure name | value | as-of date | source URL | quoted sentence.

---

## 8. Volume metrics still missing

**Why it blocks.** A marketplace or payments founder is priced on GMV or TPV, not revenue, and
gaps here mean the volume row on the football field is empty for them.

> Three jobs, all volume rather than revenue.
>
> First: MercadoLibre. I need annual total payment volume and annual gross merchandise volume
> separately, for the last reported financial year, each with the exact sentence from MercadoLibre's
> own reporting. They are two different denominators for the same enterprise value and I need them
> apart, not summed.
>
> Second: for the listed companies in the attached list where our GMV or TPV cell is blank, find
> the figure or confirm the company does not disclose one. "Does not disclose" is a useful answer
> and I want it stated explicitly rather than left blank.
>
> Third: for private marketplaces and payments companies in our set, find GMV or TPV as reported
> at the round. Start with Faire, Trendyol, GOAT Group, StockX, Whatnot, Ankorstore, Back Market,
> Vinted, Depop, Mercari, Rapyd, Tipalti, Mollie, Checkout.com, Airwallex, dLocal.
>
> Rules. Never merge GMV and TPV. State the exact period each figure covers. If a figure is a
> forward estimate rather than a reported actual, say so.

---

## 9. Paying subscribers, for the subscription fork

**Why it blocks.** Consumer subscription businesses price on subscribers as often as on revenue,
and we hold the metric for almost none of them. The 35-name list is
`docs/subscribers-pull-list-1sep.tsv`.

> For each company in the attached list, find the number of PAYING subscribers or paying members
> at the date given, with the exact sentence and the URL.
>
> Rules. Paying subscribers only. Registered users, monthly active users, downloads and "members"
> without a payment qualifier are all different numbers and I do not want them substituted; if
> only those are available, give me the figure and label it clearly as not a paying figure. State
> the exact as-of date, because a subscriber count is a point in time, not a period. Prefer the
> company's own announcement or filing.

---

## Two smaller things, no prompt needed

- **The 14 remaining source URLs** for `private-rounds-master-30aug.csv`. That file has been in the
  repo and unwired since 30 August and those URLs are the only thing blocking it.
- **The archetype lists review**, which is a decision rather than a pull. It gates the `fork_for`
  fix, which currently routes smol, Bokksu, FINN and Lyka to ecommerce and Inato, Priori and Moov
  to software on archetype alone.
