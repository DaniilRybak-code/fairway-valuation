# The lending fork, reconsidered

2 September 2026. Daniil's ruling: *"Public banks (e.g. Nu) tend to trade on book value, with some
cross check on EBITDA when they are profitable. As we can see, private neobanks are often priced
off ARR. So the ARR should be added to the quiz for the archetype and the respective range based on
PRIVATE precedents has to be shown."*

## Why the current fork is wrong, in numbers

The lending fork asks for book value as a required field, prices on price to book, and marks the
loan book and originations as reviewer context. It is built on **one** private book multiple.

| | Comparables we hold |
|---|---|
| Book multiples, private | **1**  (Zopa Oct-21, 5.6x) |
| Revenue or ARR multiples, finance archetypes | **16 median-eligible, 19 in total** |

Pricing a founder off a single comparable breaks our own standing rule that we never price off one
comp. The fork has been doing exactly that since it was built, and the reason was not judgement, it
was scarcity: until today the neobank rows were not loaded.

## What we can now show, from private precedents only

**Digital Bank & Deposits, 11 rounds, median 15.0x, range 4.7x to 51.9x**

| Company | Date | Multiple | Denominator |
|---|---|---|---|
| Monzo | May-24 | 4.7x | FY2024 revenue |
| Atom Bank | Nov-23 | 4.8x | FY ended Mar-2023 |
| Mercury | Mar-25 | 5.4x | annualised revenue |
| Chime | Apr-24 | 9.6x | FY2024 revenue |
| Revolut | Nov-25 | 12.5x | FY2025 revenue |
| Revolut | Nov-23 | 15.0x | FY2023 revenue |
| Revolut | Aug-24 | 20.5x | FY2023 revenue |
| Chime | Aug-21 | 26.3x | annual revenue |
| Qonto | Jan-22 | 41.7x | annualised revenue |
| N26 | Oct-21 | 45.0x | annual revenue |
| Revolut | Jul-21 | 51.9x | annual revenue |

**Lending & Credit, 5 rounds**: Klarna Jul-22 5.1x and Jun-21 37.6x on bank net operating income,
Better.com May-21 8.8x on net revenue, Upgrade Aug-21 21.4x on run-rate, Kriya 0.6x held pending a
unit check. **Insurance, 2 rounds**: Alan Sep-24 8.2x as a ceiling, wefox Jul-22 14.1x.

The spread is wide and the reason is visible in the table: the 2021 vintage prices at 26x to 52x
and the 2023 to 2025 vintage at 4.7x to 20.5x. That is the rate cycle, not noise, and the range
should say so rather than average across it.

## The change

**1. Add an ARR question to the lending fork.** Alongside book value, not instead of it.

```
key='arr', label='What is your annual recurring revenue, or annualised revenue?',
kind='money', required=True, maps_to='profile.revenue', peer_field='revenue_musd',
basis='ARR', period_required=True,
why='Private neobanks and lenders are priced off revenue far more often than off book. We hold
    16 private rounds priced on revenue or ARR against one priced on book, so this is the
    question that can actually be answered with comparable evidence.'
```

**2. Book value stays required, and stays the public-market anchor.** Nu, Lloyds and their peers
trade on price to book, and a founder heading for that market needs to see it. But it is presented
as the listed anchor with one private point, not as the primary range.

**3. Show two ranges, labelled by what each is built from.**

- *What private rounds paid* — the revenue and ARR range above, built from private precedents only,
  which is what Daniil asked for.
- *What the public market pays* — price to book from the listed set, with an EBITDA cross-check
  where the bank is profitable.

Never a blended number. The two answer different questions and a founder raising privately is
priced against the first.

**4. `is_balance_sheet` stays as it is.** It decides the basis from the founder's own archetype and
that logic is right. What changes is that the lending fork no longer has only one lane: a lending
founder sees the book anchor and the private revenue range side by side.

**5. Funding model still routes the emphasis.** Retained credit risk leans on book. Originate and
distribute for a fee leans on revenue. The question already exists in the fork and now has
something to switch between.

## What is still missing before this can ship

- **Listed price-to-book and EBITDA for the banks.** We hold no listed book multiples at all. Nu,
  Revolut's listed peers, the European neobanks and the incumbents all need pulling. Without them
  the public anchor is an empty box.
- **Klarna's basis.** Two Klarna rows price on bank net operating income, which is neither revenue
  nor book. Its FY2020 statutory reports contain no "Revenue" line at all. That inconsistency was
  flagged on 1 September and is still unresolved.
- **A vintage split.** With 11 neobank rounds spanning 4.7x to 51.9x, the range needs to separate
  the 2021 vintage from the 2023 to 2025 vintage or it will show a founder a spread so wide it says
  nothing.
