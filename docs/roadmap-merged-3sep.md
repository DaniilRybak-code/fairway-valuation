# Fairway: the one roadmap

**Rewritten in full: 4 September 2026, 19:05 UK (Fable), after Daniil correctly flagged that the
previous version still carried finished work as open.** The rule from here: this document has two
lists, DONE and OPEN. A finished item moves to DONE with a date the same day, and the body never
contradicts the log. No narrative sections that can silently go stale.

Pilot launches the week of **21 September 2026**. Eleven working days from 5 September.

Repo copy: `docs/roadmap-merged-3sep.md`.

---

## DONE — verified, with dates

**The 100-fixture gate: PASSED.** 102 real fixtures (43 → 102 on 3 Sep, Daniil's re-framed gate:
peer-universe depth, no revenue figures), 90 pass, 89 of 99 in-market, three hard-tech names
honestly OUT_OF_MARKET. Audited by Fable 4 Sep: all twelve checks pass, golden 0/102, the five
least-trusted tags check out against the companies' own pages, thin-lane diagnosis proven honest
by a planted comparable. *The only remnant: the march commit still needs `git push` from Daniil's
terminal (stale `.git/index.lock` to remove first) — that is an action below, not an open
workstream.*

**Engine data hygiene: DONE.** The file-versus-engine intake gate (`tools/check_intake.py`) and
the cross-file duplicate check ("no round votes twice") exist inside `tools/check_all.sh` — one
command, twelve checks, all passing (3 Sep, commits cc85d3a and e9ab546). The audit verdicts are
applied: **Klarna** restated at the pricing-date rate with entity named — $1,208.8m / 37.7x
(Jun-21) and $1,298.8m / 5.16x (Jul-22), Klarna Bank AB, per Fable's ECB pins; **LEAD School** on
the printed revenue-from-operations at 142.17x; **Starling/Upgrade** carry the Pre-money flag in
`valuation_status`; **Atom Bank** tagged pre/post-unspecified; **Oura** carries the
source-upgrade note. (3 Sep evening, e9ab546 — Fable failed to mark these on 4 Sep and the
previous version of this document wrongly listed them as open. That is what forced this rewrite.)

**Quiz testing: v1 DONE.** `tools/quiz_walker.py` walks the forks and already earned its keep:
seven questions whose answers reached nothing, now wired or flagged; `funding_model` was required
and unread, now selects the basis; `founder_metric_for()` carries the founder's own figure into
every range (a lender gets five valuations, not five multiples). (3 Sep, e9ab546.)

**Maths testing: first slice DONE.** `check_period_conversion.py` tests the run-rate/period
conversion against known answers; synthetic-revenue injection was proven to move selections and
reverted — nothing invented touches selection. Identity checks (post-money ÷ denominator =
multiple, 2% tolerance) pass across all priced rounds. (3 Sep.)

**Investors: Days 1–2 DONE.** 445-house table, both layers built and rendered (`investors.js`),
tag-overlap ranking on the shared tokeniser, geography fixed with a country table and a
two-founders test, compliance rails checked (no contact details, no incomplete cards), 92 of 92
callable houses render, 738 cards / 1,360 evidence chips across 102 fixtures, 7.2 houses per
founder. Daniil's ruling applied: unpublished cheque/geography no longer blocks a house. The
78-row enrichment applied as a source, not a patch. (3–4 Sep, 7195a84 → e16c4b4.)

**Data base (for the record):** 511 listed + 289 private load, nothing untagged, sector and
revised lending screens fully accounted (49→40+9, 22→13+9 with written reasons), Atom Bank as the
second priced book comparable, user-count sweep finished, basis/period audit standing (117
agreeing and rising), durability protocol + intake gate holding since 31 Aug.

**Service shell: decisions 3 of 4 DONE** (3 Sep working, `docs/service-shell-decisions-3sep.md`):
sole-trader path viable with drafted disclaimer text; three retention clocks designed (90 days /
6 years / de-identified with the re-identification caution); Stripe deferred, invoice the pilot.

---

## OPEN — everything that remains, in priority order

1. **Push the march** (Daniil, 1 minute): `rm ~/fairway-valuation/.git/index.lock`, then Opus's
   commit-and-push block from the 3-Sep night handover. Until then the 102 fixtures live on one
   laptop only.
2. **The empty-lane ruling** (Daniil, then Opus same day): nine fixtures pass with an empty lane.
   Fable's recommendation stands: three-state scoring (pass both lanes / pass one lane with the
   honest empty state rendered / fail), with the gate number quoting both. One word makes it
   buildable.
3. **Recommendations, Day 3** (Opus): unit-economics and market-position dimensions, and the
   renderer into the reveal. The last promised feature with no engine behind it.
4. **Engine → reveal wiring** (Opus, week of 8 Sep): ranges + honesty flags + recommendations +
   both investor layers as one payload into the reveal. The CONTEXT-tier sentence and the six
   honesty flags reaching a founder close inside this.
5. **Reveal render harness** (Opus builds, Fable reads): all 102 fixtures rendered headless,
   screenshot contact sheet, honesty strings asserted in place.
6. **The two sourcing pulls, one batch** (Daniil): the 17-lane peer pull
   (`docs/prompts/peer-sourcing-4sep.md`) + consumer-software/edtech funds for the investor
   screen — the same gap in both workstreams, one pull fixes both.
7. **The service shell, remaining** (Daniil words, Opus wiring): the currency of the 750 (one
   word — it blocks the price on the page and the "Free" meta-description fix); entity name +
   service address (disclaimer text drafted and waiting); **the SM&CR / outside-business-interest
   answer — gates the first payment, longest lead time**; the reviewer workflow built and
   exercised end to end (lead → banker review → 24h commentary).
8. **Landing round** (Fable, on Daniil's next markup): two-layer investor block is in; legal
   placeholders come out the moment entity + currency land.
9. **Backlog, explicitly not launch-blocking:** 101 private rows awaiting a human basis look
   (burns down inside future data touches) · the 58-round master file (unwired, 14 source URLs
   owed) · 192 listed CAGRs (Daniil's next refresh; those rows stay growth-invisible until then)
   · `asset_intensity` question wiring · revenue-carrying fixtures as post-launch hardening
   (the basis/period machinery is covered by `check_period_conversion.py` for now).

## The eleven days

**Fri 5 Sep:** OPEN items 1–3 land; 4 starts. **Mon 8 – Fri 12 Sep:** wiring week — items 4–5
built and green, 6–7 land, the reviewer workflow exercised once end to end. **Mon 15 – Thu 18
Sep:** dress rehearsal with five to ten friendly founders, real reviews on the clock, fix list
only, final landing round. **Week of 21 Sep:** pilot live; daily triage; nothing new ships but
fixes.

**Launch odds as marked 4 Sep 19:05 UK:** product-complete by 18 Sep ~85% — the march finishing
two weeks early bought real slack, and the remaining build risk is concentrated in the reveal
wiring and the reviewer workflow. Paid pilot on the 21st ~60–65%, gated almost entirely by the
SM&CR answer. Some launch on the 21st ~85–90% with the pre-committed fallback: free pilot, real
reviews, invoice when compliance clears.
