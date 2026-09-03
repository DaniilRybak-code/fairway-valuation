# Prompt: find private rounds priced per PAYING SUBSCRIBER

Run this in the other LLM. It is written to be pasted whole.

---

You are sourcing comparable transactions for a startup valuation engine. I need PRIVATE FUNDING
ROUNDS or ACQUISITIONS of CONSUMER SUBSCRIPTION businesses where the number of PAYING SUBSCRIBERS
at the time of the round is publicly stated, so I can compute enterprise value per paying subscriber.

I already hold two and they agree closely: Flo Health, September 2021, $800m over 1.5 million paying
subscribers, so $533 each. Calm, December 2020, $2.0bn over 4.0 million paying subscribers, so $500
each. I want more of these.

## The shape I am looking for

Consumer apps and services billed on a recurring basis, where revenue is often not disclosed but the
subscriber count is: health and fitness, meditation and wellness, language learning, music and audio,
dating, news and reading, consumer productivity and utility apps, streaming, consumer VPN and
security, photo and video tools, consumer AI assistants.

## For every transaction, give me these fields and nothing else

| field | what it must be |
|---|---|
| company | legal or trading name |
| date | the month the price was set, YYYY-MM |
| round_type | Series C, acquisition, secondary, and so on |
| post_money_musd | post-money valuation in USD millions. Say if it is pre-money |
| paying_subscribers | the numeric count of people PAYING |
| figure_dated | the date or period the count refers to |
| registered_users | the free or registered count, if also stated. Separate field, never mixed |
| subscriber_source_url | a page where the paying count and its date both appear |
| valuation_source_url | a page where the valuation appears |
| revenue_musd | only if disclosed. Leave blank otherwise, do not estimate |

## Rules, and these matter more than the number of results

1. **PAYING is the whole question.** A registered, active, downloaded or monthly-active count is NOT
   a paying subscriber count. Report it in the separate column if you have it, never in the paying
   column. A price per registered user compares a business that monetises against one that does not,
   which is the entire difference between them.
2. **Beware the businesses where the user is not the payer.** In buy-now-pay-later the merchant pays;
   in most digital banking the customer pays nothing; in ad-supported apps the advertiser pays. These
   look like large consumer bases and are not subscription comparables. Skip them.
3. **Date the figure.** It must be as close as possible to the pricing date and should be the last
   figure available BEFORE the round. If the only count you can find is after the round, say so in
   figure_dated rather than presenting it as contemporaneous.
4. **Do not back-solve.** A subscriber count derived by dividing reported revenue by an assumed price
   per seat is an inference, not a figure. I do not want it at any confidence level.
5. **No Crunchbase or PitchBook profile pages** as the sole source.
6. Fewer, better-dated rows beat more, looser ones. Tell me which companies you checked and found
   nothing for.

Return one markdown table with the columns above, then a short list of the companies you checked and
could not source.
