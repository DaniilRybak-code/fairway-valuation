# Tagging the 41 untagged companies, and why the golden suite was rebaselined

2 September 2026, night. Follows finding 4 of `docs/handover-2026-09-02-night.md`.

## What was wrong

`selector/match_reference.py` joins `data/private-rounds.csv` to `data/private-companies-tags.csv` on
`company_key` and silently drops any round whose company has no tag row. Forty-one companies had no
tag row, so **58 rounds, 44 of them median-eligible, never reached a founder**. The correlation was
total: of the 93 companies that did reach the engine, none was missing from the tags file; of the 41
that did not, all 41 were.

## What was done

Forty-one tag rows added, taking the file from 94 to 135. Every value in every tag column was checked
against the vocabulary already in use across the other six tag files and the 94 pre-existing rows.
**Zero invented values.** Each row carries a `what_it_does` line written on how the company earns
money, not on how it markets itself, and a `taxonomy_note` wherever the supplied screening category
was reassigned.

**Result: all 184 rounds now reach the engine, up from 126.** The inventory's private count went from
178 to 236.

## Why the golden suite was rebaselined

The suite reported **28 of 43 profiles moved**, the largest move this project has recorded. That is
the point: the old baseline certified a state in which a third of the private evidence was invisible.
Peer lists cap at seven, so a better match displaces a weaker one; net, **63 private peers were gained
and 29 displaced**.

The moves are not noise. Fixtures gained the single most obvious comparable they were missing:

| Fixture | What it is | Gained |
|---|---|---|
| insforge | backend-as-a-service for AI agents | **Supabase**, matched on Postgres, Backend as a Service, Edge Functions. Tag evidence 3.8 to 11.2 |
| fyle | UK direct-to-consumer nail-care brand | **Olive & June**, a nail-care brand |
| nursa | per-diem marketplace for clinicians | **Incredible Health**, nurse hiring. Had one comparable, now two |
| levelten | renewable power purchase marketplace | **Xpansiv**, the carbon and renewable certificate exchange. Had **no** private comparable at all |
| bluerails | hotel booking infrastructure | **Brex**. Had one comparable, which breaks our own rule against pricing off one name |
| payabli, rainforest, moov, trolley, dots | payments | **Checkout.com, Mollie, MoonPay, Rapyd, Stripe**. All five went from 3 to 5 peers up to 7 |
| numida, perenna, tienda-pago, mondu | lending | **Atom Bank, Monzo, Kriya, Stenn, Clearco, Wayflyer** |
| smol, bokksu, finn, lyka, oda | consumer | **WHOOP, AG1, Packable** |

The payments and lending blocks are the answer to "the verticals a founder cannot be priced in at
all". Five payments fixtures were pricing off Marqeta and dLocal alone. Four lending fixtures were
pricing off almost nothing.

## One defect the rebaseline surfaced, and it is worth recording

`lyka` gained "AG1 (Athletic Greens)" and lost "AG1" in the same diff. That is one company under two
keys. **AG1's January 2022 round is carried in both round files**: `private-rounds.csv` as
`ag1athleticgreens` at 8.77x, and `private-rounds-consumer.csv` as `ag1` at 8.8x. Same round, same
1,315 post-money, same 150 revenue, both flagged median-eligible.

Until today the private-rounds.csv copy had no tag row, so it never reached the engine and could not
double count. **Tagging made the duplicate live.** It was caught by reading the golden diff, not by
any check.

The private-rounds.csv copy is now `in_medians = 0` with the reason in its `notes`. The row is not
deleted and the tag row is not removed: the round still votes, once, from the consumer file where a
consumer brand belongs. Median-eligible in that file went 114 to 113; 132 across both files, none
counted twice.

**The check this argues for**: nothing compares the two round files for the same company and month.
That is the same class of gap as the one in finding 4 of the night handover, and it belongs with the
file-versus-engine check as the next thing to build.

## State after

- All 184 rounds in `private-rounds.csv` reach the engine. 113 median-eligible in that file, 132 across both.
- `python3 tools/check_raw_coverage.py` PASS across three supplied files: 191 of 191, 49 of 49, 22 of 22.
- Post-money over revenue equals the stored multiple within 2% on every row, 0 failures.
- No `in_medians = 1` row lacking a multiple or either URL, 0.
- `python3 selector/golden.py` back to 0 of 43 against the new baseline.
