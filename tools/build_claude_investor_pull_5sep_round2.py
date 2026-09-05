#!/usr/bin/env python3
"""
Round two of the 5-Sep-2026 investor pull: data/raw/2026-09-05_investor-pull-claude-round2.csv.
Same columns, same rules and same verification as round one (tools/build_claude_investor_pull_5sep.py):
every deal sentence read on its URL on 5-Sep-2026 and quoted in deal_note, cheque ranges only as the
fund publishes them, stage bands only as the fund states them, no contact details. Loaded by
tools/load_investor_pull_5sep.py alongside round one.

    python3 tools/build_claude_investor_pull_5sep_round2.py
"""
import csv, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(HERE))

def header_of(path):
    for line in open(path, encoding='utf-8'):
        if not line.startswith('#'):
            return next(csv.reader([line.rstrip('\n')]))

FULL = header_of('data/investors.csv')
COLS = [c for c in FULL if c in (
    'investor_key', 'investor_name', 'house_type', 'layer', 'geographies', 'stage_bands',
    'first_cheque_low_m', 'first_cheque_high_m', 'cheque_currency', 'thesis_one_liner',
    'screening_categories', 'subsectors', 'recent_deal_1_company', 'recent_deal_1_date',
    'recent_deal_1_source_url', 'recent_deal_2_company', 'recent_deal_2_date', 'recent_deal_2_source_url',
    'cheque_range_source', 'geographies_source', 'last_verified', 'provenance', 'deal_note')]

CONS, LEARN = 'Consumer & Prosumer Software', 'Online Learning'
TODAY = '2026-09-05'
PROV = 'CLAUDE PULL 05-Sep-2026 round two, fetch-only; every page named here was read that day. '
KIN = 'https://techcrunch.com/2026/05/18/kin-health-raises-9m-to-build-an-ai-notetaker-for-patients/'
KIN_Q = "TechCrunch, 18-May-2026: Kin Health, a consumer app that records the doctor visit and writes a plain-language summary, 'has raised $9 million in a seed funding round led by Maveron' and 'The funding round also saw participation from Town Hall Ventures, Eniac Ventures, Flex Capital, Foundry Square Capital, Pear VC, and The Family Fund.'"
FAMBOT = 'https://techcrunch.com/2026/09/01/fambot-introduces-an-ai-chief-of-staff-for-families/'
FAMBOT_Q = "TechCrunch, 1-Sep-2026: Fambot, a consumer AI assistant for family logistics, 'is backed by $3.5 million in pre-seed funding, co-led by NextView Ventures and Baukunst, with participation from Correlation Ventures, Karman Ventures, and Founders Network'."

rows = []
def add(**k):
    r = {c: '' for c in COLS}
    for kk, v in k.items():
        if kk not in r: raise SystemExit('unknown column ' + kk)
        r[kk] = v
    r['last_verified'] = TODAY
    for c in ('thesis_one_liner', 'deal_note', 'provenance', 'subsectors'):
        assert '@' not in r[c] and 'linkedin' not in r[c].lower(), ('contact detail in', r['investor_key'])
    rows.append(r)

# ---------------------------------------------------------------- consumer & prosumer software, CALLABLE
add(investor_key='flex-capital', investor_name='Flex Capital', house_type='VC', layer='CALLABLE',
    geographies='', geographies_source='NOT PUBLISHED', stage_bands='Seed',
    first_cheque_low_m='0.5', first_cheque_high_m='2', cheque_currency='USD', cheque_range_source='https://www.flexcapital.com/',
    thesis_one_liner='Founders backing founders; we invest at Seed.',
    screening_categories=CONS, subsectors='seed stage; founders backing founders; follow-on through Series A and B',
    recent_deal_1_company='Kin Health', recent_deal_1_date='2026-05', recent_deal_1_source_url=KIN,
    deal_note=KIN_Q + " flexcapital.com: 'We invest at Seed.' and 'First check from $500K to $2M'.",
    provenance=PROV + 'flexcapital.com, flexcapital.com/journal.html, TechCrunch Kin Health article.')

add(investor_key='the-family-fund', investor_name='The Family Fund', house_type='VC', layer='CALLABLE',
    geographies='', geographies_source='NOT PUBLISHED', stage_bands='Series A',
    cheque_currency='USD', cheque_range_source='NOT PUBLISHED',
    thesis_one_liner='We invest in the future of the consumer ecosystem, partnering with innovators across products and technologies striving to continuously upgrade the human experience.',
    screening_categories=CONS, subsectors='health and wellness; beauty and personal care; customer-facing platforms; commerce engines',
    recent_deal_1_company='Kin Health', recent_deal_1_date='2026-05', recent_deal_1_source_url=KIN,
    deal_note=KIN_Q + " familyfund.vc/about: 'Primary focus around Series A stage, while selectively backing high conviction earlier and growthier stage businesses'. Kin Health is listed on familyfund.vc/companies. Most of the portfolio is consumer brands; software names include Superpower, Elemind, Flossy and Kin.",
    provenance=PROV + 'familyfund.vc, familyfund.vc/about/, familyfund.vc/companies/, TechCrunch Kin Health article.')

add(investor_key='gv', investor_name='GV', house_type='Corporate VC', layer='CALLABLE',
    geographies='North America, Europe, and Israel', geographies_source='https://www.gv.com/about',
    stage_bands='Seed; Series A; Series B', cheque_currency='USD', cheque_range_source='NOT PUBLISHED',
    thesis_one_liner='We support innovative founders moving the world forward; we invest from seed to growth stages across the technology and life sciences sectors.',
    screening_categories=CONS, subsectors='AI applications; healthcare; developer tools and security; frontier tech infrastructure',
    recent_deal_1_company='MOTHER.tech (Degen app)', recent_deal_1_date='2026-05',
    recent_deal_1_source_url='https://techfundingnews.com/mother-tech-15m-seed-gv-lerer-hippeau-degen-ai-app/',
    deal_note="Tech Funding News, 5-May-2026: MOTHER.tech 'has raised $15 million in seed funding' and 'Investors include GV, Lerer Hippeau Ventures, BoxGroup, and Shine Capital.' A DISTINCT HOUSE from the held 'Google' and 'Google AI Futures Fund' rows: gv.com, 'With Alphabet as our sole limited partner', 'we invest from seed to growth stages'. No cheque size published. Stage bands are the site's 'seed to growth' read as Seed through Series B.",
    provenance=PROV + 'gv.com, gv.com/about, gv.com/news, gv.com/portfolio, Tech Funding News MOTHER.tech article.')

add(investor_key='canaan', investor_name='Canaan', house_type='VC', layer='CALLABLE',
    geographies='', geographies_source='NOT PUBLISHED', stage_bands='', cheque_currency='USD', cheque_range_source='NOT PUBLISHED',
    thesis_one_liner='We back founders who make the impossible inevitable; an early-stage venture capital firm.',
    screening_categories=CONS, subsectors='AI; consumer; therapeutics; deep tech',
    recent_deal_1_company='OpenArt', recent_deal_1_date='2026-01',
    recent_deal_1_source_url='https://www.canaan.com/news/why-we-led-openart-s-30m-series-a',
    deal_note="Canaan's own post, 30-Jan-2026: 'We at Canaan are thrilled to lead OpenArt's $30M Series A'; OpenArt is an AI visual-media platform used by creators to build characters, worlds and storylines. STAGE BAND LEFT EMPTY: canaan.com/about says only 'an early-stage venture capital firm'. Consumer names in the portfolio include Instacart, Turo, Curtsy, Brigit and UrbanSitter.",
    provenance=PROV + 'canaan.com, canaan.com/about, canaan.com/news, canaan.com/companies.')

add(investor_key='town-hall-ventures', investor_name='Town Hall Ventures', house_type='VC', layer='CALLABLE',
    geographies='across the U.S.', geographies_source='https://www.townhallventures.com/our-approach',
    stage_bands='', first_cheque_low_m='3', first_cheque_high_m='30', cheque_currency='USD',
    cheque_range_source='https://www.townhallventures.com/our-approach',
    thesis_one_liner='We partner with founders who are solving long-standing healthcare challenges for underserved communities.',
    screening_categories=CONS, subsectors='healthcare for underserved communities; patient- and family-facing health tools; AI in healthcare',
    recent_deal_1_company='Kin Health', recent_deal_1_date='2026-05', recent_deal_1_source_url=KIN,
    deal_note=KIN_Q + " townhallventures.com/our-approach: 'Our initial checks range from $3M to $30M', 'We invest across all stages. We prioritize team, business model, and mission over stage.', 'we invest across the U.S.' HEALTHCARE ONLY and a $3m floor: a fit for consumer-health founders raising $2m or more, not for the rest of the cluster; the engine's cheque-fit rule keeps it off smaller raises. STAGE BAND LEFT EMPTY: 'all stages' is not a band.",
    provenance=PROV + 'townhallventures.com, /our-approach, /portfolio (Kin listed), TechCrunch Kin Health article.')

# ---------------------------------------------------------------- online learning, CALLABLE
add(investor_key='outlast-fund', investor_name='Outlast Fund', house_type='Micro VC', layer='CALLABLE',
    geographies='the Baltics and Nordics; Riga and Stockholm', geographies_source='https://www.outlastfund.com/',
    stage_bands='Pre-seed; Seed', first_cheque_low_m='0.05', first_cheque_high_m='0.25', cheque_currency='EUR',
    cheque_range_source='https://www.outlastfund.com/',
    thesis_one_liner='We believe in thoughtful progress, ruthless focus on solving the customers problems and the value of sticking with something long enough to make a real difference.',
    screening_categories=LEARN + '; ' + CONS, subsectors='B2B SaaS; applied AI; digital health; fintech',
    recent_deal_1_company='Flashka', recent_deal_1_date='2026-01',
    recent_deal_1_source_url='https://www.outlastfund.com/post/flashka-raises-1m-pre-seed-and-hits-1m-users-in-a-year',
    recent_deal_2_company='Flashka', recent_deal_2_date='2026-01',
    recent_deal_2_source_url='https://tech.eu/2026/01/12/tallinn-ai-startup-flashka-raises-eur1m-pre-seed-to-rethink-how-students-learn/',
    deal_note="Outlast's own post, 13-Jan-2026: 'At Outlast Fund, we led Flashka's EUR1M pre-seed round'; Flashka is a consumer AI study app with one million users and recurring revenue. tech.eu, 12-Jan-2026: 'Flashka has closed a EUR1 million Pre-Seed round led by Outlast Fund'. outlastfund.com: 'We write our first check at pre-seed or seed' and 'EUR50-250k - Our first check is shaped by the deal, no fixed formula'.",
    provenance=PROV + 'outlastfund.com, its Flashka post, tech.eu Flashka article.')

add(investor_key='ucp-ulixes-capital-partners', investor_name='UCP (Ulixes Capital Partners)', house_type='Micro VC', layer='CALLABLE',
    geographies='Italian founders in Italy or abroad', geographies_source='https://www.ucp.vc/',
    stage_bands='Pre-seed; Seed', cheque_currency='EUR', cheque_range_source='NOT PUBLISHED',
    thesis_one_liner='Pre-seed and seed validated tech, on the market or about to enter, leaning toward digital, wellness, edtech, digital health and agri-foodtech.',
    screening_categories=LEARN + '; ' + CONS, subsectors='digital (B2B); wellness; edtech; digital health',
    recent_deal_1_company='Flashka', recent_deal_1_date='2026-01',
    recent_deal_1_source_url='https://tech.eu/2026/01/12/tallinn-ai-startup-flashka-raises-eur1m-pre-seed-to-rethink-how-students-learn/',
    deal_note="tech.eu, 12-Jan-2026: 'Flashka has closed a EUR1 million Pre-Seed round led by Outlast Fund ... Additional investors in the round include UCP and Vento Ventures.' ucp.vc lists Flashka among its commitments (Edtech, 2025) and states 'PRE-SEED/SEED validated tech, on the market or about to enter' for 'ITALIAN FOUNDERS in Italy or abroad'. No cheque size published.",
    provenance=PROV + 'ucp.vc, tech.eu Flashka article.')

add(investor_key='movens-capital', investor_name='Movens Capital', house_type='VC', layer='CALLABLE',
    geographies='CEE (and CEE diaspora) tech companies', geographies_source='https://movenscapital.com/',
    stage_bands='Pre-seed; Seed; Series A', first_cheque_low_m='0.25', first_cheque_high_m='3', cheque_currency='EUR',
    cheque_range_source='https://movenscapital.com/',
    thesis_one_liner='A multi-stage venture capital fund investing EUR0.25-3M in CEE (and CEE diaspora) tech companies with global ambitions from day one.',
    screening_categories=LEARN + '; ' + CONS, subsectors='AI; B2B software; edtech; ecommerce enablers',
    recent_deal_1_company='BeeSpeaker', recent_deal_1_date='2025-09',
    recent_deal_1_source_url='https://tech.eu/2025/09/25/beespeaker-raises-eur2m-to-help-language-learners-become-confident-speakers/',
    deal_note="tech.eu, 25-Sep-2025: BeeSpeaker, an AI video-tutor language app that adults and teenagers pay for, raised EUR2m in seed funding; 'The round was led by Movens Capital with participation from SpeedUp Venture Capital Group and several international angel investors.' movenscapital.com: 'from pre-seed (but we like to see first paying customers) to A+ rounds', 'Initial checks: EUR250K - EUR3M'.",
    provenance=PROV + 'movenscapital.com, movenscapital.com/talk-funding/, tech.eu and ArcticStartup BeeSpeaker articles.')

add(investor_key='firstpick-vc', investor_name='Firstpick VC', house_type='Micro VC', layer='CALLABLE',
    geographies='founders from Lithuania, Latvia, and Estonia', geographies_source='https://firstpick.vc/',
    stage_bands='Pre-seed', first_cheque_low_m='0.1', first_cheque_high_m='0.5', cheque_currency='EUR',
    cheque_range_source='https://firstpick.vc/',
    thesis_one_liner="We're a generalist early-stage investor with a strong focus on AI first software.",
    screening_categories=CONS + '; ' + LEARN, subsectors='AI-first software; generalist early stage; kids learning (Liledu, Three Cubes in portfolio)',
    recent_deal_1_company='Unive', recent_deal_1_date='2025-09',
    recent_deal_1_source_url='https://tech.eu/2025/09/29/unive-nets-eur410k-to-make-admissions-guidance-more-accessible/',
    deal_note="tech.eu, 29-Sep-2025: Unive, an AI admissions-guidance assistant that students pay for, raised EUR410k: 'The total comprises EUR350,000 from Firstpick VC and a EUR60,000 grant from EduChallenger.' firstpick.vc: 'We invest at inception and pre-seed.', 'Our initial ticket is EUR100k to EUR500k depending on your stage'. Unive is guidance rather than a course product; the portfolio also holds Liledu and Three Cubes, both kids learning.",
    provenance=PROV + 'firstpick.vc, firstpick.vc/portfolio/, tech.eu Unive article.')

add(investor_key='founderful', investor_name='Founderful', house_type='VC', layer='CALLABLE',
    geographies='Switzerland; Swiss and wider European founders', geographies_source='https://www.founderful.com/',
    stage_bands='', cheque_currency='CHF', cheque_range_source='NOT PUBLISHED',
    thesis_one_liner='We back founder teams as their lead investor in their first financing round; first, fast, and founder-friendly.',
    screening_categories=LEARN + '; ' + CONS, subsectors='category-defining technology companies; Swiss founders; first financing rounds',
    recent_deal_1_company='Sparkli', recent_deal_1_date='2026-01',
    recent_deal_1_source_url='https://techcrunch.com/2026/01/24/former-googlers-seek-to-captivate-kids-with-an-ai-powered-learning-app/',
    deal_note="TechCrunch, 24-Jan-2026: Sparkli, an AI learning app for children aged 5 to 12, 'has raised $5 million in pre-seed funding led by Swiss venture firm Founderful.' The app sells to schools first with consumer access for parents planned for mid-2026, so the consumer leg is stated intent at the deal date. STAGE BAND LEFT EMPTY: the site names no band, only 'lead investor in their first financing round'. No cheque published.",
    provenance=PROV + 'founderful.com, founderful.com/about, TechCrunch and Tech Funding News Sparkli articles.')

add(investor_key='10x-founders', investor_name='10x Founders', house_type='VC', layer='CALLABLE',
    geographies='Europe and the US', geographies_source='https://www.10xfounders.com/about',
    stage_bands='Pre-seed; Seed; Series A', first_cheque_low_m='0.5', first_cheque_high_m='2.5', cheque_currency='EUR',
    cheque_range_source='https://www.10xfounders.com/about',
    thesis_one_liner='Great founders build great things: a network-powered early-stage investor backing ambitious founders in Europe and the US.',
    screening_categories=LEARN + '; ' + CONS, subsectors='generalist; network-powered early stage',
    recent_deal_1_company='Songscription', recent_deal_1_date='2025-11',
    recent_deal_1_source_url='https://www.songscription.ai/blog/seed-funding-announcement',
    deal_note="Songscription's own post, 13-Nov-2025: 'Songscription has raised a $5M round led by Reach Capital' with Emerge Capital, 10x Founders and Dent Capital; a subscription tool for learners and musicians. 10xfounders.com/about: 'Our fund specializes in Pre-Seed, Seed, and Series A investments with initial check sizes ranging from EUR500k to EUR2.5m.'",
    provenance=PROV + '10xfounders.com, 10xfounders.com/about, Songscription blog, Emerge blog.')

add(investor_key='specialist-vc', investor_name='Specialist VC', house_type='Micro VC', layer='CALLABLE',
    geographies='founders from Estonia, Latvia, Lithuania, Finland and Ukraine', geographies_source='https://specialist.vc/',
    stage_bands='Pre-seed; Seed; Series A', first_cheque_low_m='0.25', first_cheque_high_m='3', cheque_currency='EUR',
    cheque_range_source='https://specialist.vc/',
    thesis_one_liner="We mainly invest in B2B, SaaS, fintech, platforms, software enabled hardware and deep tech, but we don't limit ourselves to those areas.",
    screening_categories=CONS + '; ' + LEARN, subsectors='B2B; SaaS; fintech; platforms',
    recent_deal_1_company='Vocal Image', recent_deal_1_date='2025-09',
    recent_deal_1_source_url='https://www.frenchweb.fr/vocal-image-leve-33-millions-deuros-pour-ameliorer-la-prise-de-parole-en-public-grace-a-lia/456791',
    deal_note="FrenchWeb, 2-Sep-2025: 'Vocal Image a annonce une levee de 3,3 millions d'euros en seed. Le tour a ete mene par Educapital, avec la participation de Specialist VC et Generations Fund.' Vocal Image is a consumer voice-coaching app with about 50,000 paying users, listed on specialist.vc/portfolio. specialist.vc: 'Main focus Pre-seed to Series A', 'Ticket size EUR0 to 3m', typical starting ticket EUR250k.",
    provenance=PROV + 'specialist.vc, specialist.vc/portfolio/, FrenchWeb, educapitalvc.com/news.')

add(investor_key='white-star-capital', investor_name='White Star Capital', house_type='VC', layer='CALLABLE',
    geographies='London, New York, Montreal, Paris, Toronto, Guernsey, Berlin, Milan, and Abu Dhabi', geographies_source='https://www.whitestarcapital.com/',
    stage_bands='Seed; Series A; Series B', cheque_currency='USD', cheque_range_source='NOT PUBLISHED',
    thesis_one_liner='A global multi-stage technology investment firm backing exceptional entrepreneurs building ambitious, international businesses, from Seed through Series B.',
    screening_categories=LEARN + '; ' + CONS, subsectors='technology; consumer (Butternut Box, FINN, Freshly); digital assets',
    recent_deal_1_company='MyEdSpace', recent_deal_1_date='2025-09',
    recent_deal_1_source_url='https://www.eu-startups.com/2025/09/british-edtech-platform-myedspace-raises-e12-8-million-as-it-prepares-for-us-expansion/',
    recent_deal_2_company='MyEdSpace', recent_deal_2_date='2025-09',
    recent_deal_2_source_url='https://emergecapital.vc/myedspace-raises-15m-series-a-to-stream-the-worlds-best-teachers-to-every-student/',
    deal_note="EU-Startups, 29-Sep-2025: MyEdSpace Series A, EUR12.8m ($15m): 'The round was led by White Star Capital with participation from Educapital, Emerge, Active Partners and Coalition Capital.' Emerge's own post the same day: students at home pay per hour, 'from just GBP5 an hour'. whitestarcapital.com/news: 'backs founders from Seed through Series B'; Fund IV targets Series A to B with a separate North American Seed Fund. No cheque published.",
    provenance=PROV + 'whitestarcapital.com, whitestarcapital.com/news, EU-Startups and Emerge MyEdSpace posts.')

add(investor_key='trilogy-equity-partners', investor_name='Trilogy Equity Partners', house_type='VC', layer='CALLABLE',
    geographies='Pacific Northwest: Seattle, Bellevue, and the broader Washington, Oregon, and British Columbia region', geographies_source='https://www.trilogyequity.com/about/',
    stage_bands='Pre-seed; Seed; Series A', first_cheque_low_m='2', first_cheque_high_m='6', cheque_currency='USD',
    cheque_range_source='https://www.trilogyequity.com/about/',
    thesis_one_liner='Early-stage technology companies rooted in the Pacific Northwest; our sweet spot is leading fundraising rounds.',
    screening_categories=LEARN + '; ' + CONS, subsectors='early-stage technology; Pacific Northwest; learning (Educative, Maximal Learning, BrightCanary in portfolio)',
    recent_deal_1_company='Wild Zebra', recent_deal_1_date='2026-08',
    recent_deal_1_source_url='https://www.geekwire.com/2026/this-startup-just-raised-6m-for-an-ai-tutor-that-helps-kids-figure-it-out-themselves/',
    deal_note="GeekWire, 6-Aug-2026: Wild Zebra, an AI maths and reading tutor that families buy at $48 a month per child (and schools through E3n), raised $6m: 'The oversubscribed seed round was led by Bellevue, Wash.-based Trilogy Equity Partners, with participation from Tetherpoint Capital and angel investors'. trilogyequity.com/about: 'Most of the time, this is at the Seed stage although at times we will also invest at Pre-Seed or Series A' and 'our initial investment will range from $2 to $6 million'.",
    provenance=PROV + 'trilogyequity.com, /about/, /portfolio/, GeekWire Wild Zebra article.')

# ---------------------------------------------------------------- EVIDENCE rows: real, sourced, off the call list with the reason in deal_note
add(investor_key='correlation-ventures', investor_name='Correlation Ventures', house_type='VC', layer='EVIDENCE',
    geographies='U.S.-headquartered companies only', geographies_source='https://correlationvc.com/faqs/',
    stage_bands='Seed; Series A; Series B', first_cheque_low_m='0.1', first_cheque_high_m='4', cheque_currency='USD',
    cheque_range_source='https://correlationvc.com/approach/',
    thesis_one_liner='Sector-agnostic co-investor that fills out venture-led rounds with decisions in days.',
    screening_categories=CONS, subsectors='sector-agnostic co-investment',
    recent_deal_1_company='Fambot', recent_deal_1_date='2026-09', recent_deal_1_source_url=FAMBOT,
    deal_note=FAMBOT_Q + " EVIDENCE, NOT CALLABLE, on its own FAQ: it requires that 'at least one other venture capital firm is also making their first investment into the company' and 'We normally won't be the largest new investor in a syndicate'. Cheque from correlationvc.com/approach: 'Flexible check size from $100,000 to $4 million.'",
    provenance=PROV + 'correlationvc.com, /faqs/, /approach/, TechCrunch Fambot article.')

add(investor_key='karman-ventures', investor_name='Karman Ventures', house_type='VC', layer='EVIDENCE',
    geographies='', geographies_source='NOT PUBLISHED', stage_bands='Pre-seed; Seed; Series A; Series B',
    cheque_currency='USD', cheque_range_source='NOT PUBLISHED',
    thesis_one_liner='A multi-stage venture firm investing from pre-seed to pre-IPO.',
    screening_categories=CONS, subsectors='defence; industrial; AI',
    recent_deal_1_company='Fambot', recent_deal_1_date='2026-09', recent_deal_1_source_url=FAMBOT,
    deal_note=FAMBOT_Q + " EVIDENCE: lead role not stated anywhere, the portfolio on karman.vc is defence and deep tech (Anduril, Hadrian, Crusoe), and Fambot is not on its site. A one-off consumer participation is not a call list entry.",
    provenance=PROV + 'karman.vc, TechCrunch Fambot article.')

add(investor_key='raga-partners', investor_name='Raga Partners', house_type='Family office', layer='EVIDENCE',
    geographies='', geographies_source='NOT PUBLISHED', stage_bands='', cheque_currency='USD', cheque_range_source='NOT PUBLISHED',
    thesis_one_liner='', screening_categories=CONS, subsectors='',
    recent_deal_1_company='Joy (Joy Parenting Club)', recent_deal_1_date='2025-11',
    recent_deal_1_source_url='https://magnifyvc.medium.com/ai-parenting-app-joy-raises-14m-to-redefine-family-support-a44446270d5c',
    deal_note="Magnify Ventures' post, 14-Nov-2025: 'Joy Parenting Club, a San Francisco-based startup, has raised a $14 million Series A, co-led by Raga Partners and Forerunner Ventures'; a consumer parenting app at $12 a month. EVIDENCE: ragapartners.com publishes no stage, cheque, portfolio or thesis and reads as a registered adviser, so first-cheque practice cannot be confirmed. House type is a best reading, unconfirmed.",
    provenance=PROV + 'ragapartners.com, Magnify Medium post.')

add(investor_key='otherwise-fund', investor_name='Otherwise Fund', house_type='VC', layer='EVIDENCE',
    geographies='', geographies_source='NOT PUBLISHED', stage_bands='', cheque_currency='USD', cheque_range_source='NOT PUBLISHED',
    thesis_one_liner='Otherwise is a network of founders investing in founders.', screening_categories=CONS, subsectors='',
    recent_deal_1_company='Marker', recent_deal_1_date='2026-07',
    recent_deal_1_source_url='https://pulse2.com/marker-raises-13-million-seed-funding-to-build-an-ai-native-word-processor/',
    deal_note="Pulse 2.0, 10-Jul-2026: Marker's $13m seed led by Index Ventures 'includes participation from LocalGlobe, Betaworks, Radical Ventures, Tiny VC and Otherwise Fund'. EVIDENCE: otherwisefund.com carries a tagline only and otherwise.fund refused connections, so stage, cheque and geography are unverified. Promote if the site is read.",
    provenance=PROV + 'otherwisefund.com, Pulse 2.0 Marker article.')

add(investor_key='offline-ventures', investor_name='Offline Ventures', house_type='VC', layer='EVIDENCE',
    geographies='', geographies_source='NOT PUBLISHED', stage_bands='', cheque_currency='USD', cheque_range_source='NOT PUBLISHED',
    thesis_one_liner='A venture fund and studio for founders who seek to build differently.', screening_categories=LEARN + '; ' + CONS, subsectors='',
    recent_deal_1_company='Oboe', recent_deal_1_date='2025-09',
    recent_deal_1_source_url='https://techcrunch.com/2025/09/10/after-selling-to-spotify-anchors-co-founders-are-back-with-oboe-an-ai-powered-app-for-learning/',
    deal_note="TechCrunch, 10-Sep-2025: Oboe's $4m seed led by Eniac 'also includes investment from Haystack, Factorial Capital, Homebrew, Offline Ventures'. EVIDENCE: offline.vc renders only its meta description, so stage, cheque and lead practice are unverified.",
    provenance=PROV + 'offline.vc, TechCrunch Oboe article.')

add(investor_key='triple-point-ventures', investor_name='Triple Point Ventures', house_type='VC', layer='EVIDENCE',
    geographies='UK footprint', geographies_source='https://www.triplepoint.vc/',
    stage_bands='Pre-seed; Seed', first_cheque_high_m='5', cheque_currency='GBP', cheque_range_source='https://www.triplepoint.vc/',
    thesis_one_liner='Backing bold founders from day one; we like to lead rounds with tickets up to GBP5m.',
    screening_categories=CONS, subsectors='health; fintech; data and AI; education',
    recent_deal_1_company='Lateral', recent_deal_1_date='2026-02',
    recent_deal_1_source_url='https://www.triplepoint.vc/news/backing-lateral-health-financial-services-for-the-60/',
    deal_note="Triple Point's own post, 3-Feb-2026: 'Lateral has raised a GBP2.5m inception round to build the health and financial services platform for the 60+ mass affluent demographic', Triple Point alongside Augmentum and Tiny.vc. EVIDENCE, NOT CALLABLE: Lateral sells a private medical insurance product to consumers, not a software app, so the deal does not meet the named-consumer-app test; the house itself is a real UK pre-seed and seed lead with Education among its stated sectors. Promote the day it leads a consumer app or learning round.",
    provenance=PROV + 'triplepoint.vc, /news, /portfolio.')

add(investor_key='seek-investments', investor_name='Seek Investments', house_type='Corporate VC', layer='EVIDENCE',
    geographies='invest globally in high growth businesses', geographies_source='https://www.seekinvestments.com/',
    stage_bands='', cheque_currency='AUD', cheque_range_source='NOT PUBLISHED',
    thesis_one_liner='Technology-enabled growth companies across work and learning.', screening_categories=LEARN, subsectors='edtech; online education; HR software',
    recent_deal_1_company='Gizmo', recent_deal_1_date='2026-04',
    recent_deal_1_source_url='https://techcrunch.com/2026/04/15/ai-learning-app-gizmo-levels-up-with-13m-users-and-a-22m-investment/',
    deal_note="TechCrunch, 15-Apr-2026, Gizmo $22m Series A: 'led by Shine Capital, with participation from Ada Ventures, Seek Investments, GSV, and NFX'. EVIDENCE: an A$2bn growth fund with no first-cheque stage published.",
    provenance=PROV + 'seekinvestments.com, TechCrunch Gizmo article.')

add(investor_key='endeavor-catalyst', investor_name='Endeavor Catalyst', house_type='VC', layer='EVIDENCE',
    geographies='35+ markets', geographies_source='https://endeavor.org/catalyst/', stage_bands='', cheque_currency='USD', cheque_range_source='NOT PUBLISHED',
    thesis_one_liner='Set up to invest exclusively in Endeavor Entrepreneur-led companies.', screening_categories=LEARN + '; ' + CONS, subsectors='Endeavor Entrepreneur companies',
    recent_deal_1_company='Headway Inc', recent_deal_1_date='2026-01',
    recent_deal_1_source_url='https://tech.eu/2026/01/15/edtech-platform-headway-inc-secures-series-a-extension-with-backing-from-endeavor-catalyst/',
    deal_note="tech.eu, 15-Jan-2026: Headway Inc, gamified self-growth learning apps for adults with over 160 million users, closed 'the second tranche of its first external funding round, with Endeavor Catalyst participating and investing above its typical check size.' EVIDENCE: a co-investment vehicle restricted to Endeavor entrepreneurs, not callable cold.",
    provenance=PROV + 'endeavor.org/catalyst/, tech.eu Headway article.')

add(investor_key='forsvc', investor_name='ForsVC', house_type='Micro VC', layer='EVIDENCE',
    geographies='game companies based in Belgium, The Netherlands, France, and Germany', geographies_source='https://www.fors.vc/',
    stage_bands='', first_cheque_low_m='0.15', first_cheque_high_m='1.5', cheque_currency='EUR', cheque_range_source='https://www.fors.vc/',
    thesis_one_liner='We invest in the full gaming ecosystem, from game development studios to game technology companies, publishers and services.',
    screening_categories=CONS + '; ' + LEARN, subsectors='game studios; game technology; game publishers; game services',
    recent_deal_1_company='Artwod', recent_deal_1_date='2026-08',
    recent_deal_1_source_url='https://www.eu-startups.com/2026/08/belgian-creative-learning-platform-artwod-raises-e1-1-million-to-launch-creators-marketplace/',
    deal_note="EU-Startups, 20-Aug-2026: Artwod, a guided learning community for visual artists, raised a EUR1.1m seed: 'The round was raised with participation from Airbridge Equity Partners and ForsVC.' fors.vc: 'We invest tickets of EUR150k up to EUR1.5m.' EVIDENCE: a games-only thesis in four countries; the learning deal is an outlier.",
    provenance=PROV + 'fors.vc, EU-Startups Artwod article.')

add(investor_key='3ts-capital-partners', investor_name='3TS Capital Partners', house_type='VC', layer='EVIDENCE',
    geographies='European tech, CEE and DACH', geographies_source='https://www.3tscapital.com/', stage_bands='', cheque_currency='EUR', cheque_range_source='NOT PUBLISHED',
    thesis_one_liner='Lead and co-lead growth rounds in high-growth European technology SMEs.', screening_categories=LEARN, subsectors='SaaS; fintech; cybersecurity; IoT',
    recent_deal_1_company='BOOKR Kids', recent_deal_1_date='2026-08',
    recent_deal_1_source_url='https://www.eu-startups.com/2026/08/hungarys-bookr-kids-closes-e6-1-million-series-a-for-global-edtech-expansion/',
    deal_note="EU-Startups, 25-Aug-2026: BOOKR Kids EUR6.1m Series A led by 'TCEE Fund IV, advised by 3TS Capital Partners'; 600,000 paying students across 3,000 schools, so mostly school-paid. EVIDENCE: a self-described growth investor and a school-sold product.",
    provenance=PROV + '3tscapital.com, EU-Startups BOOKR article.')

out = 'data/raw/2026-09-05_investor-pull-claude-round2.csv'
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=COLS, lineterminator='\n')
    w.writeheader(); w.writerows(rows)
c = sum('CALLABLE' in r['layer'] for r in rows)
print('%d houses -> %s (%d CALLABLE, %d EVIDENCE)' % (len(rows), out, c, len(rows) - c))
