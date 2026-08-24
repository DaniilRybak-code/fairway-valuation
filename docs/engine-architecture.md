# Fairway reveal engine: profiler and selector

The agreed high-level architecture. Recorded 24 August 2026 because it existed only in conversation.
If anything below conflicts with something else in this repo or the project docs, THIS FILE WINS.

---

## The shape

```
quiz answers + website
        |
  [1] PROFILER - one LLM call
      in:  ~3,000 tokens (website text + answers)
      out:   ~200 tokens (just the tags)
        |
  [2] SELECTOR - code, zero tokens
      reads the CSVs, applies core/secondary,
      quality floor, recency window
        |
      5-10 named comps
        |
  [3] COMMENTARY - second LLM call
      in:  ~1,500 tokens (the selected rows only)
      out:   ~800 tokens
```

Roughly **5,500 tokens per founder.**

---

## The rule that makes it cheap and honest

**The 250-odd comparables NEVER enter a prompt.**

The model decides WHAT KIND of company we should compare to. Code finds the actual names.

If the model had to read the database to pick names it would cost 40,000+ tokens per check and it
would still invent comparables. This extends the rule already committed to in `docs/reveal-llm.md`,
*"the model never invents a number and never states a figure without a source"*, from numbers to names.

There are TWO pieces, not three. An earlier discussion referred to a "JSON contract" as a third
component. It is not one. It is only the field names the profiler and selector agree on.

---

## [1] Profiler

One LLM call. Reads the quiz answers AND the founder's website. Outputs tags, nothing else:
archetype, archetype_secondary, industry, function, buyer, gtm_motion, revenue_model,
product_role, ai_stance, product_tags.

**The website is load-bearing, not optional.** The quiz field already exists (`index.html`,
"Your website") and nothing reads it. Two reasons it matters more than it looks:

1. `product_tags` is the heaviest weight in the matcher, capped at 12 points against 3 for
   archetype, and product tags are close to underivable from a dropdown. "SaaS / B2B software"
   says nothing. The website says "restaurant point of sale with embedded payments sold to
   independent operators." Without the site the strongest matching dimension runs nearly empty.
2. Sector dropdowns are coarse and founders self-describe badly. The site is ground truth.

**Security constraint.** A fetched page is untrusted text. The profiler must be constrained to
emit ONLY values from the fixed tag vocabulary, and anything outside it is dropped rather than
passed through. Numbers still come from code, so a hostile page can at worst produce a wrong
comparable set, never a wrong valuation.

---

## [2] Selector

Plain code. No model. Four rules, each of which fixed a real observed failure:

1. **Business nature selects.** No size filter, no time filter. Size is displayed beside every
   name and never includes or excludes one.
2. **Core and secondary groups, membership decided BEFORE ranking.** One ranked list cannot do
   two jobs: scored against the whole universe, a healthtech founder gets Guidewire above Veeva.
   Core = strong on what it does AND who it sells to. Secondary = same business model, different
   end market. The gap between the two ranges is the finding, not a defect.
3. **Quality floor.** Relative, roughly 45% of the best score with an absolute minimum. Below it a
   name is not a comparable and is not shown, even if that means three names instead of five.
   Without this a consumer-neobank profile returned Perplexity at 142.9x as its fourth comparable.
4. **Recency orders, it does not select.** Most recent qualifying transaction per company; widen
   the window until there are enough QUALIFYING names, never by lowering the bar.

Plus one on the data side: rows carrying `in_medians=0` stay visible but come out of every median.

---

## [3] Commentary

Second LLM call. Receives only the selected rows. Writes the ranges, the drivers and the
positioning. Guard rails stay in code exactly as `docs/reveal-llm.md` already specifies.

---

## What this architecture guarantees

- **Adding names to existing sectors requires no engine change.** Drop rows in the CSV.
- **Adding new archetypes or revenue models requires no engine change.** Vocabulary is a data
  file. Proven: the ten financial archetypes and four revenue models added for the fintech set
  required no matcher change at all.
- The matcher contains exactly ONE hardcoded vocabulary value, `'Horizontal'`, used as a sentinel
  in five places. This is verified, not assumed, and must stay true.
- Weights live in a config object, never in code, so tuning is a config change.

**Golden tests are built BEFORE the engine.** Roughly 20 founder profiles with their expected
comparables, snapshotted. Any later change then produces a readable diff rather than a silent
shift. This is what makes it safe to wire the engine now and deepen the data afterwards.
