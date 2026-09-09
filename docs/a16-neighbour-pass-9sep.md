# The comp-of-a-comp pass (rule A16), run 9 September 2026

**What this is.** Daniil's rule of 8 September: when a fixture already holds a near-perfect
comparable, look that company's own neighbours up online and bring the priced ones in. His example
was Mambu leading to Thought Machine. On 9 September he said "pass it now" rather than waiting for
the bulk pass after the 18 September march, so this is the pass. **It is a list of candidates with a
source each. No figure is written here and nothing is loaded.** A name enters the pool only with a
priced round or a listing read on its own source and quoted in the row (rules C and D); reading each
source for the figure is the next step, and it is the same step whether it runs now or in the bulk
pass.

**How it was run.** The starting set is every name the engine judged DIRECT (the closest tier) in any
fixture's listed core lane or private lane, read from the golden snapshots after the batch of 9
September: **91 names, 32 listed and 59 private, across 55 of the 142 fixtures.** They were split into
six slices of 15 or 16 names and each slice given to a search agent with the same brief: for each
near-perfect comparable, find its closest competitors and neighbours on its own pages, its press, and
lists of its alternatives; report each as listed (exchange and ticker) or private (the latest
announced round and its month), with one line on what it does, the fixtures it would serve, and a
source URL; do not invent a round, and say so when nothing surfaces.

**Counted in and out.** 240 candidate rows came back from the six agents. 39 were the same company
found from two or more starting names (PostHog from Amplitude, Adobe, Contentsquare and Similarweb;
Lemonade from FINEOS, Guidewire and ZhongAn; and so on) and were merged into one row that lists every
neighbour it came from. 0 were already in the engine's universe (checked by exact normalised name
against all six listed files and both private files; a substring check was tried first and rejected
because it matched Clari to Claritev and Runway to Rent the Runway). 1 was dropped by name: OFX
Group, which sits in `peers-fintech.csv` and was killed by Daniil on 31 August as a micro cap, so an
agent proposing it again changes nothing. **200 candidates out: 46 listed, 154 private, serving 55
fixtures.** Toloka, which one agent called not investable because Nebius owns a majority and another
reported with a May 2025 round, is kept and flagged in its row.

**Caveats, so nobody loads a row without reading it.**

- The agents' search budgets ran out before every name was exhausted, so a starting name with few
  rows below it may simply not have been searched to the end; absence here is not evidence.
- Round dates on some private rows come from CB Insights or Wikipedia rather than the company's own
  announcement; the source column says which. The load reads the announcement.
- PhonePe filed to list in India; check whether it has listed before treating it as private.
- Loggi's latest financing (September 2025) is debt; its last equity round is earlier and is the one
  to price on.
- Transcarent merged with Accolade in April 2025, so its May 2024 round is a pre-merger price and
  Accolade itself is already a control transaction in the pool.
- Attentive's round date is reported as March 2021 by one source and differently by another; read
  the announcement.
- GB Group's neighbours (Experian, RELX, Jumio) are marked weak fit for atlas-new: identity data is
  not what atlas-new does, and the neighbours are listed only because GB Group was DIRECT for it.
- Boston Dynamics (Daniil's example for manifold) has been a Hyundai subsidiary since 2021 with no
  standalone price, so it cannot be a comparable; the warehouse-automation names under GXO are the
  investable neighbours.
- The agents were told the fixtures each starting name serves, so the "fixture(s) it would serve"
  column is their reading of the fit, not the engine's; the engine decides on the tags when a row
  is loaded and tagged.

**Where hop-aero's defence names are.** Not here: hop-aero holds no DIRECT name (it was passing on
carriers, now struck), so the rule does not reach it. The defence contractors Daniil asked for are on
the sourcing list in the status document.

**Next step.** The load: for each row, open the source, read the round figure or confirm the listing,
write the row with the quote, tag it, then one golden rebaseline with the reason and one suite run.
Rows without a figure on a reachable page are recorded as looked for and not found.

## The 200 candidates, by the fixture they would serve

| candidate | listed, or private with its latest announced round | what it does | neighbour of | fixture(s) it would serve | source |
|---|---|---|---|---|---|
| AfterShip | private (Series B, Apr 2021) | shipment tracking and returns software | Loop Returns | 99minutos | [source](https://techcrunch.com/2021/04/22/e-commerce-tracking-platform-aftership-raises-66m-led-by-tiger-global/) |
| Loggi | private (debt financing, Sep 2025; last equity round earlier) | Brazil last-mile parcel delivery platform | Xpressbees | 99minutos | [source](https://www.cbinsights.com/company/loggi/financials) |
| Optoro | private (strategic investment, Dec 2021) | returns processing and reverse logistics | Loop Returns | 99minutos | [source](https://www.optoro.com/returns-news/returns-technology-company-optoro-receives-strategic-investment-from-zebra-technologies/) |
| Shadowfax | listed (NSE:SHADOWFAX) | tech-led express parcel and hyperlocal 3PL in India | Xpressbees | 99minutos | [source](https://stockanalysis.com/quote/nse/SHADOWFAX/) |
| Circle Internet Group | listed (NYSE:CRCL) | Stablecoin issuer and payments infrastructure | Coinbase Global, Inc.; BVNK | unifold, agentcard | [source](https://www.coindesk.com/markets/2026/01/29/crypto-linked-stocks-continue-2026-plunge-but-bitcoin-miners-with-ai-pivots-outperform) ; [source](https://stablerail.com/blog/bvnk-competitors-stablecoin-payments-accounts-fiat-infrastructure) |
| Expensify | listed (NASDAQ: EXFY) | Expense management and cards | Moss | agentcard | [source](https://www.g2.com/products/moss-spend-smarter/competitors/alternatives) |
| Green Dot | listed (NYSE:GDOT) | fintech and bank holding company issuing prepaid and debit cards | Marqeta, Inc. | agentcard | [source](https://ir.greendot.com/) |
| Highnote | private (Series B, Jan 2025) | card issuing and embedded finance platform | Marqeta, Inc.; Slash | agentcard, unifold | [source](https://www.businesswire.com/news/home/20250121011744/en/) ; [source](https://www.businesswire.com/news/home/20250121011744/en/Highnote-Secures-90-Million-Series-B-Announces-Expansion-into-U.S.-Merchant-Acquiring) |
| Lithic | private (Series C, Jul 2021) | API card issuing infrastructure; names Marqeta as rival | Marqeta, Inc. | agentcard | [source](https://research.contrary.com/company/lithic) |
| Navan | listed (NASDAQ: NAVN) | Travel, expense, cards | Moss | agentcard | [source](https://www.g2.com/products/moss-spend-smarter/competitors/alternatives) |
| Payhawk | private (Series B extension, Feb 2022) | Corporate cards, spend management | Moss | agentcard | [source](https://www.cbinsights.com/research/payhawk-competitors-spendesk-pleo-moss-soldo/) |
| Rain | private (Series C, Jan 2026) | stablecoin-backed card issuing platform | BVNK | agentcard | [source](https://www.rain.xyz/resources/rain-raises-250m-series-c-to-scale-stablecoin-powered-payments-infrastructure-for-global-enterprises) |
| Relay Financial | private (growth financing, May 2026) | small-business banking and cards | Slash | agentcard | [source](https://relayfi.com/blog/relay-50m-financing-announcement/) |
| Soldo | private (Series C, Jul 2021) | Prepaid company cards | Moss | agentcard | [source](https://www.cbinsights.com/company/soldo/financials) |
| Zero Hash | private (Series D, Sep 2025) | embedded stablecoin settlement infrastructure | BVNK | agentcard, unifold | [source](https://blog.zerohash.com/zero-hash-raises-100-million-series-d-funding-5802c0555142) |
| Experian | listed (LSE:EXPN) | credit bureau and decisioning software | Fair Isaac; GB Group plc | kita, atlas-new (weak fit) | [source](https://koalagains.com/stocks/NYSE/FICO/competition) ; [source](https://koalagains.com/stocks/LSE/GBG/competition) |
| Jumio | private (private equity round, Mar 2021) | Identity verification | GB Group plc | atlas-new (weak fit) | [source](https://www.cbinsights.com/company/jumio/financials) |
| RELX (LexisNexis Risk) | listed (LSE: REL) | Risk and identity data | GB Group plc | atlas-new (weak fit) | [source](https://koalagains.com/stocks/LSE/GBG/competition) |
| Descartes Systems | listed (TSX:DSG; NASDAQ:DSGX) | logistics and supply chain software | Kinaxis; E2open | bizmark | [source](https://www.fool.ca/2022/05/22/kinaxis-vs-descartes-which-is-the-better-tech-stock-to-buy/) ; [source](https://finance.yahoo.com/quote/DSGX/profile/) |
| o9 Solutions | private (growth round, Jul 2023) | AI supply chain planning platform | Kinaxis; E2open | bizmark | [source](https://dallasinnovates.com/dallas-o9-solutions-raises-116m-in-latest-funding-round-for-a-3-7b-valuation/) ; [source](https://www.dmagazine.com/business-economy/2023/07/o9-solutions-ceo-talks-latest-116-million-capital-raise-and-3-7-billion-valuation/) |
| project44 | private (growth round, Nov 2022) | Multimodal shipment visibility platform | E2open | bizmark | [source](https://www.builtinchicago.org/articles/project44-raises-80m-2b-valuation) |
| RELEX Solutions | private (growth round, Feb 2022) | retail supply chain planning | Kinaxis | bizmark | [source](https://www.relexsolutions.com/news/relex-solutions-raises-500m-in-blackstone-led-funding-round-at-5bn-valuation/) |
| Classplus | private (Series D, Mar 2022) | Teaching platform for educators | LEAD School | bloomy | [source](https://www.cbinsights.com/company/classplus/financials) |
| Pearson | listed (NYSE:PSO; LSE:PSON) | courseware, assessment, digital learning | Duolingo | bloomy, honen | [source](https://koalagains.com/stocks/NASDAQ/DUOL/competition) |
| Physicswallah | listed (NSE: PWL) | Indian K-12 and test-prep learning | LEAD School | bloomy | [source](https://esi.in/blog/top-10-edtech-companies-india-2025) |
| Preply | private (Series D, Jan 2026) | online tutoring marketplace with AI | Duolingo | bloomy | [source](https://www.prnewswire.com/news-releases/preply-raises-150-million-to-shape-the-future-of-education-through-human-led-ai-enhanced-learning-302665890.html) |
| Speak | private (Series C, Dec 2024) | AI language tutor app | Duolingo | honen, bloomy | [source](https://www.speak.com/blog/series-c) |
| Stride | listed (NYSE:LRN) | online K-12 schools and courses | Duolingo | bloomy | [source](https://koalagains.com/stocks/NASDAQ/DUOL/competition) |
| Teachmint | private (Series B, Oct 2021) | School operating system | LEAD School | bloomy | [source](https://www.cbinsights.com/company/teachmint/financials) |
| Canary Technologies | private (Series D, Jun 2025) | AI guest management for hotels | Mews | bluerails | [source](https://www.canarytechnologies.com/press/canary-raises-series-d) |
| Cloudbeds | private (Series D, Nov 2021) | Hotel PMS, channel manager, booking engine | Guesty; Mews | bluerails | [source](https://www.prnewswire.com/news-releases/cloudbeds-raises-150m-in-funding-to-support-rapid-company-growth-301414521.html) ; [source](https://www.cloudbeds.com/articles/cloudbeds-raises-150m-in-funding-to-support-rapid-company-growth/) |
| Hostaway | private (growth round, Dec 2024) | Short-term rental management and channel software | Guesty | bluerails | [source](https://www.hostaway.com/blog/hostaway-raises-365-million/) |
| SiteMinder | listed (ASX:SDR) | Hotel distribution and channel management | Guesty; Mews | bluerails | [source](https://www.marketindex.com.au/asx/sdr) ; [source](https://stockanalysis.com/quote/asx/SDR/company/) |
| ActiveCampaign | private (Series C, Apr 2021) | Email marketing automation and CRM | Mailchimp; HubSpot, Inc. | brandjet, clarify | [source](https://en.wikipedia.org/wiki/ActiveCampaign) ; [source](https://www.cbinsights.com/company/activecampaign/financials) |
| Attentive | private (Series E, Mar 2021) | SMS and email marketing for brands | Klaviyo; Klaviyo, Inc. | brandjet | [source](https://en.wikipedia.org/wiki/Attentive_(company)) ; [source](https://www.builtinnyc.com/articles/nyc-top-funding-rounds-march-2021) |
| Attio | private (Series B, Aug 2025) | AI-native CRM | Salesforce | clarify, brandjet | [source](https://www.finsmes.com/2025/08/attio-raises-52m-in-series-b-funding.html) |
| Bloomreach | private (growth round, Feb 2022) | Ecommerce marketing automation and discovery | Klaviyo | brandjet | [source](https://en.wikipedia.org/wiki/Bloomreach) |
| Brevo | private (growth round, Dec 2025) | SMB email, SMS and CRM suite | Mailchimp; HubSpot, Inc. | brandjet, clarify | [source](https://en.wikipedia.org/wiki/Brevo) ; [source](https://www.cbinsights.com/company/sendinblue/financials) |
| Criteo | listed (NASDAQ: CRTO) | Commerce media platform | Zeta Global Holdings Corp. | brandjet | [source](https://adtechlist.io/alternative-to-zeta-global) |
| Insider | private (Series E, Oct 2024) | AI personalization across web, app and messaging | Braze, Inc. | brandjet | [source](https://www.businesswire.com/news/home/20241031435852/en/) |
| Iterable | private (Series E, Jun 2021) | cross-channel customer engagement platform | Braze, Inc. | brandjet | [source](https://iterable.com/blog/our-next-chapter-series-e-funding-announcement/) |
| MoEngage | private (Series F extension, Dec 2025) | AI customer engagement platform | Klaviyo; Braze, Inc. | brandjet | [source](https://techcrunch.com/tag/moengage/) ; [source](https://www.moengage.com/in-the-news/moengage-gets-additonal-180m-in-series-f-funding/) |
| Postscript | private (Series C, Jun 2022) | SMS marketing for Shopify merchants | Klaviyo, Inc. | brandjet | [source](https://sacra.com/c/postscript/) |
| StackAdapt | private (Series B extension, Feb 2025) | Programmatic advertising platform | Zeta Global Holdings Corp. | brandjet | [source](https://www.cbinsights.com/company/stackadapt/financials) |
| The Trade Desk | listed (NASDAQ: TTD) | Programmatic demand-side platform | Zeta Global Holdings Corp. | brandjet | [source](https://adtechlist.io/alternative-to-zeta-global) |
| ShipBob | private (Series E, Jun 2021) | ecommerce fulfilment 3PL network | Packable | byrd | [source](https://research.contrary.com/company/shipbob) |
| Stord | private (Series D, May 2022) | software plus port-to-porch 3PL fulfilment | Packable | byrd | [source](https://research.contrary.com/company/stord) |
| Beautiful.ai | private (Series B, May 2018) | AI-assisted presentation design | Gamma | chronicle | [source](https://www.beautiful.ai/blog/series-b-announcement) |
| Pitch | private (Series B, May 2021) | collaborative presentation software | Gamma | chronicle | [source](https://pitch.com/blog/pitch-series-b-funding) |
| Handshake | private (Series F, Jan 2022) | Careers network, AI expert data | Mercor | clera, standout, tsenta | [source](https://www.troveo.ai/resources/mercor-alternatives) |
| Paraform | private (Series B, Mar 2026) | agentic hiring marketplace, recruiters plus AI | Micro1 | clera, tsenta | [source](https://www.paraform.com/blog/series-b) |
| Prolific | private (funding round, Jul 2023) | vetted human participants for AI data | Micro1 | clera, tsenta | [source](https://techcrunch.com/2023/07/11/prolific-raises-32m-to-train-and-stress-test-ai-models-using-its-network-of-120k-people/) |
| Toloka | private (round led by Bezos Expeditions, May 2025; majority-owned by Nebius, check the round is priced before loading) | Managed expert data workforce | Mercor; Invisible Technologies | clera, standout, tsenta, qokedas | [source](https://www.cbinsights.com/company/toloka/financials) ; [source](https://nebius.com/newsroom/nebius-welcomes-bezos-expeditions-as-lead-investor-in-ai-data-business-toloka) |
| Clover Health | listed (NASDAQ:CLOV) | Medicare Advantage insurer with physician software | Devoted Health | denta | [source](https://stockanalysis.com/stocks/clov/company/) |
| Oscar Health | listed (NYSE:OSCR) | Tech-first health insurer | Devoted Health | denta | [source](https://stockanalysis.com/stocks/oscr/company/) |
| Zing Health | private (growth round, Sep 2024) | Medicare Advantage insurer for chronic special needs | Devoted Health | denta | [source](https://www.businesswire.com/news/home/20240924419214/en/) |
| LaunchDarkly | private (Series D, Aug 2021) | feature flags and experimentation | Amplitude | dif-sh, simulithic | [source](https://www.crunchbase.com/funding_round/launchdarkly-series-d--94090d05) |
| PostHog | private (Series E, Sep 2025) | open-source product and web analytics suite | Adobe Inc.; Contentsquare; Similarweb Ltd.; Amplitude | rybbit, simulithic, dif-sh | [source](https://www.thesaasnews.com/news/posthog-raises-75m-series-e-at-1-4b-valuation/) ; [source](https://www.cbinsights.com/company/posthog/financials) ; [source](https://posthog.com/blog/series-d) ; [source](https://posthog.com/blog/series-e) |
| Nium | private (Series E, Jun 2024) | Real-time cross-border payout infrastructure | Payoneer Global Inc. | dots | [source](https://en.wikipedia.org/wiki/Nium) |
| Thunes | private (Series D, Apr 2025) | Cross-border payment network for payouts | Payoneer Global Inc. | dots | [source](https://en.wikipedia.org/wiki/Thunes) |
| Bubble | private (Series A, Jul 2021) | no-code full-stack web app builder | Framer | emergent, orchids | [source](https://bubble.io/blog/bubble-series-a-100m/) |
| Cognition | private (Series E, Sep 2026) | Devin AI coding agent | Replit | emergent, orchids | [source](https://cognition.com/blog/series-e) |
| Render | private (Series C extension, Feb 2026) | developer cloud hosting and deployment; Replit peer per Sacra | Replit; Docker | emergent, orchids, herdr | [source](https://render.com/blog/series-c-extension) ; [source](https://techfundingnews.com/render-100m-ai-cloud-infrastructure/) |
| Rork | private (Seed, Apr 2026) | prompt-to-mobile-app builder | Lovable | emergent, orchids | [source](https://www.finsmes.com/2026/04/rork-raises-15m-in-seed-funding.html) |
| StackBlitz (Bolt.new) | private (Series B, Jan 2025) | prompt-to-app builder in browser | Lovable | emergent, orchids | [source](https://www.ctol.digital/news/bolt-new-series-b-funding-ai-driven-development/) |
| Transcarent | private (Series D, May 2024); merged with Accolade Apr 2025 | AI health navigation and virtual care for employers | Accolade | evergrove, insurf, scheduling-wizard | [source](https://www.businesswire.com/news/home/20240502320693/en) |
| Clari | private (Series F, Jan 2022) | revenue platform with call intelligence | Gong; Outreach | fathom | [source](https://www.clari.com/press/clari-announces-225-million-series-f/) |
| Cresta | private (Series D, Nov 2024) | generative AI for contact centers | Verint Systems | fathom | [source](https://www.finsmes.com/2024/11/cresta-raises-125m-in-series-d-funding.html) |
| Fireflies.ai | private (Series A, May 2021) | AI meeting transcription and notes | Gong | fathom | [source](https://fireflies.ai/blog/fireflies-ai-raises-14-million-series-a-to-automate-work-from-meetings/) |
| Granola | private (Series C, Mar 2026) | Bot-free AI meeting notepad | Salesloft | fathom | [source](https://www.granola.ai/blog/series-c) |
| Otter.ai | private (Series B, Feb 2021) | AI meeting notes and summaries | Gong; Salesloft | fathom | [source](https://otter.ai/blog/otter-raises-50-million) ; [source](https://techcrunch.com/tag/otter-ai/) |
| Parloa | private (Series D, Jan 2026) | AI agents for customer service | Verint Systems | fathom | [source](https://www.finsmes.com/2026/01/parloa-raises-350m-in-series-d-funding.html) |
| Read AI | private (Series B, Oct 2024) | AI meeting, email and chat summaries | Salesloft | fathom | [source](https://www.read.ai/press) |
| Uniphore | private (Series F, Oct 2025) | conversational AI for enterprises | Verint Systems | fathom | [source](https://www.finsmes.com/2025/10/uniphore-closes-260m-series-f-funding.html) |
| CarDekho | private (Series E, Oct 2021) | car marketplace, financing, insurance | Spinny | finn | [source](https://www.businesstoday.in/auto/story/cardekho-turns-unicorn-raises-250-million-in-pre-ipo-round-led-by-leapfrog-investments-309218-2021-10-13) |
| CarTrade Tech | listed (NSE:CARTRADE) | Indian vehicle marketplace | Spinny | finn | [source](https://www.cbinsights.com/company/spinny/alternatives-competitors) |
| Gozem | private (equity round, Feb 2025) | Vehicle financing for drivers, Francophone Africa | Moove | finn | [source](https://techcrunch.com/tag/gozem/) |
| Yassir | private (Series B, Nov 2022) | Ride-hailing super app, North Africa | Moove | finn | [source](https://techcrunch.com/tag/yassir/) |
| EIS | private (growth investment, Jun 2021) | core insurance platform for carriers | FINEOS | florin | [source](https://www.eisgroup.com/2021/06/29/eis-announces-growth-investment-of-more-than-100-million-from-tpg/) |
| Hippo | listed (NYSE:HIPO) | Digital home insurance carrier | Guidewire Software, Inc.; ZhongAn Online P&C | florin | [source](https://insurance.nttdata.com/post/insurtech-post-hippo-lmnd-root/) ; [source](https://stockanalysis.com/stocks/hipo/company/) |
| INSTANDA | private (round led by Toscafund, Jun 2022) | no-code core insurance platform | Sapiens International | florin | [source](https://coverager.com/instanda-raises-45-million/) |
| Kin Insurance | private (Series E, Sep 2025) | direct-to-consumer digital home insurer | Guidewire Software, Inc. | florin | [source](https://www.lw.com/en/news/2025/09/latham-watkins-advises-kin-insurance-million-series-e-financing-round) |
| Lemonade | listed (NYSE:LMND) | AI-driven digital insurance carrier | Guidewire Software, Inc.; ZhongAn Online P&C; FINEOS | florin | [source](https://insurance.nttdata.com/post/insurtech-post-hippo-lmnd-root/) ; [source](https://stockanalysis.com/stocks/lmnd/company/) ; [source](https://www.lemonade.com/investor) |
| Novidea | private (Series C, Apr 2024) | cloud insurance distribution platform for brokers, MGAs, insurers | Sapiens International | florin | [source](https://coverager.com/novidea-raises-30-million/) |
| Root | listed (NASDAQ:ROOT) | telematics-priced direct auto insurer | Guidewire Software, Inc.; ZhongAn Online P&C | florin | [source](https://insurance.nttdata.com/post/insurtech-post-hippo-lmnd-root/) ; [source](https://stockanalysis.com/stocks/root/company/) |
| Socotra | private (Series C, Mar 2022) | cloud-native core policy platform for insurers | Guidewire Software, Inc.; FINEOS | florin | [source](https://www.socotra.com/series-c-announcement/) |
| Waterdrop | listed (NYSE:WDH) | Chinese online insurance distribution | ZhongAn Online P&C | florin | [source](https://stockanalysis.com/stocks/wdh/company/) |
| Affinity | private (Series C, Sep 2021) | relationship-intelligence CRM for VCs and dealmakers | Clay | fundraisly | [source](https://techcrunch.com/2021/09/09/affinity-a-relationship-intelligence-company-raises-80m-to-help-close-deals/) |
| Cognism | private (Series C, Jan 2022) | B2B contact data, Europe focus | Apollo.io; Clay; ZoomInfo | fundraisly | [source](https://www.cognism.com/newsroom/series-c-funding-press-release) |
| Comscore | listed (NASDAQ:SCOR) | Audience and web traffic measurement | Similarweb Ltd. | fundraisly, openseo, rybbit | [source](https://stockanalysis.com/stocks/scor/company/) |
| Demandbase | private (growth financing, Feb 2023) | ABM and account intelligence platform | 6sense | fundraisly | [source](https://www.prnewswire.com/news-releases/demandbase-raises-175-million-in-new-financing-301748702.html) |
| LeadIQ | private (venture round, Oct 2021) | Prospecting and lead capture software | Apollo.io | fundraisly | [source](https://techcrunch.com/tag/leadiq/) |
| Lusha | private (Series B, Nov 2021) | B2B contact data and prospecting | Apollo.io; Clay; ZoomInfo | fundraisly | [source](https://www.calcalistech.com/ctech/articles/0,7340,L-3922213,00.html) ; [source](https://techcrunch.com/2021/11/10/lusha-a-crowdsourced-data-platform-for-b2b-sales-gets-205m-series-b-at-1-5b-valuation/) |
| Metadata.io | private (Series B, Mar 2022) | automated B2B demand generation | 6sense | fundraisly | [source](https://www.finsmes.com/2022/03/metadata-io-raises-40m-in-series-b-funding.html) |
| Socure | private (Series E, Nov 2021) | identity verification and fraud AI | Mitek Systems; Red Violet, Inc. | levocred, fundraisly | [source](https://www.socure.com/news-and-press/strategic-growth-investment-fravity-acquisition) ; [source](https://techcrunch.com/tag/socure/) |
| TechTarget | listed (NASDAQ:TTGT) | purchase-intent data and B2B media | ZoomInfo | fundraisly | [source](https://stockanalysis.com/stocks/ttgt/) |
| TransUnion | listed (NYSE:TRU) | credit bureau, emerging market presence | Fair Isaac; Red Violet, Inc. | kita, fundraisly | [source](https://koalagains.com/stocks/NYSE/FICO/competition) ; [source](https://umbrex.com/resources/company-profiles/red-violet/) |
| E2B | private (Series A, Jul 2025) | sandboxed cloud runtimes for AI agents | Docker | herdr | [source](https://e2b.dev/blog/series-a) |
| Modal | private (funding round, May 2026) | serverless cloud for AI code and agents | Docker | herdr | [source](https://siliconangle.com/2026/05/21/serverless-ai-infrastructure-startup-modal-labs-seals-355m-funding-round/) |
| Northflank | private (Series A, Nov 2024) | run containers, databases, jobs on any cloud | Docker | herdr | [source](https://northflank.com/blog/northflank-raises-22m-to-make-kubernetes-work-for-your-developers-ship-workloads-not-infrastructure) |
| Fukuyama Transporting | listed (TYO:9075) | Japanese parcel and freight carrier, own fleet | SG Holdings | hived | [source](https://stockanalysis.com/quote/tyo/9075/) |
| Seino Holdings | listed (TYO:9076) | Japanese parcel and freight carrier, own fleet | SG Holdings | hived | [source](https://stockanalysis.com/quote/tyo/9076/) |
| Franklin Covey | listed (NYSE:FC) | Corporate training and leadership content | Learning Technologies Group | honen | [source](https://stockanalysis.com/stocks/fc/company/) |
| Synthesia | private (Series E, Jan 2026) | AI video for workforce training | Learning Technologies Group | honen | [source](https://www.synthesia.io/series-e) |
| Brand24 | listed (WSE:B24) | Social listening and brand monitoring | Sprinklr, Inc.; Sprout Social, Inc. | honestly | [source](https://www.bankier.pl/inwestowanie/profile/quote.html?symbol=BRAND24) ; [source](https://stockanalysis.com/quote/wse/B24/) |
| Trustpilot | listed (LSE:TRST) | online consumer review platform | Sprout Social, Inc. | honestly | [source](https://stockanalysis.com/quote/lon/TRST/) |
| ClickHouse | private (Series D, Jan 2026) | open-source real-time analytics database with cloud service | Elastic N.V. | insforge | [source](https://clickhouse.com/company/news) |
| Convex | private (Series B, Aug 2026) | Backend platform for developers and AI agents | Supabase | insforge | [source](https://news.convex.dev/convex-raises-57m/) |
| Grafana Labs | private (Series D extension, Aug 2024) | open-source observability platform; names Elastic as rival | Elastic N.V. | insforge | [source](https://sacra.com/c/grafana-labs/) |
| Meilisearch | private (Series A, Oct 2022) | Open source search API | Algolia | insforge | [source](https://techcrunch.com/2022/10/10/meilisearch-lands-15m-investment-to-grow-its-search-as-a-service-business/) |
| Qdrant | private (Series A, Jan 2024) | open-source vector search engine for AI apps | Elastic N.V.; Algolia | insforge | [source](https://qdrant.tech/blog/series-a-funding-round/) ; [source](https://www.cbinsights.com/company/qdrant/financials) |
| Railway | private (Series B, Jan 2026) | Cloud deploy and managed databases | Supabase | insforge | [source](https://blog.railway.com/p/series-b) |
| agilon health | listed (NYSE:AGL) | Senior primary care on per-member payments | Evolent Health, Inc. | insurf | [source](https://stockanalysis.com/stocks/agl/company/) |
| Astrana Health | listed (NASDAQ:ASTH) | Care management and coordination company | Evolent Health, Inc. | insurf | [source](https://stockanalysis.com/stocks/asth/company/) |
| Health Catalyst | listed (NASDAQ:HCAT) | Data and analytics for payers and providers | Evolent Health, Inc. | insurf | [source](https://craft.co/evolent-health/competitors) |
| Healthee | private (Series B, Apr 2025) | AI benefits navigation for employees | Accolade | insurf | [source](https://www.mobihealthnews.com/news/healthee-secures-50m-oversubscribed-series-b-round) |
| Privia Health | listed (NASDAQ:PRVA) | Physician enablement for value-based care | Evolent Health, Inc. | insurf | [source](https://stockanalysis.com/stocks/prva/company/) |
| Taktile | private (Series C, Jun 2026) | decision automation for lenders | Fair Isaac | kita, levocred | [source](https://theailandscape.com/news/taktile-lands-110m-series-c-funding/) |
| Zest AI | private (customer-led round, Nov 2025) | AI credit underwriting for lenders | Fair Isaac | kita | [source](https://fintech.global/2025/11/05/ai-lending-platform-zest-ai-secures-new-funding-round/) |
| Hebbia | private (Series B, Jul 2024) | AI document analysis for financial firms | Morningstar, Inc.; AlphaSense | lato | [source](https://research.contrary.com/company/hebbia) ; [source](https://www.hebbia.com/blog/hebbia-raises-usd130m-series-b) |
| Rogo | private (Series D, Apr 2026) | AI analyst for banks, PE and hedge funds; names AlphaSense as rival | Morningstar, Inc.; AlphaSense | lato | [source](https://research.contrary.com/company/rogo) ; [source](https://www.prnewswire.com/news-releases/rogo-raises-160m-series-d-to-scale-the-agentic-platform-for-finance-302756546.html) |
| Value Line | listed (NASDAQ:VALU) | investment research publisher | Morningstar, Inc. | lato | [source](https://stockanalysis.com/stocks/valu/) |
| Ocrolus | private (Series C, Sep 2021) | document automation for lenders | Mitek Systems | levocred | [source](https://www.prnewswire.com/news-releases/ocrolus-raises-80m-in-series-c-funding-to-scale-its-financial-services-focused-document-automation-solution-301383271.html) |
| Persona | private (Series D, Apr 2025) | identity verification platform | Mitek Systems | levocred | [source](https://withpersona.com/blog/series-d/) |
| Veriff | private (Series C, Jan 2022) | document and biometric ID verification | Mitek Systems | levocred | [source](https://www.finsmes.com/2022/01/veriff-raises-100m-in-series-c-funding-at-1-5-billion-valuation.html) |
| Butternut Box | private (growth round, May 2025) | Fresh dog food subscription across Europe | BARK, Inc. | lyka | [source](https://www.eu-startups.com/2025/05/london-based-butternut-box-raises-more-than-e75-million-euros-to-expand-its-fresh-dog-food-offering/) |
| Freshpet | listed (NASDAQ:FRPT) | Fresh refrigerated dog and cat meals | BARK, Inc. | lyka | [source](https://stockanalysis.com/stocks/frpt/company/) |
| Petco | listed (NASDAQ:WOOF) | Pet retailer with vet, grooming and subscriptions | BARK, Inc. | lyka | [source](https://stockanalysis.com/stocks/woof/company/) |
| The Farmer's Dog | private (Series E, Jun 2022) | Fresh dog food subscription delivered to the door | BARK, Inc. | lyka | [source](https://forgeglobal.com/the-farmer-s-dog_ipo/) |
| AutoStore | listed (Oslo Bors:AUTO) | Automated storage and retrieval systems | Berkshire Grey; GXO Logistics, Inc. | manifold-robotics | [source](https://koalagains.com/stocks/NASDAQ/SYM/competition) ; [source](https://en.wikipedia.org/wiki/AutoStore) |
| Geek+ (Beijing Geekplus) | listed (HKEX:2590) | Goods-to-person warehouse robots | GXO Logistics, Inc. | manifold-robotics | [source](https://www.prnewswire.com/news-releases/geekplus-lists-on-hkex-main-board-pioneering-the-global-smart-logistics-transformation-with-robotics-302500963.html) |
| Geekplus | listed (HKEX:2590) | autonomous mobile warehouse robots | Berkshire Grey | manifold-robotics | [source](https://www.automatedwarehouseonline.com/geekplus-lists-hong-kong-stock-exchange/) |
| Locus Robotics | private (Series G, Sep 2026) | Autonomous mobile robots for warehouse picking | Berkshire Grey; GXO Logistics, Inc. | manifold-robotics | [source](https://www.finsmes.com/2026/09/locus-robotics-raises-41-6m-in-series-g-funding.html) |
| Symbotic | listed (NASDAQ:SYM) | robotic warehouse automation systems | Berkshire Grey; GXO Logistics, Inc. | manifold-robotics | [source](https://www.nanalyze.com/2022/04/berkshire-grey-stock-warehouse-automation/) ; [source](https://stockanalysis.com/stocks/sym/company/) |
| 7shifts | private (Series C, Feb 2022) | Restaurant scheduling and labor | Restaurant365 | marble | [source](https://www.cbinsights.com/company/7shifts/financials) |
| Lunchbox | private (Series B, Feb 2022) | Ordering and marketing for restaurant brands | Owner | marble | [source](https://techcrunch.com/tag/lunchbox/) |
| MarginEdge | private (Series C, Dec 2022) | Restaurant invoice and inventory | Restaurant365 | marble | [source](https://www.cbinsights.com/company/marginedge/financials) |
| Nory | private (Series B, Sep 2025) | AI restaurant operations | Restaurant365 | marble | [source](https://www.cbinsights.com/company/nory/financials) |
| Popmenu | private (Series C, Sep 2021) | Restaurant websites, ordering, automated marketing | Owner | marble | [source](https://www.restaurantbusinessonline.com/technology/online-ordering-company-popmenu-raises-65m-round-led-tiger-global) |
| SpotOn | private (Series F, May 2022) | Restaurant POS, ordering and operations | Owner | marble | [source](https://techcrunch.com/tag/spoton/) |
| Hokodo | private (equity round, Apr 2025) | Pan-European B2B trade credit and BNPL | Billie | mondu | [source](https://www.hokodo.co/resources/hokodo-secures-eu10m-equity-raise-led-by-korelya-capital-and-opera-tech-ventures-for-digital-trade-credit-product-innovation) |
| Slope | private (equity and debt, Jul 2024) | AI B2B payments and credit at checkout | Billie | mondu | [source](https://www.businesswire.com/news/home/20240717100691/en) |
| Two | private (equity round, Jul 2025) | B2B checkout with deferred payment terms | Billie | mondu | [source](https://tech.eu/2025/07/11/two-raises-eur13m-to-scale-its-b2b-payments-solutions/) |
| Dojo (Paymentsense) | private (private equity round, May 2025) | Card machines for UK SMBs | SumUp | moov | [source](https://www.cbinsights.com/company/paymentsense/financials) |
| Yoco | private (Series C, Jul 2021) | Card readers, SMB payments | SumUp | moov | [source](https://www.cbinsights.com/company/yoco/financials) |
| Picnic | private (growth round, Nov 2025) | Own-inventory online supermarket, scheduled delivery | Ocado Group plc | oda | [source](https://nltimes.nl/2025/11/22/online-supermarket-picnic-raises-eu430-million-expand-germany-boost-ai-automation) |
| Rohlik Group | private (Series D, Jun 2022) | Own-inventory online grocer, central Europe | Ocado Group plc | oda | [source](https://www.rohlik.group/amidst-market-turbulence-investors-show-strong-confidence-rohlik-group-eu220m-series-d-raise) |
| Botify | private (growth equity, Oct 2023) | Enterprise SEO automation | Semrush | openseo | [source](https://www.softwarereviews.com/categories/258/products/9806/alternatives) |
| Conductor | private (private equity round, Nov 2021) | Enterprise SEO platform | Semrush | openseo | [source](https://www.cbinsights.com/company/conductor/financials) |
| Profound | private (Series C, Jul 2026) | AI answer-engine visibility analytics | Similarweb Ltd. | openseo | [source](https://www.tryprofound.com/blog/profound-raises-96m-series-c) |
| Foretellix | private (Series C closing, Dec 2023) | verification and validation software for ADAS and autonomy | Applied Intuition | osseus | [source](https://www.foretellix.com/foretellix-raises-85-million-in-series-c-closing/) |
| Foxglove | private (Series B, Nov 2025) | data and visualization platform for robotics teams | Applied Intuition; Vention | osseus | [source](https://foxglove.dev/blog/foxglove-series-b) |
| Viam | private (Series C, Mar 2025) | software platform to build and run smart machines | Applied Intuition; Vention | osseus | [source](https://www.viam.com/press-releases/viam-announces-30-million-series-c) ; [source](https://www.viam.com/post/series-c) |
| BillingPlatform | private (growth equity, Jan 2024) | enterprise billing and revenue management | Zuora | paymentkit | [source](https://www.finsmes.com/2024/01/billingplatform-secures-90m-growth-equity-investment.html) |
| Easebuzz | private (Series A, Apr 2025) | Indian payment gateway and billing SaaS | Cashfree Payments | paymentkit | [source](https://easebuzz.in/news-room/press-release/easebuzz-raises-usd30mn-series-a-funding-led-by-bessemer/) |
| Gr4vy | private (Series A extension, Jan 2022) | cloud-native payment orchestration | Juspay | paymentkit | [source](https://gr4vy.com/posts/gr4vy-announces-a-15m-series-a-extension-funding-to-accelerate-rapid-growth/) |
| Metronome | private (Series C, Feb 2025) | usage-based billing platform | Zuora | paymentkit | [source](https://www.finsmes.com/2025/02/metronome-raises-50m-in-series-c-funding.html) |
| Paddle | private (Series D, May 2022) | merchant of record billing for SaaS | Zuora | paymentkit | [source](https://www.finsmes.com/2022/05/paddle-raises-200n-in-series-d-funding.html) |
| Payrails | private (Series A, Jun 2025) | enterprise payment operations and routing | Juspay | paymentkit | [source](https://www.payrails.com/blog/payrails-series-a) |
| PhonePe | private (pre-IPO round, Oct 2025; DRHP filed, check listing status) | Indian digital payments and financial services | Cashfree Payments | paymentkit | [source](https://thepaypers.com/payments/news/general-atlantic-invests-usd-600-mln-in-phonepe-ahead-of-ipo) |
| Primer | private (Series C, May 2026) | payment orchestration across processors | Juspay | paymentkit | [source](https://primer.io/blog/series-c) |
| Drata | private (Series C, Dec 2022) | Compliance automation platform | AuditBoard | payna | [source](https://www.helpnetsecurity.com/2022/12/08/drata-funding/) |
| Hyperproof | private (growth round, Aug 2023) | Compliance operations software | AuditBoard | payna | [source](https://hyperproof.io/resource/hyperproof-reaches-40m-growth-funding/) |
| Secureframe | private (Series B, Feb 2022) | Security compliance automation | AuditBoard | payna | [source](https://secureframe.com/blog/series-b) |
| Playtika | listed (NASDAQ:PLTK) | Mobile casual and social games | Roblox | playabl | [source](https://stockanalysis.com/stocks/pltk/company/) |
| Rec Room | private (growth round, Dec 2021) | Cross-platform user-generated games and rooms | Roblox | playabl | [source](https://en.wikipedia.org/wiki/Rec_Room_(video_game)) |
| Substack | private (Series C, Jul 2025) | Paid creator subscriptions | Patreon | playabl | [source](https://www.cbinsights.com/company/substack/financials) |
| Take-Two Interactive | listed (NASDAQ:TTWO) | Console and mobile game publisher | Roblox | playabl | [source](https://www.marketbeat.com/stocks/NYSE/RBLX/competitors-and-alternatives/) |
| Thinkific | listed (TSX: THNC) | Creator courses and memberships | Patreon | playabl | [source](https://circle.so/blog/patreon-alternatives) |
| Agorapulse | private (VC round, Sep 2019) | Social media scheduling suite | Buffer | postiz | [source](https://www.cbinsights.com/company/agorapulse/financials) |
| Metricool | private (corporate minority, Sep 2024) | Social publishing and analytics | Buffer | postiz | [source](https://www.cbinsights.com/company/metricool/financials) |
| Aiven | private (Series D, May 2022) | managed open-source data infrastructure cloud | Confluent | projectx | [source](https://aiven.io/press/Aiven-raises-210M-to-invest-in-sustainable-open-source-cloud) |
| Redpanda | private (Series C, Jun 2023) | Kafka-compatible streaming data platform | Confluent | projectx | [source](https://www.redpanda.com/press/redpanda-raises-100m-in-series-c-funding) |
| Temporal | private (Series C, Mar 2025) | durable execution platform for long-running workflows | Confluent | projectx | [source](https://temporal.io/news/temporal-technologies-secures-valuation-to-fuel-durable-execution) |
| Appen | listed (ASX:APX) | Data sourcing, annotation and model evaluation | Invisible Technologies | qokedas | [source](https://invisibletech.ai/blog/scale-ai-alternatives-and-competitors-how-invisible-compares) |
| Snorkel AI | private (Series D, May 2025) | Expert data development platform for AI | Invisible Technologies | qokedas | [source](https://www.businesswire.com/news/home/20250529083998/en/) |
| FullStory | private (Series E, Aug 2022) | Session replay analytics | Contentsquare | rybbit, simulithic | [source](https://www.cbinsights.com/company/fullstory/financials) |
| Mixpanel | private (Series C, Nov 2021) | product analytics for digital products | Adobe Inc.; Contentsquare; Amplitude | rybbit, simulithic | [source](https://mixpanel.com/blog/winning-product-analytics-series-c/) ; [source](https://en.wikipedia.org/wiki/Mixpanel) ; [source](https://www.research-live.com/article/news/mixpanel-completes-200m-series-c-funding-round/id/5092282) |
| Pendo | private (Series F, Jul 2021) | product analytics plus in-app guidance | Amplitude | rybbit, simulithic | [source](https://www.prnewswire.com/news-releases/pendo-raises-150-million-to-help-companies-deliver-software-that-meets-rising-user-expectations-301342064.html) |
| Hugging Face | private (Series D, Aug 2023) | open-source ML model platform | Anthropic | skybridge | [source](https://www.finsmes.com/2023/08/hugging-face-raises-235m-in-series-d-funding-valued-at-4-5-billion.html) |
| Mistral AI | private (Series D, Sep 2026) | frontier LLMs and enterprise agents | Anthropic; Cohere; OpenAI | twelvelabs, world-labs, skybridge | [source](https://www.euronews.com/business/2026/09/08/mistral-ai-raises-record-3-billion-in-samsung-led-funding-round) ; [source](https://mistral.ai/news/mistral-ai-raises-1-7-b-to-accelerate-technological-progress-with-ai) |
| Isometric | private (equity round, Jun 2026) | Carbon removal registry and certification | Xpansiv | supercritical | [source](https://isometric.com/press) |
| Patch | private (Series B, Sep 2022) | Carbon credit procurement platform | Xpansiv | supercritical | [source](https://www.patch.io/press) |
| Sylvera | private (Series B, Jul 2023) | Carbon credit ratings and procurement | Xpansiv | supercritical | [source](https://techcrunch.com/tag/sylvera/) |
| Watershed | private (Series C, Feb 2024) | Enterprise carbon accounting platform | Xpansiv | supercritical | [source](https://watershed.com/blog/series-c) |
| AI21 Labs | private (Series C, Nov 2023) | enterprise LLMs, private deployment | Cohere | twelvelabs | [source](https://www.ai21.com/blog/ai21-completes-208-million-oversubscribed-series-c-round/) |
| Runway | private (funding round, Apr 2025) | generative video models | OpenAI | world-labs, twelvelabs | [source](https://techcrunch.com/2025/04/03/runway-best-known-for-its-video-generating-models-raises-308m/) |
| Sakana AI | private (strategic investment, Mar 2026) | foundation model developer, Tokyo | Anthropic | twelvelabs | [source](https://www.finsmes.com/2026/03/sakana-ai-receives-investment-from-mitsubishi-electric-corporation.html) |
| Anchorage Digital | private (Series D, Dec 2021) | Federally chartered crypto custody bank | Fireblocks | unifold | [source](https://www.fintechfutures.com/blockchain-crypto-digital-assets/digital-asset-infrastructure-provider-anchorage-raises-350m-in-series-d-round) |
| BitGo | listed (NYSE:BTGO) | Digital asset custody and wallet infrastructure | Fireblocks | unifold | [source](https://www.businesswire.com/news/home/20260121850585/en) |
| Conduit | private (Series A, May 2025) | stablecoin cross-border payment rails | BVNK | unifold | [source](https://www.businesswire.com/news/home/20250528156066/en/Conduit-Raises-$36-Million-Series-A-to-Scale-Use-of-Stablecoins-for-Cross-Border-Payments) |
| Copper | private (Series C, Oct 2022) | Institutional custody and settlement (ClearLoop) | Fireblocks | unifold | [source](https://www.ledgerinsights.com/copper-digital-asset-custody-funding-196m/) |
| Gemini | listed (Nasdaq:GEMI) | Crypto exchange and custody | Coinbase Global, Inc. | unifold | [source](https://www.coindesk.com/markets/2026/01/29/crypto-linked-stocks-continue-2026-plunge-but-bitcoin-miners-with-ai-pivots-outperform) |
| Kraken (Payward) | private (equity round, Nov 2025); IPO filed, paused | Crypto exchange | Coinbase Global, Inc. | unifold | [source](https://capital.com/en-int/learn/ipo/kraken-ipo) |
| AssemblyAI | private (Series C, Dec 2023) | Speech-to-text API | ElevenLabs | wispr-flow | [source](https://www.cbinsights.com/company/assemblyai/financials) |
| Cartesia | private (Series A extension, Oct 2025) | Real-time voice AI models | ElevenLabs | wispr-flow | [source](https://www.cbinsights.com/company/cartesia/financials) |
| Speechmatics | private (Series B, Jun 2022) | Speech recognition API | ElevenLabs | wispr-flow | [source](https://www.cbinsights.com/company/speechmatics/financials) |
| Webflow | private (Series C, Mar 2022) | visual no-code website builder with CMS and hosting; names Framer as rival | Framer | wispr-flow | [source](https://sacra.com/c/webflow/) |
| Black Forest Labs | private (Series B, Dec 2025) | image and video generation models | Cohere; OpenAI | world-labs | [source](https://www.finsmes.com/2025/12/black-forest-labs-raises-300m-in-series-b-funding.html) ; [source](https://bfl.ai/blog/our-300m-series-b) |
| Luma AI | private (Series C, Nov 2025) | multimodal video generation models | OpenAI | world-labs | [source](https://lumalabs.ai/news/series-c) |
