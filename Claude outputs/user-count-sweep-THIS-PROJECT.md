# Prompt: finish the user-count sweep, in this project

**Run this in a NEW CHAT IN THIS SAME PROJECT, on this repo.** It is not for another LLM and not for
another dataset. Everything it needs is already in the repo.

---

You are working in the Fairway repo. Read `docs/RULES.md` section D before you touch anything, and
follow Daniil's four standing constraints: never run a git command on his machine through the
bridge, never silently drop a row, every commit instruction is `git add -A`, and no em dashes.

## The job

We hold **290 private funding rounds**. For each one we want the number of users, subscribers,
members, merchants, customers or borrowers **quoted in that round's own announcement**, and the
enterprise value per unit computed from it. Daniil: "check thoroughly the existing database of 290
private rounds, checking for each if the number of users / subscribers / members was quoted at the
announcement and calculating the respective EV / subscribers multiple for each row where available."

## What already exists, so you do not repeat it

| file | what it is |
|---|---|
| `data/raw/2026-09-03_user-count-sweep-targets.csv` | every round with its announcement URL. 241 of 290 have one, covering 217 distinct URLs |
| `data/raw/2026-09-03_user-counts-sweep-wave1.csv` | wave 1 results, 106 URLs read |
| `data/raw/2026-09-03_user-counts-sweep-wave2.csv` | wave 2 results, 53 URLs read |
| `tools/load_user_counts_3sep.py` | loads a wave file onto the rounds and computes the per-unit figure |

**About 58 URLs remain unread**, plus 49 rounds that have no announcement URL at all and need one
sourced before they can be swept. Work out which by comparing the targets file against the two wave
files. Do not re-read a URL that is already in a wave file.

## Method

Work in batches of 25 to 30 URLs, one subagent per batch, running batches in parallel. Instruct each
subagent exactly as follows, because every one of these rules was learned by getting it wrong:

1. **Only report what appears on the page you fetched.** Never supplement from memory or another
   source. If nothing countable is on the page, say NONE.
2. **Quote the wording verbatim.** "Customers" and "paying customers" are different things and the
   difference decides what the figure can be compared against.
3. If the page 404s, is paywalled or renders nothing, say UNREACHABLE. Do not substitute another
   source. A visible gap beats an invented figure.
4. **Report every countable figure on the page**, not just the first. Pages often give paying,
   active and registered counts and we want all three.
5. **Only the subject company's own counts.** Announcements are full of numbers belonging to the
   investor, the acquirer, a competitor or the market. Employee headcount is not a customer count.
6. **The company's own press release beats the trade coverage.** Where our stored URL is a
   TechCrunch or similar piece and the company published its own announcement of the same round,
   read the company's. That is how WHOOP's Series G count was missed: our URL was the trade story
   and the count is in WHOOP's own release.

## The schema, and the one rule that matters

Write each finding as: `company, round, count, metric_kind, is_paying, as_worded_on_the_page`.

`metric_kind` is one of PAYING_SUBSCRIBERS, MEMBERS, CUSTOMERS, BUSINESS_CUSTOMERS, MERCHANTS,
BORROWERS, ACTIVE_USERS, REGISTERED_USERS, or OTHER with the thing named.

**A range may only ever be built inside ONE kind.** A merchant count never meets a subscriber count,
and a borrower never meets either: a borrower pays interest on a balance, a subscriber a fee for
access, a merchant a fee on volume. Mixing them is the same error as averaging gross revenue with
net. This is why the kind matters more than the number.

`is_paying` is YES, NO or UNKNOWN: **is the counted party the party that pays?** In buy-now-pay-later
the merchant pays and the shopper does not. In most digital banking the customer pays nothing
directly. Daniil, 3-Sep: "they do not necessarily NEED to be paying, but if they are, we need to make
the respective note of it." So the count is kept either way and this is the note, not a filter.

## When you have the results

1. Write them to `data/raw/2026-09-03_user-counts-sweep-wave3.csv`, same header as wave 1 and 2,
   with the same comment block at the top explaining the method.
2. Add the file to the `SRC` list in `tools/load_user_counts_3sep.py` and run it, first without
   `--write` to read the accounting, then with `--write`.
3. Run `sh tools/check_all.sh`. All eight checks must pass. If golden moves, read the diff and say
   what moved and why before rebaselining with `python3 selector/golden.py --write`.
4. Append to `data/MANIFEST.md`: how many URLs read, how many counts found, how many loaded, and the
   kinds not loadable as a denominator.
5. Hand Daniil the `git add -A` commit command. Do not run git yourself.

## What NOT to load

Downloads, sessions, visits, app installs, locations, listings, terminals, trucks, units sold and
transactions are recorded in the raw file and are NOT loaded as a denominator. A price per download
is a number with nothing behind it. If a round already carries a money volume (originations, GMV,
payment volume), leave it: that is a better denominator and the loader will not overwrite it.
