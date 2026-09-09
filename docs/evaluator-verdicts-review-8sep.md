# The evaluator's 142 verdicts, checked one by one: what is fair, what to push back on, and the plan

Written 8 September 2026, 20:45 UK (Fable). Checked against a fresh clone of origin at `41d64fa`
(your push of 20:34 UK). The engine was run on every flagged fixture to see which words, tags and
rules produced each set, and every "better name in the pool" the evaluator names was looked up and
walked through the engine's fences to see what stops it. **Nothing in the engine, the data or the
fixtures was changed.** Every re-tag below was measured on a scratch copy in memory and is a proposal.

**One term.** "The wider ring" is the engine's secondary listed lane: names related to the founder
that did not make the pricing set. The evaluator's table (`docs/fixture-comparables-8sep.md`) shows
only the pricing set and the private lane, so the wider ring was invisible to them. That matters
below, because several names the evaluator calls "unused" are in fact shown there.

---

## 1. The short version

The evaluator marked 100 sets OK, 20 OK (weak), 13 FLAG, 4 CONFIRM OUT OF MARKET and 5 ALREADY
STRUCK. That is 142, reconciled.

**My reading of the 13 flags:** 6 are fair as written (kita, ekho-labs, manifold-robotics, bizmark,
lambda-robotics, subvysion); 3 are fair on the verdict but wrong about the cause, or right with a
fix that costs a gate pass (fundraisly, alloovium, supercritical); 2 are partly fair (publora,
princeps); 2 should be pushed back on (emergent, derya). **Of the 4 out-of-market confirmations:** 3 are
fair (one needs a strike, two are already on the No-comps list) and 1 reverses your own ruling of
6 September, so it is yours to decide. **The 5 strikes:** agree. **The 20 weak-but-OK notes:** all
reasonable as notes; three of the "better names" they suggest do not fit and I would not act on them.

**What the flags are actually caused by, counted.** Six of the thirteen come from how the TEST
COMPANY was tagged by whichever session wrote its profile, not from the engine: a wrong end market,
a wrong secondary archetype, or the archetypes in the wrong order. A re-tag fixes each one, and I
measured every re-tag. Four come from one archetype, Commerce Enablement & Fulfilment, which holds
26 carriers, forwarders, 3PLs and warehouse landlords and only 2 software rows, so it sits in the
consumer family and every supply-chain SOFTWARE company tagged with it is walled off from Kinaxis,
Manhattan and Tecsys by the family gate. One comes from the label-only fallback: it prices a lane
without telling the founder the names share nothing but a label (subvysion). One is a pool gap that
already fails the gate cleanly (princeps). The last (publora) is an imperfect set the engine
judged by business model rather than by market, which is a tagging choice.

**Two genuine engine findings the evaluator did not name but the check surfaced.** The "strong /
partial / thin" closeness label counts shared words, so a lane is called strong on the words "a",
"as", "ai" and "data"; 69 of the 116 lanes labelled strong rest on under one point of real product
evidence. And the pricing set can be filled with a BROAD lane that cannot price while a
better-matching name sits in the wider ring (lyka: BARK scores 20.8, the highest of anything, and is
not in the set).

**Two things about the evaluator's own method.** They applied a stricter bar than yours. Your rule
of 8 September is that only absolutely inadequate sets are struck (manufacturer against software,
language app against AI lab), not merely imperfect ones. Four of the thirteen flags (publora,
emergent, supercritical, derya) are imperfect sets inside the right business family, not nonsense.
And they read only the pricing set, so "the pool has X and it was not chosen" is sometimes wrong:
Sprout Social and Sprinklr are in publora's wider ring, Procore and Trimble in alloovium's, Indian
Energy Exchange in supercritical's, BARK in lyka's.

---

## 2. The thirteen flags, one by one

| # | fixture | what the evaluator says | what the engine actually did, and why | my verdict | what it needs |
|---|---|---|---|---|---|
| 1 | fundraisly | Rating agencies and data vendors for an outreach agency; "matched on the word investor" | Not the word. The fixture profile carries **secondary archetype Financial Data & Index** and **end market Financial Services**. S&P, Moody's, MSCI, FactSet, Morningstar, CRISIL and Plaid all arrive on "related type of business" plus "same end market". The only product word shared with anything is "crm" (HubSpot). | **Fair verdict, wrong cause.** | Re-tag the fixture: drop the secondary, end market Horizontal. Measured: listed becomes HubSpot, Freshworks, Salesforce (3 priced); private becomes Clay, Semrush, Gong, Apollo.io, Jasper, Contentsquare, 6sense (5 priced). **Gate: FAIL to PASS.** Whether sales tooling is the right neighbourhood for an outreach AGENCY is a second question; it is the neighbourhood the evaluator asked for. |
| 6 | publora | Social publishing API shown TomTom, PagerDuty, ZoomInfo; Sprout, Sprinklr, Buffer unused; engine calls it strong | Publora is tagged developer tool first, marketing second, buyer DEV. The pricing set is a developer-tool business-model set (Qt and GitLab fit; PagerDuty, ZoomInfo, TomTom are word matches on "api", "platform", "scheduling", "engagement"). **Sprout Social and Sprinklr ARE shown, in the wider ring** (Sprout has the highest product overlap of any listed name, 0.8, and fails only the who-it-sells-to test, because it sells to marketers and publora to developers). Buffer is the best private product match in the whole pool (1.6 points) and is cut by the seven-name cap because its only round is October 2014, twelve years old. "Strong" is the closeness label counting four shared words (see finding D). | **Partly fair.** The set is weak, not absurd: software against software, same business model. Not a strike under your bar. | Nothing on the engine for this fixture. If you would rather price a publishing API against the publishing companies, that is a tagging choice (marketing first, developer second) and it is yours; the company describes itself as an API. Fix the "strong" label (D). |
| 23 | supercritical | Carbon-removal marketplace shown Sea, MercadoLibre, Faire, Meesho; Xpansiv, IEX, CME used for levelten but not here | The fixture is tagged Third-Party Marketplace with **no secondary**, so it sits in the consumer family and no exchange can reach the pricing set. IEX is in the wider ring; CME is stopped by the family gate; Xpansiv passes the gate (energy end market) but carries no revenue multiple, only tonnes. | **Fair verdict; the fix has a cost.** | Measured both ways. Adding Market Infrastructure & Exchange as SECONDARY: IEX enters the listed set (with Sea, MercadoLibre), Xpansiv enters the private lane unpriced; gate unchanged. Making it PRIMARY, as the evaluator asks: listed becomes IEX, PSI Software, Tradeweb (3 priced); private becomes Xpansiv and The Zebra, 1 priced, **gate PASS to FAIL**, a levelten twin. Your call: a wrong-market set that prices, or an honest failure. I lean to the secondary version plus the No-comps list. |
| 44 | alloovium | Construction document AI shown sales-data and legal names; Procore, Trimble, Bentley unused | The fixture's end market is **Real Estate**; Procore, Trimble, Bentley and Nemetschek carry **Construction & Infrastructure**. The labels differ, so the construction names fail the who-it-sells-to test and sit in the wider ring (Procore has the highest product overlap, 1.0). AppFolio (property management) came in on Real Estate. The rest arrived on "intelligence", "records", "review", "document" plus the secondary archetype Data, AI & Developer Tools. | **Fair verdict, wrong cause** (not the words alone; the end-market label, and the near-duplicate industry labels already on TAKEOVER item 7). | Re-tag the fixture: end market Construction & Infrastructure, drop the Data & AI secondary. Measured: listed becomes Procore 12.5, Trimble 10.1, Bentley 9.0, **DIRECT**, 3 priced. Private stays legal and hospitality software (Legora, Harvey, Clio, AuditBoard, Restaurant365, Doctolib): the Vertical Software catch-all, which is the taxonomy rule's case, ruled yes, build after the pilot. |
| 53 | emergent | AI app builder shown Cadence, Synopsys, Zeta; give it Figma, Wix, GitLab, Atlassian like orchids | The private lane is excellent (Lovable 9.3 product points, Replit 5.2, Cursor). The listed pool holds no AI app builder. Wix scores 3.6 (below the floor); Figma, GitLab and Atlassian share no product word with emergent and are reachable only through the label fallback, which does not fire because the lane prices. Orchids got Adobe and Figma because it is tagged prosumer and seat-priced; emergent is tagged developer and usage-priced. The two companies describe themselves differently. Swapping emergent's archetypes was measured: Similarweb, Cadence, Synopsys. No better. | **Push back.** Chip-design software for an app builder is weak, not nonsense; the founder is carried by the private lane; "the same kind of product must get the same set" is not a rule the engine has, and two companies with different buyers and pricing should not be forced to. | Nothing on the engine. If you want GitLab and Atlassian shown, it is a named pin (`also_compare`), your judgement, not a rule. Pool gap for the bulk pass: a listed no-code or app-builder name. |
| 69 | kita | Software for lenders priced as a lender; banks in the set; use the levocred set | Exactly right. Kita is tagged **Lending & Credit first**, so the lender fence (your rule of 28 August: lenders and non-lenders never price each other) walls off Q2, Jack Henry, Alkami, Mitek and Mambu, and lets in Merchants Bancorp, Close Brothers, NewtekOne and BFF Bank. | **Fair, and the fix is right.** | Re-tag the fixture: Vertical Software first, Lending & Credit second. Measured: listed becomes Fair Isaac (FICO), Blend Labs, Qualco, Q2, FIS, Jack Henry, EVERTEC, DIRECT, 7 priced. Private becomes Sapiens, Mambu, Carta, Accolade, AuditBoard, Cityblock. Cost: Upstart and Pagaya leave, because the same fence now keeps lenders out. Gate unchanged (PASS). |
| 79 | ekho-labs | Seven carriers for an AI freight model; split the archetype | Correct. Commerce Enablement & Fulfilment is filed in the consumer family (it is learned from its 28 listed rows, 26 of which are carriers, forwarders, 3PLs and REITs). So Samsara, Tecsys, Kinaxis and Manhattan are stopped at the family gate before any word is scored. E2open (private, a software company) is in the same archetype and so reaches it. | **Fair.** | Root cause B. Two routes, both measured, in section 5. The honest note: the pool holds only Kinaxis, Manhattan and Tecsys as supply-chain software, and Descartes is not in it, so even the right family gives a thin lane. |
| 80 | manifold-robotics | 3PLs and warehouse landlords for a robot maker; mark the listed lane out of market | Correct. GXO is DIRECT on the tag "Warehouse Robotics" (it deploys them; a customer, not a peer). Americold, Lineage and Tritax Big Box are REITs. Symbotic and AutoStore, the listed warehouse-automation makers, are not in the pool. The private lane is right and is your pin of 6 September. | **Fair.** | Mark the listed lane thin or out of market until the bulk pass adds a listed automation maker (rule A12 part 3: not before 18 September). Root cause B also helps: with the split, the REITs cannot reach a robotics company at all. |
| 81 | bizmark | Same fault as ekho-labs | Same. And a detail worth knowing: Kinaxis scores 3.9 product points against bizmark, DIRECT-level evidence, and is stopped by the family gate. | **Fair.** | Root cause B. |
| 106 | lambda-robotics | UiPath on "robot"; Supabase, Cato, Databricks on "AI infrastructure" | UiPath arrives on the word "robotic" (from Robotic Process Automation) plus function, revenue model and GTM. Supabase, Cato and Databricks arrive on the fixture's **secondary archetype Cloud & Infrastructure**, which the session that tagged it chose because the customers are data centres. Rule A11 files a company under what it sells, not under its customers' business. | **Fair, and the cause is a fixture tag.** | Re-tag: drop the Cloud & Infrastructure secondary. Measured: private becomes Vention and Applied Intuition, 1 priced, **gate PASS to FAIL**, which is the true answer. Listed lane stays Bentley, Samsara, UiPath: no listed hardware maker in the pool, same gap as manifold. On the No-comps list as kind 2 after the re-tag. |
| 113 | subvysion | Listed lane right; private lane is restaurants, hotels, legal, travel | Correct, and **already recorded**: check 8 prints subvysion's private lane as kind 1 (served on a label) since march 1. Every private name arrived through the archetype fallback; within the fallback, the ranking is by coincidences of function, buyer and GTM, which is how Mews, Clio and Guesty (13.5 each) outrank Vention (6.0, in the same fallback). | **Fair, and it points at the real gap** (root cause C): the fallback prices the lane at the ADJACENT band and the founder is told "priced off businesses in your category rather than your exact niche". Nothing says "these share only a label with you". | The strike mechanism is per fixture, not per lane, so the evaluator's "keep listed, drop private" cannot be done as written. What can: a caveat and a pricing rule for fallback lanes, your ruling (section 5, item 3). |
| 114 | derya | Trucking and forwarding operators for an AI brokerage; same fix as ekho-labs | Half right. Derya's own page (march document): "AI-run supply chain service for hardware companies: procurement, shipping and customs, executed for the customer; more than $15M of freight handled." Its profile is tagged SERVICES_LED. It is a freight and customs broker, so Expeditors and C.H. Robinson (asset-light forwarders and brokers) are a fair neighbourhood. The trucking fleets (JSL, Reysas, Traxion) and Mitsubishi Logistics are not. Xometry, the evaluator's suggestion, is a parts marketplace and scores 4.0, below the floor. | **Push back on the framing; the set is still too asset-heavy.** | The split in root cause B sorts this too: forwarders and brokers in one archetype, fleets and warehouses in another. No fixture re-tag. |
| 117 | princeps | No insurer in the listed lane; re-map to ZhongAn and Alignment Healthcare | Princeps **already fails the gate** and is kind 2 on the No-comps list; its listed lane is BROAD, prices nothing and is shown as context. It reached wealth platforms and core banking on the end market Financial Services alone. The pool's insurers carry the end markets Insurance, Healthcare or Horizontal (the near-duplicate labels again). ZhongAn scores 4.1 (below the floor); Alignment is a Medicare plan. | **Partly fair.** The names are wrong, but the fix offered is a Chinese consumer insurer and a US Medicare plan for a data-centre insurer, which is not better than a clean failure. | Pool gap for the bulk pass: a listed commercial P&C carrier. Fold the Insurance / Financial Services labels (TAKEOVER 7) so at least Trupanion and Crawford become reachable to insurance fixtures. |

## 3. The four out-of-market confirmations and the five strikes

| # | fixture | today | my verdict | what it needs |
|---|---|---|---|---|
| 100 | hop-aero | Carries OUT_OF_MARKET, is NOT struck, and **passes the gate** on FedEx, UPS, PostNL (7 priced) and Flink, Glovo, Gopuff (5 priced). | **Fair.** Rocket cargo on parcel carriers and grocery apps is the same class as daivin and orca-aerospace, which you struck on 8 September. | Strike it (one line on the profile). Gate 130 to 129. |
| 101 | ultrasonium | Passes on PTC, Dassault, Lectra with Xometry in the wider ring, private lane on the fallback (1 priced). | **Yours to decide, and I would not strike it on the evaluator's word.** This is your own ruling of 6 September (end market set to Manufacturing so that it reaches PTC, Dassault, Lectra and Xometry). The evaluator calls that "industrial software for a metal manufacturer". Both readings are defensible; the ruling was made knowingly and is recorded on the No-comps list as kind 3 (end market alone). | Only if you now agree with the evaluator: strike it. Otherwise nothing. |
| 102 | apollo-atomics | Fails the gate; kind 2 on the No-comps list. | **Fair, already done.** | Nothing. |
| 119 | ornadyne | Fails the gate; kind 2. | **Fair, already done.** | Nothing. |
| 103, 109, 128, 130, 133 | orca-aerospace, vorelios, constellation-space, daivin, zymbly | Struck 8 September. | Agree. | Nothing. |

## 4. The twenty OK (weak) notes, grouped by what causes them

None of these is a strike under your bar, and the evaluator did not ask for one. They are useful
because they cluster.

**The Vertical Software catch-all (5 of the 20: osmaura, edviro, foreman, pazi, chromie; payna and
fed10, marked OK, have the same shape).** Owner, Guesty, Restaurant365, TravelPerk and AuditBoard reach
legal, energy, construction and government founders because Vertical Software with a Horizontal end
market matches any Vertical Software row. This is the taxonomy rule's case, **ruled yes on 6
September, build after the pilot.** Chromie's Via and IVU (transit software) arrive on the end
market Government alone; recorded as kind 3. Nothing new to decide.

**The Design & Engineering catch-all (3 of the 20: orchids, 21st, chronicle; also emergent above).** One
archetype holds CAD, EDA and PLM vendors (Autodesk, Bentley, Cadence, Synopsys, PTC, Dassault,
Nemetschek, Lectra) beside design collaboration tools (Adobe, Figma, Canva) and robotics platforms
(Vention, Applied Intuition). A presentation tool gets five CAD vendors. Same shape as root cause B,
smaller (16 listed rows). Proposal in section 5, item 5; not urgent.

**The Commerce Enablement and Owned-Inventory catch-alls (2 of the 20: sellerclaw, oda; finn,
marked OK, has the same shape).** Vegrow, WayCool, Berkshire Grey for a merchant operator; Moove, Spinny, Quince for
a grocer, on the word "own". Root cause B and the regenerated weights; recorded.

**Words that are not words (2 of the 20: bond, upstream).** BlackLine, Sidetrade and Zuora reach bond on
0.1 product points: the word "to" (Record to Report, Quote To Cash, Agentic To-Do List). The
stopword list is four words (and, of, the, for). The 6 September write-up measured a longer list
(to, a, an, as, in, on, at, by, with, from, per, vs, via, or) as harmless on the 102 and left it for
you. It was never applied. Section 5, item 4.

**The label fallback (1 of the 20: blindspot).** The whole listed lane is the fallback and has been kind 1
on the No-comps list since 5 September. The evaluator's Zeta and LiveRamp are also fallback-only.
Nothing in the pool does out-of-home media. Root cause C, pool gap.

**End-market-alone matches and the near-duplicate labels (3 of the 20: florin, denta, open-wearables).**
Florin gets PayPoint and SS&C on the end market Financial Services with no product word; Trupanion
(a full-stack pet insurer, the better peer) carries "Insurance" and cannot bridge. **Denta is the
interesting one:** ZhongAn shares 3.1 product points with it ("Health Insurance"), which is
DIRECT-level evidence, and is excluded by the 12.0 adequacy floor because its other attributes do
not coincide, while SMS Co and Medley (healthcare job boards) get in on end market plus function.
That is the "a sum is not evidence" failure in the other direction and is finding E below.
Open-wearables' private lane is care providers on the end market alone (kind 3). **Push back on the
evaluator's WHOOP and Oura:** they are consumer hardware brands and open-wearables is developer
infrastructure; the engine is right to keep them out (both score under the floor).

**The last four of the 20, and three suggested names to push back on.** Tsenta: SEEK, Visional and Upwork sell to employers;
tsenta is a consumer subscription app; all three score under the floor for it, and its private lane
(Mercor, Micro1) is DIRECT. Wispr-flow: SoundHound is in the wider ring (0.9 product points), and
fails only on buyer (business against prosumer); fine as a note. Airtop and world-labs: the listed
lanes are weak word matches (GB Group on "intelligence") because the pool has no listed
browser-automation or video-model company; the private lanes carry them.

---

## 5. What is actually wrong, and the plan for each

Seven causes. For each: what it is, which verdicts it explains, what can be done, what I measured,
and whether it is yours to decide. **Nothing here is built.** Order is by how much it fixes for how
little.

### 1. Six test companies are mis-tagged, and the live profiler will make the same mistakes

**Explains:** fundraisly, alloovium, kita, lambda-robotics, supercritical (partly), emergent (partly).
Six of the thirteen flags.

**The problem.** The fixture profiles were written by sessions reading the company's page, and each
of these carries one wrong field: an end market that is the customer's world rather than the
company's (fundraisly: Financial Services; alloovium: Real Estate for a construction company), a
secondary archetype that describes the customer (lambda-robotics: Cloud & Infrastructure), or the
archetypes in the wrong order (kita: a lender first, software second). The live profiler
(`selector/profiler.py`) is one model call given a menu of allowed values and no definition of what
archetype and end market MEAN, so a real founder who "sells to lenders" or "serves data centres"
will be tagged the same way.

**What to do.**

- Re-tag the six fixtures in `selector/golden_profiles.py` (one line each), rebaseline golden for
  those six with the reason written, run the suite. Measured effects, all in section 2: fundraisly
  FAIL to PASS; kita gets FICO, Blend, Q2, Jack Henry; alloovium gets Procore, Trimble, Bentley;
  lambda-robotics PASS to FAIL (honest); supercritical your choice of secondary or primary.
- Add four rules to the profiler prompt, in words the model can follow: the archetype is what the
  company IS and how it earns, never who it sells to; "for lenders" is Vertical Software with the
  end market Financial Services, not Lending & Credit; the end market is the customer's industry as
  spelled in the menu (construction is Construction & Infrastructure, not Real Estate); a hardware
  company keeps a hardware archetype even when its customers are data centres or grids. Add the
  four cases (kita, fundraisly, alloovium, lambda) to check 17 as profiler tests.
- Fold the near-duplicate end-market labels before march 2 (TAKEOVER 7: Real Estate & Construction
  beside Real Estate and Construction & Infrastructure; Insurance beside Financial Services;
  Retail & Commerce beside Retail & E-commerce; Transportation & Logistics beside Logistics &
  Mobility). It is a data tidy, about a dozen rows, count in and count out on each file.

**Yours to decide:** the six re-tags (each is a judgement about the company), and supercritical's
version. **Effort:** an hour, plus the suite.

### 2. Commerce Enablement & Fulfilment is a logistics-operators archetype wearing a software name

**Explains:** ekho-labs, bizmark, manifold-robotics (listed), derya, and the sellerclaw and
hop-aero strays. Four of the thirteen flags.

**The problem.** The archetype holds 28 listed rows: 20 carriers, forwarders, 3PLs and freight
fleets, 3 cold-chain operators, 3 warehouse REITs (Americold, Lineage, Tritax Big Box), and only
Baozun and BASE as software. The family map is learned from those rows by majority, so the archetype
is filed as consumer (asset-heavy), and any software company tagged with it is walled off from the
software family before a word is scored. E2open (software) and Berkshire Grey (robots) are in it on
the private side. The 6 September review already named it a catch-all to add to the taxonomy rule,
but the taxonomy rule cannot fix this one: it requires the end market to match, and both sides are
Horizontal.

**Two routes, both measured.**

- **Route A, the split the evaluator proposes.** A new archetype for supply-chain and logistics
  SOFTWARE and marketplaces (Kinaxis, Manhattan, Tecsys, E2open, Shiprocket, Freightos, Full Truck
  Alliance; Descartes when sourced), in the software family; the operators, fleets, forwarders and
  REITs stay where they are, renamed so nobody mistakes them for software. About 30 listed re-tags
  and 5 private, then golden for every logistics fixture moves (byrd, hived, 99minutos, sellerclaw,
  ekho-labs, bizmark, derya, manifold, hop-aero). Proper fix; a morning's work; after march 2 so it
  can be measured on 180 fixtures rather than 142.
- **Route B, the cheap version for the pilot.** Re-tag bizmark and ekho-labs to a software archetype
  first with Commerce Enablement second, and E2open the same way. Measured: bizmark's listed lane
  becomes ATOSS, BlackLine, **Kinaxis**, Sidetrade, SAP, UiPath, Workday, and its private lane E2open,
  Ramp, Glean, AuditBoard, FloQast, Restaurant365, Factorial. Carriers gone; the Business Applications
  catch-all in their place. Better family, worse specificity. Ekho-labs measured under two software
  archetypes and neither found a freight-software neighbourhood, because the pool has three such
  names. Route B buys little for ekho-labs and something for bizmark.

**Recommendation:** Route A after march 2, and for the pilot mark the listed lane of manifold-robotics
and ekho-labs thin (a caveat, not a change of names). **Yours to decide:** A or B, and when.

### 3. The label-only fallback prices the founder's range and does not say so

**Explains:** subvysion (private), blindspot (listed), and the label-only lanes of daivin, vorelios,
quippy, nodus-compute and markov that check 8 already prints (10 lanes, 52 comparables).

**The problem.** Rule A12 makes the fallback a recorded rescue: it fires only when a lane cannot
otherwise price two names, and every name it admits is printed by check 8. That half works. The
other half does not reach the founder: the admitted rows are not marked, the lane gets the ADJACENT
band (a pricing band), and the only caveat is "priced off businesses in your category rather than
your exact niche". For subvysion that sentence sits over a range built from Owner, Mews, Guesty and
Clio. Within the fallback the ranking is by coincidences of function, buyer and GTM, which is why
restaurant software at 13.5 outranks Vention at 6.0 in the same lane.

**What to do.** Mark each fallback row on the way out (one field), carry it into the range object,
and write one honesty caveat at IDENTITY severity: "These companies share a business-type label with
you and nothing else we can check. Shown for context." Then a ruling from you: **does a label-only
lane price at all?** Three options: price with that caveat (today's behaviour plus the sentence);
show the names and no range (the CONTEXT treatment the listed lane already has); or price only when
the founder pins a name (the `also_compare` route). My recommendation is the second: names, no
range, and the No-comps list entry it already has.

**Yours to decide:** the ruling. **Effort:** two hours once ruled; golden moves for the 10 lanes,
reason written.

### 4. The closeness label and the stopwords

**Explains:** every "the engine calls it strong" remark (publora, alloovium, ekho-labs, derya), plus
bond and upstream.

**The problem.** `_closeness` calls a lane strong when its names share four or more words with the
founder, whatever the words weigh. Lambda-robotics' private lane is strong on "a", "as", "ai", "data",
"robotics", "service". Across the 142: **116 lanes are labelled strong, and 69 of them rest on under
one point of product evidence** (a whole shared tag is worth up to 3). The founder reads "Close, on
six shared descriptors" over a lane that shares one real word. Separately, the stopword list is four
words, so "to", "a" and "as" score and count; the longer list was measured harmless on 6 September
and never applied.

**What to do.** Closeness from weighted points and non-generic words (the weight file already says
which words are generic), and the fourteen-word stopword list. Selection barely moves (on 6 September the
longer stopword list changed nothing beyond what the weight regeneration had already changed, on
the 102); the labels and caveats move for many lanes, so golden rebaselines with the reason. **Yours to approve; no ruling needed.** Effort: an hour.

### 5. Two engine rules worth measuring, found on the way

**E1. A BROAD pricing set beats a better name in the wider ring.** Lyka's core is Oisix, HelloFresh,
Naked Wines, Ocado: same end market, different kind of business, BROAD tier, which is not a pricing
tier, so the listed lane prices nothing and lyka fails the gate. BARK (pet subscription, same
archetype, the highest score of anything at 20.8) is in the wider ring because its end market label
differs. The rule that puts end market above archetype in the core split is right for most founders
and wrong here. Proposal to measure: when the core would otherwise be BROAD, admit the best
ADJACENT or DIRECT names from the wider ring first. Measure on all 142 before proposing it.

**E2. The DIRECT adequacy floor excludes the one name with real product overlap.** Denta: ZhongAn
shares "Health Insurance" (3.1 points, DIRECT-level) and is out at 7.2 against a 12.0 floor; two
healthcare job boards are in on end market plus function. The floor was calibrated on 24 August to
stop coincidence sums; here it stops evidence. Proposal to measure: a name anchored on 3.0 or more
product points clears the adequacy floor at the ADJACENT level (5.0) rather than 12.0. Measure on
all 142; the 6 September rule stands that any variant admitting a wrong name elsewhere is rejected.

**Yours to approve the measurement only.** No change proposed until measured.

### 6. The Design & Engineering split (later)

Sixteen listed rows mixing CAD, EDA and PLM vendors with design collaboration tools and robotics
platforms. Explains orchids, 21st, chronicle and half of emergent. Same shape as cause 2, smaller
effect, and none of the four sets is nonsense. After the pilot, with the taxonomy rule.

### 7. Pool gaps, for the bulk pass after the 18 September march (rule A12 part 3, nothing chased before)

Each named by the evaluator or by this check, each verified absent from the pool today:

- A listed warehouse-automation maker (Symbotic, AutoStore): manifold-robotics, lambda-robotics.
- Supply-chain software: Descartes; Manhattan and Kinaxis are held (Tecsys is tagged healthcare and
  should carry Logistics & Mobility, TAKEOVER 7).
- A listed commercial P&C carrier: princeps, florin.
- A carbon or environmental marketplace with a revenue figure, or Xpansiv's own revenue at its round:
  supercritical, levelten (already on the list).
- Out-of-home or media buying: blindspot.
- A listed no-code or app-builder name: emergent, orchids.
- A listed data-labelling or training-data vendor: markov, praxis, qokedas (your reading on 8 Sep
  was that none exists; recorded only).
- Aerospace and defence end market in the vocabulary: TAKEOVER 11, now with hop-aero as a fourth name.

---

## 6. Things in this review that touch one of your instructions

1. **Ultrasonium.** The evaluator asks for a strike; you ruled on 6 September that its end market is
   Manufacturing so it passes on PTC, Dassault, Lectra and Xometry. I have not treated the evaluator's
   verdict as overriding yours. Say if it should.
2. **Your bar of 8 September** (only absolutely inadequate sets are struck). Four flags (publora,
   emergent, supercritical, derya) do not meet it; I have marked them partly fair or push back on
   that basis rather than on taste.
3. **Rule A12 part 3** (no data pulls before the bulk pass). Two evaluator fixes ("until the pool has
   a hardware maker", "re-map to ZhongAn") are pool work; they are listed under cause 7 for the bulk
   pass and not proposed now.
4. **Your rule of 28 August** (lenders and non-lenders never price each other). The kita re-tag
   applies it in the other direction and loses Upstart and Pagaya. Named so it is not a surprise.
5. **The taxonomy rule** (ruled yes, build after the pilot). Nothing above pulls it forward. Cause 2
   is a different rule (family, not end market) and is why the taxonomy rule alone would not fix
   the freight fixtures.
6. **No engine change without your approval.** None made. The two scratch tools used here
   (`diag.py`, `whatif.py`) live in the cloud clone and are not in the repo.

## 7. What I did not do

I did not re-read the 100 plain OK rows one by one beyond the ones whose reasons named a stray;
their sets were passed by the evaluator and by your own read of the march. I did not measure
cause 2's Route A end to end (thirty re-tags is a build, not a measurement) or the two engine rules
in cause 5; each is a scratch-engine run of about an hour once you say yes. Nothing was written to
your machine: no folder is connected to this session, so this document is in the project as
`claude/Fairway_evaluator_verdicts_review_8Sep.md` and sent to you as a file; it belongs in the
repo as `docs/evaluator-verdicts-review-8sep.md` when a session next writes over the bridge.

## 8. What I need from you, in order

1. The six fixture re-tags in cause 1 (yes or no each; supercritical: secondary or primary).
2. Hop-aero: strike (recommended). Ultrasonium: keep your 6 September ruling or strike.
3. Cause 3: does a label-only lane price? (Recommendation: names, no range.)
4. Cause 4: closeness on weighted evidence, and the fourteen stopwords (recommendation: yes to both).
5. Cause 2: Route A after march 2, or Route B now (recommendation: A after march 2, caveat now).
6. Cause 5: permission to measure E1 and E2 on all 142 (no change proposed until measured).

Once you answer, the next session builds what you approved in a fresh clone, runs the twenty checks,
rebaselines golden with each reason written, and hands you one `git add -A` block.

---

# APPLIED: Daniil's answers of 8 September, and what was built on them (Fable, 9 September 2026, 00:25 UK)

Built in a fresh clone of origin at `41d64fa`, the files written into the working tree on the Mac
over the bridge, no git run. Suite: **twenty checks, all pass** (0 skipped as required, 1 to 18 and
20 run). **Gate 130 of 142**, the same count as before with a different composition: fundraisly,
lyka and princeps now PASS; ekho-labs, lambda-robotics and supercritical now FAIL, each for a
reason written on its profile. **Golden rebaselined, 130 of 142 fixtures moved, every move
attributed** (the record is `docs/golden-attribution-8sep.txt`): 96 moved only in the closeness
label or the shared-words list (rule A14), 11 re-tagged fixtures, 10 through the Route A rows, 3
through the folded end-market labels, 10 through the stopwords changing a score by a few tenths
(bond loses BlackLine, Sidetrade and Zuora, which was the point; moov swaps MoonPay for Rapyd; the
rest are one name at the edge of a lane).

## What his answers were, and what each became

| his answer | what was done | where |
|---|---|---|
| **Fundraisly**: rating agencies wrong; HubSpot somewhat; Freshworks and Salesforce not; the angle is a platform to find investors | Re-tagged on that angle: investor database and outreach platform, Horizontal, sales-intelligence words. Listed **ZoomInfo, Red Violet, Similarweb**, HubSpot in the wider ring; private **Clay, Apollo.io, 6sense**. Gate FAIL to PASS. Red Violet is a stray. Morningstar (owns PitchBook, which Fundraisly names as a competitor) is a pin he can add by name. | `selector/golden_profiles.py` |
| **Fundraisly is our investor tool "on steroids"; analyse how they work and replicate** | Written into the status document as a TO DO with a first read of their own comparison table (300k investor database, investor intelligence, warm and targeted outreach, service, warm paths from unicorn founders, $1k to 5k a month). | `docs/STATUS-2026-09.md` |
| **Publora**: TomTom, PagerDuty, ZoomInfo, Sprinklr wrong; Sprout somewhat; Buffer good | No re-tag (he did not ask for one). Buffer is the best product match in the private pool and is cut by the seven-name cap because its only round is October 2014; a pin would bring it in. Recorded as an open question. | status document |
| **Supercritical**: Sea, MELI, Meesho wrong; Xpansiv closer; IEX ok; check STX; very similar to levelten | Re-tagged as a levelten twin (exchange first, marketplace second, environmental-commodities words). Listed **Indian Energy Exchange, CME, Multi Commodity Exchange of India**; private **Xpansiv** alone, unpriced, so it FAILS the gate as levelten does. **STX checked:** right sector, a principal trader with a credit facility rather than a marketplace, no priced equity round surfaced; on the sourcing list with that caveat. | profiles; `docs/sourcing-list-8sep.md` |
| **Alloovium**: Procore, Trimble, Bentley make sense | Re-tagged: end market Construction & Infrastructure, no Data & AI secondary. Listed **Procore, Trimble, Bentley**, DIRECT. | profiles |
| **Emergent**: agree; why not Lovable and Replit? | They are in its private lane and always were (Lovable 25.3, Replit 19.7). Only the listed lane lacked an equivalent, because both are private. Nothing changed. | |
| **Kita**: not a lender; closer to Mambu, Tuum, Thought Machine | Re-tagged software first. Listed **Fair Isaac, Blend, Qualco, Q2, FIS, Jack Henry, EVERTEC**; private **Sapiens, Mambu**, Carta, Accolade, AuditBoard, Cityblock. Upstart and Pagaya leave (his lender fence). Tuum and Thought Machine are not in the pool: sourcing list. | profiles; sourcing list |
| **The comp-of-a-comp rule** (look up the neighbours of a near-perfect comp, throughout the fixtures) | Rule **A16** in the rulebook. It is a data pull, so it runs inside the bulk pass after the 18 September march (A12 part 3), over every fixture with a DIRECT name; the sourcing list carries the first neighbours (Mambu to Thought Machine, Tuum, 10x, Provenir, Taktile, Zest). **Say if you want it run now instead.** | `docs/RULES.md` |
| **Ekho-labs**: Samsara agreed; Kinaxis, Manhattan, Tecsys less perfect; Eurowag | Route A (below); Samsara **pinned on his word** (it shares no product word); the Data & AI secondary dropped because it handed the set GB Group, Similarweb, ZoomInfo and Amplitude. Listed **Kinaxis, Tecsys, Manhattan, Samsara**; private **E2open** alone, so it FAILS the gate until a second priced supply-chain software round is sourced. Eurowag on the sourcing list. | profiles; sourcing list |
| **Manifold**: close to Boston Dynamics | Boston Dynamics is a Hyundai subsidiary with no standalone price and cannot be a comparable. Symbotic, AutoStore, Locus, Exotec, Agility, GreyOrange on the sourcing list. Set unchanged (his 6 Sep pins hold the private lane). | sourcing list |
| **Lambda-robotics**: same as ekho-labs; Vention and Applied Intuition make sense | Cloud & Infrastructure secondary dropped. Private **Vention, Applied Intuition**, 1 priced, gate PASS to FAIL until a listed robotics maker is sourced. | profiles |
| **Subvysion**: close to alloovium, also serving contractors | Its listed lane already is (Nemetschek, Procore, Bentley, Autodesk, Trimble) and alloovium's now converges on it. Both private lanes wait for a construction round (sourcing list). Its label-only private lane is cause 3, parked on his instruction. | sourcing list |
| **Derya**: close to Salesforce, vertical; plus the supply-chain peers | Route A archetype first, Business Applications second, as he read it. Listed **Kinaxis, Manhattan, SPS Commerce**, DIRECT; private E2open and business-application rounds. The tension with the company's own page (a services-led broker that has handled $15m of freight) is written on the profile so he can reverse it. | profiles |
| **Princeps**: priced as insurers; sourcing issue | The Insurance end market folded (TAKEOVER 7): princeps and florin carry Insurance, as do Wefox, Coalition, The Zebra and Sapiens. Princeps now PASSES on **Crawford, Trupanion, CCC** (claims, pet insurance, claims software), which is insurance and still not a data-centre insurer; florin gets **Guidewire, FINEOS, Crawford, ZhongAn, Trupanion**. Specialty P&C carriers on the sourcing list. | `tools/apply_industry_folds_8sep.py`; sourcing list |
| **1: agree, proceed** | The six re-tags above plus lyka; the four profiler rules in the prompt with check 17 asserting them (rule A13); the end-market folds (10 rows, count in 204, count out 204). | profiles; `selector/profiler.py`; `tools/check_profiler.py`; `tools/apply_industry_folds_8sep.py` |
| **2: Route A** | `Supply Chain & Logistics Software`, software family: Kinaxis, Manhattan, Tecsys first (Tecsys keeps Healthcare, its market), E2open first; Samsara, Freightos, Full Truck Alliance, Loadsmart, Shiprocket second (Shiprocket stays with the operators first so byrd, hived and 99minutos keep it). Fork route and investor aliases added. 9 rows across three files, count in equals count out on each. Rule A15. | `tools/apply_supply_chain_software_8sep.py`; `selector/quiz_fork.py`; `selector/investors.py` |
| **3: parked, add to the status document** | The label-only fallback lane (subvysion private, blindspot listed and the other kind-1 lanes) still prices at the ADJACENT band with no caveat that says "label only". Written into the status document as open, to be revisited after the bulk pass, as he expects re-tagging and data to shrink it. | status document |
| **4: approved; generic words cannot count** | Rule **A14**: the closeness label and the shared-words sentence ignore words carried by 25 or more companies; the stopword list is eighteen words. The weight file regenerated: 405 in, 400 out, the five dropped named (a, as, in, on, to); check 16 green. Gate rule 4 narrowed so a set anchored on end market plus archetype, or on a narrow archetype, is not called "nothing" (it had failed fyle, tienda-pago, wondering and moov on the new label). **Scope choice to flag:** a generic word still scores its small weight and still clears the relevance gate, because zeroing it was measured on 6 Sep to cost real passes; he can widen the rule. | `selector/match_reference.py`; `tools/peer_universe_check.py` |
| **E1: BARK must be in lyka's set** | Both sell pet products; lyka carried Food & Grocery and BARK and Chewy carry Retail & E-commerce, so the end-market test kept the highest-scoring name out. Lyka re-tagged to the pool's pet label: listed **BARK 30.7, YETI, Hims & Hers**, DIRECT, Chewy in the wider ring; private keeps Huel and AG1, gains Thrasio, Quince, SKIMS, loses OLIPOP and Liquid Death. Gate FAIL to PASS. A Pet Care end market would be cleaner (sourcing list, taxonomy build). **E1 as a general rule then measured on all 142: zero fixtures move**, so no rule change is proposed. | profiles |
| **E2: measure first** | Measured two ways on all 142. Strong form (score lifted to the floor): 15 lanes move, and it lets Rent the Runway into a parcel network on "reverse logistics", Verint into a voice app, Microsoft into an agent runtime. Gentle form (exempt from the adequacy floor, score unchanged): 3 lanes move; denta gains ZhongAn and loses Veeva, rybbit gains Adobe and loses five names, florin loses Crawford and Trupanion. **Rejected both ways** under the 6 Sep rule that a variant admitting a wrong name elsewhere is not built. ZhongAn for denta is a pin if he wants it. | `measure_e1_e2.py` (scratch, not in the repo) |
| **6: resolved by re-tagging?** | Partly. The three fixtures (orchids, 21st, chronicle) are correctly tagged; the Design & Engineering archetype itself mixes CAD and EDA vendors with design tools. Only a split like Route A fixes it; post-pilot, with the taxonomy rule. | status document |
| **7: sourcing list; he will provide comps later** | `docs/sourcing-list-8sep.md`: every name above with what it fixes and the caveats, plus the A16 procedure and one that touches his 8 Sep reading (Appen, Innodata and TELUS Digital are listed training-data vendors; put to him before they are pulled). | `docs/sourcing-list-8sep.md` |

## Still open for him, as of 00:25 UK, and what he answered by 10:10 UK the same morning

1. **Hop-aero and ultrasonium strikes**: ~~not answered; both untouched.~~ **Hop-aero struck, 9 Sep**
   ("definitely should not be compared to FedEx and UPS. This is a US military contractor. Should be
   compared to such."); fails the gate as kind 4; defence contractors and launch companies put on the
   sourcing list. **Ultrasonium not ruled on, untouched.**
2. **Publora**: ~~pin Buffer or leave as is.~~ **Pinned, 9 Sep** ("indeed seem to match with Buffer").
3. **The label-only fallback lane** (cause 3): parked on his word until after the bulk pass. Unchanged.
4. **Whether A14 should also zero generic words in the score**: ~~not done.~~ **Done, 9 Sep.** His
   question was why it had been zeroed in one place and not the other; the answer is that the 8-Sep
   change reached the label and the shared-words sentence (what a founder reads) and not the score
   and the relevance gate (what the engine decides), on the strength of the 6-Sep measurement. His
   ruling covers both. `GENERIC_WORDS_SCORE = False`; measured first (108 lanes across 67 fixtures),
   applied, 92 golden files moved and attributed (`docs/golden-attribution-9sep.txt`), gate 130 to
   125: acti, lyka, rainforest and tienda-pago now rest on one priced private round each.
5. **Derya**: ~~his reading or the company's page.~~ **Answered, 9 Sep**, to his "do you not agree
   with my reading?": half. His reading fits what Derya sells; its YC page (read again 9 Sep) says it
   executes procurement, shipping and customs for hardware companies and counts "more than $15M in
   freight" handled, which is how a forwarder measures itself. His tagging stands (Kinaxis,
   Manhattan, SPS Commerce listed), the page's reading stays on the profile, and the point that will
   matter when it is priced is the basis: a broker's turnover is the freight, its margin is the
   revenue.
6. **The three listed training-data vendors**: ~~against his reading of 8 Sep.~~ **Kept, 9 Sep**
   ("noted, keep it").
7. **The comp-of-a-comp rule (A16)**, scheduled for the bulk pass: **run now, 9 Sep** ("pass it
   now"). 91 DIRECT names, 55 fixtures, 240 rows in, 39 merged, OFX Group dropped by name, 200
   candidates out with a source each (46 listed, 154 private), none loaded:
   `docs/a16-neighbour-pass-9sep.md`.
8. **The sourcing list** is now carried in full inside `docs/STATUS-2026-09.md` on his word ("otherwise
   it will get lost"); the file stays as the copy to edit first.
