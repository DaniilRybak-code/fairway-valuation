# -*- coding: utf-8 -*-
"""Golden test inputs.

WHY THIS EXISTS. Every later change to weights, tags or data should produce a READABLE DIFF
rather than a silent shift. These profiles are frozen; the expected comparable sets are
snapshotted next to them in selector/golden/. Running golden.py --check prints the difference.

WHAT IS AND IS NOT IN HERE YET. Twelve profiles spanning the three vocabulary families, written
so that each one exercises something specific (named in the comment on each). The 21 website
profiles from claude/Fairway_profiler_website_test.md belong here too and are NOT yet included:
that document's appendix gives nine of the ten fields for each company but not product_tags, and
product_tags is the heaviest weight in the matcher, so adding them without it would freeze a
weak fixture. They go in as soon as the profiler run that produced them can supply the tags.
"""

def P(**k):
    d = dict(archetype='', archetype_secondary=None, industry='Horizontal', function='',
             buyer='CONSUMER', gtm_motion='', revenue_model='', product_role='',
             asset_intensity='', purchase_frequency='', ai_stance='AI_NEUTRAL',
             product_tags='', growth=30.0, gm=70.0)
    d.update(k); return d

RETIRED_INVENTED = [

 # --- consumer family -----------------------------------------------------
 # Exercises: core/secondary split inside one archetype across end markets.
 ("car-marketplace-uk", "UK car marketplace charging dealers a monthly listing subscription", P(
   archetype='Classifieds & Listings', archetype_secondary='Third-Party Marketplace',
   industry='Automotive', function='Listings & Discovery', buyer='SMB',
   gtm_motion='ENT_SALES', revenue_model='LISTING_FEE', product_role='AGGREGATOR',
   asset_intensity='NONE', purchase_frequency='EPISODIC', ai_stance='AI_EMBEDDED',
   product_tags='Auto Classifieds|Car Listings|Dealer Marketing|Vehicle Search|Used Cars',
   growth=25.0, gm=88.0)),

 # Exercises: OWN_PRODUCT must not pull resale retailers.
 ("d2c-skincare", "Direct-to-consumer skincare brand, own formulations, paid social", P(
   archetype='Consumer Brand', industry='Apparel & Beauty', function='Commerce Operations',
   buyer='CONSUMER', gtm_motion='PAID_ACQUISITION', revenue_model='PRODUCT_SALES',
   product_role='BRAND', asset_intensity='OWN_PRODUCT', purchase_frequency='REPEAT_TRANSACTION',
   ai_stance='AI_NEUTRAL',
   product_tags='Skincare|Cosmetics|Direct-to-Consumer|Owned Brand|Beauty|Repeat Purchase',
   growth=45.0, gm=72.0)),

 # Exercises: the gross-profit denominator rule firing on a margin gap.
 ("quick-commerce", "Grocery quick commerce, own dark stores, 20-minute delivery", P(
   archetype='Local Delivery & On-Demand', archetype_secondary='Owned-Inventory Retail',
   industry='Food & Grocery', function='Commerce Operations', buyer='CONSUMER',
   gtm_motion='PAID_ACQUISITION', revenue_model='GMV_RETAIL', product_role='DESTINATION',
   asset_intensity='MIXED', purchase_frequency='REPEAT_TRANSACTION', ai_stance='AI_NEUTRAL',
   product_tags='Quick Commerce|Dark Stores|Grocery Delivery|Local Delivery|Courier Network',
   growth=90.0, gm=25.0)),

 # Exercises: two-sided marketplace where the SELLER pays, against one where the guest pays.
 ("resale-marketplace", "Peer-to-peer resale marketplace for second-hand clothing", P(
   archetype='Third-Party Marketplace', industry='Apparel & Beauty',
   function='Marketplace Operations', buyer='SMB', gtm_motion='NETWORK_EFFECT',
   revenue_model='TAKE_RATE', product_role='DESTINATION', asset_intensity='NONE',
   purchase_frequency='REPEAT_TRANSACTION', ai_stance='AI_EMBEDDED',
   product_tags='Online Marketplace|Recommerce|Luxury Resale|Circular Fashion|Third-Party Sellers|Authentication',
   growth=40.0, gm=78.0)),

 # Exercises: consumer subscription content against ad-supported media.
 ("consumer-learning-app", "Consumer language-learning app on a freemium subscription", P(
   archetype='Online Learning', archetype_secondary='Gaming & Virtual Economy',
   industry='Education', function='Content & Community', buyer='CONSUMER',
   gtm_motion='ORGANIC_BRAND', revenue_model='SUBSCRIPTION_CONSUMER', product_role='DESTINATION',
   asset_intensity='NONE', purchase_frequency='SUBSCRIPTION', ai_stance='AI_NATIVE',
   product_tags='Language Learning|Consumer Subscription|Gamification|Mobile App|Freemium|AI Tutor',
   growth=55.0, gm=73.0)),

 # Exercises: RESALE_INVENTORY, the bucket where a revenue multiple is meaningless.
 ("online-pet-retail", "Online pet food and supplies retailer on an autoship subscription", P(
   archetype='Owned-Inventory Retail', industry='Retail & E-commerce',
   function='Commerce Operations', buyer='CONSUMER', gtm_motion='PAID_ACQUISITION',
   revenue_model='GMV_RETAIL', product_role='DESTINATION', asset_intensity='RESALE_INVENTORY',
   purchase_frequency='REPEAT_TRANSACTION', ai_stance='AI_NEUTRAL',
   product_tags='Online Pet Retail|Consumables|Subscription Commerce|Autoship|Owned Inventory|Fulfilment',
   growth=20.0, gm=29.0)),

 # --- software family, regression ----------------------------------------
 # Exercises: adding 74 consumer names must not pull any of them into a software set.
 ("restaurant-pos", "Restaurant point of sale for independent operators", P(
   archetype='Vertical Software', archetype_secondary='Commerce & Payments Software',
   industry='Hospitality', function='Operations', buyer='SMB', gtm_motion='MIDMARKET',
   revenue_model='PLATFORM', product_role='SOR', ai_stance='AI_EMBEDDED',
   product_tags='Restaurant Software|Point of Sale|POS|Online Ordering|Restaurant Payments',
   growth=25.0, gm=45.0)),

 # Exercises: the word "marketplace" must not now drag consumer names in.
 ("b2b-procurement", "B2B procurement and supplier marketplace for manufacturers", P(
   archetype='Business Applications', industry='Manufacturing', function='Supply Chain',
   buyer='LOB', gtm_motion='ENT_SALES', revenue_model='PLATFORM', product_role='SOR',
   ai_stance='AI_EMBEDDED',
   product_tags='Procurement|Supplier Marketplace|Sourcing|Spend Management|Supply Chain',
   growth=30.0, gm=72.0)),

 # Exercises: design tooling, the profile the size gate would once have broken.
 ("design-tool", "Collaborative browser-based design and prototyping tool", P(
   archetype='Design & Engineering', industry='Horizontal', function='Engineering & Design',
   buyer='LOB', gtm_motion='PLG', revenue_model='SEATS', product_role='SOE',
   ai_stance='AI_EMBEDDED',
   product_tags='Design Tool|Prototyping|Collaborative Design|UI Design|Whiteboard|Website Builder',
   growth=40.0, gm=88.0)),

 # --- fintech family ------------------------------------------------------
 # Exercises: the quality floor. Before it, this profile returned Perplexity at 142.9x.
 ("consumer-neobank", "Consumer neobank earning interchange and net interest on deposits", P(
   archetype='Digital Bank & Deposits', archetype_secondary='Lending & Credit',
   industry='Horizontal', function='Banking & Lending', buyer='CONSUMER',
   gtm_motion='PLG', revenue_model='NET_INTEREST', product_role='SOR',
   ai_stance='AI_NEUTRAL',
   product_tags='Digital Bank|Neobank|Current Account|Debit Card|Interchange|Consumer Deposits|Savings',
   growth=45.0, gm=80.0)),

 # Exercises: sells software TO financials, so it must keep software peers, not banks.
 ("core-banking-software", "Cloud core banking software sold to mid-size banks", P(
   archetype='Vertical Software', industry='Financial Services', function='Banking & Lending',
   buyer='ENT_IT', gtm_motion='ENT_SALES', revenue_model='PLATFORM', product_role='SOR',
   ai_stance='AI_EMBEDDED',
   product_tags='Core Banking|Digital Banking|Bank Software|Loan Origination|Deposit Systems',
   growth=20.0, gm=62.0)),

 # Exercises: a name that straddles commerce and payments, the reason MELI needed a dedup rule.
 ("smb-payments", "Payments and working capital for small online merchants", P(
   archetype='Merchant Acquiring & PSP', archetype_secondary='Lending & Credit',
   industry='Horizontal', function='Finance & Payments', buyer='SMB',
   gtm_motion='PLG', revenue_model='TAKE_RATE', product_role='INFRA_LAYER',
   ai_stance='AI_EMBEDDED',
   product_tags='Merchant Acquiring|Online Payments|Checkout|Merchant Credit|SMB Banking|Payment Processing',
   growth=35.0, gm=45.0)),
]



# ---------------------------------------------------------------------------
# THE TWELVE PROFILES ABOVE ARE RETIRED, 25 AUGUST 2026. THEY WERE INVENTED BY ME.
#
# They are kept in the file, unused, as evidence rather than as tests. Run against the same
# engine on the same day, the two sets score like this on the best listed match:
#
#                        best score     tag points
#   twelve invented      22.8 - 41.3     7.3 - 12.0     12 of 12 return a comparable set
#   twenty-one real       8.0 - 22.6      0.0 -  3.9      1 of 21 returns a comparable set
#
# The invented profiles were not a test. Writing them, I reached for the dataset's own tag
# vocabulary without noticing, so every one of them matched by construction. They passed
# because I had written the answer into the question. The real companies wrote their own tags,
# on their own websites, and share almost nothing with the listed set.
#
# This is why the standing instruction is to test only on real cases.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# THE 21 FIELD-TEST COMPANIES, PROFILED FROM THEIR LIVE WEBSITES, 25 AUGUST 2026
#
# Every one is a REAL company. Twenty are Product Hunt launches from around August 2026 plus
# fyle.io, chosen at random as a stand-in for inbound traffic. All ten fields were re-derived
# from the live sites rather than carried over from the hand-profiling of 24 August, and the
# diff against that hand pass is recorded in docs/. Fyle is now IN SCOPE: it is a physical
# direct-to-consumer brand and the consumer vocabulary now exists to describe it.
#
# growth and gm are None on all 21 and that is not laziness. No website publishes either. They
# are quiz-only fields, so these fixtures deliberately exercise the path a founder takes before
# the quiz financials arrive, and they test the qualitative matching that the weights govern.
# The consequence is that these 21 do not cover growth or margin scoring; the invented profiles
# used to, and when they go, that coverage goes with them.
#
# asset_intensity and purchase_frequency are blank on the twenty software companies, matching
# how every software and fintech peer row is tagged, so those two axes stay silent rather than
# paying points for a shared blank. Fyle carries both, because a consumer brand has a real
# answer to each.
REAL = [
 ('fundraisly', 'Investor matching and outreach run as a productized agency for founders raising',
  dict(archetype='Marketing & Customer Engagement', archetype_secondary='Financial Data & Index',
   industry='Financial Services', function='Sales', buyer='SMB', gtm_motion='MIDMARKET',
   revenue_model='SERVICES_LED', product_role='AGGREGATOR', asset_intensity='', purchase_frequency='',
   ai_stance='AI_EMBEDDED', growth=None, gm=None,
   product_tags='Investor Outreach|Investor Database|AI Investor Matching|Warm Intro Mapping|Done-For-You Fundraising|Investor Meeting Booking|Fundraising CRM')),
 ('goldfish', 'Local-first AI memory layer for Mac and Windows that drafts in your own tone',
  dict(archetype='Consumer & Prosumer Software', archetype_secondary='',
   industry='Horizontal', function='Productivity', buyer='PROSUMER', gtm_motion='PLG',
   revenue_model='', product_role='TOOL', asset_intensity='', purchase_frequency='',
   ai_stance='AI_NATIVE', growth=None, gm=None,
   product_tags='AI Memory|Local-First Desktop App|Context-Aware Writing Assistant|Tone Matching|Cross-App Context Capture|Inline Reply Drafting')),
 ('upstream', 'AI layer over Gmail that triages, drafts and tracks follow-ups for a team',
  dict(archetype='Communications & Collaboration', archetype_secondary='Business Applications',
   industry='Horizontal', function='Productivity', buyer='SMB', gtm_motion='PLG',
   revenue_model='SEATS', product_role='SOE', asset_intensity='', purchase_frequency='',
   ai_stance='AI_NATIVE', growth=None, gm=None,
   product_tags='AI Email Client|Gmail Inbox Assistant|Agentic Inbox|AI Reply Drafting|Shared Team Inbox|Follow-Up Tracking|Human-In-The-Loop Approval')),
 ('bond', 'AI chief of staff in Slack that captures commitments and works a prioritised list',
  dict(archetype='Business Applications', archetype_secondary='Communications & Collaboration',
   industry='Horizontal', function='Productivity', buyer='LOB', gtm_motion='PLG',
   revenue_model='SEATS', product_role='SOE', asset_intensity='', purchase_frequency='',
   ai_stance='AI_NATIVE', growth=None, gm=None,
   product_tags='AI Chief Of Staff|Agentic To-Do List|Slack-Native Assistant|Meeting Prep And Follow-Up|Task Prioritization|Company Context Brain')),
 ('mailwarm', 'Email warm-up and deliverability across a network of aged real inboxes',
  dict(archetype='Marketing & Customer Engagement', archetype_secondary='',
   industry='Horizontal', function='Marketing', buyer='SMB', gtm_motion='PLG',
   revenue_model='CONSUMPTION', product_role='TOOL', asset_intensity='', purchase_frequency='',
   ai_stance='AI_NEUTRAL', growth=None, gm=None,
   product_tags='Email Warmup|Email Deliverability|Sender Reputation|Inbox Placement Monitoring|Spam Score Monitoring|Blacklist Monitoring|Cold Email Infrastructure')),
 ('publora', 'One API and MCP server for publishing and engagement across ten social networks',
  dict(archetype='Data, AI & Developer Tools', archetype_secondary='Marketing & Customer Engagement',
   industry='Horizontal', function='Content & Community', buyer='DEV', gtm_motion='PLG',
   revenue_model='SEATS', product_role='INFRA_LAYER', asset_intensity='', purchase_frequency='',
   ai_stance='AI_EXPOSED', growth=None, gm=None,
   product_tags='Social Media Publishing API|MCP Server|Multi-Platform Post Scheduling|OAuth Abstraction Layer|Social Engagement API|Agency Workspaces')),
 ('bluerails', 'Makes hotels discoverable and bookable by AI travel agents, bypassing OTA commission',
  dict(archetype='Vertical Software', archetype_secondary='Commerce & Payments Software',
   industry='Hospitality', function='Listings & Discovery', buyer='SMB', gtm_motion='PLG',
   revenue_model='PLATFORM', product_role='PLATFORM_SUITE', asset_intensity='', purchase_frequency='',
   ai_stance='AI_NATIVE', growth=None, gm=None,
   product_tags='Hotel AI Visibility Score|Agentic Commerce For Hotels|Channel Manager|Agent-Ready Checkout|Direct Booking Infrastructure|Agentic Payments And Settlement|AI Agent Discovery Registry')),
 ('elentaria', 'One system that runs commercial operations from acquisition through retention',
  dict(archetype='Business Applications', archetype_secondary='Marketing & Customer Engagement',
   industry='Horizontal', function='Operations', buyer='LOB', gtm_motion='ENT_SALES',
   revenue_model='', product_role='PLATFORM_SUITE', asset_intensity='', purchase_frequency='',
   ai_stance='AI_NATIVE', growth=None, gm=None,
   product_tags='Commercial Operations Platform|Agentic Revenue Execution|AI Workflow Automation|Customer Lifecycle Automation|GTM Channel Planning|B2B Deal And Order Coordination')),
 ('browseract', 'Describe the data you want and it builds, hosts and runs the scraper',
  dict(archetype='Data, AI & Developer Tools', archetype_secondary='Cloud & Infrastructure',
   industry='Horizontal', function='Data & Analytics', buyer='DEV', gtm_motion='PLG',
   revenue_model='CONSUMPTION', product_role='INFRA_LAYER', asset_intensity='', purchase_frequency='',
   ai_stance='AI_NATIVE', growth=None, gm=None,
   product_tags='Web Scraping API|Browser Automation|No-Code Web Scraper|AI Agent Browser Infrastructure|Proxy Rotation|CAPTCHA Handling|MCP Server|Self-Healing Scrapers')),
 ('sellerclaw', 'A supervised team of AI agents that runs a merchant Shopify, eBay and Amazon stores',
  dict(archetype='Commerce Enablement & Fulfilment', archetype_secondary='Marketing & Customer Engagement',
   industry='Retail & E-commerce', function='Commerce Operations', buyer='SMB', gtm_motion='PLG',
   revenue_model='CONSUMPTION', product_role='PLATFORM_SUITE', asset_intensity='', purchase_frequency='',
   ai_stance='AI_NATIVE', growth=None, gm=None,
   product_tags='AI Agents For Ecommerce|Multichannel Store Automation|Amazon And Shopify Seller Tools|Product Sourcing Automation|AI Ad Management|Listing Generation|Order Fulfilment Automation')),
 ('honestly', 'Verifies and structures what people say about a product across social platforms',
  dict(archetype='Marketing & Customer Engagement', archetype_secondary='',
   industry='Retail & E-commerce', function='Marketing', buyer='LOB', gtm_motion='ENT_SALES',
   revenue_model='', product_role='TOOL', asset_intensity='', purchase_frequency='',
   ai_stance='AI_EMBEDDED', growth=None, gm=None,
   product_tags='Social Listening|Consumer Insights|Reddit And TikTok Monitoring|Post Authenticity Verification|Product Attribute Analysis|Creator And Affiliate Attribution')),
 ('insforge', 'Backend-as-a-service built so AI coding agents can operate every service end to end',
  dict(archetype='Cloud & Infrastructure', archetype_secondary='Data, AI & Developer Tools',
   industry='Horizontal', function='Engineering & Design', buyer='DEV', gtm_motion='PLG',
   revenue_model='CONSUMPTION', product_role='INFRA_LAYER', asset_intensity='', purchase_frequency='',
   ai_stance='AI_NATIVE', growth=None, gm=None,
   product_tags='Backend As A Service|AI Coding Agent Backend|Portable Postgres Database|Authentication And Storage|Edge Functions|LLM Model Gateway|Vector Search|Agent CLI And Skills')),
 ('honen', 'Turns company documents and recordings into structured courses with a 1:1 AI tutor',
  dict(archetype='Online Learning', archetype_secondary='Business Applications',
   industry='Education', function='HR & Workforce', buyer='SMB', gtm_motion='PLG',
   revenue_model='SEATS', product_role='PLATFORM_SUITE', asset_intensity='', purchase_frequency='',
   ai_stance='AI_NATIVE', growth=None, gm=None,
   product_tags='AI Course Creation|AI Tutor|Corporate Training Platform|LMS Integration|Workforce Development|Auto-Graded Assessments|Certification Prep')),
 ('agentx', 'Build, evaluate and deploy multi-agent systems with CI/CD against test sets',
  dict(archetype='Data, AI & Developer Tools', archetype_secondary='Business Applications',
   industry='Horizontal', function='Engineering & Design', buyer='DEV', gtm_motion='PLG',
   revenue_model='PLATFORM', product_role='PLATFORM_SUITE', asset_intensity='', purchase_frequency='',
   ai_stance='AI_NATIVE', growth=None, gm=None,
   product_tags='Multi-Agent Orchestration|Agent Evaluation Framework|Agent CI/CD|Runtime Tracing And Monitoring|No-Code Agent Builder|White-Label AI Agents|Multi-Channel Agent Deployment')),
 ('skybridge', 'MIT-licensed TypeScript and React framework for building MCP apps',
  dict(archetype='Data, AI & Developer Tools', archetype_secondary='',
   industry='Horizontal', function='Engineering & Design', buyer='DEV', gtm_motion='PLG',
   revenue_model='', product_role='INFRA_LAYER', asset_intensity='', purchase_frequency='',
   ai_stance='AI_NATIVE', growth=None, gm=None,
   product_tags='MCP App Framework|React Framework|TypeScript SDK|Model Context Protocol|Open Source Developer Framework|MCP Server Audit')),
 ('acti', 'A free mobile keyboard that embeds AI agents into any text field',
  dict(archetype='Consumer & Prosumer Software', archetype_secondary='',
   industry='Horizontal', function='Productivity', buyer='CONSUMER', gtm_motion='PLG',
   revenue_model='', product_role='TOOL', asset_intensity='', purchase_frequency='',
   ai_stance='AI_NATIVE', growth=None, gm=None,
   product_tags='Agentic Keyboard|Mobile AI Keyboard|Unified Command Layer|Skill Keys|Skill Builder|App And API Integrations')),
 ('pazi', 'Turns a business idea into an AI agent team that runs the operating work on credits',
  dict(archetype='Business Applications', archetype_secondary='Marketing & Customer Engagement',
   industry='Horizontal', function='Operations', buyer='SMB', gtm_motion='PLG',
   revenue_model='CONSUMPTION', product_role='PLATFORM_SUITE', asset_intensity='', purchase_frequency='',
   ai_stance='AI_NATIVE', growth=None, gm=None,
   product_tags='AI Agent Team|Business Operations Automation|Autonomous Company|Solopreneur Business Tools|AI Outreach And Content|Credit Based Agent Runs')),
 ('openseo', 'Open-source alternative to Ahrefs and Semrush, billed by usage and exposed over MCP',
  dict(archetype='Marketing & Customer Engagement', archetype_secondary='Data, AI & Developer Tools',
   industry='Horizontal', function='Marketing', buyer='SMB', gtm_motion='PLG',
   revenue_model='CONSUMPTION', product_role='TOOL', asset_intensity='', purchase_frequency='',
   ai_stance='AI_EMBEDDED', growth=None, gm=None,
   product_tags='Open Source SEO Platform|Keyword Research|Backlink Analysis|Rank Tracking|Site Audit|MCP Server For SEO Data|AI Visibility Tracking|Self Hostable')),
 ('context-dev', 'One API that turns any URL into LLM-ready markdown, plus crawling and enrichment',
  dict(archetype='Data, AI & Developer Tools', archetype_secondary='Cloud & Infrastructure',
   industry='Horizontal', function='Data & Analytics', buyer='DEV', gtm_motion='PLG',
   revenue_model='CONSUMPTION', product_role='INFRA_LAYER', asset_intensity='', purchase_frequency='',
   ai_stance='AI_EMBEDDED', growth=None, gm=None,
   product_tags='Web Scraping API|LLM Ready Markdown|Website Crawler And Sitemap API|Structured Data Extraction|Brand Data Enrichment|Screenshot API|Typed SDKs')),
 ('anysearch', 'Privacy-first real-time search infrastructure built for agents rather than humans',
  dict(archetype='Data, AI & Developer Tools', archetype_secondary='Cloud & Infrastructure',
   industry='Horizontal', function='Data & Analytics', buyer='DEV', gtm_motion='PLG',
   revenue_model='', product_role='INFRA_LAYER', asset_intensity='', purchase_frequency='',
   ai_stance='AI_NATIVE', growth=None, gm=None,
   product_tags='Agent Search API|AI Native Search Infrastructure|MCP Search Integration|Structured Search Output|Source Deduplication And Filtering|Citation Backed Results|Vertical Search')),
 ('fyle', 'UK direct-to-consumer nail-care brand selling a blade-free manicure kit and its refills',
  dict(archetype='Consumer Brand', archetype_secondary='Owned-Inventory Retail',
   industry='Apparel & Beauty', function='Commerce Operations', buyer='CONSUMER',
   gtm_motion='PAID_ACQUISITION', revenue_model='PRODUCT_SALES', product_role='BRAND',
   asset_intensity='OWN_PRODUCT', purchase_frequency='REPEAT_TRANSACTION',
   ai_stance='AI_NEUTRAL', growth=None, gm=None,
   product_tags='Blade Free Manicure Kit|Nail And Cuticle Care|At Home Manicure System|Cuticle Sealing Balm|Nail Buffers And Filing Strips|DTC Beauty Brand|Consumable Refill Packs')),
]

PROFILES = REAL
