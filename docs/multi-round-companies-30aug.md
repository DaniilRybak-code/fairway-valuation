# One company, several priced rounds: what the engine does with them

30-Aug-2026. Written after Daniil asked us to double check Meesho, where one company
carries 45.8x and 4.2x.

## Meesho is not wrong

Both rows are right, and they were checked line by line.

| Row | Date | Round | Post-money | Denominator | Multiple |
|---|---|---|---|---|---|
| meesho-2021-09 | Sep-21 | Series F, $570m raised | $4,900m | FY2021 net revenue to 31-Mar-21, INR 793 crore, about $107m at 74.1 | 45.8x |
| meesho-2024-05 | May-24 | Series F, $275m raised | $3,900m | FY2024 net revenue to 31-Mar-24, INR 7,615 crore, $922m at 82.572 | 4.2x |

4,900 / 107 = 45.8. 3,900 / 922 = 4.2. Both denominators are filed accounts, both are
net revenue, both describe a year that had already ended at the pricing date, neither is
a threshold. Revenue grew 8.6 times between the two rounds while the valuation fell 20
per cent. That is a real repricing of an Indian value-commerce marketplace between the
2021 peak and 2024, not a data error.

## The real defect is which of the two we show

Seven companies carry more than one priced round: AlphaSense (3), Klarna, Meesho, Mews,
Scale AI, SKIMS, Vinted. That is 63 priced rows from 55 companies.

`select_private` already keeps one row per company, so nothing double counts in a median.
It picks the row with the highest business-nature score, and breaks a tie on the later date.

The scores always tie. Two rounds of the same company carry the same tags, so the score is
identical every time, in all 103 fixture-and-company pairs we tested. Recency therefore
decides on its own, every time. That is the thing we said must never select a comparable.

Eight priced rows, 13 per cent of the priced private evidence, can never be reached by any
founder:

| Never shown | Multiple | Shown instead |
|---|---|---|
| Meesho Sep-21 | 45.8x | Meesho May-24, 4.2x |
| Klarna Jun-21 | 37.6x | Klarna Jul-22, 5.1x |
| AlphaSense Sep-23 | 25.0x | AlphaSense Jun-24, 20.0x |
| AlphaSense Jun-22 | 17.0x | AlphaSense Jun-24, 20.0x |
| Mews Mar-24 | 12.0x | Mews Jan-26, 12.5x |
| Scale AI May-24 | 9.9x | Scale AI Jun-25, 14.5x |
| Vinted Oct-24 | 8.4x | Vinted Apr-26, 7.3x |
| SKIMS Jul-23 | 5.3x | SKIMS Nov-25, 5.0x |

The two largest losses are the two highest multiples in the set. A founder at $10m of
revenue growing 150 per cent is far closer to Meesho at $107m and Klarna in its growth
years than to Meesho at $922m or Klarna after the repricing, and today we hand that founder
the mature round and nothing else.

## Proposed rule

Keep one company, one vote. Choose the round by closeness to the founder rather than by
date: revenue scale first, then growth rate at the round, then maturity, on the same five
dimensions we use for the next best neighbour. Fall back to the later date only when the
founder has given us neither revenue nor growth.

Not implemented. Needs Daniil's call on the ordering of the dimensions.
