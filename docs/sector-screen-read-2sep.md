# Sector screen, read and written down

2 September 2026. Daniil's data dump for area 3 of `docs/data-pull-prompts-2sep.md`, the
verticals a founder cannot be priced in at all. Four photographs, transcribed to
`data/raw/2026-09-02_sector-screen.csv`. The photographs themselves are kept beside it as
`data/raw/2026-09-02_sector-screen-p01..p04.jpg`.

**Yes, I can read it.** All 51 rows, all 27 source columns, both source URLs on every row. The
sheet says 51 qualifying rounds and it has exactly 51. Nothing in it was illegible enough to
guess at, and the four photographs overlap by design so every field appears twice.

## What the sheet is

Header, quoted: *"Priced Private Funding Rounds - Sector Screen / 51 qualifying rounds |
1 Jan 2021-2 Sep 2026 | original template columns preserved / Included only where both a public
post-money valuation and a contemporaneous revenue-type figure were identified; estimates are
explicitly labelled."*

51 rounds, 41 companies, nine blocks. The blocks are not a column in the sheet, they are the
order the rows sit in. I have recorded them as `sector_block_inferred` and labelled the field as
mine, not yours, so nobody later mistakes it for something you wrote.

| Block | Rounds |
|---|---|
| Digital health | 8 |
| Energy retail | 7 |
| Agri supply chain | 6 |
| Crypto infrastructure | 6 |
| Edtech | 6 |
| Insurance | 6 |
| Gaming | 6 |
| Fitness and wellness | 4 |
| Consumer brand | 2 |

## Three columns are empty on all 51 rows

Pre-money valuation. The whole transaction-value block, all three columns. And **the implied
multiple**, which is blank on every row even though the tab is named "with Multiples". I have
carried all three as empty fields rather than dropping them, per durability rule 11, and computed
the multiples myself below.

## What actually prices

Of 51 rows:

- **32 give a multiple straight away**, valuation and denominator in the same currency.
- **11 more need an FX conversion first**: five Indian rows and five Octopus rows carry a USD
  valuation against an INR or GBP denominator, plus Voodoo which is EUR against USD.
- **8 have no denominator at all**, so no multiple can be formed from them.

Of the 32, only **21 survive a strict gate** (denominator present, same currency, not a floor,
not a forward figure, not a part-year figure annualised by us). That is the honest count of what
this sheet adds to the fixture set as it stands. (An earlier draft said 18; that gate wrongly
excluded Thirty Madison and The Zebra, whose denominators the SOURCE had already annualised.)

## The eight rows with no denominator

Two of them are deliberate and correct: Fireblocks records a reported range rather than a number,
ConsenSys records "nine figures". The other six look like omissions, because the metric column
next door holds a clean figure:

| Row | Company | Metric sitting unused |
|---|---|---|
| 33 | upGrad | RUN_RATE 165.0 USD |
| 34 | LEAD School | RUN_RATE 80.0 USD |
| 39 | EGYM | REVENUE 130.0 USD, FY2022 actual |
| 51 | Roblox | REVENUE 923.9 USD, from the audited S-1 |
| 52 | Epic Games | REVENUE 5,100.0 USD |
| 56 | Dream Sports | REVENUE 27,060.0 INR |

Roblox is the sharpest of these. Its revenue source is the SEC S-1 itself, the best-sourced
figure anywhere in the sheet, and the row produces no multiple.

## Five things to fix before this loads

**1. Two rows are the same round entered twice.**

- Alan, EUR 183m at EUR 2,700m post, ARR EUR 182m, same shareholder letter as the source, appears
  at row 27 dated 05-May-2022 and at row 50 dated 9-May-2022, filed under two different blocks.
- BetterUp, US$300m at US$4,700m post, ARR US$100m, appears at row 37 dated 2021-10-08 and at
  row 40 dated 08-Oct-2021. Same date, written two ways. Only the revenue source URL differs.

Dedupe takes the sheet to 49 distinct rounds.

**2. Discord's denominator does not match its own metric.** The metric column says REVENUE 130.0
for FY2020. The denominator column says 310.0 for FY2021. The multiple is 48.4x on the metric and
much lower on the denominator. One of the two is wrong, or the choice is deliberate and nothing
in the sheet says so.

**3. Fuse Energy carries a US$5,000m post-money on a US$70m Series B.** Neither source supports
it: one is a Goodwin mandate announcement, the other a Sifted story about the raise. Nothing there
is a valuation announcement. I have not loaded it.

**4. eFishery is in the agri block.** Its reported figures were later found to have been
fabricated by management. It must not be used as a comparable whatever the sourcing says. This
matters more than it looks, because of point 5.

**5. The two verticals with the biggest gaps depend entirely on the FX work.** Agri supply chain
has six rows, five of them USD valuation against INR revenue. Its one FX-free row is eFishery.
Energy retail has seven rows, five of them USD valuation against GBP revenue. Its two FX-free rows
are Enpal, whose denominator is a floor, and Fuse Energy. So both blocks are empty until the FX
conversion is done at the correct rate for each fiscal year.

## Nineteen rows carry a qualifier, and the qualifier changes the answer

Eleven estimates or approximations, seven floors (">"), two forward figures, two vague ranges.
A floor makes the multiple a **ceiling**, not a point. Four more rows carry a part-year
denominator against a full valuation: Devoted Health H1, wefox four months, MoonPay eleven
months, BlockFi a single month. These need annualising before they sit beside anything else, and
the annualisation is our assumption, not the sheet's.

## Computed multiples, for the record

The sheet's own multiple column is empty, so these are ours, post-money over denominator, only
where the currencies already agree.

| Block | n | Median | Range |
|---|---|---|---|
| Crypto infrastructure | 4 | 24.2x | 6.8x to 60.0x |
| Digital health | 8 | 15.8x | 7.4x to 57.1x |
| Edtech | 4 | 35.8x | 15.4x to 47.0x |
| Insurance | 6 | 11.9x | 6.7x to 22.5x |
| Fitness and wellness | 3 | 15.6x | 10.4x to 47.0x |
| Gaming | 2 | 27.3x | 6.2x to 48.4x |
| Consumer brand | 2 | 9.0x | 8.8x to 9.2x |
| Energy retail | 2 | 11.1x | 5.5x to 16.7x |
| Agri supply chain | 1 | 5.3x | one row only |

Four of the nine blocks have three rows or fewer once the currencies have to agree, and our own
rule is that we never price off one comp. Edtech, digital health, insurance and crypto are the
four that can carry a fork today. The rest need the FX work first, and after the FX work agri
gets five and energy gets seven.

## Sourcing, said plainly

22 of the 51 rows use the **same URL** for the valuation and for the revenue, which is fine when
the article carries both and worth knowing when it does not. Seven rows lean on sources we would
normally treat as tier 4 or worse:

- Virta Health and Ro: sacra.com, an estimator site.
- MasterClass: forgeglobal.com for both figures, a secondary-market marks page.
- Ninjacart: a CB Insights company page.
- Vegrow: gokulnk.com, a personal notes blog.
- Doctolib: scanfacture.fr, a French filings aggregator.
- Restore Hyper Wellness: a press index page rather than the release.
- Dream Sports: a **staging** subdomain, `staging.dreamsports.group`, not the live newsroom.

Two more sit behind a paywall (The Information, for both Epic Games rows), so we cannot verify
what they say.

## Staleness

Four rows price on a denominator more than a year older than the round: ElasticRun (Feb-2022 on
FY ended Mar-2021), Guild Education (Jun-2022 on FY2020), Epic Games (Apr-2022 on FY2020),
Celsius (Oct-2021 on FY2020). Not wrong, since the sheet records the period honestly, but they
should not be quoted to a founder as current.
