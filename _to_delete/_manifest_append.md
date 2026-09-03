
## 2026-09-03 (night, 6): the sweep finished, and a promotion caught on the way

### What wave 3 read

**The 58 said to remain could not be named, so wave 3 read 224 rounds.** Waves 1 and 2 recorded
only the URLs that produced a finding, never which URLs were read. 66 rounds carried a finding and
224 did not, so "159 of 217 read" could not be reproduced from any file in the repo and the 58
remaining could not be listed. Under D12 a set that cannot name what fell out of it is not a set you
may act on, so every round without a finding was read again, including pages waves 1 and 2 had
already read and found nothing on. Daniil approved the wider scope before any agent ran.

**Also corrected: no round is missing a URL.** The targets file was described as 241 URLs with 49
rounds carrying none. All 290 carry one; the 49 are the same kind of link with the scheme missing
(`techcrunch.com/2022/01/09/ankorstore...`). They were read with `https://` prepended. The targets
file was not edited: raw files are append-only.

**222 distinct pages read, 398 countable figures, across 158 of the 224 rounds.** Eight agents read
the 223 stored URLs, each told to report only what appears on the page it fetched, to quote
verbatim, to report every figure and not just the first, to take only the subject company's own
counts, and to prefer the company's own release over the trade story.

**62 URLs came back dead, and Daniil's ruling was to check independently rather than record a gap:**
"Announcement URL could not be read - check it independently then." Three further agents re-read
those 62 against a working page for the SAME round, found through the company's own release at its
new path, a syndicated PR Newswire or BusinessWire copy, or trade coverage of that round.
**60 of the 62 recovered.** That is where 1Password, Airwallex, Docker, Mambu, Mercury, Miro, N26,
Personio, Plaid, Pleo, Qonto, Raisin, Revolut, Snyk, SumUp and Tipalti came from. Most of the 62
were 404s on the companies' own newsroom pages: link rot in our stored URLs, not missing data.

Two did not recover and both look mis-dated at source rather than merely unlinked. **Checkout.com
Dec-23**: no Checkout.com round exists in December 2023; the $11bn internal cut was Dec 2022 and the
$12bn buyback Sept 2025. **Revolut Nov-23**: the stored URL is an annual-report page, not a round,
and Revolut has no November 2023 funding event. Both are worth a look at the source sheet.

`data/raw/2026-09-03_user-counts-sweep-wave3.csv` holds the figures.
`data/raw/2026-09-03_user-counts-sweep-wave3-readlog.csv` is new and is the thing waves 1 and 2
lacked: one row per round for all 224, FOUND, NONE or UNREACHABLE, with the page actually read.
A URL that finds nothing now leaves a trace.

### What loaded

**79 counts loaded, 63 into `private-rounds.csv` and 16 into `private-rounds-consumer.csv`.**
Every count matched a round: **counts with no matching round in either file, 0.**

**The loader now writes to BOTH private round files.** Until wave 3 it wrote only to
`private-rounds.csv`, so the 52 rounds in the consumer file could never receive a count however well
it was sourced, and waves 1 and 2 lost 19 of them without saying so. Daniil, 3-Sep: "Why are there
two separate CSVs for private rounds? We should have 1 CSV with all data combined." The merge is its
own job and is not done here. As a step toward it the consumer file gained the five volume columns
the main file already had (`volume_metric`, `volume_musd`, `volume_period`, `volume_basis`,
`ev_volume_x`), which moves the two schemas together rather than apart.
`selector/match_reference.py` already read those columns from both files, so nothing on the engine
side changed.

**135 rounds now carry a count**: BUSINESS_CUSTOMERS 59, CUSTOMERS 34, MERCHANTS 15, ACTIVE_USERS
11, REGISTERED_USERS 6, MEMBERS 5, PAYING_SUBSCRIBERS 5.

**155 rounds already carry a money volume and were not overwritten.** An originations, GMV or
payment-volume figure is a better denominator and the count stays in the raw file.

**275 figures are recorded in raw and are NOT loadable as a denominator, across 186 kinds**:
downloads, sessions, visits, app installs, locations, listings, terminals, trucks, units sold,
transactions, warehouses, charge points, employees, patients covered, event attendees, community
members. A price per download is a number with nothing behind it.

**Sixteen figures were re-kinded to OTHER before loading**, each a real verbatim quote that is not
the round's customer count: penetration statistics (Klarna "30 of the top 100 US retailers"),
threshold subsets (Klaviyo 1,458 above $50k ARR, Ramp 2,200 above $100k, Databricks 300 above $1m
run-rate), a prior round's figure (Gorgias 4,500 stores, stated on the page as the Series B number),
flows rather than stocks (Pipe 1,000 signups since March, Deel 1,800 as the April 2021 endpoint),
named sub-segments (Canva 600,000 nonprofits, Monzo 400,000 business clients against 9m retail
customers, Octopus 25,000 business-division customers against 2.5m, MoonPay 250 wallets against 7m
customers), stale about-boilerplate (Miro 25m users and 100,000 client orgs, both contradicted by
the body of the same release) and one figure contradicted on its own page (Contentsquare "over one
million customers" against the 1,000 enterprise customers stated in the same release). Without these
the loader's rank would have priced Canva per nonprofit and Monzo per business client.

### The promotion the sweep caught, which was not the sweep's

**`tools/load_user_counts_3sep.py` set `in_medians = '1'` on every row it loaded a count into.**
There is one `in_medians` gate in `selector/match_reference.py` and it governs whether a row may
price AT ALL, on any basis. So loading a user count also switched that row's REVENUE multiple back
on. **17 rows flipped from 0 to 1, and 12 of them carried a revenue multiple that had been excluded
by hand.** Golden showed it: Decagon entered two founders' ranges at 150.0x and lifted the top from
105.3 to 150.0, and Decagon's revenue bound is `<=`, so 150.0x means "at most 150x". Factorial's
denominator is GROSS_REVENUE, which is precisely the case `match_reference` warns about at line
1205: "That is how Razorpay's 67.6x on a gross denominator sat in the fintech file for four days."

The line was in the tool before wave 3 and ran over 56 rows in the 17:52 commit, so part of this was
already in the baseline. Both round files were restored to `e9ab546` and the load re-run with the
promotion removed, so the state below is the state as if the bug had never run.

**The gate is now raised only where there is no revenue multiple to readmit.** Where a row carries
one and was excluded, the count is still written and still visible, and the row is named in the
tool's output as BLOCKED. Thirteen rounds are blocked this way: Decagon, Airwallex May-25, Huntress,
Vercel, Databricks, Apollo.io, Snyk, Factorial, Docker, PayFit, Miro, Salesloft, Flipkart. D8: a
figure in the file but not in the engine is reported as absent, not as pending.

**This needs a ruling.** One gate cannot serve two lanes. A row barred from revenue ranges for a
gross denominator or a bounded figure may still be perfectly good evidence per merchant or per
subscriber, and today it cannot price on either. The fix is to split `in_medians` into a revenue
gate and a count gate. It is not something to slip in inside a data sweep.

### Golden

**7 of 43 profiles moved, no peer names moved and no range moved.** The only change in the
snapshots is `in_medians` going False to True on four rounds that now have a denominator where they
had none: CommerceIQ Mar-22, Glovo Dec-21, Gorgias Aug-22 and Loop Returns Jul-21. Deliberately
rebaselined, now 0 of 43.

**All eight checks pass.**

**State: 511 listed on 1-Sep data with 13 frozen as stale, 290 private rounds, 210 median-eligible,
135 carrying a user count, peer universe 39 of 43, all eight checks green.**
