
## 2026-09-03 (night, 7): Decagon, and what checking it turned up

Daniil, on seeing Decagon at 150x: "should be shown on the FF as a diamond, not included in the bar
range I would say. If its multiple based on number of users is more reasonable (closer to median
that we show for this type of companies), the USER multiple can be included in the range."

Checking whether Decagon's count could price where its revenue could not found that it cannot, and
found three more of the same shape, two of them loaded from waves 1 and 2 this afternoon.

### A flow is not a stock, and four figures were both

**Decagon's count is "more than 100 NEW global enterprise customers ... joined the Decagon family".**
That is customers ADDED, not the installed base, so $45m per customer added is not a denominator.
It is the same objection as Pipe's "1,000 signups since March", which was re-kinded earlier today;
this one was missed because the word "new" sits mid-sentence.

Scanning all 135 loaded counts for the same shape found four:

| round | figure | why it cannot price |
|---|---|---|
| Decagon Jan-26 | 100 new enterprise customers | period addition |
| Glossier Mar-19 | 1,000,000 new customers introduced | period addition |
| Fundbox Nov-21 | 325,000 businesses "since its founding" | cumulative since inception |
| Pipe May-21 | 4,000 signed up "since its public launch in June 2020" | cumulative since inception |

The since-inception two are barred by a rule Daniil already gave on 2-Sep: "multiples cannot be
calculated over all time origination volumes." `match_reference` enforces it for money volumes by
testing `vol_period` for INCEPTION, but this loader writes `'At the round'` for every count, so the
guard could never fire on the count lane. All four are now in `EXCLUSIONS` in the loader with a
reason, per D12. The raw files were not edited; they are append-only.

**Counts loaded 135 to 131.**

### The loader now takes its own work back out before reloading

Excluding Fundbox stopped it loading again but left the stale $3,385 per business customer that
wave 2 had already written. A run was a patch on top of its own output, not a rebuild. The loader
now clears the five volume columns on any row carrying its own stamp before it loads, so running it
twice gives the same file, and a figure that is excluded can actually be taken back out. It also
made the accounting honest: "rounds that already carry a money volume" was 155, of which 135 were
this tool's own previous output. The real number is **20**.

### Four more rows the promotion had left behind

Restoring the data files to `e9ab546` did not undo the `in_medians` promotion, because `e9ab546` is
AFTER the buggy load in `cc85d3a` and carries other real work. Four rows kept a raised gate:
**Anthropic Sep-25, OpenAI Mar-25, Perplexity Jan-24 and Shiprocket Aug-22.** All four read
`in_medians=0` at `02836c8`, the last commit before any count was loaded, read through the GitHub
MCP rather than by running git on Daniil's machine. They are corrected by name in the loader and
the blocked list is now **16**.

Golden shows what they had been doing. **OpenAI Mar-25 at 54.5x was pricing goldfish, publora and
acti.** **Shiprocket Aug-22 at 16.03x on a GROSS_REVENUE denominator was pricing sellerclaw, hived,
byrd and 99minutos**, which is the Razorpay case in four founders' answers at once. Both are now out
of every range and stay visible as context. Three ranges got thinner and are flagged thin, which is
the honest reading: goldfish and acti go from 3 names to 2 with the mid moving 54.5 to 120.0, and
publora from 3 to 2 with the high moving 54.5 to 20.0. Rebaselined, now 0 of 43.

Verified to zero: no row in `private-rounds.csv` now carries an `in_medians` value that differs from
`02836c8` except the 11 where a count is the row's only denominator.

### Still open, and it is the same question Daniil asked

**Two thirds of the count lane is bounded and nothing records it.** 90 of the 131 loaded counts are
worded "more than X" or "over X". A count that is a floor makes enterprise value per unit a
CEILING. The revenue lane has a `bound` column and `honesty.py` fires "At most Nx" from it; the
count lane has no bound at all, because this loader never wrote one. So the caveat that fires for a
bounded revenue multiple does not fire for a bounded count.

**And a bounded figure should not set the edge of a bar.** Today it does. Four fixtures have their
private range high set by a `<=` row, and in two of them, upstream and bond, Glean's "at most 72x"
is the top of the bar the founder sees while the caveat underneath says the true figure is lower.
Daniil is right that this should be a diamond. The rule that follows is about the KIND of
measurement, not its level: a point estimate sets a bar edge, a bounded figure never does, and each
metric kind gets its own bar. Not built. It needs his ruling alongside the `in_medians` split.

**State: 511 listed on 1-Sep data with 13 frozen as stale, 290 private rounds, 205 median-eligible,
131 carrying a user count, peer universe 39 of 43, all eight checks green, golden 0 of 43.**
