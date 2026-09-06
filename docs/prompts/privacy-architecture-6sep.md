# Prompt for another Opus: build the no-storage reveal

Fairway. Build the architecture in which we never receive a founder's financial figures unless they
choose, after seeing their football field, to send them for review.

Read `claude/Fairway_STATUS_2026-09.md` in the project first, then `docs/RULES.md`, then
`selector/reveal_payload.py` and `reveal-client.js`. Work from a fresh clone of origin in the cloud.
Never run any git command on Daniil's laptop, including read-only ones; write the files and hand him
`git add -A`.

## What Daniil asked for, in his words

"Is there a way to do all the same for the founder WITHOUT storing his financials? So we say
transparently, we only take a record of the company data (profile, website), without storing the
numbers. Then he gets the reveal based on the numbers he put in (we still do not see any financials
at that point). Then if the user wants to have his numbers and ff reviewed, he presses a button and
it comes through to us, in which case he would specifically agree for us to see it."

## Why this is nearly free, and what the boundary actually is

The engine already computes every peer chart with NO founder figure. That is not a coincidence: the
whole payload is built that way, `founder_metric_for` returns None when a figure is absent, and the
multiplication was deliberately left on the page rather than in the payload. So the server side is
already shaped for this.

The boundary is between SELECTION and PRICING, and it was measured on 6-Sep rather than assumed:

- **Selection needs two ratios and nothing else.** `growth` gates which private rounds a founder is
  compared against (`band_compatible`) and ranks peers (`g_rank`); `gm` decides whether the reveal
  leads on revenue or gross profit (`denominator`) and scores. Both are percentages. Neither says
  anything about the size of the business.
- **Revenue touches selection in exactly one place**, `_one_round_per_company`, as a tie-break
  between two rounds of the same company an order of magnitude apart, and it degrades to no
  preference when absent. Confirm this is still the only place before you rely on it.
- **Everything else is pricing.** Revenue, ARR, book value, net income, originations, every user
  count: used only to multiply a peer multiple. They never need to leave the browser.

## What to build

1. **Stop sending the figures.** `reveal-client.js` currently posts `revenue`, `revenue_exact`,
   `arr_exact`, `profit` and `raise` to `/api/reveal`. The default request must carry the profile
   (company, website, tags, country, stage), `growth` and `gross_margin`, and no absolute figure.
2. **Multiply on the page.** The payload's ranges carry `low`, `mid`, `high` per lane per basis, and
   `charts` carries the same in Daniil's reading order. The page computes `founder_low = figure x
   low` from a value held in a JavaScript variable. `tools/check_reveal_payload.py` already
   recomputes exactly this arithmetic server-side for the fixtures, so use it as the specification.
   Do NOT use localStorage or sessionStorage for the figures.
3. **The consent button.** "Send my numbers for the banker review" posts the figures explicitly, in
   one request the founder triggers, with wording on the button that says what is being sent and to
   whom. Nothing is sent before that click. The 24-hour free banker read is the thing it buys, so
   the button belongs beside that promise.
4. **Say it on the page, before the quiz.** One plain sentence: we do not receive your revenue
   figures; the comparables are chosen on your growth rate and your margin, and the multiplication
   happens in your browser. `docs/lead-capture.md` holds the privacy copy; the disclaimer in
   `index.html` has to match what the code does, not the other way round.
5. **A check that keeps it true.** Add to `tools/check_all.sh`, in the shape of check 14. It must
   fail if the default request body contains any field outside an allowlist of profile fields plus
   `growth` and `gross_margin`. The lesson of the last two days is that a boundary with no check is
   a boundary that quietly moves.

## Constraints that bind you

- **Two things still cross, and the page must not pretend otherwise.** Growth and gross margin are
  needed for selection. They are ratios, not amounts, and the copy should say exactly that rather
  than claiming we receive nothing.
- **The paid reveal is a separate question.** The $250 and $750 tiers involve a banker and possibly
  a model reading the figures. That is what the consent button is for. Do not quietly route figures
  to `config/reveal-prompt.js` on the free path.
- **Rule E8 as amended on 6-Sep.** The free tier already sends the public lane complete and every
  other lane blurred with comparable names and dates but no figures. `build(prof, tier='free')` does
  this. The privacy work sits on top of it and must not weaken it.
- Never drop a row silently; count in and count out on every change. No figure from your own head.
  No em dashes. Plain words, short sentences.
- Run `FAIRWAY_NO_GIT=1 sh tools/check_all.sh` before and after every change. Golden must not move
  without the reason written down. It is fifteen checks today and check 1 is RED by design because
  the public pull is not loaded; every other check must stay green.

## Sequencing, and this matters

**The page does not read the payload at all yet.** `renderRecommendations` and `renderInvestors`
exist and nothing calls them; the football field is drawn from figures typed into `index.html`. So
this job and the engine-to-reveal wiring are the same job. Wire it the private way from the start
rather than wiring it openly and retrofitting.

## What to hand back

A short document: what you built, the request body before and after with the removed fields named,
what the new check asserts, the suite counts before and after, and the `git add -A` command for
Daniil. Flag anything that touches one of his standing instructions in the moment rather than at the
end.
