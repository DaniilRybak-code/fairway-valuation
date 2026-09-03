# Prompt: enrich the callable investor list

Paste this whole thing into the other LLM, together with the attached
`2026-09-03_investor-enrichment-targets.csv`.

---

You are completing an investor database for a startup valuation service. A founder is shown a short
list headed **"writing first cheques in your sector right now"**, and a house only appears on it
when its row is complete. **78 of our 140 callable houses are incomplete and therefore invisible to
every founder.** Your job is to complete them.

I am attaching the 78 rows. Each has `investor_key`, `investor_name`, `house_type`, what it `needs`,
and what we already hold, including `sectors_we_have_evidence_for`, which is the sectors we have
watched that house actually deal in.

## Question zero, and answer it for every house before anything else

**Does this house belong on a list of people writing FIRST CHEQUES at all?**

The list exists for founders raising roughly $0.5m to $20m. Many of the 78 arrived here because we
observed them in a late-stage round of a company in our comparables set, not because they lead early
rounds: Accel, Andreessen Horowitz, Benchmark, Bessemer, Coatue, DST Global, BlackRock, Baillie
Gifford, D. E. Shaw and others are on the list for that reason.

For each house answer `callable` or `evidence_only`:

- **callable** means it genuinely leads or co-leads pre-seed, seed or Series A rounds today, with a
  first cheque a founder in that range could receive.
- **evidence_only** means it is a real and relevant investor but a growth or crossover house. It
  stays in our database as part of "the houses behind your reference rounds" and comes off the call
  list.

Getting this right matters more than filling every field. A seed founder told to call Benchmark is
worse served than one shown six houses that actually write their cheque.

## For every house you mark `callable`, fill these

| field | what it must be |
|---|---|
| `first_cheque_low_m` | the low end of the typical FIRST cheque, in USD millions. 0.25 means $250k |
| `first_cheque_high_m` | the high end, USD millions. Leave blank if only one figure is stated |
| `cheque_currency` | USD, GBP or EUR: the currency the source states, before any conversion |
| `geographies` | where they invest, semicolon separated. Use country or region names as they state them: UK; Europe; US; Global; MENA; India; Southeast Asia. **"Global" is a real answer** and must not be used as a shrug |
| `stage_bands` | semicolon separated from exactly this list: Pre-seed; Seed; Series A; Series B; Series C |
| `thesis_one_liner` | one sentence, in their words where possible, saying what they back. No adjectives we would not put in front of a founder |
| `cheque_range_source` | the URL where the cheque range is stated |
| `geographies_source` | the URL where the geography is stated |

## Rules, and they matter more than coverage

1. **Every figure needs a URL where it actually appears.** The fund's own site, its published
   investment criteria, a named publication, or a fund announcement. A number with no source does
   not go in the file: in this project a figure with no source does not exist.
2. **Do not estimate a cheque size.** If a fund does not state one, leave both cheque fields blank
   and write `NOT STATED` in `cheque_range_source`. That is a useful answer. An invented range would
   put a house in front of a founder raising the wrong amount, which is the exact failure this list
   exists to avoid.
3. **Public information only.** Nothing behind a login, no scraping of gated databases, and **no
   contact details of any kind**: no names of partners, no emails, no phone numbers. We publish a
   map, not an introduction.
4. **Do not convert currency.** Record what the source says and which currency it is in.
5. **A fund's own "investment criteria" or "what we back" page beats a press profile**, and both
   beat an aggregator. Do not use Crunchbase or PitchBook profile pages as a sole source.
6. If a fund has raised no new vehicle and shows no new investment since 2024, say so in a
   `dormant_note` column rather than filling the row. A stale house on a call list is the single
   failure mode we are most trying to avoid.
7. Where the fund states a cheque range for a specific programme (an accelerator cheque, an EIS
   fund, a regional co-investment fund), record THAT range and name the programme in
   `cheque_range_source`. Several of these houses deploy several vehicles with very different sizes.

## Output

One CSV, with a header, these columns exactly and in this order:

```
investor_key,investor_name,verdict,first_cheque_low_m,first_cheque_high_m,cheque_currency,
geographies,stage_bands,thesis_one_liner,cheque_range_source,geographies_source,dormant_note
```

`verdict` is `callable` or `evidence_only`. One row per input row, including the ones you mark
`evidence_only` (leave their other fields blank). Keep `investor_key` exactly as given: it is how
the file is joined back and a changed key silently drops the row.

At the end, outside the CSV, give me three short lists: houses you marked `evidence_only` and why in
five words each; houses where no cheque range is published anywhere; and any house you believe is
dormant.
