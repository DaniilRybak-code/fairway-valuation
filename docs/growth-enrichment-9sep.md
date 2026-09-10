# Growth enrichment of the private rounds, 9 September 2026

**Written by Fable on 9 September 2026 against origin `main` at `18672d8`, from the work order
`docs/prompts/growth-enrichment-9sep.md`. Every number below reproduces from
`python3 tools/load_growth_enrichment_9sep.py` and from the raw file it reads.**

## In one paragraph

163 private rounds priced a founder's range with no growth figure. Every one of the 163 now ends
in one of two states: 97 carry a year-on-year revenue growth rate with the page it was read from and
the sentence quoted, and 66 carry a reason in plain words why no usable rate exists on a readable
page. The 97 were written into the three growth columns that already existed, on the 97 rows that
were empty, and nothing else in either file changed: 320 rows in, 320 out, and the loader checks
every other byte. Growth coverage on rounds that price a founder's range goes from 56 of 219 to
153 of 219. Twenty checks pass. Golden did not move (0 of 142), because the test companies carry no
growth rate and growth only acts once a founder supplies one. The gate is 124 of 142 before and
after.

## The thresholds I used, and a mistake in the work order

The work order's table says MATURE below 65 and HYPER above 162. The code says otherwise, and the
order told me to trust the code: `selector/match_reference.py` has `BAND_LOW, BAND_HIGH = 77.0,
206.0`, fitted on 27 August on 51 rounds. So a round is MATURE below 77 per cent, GROWING from 77
to 206 inclusive, and HYPER above 206. The loader imports `band_of` from the code rather than
carrying its own copy, and refuses to write a row whose band in the raw file disagrees with the
code. The table in the order should be corrected. The same code comment says to rerun
`tools/refit_growth_bands.py` when coverage grows materially; it has grown from 73 rounds with a
figure to 170, and I have not rerun it, because that changes the bands for every row and is a
ruling, not an enrichment.

## What closed, and on what basis

| | rounds |
|---|---|
| Found and loaded | 97 |
| DISCLOSED (the company or the round announcement states the rate) | 46 |
| THIRD_PARTY_DATED (a credible third party states it, or the source is more than about nine months from the round) | 25 |
| DERIVED (computed from two figures on the same measure, arithmetic in the raw file) | 18 |
| STATED (a founder or executive says it in an interview, nothing filed behind it) | 8 |
| Not found | 66 |

Bands of the 97: MATURE 38, GROWING 43, HYPER 16.

20 of the 97 are floors. The source says "more than doubled" or "over 50%" and the file records the
floor, 100 or 50, exactly as it already did for Glossier, TravelPerk, Outreach and Ramp. Each floor
is marked `growth_is_floor = yes` in the raw file so a later pass can tighten it. A floor can put a
round one band too low; that is the known cost of the convention and it is the file's, not mine.

## Decisions I made that touch the order, each reversible in one line

These are the places where the order, the file's own conventions and the sources pulled in
different directions. I followed the file's conventions and named every row, so you can strike any
group by transaction id.

1. **"Revenue" wording on a row that prices on ARR or a run rate.** The order says an ARR row needs
   ARR growth. The file already accepts a company saying "revenue grew 3x" in the same breath as its
   ARR (Scale AI, Salesloft, Loft, Apollo). I did the same, and the raw file's `growth_measure_seen`
   column says what the source actually called it. Rows where the wording is "revenue" on an ARR or
   run-rate row (17): 6sense-2022-01, betterup-2021-10, brex-2022-01, calm-2019-02, calm-2019-07,
   cityblock-health-2021-09, contentsquare-2022-07, databricks-2023-09, deel-2025-10,
   fireblocks-2022-01, moss-2026-08, plaid-2025-04, spendesk-2022-01, the-zebra-2021-04,
   thirty-madison-2021-06, upgrad-2021-08, vedantu-2021-09. Three more use a quarter's revenue growth against the same
   quarter a year earlier, which is the growth of the run rate the row prices on:
   airwallex-2021-11, creditas-2022-01, mambu-2021-12. Bookings, GMV, volume and user growth were
   never accepted.

2. **Two rows where the sentence does not name what grew.** jobandtalent-2021-12 ("Its business
   growth rate is 130% annually") and mews-2026-01 ("The company grew at over 50% year-on-year",
   in a sentence that also gives the revenue). I recorded both on the ordinary reading that a
   company's growth rate is its revenue growth, and marked them `MEASURE NOT NAMED` in the notes.
   Strike them if you read it differently.

3. **Estimator figures were held out.** Five candidates rest only on Sacra estimates. Earlier
   sessions loaded two Sacra figures (Writer, Snyk), but the order says a credible third party and a
   founder would be banded against an estimate presented as fact. Held out, recorded as not found
   with the figure in `seen_not_loaded`: skims-2023-07 (50, 2023 vs 2022), suno-2025-11 (404.4,
   and Sacra's own sentence contradicts its table), mercury-2025-03 (97, 2024 vs 2023). For
   betterup-2021-10 and oura-2024-12 the company's own floor at the round ("more than doubled")
   was used instead of Sacra's 127 and 53.

4. **One two-year average, annualised.** carta-2021-08: ARR "around $150 million, up from $50
   million two years ago" (The Information, Feb 2021). Annualised geometrically to 73.2 a year, as
   the file does for Guesty and Apollo. It is an average, not a last-twelve-months rate.

5. **One window that is not twelve months, annualised.** canva-2025-08: the source says 50 per cent
   "in just over a year", $3.3bn in July 2025 against $2.2bn in May 2024, fourteen months.
   Annualised to 41.6, as the file does for Moove and Vinted. Canva's own May 2024 release said
   "more than $2.3 billion", which would give at most 36.3. MATURE either way.

6. **The nine-month rule.** Where the only figure sits more than about nine months from the round
   the basis is THIRD_PARTY_DATED and the gap is in the notes: revolut-2021-07 (annual report
   signed 20 months after), raisin-2023-03 (14 months, but the row itself prices on FY2023),
   pinelabs-2021-05 (14), checkoutcom-2023-12 (13), zepz-2021-08 (13), chime-2024-04 (13),
   mollie-2021-06 (12), epic-games-2022-04 (11, and the growth period ends 16 months before the
   round), restore-hyper-wellness-2021-12 (10 months before), mews-2026-01 (10 months before).

7. **One journalist's inference rejected.** ramp-2021-08: TechCrunch quotes the CEO on
   transaction volume up 1,000 per cent and adds that revenue rose "by the same amount" because of
   the business model. The revenue sentence is the journalist's, not the CEO's, so it is not found.

8. **One aggregator-grade source loaded and flagged.** shein-2023-05: 44.6 from the Business of
   Apps statistics table (2021 $15.7bn, 2022 $22.7bn, citing Daxue, Forbes and the FT). The primary
   pages were blocked or paywalled. The row's own $22.7bn matches the table. Basis
   THIRD_PARTY_DATED, notes say AGGREGATOR.

9. **One bookings line, loaded because it is the line the row prices on.** whoop-2026-03: the
   company's release says "bookings grew 103% year-over-year, exiting the year at a $1.1B run
   rate", and the row's $1,100m ARR_RUNRATE is that same bookings run rate. The growth is of the
   exact line the row holds, so it was loaded, and the basis mislabel is flagged below. If the
   basis audit strikes the revenue, this goes with it.

10. **One period not confirmed.** monzo-2024-05: 147.5 from Monzo's own report page (FY24 £880.0m
    against FY23 £355.6m). Monzo moved its year end from February to March in that year, so FY24 may
    be thirteen months; the PDF is robots-blocked and no readable page says. If it is thirteen
    months the twelve-month equivalent is about 128. GROWING either way.

11. **`STATED` is now in use.** The file carried no row on that basis before today. Eight rows use
    it, all executive statements in interviews with no filing or release behind them: blockworks,
    brex-2022-01, fireblocks (both), incrediblehealth, perplexity, spendesk, vedantu.

## What I touched, and what I did not

Written: `data/raw/2026-09-09_private-growth-enrichment.csv` (163 rows, every target column plus
the source URL, the quote, the arithmetic, the source date, what the source called the measure,
whether it is a floor, figures seen but not loaded, flags and notes), the filled work list
`docs/growth-enrichment-targets-9sep.csv`, `tools/load_growth_enrichment_9sep.py`, one row in
`data/MANIFEST.md`, and this document.

Changed in the data: the three growth columns on 92 rows of `data/private-rounds.csv` and 5 rows of
`data/private-rounds-consumer.csv`. The loader re-reads both files after writing and compares every
line: the 97 loaded lines differ in those three columns only, and the other 223 lines are byte for
byte the same. I also diffed the files independently of the loader and got the same answer. Run it
a second time and it reports 0 loaded, 97 already loaded, 0 refused. Give it a raw figure for a row
that already carries a different figure and it refuses and names the row (tested on a copy).

One line outside the order: `tools/check_intake.py` now knows that the raw file's identifying
columns are `company_key` and `company_name`, so check 1 reports it INGESTED (159 of 159 names)
instead of PARTIAL. Without that line the check samples the first four columns, one of which is
`transaction_id`, and reports a problem where there is none. Nothing else in the tools changed.

Not touched, on purpose: every revenue figure, basis, date, note and multiple, including the ones
listed under "looks wrong" below.

## Gate, golden, and what the enrichment does once a founder supplies a growth rate

`python3 tools/peer_universe_check.py`: 124 of 142 before, 124 of 142 after, the same 18 failures
for the same reasons. Golden: 0 of 142 profiles moved, so no rebaseline and no attribution file.
That is expected rather than disappointing: `band_compatible` gates the private lane only when the
founder has a growth band, and the 142 test companies carry no growth rate (rule E9: fixtures carry
no figures). Growth on a round does nothing until a founder's growth arrives with the quiz.

To show what it will do, I ran a read-only probe outside the repo: every fixture, with a founder
growth of 40, 120 and 300 per cent, against the files before and after the load, 426 lanes each
way. 91 lanes on 69 fixtures pick a different private set after the load: 34 fixtures at 40 per
cent, 11 at 120, 46 at 300. Two examples. A founder growing 40 per cent who matched anysearch used
to be shown Perplexity (now HYPER at 530 and excluded) and is shown Weights & Biases instead. A
founder growing 300 per cent who matched 99minutos used to be shown Xpressbees and Delhivery, both
now MATURE at 33 and 31 and excluded, and the lane shrinks from five names to three. That second
example is the rule working and the pool being thin, not a fault in the data, but it is worth
knowing that band gating can now shorten lanes that were full only because their growth was blank.

## Every row that did not close, and why

Plain words here; the full reason, every page tried and any figure seen on a different measure or
date are in the raw file's `not_found_reason` and `seen_not_loaded` columns.

| round | why it did not close |
|---|---|
| alan-2022-05 | The Q1 2022 letter gives ARR of EUR182m with no prior-year comparison; a year earlier Alan said only "over EUR100m", a bound, so no rate. |
| alphasense-2022-06 | Series D release gives user and customer growth only; ARR is a bound, so nothing to derive. |
| alphasense-2023-09 | Series E coverage gives no ARR rate; the only later figure is an 18-month doubling (summer 2022 to end 2023). |
| anthropic-2024-01 | No public run-rate exists for January 2023 to set against the $87m the row holds; Claude launched in March 2023. |
| anysphere-cursor-2025-06 | Only sub-year comparisons exist (vs mid-April 2025, doubling every two months); ARR is a bound, so nothing derived. |
| away-2019-05 | Row prices on FY2018 revenue; no page gives FY2017 revenue or the FY2018 rate (only 2017 vs 2016, and a 2019 forecast). |
| blockchaincom-2022-03 | Row source returns 404; round coverage gives valuation only; Fortune gives $1.5bn "year to date" with no prior year. |
| brex-2021-10 | Row source returns 404; the only statement is "on track to double revenue this year" from unnamed sources, a forecast. |
| buffer-2014-10 | The October 2013 base was a bookings-inflated run rate by Buffer's own admission, so it cannot be set against the MRR-based ARR of October 2014. |
| bvnk-2024-12 | Only payments-volume growth published (200 per cent); no revenue rate. |
| canva-2024-05 | Bound row; the only rate is "nearly 50%" in a newsletter with no period, which is not a stated rate. |
| chainalysis-2022-05 | Series F release gives customer-count growth and a regional statement only; Sacra places $190m ARR in 2023, not 2022 (flagged below). |
| cohere-2023-06 | Cohere published no revenue in June 2023; the row's own source page has no revenue figure at all (flagged below). |
| consensys-2022-03 | Only "nine figures" of 2021 revenue, a bound; no growth rate anywhere readable. |
| floqast-2024-04 | Only a Deloitte three-year figure (409 per cent, fiscal 2020 to 2023) on revenue, not ARR, ending well before the round. |
| framer-2025-08 | Only the $50m ARR level and a $100m target; no prior-year ARR. |
| fundbox-2021-11 | Bound row; the round sources give customer-acquisition growth only. |
| gamma-2025-11 | Bound row; the $100m ARR release and coverage state no rate; earlier milestones have no dates. |
| genspark-2025-11 | The company reached $50m run rate within five months of launch; there is no year-earlier base. |
| glean-2025-06 | Bound row; the $100m ARR release gives customer doubling only; the only rate is a Sacra estimate for a later period. |
| gorillas-2021-10 | Founded mid-2020; no year-earlier run rate exists, and the sources give monthly growth only. |
| guild-education-2022-06 | Forbes says Guild does not disclose revenues; only user growth is given. |
| happy-money-2022-02 | Only originations growth published (42 per cent average), not revenue. |
| klaviyo-2021-05 | The S-1 starts at 2021; no FY2020 revenue on any readable page, so the FY2021 rate cannot be built. |
| konfio-2021-09 | VEF's slides carry no readable revenue text; round coverage gives loan-book and user growth only. |
| loadsmart-2020-11 | Bound row; the sources give year-to-date growth ("250% since January 2020") and a Q4-only rate, not 2020 over 2019. |
| lovable-2025-12 | Launched November 2024; no ARR twelve months before the round on any page, only milestones within 2025. |
| masterclass-2021-05 | Round coverage gives content and headcount growth and a "tenfold" weekly anecdote; the row's source page has no revenue at all (flagged below). |
| mercor-2025-02 | Only a month-on-month rate and an ARR level at the round; the only annual figures are an anonymous newsletter and Sacra. |
| mercury-2025-03 | Estimator only (Sacra 97 per cent, 2024 vs 2023); held out for your ruling. |
| moonpay-2021-11 | Only transaction-volume growth (35x) and month-on-month revenue growth; no 2020 revenue. |
| n26-2021-10 | Row source returns 404 and N26 no longer lists 2021 releases; TechCrunch gives transaction volume only. |
| notion-2026-01 | Row source (Forbes) returns 403 on every route; bound row, so only a stated rate would do. |
| nubank-2021-06 | The F-1 is too large to read here; the readable part gives FY2020 and LTM Sep-2021 revenue, nine months apart, no FY2019. |
| olivejune-2024-12 | Helen of Troy gives a 2019 to 2023 CAGR and an approximate 2024 figure, no 2023 net sales. |
| oxylabs-2026-07 | Bootstrapped until this round; every source gives the $350m ARR level only. |
| patreon-2021-04 | Bound row; The Information is paywalled and the release gives creator payouts, not revenue. |
| plaid-2021-04 | Row source returns 404; round coverage gives customer growth (60 per cent) only. |
| pleo-2021-12 | Row source returns 404; round coverage gives customer counts; the only rate is from 2023. |
| qonto-2022-01 | Row source returns 404; Qonto's own Series D release PDF is robots-blocked; TechCrunch gives client count only. |
| quince-2026-03 | No source URL on the row; Bloomberg and WSJ blocked; only Sacra run-rate estimates, which are not FY net revenue. |
| ramp-2021-08 | The stated 1,000 per cent is transaction volume; the revenue sentence is the journalist's inference. |
| ramp-2025-07 | Only point-in-time run rates 17 months apart and customer growth; no twelve-month rate. |
| remote-2022-04 | Row source returns 404 and every guessed page failed; nothing readable. |
| restaurant365-2023-05 | The release says only "crossed $100M in revenue"; bound row, no rate. |
| ro-2021-03 | Forbes gives an estimated 2020 gross revenue only; Sacra's rate is for 2021, after the round. |
| roblox-2021-01 | The row's S-1/A link returns 404 and EDGAR search is blocked; the Nov 2020 S-1 gives 2019 on the pre-restatement basis, which cannot be set against the restated $923.9m. |
| sierra-2026-05 | Milestones only ($100m ARR Nov 2025, over $150m Feb 2026); the year-earlier base exists only as a Sacra estimate. |
| skims-2023-07 | Estimator only (Sacra 50 per cent); held out for your ruling. |
| skims-2025-11 | Only a 2022 to 2024 CAGR and a "over $1 billion" 2025 projection; NYT and Reuters blocked. |
| stockx-2021-04 | No source URL on the row; the search allowance ran out before this row and guessed pages failed. Should be retried with search. |
| strava-2025-05 | WSJ blocked; The Information paywalled; only a headline "50%+" on revenue eight months after the round. |
| stripe-2023-03 | No readable page gives 2022 net revenue or its growth; the row's own $4.1bn could not be corroborated (flagged below). |
| stripe-2024-02 | No readable page gives 2023 net revenue growth; The Information paywalled; the row's $5.6bn looks inconsistent (flagged below). |
| sumup-2022-06 | Row source times out or 404s; nothing else readable for June 2022. |
| suno-2025-11 | Estimator only, and Sacra's sentence contradicts its own table; held out. |
| supabase-2025-10 | Row source (The Information) paywalled; Sacra's 232 per cent has no stated base period. |
| vanta-2024-07 | Bound row; the Series C post gives customer doubling only. |
| vention-2026-01 | Only a segment rate (physical AI up 400 per cent) and revenue levels that disagree with each other (flagged below). |
| vercel-2024-05 | Every source gives the "over $100 million" level only. |
| virta-health-2021-04 | Row source (Sacra) gives an estimated 2021 revenue with no 2020 figure; no round-era page reachable. |
| voodoo-2021-08 | Row source gives "reportedly $400 million in 2020" only, and does not carry the $336.9m the row holds (flagged below). |
| wefox-2021-05 | No 2019 revenue on any readable page; 2020 is $140m. |
| wiz-2024-05 | Only the $350m ARR level and a $1bn target; no year-earlier figure. |
| yotpo-2021-03 | Only product-line growth (SMS 170 per cent, loyalty doubled), not company ARR. |
| zopa-2021-10 | Only the run rate and a forecast to double by 2022; Zopa's newsroom unreachable. |

About twenty of these were researched after the session's search allowance ran out, so they rest
on direct page reads only and may close with a search: notion, quince, stockx, vercel, cohere,
masterclass, plaid-2021, remote, skims-2025, virta, mercor, qonto, zopa, sumup-2022, voodoo,
restaurant365, wiz, pleo, wefox-2021-05, roblox, nubank, n26, klaviyo, stripe-2023, stripe-2024.

## What looks wrong and was not touched

Flagged, not fixed. Each is in the raw file's `flags` column against its row. The basis audit is
separate work and this order did not touch it.

**Revenue figures that contradict the page they cite or the growth source**

- turing-2025-03: row holds $167m ARR "at pricing"; its own source says $300m ARR (January 2025), and the 200 per cent attaches to the $300m.
- stripe-2025-02: row holds $5.6bn net revenue; The Information via Axios says 2024 revenue was $5.1bn after 28 per cent growth. The same $5.6bn sits on stripe-2024-02, so one of the two years is mislabelled. stripe-2023-03's $4.1bn could not be corroborated on any readable page.
- zepz-2021-08: row holds $338m "FY2021 revenue as stated in the round announcement"; the company's own release says 2020 $238m, 2021 $399m. Neither is $338m.
- deel-2022-05: row holds $295m ARR for a May 2022 round; that is Deel's end-2022 figure, published January 2023. At the round the disclosed ARR was "crossed $100 million" (April 2022).
- mercury-2025-03: row holds $650m annualized revenue; that is the September 2025 figure. At the March 2025 round the company said $500m revenue for 2024, which would make the multiple about 7.0x, not 5.4x.
- fireblocks-2022-01: row holds $100m ARR at January 2022; the CEO said 2021 revenue was $60m and the company announced passing $100m ARR in September 2022.
- alan-2024-09: row holds EUR450m forward ARR; Alan's own Q4 letter says year-end 2024 ARR was over EUR500m.
- egym-2023-07: row holds $119.8m; the source says $130m in revenues in 2022 (the growth is on the $130m line).
- klarna-2021-03: row holds $1,187.3m; the release says US$1.087bn (SEK 10bn), the same SEK figure at a different exchange rate.
- juspay-2026-01: row prices on INR 514 crore (the company release); Entrackr's filed figure is INR 540 crore.
- canva-2024-05: row holds $2,200m; Canva's own release says "more than $2.3 billion".
- vention-2026-01: the company's October 2025 release says $60m annual revenue; The Logic in January 2026 has the CEO at "just under $100 million".
- voodoo-2021-08: row holds $336.9m; its own source says "reportedly $400 million in 2020".
- brex-2022-01: the $312m annualized revenue does not appear on the row's source page; Sacra attaches it to end-2022.
- ramp-2021-08: row holds $100m annualized revenue at August 2021; TechCrunch (March 2025) says Ramp crossed $100m "before its third birthday in March 2022".
- ramp-2025-07: the $700m is a January 2025 figure reused for a July 2025 round; by September the company reported $1bn.
- chainalysis-2022-05: Sacra places $190m ARR in 2023 and about $140m in 2022; the row holds $190m at May 2022.
- oura-2024-12: row prices a December 2024 round on Sacra's FY2023 estimate ($225m) while the company said revenue had more than doubled in the year to the round.
- mollie-2021-06: row holds $120m annual revenue at June 2021; Dutch filings coverage gives EUR59m for 2020 and just over EUR97m for 2021.
- dream-sports-2021-11: the FY20 base in the FY21 filing (INR 1,670 crore) differs from Entrackr's earlier FY20 article (INR 2,070 crore); on the unrestated base FY21 growth would be about 23 per cent, not 53.
- blockchaincom-2022-03: the $1.5bn is Fortune's "year to date" figure from mid-October 2021, labelled LTM on a March 2022 row.
- guild-education-2022-06: the $100m ARR is Forbes' figure "for 2020", eighteen months before the round.
- epic-games-2022-04: an April 2022 round priced on FY2020 revenue; The Information briefing the row cites said Epic projected 2020 revenue 36 per cent below 2018, which does not match the $5.1bn.
- cohere-2023-06, masterclass-2021-05, nubank-2021-06: the row's cited source page contains no revenue figure at all.
- restore-hyper-wellness-2021-12: a December 2021 round priced on calendar 2020 revenue; the round release says 2021 system-wide sales grew 158 per cent, so the multiple is on stale revenue.
- revolut-2023-11 and revolut-2025-11: each prices on a fiscal year that had not closed at the round (FY2023 published July 2024; FY2025 published March 2026). Same for chime-2024-04 (FY2024 revenue on an April 2024 round).

**Currency carried over unconverted, or figures in the wrong unit**

- revolut-2021-07: 636.0 "musd" is GBP636m (FY2021 revenue in pounds).
- starling-bank-2021-03: 145.0 is the source's "c.£145 million".
- atombank-2023-11: 76.0 is GBP76m of net interest income, not gross revenue and not dollars; a BANK_NOI basis would fit.
- enpal-2023-01: 400.0 is "more than 400 million euros".
- doctolib-2022-03: 181.3 is EUR181m.
- blockfi-2021-03: the $50m the row prices on as LTM gross revenue is called "monthly revenue" by both TechCrunch and BlockFi's own release; taken literally the annual figure is about $600m and the 60x multiple about 5x.
- devoted-health-2021-10: the $247.3m is six-month revenue (January to June 2021), labelled LTM.

**Basis that looks mislabelled**

- whoop-2026-03: the $1.1bn ARR_RUNRATE is a bookings run rate in the company's own words.
- VEGROW-2023-12: Entrackr calls the INR 361 crore both "gross revenue" and "GMV"; the row calls it revenue from operations.
- packable-2021-09: labelled GROSS_REVENUE; Packable's later 8-K calls the line "net revenue".
- better-2021-05: labelled net revenue; the deck says "Revenue" with no definition.
- olivejune-2024-12: labelled GROSS_REVENUE; the source says "net sales revenue".
- harrys-2021-03, rapyd-2021-01: sources say "sales", gross or net not stated.
- restaurant365-2023-05: labelled ARR; the release says "$100M in revenue".
- huel-2022-11: labelled NET_REVENUE; sources say "revenue" or "sales".
- canva-2024-05: an annualised run rate labelled NET_REVENUE with period RUN_RATE.

**Bounds not marked as bounds**

Revenue is a floor in the source but `revenue_metric` does not say so: aledade-2023-06 ("more than
$475 million"), blockworks-2023-05 ("significantly exceeded" $20m), alan-2026-06 ("more than EUR800
million"), happy-money-2022-02 ("over $100M"), vercel-2024-05 ("exceeded $100 million"),
consensys-2022-03 ("nine figures"), strava-2025-05 ("nears $500M"), skims-2025-11 ("over $1
billion"), yotpo-2021-03 ("exceeded $100 million"), blockfi-2021-03 ("over $50 million").

**Source links on the rows that no longer resolve**

airwallex-2025-12, canva-2024-05, carta-2021-08, chainalysis-2021-06, chime-2021-08,
contentsquare-2022-07, creditas-2022-01, deel-2022-05, fireblocks (both), mambu-2021-12,
mollie-2021-06, n26-2021-10, plaid-2021-04, pleo-2021-12, qonto-2022-01, remote-2022-04,
revolut-2024-08, revolut-2023-11, revolut-2021-07, roblox-2021-01, spendesk-2022-01,
stripe-2023-03, sumup-2022-06, vercel-2024-05, wefox-2022-07 (404 or timeout); economictimes
(dehaat, vedantu), Reuters, WSJ, NYT and The Verge are blocked from this session; Forbes and CNBC
often return 403; scanfacture.fr, sec.gov cgi-bin and Monzo's PDF are robots-blocked. Where a live
copy of the same release existed, the raw file cites it.

## Every row that was loaded

Source column is the site the sentence was read on and the date of that page; the full URL and the
verbatim sentence are in the raw file. Quotes in the raw file are copied exactly as the page prints
them, including the page's own punctuation.

| round | date | prices on | growth % | band | basis | floor | where it came from |
|---|---|---|---|---|---|---|---|
| 6sense-2022-01 | 2022-01 | ARR_RUNRATE | 100 | GROWING | DISCLOSED | yes | prnewswire.com (2022-03) |
| airwallex-2021-11 | 2021-11 | ARR_RUNRATE | 165 | GROWING | DISCLOSED |  | airwallex.com (2021-11) |
| airwallex-2025-12 | 2025-12 | ARR_RUNRATE | 90 | GROWING | DISCLOSED |  | airwallex.com (2025-12) |
| alan-2024-09 | 2024-09 | ARR | 48 | MATURE | DISCLOSED |  | alan.com (2025-01) |
| alan-2026-06 | 2026-06 | ARR | 53 | MATURE | DISCLOSED |  | prnewswire.com (2026-06) |
| aledade-2023-06 | 2023-06 | GROSS_REVENUE | 50 | MATURE | DISCLOSED | yes | aledade.com (2023-06) |
| algolia-2021-07 | 2021-07 | ARR | 180 | GROWING | DISCLOSED |  | techcrunch.com (2021-07) |
| atombank-2023-11 | 2023-11 | GROSS_REVENUE | 61 | MATURE | DERIVED |  | atombank.co.uk (2023-07) |
| auditboard-2024-05 | 2024-05 | ARR | 40 | MATURE | THIRD_PARTY_DATED |  | hgcapital.com (2024-09) |
| better-2021-05 | 2021-05 | NET_REVENUE | 884 | HYPER | DISCLOSED |  | sec.gov (2021-05) |
| betterup-2021-10 | 2021-10 | ARR | 100 | GROWING | DISCLOSED | yes | betterup.com (2021-07) |
| blockfi-2021-03 | 2021-03 | GROSS_REVENUE | 3233.3 | HYPER | DERIVED | yes | techcrunch.com (2021-03) |
| blockworks-2023-05 | 2023-05 | GROSS_REVENUE | 100 | GROWING | STATED | yes | axios.com (2023-05) |
| brex-2022-01 | 2022-01 | ARR_RUNRATE | 100 | GROWING | STATED | yes | techcrunch.com (2022-01) |
| calendly-2021-01 | 2021-01 | NET_REVENUE | 100 | GROWING | THIRD_PARTY_DATED |  | siliconangle.com (2021-01) |
| calm-2019-02 | 2019-02 | ARR_RUNRATE | 300 | HYPER | DISCLOSED |  | globenewswire.com (2019-02) |
| calm-2019-07 | 2019-07 | ARR_RUNRATE | 300 | HYPER | DISCLOSED |  | beautymatter.com (2019-07) |
| canva-2025-08 | 2025-08 | ARR_RUNRATE | 41.6 | MATURE | DERIVED |  | capitalbrief.com (2025-07) |
| carta-2021-08 | 2021-08 | ARR | 73.2 | MATURE | THIRD_PARTY_DATED |  | news.fintech.io (2021-02) |
| chainalysis-2021-06 | 2021-06 | ARR | 100 | GROWING | DISCLOSED | yes | cnbc.com (2021-03) |
| checkoutcom-2023-12 | 2023-12 | GROSS_REVENUE | -14 | MATURE | THIRD_PARTY_DATED |  | paymentexpert.com (2025-01) |
| chime-2021-08 | 2021-08 | GROSS_REVENUE | 200 | GROWING | THIRD_PARTY_DATED | yes | cnbc.com (2021-08) |
| chime-2024-04 | 2024-04 | GROSS_REVENUE | 30.9 | MATURE | THIRD_PARTY_DATED |  | sec.gov (2025-05) |
| cityblock-health-2021-09 | 2021-09 | ARR_RUNRATE | 100 | GROWING | DISCLOSED | yes | fiercehealthcare.com (2021-09) |
| contentsquare-2022-07 | 2022-07 | ARR | 100 | GROWING | DISCLOSED | yes | contentsquare.com (2022-07) |
| creditas-2022-01 | 2022-01 | ARR_RUNRATE | 233 | HYPER | DISCLOSED |  | techcrunch.com (2022-01) |
| databricks-2023-09 | 2023-09 | ARR_RUNRATE | 50 | MATURE | DISCLOSED | yes | databricks.com (2023-09) |
| deel-2022-05 | 2022-05 | ARR | 417.5 | HYPER | DISCLOSED |  | techcrunch.com (2023-01) |
| deel-2025-10 | 2025-10 | ARR_RUNRATE | 75 | MATURE | DISCLOSED |  | businesswire.com (2025-06) |
| dehaat-2022-10 | 2022-10 | GROSS_REVENUE | 255.6 | HYPER | DERIVED |  | entrackr.com (2022-11) |
| delhivery-2021-05 | 2021-05 | NET_REVENUE | 31.1 | MATURE | DERIVED |  | entrackr.com (2021-11) |
| devoted-health-2021-10 | 2021-10 | GROSS_REVENUE | 128 | GROWING | THIRD_PARTY_DATED |  | medcitynews.com (2021-10) |
| discord-2021-09 | 2021-09 | GROSS_REVENUE | 188.9 | GROWING | DERIVED |  | gamesbeat.com (2021-03) |
| dlocal-2021-04 | 2021-04 | NET_REVENUE | 88.4 | GROWING | DISCLOSED |  | sec.gov (2021-05) |
| doctolib-2022-03 | 2022-03 | GROSS_REVENUE | 69.8 | MATURE | THIRD_PARTY_DATED |  | pappers.fr |
| dream-sports-2021-11 | 2021-11 | GROSS_REVENUE | 53 | MATURE | THIRD_PARTY_DATED |  | entrackr.com (2022-04 | 2022-06) |
| egym-2023-07 | 2023-07 | GROSS_REVENUE | 70 | MATURE | DISCLOSED |  | techcrunch.com (2023-07) |
| elasticrun-2022-02 | 2022-02 | GROSS_REVENUE | 114 | GROWING | THIRD_PARTY_DATED |  | entrackr.com (2022-03) |
| enpal-2023-01 | 2023-01 | GROSS_REVENUE | 277 | HYPER | DISCLOSED |  | corporate.enpal.com (2023-07) |
| epic-games-2021-04 | 2021-04 | GROSS_REVENUE | 21.4 | MATURE | DERIVED |  | techmeme.com (2021-05) |
| epic-games-2022-04 | 2022-04 | GROSS_REVENUE | 21.4 | MATURE | THIRD_PARTY_DATED |  | techmeme.com (2021-05) |
| fireblocks-2021-07 | 2021-07 | ARR | 350 | HYPER | STATED |  | techcrunch.com (2021-07) |
| fireblocks-2022-01 | 2022-01 | ARR | 600 | HYPER | STATED | yes | algemeiner.com (2022-01) |
| gopuff-2021-07 | 2021-07 | NET_REVENUE | 200 | GROWING | THIRD_PARTY_DATED | yes | theinformation.com (2021) |
| harrys-2021-03 | 2021-03 | NET_REVENUE | 25 | MATURE | THIRD_PARTY_DATED |  | forbes.com (2021-03) |
| huel-2022-11 | 2022-11 | NET_REVENUE | 40 | MATURE | DISCLOSED |  | highlandeurope.com (2022-12) |
| incrediblehealth-2022-08 | 2022-08 | GROSS_REVENUE | 500 | HYPER | STATED |  | forbes.com (2022-08) |
| jobandtalent-2021-12 | 2021-12 | GROSS_REVENUE | 130 | GROWING | DISCLOSED |  | techcrunch.com (2021-12) |
| juspay-2026-01 | 2026-01 | GROSS_REVENUE | 61 | MATURE | DISCLOSED |  | juspay.io (2025-11) |
| klarna-2021-03 | 2021-03 | BANK_NOI | 40 | MATURE | DISCLOSED |  | investors.klarna.com (2021-03) |
| lead-school-2022-01 | 2022-01 | GROSS_REVENUE | 99.7 | GROWING | DERIVED |  | entrackr.com (2021-10) |
| loadsmart-2022-02 | 2022-02 | GROSS_REVENUE | 134 | GROWING | DISCLOSED |  | prnewswire.com (2022-02) |
| mambu-2021-12 | 2021-12 | ARR | 120 | GROWING | DISCLOSED |  | businesswire.com (2021-12) |
| meesho-2021-09 | 2021-09 | NET_REVENUE | 158.3 | GROWING | DERIVED |  | entrackr.com (2022-02) |
| mews-2026-01 | 2026-01 | NET_REVENUE | 50 | MATURE | THIRD_PARTY_DATED | yes | prnewswire.com (2025-03) |
| mollie-2021-06 | 2021-06 | GROSS_REVENUE | 64.4 | MATURE | THIRD_PARTY_DATED |  | quotenet.nl (2022-06) |
| monzo-2021-12 | 2021-12 | GROSS_REVENUE | 17.9 | MATURE | DERIVED |  | monzo.com |
| monzo-2024-05 | 2024-05 | GROSS_REVENUE | 147.5 | GROWING | DERIVED |  | monzo.com (2024-06) |
| moss-2026-08 | 2026-08 | ARR | 65 | MATURE | DISCLOSED |  | dealroom.co (2026-08) |
| ninjacart-2021-12 | 2021-12 | GROSS_REVENUE | 60 | MATURE | THIRD_PARTY_DATED |  | inc42.com (2022-06) |
| noom-2021-05 | 2021-05 | GROSS_REVENUE | 100 | GROWING | DERIVED |  | pymnts.com (2021-05) |
| octopus-energy-group-2021-09 | 2021-09 | GROSS_REVENUE | 62 | MATURE | DISCLOSED |  | octopus.energy (2022-01) |
| octopus-energy-group-2021-12 | 2021-12 | GROSS_REVENUE | 62 | MATURE | DISCLOSED |  | octopus.energy (2022-01) |
| octopus-energy-group-2022-07 | 2022-07 | GROSS_REVENUE | 110 | GROWING | DISCLOSED |  | octoenergy-production-media.s3.amazonaws.com (2022-12) |
| octopus-energy-group-2023-12 | 2023-12 | GROSS_REVENUE | 197 | GROWING | DISCLOSED |  | octoenergy-production-media.s3.amazonaws.com (2024-01) |
| octopus-energy-group-2024-05 | 2024-05 | GROSS_REVENUE | 197 | GROWING | DISCLOSED |  | octoenergy-production-media.s3.amazonaws.com (2024-01) |
| oura-2024-12 | 2024-12 | GROSS_REVENUE | 100 | GROWING | DISCLOSED | yes | businesswire.com (2024-12) |
| owner-2026-08 | 2026-08 | ARR | 100 | GROWING | DISCLOSED | yes | owner.com (2026-08) |
| packable-2021-09 | 2021-09 | GROSS_REVENUE | 51.5 | MATURE | DISCLOSED |  | sec.gov (2021-09) |
| perplexity-2025-07 | 2025-07 | ARR_RUNRATE | 530 | HYPER | STATED |  | americanbazaaronline.com (2025-03) |
| pinelabs-2021-05 | 2021-05 | NET_REVENUE | -14.2 | MATURE | THIRD_PARTY_DATED |  | entrackr.com (2022-07) |
| plaid-2025-04 | 2025-04 | ARR | 25 | MATURE | DISCLOSED | yes | techcrunch.com (2025-04) |
| raisin-2023-03 | 2023-03 | GROSS_REVENUE | 92.7 | GROWING | THIRD_PARTY_DATED |  | paymentandbanking.com (2024-05) |
| rapyd-2021-01 | 2021-01 | GROSS_REVENUE | 400 | HYPER | DERIVED |  | calcalistech.com (2021-01) |
| restore-hyper-wellness-2021-12 | 2021-12 | GROSS_REVENUE | 141 | GROWING | THIRD_PARTY_DATED |  | businesswire.com (2021-02) |
| revolut-2021-07 | 2021-07 | GROSS_REVENUE | 190 | GROWING | THIRD_PARTY_DATED |  | assets.revolut.com (2023-02) |
| revolut-2023-11 | 2023-11 | GROSS_REVENUE | 95 | GROWING | DISCLOSED |  | revolut.com (2024-07) |
| revolut-2024-08 | 2024-08 | GROSS_REVENUE | 95 | GROWING | DISCLOSED |  | revolut.com (2024-07) |
| revolut-2025-11 | 2025-11 | GROSS_REVENUE | 46 | MATURE | DISCLOSED |  | revolut.com (2026-03) |
| scale-ai-2025-06 | 2025-06 | NET_REVENUE | 129.9 | GROWING | DERIVED |  | bloomberg.com (2025-04) |
| shein-2023-05 | 2023-05 | NET_REVENUE | 44.6 | MATURE | THIRD_PARTY_DATED |  | businessofapps.com (2026-06) |
| spendesk-2022-01 | 2022-01 | ARR | 100 | GROWING | STATED | yes | techcrunch.com (2022-01) |
| starling-bank-2021-03 | 2021-03 | ARR_RUNRATE | 400 | HYPER | DISCLOSED |  | starlingbank.com (2021-03) |
| stripe-2025-02 | 2025-02 | NET_REVENUE | 28 | MATURE | THIRD_PARTY_DATED |  | axios.com (2025-03) |
| sumup-2023-12 | 2023-12 | GROSS_REVENUE | 30 | MATURE | DISCLOSED | yes | techcrunch.com (2023-12) |
| the-zebra-2021-04 | 2021-04 | ARR_RUNRATE | 113.5 | GROWING | DERIVED |  | prnewswire.com (2021-04) |
| thirty-madison-2021-06 | 2021-06 | ARR_RUNRATE | 200 | GROWING | DISCLOSED |  | prnewswire.com (2021-06) |
| turing-2025-03 | 2025-03 | ARR | 200 | GROWING | DISCLOSED |  | businesswire.com (2025-01) |
| upgrad-2021-08 | 2021-08 | ARR_RUNRATE | 100 | GROWING | DISCLOSED |  | newswire.ca (2021-04) |
| vedantu-2021-09 | 2021-09 | ARR_RUNRATE | 300 | HYPER | STATED | yes | techcrunch.com (2021-09) |
| VEGROW-2023-12 | 2023-12-13 | GROSS_REVENUE | 258.1 | HYPER | DERIVED |  | entrackr.com (2024-01) |
| vinted-2024-10 | 2024-10 | NET_REVENUE | 61 | MATURE | THIRD_PARTY_DATED |  | techcrunch.com (2024-10) |
| waycool-foods-2022-06 | 2022-06 | GROSS_REVENUE | 142.5 | GROWING | DERIVED |  | entrackr.com (2023-01) |
| wefox-2022-07 | 2022-07 | GROSS_REVENUE | 128.6 | GROWING | DERIVED |  | businesswire.com (2022-07) |
| whoop-2026-03 | 2026-03 | ARR_RUNRATE | 103 | GROWING | DISCLOSED |  | whoop.com (2026-03) |
| xpressbees-2022-02 | 2022-02 | NET_REVENUE | 32.7 | MATURE | THIRD_PARTY_DATED |  | entrackr.com (2022-03) |
| zepz-2021-08 | 2021-08 | GROSS_REVENUE | 67 | MATURE | THIRD_PARTY_DATED |  | prnewswire.com (2022-09) |


## What happens next, in my view

Three things need a ruling and nothing else does. First, whether the five estimator figures held
out (item 3 above) should be loaded on the file's existing Sacra precedent; one line in the raw
file and one loader run does it. Second, whether the 17 "revenue wording on an ARR row" figures
and the two "measure not named" rows stay; if not, blank them in the raw file and the loader will
not refuse, because the rows in the data files would then have to be cleared by hand, which this
loader does not do on purpose. Third, whether to rerun `tools/refit_growth_bands.py` now that 170
rounds carry a rate rather than 51; the code comment expects the boundaries to fall as coverage
widens, and every band on every row would move with them.

Separately, the revenue-figure contradictions above are the basis audit's list. Ten of them are
currency carried over unconverted or a wrong unit, which change a multiple by a third or more, and
one (BlockFi) by a factor of twelve.
