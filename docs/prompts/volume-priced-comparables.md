# Prompt: find private rounds priced on VOLUME rather than revenue

Run this in the other LLM. It is written to be pasted whole.

---

You are sourcing comparable transactions for a startup valuation engine. I need PRIVATE FUNDING
ROUNDS or ACQUISITIONS where the company was, or credibly can be, valued against a PHYSICAL OR
TRANSACTIONAL VOLUME rather than against revenue, because these businesses often disclose the
volume and not the revenue.

## What I am looking for

Companies that operate a marketplace, exchange, registry or clearing venue for a commodity or
certificate, where the value driver is the quantity transacted. Examples of the shape:

- environmental commodity exchanges and carbon credit venues (Xpansiv and its CBL exchange, AirCarbon
  Exchange, Climate Impact X, Carbonplace, ACX, Puro.earth, Ecosecurities, South Pole)
- renewable energy certificate and power purchase agreement marketplaces (LevelTen Energy, Pexapark,
  Zeigo, Flexidao, Granular Energy, EnergyTag participants)
- energy and commodity trading venues and data platforms (Enverus, Amperon, Ohm Analytics, kWh
  Analytics, Arcadia)
- any similar venue where a press release quotes tonnes, megawatt hours, certificates, barrels or
  contracts cleared, but no revenue

## For every transaction you find, give me these fields and nothing else

| field | what it must be |
|---|---|
| company | legal or trading name |
| date | the month the price was set, YYYY-MM |
| round_type | Series B, acquisition, secondary, and so on |
| post_money_musd | post-money valuation in USD millions. Say if it is pre-money |
| volume_figure | the numeric quantity |
| volume_unit | the unit exactly as stated: MtCO2e, tonnes, MWh, certificates, contracts, barrels |
| volume_period | the period it covers. A FLOW over a stated period, for example CY2021 or the twelve months to June 2022 |
| volume_source_url | a page where BOTH the figure and its period appear |
| valuation_source_url | a page where the valuation appears |
| revenue_musd | only if a revenue figure is also disclosed. Leave blank otherwise, do not estimate |

## Rules, and I care about these more than about volume of results

1. **A since-inception or cumulative total is not an answer.** "5 million tonnes cleared since
   launch" grows with age and says nothing about what the business is worth. I need a figure for a
   stated period. If the only figure available is cumulative, still report it, but put CUMULATIVE in
   the volume_period field so I can exclude it.
2. **The volume figure must be as close as possible to the pricing date**, and must be the last
   completed period BEFORE the round, not a later actual. If the only figure you can find postdates
   the round, say so in the period field.
3. **Do not convert units.** If the release says MtCO2e, write MtCO2e. Different units cannot be
   compared with each other and I need to know which one each row is in.
4. **Do not estimate, model or infer a figure.** If a market-size study times a claimed market share
   would produce a number, that is not a disclosure and I do not want it. Company statements,
   filings, and named publications reporting them only.
5. **No Crunchbase or PitchBook profile pages** as the sole source. I need the underlying
   announcement.
6. If you find fewer than ten, that is a fine answer. Tell me which companies you checked and found
   nothing for, so I do not pay to check them again.

Return one markdown table with the columns above, then a short list of the companies you checked and
could not source.
