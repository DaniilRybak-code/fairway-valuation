# The five findings, answered

3 September 2026, late. Daniil's five questions about what `check_field_reach` surfaced.

## 1 and 2. You do not need to repaste anything. Both were in the data.

**Logistics growth.** `revenue_growth_pct` is populated on **116 of the 123 rows** in
`data/peers-logistics-services.csv`. United Parcel Service 4, FedEx 4, XPO 5, GXO 5, RXO 10, and so
on down the file. The transcription was complete and correct.

The loader looked for three column names and that file uses a fourth. It reads
`revenue_growth_cagr_cy0_cy2_pct`, then `revenue_growth_cagr_cy1_cy3_pct`, then
`revenue_growth_ntm_pct`, and then gave up. Fixed. It now reads `revenue_growth_pct` as a last
resort, for DISPLAY only, and deliberately gives it no rank weight, because that file does not state
the horizon and the standing rule is that only a multi-year rate may rank a peer.

**BVPS.** `bvps_2026`, `bvps_2027` and `bvps_ntm` are each populated on **57 of the 79 rows** in
`data/peers-lending.csv`, which is every row that has a price-to-book. You were right and the file
was right.

The loader discarded the entire lending row for any ticker it had already seen in the fintech pull.
Twelve neobanks are in both files, so for all twelve the book values behind the multiples never
arrived. Now merged, and the merge covers the denominators as well as the ratios: Nu Holdings bvps
3.7 with 3.9x price to book, Klarna 7.6 with 1.9x, Inter & Co 5.4 with 1.0x, SoFi 9.5 with 2.0x.

**Both failures were in the loader, not in the data, and it is the same failure twice: a file that
spells something differently from the file the code was written against.**

## 3. Retention is in the hover table

`peer_table()` now returns exactly what you described, for every name actually in a range:

```
NAME                              MULTIPLE   GROWTH  RETENTION
Agora, Inc.                            0.8    15.0%     109.0%
Sinch AB (publ)                        1.4     2.0%          -
Twilio Inc.                            5.2    15.0%     116.0%
SoundHound AI, Inc.                   11.8    28.0%          -
Datadog, Inc.                         16.4    27.0%     122.0%
Snowflake Inc.                        17.6    28.0%     126.0%
Cloudflare, Inc.                      31.8    31.0%     120.0%
```

Every range carries it as `table`, so the reveal can render it on hover. `show_retention` is true
only where the names in front of the founder carry a retention figure, which restricts the column to
software without anything having to be kept in step with a hard-coded archetype list: browseract
gets it, an ecommerce or grocery fixture does not.

`growth_basis` travels beside growth, because the peers pulls measure growth over three different
windows. A founder comparing themselves against "26%" should be told whether that is one forward
year or a two-year compound rate.

## 4. MercadoLibre, and a second case underneath it

Both MELI rows are your own pulls, both dated 2026-08-30, both carrying an identical enterprise
value of $104,938m. They differ only on the NTM revenue:

| pull | NTM revenue | multiple |
|---|---|---|
| ecommerce | 49,038 | 2.1x |
| fintech | 46,874 | 2.2x |

**The ecommerce figure is the one that reconciles.** Both pulls agree that CY2027 revenue is 53,210,
and the ecommerce pull gives CY2026 as 41,673. Next twelve months from 30 August 2026 is four months
of 2026 and eight months of 2027, so 0.333 x 41,673 + 0.667 x 53,210 = 49,364. That is 0.7% from the
ecommerce figure and 5% from the fintech one. So 2.1x stands and the fintech NTM is the outlier.

The 26% is also right, and it is not in conflict with anything: 26% is MELI's CY+1 to CY+3 compound
rate from the ecommerce pull, and the 36% in the fintech pull is its CY+0 to CY+2 rate. Two windows
of the same company. That is why `growth_basis` now travels with every growth figure.

New tool, `tools/check_cross_pull.py`, because the peers files are refreshed from the screens, so a
note written into one would be overwritten by the next pull. It compares every shared measure across
the 20 tickers that appear in more than one pull, and tests whether each pull's enterprise value
reconciles from the bridge components that same row carries. It found something you have not seen:

**nCino is priced 13% too low right now.** Both pulls agree on market cap (2,259) and NTM revenue
(658). The fintech pull shows net debt 224 and minority interest 14, so 2,259 + 238 = 2,497, and it
ties: **3.8x**. The software pull states an enterprise value of 2,630 with no bridge components at
all, which is 371 above market capitalisation with nothing shown to explain it: **3.3x**. The engine
uses the software row. This needs your ruling: either the fintech pull wins for nCino, or we adopt
the general rule that the pull whose enterprise value reconciles from its own components wins.

## 5. Xpansiv: the volume was in the release, so it prices on its own basis

Checked, from the source already cited on the row. Xpansiv's own press release says, verbatim:

> "Total carbon offset volume transacted on CBL exceeded 121.5 MtCO2e last year, up 288% on 2020
> levels"

and gives no revenue figure anywhere. So this is the company's own disclosure of the thing an
environmental-commodity exchange is actually judged on, and your read is right. Barring it was
wrong. What was wrong about the original row is that it was labelled a multiple.

**The unit is now recorded rather than the row rejected.** `vol_unit` holds MTCO2E, MWH, KWH, GWH,
BARRELS or USD. A ratio may only be built from rows sharing a unit, and it is never written as an x.
$1,400m over 121.5 MtCO2e is **eleven dollars fifty per annual tonne of CO2 equivalent cleared**,
and that is the sentence `throughput_label()` produces. Writing it as 11.52x is what made it look
like a normal revenue multiple and nearly put it in a founder's range.

**New basis, `THROUGHPUT`**, offered on the private lane to an exchange archetype or to any founder
who answers the new question with a non-dollar unit. Xpansiv is released into the medians on that
basis. LevelTen now gets a throughput reading beside its revenue one.

**New quiz fork, `exchange`**, for Market Infrastructure & Exchange and Financial Data & Index:

- volume transacted or cleared over the last twelve months, REQUIRED, a flow and never a
  since-inception total
- the unit, REQUIRED, because it decides which comparables the founder can be shown at all and how
  their own answer is written
- net revenue, OPTIONAL, which is the reverse of every other fork and deliberate: most exchanges we
  hold disclose throughput and no revenue line

LevelTen routes here now.

**A point-in-time stock is still barred, and that is a different objection.** Flo Health and Calm
carry "millions" of users at the round date. A count of users you have is not a volume you moved
through, and a per-user figure would be a price per customer dressed up as a throughput measure.

**One thing I did not load.** The same release implies a notional dollar value: the voluntary carbon
market passed $1bn in 2021 and CBL claimed more than 41% of it by notional, which would put CBL
around $410m and give roughly 3.4x. That is a third-party market-size estimate multiplied by a
claimed share, not a disclosure, so it is recorded in the row's notes and not used.

## State

```
listed 511 | private rounds 290 | median-eligible 181
check_field_reach   PASS
check_raw_coverage  PASS
check_engine_reach  PASS   290 rows, 290 loaded, no double vote
check_cross_pull    2 companies where two of your own pulls disagree: MELI (settled above),
                    nCino (needs your ruling)
golden              0 of 43 after rebaseline
peer universe       39 of 43
```

The peer-universe gate is now basis-aware: a fixture is judged on the widest range it can be priced
on across every basis its fork supports, not on its revenue range alone. Judging a lender or an
exchange on revenue would fail companies that have a perfectly good book or throughput range and no
revenue line, which for both archetypes is the normal condition rather than an edge case.

The four that still fail are all private-side and all genuine: finn, fundraisly, levelten,
priori-legal.
