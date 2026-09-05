# Fairway, 5 September 2026, evening. Claude's pull under the 4-Sep work order.

Written 21:15 UK, Saturday 5 September 2026, by the clock. Work order: `docs/prompts/work-order-claude-4sep.md`.

## The short version

- **27 private rounds written, 24 companies, every figure read on its URL on 5 September.** 24 rounds
  for the thin private lanes plus the three control transactions the work order names (Sapiens,
  Accolade, Udemy). LTG is not in: its offer value is not on any page I could reach without search.
- **19 investor houses written, 17 CALLABLE and 2 EVIDENCE.** Callable houses reaching Consumer &
  Prosumer Software go from 14 to 47 (16 from the pull, 17 promoted from the new rounds' own investors by the builder's existing rule, banded by round size so they do not reach a seed founder), Online Learning from 3 to 12. Short of the thirty asked for,
  and the reason is in Part 2.
- **The gate moves from 81 to 89 of 102 on the dry run**: agentcard, bizmark, finn, marble, osseus,
  payna, priori-legal and wispr-flow flip to PASS. Nothing regresses. All fourteen checks pass on the
  loaded scratch copy, golden rebaselined.
- **Nothing is loaded on the laptop.** Rule D14: raw first. Commit 1 is the raw files, the scripts and
  these documents. Then `python3 tools/load_claude_pull_5sep.py` does the load and refuses to run
  until git says the raw files are committed. Commit 2 is the load. Both blocks are at the foot.
- **One constraint to know about.** This session's web search was capped at 200 calls and the cap was
  reached partway through the sourcing. Every KEPT figure was verified page by page after that; the
  REJECTIONS marked "no source" were made fetch-only and are weaker. A follow-up list is at the end.
- **Your dedupe rule was applied**: company plus month plus post-money, name matching token-based and
  case-insensitive, against all 290 held rounds. Zero name overlaps, so no collisions to manage; the
  three you named (wefox, Monzo, AG1) are untouched. None of the 27 new rows is a company we hold.

## Step 0, the two diagnostics read together

`thin_lane_diagnosis.py`: 17 thin lanes, all 17 confirmed as genuine sourcing requests (the next-best
name in our own database is BROAD-tier in every case). `peer_universe_check.py`: 81 of 102, and 16 of
the 21 failures are "fewer than two priced private rounds". So no lane was skipped as a tier or ruling
question. The eighteen fixtures in the order split as follows after sourcing:

| fixture | before | rows added to its lane | after (dry run) |
|---|---|---|---|
| agentcard | 1 priced | Slash, BVNK (Moss held) | PASS |
| bizmark | 0 priced | E2open (CONTROL), Berkshire Grey reaches it too | PASS |
| finn | 1 priced | Spinny, Moove x2 | PASS |
| marble | 1 priced | Owner (Restaurant365 held) | PASS |
| osseus | 1 priced | Applied Intuition, Vention | PASS |
| payna | 1 priced | Legora (AuditBoard held) | PASS |
| priori-legal | 1 priced | Legora, plus Mercor and Micro1 as marks | PASS |
| wispr-flow | 1 priced | Suno x2, Framer, Genspark | PASS |
| paymentkit | 0 priced | Zuora (CONTROL), Juspay, Cashfree | still FAIL, 1 priced: Juspay and Cashfree are gross-basis (see below) |
| clera, standout, nursa, tsenta | 0 priced | Mercor x2, Micro1 land in all four lanes | still FAIL: every disclosed figure in this archetype is gross billings (see below) |
| manifold-robotics | 0 priced | Berkshire Grey (CONTROL) | still FAIL, 1 priced |
| levelten | 1 priced | nothing qualified | FAIL |
| tash | 1 priced | nothing qualified | FAIL |
| ultrasonium, apollo-atomics | OUT_OF_MARKET | nothing qualified (pre-revenue sector) | FAIL, as expected |

**The basis trap, confirmed the hard way.** The work order's own warning was right. Mercor (Feb-25,
$2bn on $75m; Oct-25, $10bn on >$450m) and Micro1 (Sep-25, $500m on $50m) are the only rule-compliant
rounds in the talent-marketplace archetype, they land in the clera, standout, nursa and tsenta lanes,
and they price none of them: their ARR is stated by the CEO to be gross of contractor pay, the fixtures
default to NET_REVENUE, and gross never bands with net (B3). Same for Juspay and Cashfree against
paymentkit: Indian PSP revenue from operations is gross of processing cost. They are recorded honestly
as GROSS_REVENUE and they will price a founder who answers gross. What those five fixtures need is a
round that discloses NET revenue or ARR, and in this archetype nobody does.

## Part 1. Private rounds: count in, count out

**About 460 candidate-lane examinations across 18 lanes, 27 rows written.** Every kept row's valuation
and revenue sentence is quoted in its `notes` column with the URL, and the multiple is recomputed from
the two figures (identity check passes on all 27). FX at the ECB reference rate on the pricing date
(the Klarna convention): INR 85.44 (31-Mar-2025), 87.37 (5-Feb-2025), 91.86 (23-Jan-2026); EUR 1.1554
(5-Aug-2026).

### The 27 rows

| row | type | valuation $m | revenue $m, basis, period | x | in medians | note |
|---|---|---|---|---|---|---|
| slash-2026-04 | PRIMARY | 1,400 | 250 ARR run-rate, >, 2025 | <=5.6 | 1 | company release; TechCrunch says $300m the same day |
| bvnk-2024-12 | PRIMARY | 750 (around) | 40 annualized | 18.8 | 1 | Fortune exclusive; later Mastercard deal has no revenue |
| moss-2026-08 | PRIMARY | >1,155 (EUR 1bn) | >80.9 ARR (EUR 70m) | 14.3 | **0** | both floors, needs a ruling |
| zuora-2024-10 | CONTROL, listed | 1,700 | 445.8 LTM Jul-24, filed | 3.8 | 1 | LTM built from three 8-Ks |
| juspay-2026-01 | MIXED | 1,200 | 58.8 FY2025 rev from ops, gross | 20.4 | 1 | FY ten months old; primary plus secondary |
| cashfree-2025-02 | PRIMARY | 700 (sourced) | 73.6 FY2024 rev from ops, gross | 9.5 | 1 | flat revenue, loss-making |
| spinny-2025-03 | MIXED | 1,500 post | 545.1 FY2025 rev from ops | 2.7 | 1 | owned-inventory car retail; round grew to ~$170m |
| moove-2024-03 | PRIMARY | 750 post | 115 ARR | 6.5 | 1 | owned fleet, gig drivers, not consumer subscription |
| moove-2026-08 | PRIMARY | 2,100 | 420 ARR | 5.0 | 1 | includes acquired Kovi and Tokyo Taxi |
| e2open-2025-05 | CONTROL, listed | 2,100 EV | 607.7 FY2025 GAAP | 3.5 | 1 | shrinking; a true EV/revenue |
| berkshire-grey-2023-03 | CONTROL, listed | 375 | 65.9 FY2022 GAAP | 5.7 | 1 | distressed; $375m read as fully diluted equity, proxy cited |
| restaurant365-2023-05 | PRIMARY | >1,000 | >100 revenue | 10.0 | **0** | both floors, needs a ruling |
| owner-2026-08 | PRIMARY | 2,300 | >100 ARR | <=23.0 | 1 | front of house, not back office |
| auditboard-2024-05 | CONTROL | >3,000 | >200 ARR late 2023 | 15.0 | **0** | both floors, needs a ruling |
| legora-2026-04 | PRIMARY | 5,600 post | >100 ARR | <=56.0 | 1 | one row for the $600m round at the extension's post |
| applied-intuition-2025-06 | MIXED | 15,000 | ~400 ARR Dec-2024 | <=37.5 | 1 | ARR from The Information via techstartups.com, six months stale |
| vention-2026-01 | PRIMARY | >1,000 | <100 revenue | >=10.0 | 1 | CEO to The Logic; mostly hardware revenue |
| suno-2025-11 | PRIMARY | 2,450 post | 200 annual revenue | 12.3 | 1 | company to WSJ via TechCrunch |
| suno-2026-06 | PRIMARY | 5,400 | 300 ARR Feb-26 | <=18.0 | 1 | three months stale on a fast grower |
| framer-2025-08 | PRIMARY | 2,000 | 50 ARR | 40.0 | 1 | CEO to TechCrunch, break-even |
| genspark-2025-11 | PRIMARY | 1,250 post | >50 run rate | <=25.0 | 1 | investor's release, milestone dated before the round |
| mercor-2025-02 | PRIMARY | 2,000 | 75 ARR, gross | 26.7 | 1 | gross of contractor pay |
| mercor-2025-10 | PRIMARY | 10,000 | >450 run rate, gross, Sep-25 | <=22.2 | 1 | round page carries only a projection |
| micro1-2025-09 | PRIMARY | 500 | 50 ARR, likely gross | 10.0 | 1 | later coverage says gross |
| sapiens-2025-08 | CONTROL, listed | 2,500 | 549.1 LTM Jun-25, filed | 4.6 | 1 | work-order control transaction |
| accolade-2025-01 | CONTROL, listed | 621 | 446.7 LTM Nov-24, filed | 1.4 | 1 | work-order control transaction |
| udemy-2025-12 | CONTROL, listed | 1,025 (41% of $2.5bn) | 795.8 LTM Sep-25, filed, gross | 1.3 | **0** | all-stock; value is arithmetic on two stated figures, needs a ruling |

**Four rows are held out of the medians and need your word**: Moss, Restaurant365 and AuditBoard
because valuation and revenue are both stated as floors (a floor over a floor has no direction, so
the ratio is not a bound); Udemy because no standalone price exists in the release, only an exchange
ratio, a combined implied equity value and an ownership split. Release any of them the way Vegrow was
released, with a note, or leave them as marks.

**Four LTM denominators are arithmetic on filed figures** (Zuora, Sapiens, Accolade, Udemy: last full
year plus year-to-date less prior year-to-date), with all three components and their SEC URLs in the
row. That is the same construction the file already uses for LTM; flag it if you want them shown as
FY figures instead.

**Rejected, by lane and by name.** Reason codes: NR = no disclosed revenue; NV = no disclosed
valuation; NS = no source reachable; P23 = last priced round before 2023; CT = control deal, terms
undisclosed; NC = not a comparable; FW = forward figure only.

- *agentcard (33 examined, 3 kept)*: Rain NR (only "$3bn annualized transactions"; CEO declined revenue
  at Series A); Highnote NR; Lithic P23; Unit P23; Synctera NV/NR; Extend NV/NR; Column NS; Lead Bank NR;
  Zeta NC (revenue sentence reads India-only, entity risk); Skyfire NV; Payman NS; Nekuda NV; Natural
  NV/NR; Bridge (Stripe) CT/NR; BVNK/Mastercard CT/NR (Dec-24 figure 15 months stale); Conduit NV;
  Zero Hash NR; KAST FW (forward run-rate target only); Baanx NV; Gnosis Pay NS; Mesh NR; Jeeves P23;
  Payhawk no closed round; Pliant NV/NR; Karat NV/NR; Airbase CT (revenue only as ~1% of acquirer);
  Clara NV/NR; Aspire NV; Reap CT/NR; Swan NV/NR.
- *paymentkit (30 examined, 3 kept)*: Chargebee P23; Recurly NS; Maxio NS; Orb NV/NR (Adyen deal, no
  terms); Metronome NV/NR (Stripe deal, "terms not released"); Lago NV; Paddle P23 (2025 was debt);
  Lemon Squeezy CT; Sequence NS; Alguna NS; Primer P23; Gr4vy NV/NR; Spreedly P23; Corefy NS; IXOPAY
  NS; Paydock NS; Butter NV/NR; FlexFactor NS; Finix NV/NR ("would not disclose valuation"); Payrix P23;
  Tilled NV; Preczn NS; Yuno NV/NR; Payrails NV/NR; CellPoint NS; Nuvei NC (listed take-private, out of
  scale, not read); Rainforest and Payabli are fixtures.
- *finn (30 examined, 3 kept)*: Kavak NR ($2.2bn Mar-25, no revenue anywhere read); Carvolution debt
  only; Carsome NV (FY22 revenue 15 months stale); CARS24 P23; Carro no round; FlexCar NV/NR;
  Spotawheel NV/NR (equity plus debt, no valuation); Dance NV; Whizz NV; Upway NV/NR; Splend NV; Turo
  P23 and peer-to-peer; Kyte P23; Virtuo P23; Grover P23 (2023+ was debt); Bike Club P23; elmo NV; Feather
  P23; Zoomo NV/NR; Karvi, InstaCarro NS; Onto, Autonomy, ViveLaCar insolvent; Cluno, Bipi P23 CT;
  Swapfiets, Lynk & Co, Kinto, Drivalia captive, no round; Getaround, Zoomcar, Cazoo listed.
- *tash (31 examined, 0 kept)*: CollX NV/NR; Goldin (eBay) CT; Collectors/PSA CT (SGC, Beckett terms
  undisclosed); Yieldstreet NV/NR; Fanatics NC (conglomerate, no segment figures); Alt P23; Rally P23;
  Masterworks P23; Republic P23; Public.com NS (a 2023+ round may exist, no page reached); Arrived P23;
  Vinovest P23; Catawiki P23; Arena Club NS; Courtyard NS; Splint NS; Chrono24 P23; Otis, TCGplayer
  P23 CT; Collectable, Card Ladder CT; Dibbs, Timeless defunct; Konvi, Vint, Rares, Loupe, Drip,
  Collectr, Ludex, Mantel NV/NR; Fundrise no round; Whatnot, MoonPay held.
- *levelten (22 examined, 0 kept)*: Crux NV (volume only); Watershed NR ($1.8bn, no revenue); Sylvera
  NV/NR; Pexapark NV/NR; Persefoni NV/NR; Arcadia NV/NR (2024) and P23 valuation; AirCarbon P23;
  Reunion no round; Enmacc NV/NR; Carbonplace pre-revenue; Banyan NV/NR; Isometric NV/NR; Rubicon
  Carbon P23; Patch P23; Pachama P23; Evergrow, Basis Climate NV/NR; Zeigo P23 CT; Piclo, Electron,
  Renewabl, Station A, Cloverly, Senken, Toucan, Flowcarbon, Ndustrial P23 or NV/NR.
- *bizmark (30 examined, 1 kept)*: Zip NR (CEO declined revenue; $107bn spend processed is volume);
  Altana NR; o9 P23 (growth rates only); project44 P23; Logility CT with no stated total value (per-share
  only; equity value would be arithmetic on the share count); Blue Yonder/One Network NS; FourKites
  P23; Pando NV; Everstream NV; Interos P23; Resilinc CT; Ivalua, Zycus, GEP no round; Fairmarkit,
  Keelvar, Arkestro, Vendr, Tropic, Craft, Anvyl, Nextmv, Lily AI P23; Levelpath, Omnea, Pactum, Tacto,
  Syrup NV/NR; Spendflo, Inventoro, Verusen, Globality, Rebound NS; Peak.ai CT; Tradeshift NS/distressed.
- *manifold-robotics (34 examined, 1 kept)*: Magazino CT; Geek+ listed (HK IPO Jul-25); Hai Robotics
  P23; Locus P23; Exotec P23; GreyOrange P23/NV; Dexterity NR ($1.65bn); Dexory NV/NR; Pickle, Ambi,
  Nomagic, Brightpick, Formic, Cobot, Gather AI, Verity, Mytra, Vecna, Fox, Third Wave, Mujin, Standard
  Bots, Robust.AI NV/NR; Rapid Robotics P23; Bear Robotics NV and wrong segment; Plus One NV; Covariant
  NV/NR; Agility NR; Apptronik NV/NR; Nimble NR; Attabotics insolvent; Clearpath/OTTO CT; 6 River CT;
  Symbotic, Zebra, AutoStore, Ocado listed.
- *marble (27 examined, 2 kept)*: Restaurant365 May-24 NV/NR ("up-round" only); Owner May-25 NR;
  MarginEdge NV/NR; Nory NV ("tripled revenues", no figure); Petpooja near miss (valuation is
  Entrackr's estimate from RoC filings and FY24 revenue is 18 months stale; URLs in the agent note);
  SevenRooms CT/NR ($1.2bn, DoorDash); Tock CT/NR ($400m, Amex); Choco P23; Deliverect P23; Foodics
  NV/NR; SpotOn P23; GrubMarket NC/NV; Crunchtime, Fourth PE; 7shifts P23; Slice, Popmenu, Lunchbox,
  Sunday, Flipdish P23; Apicbase, Meez, Galley, Craftable, Rekki, Notch, Qu, Grubtech, Urbanpiper,
  Xenia, Opsi, Storekit, Incentivio, Grubbrr, Yumpingo, Tablecheck, iiko, Posist, Cuboh, Zenchef NV/NR;
  Bbot, Preoday, Nextbite defunct or P23; Otter NS; Lighthouse NS (hotel, $370m Series C Nov-24, not
  reached).
- *payna (44 examined, 2 kept)*: Norm Ai NR ($1.2bn Jul-26, clean valuation, no revenue); Persona NR
  ($2bn, "doubling revenue" only); Filevine NV; Drata P23; Hyperproof NV/NR; Sprinto NV/NR; Sardine
  NV; AgentSync P23; OpenGov CT/NR ($1.8bn reported, Cox); PermitFlow NV/NR; Medallion NS; Fenergo no
  round; Quantexa NS; Legora kept (also serves priori-legal); Secureframe, Thoropass, Scrut NV/NR;
  Regology, Compliance.ai, Ascent, Saifr, Harbor, Symplr, Sertifi, Greenlight Guru, Aumni, Cardinal,
  Accord, Beyond Compliance, Lawtrades, Lexcheck, 4Comply, Warp no round or CT; CertifyOS, Verifiable
  NV/NR; Middesk P23; ComplyAdvantage, Hummingbird, Unit21, Alloy, Socure, Trulioo P23; Cable,
  Flagright, Greenlite, Parcha, Zango NV/NR; Clariti, GovPilot, Pulley, SmartGov NV/NR; Tyler listed.
- *osseus (34 examined, 2 kept)*: Applied Intuition Mar-24 NR; Shield AI FW (revenue is a 2026
  projection and Fortune's arithmetic; defence buyer); Auterion NR (Sep-25) and no closed 2026 round;
  Divergent NR ("fivefold"); Hadrian NR at every priced round; Skild NR; Genesis NR; Physical
  Intelligence, Figure, 1X, Sanctuary NR; Foxglove NV/NR; Viam NV/NR; Rerun NV/NR; Roboflow NV/NR;
  Encord NV; Voxel51 NV/NR; Memfault NV/NR; Bright Machines NV/NR; Mujin NV/NR; Gecko NR; Machina NS;
  rFpro P23 CT; Arduino, Edge Impulse CT; Formant, InOrbit, Roboto, Freedom, Duality, Cognata, Parallel
  Domain, Realtime, Robust, Hillbot, Particle, Golioth, Balena NS/NR.
- *wispr-flow (42 examined, 4 kept)*: Photoroom rejected on re-read: the "$50m ARR" was "on track for",
  a target, not an achieved figure; Synthesia dropped: enterprise buyer and its $100m ARR post-dates
  the Jan-25 round by three months; Granola NR (both rounds); Motion NC (segment ARR only); Read AI
  NV; Cluely NS (CEO later admitted the revenue claim was false); Speak NR; Grammarly no valued equity
  round since 2021; Loom CT/NR; Browser Company CT/NR; Captions NV (non-dilutive; app-store revenue
  is not company revenue); Runway NR; Linear NR; Raycast NV ("we don't share much about revenue");
  Manus NR/CT unwound; HeyGen NS; Bolt.new NS; Otter, Fireflies, Descript, Fathom P23; Superhuman,
  Rewind CT; Krisp, Speechify, tl;dv, Aqua, Willow, Monologue, Typeless, Cal AI, Luzia, Tome,
  Consensus, Elicit, Krea, Ideogram, Pika, Sesame, Hume, Opus Clip, Fyxer NS/NR.
- *clera, standout, tsenta, nursa, priori-legal (77 lane-examinations, 4 kept)*: Paraform NV (>$100m
  annualized revenue, no valuation); Juicebox, Alpharun, Apriora, Metaview NS; Moonhub CT (Salesforce);
  Dover, Eightfold, Gem, Paradox, Phenom, HireVue, Beamery P23; SmartRecruiters CT (SAP); Greenhouse
  P23 CT; Cluely NS; Fika Jobs NV; Handshake P23; Toloka NS; Braintrust, Contra, A.Team, Malt, Andela,
  Catalant P23; Instawork NV/NR; Traba P23/NS; Jobright NV/NR; Final Round AI NV; Simplify, LazyApply,
  Sonara, Huntr, Teal, Kickresume, Careerflow NS; Otta CT; Welcome to the Jungle NS; Hired no round;
  CakeResume NV; ShiftKey NR (>$2bn, no revenue); ShiftMed NV/NR ("declined to disclose valuation");
  Clipboard Health P23; Nomad, IntelyCare, connectRN, CareRev, Trusted P23; Vivian no round; Wonolo,
  Zenjob P23; Veryable, Coople NS; Indeed Flex captive; Lawhive NV/NR; Eudia NV (>$125m ARR, no
  valuation anywhere); Lawyers On Demand CT; Axiom, Peerpoint no round; Lawtrades, LawFlex, Paragon,
  Hire an Esquire, Legal.io, Marble Law, Flex Legal NS; EvenUp NS; Filevine NV; Spellbook, Supio,
  Luminance, Robin AI, Brightflag NV.
- *ultrasonium (17 examined, 0 kept)*: Hadrian Series B Dec-23 rejected: valuation is a journalist's
  "roughly $500m" eight months later and the two revenue statements ($3m FY2023 vs "well above $20m")
  contradict each other; Hadrian later rounds NR; Divergent NR; Machina NV/NR; VulcanForms NV/NR;
  Freeform NV/NR; Fabric8Labs NV/NR; Firestorm NV (contract ceiling is not revenue); Seurat NV/NR
  (projection only); Fictiv CT/NR; Formlabs, Carbon P23; Relativity NR; Meltio NS; Velo3D, Desktop
  Metal, Xometry, Protolabs, Markforged, Nano Dimension listed; the rest not reached.
- *apollo-atomics (16 examined, 0 kept)*: X-energy NV/NR; Valar pre-revenue ($6bn); Radiant
  pre-revenue; Aalo pre-revenue; TerraPower pre-revenue; Last Energy pre-revenue; Zeno NV/NR and not a
  reactor company; newcleo near miss (de-SPAC at $2.4bn pre-money May-26 against FY2024 "revenue,
  other income and financial income" of ~$80m from acquired subsidiaries, 17 months apart; URLs in the
  agent note); Kairos, Helion, CFS pre-revenue; Oklo, NuScale, Nano Nuclear, Terrestrial, Deep Fission
  listed; USNC bankrupt.
- *the four control transactions in the order*: Sapiens, Accolade, Udemy written (Udemy held for a
  ruling); **LTG not written**: the General Atlantic offer value is not on ltgplc.com's results page
  and I could not reach an RNS or the acquirer's page without search. Its denominator is ready when
  the offer page is found: FY2023 revenue GBP 562.3m (annual report 2023,
  https://ltgplc.com/wp-content/uploads/2024/04/LTG_Annual_Report_2023_Digital_pages.pdf) plus H1
  2024 GBP 250.3m less H1 2023 GBP 284.6m (https://ltgplc.com/news/half-year-results-2024/) = GBP 528.0m
  LTM to 30-Jun-2024, the last closed period before the offer.

### Tags

24 tag rows in `data/raw/2026-09-05_private-companies-tags-claude.csv`, same vocabulary as the
working file, archetype on how the company earns money. Judgement calls worth a second pair of eyes:
Moove tagged Owned-Inventory Retail with a Lending & Credit secondary and CHANNEL motion (owned fleet,
weekly payments, sold through Uber); Vention PRODUCT_SALES rather than SEATS (mostly hardware); Owner
Vertical Software with a Marketing secondary (front of house); Sapiens and Accolade PLATFORM; Udemy
Online Learning with TAKE_RATE. The dry run shows every row landing in the lane it was sourced for.

## Part 2. Investor houses

**100 funds examined, 19 rows written, 17 CALLABLE.** Consumer cluster 13 callable (NFX, Lerer Hippeau,
BoxGroup, Betaworks, Homebrew, Haystack, Eniac, Maveron, Pear, NextView, Baukunst, Y Combinator,
Techstars), learning cluster 4 callable (Reach Capital, Emerge, Educapital, Magnify; YC carries both),
and 2 EVIDENCE (Tiny VC, which says it does not lead; Shine Capital, which led Gizmo's Series A and joined
MOTHER.tech's seed but whose site refused every connection, so stage, cheque and thesis are unverified;
promote it the day the site is read). Every deal sentence is quoted in `deal_note` with its URL; every
cheque range is the fund's own page; three rows carry an empty stage band because the site names none
(Haystack, YC, Techstars). No contact details anywhere (asserted in the build script).

**Why 19 and not 30.** Fetch-only sourcing after the cap, and the honest shape of the market: most
education specialists (Brighteye, Rethink, JFF, LearnLaunch, Owl, New Markets) spent the last twelve
months writing cheques into school- and employer-facing products, not consumer apps; a dozen consumer
seed funds have sites that publish no dated deals (Slow, Chapter One, Village Global, Shrug, Hustle,
Weekend, Kima, Founders Inc, Afore, Floodgate); and eleven sites were unreachable (Shine, Sugar,
Corazon, Behind Genius, Mucker, Lightshed, Moth, Stellation, Interlace, Kaplan, Marathon, Firework,
ETS). The full verdict list per fund is in the two agent reports, reproduced in the project handover.

**What the two checks say, run on the loaded scratch copy.**

`tools/investor_check.py`: 506 houses, 142 CALLABLE, 131 render, 11 refused. Nine of the eleven are
mine, and all nine are refused for "no first-cheque range and no round-size range" or "no stage
band". `tools/investor_coverage.py`: 142 of 142 can render; 813 callable cards, 8.0 a founder, no
founder under three. **The two tools disagree, and the engine sides with the second.** Your ruling
of 2 September, that an unpublished cheque or geography no longer blocks an active house, is built
into `selector/investors.py` (`renderable()` requires only a dated, sourced deal; the card says
"First cheque not published"), but `investor_check.py` still demands both cheque ends or a round
size. It refuses BoxGroup ("up to $1M"), Betaworks ("up to $250k") and Educapital ("up to EUR10m")
for publishing a ceiling only, which the engine renders as "First cheque up to $1m". That check is
stale against the ruling; I have not changed it, because a check is a rule and rules are yours.

**Is any founder better off?** Not by the coverage tool's number, which cannot move: the list is
capped at eight cards and the test fixtures carry no raise amount and no country, so every fixture
was already at eight. Measured the way a founder would see it: callable houses reaching Consumer &
Prosumer Software go from 14 to 47 (16 from the pull) and Online Learning from 3 to 12, and a seed founder raising $2m
in the US now gets Homebrew, Betaworks and BoxGroup on the first page (goldfish, acti, welltory,
planeat), a UK founder gets Betaworks, BoxGroup, Educapital and Emerge (wondering, befreed). The
generalists still rank first, and that is a ranking rule worth your eye: inside a tier the list is
ordered by deal count in the founder's sector, which the houses promoted from our own rounds carry
as counts and a pulled specialist carries as one. A seed specialist with one named consumer deal
therefore sits below Accel with three. Whether that is the order a founder wants is your call.

## What I did not do, and what a search-enabled session should do next

1. **Re-check the "no source" rejections** made after the cap, in this order of value: HeyGen (Jun-24
   $500m; ARR was reported in press), Bolt.new/StackBlitz (Jan-25; ARR reported), Zip and Altana ARR at
   their 2024 rounds (The Information), Highnote (Forbes Jan-25), Public.com 2023+ financing, Petpooja
   FY25 revenue, Norm Ai and Persona ARR near their rounds, Lighthouse Nov-24, LTG's offer page,
   Logility's stated deal value, Blue Yonder/One Network.
2. **Net-basis rounds for the talent-marketplace archetype** (clera, standout, nursa, tsenta) and for
   billing infrastructure (paymentkit). Gross rows are in; they do not price a net founder.
3. **levelten and tash** have no compliant round at all; the honest answer may be a listed lane (already
   in your ticker request) and control marks.
4. **Investors**: the eleven unreachable fund sites, and the learning specialists whose portfolio
   pages are undated (Bling, Avalanche, Transcend, Learn Capital).

## Commit 1, the raw files (run in your own terminal; rm -f only if the lock is still there)

```
cd ~/fairway-valuation && rm -f .git/index.lock && git add -A && git commit -m "Claude's 5-Sep pull, raw files: 27 private rounds, 24 tag rows, 19 investor houses

Part 1 of the 4-Sep work order. 24 rounds for the eighteen thin private lanes
plus the three control transactions the order names (Sapiens, Accolade, Udemy),
every figure read on its URL on 5 September and quoted in the row. About 460
candidate-lane examinations, every rejection named in the handover. FX at ECB
reference rates on the pricing date. Four rows held out of the medians for a
ruling: Moss, Restaurant365, AuditBoard (floor over floor) and Udemy (all-stock,
no standalone price stated).

Part 2: 19 houses for Consumer & Prosumer Software (14 to 47 callable, 16 from the pull) and Online
Learning (3 to 12), 17 callable with a dated first-cheque deal read on its URL,
published cheque ranges only, no contact details.

Nothing loaded yet (D14: raw first). tools/load_claude_pull_5sep.py is the second
step and refuses to run until these files are in a commit. Dry run on a scratch
copy: gate 81 to 89 of 102, all fourteen checks pass.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_015S1xtdo14ySg8B73qvYBsv" && git push
```

## Commit 2, the load (after commit 1 is in)

```
cd ~/fairway-valuation && python3 tools/load_claude_pull_5sep.py && sh tools/check_all.sh && git add -A && git commit -m "Load the 5-Sep pull: 27 rounds, 24 tags, investor table rebuilt, golden rebaselined 81 to 89

agentcard, bizmark, finn, marble, osseus, payna, priori-legal and wispr-flow
flip to PASS; nothing regresses. check_raw_coverage now accounts for every
supplied row. Investor table 445 to 506 houses through the new source hook in
build_investors_table.py.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_015S1xtdo14ySg8B73qvYBsv" && git push
```
