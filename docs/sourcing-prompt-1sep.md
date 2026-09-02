# Sourcing prompt for the other LLM

Paste everything between the lines. It is written so the output drops straight into our files.
Two jobs are in here. Run them as two separate conversations, not one, or the output will blur.

---
---

## JOB 1: the 34 companies where an earlier pass found nothing

**Read this first, because the earlier pass failed in a specific way and I do not want it repeated.**

We checked 34 companies and concluded 18 had no revenue figure and 16 had one that was unusable.
Spot-checking two of those conclusions found both were wrong, for the same reason: **we searched the
specific funding round we had on file, and never asked whether the company had a DIFFERENT round
that did disclose something.**

- WHOOP: our file holds the August 2021 Series F, whose announcement genuinely has no revenue. But
  WHOOP's March 2026 Series G announcement says, in the company's own words, that bookings "exited
  the year at a $1.1B run rate", against a $10.1bn valuation. Perfect data, one round later.
- Strava: our file holds the November 2020 round. In May 2025 Strava raised at $2.2bn, and the Wall
  Street Journal reported it was "nearing $500 million in annual recurring revenue".

A third failure was different: **we only ever asked about revenue.** Checkout.com discloses no
revenue, but its September 2025 announcement says it expects to process "more than $300bn in total
eCommerce payment volume in 2025" against a $12bn valuation. We can price a payments company on
volume. Nobody asked.

So this job has three questions per company, not one.

```
You are sourcing financing-round data for a valuation comparables database. Accuracy matters far
more than completeness. A wrong figure is worse than a blank, and an invented figure is worse than
both. Never guess, never fill a gap with a plausible number, and never use your own knowledge as
the source: every number must come from a document you can name and link.

THE TASK

For each company below, search the COMPANY, not a single round. Find EVERY priced funding round it
has raised between 2019 and today where the valuation is public. Then, for each of those rounds, ask
three separate questions:

  QUESTION 1. Was an absolute REVENUE, ARR or run-rate figure public at or before that round?
  QUESTION 2. Was an absolute TRANSACTION VOLUME figure public at or before that round?
              (payment volume, TPV, GMV, gross merchandise value, gross bookings, loans originated)
  QUESTION 3. Was an absolute SUBSCRIBER or PAID MEMBER count public at or before that round?

A company that fails question 1 may still pass 2 or 3, and that is a useful result, not a
consolation prize. Report all three for every round.

START WITH THE MOST RECENT ROUND AND WORK BACKWARDS. Later rounds disclose more, because companies
get more confident about their numbers as they grow. The most recent round is where you are most
likely to find something.

WHAT COUNTS AS A USABLE FIGURE

It must satisfy ALL of these:

1. AN ABSOLUTE NUMBER, in a stated currency or unit. "Revenue doubled", "grew 3.5x", "our fastest
   year" are not figures. A threshold like "revenue exceeded $300 million" or "nearing $500 million"
   IS usable and must be flagged as a threshold, saying which side: "exceeded" puts a ceiling on the
   multiple, "nearing" puts a floor under it.
2. A STATED PERIOD. Which year, or which twelve months, or "run rate exiting 2025". A number with no
   period attached is excluded outright, however reputable the source.
3. PUBLIC AT OR BEFORE THAT ROUND WAS PRICED. This is the rule people get wrong most often. A figure
   that first appeared in an IPO prospectus two years later is hindsight: the investors who set that
   price could not have seen it. If the only figure you find was published after the round, report
   it, label it HINDSIGHT, and say so plainly.
4. A NAMED SOURCE WITH A URL AND A PUBLICATION DATE.

SOURCE QUALITY, best first. Say which tier each figure is.
  Tier 1: the company itself. Press release, newsroom post, blog, filed accounts, prospectus.
          THE FUNDING ANNOUNCEMENT ITSELF IS THE SINGLE BEST PLACE TO LOOK AND IS OFTEN SKIPPED.
          Check the company's own newsroom or press-centre page for every round.
  Tier 2: a filing or regulator. Companies House, SEC, local equivalent.
  Tier 3: contemporaneous reporting that names its own source. Bloomberg, FT, WSJ, Reuters,
          TechCrunch, Forbes, Sifted, when they say where the number came from.
  Tier 4: estimate aggregators and profile sites (CB Insights, PitchBook profiles, Sacra, Growjo,
          Latka, Tracxn). USABLE ONLY IF TIERS 1 TO 3 ARE EMPTY, and must be labelled an estimate.
          Never present a tier-4 figure as a company disclosure.

GROSS OR NET, for any revenue figure. Say which, and quote the wording that tells you. The test is
ownership, not size: does the revenue line contain money that belongs to somebody else? A
marketplace commission is NET. A freight broker's revenue holds the carrier's fee, so it is GROSS. A
staffing platform's holds the worker's wage, so GROSS. A first-party retailer keeps the whole sale
price, so it is NET even though the number looks large. If a company reports both, give both.

WHICH ENTITY. If the group has several legal entities, say which one the figure belongs to and
whether it is the same entity the valuation covers. Flipkart India Private Limited is the wholesale
arm and Flipkart Internet Private Limited is the marketplace, five times apart, and using the wrong
one changed a multiple from 34x to 6x.

OUTPUT. One row per ROUND, not per company, tab separated, with a header row:

company | round_date | round_name | valuation | valuation_currency | metric_type | metric_value |
metric_currency_or_unit | period_covered | gross_or_net | entity_named | threshold_direction |
source_tier | source_url | publication_date | exact_wording_quoted | available_at_pricing_yes_no |
confidence | notes

metric_type is one of: REVENUE, ARR, RUN_RATE, PAYMENT_VOLUME, GMV, GROSS_BOOKINGS,
LOANS_ORIGINATED, PAID_SUBSCRIBERS, NONE_FOUND.

If a round genuinely has nothing on all three questions, give me the row anyway with metric_type
NONE_FOUND and the notes saying what you searched. A documented blank is a useful result. A
fabricated number is not.

THE COMPANIES

Payments and fintech infrastructure:
  Paddle, Checkout.com, Primer, TrueLayer, Mollie, SumUp, Rapyd

Lending and financing:
  Wayflyer, Lendable, Zilch, Stenn, Tala, Pipe, Clearco, Oxyzo

Healthcare and labour marketplaces:
  Incredible Health, Clipboard Health, Nomad Health, Instawork, Malt

Logistics and delivery:
  Flock Freight, Veho, Getir, Rappi, Lalamove, J&T Express, Ninja Van

Consumer subscription:
  MasterClass, Daily Harvest, Strava, WHOOP, Flo Health, Calm

Commodities:
  Xpansiv

THREE I HAVE ALREADY DONE, so you can see the standard and skip them:

  WHOOP, 2026-03-31, Series G, $10.1bn valuation, RUN_RATE $1.1bn exiting 2025, tier 1, company
  newsroom, wording "bookings grew 103% year-over-year, exiting the year at a $1.1B run rate".
  Strava, 2025-05-22, $2.2bn valuation, ARR "nearing $500 million", tier 3, WSJ via PYMNTS,
  threshold direction: revenue is BELOW $500m so the multiple is a FLOOR above 4.4x.
  Checkout.com, 2025-09-26, $12bn valuation, PAYMENT_VOLUME "more than $300bn in total eCommerce
  payment volume in 2025", tier 1, company newsroom. No revenue figure exists; the volume does.
```

---
---

## JOB 2: private rounds in the verticals we cannot price at all

```
You are sourcing financing-round data for a valuation comparables database. The same rules as
before apply and they are not negotiable: absolute number, stated period, public at or before
pricing, named source with a URL, gross or net stated, entity named, tier stated, nothing invented,
a documented blank preferred over a guess.

THE TASK

I have almost no private comparables in the verticals below, so a founder in any of them currently
cannot be given a valuation range at all. I need priced funding rounds where BOTH the valuation and
a contemporaneous revenue figure are public.

WORK REVENUE FIRST, NOT VALUATION. Most rounds have a public valuation and no public revenue, so
searching by valuation wastes time. Start from companies known to have disclosed revenue, ARR or
run rate around a funding event, then check whether the round valuation is public too. A company
with both is worth ten with only one.

Aim for six to ten usable rows per vertical. Fewer real ones is much better than more padded ones.

THE VERTICALS, in priority order:

1. HEALTHCARE AND DIGITAL HEALTH. Care delivery, provider software, patient platforms, health
   insurance technology, clinical trials, mental health.
2. FITNESS, WELLBEING AND CONSUMER HEALTH. Subscription apps, connected hardware, nutrition.
3. EDUCATION AND LEARNING. Consumer learning, workforce and corporate training, school software.
4. INSURANCE AND INSURTECH. Distribution, underwriting, claims, embedded insurance.
5. GAMING AND INTERACTIVE. Studios, platforms, tools, user-generated content.
6. ENERGY, CLIMATE AND SUSTAINABILITY. Clean energy, storage, EV charging, carbon accounting.
7. CRYPTO AND DIGITAL ASSETS. Exchanges, custody, infrastructure, analytics.
8. AGRICULTURE AND FOOD PRODUCTION.

For each row I also need, so I can match a founder to the right neighbour:

  what_the_company_actually_does   one plain sentence, no marketing language
  who_it_sells_to                  consumer, small business, mid-market, enterprise, government
  revenue_model                    subscription, transaction fee, take rate, licence, usage, mixed
  country_of_headquarters
  growth_at_the_round              only if disclosed, with its source; leave blank otherwise

Same output format as before, one row per round, tab separated, with those five extra columns
appended.

Do not include: companies that were already public at the round date, debt-only rounds, grants,
and rounds where the valuation is described only as "reportedly" with no named source.
```

---
---

## Why the two jobs are separate

Job 1 is verification. It asks the model to overturn an earlier conclusion on 34 named companies,
and the risk is that it agrees too easily and hands back blanks. The three worked examples at the
end of the prompt exist to stop that: they show that the earlier blanks were wrong, and how.

Job 2 is discovery. It asks the model to find companies we have not named, and the risk is the
opposite: that it invents or pads to hit the count.

Mixing them lets the model average the two behaviours and do neither well.

## What I do when it comes back

Save the raw output to `data/raw/` before anything else touches it, per the durability protocol.
Then every figure gets checked against its own URL before it enters a valuation. Nothing from an
LLM enters the database as a source; the LLM finds the document, and the document is the source.
