# Prompt: sweep every private round announcement for a count

Run this in another chat in this project. The target list is in the repo at
`data/raw/2026-09-03_user-count-sweep-targets.csv`: 290 rounds, 241 with an announcement URL, 217
distinct URLs. Wave one covered 106 of them and is recorded in
`data/raw/2026-09-03_user-counts-sweep-wave1.csv`. This prompt is for the remaining 111.

---

You are extracting countable figures from startup funding announcements for a valuation engine. I
am building enterprise-value-per-unit multiples, so a count stated in the announcement itself is
exactly what I need.

I will give you a list of `company | round month | URL`. **Fetch each URL and report every countable
figure of people or businesses that appears on that page.**

## What counts, and label each one with the kind

| kind | what it is |
|---|---|
| PAYING_SUBSCRIBERS | people paying a recurring fee for access |
| MEMBERS | members, where the page does not say whether they pay |
| CUSTOMERS | customers, unqualified |
| BUSINESS_CUSTOMERS | companies, organisations, teams, schools, gyms, practices, firms |
| MERCHANTS | merchants, sellers, shops, restaurants |
| BORROWERS | borrowers, cardholders |
| ACTIVE_USERS | monthly or daily active users |
| REGISTERED_USERS | registered, signed-up or total users |
| OTHER | downloads, sessions, visits, locations, trucks, units sold. Say which |

Also set `is_paying` to YES, NO or UNKNOWN: **is the counted party the party that pays?** In
buy-now-pay-later the merchant pays and the shopper does not, so a shopper count is NO. In digital
banking a customer usually pays nothing directly, so it is NO or UNKNOWN. This is a note on the
figure, not a filter: I want the count either way.

## Rules

1. **Only report what appears on the page you fetched.** Do not supplement from memory or from
   another source. If the page states nothing countable, write NONE for that company.
2. **Quote the wording verbatim.** "Customers" and "paying customers" are different things and the
   difference decides what the figure can be compared against.
3. If the page is a 404, a paywall or renders nothing, write UNREACHABLE. Do not substitute another
   source. I would rather have a gap I can see.
4. **Report every countable figure on the page, not just the first.** A page often gives paying,
   active and registered counts, and I want all three.
5. **Do not report figures about somebody else.** Announcements are full of counts belonging to the
   investor, the acquirer, a competitor or the market. If the number is not the subject company's
   own, either leave it out or mark it clearly as belonging to another party.
6. Employee headcount is not a customer count. Skip it.

## Output

One markdown table, one row per figure:

`Company | Round | Count | Kind | is_paying | Verbatim quote`

Then a short list of the pages that were UNREACHABLE, so I know what to re-source rather than
re-check.

## The list

[paste the remaining rows of data/raw/2026-09-03_user-count-sweep-targets.csv here, 25 to 30 at a
time. More than that and the fetches start being skipped.]
