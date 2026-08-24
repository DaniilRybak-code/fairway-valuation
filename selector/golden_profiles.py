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

PROFILES = [

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
