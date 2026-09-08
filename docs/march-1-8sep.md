# March 1 of four: 8 September 2026

**What a march is.** Daniil's ruling of 5 September, 23:10 UK (rule A12 part 3): on 8, 11, 15
and 18 September we run a march, not a data pull. Thirty to forty new test companies each time,
taken at random from Y Combinator and Product Hunt with no regard for whether we hold comparables
for them. The point is to find the blind spots before founders do. The pool is big enough; a gap
found here goes on the No-comps list and is resolved once, in bulk, after the 18 September march.
Nothing in this document is a request to pull data now.

**Headline.** 40 new companies, fixtures 102 to 142. **Gate 135 of 142** (97 of 102 before; 38 of
the 40 new companies pass). Two new failures, both honest: Ornadyne (military reconnaissance
drones) and PRINCEPS (insurance for data centres). Nineteen checks, all pass. Golden rebaselined:
40 new fixture files, none of the 102 existing fixtures moved.

**One thing to decide, Daniil, at the foot: whether three of the forty should carry a stage other
than Seed.**

---

## 1. How the forty were chosen

Read in Chrome on 8 September 2026 between 18:20 and 18:35 UK:

- `ycombinator.com/companies?batch=Fall 2026` (37 companies, the whole batch so far)
- `ycombinator.com/companies?batch=Summer 2026` (the first 80 of 234 the page loads)
- `ycombinator.com/companies?batch=Spring 2026` (the first 60 of 195)
- `ycombinator.com/companies?batch=Winter 2026` (the first 60 of 199)
- `producthunt.com/leaderboard/weekly/2026/36/all` (36 launches, week of 31 August)

Every company on those pages that was not already one of the 102 went into a pool: 36, 68, 55, 59
and 29 names. Left out before the draw, with the reason: the 19 names already in the fixture set
(Maritime, Edviro, Caution, Magma, Osseus, Wondering, Florin, Hop Aero, Levocred, Care GP,
Agentcard, Denta, Ekho Labs, Akkari, InsForge, ProjectX, Apollo Atomics, Plena Health, Unifold);
three Product Hunt entries that are a model or feature release by OpenAI or Google, because a
founder cannot be compared with a feature; a SurveyMonkey advert on the Product Hunt page; and Nex
and Hyperprobe, which appear on both lists and were kept once, in the YC pool.

Eight were then drawn from each pool by a seeded random draw (Python `random.Random(20260908)`,
the date, so the draw is reproducible; the pool and the draw are in the session's `pool.py` and
the first eight of each shuffled list were taken in order). Nobody chose a company by hand.

Two guessed page addresses returned nothing (`/companies/playabl-ai`, `/companies/aster`); both
companies were found through the directory search (`/companies/playablai`, `/companies/asterlab`)
and read there. No company was substituted.

## 2. The forty, one line each

Every company is real and was read off the page named. The label in the fixture is the company's
own tagline. "Stage" is what the page states; none of the forty pages states a funding stage, so
the Seed default at the foot of `selector/golden_profiles.py` applies to all forty as a stated
test condition, not as a claim about any of them.

### Fall 2026 (YC)

| key | company | what it sells, in one sentence | website | page read |
|---|---|---|---|---|
| orca-aerospace | Orca Aerospace | Onboard AI spacecraft operators: LLMs controlling a satellite from the vehicle through deterministic tooling. | orcaaerospace.com | ycombinator.com/companies/orca-aerospace |
| simulithic | Simulithic | Simulations of a company's real users, grounded in session data, to predict how a product change performs before it ships. | simulithic.com | ycombinator.com/companies/simulithic |
| qokedas | Qokedas | Turns real-world signals that are never written down into training data so AI labs can make models better at science. | qokedas.com | ycombinator.com/companies/qokedas |
| lambda-robotics | Lambda Robotics | Builds and deploys robots for the data-centre infrastructure that runs frontier AI. | lambdarobotics.ai | ycombinator.com/companies/lambda-robotics |
| quippy | Quippy | Consumer daily-practice app for social skills: short realistic conversations with line-by-line feedback and an adaptive curriculum. | quippyapp.com | ycombinator.com/companies/quippy |
| herdr | herdr | Open-source (Apache-2.0) runtime for fleets of coding agents: a background server owns their terminal sessions, an attention queue, CLI, socket API and plugin marketplace. | herdr.dev | ycombinator.com/companies/herdr |
| vorelios | Vorelios | Foundation models that learn physics end to end and replace slow engineering simulations with results in seconds. | vorelios.com | ycombinator.com/companies/vorelios |
| nodus-compute | Nodus Compute | "Intelligent execution layer for AI workloads"; the page says nothing more, so the tags stay close to that line. | nodus-compute.ai | ycombinator.com/companies/nodus-compute |

### Summer 2026 (YC)

| key | company | what it sells, in one sentence | website | page read |
|---|---|---|---|---|
| openrelay | OpenRelay | One inference endpoint routed across accelerators and clouds, two-sided: GPU owners plug their capacity in. Launch post: 100 billion tokens a week across 22 locations. | openrelay.inc | ycombinator.com/companies/openrelay |
| praxis-robotics | Praxis Robotics | Captures first-person human demonstration data inside real businesses and sells it to frontier labs and humanoid companies as robot training data. | praxisrobotics.io | ycombinator.com/companies/praxis-robotics |
| subvysion | SubVysion | Autonomous rovers with ground-penetrating radar that map underground utilities to the centimetre; a mapping service sold to construction contractors. | subvysion.com | ycombinator.com/companies/subvysion |
| derya | Derya | AI-run supply chain service for hardware companies: procurement, shipping and customs, production visibility, executed for the customer. Launch post: more than $15M of freight handled. | usederya.com | ycombinator.com/companies/derya |
| chromie | Chromie | AI operating system for government contractors: opportunity signals before the RFP, win-probability models, proposal drafting, a company brain. | chromie.dev | ycombinator.com/companies/chromie |
| opentag | OpenTag | Model-agnostic AI coworker in Slack and Teams that does tasks in the thread, keeps the company wiki current and suggests automations. Launch post: live with 10 teams. | tryopentag.com | ycombinator.com/companies/opentag |
| princeps | PRINCEPS | AI-native insurance company for the compute buildout: underwrites SLA, GPU residual-value and outage risk for data centres and neoclouds. London. | princeps.dev | ycombinator.com/companies/princeps |
| markov | Markov | Sells expert computer-use training data (screen recordings, actions, annotations) to frontier AI labs; the page says 33k+ hours sold. | markovstudios.com | ycombinator.com/companies/markov |

### Spring 2026 (YC)

| key | company | what it sells, in one sentence | website | page read |
|---|---|---|---|---|
| ornadyne | Ornadyne | Flapping-wing reconnaissance drones for the military that look, fly and sound like birds. Defence hardware; out of market. | ornadyne.com | ycombinator.com/companies/ornadyne |
| panacea | Panacea | FDA regulatory services for biotech and medical-device companies: ex-FDA consultants paired with an AI platform, fixed milestone pricing. A services business. | withpanacea.com | ycombinator.com/companies/panacea |
| gigacatalyst | Gigacatalyst | An AI customisation layer embedded inside a B2B SaaS product so its customers build their own dashboards, reports and forms on the vendor's APIs. | gigacatalyst.com | ycombinator.com/companies/gigacatalyst |
| raspire | RASPIRE | Runtime security for mobile apps: upload the compiled app, it is hardened automatically, attacks are detected and blocked in production. Launch post: apps used by 20M+ end users. | raspire.com | ycombinator.com/companies/raspire |
| playabl | Playabl.ai | A TikTok-style feed of user-generated games anyone can play, create from a prompt, publish and monetise; own AI-native game engine. Page: 40k DAU, 300k WAU (June update). | playabl.ai | ycombinator.com/companies/playablai |
| aster | Aster | An autonomous research lab: thousands of AI research agents orchestrated in parallel toward one goal. What it charges for is not on the page. | asterlab.ai | ycombinator.com/companies/asterlab |
| auxos | Auxos | AI customer twins for market research: 1:1 replicas of a company's customers built by interviewing real people, then a 24/7 simulated panel that tests ads, pricing and pages in minutes. | useauxos.com | ycombinator.com/companies/auxos |
| lattice-health | Lattice Health | Read-only monitoring and governance layer for medical imaging AI deployed in hospitals: agreement with the radiologist, drift, subgroup performance, compliance evidence. | latticehealthai.com | ycombinator.com/companies/lattice-health |

### Winter 2026 (YC)

| key | company | what it sells, in one sentence | website | page read |
|---|---|---|---|---|
| turnstone | Turnstone | A local AI workspace that turns a person's email, calendar, Slack, Drive and folders into a second brain shared by their agents; runs on their own machine and model. | myturnstone.ai | ycombinator.com/companies/turnstone |
| constellation-space | Constellation Space | AI operating system for satellite constellations: predicts link failures and reroutes traffic autonomously; sold to satellite operators. Launch post: design-partner phase. | constellation.space | ycombinator.com/companies/constellation-space |
| foreman | Foreman | All-in-one AI project management for construction contractors: takeoffs, estimates and proposals from plans, then every document and change order in one place per job. | foreman.co | ycombinator.com/companies/foreman |
| daivin | DAIVIN! | Tankless dive gear: a vest with electrolysers that makes breathable oxygen from water, for professional, commercial and military divers. Hardware; out of market. | daivin.tech | ycombinator.com/companies/daivin |
| fed10 | Fed10 | Legislative consulting staffed by AI agents: monitors every bill, flags threats to a business, drafts the fix, says who to call. | fed10.ai | ycombinator.com/companies/fed10 |
| veriad | Veriad | An agent that checks marketing content against brand and legal guidelines before publication, for enterprises with large ad spend. London. | veriad.com | ycombinator.com/companies/veriad |
| zymbly | Zymbly | Voice-first agents for aircraft maintenance technicians: troubleshooting across manuals, parts ordering, voice notes into compliant paperwork; sold to airline maintenance teams. London. | zymbly.com | ycombinator.com/companies/zymbly |
| remix | Remix | Consumer app that auto-generates social posts, articles, carousels and short video from a person's own photos, voice notes and profiles. | remix.re | ycombinator.com/companies/remix-3 |

### Product Hunt, week of 31 August 2026

| key | company | what it sells, in one sentence | website | page read |
|---|---|---|---|---|
| brandjet | BrandJet AI | Outreach campaigns across email, LinkedIn, WhatsApp and Instagram plus brand and competitor tracking with sentiment analysis. | brandjet.ai | producthunt.com/products/brandjet-ai |
| myaicademy | myAIcademy | Personalised AI-skills training for a person's role and tools: follow-along lessons, simulations of real AI tools, in-work guidance. | myaicademy.com | producthunt.com/products/myaicademy |
| airtop | Airtop | Describe a workflow in plain English and it compiles into a coded web automation that logs in, browses and completes tasks, healing itself when a run breaks. Sixth launch. | airtop.ai | producthunt.com/products/airtop |
| world-labs | World Labs (Atlas) | A world model: text, images, video and 3D in, camera-controlled video out, scene reconstruction and space-time simulation for robotics; early access. | worldlabs.ai | producthunt.com/products/atlas-by-world-labs |
| browzer | Browzer | Connect a GitHub repo and it drafts docs, guides, changelogs and blog posts and heals them on every merge; automates a DevRel team's technical output. | trybrowzer.com | producthunt.com/products/browzer |
| magicrew | MagiCrew | Open-source AI agent platform: specialised digital workers that research, analyse and write reports and presentations, with enterprise controls. | magicrew.ai | producthunt.com/products/magicrew |
| twelvelabs | TwelveLabs (Compliance) | Video-understanding models sold as an API; this week's launch reviews a video library against the customer's own compliance rules. Sixth launch. | twelvelabs.io | producthunt.com/products/twelvelabs |
| dif-sh | dif.sh | Open-source feature flags as markdown files living with the code, installed by a coding agent, with a paid cloud that reads the results. | dif.sh | producthunt.com/products/dif-sh |

## 3. The gate, re-scored

`python3 tools/peer_universe_check.py`: **142 fixtures, 135 refine the peer universe, 7 do not.**
Before the march: 97 of 102. Of the 40 new companies, 38 pass.

The seven that fail, and why, in the tool's own words:

| fixture | why it fails |
|---|---|
| apollo-atomics | no public lane with 2 priced comparables (core 0, secondary 0); no lane produced a range object. Unchanged since 3 Sep. |
| fundraisly | no private lane: 1 priced round. Unchanged. |
| levelten | no private lane: 1 priced round. Unchanged. |
| lyka | no public lane with 2 priced comparables. Unchanged. |
| mondu | no private lane: 1 priced round. Unchanged. |
| **ornadyne** (new) | no public lane with 2 priced comparables (core 0, secondary 0); every lane is THIN_OVERLAP; the set rests on nothing but a shared word. The listed side reached government-software names (Tyler Technologies, i3 Verticals, Via) on the Government end market alone; the private side was rescued on the Design & Engineering label with Vention, Canva, Applied Intuition and Figma. There is no defence hardware in the pool. |
| **princeps** (new) | no public lane with 2 priced comparables (core 0, secondary 0); every lane is THIN_OVERLAP. The listed side reached wealth and banking software (HUB24, Netwealth, nCino, Temenos, SS&C) on the Financial Services end market alone and none of them priced; the private side holds Sapiens, Wefox, Coalition and The Zebra, two of them priced. Insurance for compute infrastructure has no public insurer in the pool. |

Eleven pass with an empty secondary lane (allowed since 4 Sep), seven of them new: constellation-
space, herdr, praxis-robotics, qokedas, remix, simulithic and subvysion, beside acti, bylaw, clera
and emergent from before. Seventeen of the 142 pass with a secondary lane resting on one priced
name, reported and not decisive.

## 4. The No-comps list, grown

Check 8 prints all three kinds. After the march:

**Kind 1, served on a label, not on evidence: 10 lanes, 52 comparables** (2 lanes, 8 comparables
before). The eight new lanes, each a hole in the pool rather than a feature:

| fixture | lane | what the fallback handed it, on which label |
|---|---|---|
| vorelios | listed | GB Group, SoundHound, Dynatrace, Snowflake, Elastic, LiveRamp on Data, AI & Developer Tools. No engineering-simulation company is in the pool. |
| markov | listed | Snowflake, Elastic, Dynatrace, GB Group, MongoDB, Palantir on Data, AI & Developer Tools. No listed training-data vendor is in the pool. |
| daivin | listed | Bentley, PTC, Dassault, Autodesk, Figma, Lectra on Design & Engineering. Dive gear handed CAD software: the rule A11 consequence, again. |
| daivin | private | Applied Intuition, Figma, Miro on Design & Engineering. Same. |
| nodus-compute | private | Oxylabs, Anthropic, Clay, Lovable, Supabase on Cloud & Infrastructure and Data, AI & Developer Tools. |
| ornadyne | private | Canva, Applied Intuition, Figma on Design & Engineering. Drones handed design software. |
| quippy | private | WHOOP, Udemy, Oura, Vedantu, upGrad, MasterClass on Online Learning and consumer software. Its listed lane is fine (Duolingo, Coursera, Nerdy). |
| subvysion | private | Owner, Mews, Canva, Sapiens, Clio, Guesty on Vertical Software and Design & Engineering. Its listed lane is fine (Nemetschek, Procore, Bentley, Autodesk, Trimble). |

**Kind 2, not served at all: 7 of 142 fixtures** (5 of 102 before), the table in section 3.

**Kind 3, served on a generic word or the end market alone: 428 of 1,570 comparable slots**
(302 of 1,120 before), 315 on words carried by 25 or more companies and 113 on the end market
alone; 102 fixtures and 167 of 284 lanes carry at least one. **Lanes resting on nothing else: 8**
(4 before); the four new ones are qokedas listed, praxis-robotics listed, princeps listed and
ornadyne listed. qokedas and praxis-robotics reach Snowflake and Palantir on the words "ai" and
"data" alone.

## 5. What the march found, read by a person rather than by the gate

The gate scores whether a lane holds priced names. It does not score whether the names make
sense, and that is where a march earns its keep. Reading the 40 new sets side by side:

1. **Aerospace, space and aviation have no home in the pool or in the vocabulary.** Orca
   Aerospace passes on Samsara, Constellation Software and Rubrik (listed) and Owner, Applied
   Intuition, Guesty and Restaurant365 (private). Constellation Space passes on Amdocs, Cerillion
   and Oracle (Telecom, fair) and on Owner, Guesty and Restaurant365 (not fair). Zymbly, aircraft
   maintenance, passes on Samsara, BlackLine and Blackbaud, and on TravelPerk plus restaurant and
   healthcare rounds. All three are passes a banker would strike. TAKEOVER item 11 (an Aerospace &
   Defence end market) now has three more names behind it.
2. **Vertical Software with a Horizontal end market is a catch-all that hands out restaurant and
   hospitality rounds.** Owner, Guesty and Restaurant365 appear in the private lanes of orca-
   aerospace, constellation-space, zymbly, foreman and fed10. This is exactly the case the
   taxonomy rule (ruled yes 6 Sep, build after the pilot) is written for: an archetype match only
   counts when the industry matches too.
3. **Hardware keeps getting design software.** Ornadyne and DAIVIN! follow Ultrasonium and Apollo
   Atomics into Design & Engineering and Owned-Inventory Retail, and are handed Figma, Canva,
   Miro and CAD vendors. Rule A11 says hardware is filed under what it sells; the pool has almost
   nothing that sells hardware. Both are OUT_OF_MARKET and fail or pass on labels, so nothing
   wrong reaches a founder, but the fourth march will find more of these.
4. **AI training-data vendors have a good private lane and no listed lane.** Markov, Praxis and
   Qokedas all reach Scale AI, Turing, Invisible Technologies and Bright Data on the private
   side, which is right, and Snowflake and Palantir on the listed side on the words "ai" and
   "data", which is not. A listed data-services name or two belongs on the bulk-pass list.
5. **Engineering simulation is absent.** Vorelios reaches Anthropic, Clay and Cohere privately and
   nothing on the listed side except the label. Synopsys and Cadence are in the pool and reached
   emergent on the word "automation"; nothing brings them to a physics-simulation company.
6. **Insurance for a new asset class fails cleanly.** PRINCEPS is the first insurtech fixture to
   fail: florin and denta pass because they insure businesses and teeth, which the pool covers.
7. **Government affairs reaches legal software and not the obvious listed peer.** Fed10 gets
   Intapp, LegalZoom, Legora, Harvey and Clio. The listed company that does what Fed10 does
   (legislative and regulatory monitoring) is not in the pool; a name for the bulk pass.
8. **Where the pool is deep the sets are good.** Playabl gets Roblox, Epic Games, Voodoo and
   Patreon. RASPIRE gets SentinelOne, Zscaler, Fortinet, Wiz, Snyk and Cato. myAIcademy gets
   Duolingo, Coursera, Docebo, Udemy and upGrad. OpenRelay, Nodus and herdr get the cloud names.
   Auxos and Veriad get the marketing-software names. The three frontier-lab products (World
   Labs, TwelveLabs, Aster) get Anthropic, OpenAI and Cohere. A founder in those markets is served.
9. **One re-tag on the way, and it is a tagging lesson.** Quippy tagged Consumer & Prosumer
   Software first got F-Secure, Life360 and Opera on the word "app" and never reached Duolingo.
   Tagged Online Learning first (the way wondering is tagged, and the way the page's own tags
   lead) it gets Duolingo, Coursera and Nerdy. The learning archetype has to be primary for the
   learning peers to arrive; a consumer learning app tagged as consumer software first is served
   on "app".

None of this is chased now. Items 1, 3, 4, 5, 6 and 7 are sourcing gaps for the bulk pass after
the 18 September march. Item 2 is the taxonomy rule, already ruled, build after the pilot. Item 9
is a tagging lesson for the profiler and for marches 2 to 4.

## 6. Golden: what moved and why, written before the rebaseline

Run before writing: `python3 selector/golden.py` reported **102 ok, 40 MISSING FIXTURE, 0 DIFF,
0 SCORE.** So the only change to the golden set is the creation of 40 new fixture files; no
existing fixture's comparables, ranges or investor list moved, because adding a fixture changes
nothing about any other fixture's selection. Quippy was re-tagged once (section 5, item 9)
before its baseline was written, so the written baseline holds the Online Learning tagging.
`python3 selector/golden.py --write` then wrote 142 files and the check reads 0 of 142 moved.

## 7. Suite

`FAIRWAY_NO_GIT=1 sh tools/check_all.sh` in a fresh clone of origin at `91c3d7a` with these
changes applied: nineteen checks (0 skipped as required, 1 to 18 run), all pass. Check 11 walks
142 fixtures, 1,121 callable cards; check 12 reports 7.9 houses a founder and one fixture with
fewer than three (ornadyne, 1); check 13 renders market position for 134 and evidence gaps for
142; check 14 assembles 142 of 142 payloads, 140 able to show two or more peer charts with no
founder figure. Golden 0 of 142 moved. Gate 135 of 142.

## 8. For Daniil: one decision

**Three of the forty are visibly not seed companies and carry the Seed default anyway.** World
Labs (a frontier lab with a long funding history), TwelveLabs (sixth Product Hunt launch, a model
platform sold to enterprises) and Airtop (sixth launch; the founder previously founded Adap.tv and
Shopping.com). None of the pages read states a stage, and the rule is that nothing goes on a
fixture the page did not say, so all three sit at Seed as a test condition. The stage decides
which investors a founder is shown, so at Seed these three get seed funds. Say a stage for each
and it goes on the fixture; say nothing and the default stands, which is harmless for a test set
and wrong for a real founder.

## 9. Files

`selector/golden_profiles.py` (the REAL_4 block, OUT_OF_MARKET extended, PROFILES assembly),
`selector/golden/*.json` (40 new files), this document, `docs/STATUS-2026-09.md`.
