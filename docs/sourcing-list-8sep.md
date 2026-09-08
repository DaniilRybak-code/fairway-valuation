# Sourcing list, 8 September 2026: names to look for in the bulk pass

**What this is.** The names the evaluator's review and Daniil's answers of 8 September put on the
list, for the one bulk pass after the 18 September march (rule A12 part 3: nothing here is chased
before then). Daniil will add his own comparables at a later stage; this file is where they go too.
Every name below was checked against the pool on 8 September and is absent unless marked. **No
figure is written here.** A name enters the pool only with a priced round or a listing, read from
its source and quoted in the row (rules C and D); a name without one is recorded as looked for and
not found.

**One rule that runs inside the pass, new on 8 September (A16).** Where a fixture already holds a
near-perfect comparable, look up that company's own neighbours online (its competitors' pages, its
press, who its investors also backed) and bring the priced ones in. Daniil's example: Mambu led to
Thought Machine. The fixtures to start from are the ones whose set holds a DIRECT name; check 8
prints the tier of every lane.

| for | names to look for | what it fixes | notes |
|---|---|---|---|
| kita, levocred | **Tuum**, **Thought Machine** (core banking, private); their neighbours by A16: 10x Banking, Provenir, Taktile, Zest AI | the software-for-lenders private lane holds Mambu and Sapiens and little else | Daniil: "closer to Mambu, Tuum, Thought Machine" |
| ekho-labs, bizmark, derya | **Eurowag** (W.A.G. payment solutions, London-listed: fleet payments and telematics), **Descartes Systems** (listed logistics software), **project44**, **FourKites**, **Flexport** (private) | the new Supply Chain & Logistics Software archetype holds three listed rows and one priced private round; ekho-labs fails the gate on the private lane | Daniil: Eurowag "would also make sense"; Kinaxis, Manhattan, Tecsys "less perfect" (planning and stock, not vehicles) |
| manifold-robotics, lambda-robotics | **Symbotic** (listed), **AutoStore** (listed, Oslo), **Locus Robotics**, **Exotec**, **Agility Robotics**, **GreyOrange** (private); Geek+ (check whether listed) | no listed warehouse-automation or robotics maker in the pool; manifold's listed lane is 3PLs and REITs | Daniil asked for "something close to Boston Dynamics": it has been a Hyundai subsidiary since 2021 with no standalone price, so it cannot be a comparable; the names here are the investable neighbours |
| supercritical, levelten | **STX Group** (Amsterdam, environmental-commodities trader); **Xpansiv**'s own revenue at its round; **Climate Impact X**, **AirCarbon Exchange**, **Puro.earth** (Nasdaq-owned), **Patch**, **Watershed** | both fail the gate on the private lane: Xpansiv prices on tonnes only | STX, checked on Daniil's question: right sector (carbon credits, renewable certificates, biofuel tickets), but it trades as principal with a credit facility rather than running a marketplace, and no priced equity round surfaced; include only if a priced round is found, and label the business-model difference. Sources: [STX Group, about](https://stxgroup.com/about-us/), [Silicon Canals on its credit facility](https://siliconcanals.com/amsterdams-stx-group-raises-150m/) |
| princeps, florin | listed specialty and commercial P&C carriers: **Kinsale Capital**, **Skyward Specialty**, **Bowhead Specialty**, **Hamilton Insurance**, **Beazley**, **Hiscox**, **Lancashire**; insurtech carriers **Lemonade**, **Root**, **Hippo** | the pool's listed insurers are a Chinese consumer insurer, a pet insurer, a claims adjuster and health plans | Daniil: princeps "should be priced as insurers, so most likely sourcing issue" |
| alloovium, subvysion, foreman | construction-tech private rounds: **Buildots**, **Doxel**, **Trunk Tools**, **Built Robotics**, **Dusty Robotics**, **Versatile**; Fieldwire (acquired by Hilti; a control transaction if the price is public) | no construction private round in the pool; all three get legal and hospitality software on the Vertical Software label | Daniil: subvysion "should be close to alloovium, also serving contractors"; the listed lanes now converge (Procore, Trimble, Bentley, Nemetschek) |
| emergent, orchids | a listed no-code or app-builder name; private rounds for **Bubble**, **OutSystems** | the listed pool has no AI app builder; Cadence and Synopsys stand in | Lovable, Replit and Cursor already carry the private lane |
| blindspot | out-of-home media, listed: **Clear Channel Outdoor**, **Lamar**, **Outfront**, **JCDecaux**, **Stroer**; private: **Broadsign** | the whole listed lane is the label fallback (kind 1 since 5 Sep) | |
| markov, praxis-robotics, qokedas | listed data-services and annotation vendors to verify: **Appen** (ASX), **Innodata** (Nasdaq), **TELUS Digital** | the listed lane rests on "ai" and "data" (kind 3) | **Touches Daniil's reading of 8 Sep that no listed names exist in this sector:** these three are listed and sell training data and annotation; put to him before they are pulled |
| fundraisly | **Morningstar** is in the pool and owns PitchBook, which Fundraisly names as a competitor: a pin by name if Daniil wants it; rounds for **Dealroom**, **Boardy**, **OpenVC**, **Metal** if any is priced | the listed lane is ZoomInfo, Red Violet, Similarweb | Red Violet is a stray (people-search data) |
| orca-aerospace, constellation-space, zymbly, hop-aero, ornadyne, daivin | an Aerospace & Defence end market in the vocabulary (TAKEOVER 11) and the first names under it | five struck, two out of market | taxonomy build |
| lyka | a Pet Care end market, so BARK, Chewy, Trupanion and lyka share one label instead of borrowing Retail & E-commerce | lyka now passes on BARK; a cleaner label would keep its food-brand private lane too | taxonomy build |
| tash | Whatnot's GMV reading (rule B8 wiring) or a second collectibles round with a revenue figure | on the No-comps list since 6 Sep | unchanged |
| unifold, and the rest of TAKEOVER 10 | the loose ends of the 5 Sep pull named in the status document | | unchanged |

**How to run the pass, in order.** (1) The A16 neighbour lookup over every fixture with a DIRECT
name, listing candidates with a source each. (2) The table above. (3) Daniil's own comparables.
(4) One load script with count in and count out, one golden rebaseline with the reason written,
one suite run. Nothing loads without a URL that shows the figure.
