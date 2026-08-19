# The reveal engine: model in the loop, guard rails in the code

Every completed check now goes through a model with fixed settings and a verified data pack. This is how it is wired, what it costs, and where it will break.

## The shape

```
answers  ->  /api/reveal  ->  anchor band from data/comps.js
                              |
                              +-> Claude, system prompt from config/reveal-prompt.js
                              |   constrained to a corridor, forced tool output
                              |
                              +-> guard rails in code
                                  |
                                  +-> pass: range, basis sentence, 4 reference points, 3 concerns
                                  +-> fail: deterministic range, no reference points
```

Three files hold everything a non-engineer would want to change:

- **`config/reveal-settings.js`** the dial panel. Model, temperature, corridor width, range width limits, how many reference points and how many are visible, rate limit, timeout.
- **`config/reveal-prompt.js`** the system prompt. How it reasons, the tone, the six non-negotiable rules.
- **`data/comps.js`** the verified pack. Nothing enters this file that we cannot attribute to a named source with a vintage.

## The rule that matters

**The model never invents a number and never states a figure without a source.**

Two mechanisms enforce it rather than requesting it.

First, the model does not choose the range freely. The code computes an anchor from the pack, widens it into a corridor, and tells the model it may position inside that corridor and nowhere else. Output outside gets clamped, and the clamp is recorded. So the worst case is a badly positioned range, never an absurd one.

Second, every reference point must carry a source string. Anything without one is dropped before rendering. If fewer than two survive, the whole response is discarded and the founder gets the deterministic range with no reference points at all. Showing nothing is a fine outcome. Showing a fabricated comparable round is not: a founder who checks one and finds it does not exist is gone, and so is the referral behind them.

## What the founder sees

Result screen appears immediately with the first-pass range, so nothing waits on the network. A card slides in under it, "What the range is built on", showing four skeleton rows while the engine runs. Ten to twenty seconds later the four reference points populate: the first two open with their sources printed, the last two blurred behind a Locked tag. The range updates if the engine moved it, and the line under the range becomes the basis sentence, something like:

> Positioned against the Seed median post-money of $24M for Q4 2025 (Carta), less the midpoint of the stated raise, adjusted up for growth above 15% a month. Market data vintage 2025-Q4.

The visible wait is deliberate. Work that takes a moment and then shows its sources reads as work. An instant number reads as a calculator.

## Reference point design

Four anchors, ordered by how much they support the number, two shown and two locked. The prompt asks for a mix:

- **market**, drawn from the pack with the source named
- **method**, for example what an ARR multiple implies against what the stage benchmark implies, and where the two disagree
- **positioning**, placing this company against the cohort on growth or profitability

The locked two should be the ones a founder would most want to read, with labels specific enough to sting. That is the deprivation lever, and it is honest here because the paid report genuinely does show the working.

## Geography

Deliberately not segmented. Carta's data is predominantly US and the US generates most of the data points, so it is the spine. The prompt is told the anchors are US-weighted and instructed to adjust explicitly, with a note in the basis sentence, rather than applying a silent regional discount. Country comes from the Vercel edge header. When the reviewers are ready to put real regional multiples into `COMPS.regions`, the engine picks them up with no code change.

## What it costs and how fast

Roughly 2,500 tokens in and under 1,000 out per check, so cents rather than pounds at the volumes this will see. Vercel gives 300 seconds of function duration even on Hobby with Fluid compute, so the call comfortably fits in the request path; the timeout is set to 25 seconds because a founder should not wait longer than that.

Identical answer sets are cached for 24 hours, which keeps cost down and means two founders with the same profile see the same number. Temperature is zero for the same reason. There is a per-IP rate limit because an unauthenticated endpoint that calls a paid API is otherwise someone else's free compute.

Contact details are never sent to the model. It receives the nine answers, the free text and the country, and nothing that identifies a person.

## Setup

One environment variable in Vercel: `ANTHROPIC_API_KEY`. Optionally `ANTHROPIC_MODEL` to pin a version; check the current model list before pinning rather than assuming an identifier still exists. Without the key the endpoint returns the deterministic range and the site behaves exactly as it does today.

## Known limits, in order of how much they matter

1. **The dispersion around the anchor is an assumption.** The pack has medians, not percentiles, so the corridor is built with placeholder multipliers marked as such in `api/reveal.js`. Replacing them with real p25 and p75 figures is the single highest-value improvement available.
2. **The sector overlay is empty.** The prompt is told not to state sector multiples as fact, so sector currently affects the investor list and not the range. An afternoon with the reviewers fixes this and it is the part no competitor can copy.
3. **No Pre-seed anchor.** The cited Carta release covers Seed and Series A. Pre-seed falls back to patterns and the copy says so.
4. **Web search is off.** The setting exists. Turning it on gets fresher sector multiples at the cost of latency, and every figure returned still needs a source before it renders. Verify the current tool version string before enabling.
5. **Cache and rate limit are per instance.** Serverless means several instances, so both are best-effort. Fine at this volume, worth moving to KV if traffic grows.

## The loop that makes it better

Every reviewer correction is a labelled example. When a banker moves a range in the 24 hour email, that says the anchor or the positioning was wrong for that cell. Log the correction next to the inputs in the leads sheet and after about thirty of them the pack can be tuned against reality rather than against judgement. That is also the thing that eventually justifies a licensed data feed.
