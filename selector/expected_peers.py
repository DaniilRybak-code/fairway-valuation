# -*- coding: utf-8 -*-
"""The market's own comparable set, frozen next to ours.

Daniil's test, 28-Aug: google the company name and read the SPONSORED results, then google
"alternatives to X". Sponsored results are companies that have PAID to sit beside that name. An
alternatives page is written by someone who had to choose between them. Both are a comp set revealed
by the market rather than derived from our tags, which makes them the sharpest outside check we have
on whether the engine is picking sensible companies.

WHY THIS IS A FILE AND NOT A LIVE CALL. Three reasons, each sufficient on its own: reading a search
results page programmatically is scraping, and we do not scrape; sponsored slots are personalised,
geo-varied and re-auctioned continuously, so two runs an hour apart disagree; and a golden fixture
has to be deterministic, or a diff stops meaning "the engine changed" and the suite stops being
worth running. So a human runs the searches, the names are written down here with a date, and the
suite reports COVERAGE rather than asserting equality.

HOW THE FIRST 43 WERE BUILT. Four independent research passes on 30-Aug-2026, each told in writing
not to invent companies and to return an empty list rather than a plausible one. Every name below
came back attached to a real source: a company's own /vs/ or /compare page, a Product Hunt
alternatives module, a CB Insights competitor page, a trade-press roundup, or in one case a Mumsnet
thread. Where a search returned a different company of the same name the result was discarded, and
that is recorded in the source line: Honestly (a German employee-engagement firm), AgentX (a
LinkedIn outreach bot), Fyle (an expense-management SaaS), Upstream (livestreaming software).

FIELDS
  peers       companies a human would put in the set. Real names, no inventions.
  listed      the subset that is publicly traded, where any are.
  source      how the names were arrived at, in one line, including what was thrown away.
  checked     the date the searches were run. A stale set is still usable, it is just not fresh.
  confidence  HIGH   a first-party or named-competitor source
              MEDIUM a credible roundup, or several weaker sources agreeing
              LOW    a category proxy, or a set too thin to be worth much. Read these with care.

COVERAGE IS NOT A SCORE TO MAXIMISE. A peer we do not hold in the file cannot be surfaced, so a low
number usually means a data gap, not a matcher defect. Read it against the sourcing list before
touching a single weight.

THREE RESULTS WORTH READING BEFORE ANYTHING ELSE
  payabli   the human set is Rainforest, Finix, Tilled, Adyen for Platforms, Worldpay for Platforms,
            Stripe Connect, Stax Connect. Klarna is not in it and never was.
  hived     the human set is Packfleet, Zedify, Fin, Delivery Mates, Pedal Me and the rest of UK
            sustainable last mile. Wolt, which we were pricing it off, appears in no comparison
            with Hived anywhere.
  mondu     the human set is Billie, Hokodo, Two, Kriya, Tranch, Previse, TreviPay. Klarna and
            Affirm surfaced and were deliberately excluded as consumer credit risk, which is the
            same distinction the engine got wrong on Payabli.
"""

EXPECTED_PEERS = {

 # --- software -------------------------------------------------------------------------------
 'fundraisly': dict(
    peers=['Exitfund', 'VC Boom', 'Go Global World', 'Flowlie', 'Raizer'],
    listed=[],
    source='Product Hunt alternatives page for Fundraisly',
    checked='2026-08-30', confidence='HIGH'),
 'goldfish': dict(
    peers=['Raycast', 'Limitless', 'Cursor'],
    listed=[],
    source='MakerStack review. Rewind became Limitless, acquired by Meta Dec-2025, so one lineage not two',
    checked='2026-08-30', confidence='MEDIUM'),
 'upstream': dict(
    peers=['Shortwave', 'Superhuman', 'Spark', 'Quartz', 'Snoooz AI', 'Canary Mail', 'Slashy',
           'Inbox Zero'],
    listed=[],
    source='Product Hunt alternatives plus a rival own compare page, Shortwave on both. SaaSworthy hits discarded, different Upstream',
    checked='2026-08-30', confidence='HIGH'),
 'bond': dict(
    peers=['Pally', 'Amie', 'Town', 'Martin', 'Coworker', 'Fellow.ai', 'Lindy AI'],
    listed=[],
    source='Product Hunt alternatives, readywhen AI chief of staff roundup, a Bond vs Lindy piece',
    checked='2026-08-30', confidence='HIGH'),
 'mailwarm': dict(
    peers=['Warmy.io', 'Folderly', 'Warmbox', 'Mailivery', 'Mailreach', 'Warmup Inbox', 'Mailforge'],
    listed=[],
    source='Product Hunt alternatives plus warmforge roundup, Warmy and Folderly named on both',
    checked='2026-08-30', confidence='HIGH'),
 'publora': dict(
    peers=['Ayrshare', 'Buffer', 'Publer', 'Postiz', 'Blotato', 'Oktopost'],
    listed=[],
    source='Publora own vs posts against Publer, Buffer and Ayrshare, plus an MCP social roundup',
    checked='2026-08-30', confidence='HIGH'),
 'bluerails': dict(
    peers=['Agentic Hospitality'],
    listed=[],
    source='Hospitality Net coverage of the first hotel MCP booking. One name, deliberately not padded',
    checked='2026-08-30', confidence='LOW'),
 'elentaria': dict(
    peers=['Clay', 'Apollo.io', 'Attio', 'Jeeva AI'],
    listed=[],
    source='Product Hunt alternatives. Category fit uncertain: PH describes a narrower product than the site does',
    checked='2026-08-30', confidence='LOW'),
 'browseract': dict(
    peers=['Browser Use', 'Browserbase', 'Firecrawl', 'Apify', 'Scrapeless', 'ScrapeGraphAI'],
    listed=[],
    source='BrowserAct own comparison posts plus an alternatives directory. Playwright excluded, not a company',
    checked='2026-08-30', confidence='HIGH'),
 'honestly': dict(
    peers=['buzzabout', 'Kraftful', 'Glimpse', 'Senja', 'Famewall'],
    listed=[],
    source='Product Hunt alternatives for usehonestly.com. G2 results discarded, unrelated German firm of the same name',
    checked='2026-08-30', confidence='MEDIUM'),
 'insforge': dict(
    peers=['Supabase', 'Firebase'],
    listed=[],
    source='InsForge own docs alternatives page names exactly these two. Kept short rather than padded',
    checked='2026-08-30', confidence='HIGH'),
 'honen': dict(
    peers=['Coursebox', 'Courseau', 'LearnHouse', 'AcademyOcean', 'Learn.xyz', '360Learning', '7taps'],
    listed=[],
    source='Product Hunt Honen alternatives plus a second roundup, both document-to-course platforms',
    checked='2026-08-30', confidence='HIGH'),
 'agentx': dict(
    peers=['LangSmith', 'Braintrust', 'Arize AI', 'Langfuse', 'Patronus AI', 'Galileo', 'Humanloop'],
    listed=[],
    source='Name collision: every AgentX alternatives page indexes an unrelated outreach bot. Searched on the description instead',
    checked='2026-08-30', confidence='MEDIUM'),
 'skybridge': dict(
    peers=['MCP-UI', 'mcp-use', 'OpenAI Apps SDK'],
    listed=[],
    source='Alpic own blog comparing MCP Apps to ChatGPT Apps, plus the other open frameworks solving the same problem',
    checked='2026-08-30', confidence='MEDIUM'),
 'acti': dict(
    peers=['Gboard', 'Microsoft SwiftKey', 'Wispr Flow', 'Fleksy', 'Typewise', 'CleverType', 'Yaps'],
    listed=['Gboard', 'Microsoft SwiftKey'],
    source='Acti own /vs/ pages against Gboard, Grammarly and Wispr Flow, plus an AI keyboard roundup',
    checked='2026-08-30', confidence='HIGH'),
 'pazi': dict(
    peers=['MindPal', 'Lindy', 'Taskade', 'DayZero', 'Abbi', 'Modelize.ai'],
    listed=[],
    source='Product Hunt Pazi alternatives plus an autonomous agent review of the same category',
    checked='2026-08-30', confidence='MEDIUM'),
 'openseo': dict(
    peers=['Ahrefs', 'Semrush', 'Ubersuggest', 'Screpy', 'Wope', 'Keyword Insights'],
    listed=['Semrush'],
    source='OpenSEO own README and its open-alternative listing name the incumbents; Product Hunt adds the cheaper tier',
    checked='2026-08-30', confidence='HIGH'),
 'context-dev': dict(
    peers=['Firecrawl', 'Apify', 'Exa', 'Tavily', 'Jina AI', 'ScraperAPI', 'ScrapingBee', 'Spider',
           'Browse.ai', 'Crawl4AI'],
    listed=[],
    source='context.dev own /compare page names all ten, and a case study names a customer switching from Firecrawl',
    checked='2026-08-30', confidence='HIGH'),
 'anysearch': dict(
    peers=['Exa', 'Tavily', 'Brave Search API', 'SerpAPI', 'Perplexity', 'Firecrawl'],
    listed=[],
    source='AnySearch names no competitor anywhere. An agentic search benchmark used as a category proxy, so treat with care',
    checked='2026-08-30', confidence='LOW'),

 # --- ecommerce ------------------------------------------------------------------------------
 'sellerclaw': dict(
    peers=['StoreClaw', 'Minami AI', 'SellerChamp', 'Lindy', 'Relevance AI', 'Beam AI'],
    listed=[],
    source='A SellerClaw review names the first three; a second review adds the agent platforms',
    checked='2026-08-30', confidence='HIGH'),
 'fyle': dict(
    peers=['Olive & June', 'Sundays', 'Le Mini Macaron'],
    listed=[],
    source='No alternatives page exists for this brand, and the name collides with an expense SaaS. Adjacent manicure kits only, not confirmed substitutes',
    checked='2026-08-30', confidence='LOW'),
 'smol': dict(
    peers=['Bower Collective', 'Grove Collaborative', 'Splosh', 'Ecover', 'Eco Egg', 'Miniml',
           'Fill', 'Tallow + Ash'],
    listed=['Grove Collaborative'],
    source='CB Insights names Bower Collective top competitor; a Which laundry subscription review; a real consumer thread asking for alternatives',
    checked='2026-08-30', confidence='HIGH'),
 'bokksu': dict(
    peers=['TokyoTreat', 'Sakuraco', 'Japan Crate', 'Umai Crate', 'ZenPop', 'Universal Yums',
           'SnackCrate'],
    listed=[],
    source='Many direct vs Bokksu review posts, plus Bokksu own comparison page',
    checked='2026-08-30', confidence='HIGH'),
 'finn': dict(
    peers=['Sixt', 'Onto', 'Cluno', 'ViveLaCar', 'CARIFY'],
    listed=['Sixt'],
    source='CB Insights states Finn competitors are Onto, imove and Sixt. Cluno was acquired by Cazoo, still a real comparable',
    checked='2026-08-30', confidence='HIGH'),
 'lyka': dict(
    peers=['Scratch', '5 Hounds by Dr Will', 'Petzyo', 'Nosh Project', 'Raw & Fresh', 'Doggy Grub'],
    listed=[],
    source='An Australian fresh dog food ranking that rates Lyka against these named local brands',
    checked='2026-08-30', confidence='HIGH'),
 'oda': dict(
    peers=['Picnic', 'MatHem', 'Rohlik Group', 'Ocado'],
    listed=['Ocado'],
    source='Sifted groups Oda with wide-selection online grocers. Quick commerce names excluded, different model',
    checked='2026-08-30', confidence='HIGH'),

 # --- marketplace ----------------------------------------------------------------------------
 'inato': dict(
    peers=['Elligo Health Research', 'Javara', 'Circuit Clinical', 'Care Access', 'Formation Bio',
           'ObvioHealth'],
    listed=[],
    source='No direct vs page anywhere. A synthesis of CB Insights and site-network trade press. Castor and Transcelerate dropped, wrong category',
    checked='2026-08-30', confidence='LOW'),
 'supercritical': dict(
    peers=['Patch', 'Puro.earth', 'Carbonfuture', 'Senken', 'Watershed', 'CUR8'],
    listed=[],
    source='Two carbon removal marketplace roundups list Supercritical alongside these, plus a direct CUR8 comparison',
    checked='2026-08-30', confidence='MEDIUM'),
 'priori-legal': dict(
    peers=['Axiom', 'UpCounsel', 'PERSUIT', 'LawTrades', 'Legal Hero', 'Lawdingo', 'LAWCLERK',
           'Hire an Esquire'],
    listed=[],
    source='CB Insights Priori competitor page and its Axiom vs Priori page, plus a legal marketplace directory. G2 and Craft discarded as noise',
    checked='2026-08-30', confidence='MEDIUM'),
 'nursa': dict(
    peers=['ShiftKey', 'Clipboard Health', 'CareRev', 'IntelyCare', 'ShiftMed', 'connectRN',
           'Gale Healthcare Solutions'],
    listed=[],
    source='An investigative piece on per-diem nursing apps and a top-12 staffing roundup, both naming Nursa among them',
    checked='2026-08-30', confidence='HIGH'),
 'levelten': dict(
    peers=['Pexapark', 'PPAYA', 'Renewable Exchange', 'Flett Exchange', 'REsurety', 'FlexiDAO'],
    listed=[],
    source='Four separate compare pages triangulating on the same power purchase agreement marketplace cluster',
    checked='2026-08-30', confidence='HIGH'),

 # --- payments -------------------------------------------------------------------------------
 'payabli': dict(
    peers=['Rainforest', 'Finix', 'Tilled', 'Adyen for Platforms', 'Worldpay for Platforms',
           'Stripe Connect', 'Stax Connect'],
    listed=['Adyen for Platforms'],
    source='A direct Payabli vs Rainforest comparison, Rainforest own competitor page naming Payabli, and payfac-as-a-service roundups. KLARNA IS NOT IN IT',
    checked='2026-08-30', confidence='HIGH'),
 'rainforest': dict(
    peers=['Payabli', 'Finix', 'Tilled', 'Modulr', 'Stripe Connect', 'Adyen for Platforms',
           'Infinicept', 'Exact Payments'],
    listed=['Adyen for Platforms'],
    source='CB Insights states Rainforest top competitors include Modulr, Tilled and Payabli; Rainforest own payfac post adds the rest',
    checked='2026-08-30', confidence='HIGH'),
 'moov': dict(
    peers=['Stripe', 'Finix', 'Worldpay for Platforms', 'Unit', 'Bond', 'Lithic', 'Block'],
    listed=['Block'],
    source='A Contrary Research breakdown names Stripe, Finix and Payrix as payfac rivals and Unit and Bond on banking rails; Craft adds Lithic',
    checked='2026-08-30', confidence='MEDIUM'),
 'trolley': dict(
    peers=['Tipalti', 'PayPal', 'Payoneer', 'Stripe', 'Wise', 'Hyperwallet'],
    listed=['PayPal', 'Wise', 'Payoneer'],
    source='Tipalti own Trolley competitors page plus Trolley own vs Tipalti, vs Hyperwallet and vs Payoneer posts',
    checked='2026-08-30', confidence='HIGH'),
 'dots': dict(
    peers=['Routable', 'Trolley', 'Tipalti', 'Hyperwallet', 'Stripe Connect', 'PayPal', 'Checkbook'],
    listed=['PayPal'],
    source='Routable own Dots alternatives page plus Dots own compare pages. G2 results discarded, they were payroll tools',
    checked='2026-08-30', confidence='MEDIUM'),

 # --- lending and balance sheet --------------------------------------------------------------
 'mondu': dict(
    peers=['Billie', 'Hokodo', 'Two', 'Kriya', 'Tranch', 'Previse', 'TreviPay'],
    listed=[],
    source='CB Insights states Mondu competitors are Tranch, Previse, Billie and Hokodo. Klarna and Affirm surfaced and were excluded as consumer credit risk. Hokodo reportedly ceased trading Nov-2025',
    checked='2026-08-30', confidence='HIGH'),
 'numida': dict(
    peers=['Asaak', 'Platinum Credit', 'Pezesha', 'Tenakata', 'Unguka Bank', 'Lupiya'],
    listed=[],
    source='Uganda lender directories plus direct Numida compare pages. Indian lenders dropped, wrong geography',
    checked='2026-08-30', confidence='MEDIUM'),
 'perenna': dict(
    peers=['Habito', 'April Mortgages', 'Kensington Mortgages', 'Atom Bank'],
    listed=[],
    source='Which names Kensington a rival of the new bank; a broker trade piece pairs Perenna with April Mortgages on long-term fixes',
    checked='2026-08-30', confidence='HIGH'),
 'tienda-pago': dict(
    peers=['Konfio', 'KEO World'],
    listed=[],
    source='The CB Insights company page names KEO World and discusses Konfio. Two names only. Aggregator noise discarded',
    checked='2026-08-30', confidence='LOW'),

 # --- delivery -------------------------------------------------------------------------------
 'hived': dict(
    peers=['Packfleet', 'Zedify', 'Fin Sustainable Logistics', 'Delivery Mates', 'Pedal Me',
           'Pedal and Post', 'Gophr', 'Stuart', 'Quiver', 'Koiki'],
    listed=[],
    source='CB Insights Hived alternatives, UK sustainable delivery trade coverage, and cargo bike funding pieces. WOLT APPEARS IN NO COMPARISON WITH HIVED',
    checked='2026-08-30', confidence='MEDIUM'),
 'byrd': dict(
    peers=['Frisbo', 'Omnipack', 'Warehousing1', 'everstox', 'ShipBob', 'ShipMonk', 'Zenfulfillment'],
    listed=[],
    source='CB Insights byrd alternatives page plus a direct byrd vs ShipBob comparison',
    checked='2026-08-30', confidence='HIGH'),
 '99minutos': dict(
    peers=['Treggo', 'Cargamos', 'iVoy', 'iMile Mexico', 'Estafeta', 'Paquetexpress'],
    listed=[],
    source='A TechCrunch piece names 99minutos as a competitor, and a Mexico logistics roundup flags three more as similar. DHL, FedEx and UPS excluded on scale',
    checked='2026-08-30', confidence='HIGH'),
}
