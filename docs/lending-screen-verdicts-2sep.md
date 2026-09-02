# Lending and credit screen: review

2 September 2026. Source: four screenshots of "Lending and Credit - Priced Private Funding Rounds",
22 rows, transcribed to `data/raw/2026-09-02_lending-screen.csv`. Addresses point 4 of
`docs/data-pull-prompts-2sep.md`.

## The short answer

**It does not deliver what point 4 asked for, and it delivers something more useful instead.**

Point 4 asked for balance-sheet measures, in its own words: "net loan book or gross loans
outstanding; total equity or net asset value; loans originated in the last twelve months; customer
deposits", on the reasoning that "lenders price on book, so revenue figures do not help here".

**Not one row carries a net loan book, total equity, NAV or customer deposits figure.** Wayflyer's
FY2021 originations is the only thing close to the fourth measure. So Zopa at 5.6x is still the only
priced book multiple we hold, and the four fixtures pricing off it alone are still pricing off it
alone. That gap is untouched.

What arrived instead is the private revenue and ARR evidence that **ruling 7** asked for: "Private
neobanks are often priced off ARR. So ARR should be added to the quiz for the archetype and the
respective range based on PRIVATE precedents has to be shown." On that it delivers.

## What is usable, sorted by what the denominator actually is

All 19 readable multiples recompute exactly. Zero mismatches. The arithmetic is not the problem.
What the denominators *are* is the problem.

| Kind | Rows | Verdict |
|---|---|---|
| Periodic revenue or ARR | **7** | Usable as revenue multiples |
| Income-statement line, not revenue | 1 | Klarna Jul-22, load as its own basis |
| Periodic volume or originations | 3 | Volume lane, not the revenue median |
| Third-party ARR sitting on the platform | 1 | Pipe. Not the company's own revenue |
| **Cumulative since inception** | **10** | **Not multiples at all** |

The seven real ones, and they are a proper range for a neobank and lender archetype:

| Company | Date | Multiple | Denominator |
|---|---|---|---|
| Klarna | Jun-21 | ≤45.60x | FY2020 full-year revenue |
| Monzo Bank | Dec-21 | 42.32x | FY ended 28-Feb-2021 |
| Konfio | Sep-21 | 39.23x | LTM revenue at Jun-2021 |
| Nubank | Jun-21 | 31.15x | FY2020 revenue |
| Klarna | Mar-21 | ≤31.00x | FY2020 full-year revenue |
| Creditas | Jan-22 | 24.00x | 2021 annualised revenue |
| Starling Bank | Mar-21 | 7.59x | Jan-2021 annualised run-rate |

Every one is a 2021 or early-2022 vintage. That is the 26x to 52x peak the lender fork spec already
identified, and it means this sheet **cannot on its own build the vintage split the spec calls for**.
There is no 2023 to 2025 revenue-priced lender here at all.

## The thing that must not happen

**Ten of the 22 rows are struck on a cumulative-since-inception figure**: cumulative loans disbursed,
cumulative credit delivered, cumulative purchases financed, cumulative mortgage completions,
cumulative capital advanced, loans funded since launch. MNT-Halan, Atom Bank, Fundbox, Zilch, Billie,
Clearco, Upgrade twice, Tala, Happy Money.

A valuation divided by an all-time cumulative flow is not a multiple. It compares a point-in-time
price to everything the company has ever done, so it falls as the company ages and says nothing about
what a founder is worth. That is what produces the 0.15x, 0.30x, 0.44x, 0.48x, 0.60x and 0.74x in
this sheet. **If those load as EV/revenue they will halve the lending median and the number will be
meaningless.** The sheet itself is honest about this, saying "metrics preserve ... cumulative-volume
definitions" and marking floor-on-floor observations NM. The risk is on our side, at load time.

They are not worthless: they belong in the volume overlay next to GMV and TPV, as EV over cumulative
originations, clearly labelled. They are not revenue evidence.

## Cross-check against the engine: 8 of the 22 rounds are already loaded

This is the second time today a supplied sheet has turned out to be a check on the engine.

**Klarna, and this settles open decision 2.** The blocker was recorded as "two rows price on bank net
operating income, which is neither revenue nor book, and Klarna's FY2020 statutory reports contain no
Revenue line at all". This sheet confirms it and narrows the disagreement to one thing.

| Round | Engine | This sheet |
|---|---|---|
| Klarna Jun-21 | 1,212.1, basis BANK_NOI, 37.6x | 1,000.0, labelled FULL-YEAR REVENUE, ≤45.60x |
| Klarna Jul-22 | 1,303.7, basis BANK_NOI, 5.1x | 1,600.0, labelled TOTAL NET OPERATING INCOME, 4.19x |

Both sheets are using the same underlying figure: Klarna's total net operating income, SEK 9.7bn for
FY2020 and SEK 13.7bn for FY2021. **The gap is entirely the exchange rate.** SEK 9.7bn is $1,212m at
about 8.0 SEK per dollar and $1,000m at about 9.7. SEK 13.7bn is $1,304m at 10.5 and $1,600m at 8.6.
So this is not a basis dispute, it is an FX-date dispute, and neither file records the rate it used.

Two consequences. **Klarna has no revenue line, now confirmed from a second independent pull, so the
lending fork can stop waiting on that question.** And this sheet's two "FULL-YEAR REVENUE" labels on
the FY2020 rows are wrong; it is net operating income, as the sheet's own third Klarna row says.

**Upgrade, twice, and the engine is right.** The sheet carries 6,000 and 3,325 as PRE-money. The
engine carries 6,280 and 3,430, which is those figures plus the money raised. Both correct, and the
engine uses the right one. Three rows in this sheet are pre-money: Starling, and Upgrade twice.
Starling's 7.59x is therefore struck on a pre-money valuation while the other six revenue multiples
are struck on post-money. **Not like for like, and it is the lowest of the seven.**

**Wayflyer is a genuine unlock.** The engine holds Wayflyer Feb-22 at a 1,600 post-money with no
denominator, basis NONE, out of the medians. This sheet gives FY2021 originations of 500, so 3.20x.
An originations multiple, not revenue, but it takes an unpriced row and prices it.

**Fundbox is not a conflict.** The engine prices it on 100 ARR at 11.00x. The sheet adds a cumulative
volume figure. Different metric, no dispute.

**Eleven new companies**: Billie, Clearco, Happy Money, Konfio, MNT-Halan, Monzo Bank, Nubank, Pipe,
Starling Bank, Tabby, Zilch.

## Defects to flag back

1. **No FX rate, date or source anywhere.** Columns AC to AN are empty in every row. Four rows
   convert currency: Konfio MXN at an implied 0.0487, Monzo GBP at 1.3205, Zilch GBP at 1.3410,
   Billie EUR at 1.1608. None is reproducible from the file. The sector screen recorded all of this;
   this sheet does not. Konfio's implied 20.54 MXN per dollar is also a little weak for late
   September 2021, when MXN traded nearer 20.0, and it is the row with the second-highest multiple.
2. **Three implied-multiple cells could not be read** from the screenshots: Tabby Nov-23, MNT-Halan
   and Zilch. They compute to 0.25x, 0.50x and 14.91x. They are marked UNREADABLE in the raw file
   rather than guessed. Please confirm from the sheet.
3. **Two Klarna rows are labelled FULL-YEAR REVENUE and are net operating income.**
4. **Three rows are pre-money** and are not marked as an exception anywhere in the sheet.

## Recommendation

- **Load the 7 revenue and ARR rows** into the private set, tagged, so they reach a lending founder.
  Correct the two Klarna labels to net operating income first, and decide the FX date.
- **Load Wayflyer's originations** to price a row that currently prices nothing.
- **Do not load the 10 cumulative rows as revenue multiples.** Volume overlay or nothing.
- **Point 4 stays open.** The book measures it asked for did not arrive, so Zopa is still the only
  priced book comparable and the lender fork still cannot show a book range from more than one name.
