# Matching refinement, 6 September 2026 (Fable)

Written 6 September 2026, 12:05 UK, in a fresh clone of origin at `fb260b2`. No git ran on the
laptop. **Nothing in the engine or the data was changed.** Every figure below was measured on a
scratch copy of the engine by `tools/measure_matching_variants_6sep.py`, and every measurement can be
re-run with the command beside it. The suite was run before and after (both times: gate 95 of 102,
golden 0 of 102 moved, check 1 red on the unloaded public pull, the other fourteen green).

**The one-paragraph version.** The three fixtures in task (1) are not matcher failures: levelten
and tash are sourcing gaps (the only true comparables we hold either carry no revenue multiple or
are held out of the medians), and manifold-robotics has one direct comparable and nothing else
that a defensible rule can reach. No change I measured lets a real comparable through for them
without letting a wrong one through, so they stay on the No-comps list for the bulk pass. The
taxonomy rule (task 2) moves 29 of 102 fixtures, costs one gate pass, and the names it removes are
label-only names. The biggest finding is in task (3): **the token-weight file that decides which
words count as product vocabulary is stale.** It was last computed on 24 August from five tag
files; there are seven now and the private set has more than tripled. 193 words that are generic
by the file's own rule ("own", "health", "warehouse", "freight", "deposit") carry full weight, and
246 of the 1,185 core and private comparables shown today are admitted on generic words alone (a
clinical-trials marketplace is shown eBay, Etsy, Whatnot and Vinted on the word "marketplace").
Regenerating the file is not a new rule; it is the existing rule run on the current data. It
changes 75 of 102 fixtures, surfaces one more human-verified peer, and needs Daniil's eyes because
of its size, so it is proposed and not applied.

---

## What Daniil has to decide, in order

1. **Regenerate the token-weight file** (task 3, the big one). Yes or no. If yes, the command is
   at the foot; it rebaselines golden for 75 fixtures with the reason written in this document.
2. **The taxonomy rule** (task 2). The measurement is below. Ruling only; not before the pilot.
3. **Four re-tags** (task 3): ultrasonium's end market, Owner's secondary archetype, AuditBoard's
   primary, and whether apollo-atomics keeps its tag. Each with its measured effect.
4. **Nothing for task (1)**: the recommendation is to leave the three fixtures on the No-comps list.

---

## Task 1. levelten, manifold-robotics, tash

**How to read the tables.** For each fixture I listed every private round that shares an archetype
slot with the founder, which is the widest pool the engine could ever reach for it, and asked the
engine's own fences, in the order they run, which one stops each round. The full tables (36, 21
and 36 rounds) are in Appendix A; reproduce with
`python3 tools/diagnose_private_lane_6sep.py`.

**One correction to the brief's list of reasons.** "Outside the 24-month window" is no longer a
reason a round does not price. Since 26 August the window is an output, not a fence: the engine
reports the age of the oldest round it shows, and nothing is excluded for age. The rounds shown to
levelten and tash are 64 months old (The Zebra, April 2021), which is a caveat on the page rather
than a filter. So each round falls to one of: the family gate, the relevance gate, the score
floors, or having no revenue multiple on the founder's basis.

### levelten (power purchase agreement marketplace; Market Infrastructure & Exchange, secondary Third-Party Marketplace; Energy & Utilities)

36 rounds share a slot. **33 are stopped by the family gate**, correctly: they are the consumer
marketplaces (Vinted, Whatnot, Meesho, Faire, StockX, Flipkart and the rest), which carry the
Third-Party Marketplace label and nothing else in common with a power-purchase exchange. 1 is
stopped by the relevance gate (Blockchain.com, a crypto exchange, shares only the archetype label).
**2 are picked**: Xpansiv (July 2022, the environmental-commodities exchange, the one true
comparable, DIRECT tier) and The Zebra (April 2021, a car-insurance comparison site, ADJACENT).

Why the lane does not price: **Xpansiv carries no revenue multiple.** Its row prices only on
throughput, dollars per tonne of CO2 cleared, on Daniil's 3-Sep ruling, and we hold no other row in
that unit, so it is a single point. The Zebra prices at 6.67x but it is one name, and it is in the
lane on the word "marketplace" alone (worth 0.07 points; see task 3). So levelten has one real
comparable with no revenue figure and one weak one with a figure. **That is a sourcing gap, and the
thin-lane diagnosis already lists it as one of the three genuine sourcing requests.** No matcher
change reaches a second real name because the pool holds none.

### manifold-robotics (warehouse robotics as a service; Commerce Enablement & Fulfilment, secondary Design & Engineering; Horizontal)

21 rounds share a slot. **1 is picked**: Berkshire Grey (March 2023, 5.69x net, a control
transaction), a DIRECT hit on three whole tags. **10 are stopped by the relevance gate** (they share
only the label: the Indian parcel carriers Xpressbees and Delhivery, E2open, and the agri and
grocery supply-chain rows). **8 are stopped by the family gate**: the design-software rows (Figma,
Miro, Canva, Framer, Lovable), Applied Intuition, and **Vention** (January 2026, industrial
automation cells, 10.0x on a gross label), which is the one row that is arguably a real adjacent
comparable. 1 is below the absolute score floor (Packable), 1 is held out of the medians
(Shiprocket).

Why Vention is three fences deep, and why I do not propose opening them:

- **The family gate.** Vention carries BOTH of manifold's archetypes, swapped (primary Design &
  Engineering, secondary Commerce Enablement & Fulfilment). Family is learned from the primary
  archetype by majority vote, so Vention is filed under software and manifold under consumer. I
  measured two bridges. A bridge on "shares both archetype slots" changes 5 fixtures and does not
  move manifold. A bridge on "carries the founder's primary archetype in either slot" changes 17
  fixtures, and one of the names it admits is Vention into sellerclaw, a merchant-account operator:
  a wrong comparable through. Rejected.
- **The relative floor.** Even with the family gate open, Vention scores 7.2 against Berkshire
  Grey's 26.5, and the lane keeps only names above 45 per cent of the best score, which is 11.9.
  One excellent comparable evicts every second one. I measured a top-up that reaches below the
  relative floor (never below the absolute floor of 5.0, never through the archetype fallback,
  only when the lane cannot price two names). It moves tash to PASS by admitting **Carta**, a cap
  table software company, into a trading-card platform: a wrong comparable through. Rejected.
- **The basis label.** Vention is labelled GROSS_REVENUE. Under rule B3's ownership test (does the
  line hold money that belongs to somebody else) a company that designs, builds and ships its own
  automation hardware keeps the whole sale price, which is NET in our sense. Claude flagged this
  row as a doubtful call on 5 Sep. If it is relabelled net AND the two fences above were opened,
  manifold's net lane would hold two names. Three changes to move one fixture, two of them measured
  as letting wrong names through elsewhere. Not proposed; the label question goes to the B3 audit.

**Verdict:** manifold-robotics stays on the No-comps list. What it needs is a second
warehouse-automation round in the bulk pass, not a looser matcher.

### tash (investing platform for sports and trading cards; Wealth & Capital Markets Platform, secondary Third-Party Marketplace; Financial Services)

36 rounds share a slot. **2 are picked**: The Zebra (net, 6.67x, on the word "marketplace") and
Raisin (a savings marketplace, gross, 6.43x, DIRECT on the shared end market and archetype). One
net round and one gross round, so each reading holds one name and neither is a range, exactly as
the brief says. **33 are stopped by the family gate**, and among them are the two rows that ARE
tash's business: **Whatnot** (live-shopping for collectibles and trading cards, four rounds, shares
"Collectibles", "Trading" and "Marketplace") and **StockX** (collectibles resale, shares
"Collectibles"). 1 is stopped by the adequacy floor: Carta, DIRECT on label plus Financial
Services, at 8.0 against the 12.0 floor.

Why opening the family gate would not help: **Whatnot has never disclosed revenue.** All four rows
carry GMV only (2.5x on the August 2026 round, 1.66x on January 2025), and no fixture is offered a
GMV reading today (rule B8: "the football field wiring is not" done). StockX's 9.5x is a gross
ceiling held out of the medians on the 31-Aug ruling. So the two true comparables cannot price on
any reading the fork offers, and the names the gate would let through beside them are Vinted,
Meesho and Back Market: second-hand clothing and phones. **Verdict:** tash stays on the No-comps
list. Its answer is either a GMV reading (post-launch wiring, and then Whatnot and StockX are a
two-name GMV range if the family gate is bridged for them) or a second collectibles round with a
revenue figure in the bulk pass.

**One thing task 1 did find, and it is task 3's finding too:** The Zebra reaches both levelten and
tash on a single shared word, "marketplace", worth 0.07 points. Carta is DIRECT-tier for tash on
the label Wealth & Capital Markets Platform plus Financial Services, held out only by the score
floor; that label is as much a catch-all as the four in the taxonomy proposal.

---

## Task 2. The taxonomy rule, measured

The rule: for Vertical Software, Data AI & Developer Tools, Business Applications and Cloud &
Infrastructure, an archetype match counts only when the industry field matches too (Horizontal
equals Horizontal). Applied on a scratch copy everywhere the engine tests archetype equality: the
score, the tier, the relevance fallback, axis A and axis B. `_anchored` already demands the industry
and is unchanged. Command: `python3 tools/measure_matching_variants_6sep.py taxonomy`.

**102 fixtures in, 102 snapshotted, 0 dropped. 29 change peers. 21 gain at least one name. 29 lose
at least one name. Gate 95 to 94.** The one verdict that moves is alloovium (construction document
AI, Vertical Software plus Real Estate), whose private lane today is Applied Intuition (vehicle
simulation) and Clio (legal software), both label-only; under the rule it loses them and gains
nothing that prices, so it fails honestly instead of passing on names that were wrong.

What the rule removes, by name, is what it promised to remove:

| fixture | what it is | loses | gains |
|---|---|---|---|
| edviro | AI for energy infrastructure (Vertical Software, Energy) | Owner (restaurants), Mews (hotels), Sapiens (insurance), Clio (legal), AuditBoard (audit): five vertical-software rows from five other industries | nothing on the private lane; private priced 5 to 2, still a range |
| open-wearables | wearable health data infrastructure (Vertical Software, Healthcare) | Twilio, Agora, Cloudflare, Datadog, Sinch from core (Cloud & Infrastructure label, Horizontal) | Veeva, Waystar, Weave, Tecsys (healthcare software) |
| publora, browseract, skybridge, context-dev, anysearch, magma, atlas-new | AI developer tools | TomTom (maps; carried Data, AI & Developer Tools with an Automotive industry) | Agora, Akamai, IONOS, Teradata in the freed seats |
| care-gp, levocred, payna | vertical founders in healthcare, lending, compliance | Owner, Restaurant365 (restaurant software) | |
| upstream, bond, osmaura, clarify | horizontal business applications | Gorgias, Restaurant365, TravelPerk (vertical rows) | PayFit, Calendly, Jasper, Buffer (horizontal rows) |

Whether the archetype FALLBACK (the recorded rescue) also obeys the rule makes no difference on the
102: measured both ways, identical result
(`python3 tools/measure_matching_variants_6sep.py taxonomy_fallback_raw`).

**My read, for the ruling.** The rule does what the 5-Sep review said it would: it stops a
restaurant back-office system being a comparable for a grid-operations company, at the price of
one honest failure. It is ready to build after the pilot. Two labels outside the four behave the
same way and are worth adding to the list when it is built: Wealth & Capital Markets Platform
(Carta is DIRECT-tier for a trading-card platform on it) and Commerce Enablement & Fulfilment
(parcel carriers and warehouse robots share it).

---

## Task 3. The tags

### 3a. The two hardware fixtures

**ultrasonium** (metal manufacturing to order; Owned-Inventory Retail, secondary Design &
Engineering, industry Horizontal). Today it fails on the listed lane and is served Moove, Quince,
Olive & June, Flink and Octopus Energy on the private lane by the fallback, all recorded.

| change measured | listed core becomes | private lane becomes | gate |
|---|---|---|---|
| archetype to Design & Engineering, industry unchanged | Mensch und Maschine, Roper, **DocuSign** (shares the word "contract": Contract Manufacturing against Contract Management) | Vention, Applied Intuition, **Figma, Miro** (fallback) | FAIL to PASS, falsely |
| **industry Horizontal to Manufacturing, archetype unchanged** | **PTC, Dassault Systemes, Lectra**; secondary Kinaxis, **Xometry** (on-demand manufacturing), MonotaRO | unchanged (Moove, Quince and the rest, still recorded) | FAIL to PASS |
| both | PTC, Dassault, Lectra; Xometry in secondary | Vention, Applied Intuition, Figma, Miro (fallback) | FAIL to PASS |

**Proposal: change the industry to Manufacturing and leave the archetype.** The end market is
what the profile was missing: it sells to manufacturers, and the seven rows tagged Manufacturing
include Xometry, which is the closest listed business to it we hold. The archetype change alone is
a trap: it passes the gate on DocuSign. Whether to ALSO move it to Design & Engineering, as A11's
second clause says, is Daniil's call; it swaps the private nonsense from consumer retail to design
software, both recorded, and keeps Vention. The private lane is a hole under every tag.

**apollo-atomics** (compact nuclear reactors; Owned-Inventory Retail, secondary Design &
Engineering, Energy & Utilities). Fails on the listed lane, no range at all. Moving it to Design &
Engineering leaves it failing and swaps Octopus Energy and Enpal (energy companies, reached on the
shared end market) for Figma and Miro through the fallback. **Proposal: keep the tag.** The energy
end market is doing the only useful work here.

### 3b. The 24 tag rows Claude wrote on 5 September

I checked where each row is actually served (Appendix B has the table). Verdicts:

| row | verdict | reason |
|---|---|---|
| Slash, BVNK, Moss, Juspay, Cashfree, Zuora | keep | land in the payments lanes they were sourced for (agentcard, unifold, paymentkit, moov, dots, trolley, rainforest) on whole shared tags |
| Spinny, Suno, Framer, Genspark, Legora, Mercor, Micro1, Sapiens, Accolade, Udemy, Restaurant365, Berkshire Grey, E2open, Applied Intuition | keep | each serves the founders it was sourced for on real tags (Mercor and Micro1 are what flipped clera, standout and tsenta; Accolade serves insurf and evergrove on Payer Decisioning and Care Coordination). Where they also reach a wrong founder it is on a generic word, which is 3c |
| **Moove** (Owned-Inventory Retail, secondary Lending & Credit) | keep, flagged | it is a vehicle-finance business, and the label is a stretch, but no better one exists in the vocabulary and it is finn's best comparable (25.9 on Car Subscription, Owned Vehicle Fleet, EV Fleet). The nonsense it serves (ultrasonium, oda on the word "own") comes from those fixtures' tags and the stale weights, not from Moove's row |
| **Vention** | keep the tags, **audit the basis** | GROSS_REVENUE looks wrong under B3's ownership test: it ships its own hardware and keeps the sale price. Belongs in the standing B3 audit, read against the source in the row |
| **Owner** (Vertical Software, secondary Marketing & Customer Engagement) | **drop the secondary** | measured: the secondary only ever served non-restaurant founders. Owner reaches 12 fixture-lanes today; marble (restaurant back office) on real tags, the other eleven on "ai", "operations" or "business". Dropping the secondary removes it from six of them (fundraisly, elentaria, pazi, clarify, lightfield, akkari), gate unchanged, and it stays with marble |
| **AuditBoard** (Vertical Software, industry Horizontal) | swap to Business Applications primary, Vertical Software secondary | "Vertical Software" with industry "Horizontal" contradicts itself; audit and compliance workflow sells across industries. Measured: 0 fixtures move today, so this is a tidy, not a fix |

### 3c. Rows served as nonsense, and why

The archetype fallback fired for 2 lanes and both are recorded in check 8 (blindspot's listed lane,
ultrasonium's private lane). Those are the only two "served on a label". **The larger problem is
comparables served on a word.** The relevance gate's vocabulary route accepts any shared token
above zero, and the weight that makes a token nearly worthless comes from a file that has not been
regenerated since 24 August. Measured today (`python3 tools/measure_matching_variants_6sep.py none
--weak-words`): **246 of 1,185 core and private members are admitted with no whole tag in common and
every shared word carried by 25 or more companies.** Examples: inato (clinical-trials marketplace)
is shown eBay, Etsy, PDD, Whatnot, Vinted, Udemy, Faire and Meesho on "marketplace"; bond is shown
Zuora and BlackLine on "to" (from Quote To Cash); Owner reaches nine founders on "ai"; The Zebra
reaches levelten and tash on "marketplace"; Moove reaches oda on "own".

**The weight file, measured** (`python3 tools/regenerate_token_weights_6sep.py --dry-run`): 7 tag
files, 770 tag rows in. 400 tokens are generic by the file's own rule (carried by more than five
companies); the committed file lists 207; **193 generic words are absent and carry full weight**
("deposit" 32 carriers, "freight" 28, "own" 21, "warehouse" 15, "fulfilment" 15, "health" 14).
Of the words it does list, "lending" has gone from 16 carriers to 73, "credit" 28 to 87, "bank" 12
to 59, "consumer" 37 to 92, each still at its August weight. The old script,
`selector/regenerate_token_weights.py`, reads three files out of `git show` at a path that no
longer exists and does not read the lending or logistics files at all.

**What regenerating does** (`python3 tools/measure_matching_variants_6sep.py weights`): 75 of 102
fixtures change peers, 56 gain a name, 66 lose one, **gate 95 to 94**, human-verified peers
surfaced **15 to 16 of the 29 we hold**, generic-word admissions 246 to 216. The changes I read are
for the better: inato's private lane goes from Whatnot, Vinted, Udemy, Faire, Meesho to Aledade,
Incredible Health, Doctolib, Cityblock Health and DeHaat, and its core from eBay, Etsy, PDD to
Waystar, Phreesia, Tecsys; Owner leaves fundraisly, Clay and Semrush leave with it. The one gate
loss is mondu (B2B buy-now-pay-later): its listed side improves (book range 2 to 4 names, Klarna
and Upstart in) and its private ARR range drops from two names to one because Happy Money, a
consumer debt-consolidation lender it reached on the word "credit", falls out and the lane does
not reach for another. That exposes a pre-existing weakness, recorded below, not a fault in the
weights.

**Variants measured on top of the fresh weights, all rejected, with the numbers:**

| variant | what it does | gate | human peers | verdict |
|---|---|---|---|---|
| stopwords | stops "to, a, an, as, in, on, at, by, with, from, per, vs, via, or" (today only and/of/the/for) | 94 | 16 | same result as weights alone on the 102; harmless, and it is what makes "Quote To Cash" stop handing out "to". Include with the regeneration if Daniil wants it |
| vocab50 | the vocabulary route needs a whole tag or a word carried by 50 or fewer companies | 93 | 16 | loses tienda-pago, mondu |
| vocab25 | ... 25 or fewer | 91 | 14 | loses acti, rainforest too |
| vocab10 | ... 10 or fewer | 81 | 15 | fallback fires for 35 lanes |
| specific_word (stale weights) | a word absent from the weight file, or a whole tag | 81 | | 92 fixtures change |
| lane_topup | the top-up counts a row as priced if it prices on any reading the lane offers | 92 | | counts one book name plus one ARR name as "two priced"; numida, kita, tienda-pago lose Zopa |

So the gate stays as it is. Tightening it costs real passes, and the honest treatment of a
comparable admitted on a generic word is the one A12 already prescribes for the fallback: **record
it**. Proposed and not built: `relevance_route` returns a fourth answer, "shared generic word only",
and check 8 prints those names under the No-comps list as a third kind of entry, so the bulk pass
can see them. No selection changes, no golden movement.

**Findings recorded, no proposal:** (i) for a lender, the private top-up counts a gross-revenue
row as a price, so mondu's lane sat at "two priced" on Kriya's 0.6x and never reached for a second
ARR name; a correct fix has to count two on the SAME reading and the simple version measured above
makes it worse. (ii) The industry vocabulary has near-duplicates that never match each other:
Retail & Commerce (4 rows: Shiprocket, Pine Labs, ElasticRun, Spinny) beside Retail & E-commerce
(55); Transportation & Logistics (Loadsmart) beside Logistics & Mobility (Xpressbees, Delhivery,
Moove); Real Estate & Construction (Better.com) beside Real Estate and Construction &
Infrastructure; Insurance (4 rows) beside Financial Services. Under the taxonomy rule these
spellings would matter, so they are worth folding before it is built.

---

## Task 4. The suite

Before: gate 95 of 102, golden 0 of 102 moved, check 1 FAIL (the unloaded public pull, by design),
checks 2 to 14 PASS. After: identical, because nothing in `selector/` or `data/` was touched. Three
tools were added: `tools/diagnose_private_lane_6sep.py`, `tools/measure_matching_variants_6sep.py`
and `tools/regenerate_token_weights_6sep.py`. The control variant (`none`) snapshots 102 of 102 and
moves 0, which is how the measurer is known to be measuring the engine and not itself.

---

## Commands for Daniil

To commit this session's tools and documents (nothing else changes):

```
cd ~/fairway-valuation && rm -f .git/index.lock && git add -A && git commit -m "Matching refinement measured: three fixtures diagnosed, taxonomy rule 29 of 102, stale token weights found (193 generic words at full weight), re-tags proposed

Fable, 6-Sep. Nothing in the engine or data changed. Three tools added and one document.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DZUddHXsVGtwUWxWNxGgLu" && git push
```

If the answer to decision 1 is yes, this regenerates the weight file, rebaselines golden (75
fixtures move, reason: this document, section 3c), and runs the suite:

```
cd ~/fairway-valuation && rm -f .git/index.lock && python3 tools/regenerate_token_weights_6sep.py && python3 selector/golden.py --write && sh tools/check_all.sh
```

Then, if the suite reads gate 94 and only check 1 red:

```
cd ~/fairway-valuation && git add -A && git commit -m "Token weights regenerated from all seven tag files; golden rebaselined, 75 of 102 fixtures, reason in docs/matching-refinement-6sep.md 3c" && git push
```

The re-tags (3a, 3b) are not applied. Each is one line in `selector/golden_profiles.py` or one row
in `data/private-companies-tags.csv`, and the measured effect of each is above.

---

## Appendix A. Every held round, and the fence that stops it

Columns: company, round date, months old at August 2026, net multiple, gross multiple, in the
medians, the fence. "family gate" means the row sits in a different business family (consumer,
software, fintech) and shares no specific end market with the founder. "RELEVANCE GATE" means it
shares only the archetype label, which the fallback could reach if the lane could not price at all.

### levelten, 36 rounds

| company | date | age | net | gross | in med | why it does not price |
|---|---|---|---|---|---|---|
| Xpansiv | Jul-22 | 49m | - | - | Y | PICKED; no revenue multiple (throughput only, one point) |
| The Zebra | Apr-21 | 64m | 6.67 | - | Y | PICKED; one name, admitted on the word "marketplace" |
| Blockchain.com | Mar-22 | 53m | - | 9.33 | Y | relevance gate: archetype label only |
| Back Market | Jan-22 | 55m | - | - | Y | family gate |
| Ankorstore | Jan-22 | 55m | - | - | Y | family gate |
| Meesho | May-24 | 27m | 4.20 | - | Y | family gate |
| Meesho | Sep-21 | 59m | 45.80 | - | Y | family gate |
| Faire | Nov-25 | 9m | - | - | N | family gate |
| Faire | Nov-21 | 57m | - | - | N | family gate |
| Whatnot | Aug-26 | 0m | - | - | N | family gate |
| Whatnot | Oct-25 | 10m | - | - | N | family gate |
| Whatnot | Jan-25 | 19m | - | - | Y | family gate |
| Whatnot | Jul-22 | 49m | - | - | N | family gate |
| Vinted | Apr-26 | 4m | 7.30 | - | Y | family gate |
| Vinted | Oct-24 | 22m | 8.40 | - | Y | family gate |
| Vinted | May-21 | 63m | - | - | Y | family gate |
| Vestiaire Collective | Sep-21 | 59m | - | - | N | family gate |
| GOAT Group | Jun-21 | 62m | - | - | N | family gate |
| StockX | Apr-21 | 64m | - | 9.50 | N | family gate |
| Flipkart | Jul-23 | 37m | - | 5.20 | N | family gate |
| Flipkart | Jul-21 | 61m | - | 6.40 | N | family gate |
| Trendyol | Aug-21 | 60m | - | - | N | family gate |
| Loadsmart | Feb-22 | 54m | - | 5.20 | Y | family gate |
| Loadsmart | Nov-20 | 69m | - | 4.00 | Y | family gate |
| Ninjacart | Dec-21 | 56m | - | 7.10 | Y | family gate |
| Vegrow | Dec-23 | 32m | - | 6.68 | Y | family gate |
| ElasticRun | Feb-22 | 54m | - | 10.36 | Y | family gate |
| Glovo | Dec-21 | 56m | - | - | Y | family gate |
| Wolt | Nov-21 | 57m | 23.50 | - | Y | family gate |
| Dream Sports | Nov-21 | 57m | - | 23.40 | Y | family gate |
| Udemy | Dec-25 | 8m | - | 1.29 | Y | family gate |
| DeHaat | Oct-22 | 46m | - | 4.50 | Y | family gate |
| Loft | Mar-21 | 65m | 14.70 | - | Y | family gate |
| SHEIN | Jan-24 | 31m | 1.40 | - | N | family gate |
| SHEIN | May-23 | 39m | 2.90 | - | Y | family gate |
| SHEIN | Apr-22 | 52m | - | - | N | family gate |

### manifold-robotics, 21 rounds

| company | date | age | net | gross | in med | why it does not price |
|---|---|---|---|---|---|---|
| Berkshire Grey | Mar-23 | 41m | 5.69 | - | Y | PICKED; one name |
| Vention | Jan-26 | 7m | - | 10.00 | Y | family gate (software); would also fall under the relative floor at 7.2 against 11.9; gross label doubtful |
| Applied Intuition | Jun-25 | 14m | 37.50 | - | Y | family gate (software) |
| Figma | Jul-24 | 25m | 17.90 | - | Y | family gate |
| Miro | Jan-22 | 55m | 58.30 | - | N | family gate |
| Lovable | Dec-25 | 8m | 33.00 | - | Y | family gate |
| Canva | Aug-25 | 12m | 12.70 | - | Y | family gate |
| Canva | Apr-24 | 28m | 11.80 | - | Y | family gate |
| Framer | Aug-25 | 12m | 40.00 | - | Y | family gate |
| Xpressbees | Feb-22 | 54m | 8.94 | - | Y | relevance gate: archetype label only |
| Delhivery | May-21 | 63m | 5.97 | - | Y | relevance gate: archetype label only |
| E2open | May-25 | 15m | 3.46 | - | Y | relevance gate: archetype label only |
| Ninjacart | Dec-21 | 56m | - | 7.10 | Y | relevance gate: archetype label only |
| ElasticRun | Feb-22 | 54m | - | 10.36 | Y | relevance gate: archetype label only |
| WayCool Foods | Jun-22 | 50m | - | 5.91 | Y | relevance gate: archetype label only |
| Epic Games | Apr-21 | 64m | - | 5.63 | Y | relevance gate: archetype label only |
| Epic Games | Apr-22 | 52m | - | 6.18 | Y | relevance gate: archetype label only |
| Vegrow | Dec-23 | 32m | - | 6.68 | Y | relevance gate: archetype label only |
| Rent the Runway | Mar-19 | 89m | - | - | N | relevance gate: archetype label only |
| Shiprocket | Aug-22 | 48m | - | 16.03 | N | passes the gates; held out of the medians |
| Packable | Sep-21 | 59m | - | 4.15 | Y | below the absolute score floor (2.6 against 5.0) |

### tash, 36 rounds

| company | date | age | net | gross | in med | why it does not price |
|---|---|---|---|---|---|---|
| The Zebra | Apr-21 | 64m | 6.67 | - | Y | PICKED; the one net name, admitted on the word "marketplace" |
| Raisin | Mar-23 | 41m | - | 6.43 | Y | PICKED; the one gross name |
| Carta | Aug-21 | 60m | 49.33 | - | Y | DIRECT on label plus Financial Services; below the adequacy floor (8.0 against 12.0) |
| Whatnot | Aug-26 | 0m | - | - | N | family gate; GMV only, 2.5x, no fork offers GMV |
| Whatnot | Oct-25 | 10m | - | - | N | family gate; partial period, no multiple |
| Whatnot | Jan-25 | 19m | - | - | Y | family gate; GMV only, 1.66x |
| Whatnot | Jul-22 | 49m | - | - | N | family gate; no multiple |
| StockX | Apr-21 | 64m | - | 9.50 | N | family gate; gross ceiling held out of the medians |
| Vinted | Apr-26 | 4m | 7.30 | - | Y | family gate |
| Vinted | Oct-24 | 22m | 8.40 | - | Y | family gate |
| Vinted | May-21 | 63m | - | - | Y | family gate |
| Vestiaire Collective | Sep-21 | 59m | - | - | N | family gate |
| GOAT Group | Jun-21 | 62m | - | - | N | family gate |
| Dream Sports | Nov-21 | 57m | - | 23.40 | Y | family gate |
| Meesho | May-24 | 27m | 4.20 | - | Y | family gate |
| Meesho | Sep-21 | 59m | 45.80 | - | Y | family gate |
| Flipkart | Jul-23 | 37m | - | 5.20 | N | family gate |
| Flipkart | Jul-21 | 61m | - | 6.40 | N | family gate |
| Trendyol | Aug-21 | 60m | - | - | N | family gate |
| Ankorstore | Jan-22 | 55m | - | - | Y | family gate |
| SHEIN | Jan-24 | 31m | 1.40 | - | N | family gate |
| SHEIN | May-23 | 39m | 2.90 | - | Y | family gate |
| SHEIN | Apr-22 | 52m | - | - | N | family gate |
| Back Market | Jan-22 | 55m | - | - | Y | family gate |
| Glovo | Dec-21 | 56m | - | - | Y | family gate |
| Wolt | Nov-21 | 57m | 23.50 | - | Y | family gate |
| Faire | Nov-25 | 9m | - | - | N | family gate |
| Faire | Nov-21 | 57m | - | - | N | family gate |
| Loft | Mar-21 | 65m | 14.70 | - | Y | family gate |
| Udemy | Dec-25 | 8m | - | 1.29 | Y | family gate |
| Ninjacart | Dec-21 | 56m | - | 7.10 | Y | family gate |
| Vegrow | Dec-23 | 32m | - | 6.68 | Y | family gate |
| ElasticRun | Feb-22 | 54m | - | 10.36 | Y | family gate |
| Loadsmart | Feb-22 | 54m | - | 5.20 | Y | family gate |
| Loadsmart | Nov-20 | 69m | - | 4.00 | Y | family gate |
| DeHaat | Oct-22 | 46m | - | 4.50 | Y | family gate |

## Appendix B. Where the 24 rows of 5 September are served today

Fixture-lanes each row reaches, with the engine's own reason. "on a word" means no whole tag in
common. Reproduce: the listing script is in this session's log; the same facts come from
`python3 tools/measure_matching_variants_6sep.py none --weak-words` for the generic-word cases.

| row | reaches | on tags | on a word only |
|---|---|---|---|
| Slash | agentcard, unifold | both | |
| BVNK | agentcard, unifold | both | |
| Moss | agentcard | yes | |
| Zuora | paymentkit | yes | bond ("to") |
| Juspay | paymentkit | yes | unifold ("payment") |
| Cashfree | dots, moov, payabli, paymentkit, trolley | yes | rainforest ("payments") |
| Spinny | finn, oda | yes | smol ("delivery") |
| Moove | finn | yes | oda ("own"); ultrasonium (fallback, label only) |
| E2open | bizmark, ekho-labs | yes | hop-aero ("logistics") |
| Berkshire Grey | manifold-robotics, sellerclaw | yes | bizmark ("automation"); ultrasonium (fallback) |
| Restaurant365 | marble | yes | clarify, osmaura, payna ("automation", "management"); bluerails (label plus Hospitality) |
| Owner | marble | yes | akkari, bluerails, care-gp, clarify, edviro, elentaria, fundraisly, levocred, lightfield, osmaura, pazi ("ai", "operations", "business", "agent") |
| AuditBoard | payna | yes | edviro ("automation", "management") |
| Legora | alloovium, priori-legal | yes | levocred ("document"), osmaura ("law", "legal"), payna (label plus industry) |
| Applied Intuition | osseus | yes | alloovium ("intelligence") |
| Vention | osseus | yes | 21st ("design") |
| Suno | | | acti, goldfish, planeat ("ai", "app", "generation") |
| Framer | chronicle, wispr-flow | yes | 21st, acti, goldfish, orchids, planeat ("ai", "builder", "design") |
| Genspark | anysearch | yes | acti, atlas-new, goldfish, orchids, projectx, wispr-flow ("ai", "agent") |
| Mercor | clera, standout, tsenta | yes | nursa, priori-legal ("marketplace", "talent") |
| Micro1 | clera, priori-legal, standout, tsenta | yes | nursa ("marketplace") |
| Sapiens | florin | yes | edviro ("management", "software"); levocred (label plus industry) |
| Accolade | evergrove, insurf, scheduling-wizard | yes | denta, open-wearables ("benefits", "health"); inato (label plus industry) |
| Udemy | befreed, wondering | yes | bloomy, honen ("learning", "course"); inato ("marketplace") |

---

# Follow-ups, 6 September, evening (Fable, 22:10 UK)

Daniil's thirteen points of the afternoon, in his order, each with what was done. Worked in a fresh
clone of origin at `5e518d2` (the regenerated weights and the rebaselined golden, both pushed).
Suite before: gate 94 of 102, golden 0, sixteen checks, only check 1 red. Suite after: gate 94,
golden 0 against the rebaselined fixtures, **seventeen checks**, only check 1 red.

**Applied (four things, each with count in and count out):**

- **StockX released into the medians** on the ruling that a "more than" figure is a ceiling, not an
  exclusion (`tools/apply_stockx_release_6sep.py`: 52 rows in, 52 out, 1 changed, 0 dropped). It
  prices the GROSS lane only, as "at most 9.5x". It reaches no fixture yet: tash is in the fintech
  family and StockX in the consumer one (see point 5).
- **Check 16, `tools/check_token_weights.py`**: recomputes the weight file from the seven tag files on
  every suite run and fails if the committed file differs, printing the one command that fixes it.
  This is why it can never sit stale for two weeks again (point 2).
- **The No-comps list has a third kind of entry** (check 8): comparables that cleared the relevance
  gate with no whole tag in common and either only words carried by 25 or more companies, or the
  end market alone. **293 names across 69 fixtures today.** Recorded, not removed (point 12).
- **BVNK's archetypes swapped** to Crypto & Digital Assets first, Card Issuing & BaaS second, on
  Daniil's word (`tools/apply_bvnk_swap_6sep.py`: 204 rows in, 204 out, 1 changed). Measured first:
  0 fixtures change peers. Golden moved for two fixtures in text only (agentcard's score digit,
  unifold's reason for BVNK) and was rebaselined for that reason.

**Measured and rejected, with the numbers** (`tools/measure_matching_variants_6sep.py <name>`):

| variant | what it does | result | why rejected |
|---|---|---|---|
| family_vocab | family gate admits a row sharing an archetype and a rare word | 13 change; tash gains Whatnot, StockX | also admits Harvey and Legora into health insurance, Gong and Semrush into a freight model, on "review", "deal", "forecasting" |
| family_vocab (whole tag or two words) | tighter version | 11 change, manifold not reached | still admits Gong and Harvey |
| tier_floor | relative floor judged within a tier | 29 change, gate 95 | Costco and FirstCash into a laundry subscription, Delivery Hero into a snack box, Anthropic into an SEO tool |
| rescue_words | below the relative floor only for names sharing a whole tag or rare word, only when the lane cannot price two | on its own moves nothing (family gate first) | kept as a tool; safe but blocked |
| family_secondary | admits a row whose primary archetype is the founder's secondary | 23 change, gate 95 | passes levelten on Whatnot, Vinted, Faire, Meesho |
| endmarket_primary | end-market route needs the founder's primary archetype | 24 change, gate 94 | inato swaps healthcare names for Ninjacart, Glovo, Wolt |
| retag_manifold (+ Berkshire Grey) | Design & Engineering first | manifold's listed core becomes Cadence, Synopsys, UiPath; bizmark fails | wrong |
| retag_tash | Third-Party Marketplace first | tash passes on Whatnot, StockX, eBay; loses Robinhood, HUB24, Netwealth | trades the listed lane for the private one |

**The conclusion, plainly.** Five different loosenings of the family gate were measured and every
one admitted wrong names somewhere. The family gate is right. For manifold-robotics (Vention,
Applied Intuition) and tash (Whatnot, StockX) the names Daniil wants are held back by the family
each row was FILED under, and no rule that reaches them without also reaching the wrong ones was
found in an evening. The remaining route is the one rule A2 already uses for OFX and EML: **a named
list, with a written reason each, that cannot spread.** An "also compare with" list per test
company (manifold: Vention, Applied Intuition; tash: Whatnot, StockX), pinned past the family gate
and the relative floor, is the banker's judgement the free-tier review exists to apply. Not built;
on the takeover list.

**Answers to the numbered points:**

1. Yes. levelten, manifold-robotics and tash are on the No-comps list, kind 2, and have been since
   check 8 started printing it; levelten is also now kind 1 (The Zebra reaches it only through the
   recorded fallback since the weights were regenerated).
2. The weight file: every company carries a list of product words. When a founder and a company
   share a word, the engine adds points for it, and the file says how much each word is worth: 5
   divided by the number of companies carrying it, so "marketplace" (75 carriers) is worth 0.07 and
   "robotics" (5 or fewer) is worth 1.0. It was stale because it is produced by a script, the script
   read five of seven files from a folder path that no longer existed, nobody re-ran it after the
   lending and logistics files arrived, and nothing checked it. Regenerated (your commit
   `5e518d2`), and check 16 now guards it.
3. levelten: we hold exchanges on the listed side (its core is Indian Energy Exchange, Clarkson, CME;
   secondary MCX, Deutsche Boerse, ICE) and three climate rows on the private side (Xpansiv, which
   prices on tonnes of CO2 only; Octopus Energy and Enpal, energy retail and solar, wrong kind of
   business). Noted on the No-comps list for the bulk pass: a peer like Xpansiv with a revenue
   figure, or Xpansiv's own revenue at the round. The quiz: the exchange fork already asks for a
   throughput volume and its unit (levelten routes there); a climate company on the marketplace
   fork is not asked. Noted in the status file for the quiz work.
4. Berkshire Grey is in. Vention and Applied Intuition are behind the family gate and the relative
   floor; see the conclusion above.
5. Robinhood is already in tash's listed core (with XP, HUB24, Netwealth). StockX is released
   (above). Whatnot has never disclosed revenue: all four rounds are GMV only, and no fork offers a
   GMV reading yet (rule B8's wiring). Both are behind the family gate.
6. edviro: agreed and recorded. It sits in kind 3 today (AuditBoard on "automation, management").
   When the taxonomy rule is built after the pilot, edviro falls to the archetype fallback and is
   served other vertical software as a recorded rescue, which is exactly the instruction.
7. ultrasonium: Mensch und Maschine, DocuSign and Roper never reached it. They appeared only in a
   variant I measured and rejected on the morning (moving its archetype to Design & Engineering):
   DocuSign came through on the word "contract" (Contract Manufacturing against Contract
   Management), which is the generic-word problem again. Today its listed lane is empty and its
   private lane is the recorded fallback. Vention ships hardware ordered through its design
   platform ("mostly hardware revenue" in the row) and is tagged Design & Engineering, which is
   why it can reach a manufacturer at all; a software row cannot. Nothing is broken in the engine
   here; the pool holds no metal manufacturer.
8. The six payments rows all carry function Finance & Payments, and the differences you name are
   in the fields the engine reads: Slash and Moss are Card Issuing & BaaS (Slash TRANSACTION_FEE,
   Moss PLATFORM); Zuora is billing software (Commerce & Payments Software, SEATS, ENTERPRISE);
   Juspay is orchestration and Cashfree a gateway (both TRANSACTION_FEE, INFRA_LAYER; Juspay
   ENTERPRISE, Cashfree SMB). BVNK swapped to Crypto & Digital Assets first, as above.
9. Accolade is the Transcarent take-private: CONTROL, $621m, LTM revenue $446.7m to Nov-24, 1.39x,
   marked as a control transaction on the field (rule B6) and never in a minority median.
10. Geography: **there is no country or region field on a private row.** Finn (Germany) and Moove
    (Africa and emerging markets, now Japan) match on Car Subscription, Owned Vehicle Fleet, EV
    Fleet, and nothing can flag the difference. Takeover item: a `country` column on both private
    files and a caveat in the honesty copy when it differs.
11. Owner: the regenerated weights already took it out of fundraisly, elentaria, pazi, clarify and
    lightfield; it stays with marble.
12. inato: DeHaat and Vegrow reach it on "marketplace" and "network" (kind 3, recorded); Accolade,
    Aledade, Cityblock and Tecsys on the end market alone (kind 3, recorded); Waystar and Phreesia
    on the word "patient". Requiring the founder's primary archetype on the end-market route was
    measured and swaps the healthcare names for Ninjacart, Glovo and Wolt, which is worse. inato has
    no comparable in the pool. Tecsys's industry tag (Healthcare & Life Sciences) is questionable
    for a supply-chain software company; re-tag candidate for the bulk pass.
13. Owner and fundraisly are no longer paired (point 11). Owner cannot be paired with Toast: one is
    a private round and the other a listed company, and the lanes never mix; the listed lane for a
    restaurant founder already leads with Toast (marble's core: Toast, PAR, Agilysys).

**Commands for Daniil** (the six new or changed files were written into your working tree over the
bridge; no git ran):

```
cd ~/fairway-valuation && rm -f .git/index.lock && git add -A && git commit -m "StockX released (threshold ruling), BVNK swapped, check 16 guards the token weights, No-comps list kind 3, follow-ups answered

Fable, 6-Sep evening. StockX gross ceiling in_medians 0 to 1 (52 rows in, 52 out). BVNK to
Crypto & Digital Assets primary (204 in, 204 out; golden text-only move on agentcard and unifold,
rebaselined). tools/check_token_weights.py is check 16. peer_universe_check prints kind 3:
293 comparables across 69 fixtures admitted on generic words or the end market alone. Eight
matcher variants measured for manifold and tash and rejected with the names each let through.
Gate 94 of 102, golden 0 moved, only check 1 red.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01DZUddHXsVGtwUWxWNxGgLu" && git push
```

---

# Follow-ups, 6 September, late evening (Fable, 23:40 UK)

**First, the push.** Origin is still at `5e518d2`. The terminal shows `git add -A` then `git push`,
and "Everything up-to-date": the `git commit` step between them was skipped, so the files are
staged on the Mac and nothing left it. The one command at the foot of the status document does all
three steps. Everything from this evening, including what follows, is in that same batch.

**The ceiling ruling applied throughout.** Of 320 private rounds, 84 are held out of the medians.
Twelve carry a printed multiple with a ceiling or floor mark. Ten were held for the bound and
nothing else and are released by `tools/apply_ceiling_ruling_6sep.py` (268 rows in, 268 out, 10
changed): Anthropic Sep-25 (at most 36.6x) and May-26 (at most 20.5x), Databricks (at most 28.7x),
Docker (at most 42.0x), Miro (at most 58.3x), Notion (at most 18.3x), PayFit (at most 45.5x),
Vercel (at most 32.5x), Decagon (at most 150x), Factorial (at least 33.3x). Two stay held for a
reason the ruling does not touch, named in the script: Perplexity Jan-24 (the valuation is
press-reported, not company-disclosed) and Marqeta May-20 (the revenue basis is unstated). One
flag: Factorial's field says GROSS and its own note says "corrected to NET"; released on the field,
contradiction to the B3 audit. **27 fixtures' private ranges gain these names** (the AI and
developer-tool founders, mostly), golden rebaselined on that reason. The other 72 held rows carry no
multiple at all, or are duplicates, estimates, secondary-only rounds, originations multiples, or
rows with an entity or period problem; none is a threshold case.

**BVNK.** "Infrastructure" was my loose word; the label it carries has nothing to do with ports.
On "payments / market / DeFi infrastructure" it now reads Crypto & Digital Assets first and
Cross-Border & FX second (settlement rails), instead of Card Issuing second. Measured: BVNK enters
trolley's and dots' private lanes (both payouts businesses) in place of dLocal and Rapyd. Three
fixtures rebaselined (trolley, dots, agentcard's score digit).

**"293 names" explained.** Not 293 companies without comparables. There are 1,117 comparable slots
across the 102 test companies (one name sitting in one founder's lane). 294 of those slots got in
on weak evidence: 217 on a word carried by 25 or more companies ("marketplace", "automation",
"payments"), 77 on the end market alone with no product word in common (any healthcare company for
inato). They are spread over 69 test companies and 116 of the 204 lanes. **Only 3 lanes rest on
nothing else** (moov's listed lane, all payments companies sharing "payments", which is fine; smol's
and hop-aero's private lanes, which are not). Check 8 now prints exactly this split. It is a map of
where the evidence is thin, for the bulk pass and for the banker reading the free tier, not a
count of failures. The names are kept because every tighter gate measured today cost real peers.

**Tags for the four names: the honest answer, and what was built instead.** Product tags cannot do
it. The family gate runs before any word is scored and reads only the archetype family and the end
market, so no tag on Vention or Whatnot reaches it; and the five rule-level ways of opening that
gate measured this afternoon each let wrong names through elsewhere. What works without touching
the rest of the dataset is the thing rule A2 already does for OFX and EML, in reverse: **a named
list on the founder's side, with a written reason each.** Built as `also_compare` on the profile
(`selector/golden_profiles.py`): a named row passes the family gate and the relative floor for
that founder only, sits at least ADJACENT, is marked `pinned` with the reason, and is printed by
check 8 under PINNED BY NAME on every run. First entries, your words: manifold-robotics: Vention,
Applied Intuition; tash: Whatnot, StockX. **Measured: exactly two fixtures change. Gate 94 to 96.**
manifold-robotics prices Berkshire Grey 5.69x and Applied Intuition at most 37.5x on the net
reading, Vention at least 10.0x on the gross reading; tash prices Raisin 6.43x and StockX at most
9.5x on the gross reading, Whatnot shown and unpriced (GMV only, until a GMV reading exists).

**One flake fixed on the way.** ZoomInfo's score for floqer read 5.8 in one run and 5.9 in the next:
the word points were summed over an unordered set, whose order differs per Python process, and the
float landed either side of a rounding boundary. Now summed in sorted order
(`selector/match_reference.py`, `tag_overlap`); golden verified stable across three hash seeds.

**Suite after all of it:** gate 96 of 102, golden 0 moved against the rebaselined fixtures,
seventeen checks, only check 1 red. Files changed: `selector/match_reference.py`,
`selector/golden_profiles.py`, 33 fixtures under `selector/golden/`, `data/private-rounds.csv`,
`data/private-rounds-consumer.csv`, `data/private-companies-tags.csv`, `tools/check_all.sh`,
`tools/peer_universe_check.py`, `tools/check_token_weights.py`, `tools/apply_ceiling_ruling_6sep.py`,
`tools/apply_stockx_release_6sep.py`, `tools/apply_bvnk_swap_6sep.py`,
`tools/measure_matching_variants_6sep.py`, this document and the status document.

## Appendix C. The prompt this work ran on (Daniil, 5 Sep, 23:10 UK; moved here from the status document on 6 Sep when the to-do was closed)

> Fairway, matching refinement. Read `claude/Fairway_STATUS_2026-09.md` first, then `docs/RULES.md`
> and `docs/taxonomy-review-5sep.md`. The pool is not to be enlarged; the job is to make the engine
> find the comparables it already holds, and to stop it serving wrong ones. Work from a fresh clone
> in the cloud, never git on the laptop. Do these in order and report each with counts: (1) The two
> fixtures that still fail on the private lane (levelten, manifold-robotics) and tash, which holds
> one net round and one gross round so neither lane is a range. For each, list every held round in
> its archetype and say exactly why it does not price: no revenue, barred by the relevance gate, or
> outside the 24-month window. The gross-basis cases are DONE, not deferred: Opus built the
> net-and-gross split on 5 Sep and it flipped clera, nursa, paymentkit, standout and tsenta, so do
> not re-diagnose them. Propose the smallest change for the rest that would let a real comparable
> through without letting a wrong one through, and say which fixtures it moves. (2) Measure the
> taxonomy proposal before Daniil rules on it: apply "for Vertical Software, Data AI & Developer
> Tools, Business Applications and Cloud & Infrastructure, an archetype match counts only if the
> industry matches too" on a scratch copy, and report which of the 102 fixtures change peers, which
> gain, which lose. (3) The tags. Check the two hardware fixtures tagged Owned-Inventory Retail (see
> rulebook A11, which now records why), the 24 tag rows Claude wrote on 5 Sep (the handover names its
> own doubtful calls: Moove, Vention, Owner, Sapiens, Accolade, Udemy), and any row where the
> fallback served a nonsense comparable. Propose re-tags as a list with the reason beside each; do
> not apply them. (4) Run the full suite (`FAIRWAY_NO_GIT=1 sh tools/check_all.sh`, fifteen checks
> now) before and after every change; golden must not move without the reason written down. Rules
> that bind you: never drop a row silently, count in and count out on every change, no figure from
> your own head, no em dashes, plain words. Hand back a short document with the proposals and the
> commands for Daniil (`git add -A`).
