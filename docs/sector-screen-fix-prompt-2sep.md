# Sector screen fix prompt

Paste everything below the line into your other LLM with the workbook attached.

---

Your workbook "Priced Private Funding Rounds — Sector Screen" has 51 rows. Only 21 give a usable
multiple. Fix the other 30, keeping the same rows and columns.

**Rules.** Every figure needs a URL and the sentence containing it, quoted. NOT FOUND is valid;
never estimate. Use what was public at the round date. Estimator sites are a last resort, tagged
`source_tier = 4`.

**1. Currency mismatch, 11 rows.** 6, 7, 8, 9, 11 (INR), 12, 13, 15, 16, 17 (GBP), 53 (USD against
a EUR valuation). Restate the denominator into the valuation's currency, never the reverse.
Add `denominator_converted`, `fx_rate_used`, `fx_rate_date` (the announcement date, not the year
end), `fx_rate_source`.

**2. Missing denominators, 8 rows.** Rows 33, 34, 39, 51, 52, 56 have a clean number unused beside
them (upGrad 165, LEAD School 80, EGYM 130, Roblox 923.9 from the audited S-1, Epic Games 5,100,
Dream Sports 27,060). Use it or explain in `denominator_blank_reason`. Rows 23 and 24 hold "a range
from $50m" and "nine figures": find a firm number, else `bound = GTE`. Row 39's USD metric also
needs restating into EUR.

**3. Floors, 7 rows.** 18, 19, 20, 24, 25, 31, 48. Find the firm figure, or keep the floor and set
`bound = GTE` so the ceiling is explicit.

**4. Part-year denominators, 4 rows.** BlockFi one month, MoonPay eleven, Devoted Health H1, wefox
four. Use the full year, or a published annualisation you can cite, or record `period_months` and
leave the annualising to us. Never annualise it yourself and call it reported.

**5. Forward figures, 3 rows.** 42 Oura, 43 Athletic Greens, 34 LEAD School. Use the trailing figure
public at the round; keep the forward one in `forward_metric`.

**6. Contradictions.** Row 54 Discord: metric 130 for FY2020, denominator 310 for FY2021. Pick one,
cite it. Row 14 Fuse Energy: $5,000m post on a $70m Series B, and neither source states a
valuation. Find one or set NOT FOUND. Rows 27 and 50 are one Alan round four days apart; rows 37
and 40 are one BetterUp round. Delete one of each.

**7. Sourcing.** Rows 6, 7, 29, 30, 32, 35, 41, 52, 55, 56 rest on weak sources; replace where you
can (56 needs the live URL, not staging). Rows 8, 21, 38, 55 price on a figure over a year old:
find one closer, or confirm it was the latest public number.

**8. Mark, do not fix.** Row 10 eFishery (figures later found fabricated) and row 21 Celsius
(bankruptcy, fraud findings): set `excluded = YES` with a reason.

Finally fill the **implied multiple** column, blank on all 51 rows today, as post-money over
denominator in one currency, and state at the top how many rows now give a multiple, how many are
ceilings, how many are NOT FOUND. The target is **48**: 51 less two duplicates and eFishery. Do not
pad to 51.
