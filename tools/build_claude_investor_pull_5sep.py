#!/usr/bin/env python3
"""
Builds data/raw/2026-09-05_investor-pull-claude.csv: the first-cheque houses Claude sourced and
verified on 5-Sep-2026 for the two thin clusters, Consumer & Prosumer Software and Online Learning
(docs/prompts/work-order-claude-4sep.md, Part 2).

Columns are a subset of data/investors.csv, in that file's order, so the file loads without a
translation step. Every deal was read on the URL in its row on 5-Sep-2026 and the sentence naming
the fund is in deal_note. Cheque ranges are what the fund publishes on the page in
cheque_range_source; NOT PUBLISHED otherwise. Stage bands are only what the fund states; an empty
cell means the site names no band. No contact details of any kind.

    python3 tools/build_claude_investor_pull_5sep.py
"""
import csv, os

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
PROV = 'CLAUDE PULL 05-Sep-2026, fetch-only (session search budget exhausted); every page named here was read that day. '

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

# ---------------------------------------------------------------- consumer & prosumer software
add(investor_key='nfx', investor_name='NFX', house_type='VC', layer='CALLABLE',
    geographies='U.S., Israel, Latin America and Europe', geographies_source='https://www.nfx.com/about',
    stage_bands='Pre-seed; Seed', cheque_currency='USD', cheque_range_source='NOT PUBLISHED',
    thesis_one_liner='We back exceptional Founders building market-transforming companies.',
    screening_categories=LEARN + '; ' + CONS, subsectors='consumer; marketplaces; AI; network effects',
    recent_deal_1_company='Gizmo', recent_deal_1_date='2026-04',
    recent_deal_1_source_url='https://techcrunch.com/2026/04/15/ai-learning-app-gizmo-levels-up-with-13m-users-and-a-22m-investment/',
    deal_note="TechCrunch, 15-Apr-2026, $22m Series A into Gizmo (AI study app for students, gamified): 'The Series A round was led by Shine Capital, with participation from Ada Ventures, Seek Investments, GSV, and NFX'. NFX led Gizmo's earlier $3.5m seed per the same article. Stage from nfx.com/about: 'We typically invest in seed and pre-seed companies.' No cheque size published.",
    provenance=PROV + 'nfx.com, nfx.com/about, TechCrunch Gizmo article.')

add(investor_key='lerer-hippeau', investor_name='Lerer Hippeau', house_type='VC', layer='CALLABLE',
    geographies='based in New York City', geographies_source='https://www.lererhippeau.com/portfolio',
    stage_bands='Pre-seed; Seed', cheque_currency='USD', cheque_range_source='NOT PUBLISHED',
    thesis_one_liner='Generalist investors, specializing in pre-seed and seed.',
    screening_categories=CONS, subsectors='consumer; digital health; AI; commerce',
    recent_deal_1_company='MOTHER.tech (Degen app)', recent_deal_1_date='2026-05',
    recent_deal_1_source_url='https://techfundingnews.com/mother-tech-15m-seed-gv-lerer-hippeau-degen-ai-app/',
    deal_note="Tech Funding News, 5-May-2026: 'MOTHER.tech, a creative studio based in Brooklyn, has raised $15 million in seed funding' and 'Investors include GV, Lerer Hippeau Ventures, BoxGroup, and Shine Capital.' Degen is a one-tap consumer AI app for images, videos and memes. Participation, not lead; the site states pre-seed and seed as its specialism.",
    provenance=PROV + 'lererhippeau.com, lererhippeau.com/portfolio, Tech Funding News article.')

add(investor_key='boxgroup', investor_name='BoxGroup', house_type='VC', layer='CALLABLE',
    geographies='Built in NYC + SF; funds companies anywhere', geographies_source='https://www.boxgroup.com/about',
    stage_bands='Pre-seed; Seed; Series A', first_cheque_high_m='1', cheque_currency='USD',
    cheque_range_source='https://www.boxgroup.com/about',
    thesis_one_liner='The Earliest Investor: we invest as early as the pre-seed round and as late as Series A.',
    screening_categories=CONS, subsectors='consumer; marketplaces; developer tools; frontier',
    recent_deal_1_company='MOTHER.tech (Degen app)', recent_deal_1_date='2026-05',
    recent_deal_1_source_url='https://techfundingnews.com/mother-tech-15m-seed-gv-lerer-hippeau-degen-ai-app/',
    recent_deal_2_company='Era Computer', recent_deal_2_date='2026-04',
    recent_deal_2_source_url='https://techcrunch.com/2026/04/23/era-computer-raises-11m-to-build-a-software-platform-for-ai-gadgets/',
    deal_note="Tech Funding News, 5-May-2026, $15m seed: 'Investors include GV, Lerer Hippeau Ventures, BoxGroup, and Shine Capital.' Second deal shows it co-leads: TechCrunch, 23-Apr-2026, Era Computer '$9 million seed round (led by Abstract Ventures and BoxGroup)', a device software platform rather than a consumer app. Cheque from boxgroup.com/about: 'Investing up to $1M'; low end not published.",
    provenance=PROV + 'boxgroup.com/about, boxgroup.com/portfolio, Tech Funding News, TechCrunch Era article.')

add(investor_key='betaworks', investor_name='Betaworks', house_type='VC', layer='CALLABLE',
    geographies='companies based anywhere in the world; in-person time in NYC required for Camp', geographies_source='https://www.betaworks.com/camp/application',
    stage_bands='Pre-seed; Seed', first_cheque_high_m='0.25', cheque_currency='USD',
    cheque_range_source='https://www.betaworks.com/camp/application',
    thesis_one_liner='A thematic investment and in-residence program for startups building in frontier technologies.',
    screening_categories=CONS, subsectors='AI; agents; interfaces; native applications',
    recent_deal_1_company='Marker', recent_deal_1_date='2026-07',
    recent_deal_1_source_url='https://pulse2.com/marker-raises-13-million-seed-funding-to-build-an-ai-native-word-processor/',
    deal_note="Pulse 2.0, 10-Jul-2026: 'Index Ventures has led a $13 million seed round for Marker, a London-based startup developing an AI-native word processor ... The funding round includes participation from LocalGlobe, Betaworks, Radical Ventures, Tiny VC and Otherwise Fund'. Cheque from the Camp application page: 'Betaworks and our syndicate partners will each invest up to $250k for a total of up to $500k investment per team'; the Betaworks half is recorded. Stage: the Camp page describes Betaworks as 'a pre-seed and seed stage investor'.",
    provenance=PROV + 'betaworks.com, betaworks.com/camp, betaworks.com/camp/application, Pulse 2.0 article.')

add(investor_key='homebrew', investor_name='Homebrew', house_type='VC', layer='CALLABLE',
    geographies='North or South America, initially targeting markets in those geographies', geographies_source='https://www.homebrew.co/',
    stage_bands='Pre-seed; Seed', first_cheque_low_m='0.1', first_cheque_high_m='0.5', cheque_currency='USD',
    cheque_range_source='https://www.homebrew.co/',
    thesis_one_liner='Capital, counsel and commitment for mission-driven founders reimagining the world we live in.',
    screening_categories=LEARN + '; ' + CONS, subsectors='mission-driven founders; consumer; AI',
    recent_deal_1_company='Oboe', recent_deal_1_date='2025-09',
    recent_deal_1_source_url='https://techcrunch.com/2025/09/10/after-selling-to-spotify-anchors-co-founders-are-back-with-oboe-an-ai-powered-app-for-learning/',
    deal_note="TechCrunch, 10-Sep-2025: 'The startup's $4 million seed round was led by Eniac Ventures ... The round also includes investment from Haystack, Factorial Capital, Homebrew, Offline Ventures'. Oboe is a consumer AI learning app with a free tier, $15 and $40 a month plans. Cheque from homebrew.co: '90% of what we do is pre-seed/seed investments of between $100k and $500k.' Deal sits exactly twelve months back on 5-Sep-2026.",
    provenance=PROV + 'homebrew.co, homebrew.co blog post on Oboe, TechCrunch Oboe article.')

add(investor_key='haystack', investor_name='Haystack', house_type='VC', layer='CALLABLE',
    geographies='Silicon Valley and beyond', geographies_source='https://haystack.vc/about-us',
    stage_bands='', first_cheque_low_m='1', first_cheque_high_m='3', cheque_currency='USD',
    cheque_range_source='https://haystack.vc/',
    thesis_one_liner='Backing outlier founders at the earliest stages.',
    screening_categories=LEARN + '; ' + CONS, subsectors='software; consumer; AI',
    recent_deal_1_company='Oboe', recent_deal_1_date='2025-09',
    recent_deal_1_source_url='https://techcrunch.com/2025/09/10/after-selling-to-spotify-anchors-co-founders-are-back-with-oboe-an-ai-powered-app-for-learning/',
    deal_note="TechCrunch, 10-Sep-2025, $4m seed led by Eniac with 'investment from Haystack, Factorial Capital, Homebrew'. Cheque from haystack.vc: 'We typically invest $1M to $3M in initial rounds and can lead or participate.' STAGE BAND LEFT EMPTY: the site says 'earliest stages' and 'initial rounds', not a named band, and silence is not a claim; the render gate will hold this row until a band is stated or ruled.",
    provenance=PROV + 'haystack.vc, haystack.vc/about-us, TechCrunch Oboe article.')

add(investor_key='eniac-ventures', investor_name='Eniac Ventures', house_type='VC', layer='CALLABLE',
    geographies='NYC', geographies_source='https://eniac.vc/',
    stage_bands='Seed', cheque_currency='USD', cheque_range_source='NOT PUBLISHED',
    thesis_one_liner='We partner with founders from 0 to 1.',
    screening_categories=LEARN + '; ' + CONS, subsectors='seed; 0 to 1; AI; consumer',
    recent_deal_1_company='Oboe', recent_deal_1_date='2025-09',
    recent_deal_1_source_url='https://techcrunch.com/2025/09/10/after-selling-to-spotify-anchors-co-founders-are-back-with-oboe-an-ai-powered-app-for-learning/',
    recent_deal_2_company='Kin Health', recent_deal_2_date='2026-05',
    recent_deal_2_source_url='https://techcrunch.com/2026/05/18/kin-health-raises-9m-to-build-an-ai-notetaker-for-patients/',
    deal_note="TechCrunch, 10-Sep-2025: 'The startup's $4 million seed round was led by Eniac Ventures, the VC firm that led Anchor's seed.' TechCrunch, 18-May-2026, Kin Health $9m seed led by Maveron 'with participation from Town Hall Ventures, Eniac Ventures, Flex Capital, Foundry Square Capital, Pear VC, and The Family Fund'. Stage from eniac.vc: 'from 0 to 1' with the site's seed positioning; no cheque size published.",
    provenance=PROV + 'eniac.vc, eniac.vc/stories, TechCrunch Oboe and Kin Health articles.')

add(investor_key='maveron', investor_name='Maveron', house_type='VC', layer='CALLABLE',
    geographies='', geographies_source='NOT PUBLISHED',
    stage_bands='Seed', cheque_currency='USD', cheque_range_source='NOT PUBLISHED',
    thesis_one_liner='A consumer-centric venture capital firm focused on partnering with world-class entrepreneurs that change the way we live.',
    screening_categories=CONS, subsectors='consumer brands; healthcare; commerce; consumer behavior change',
    recent_deal_1_company='Kin Health', recent_deal_1_date='2026-05',
    recent_deal_1_source_url='https://maveronvc.substack.com/p/maveron-leads-9m-seed-round-in-kin',
    recent_deal_2_company='Kin Health', recent_deal_2_date='2026-05',
    recent_deal_2_source_url='https://techcrunch.com/2026/05/18/kin-health-raises-9m-to-build-an-ai-notetaker-for-patients/',
    deal_note="Maveron's own post, 21-May-2026: 'Maveron have led a $9 million seed round in Kin Health', a free consumer app that records the doctor visit and writes a plain-language summary. TechCrunch, 18-May-2026: 'the startup has raised $9 million in a seed funding round led by Maveron.' Stage band 'Seed' is what the fund states in its own words about this round ('led a ... seed round'); maveron.com describes 'early-stage investing in consumer brands' without naming bands. No cheque size or geography published.",
    provenance=PROV + 'maveron.com, maveronvc.substack.com Kin post, TechCrunch Kin Health article.')

add(investor_key='pear-vc', investor_name='Pear VC', house_type='VC', layer='CALLABLE',
    geographies='San Francisco and Menlo Park, California (offices)', geographies_source='https://pear.vc/how-we-invest',
    stage_bands='Pre-seed; Seed', first_cheque_low_m='0.25', first_cheque_high_m='6', cheque_currency='USD',
    cheque_range_source='https://pear.vc/how-we-invest',
    thesis_one_liner="We're seed specialists that partner with founders at the earliest stages to turn great ideas into category-defining companies.",
    screening_categories=CONS, subsectors='seed specialists; pre-seed (PearX); company builders',
    recent_deal_1_company='Kin Health', recent_deal_1_date='2026-05',
    recent_deal_1_source_url='https://techcrunch.com/2026/05/18/kin-health-raises-9m-to-build-an-ai-notetaker-for-patients/',
    deal_note="TechCrunch, 18-May-2026, $9m seed led by Maveron: 'The funding round also saw participation from Town Hall Ventures, Eniac Ventures, Flex Capital, Foundry Square Capital, Pear VC, and The Family Fund.' Cheque from pear.vc/how-we-invest: 'We write early checks that range from $250K to $6M', pre-seed $250K to $2M, seed $1M to $6M.",
    provenance=PROV + 'pear.vc, pear.vc/how-we-invest, pear.vc/news, TechCrunch Kin Health article.')

add(investor_key='nextview-ventures', investor_name='NextView Ventures', house_type='VC', layer='CALLABLE',
    geographies='North America; offices in San Francisco, New York, and Boston', geographies_source='https://nextview.vc/approach/',
    stage_bands='Pre-seed; Seed', first_cheque_low_m='0.25', first_cheque_high_m='4', cheque_currency='USD',
    cheque_range_source='https://nextview.vc/approach/',
    thesis_one_liner='We lead rounds for pre-traction companies that leverage AI and software to tackle mass market human problems.',
    screening_categories=CONS, subsectors='mass market end users; AI and software; pre-traction',
    recent_deal_1_company='Fambot', recent_deal_1_date='2026-09',
    recent_deal_1_source_url='https://techcrunch.com/2026/09/01/fambot-introduces-an-ai-chief-of-staff-for-families/',
    deal_note="TechCrunch, 1-Sep-2026: 'The startup is backed by $3.5 million in pre-seed funding, co-led by NextView Ventures and Baukunst'. Fambot is a consumer AI assistant for family logistics. Cheque from nextview.vc/approach: 'Our initial investments range from $250K to $4M'.",
    provenance=PROV + 'nextview.vc, nextview.vc/approach/, nextview.vc/press/, TechCrunch Fambot article.')

add(investor_key='baukunst', investor_name='Baukunst', house_type='VC', layer='CALLABLE',
    geographies='', geographies_source='NOT PUBLISHED',
    stage_bands='Pre-seed', cheque_currency='USD', cheque_range_source='NOT PUBLISHED',
    thesis_one_liner='A collective of creative technologists advancing the art of building; we lead pre-seed rounds and often invest the full round ourselves.',
    screening_categories=CONS, subsectors='creative technologists; technology and design frontiers; pre-seed',
    recent_deal_1_company='Fambot', recent_deal_1_date='2026-09',
    recent_deal_1_source_url='https://techcrunch.com/2026/09/01/fambot-introduces-an-ai-chief-of-staff-for-families/',
    deal_note="TechCrunch, 1-Sep-2026: '$3.5 million in pre-seed funding, co-led by NextView Ventures and Baukunst'. baukunst.co/investments lists Fambot as 'Pre-seed lead' and states: 'We lead pre-seed rounds out of our inaugural $100M fund and often invest the full round ourselves.' No cheque size or geography published.",
    provenance=PROV + 'baukunst.co, baukunst.co/investments, TechCrunch Fambot article.')

add(investor_key='y-combinator', investor_name='Y Combinator', house_type='Accelerator', layer='CALLABLE',
    geographies='', geographies_source='NOT PUBLISHED',
    stage_bands='', first_cheque_low_m='0.5', first_cheque_high_m='0.5', cheque_currency='USD',
    cheque_range_source='https://www.ycombinator.com/deal',
    thesis_one_liner='Make something people want.',
    screening_categories=LEARN + '; ' + CONS, subsectors='consumer; education; AI',
    recent_deal_1_company='Doomersion', recent_deal_1_date='2026-01',
    recent_deal_1_source_url='https://www.ycombinator.com/companies/doomersion',
    recent_deal_2_company='Wondering', recent_deal_2_date='2026-06',
    recent_deal_2_source_url='https://www.ycombinator.com/companies/wondering',
    deal_note="Standard deal from ycombinator.com/deal: 'We invest $125,000 on a post-money SAFE in return for 7% of your company' and 'We invest $375,000 on an uncapped SAFE with a Most Favored Nation (MFN) provision', $500,000 in total. Doomersion, batch 'Winter 2026', 'Doomscroll to learn languages', a consumer language app founded 2025 in San Francisco; Wondering, batch 'Summer 2026', a consumer learning app. DATES ARE BATCH LABELS mapped to the batch's first month, not calendar deal dates. STAGE BAND LEFT EMPTY: ycombinator.com/about says companies 'arrive at YC at all different stages'. Wondering is one of our own fixtures, so YC is presumably already on its cap table.",
    provenance=PROV + 'ycombinator.com/deal, ycombinator.com/about, company pages for Doomersion and Wondering.')

add(investor_key='techstars', investor_name='Techstars', house_type='Accelerator', layer='CALLABLE',
    geographies='Programs in Boulder, Boston, Chicago, New York City, Columbus, London, Tokyo, Baltimore, Alabama and Anywhere (remote)', geographies_source='https://www.techstars.com/',
    stage_bands='', first_cheque_low_m='0.22', first_cheque_high_m='0.22', cheque_currency='USD',
    cheque_range_source='https://www.techstars.com/newsroom/techstars-tokyo-accelerator-announces-class-of-2026',
    thesis_one_liner='Three months of intensive, mentorship-driven support, connecting you with the specialized expertise, global community, and capital you need to grow faster.',
    screening_categories=CONS, subsectors='AI; healthtech; mental wellness; consumer',
    recent_deal_1_company='Wiillow', recent_deal_1_date='2026-08',
    recent_deal_1_source_url='https://www.techstars.com/newsroom/techstars-tokyo-accelerator-announces-class-of-2026',
    deal_note="Techstars newsroom, 18-Aug-2026, Tokyo class of 2026: 'every company gets $220K in capital, three months of relentless hands-on mentorship'; Wiillow is 'AI-driven personalized wellness and mental health platform delivering tailored digital support tools.' STAGE BAND LEFT EMPTY: the accelerators page names no band. The $220K is the programme's published standard cheque.",
    provenance=PROV + 'techstars.com, techstars.com/accelerators, techstars.com/newsroom Tokyo class release.')

add(investor_key='shine-capital', investor_name='Shine Capital', house_type='VC', layer='EVIDENCE',
    geographies='', geographies_source='NOT PUBLISHED', stage_bands='', cheque_currency='USD', cheque_range_source='NOT PUBLISHED',
    thesis_one_liner='', screening_categories=LEARN + '; ' + CONS, subsectors='',
    recent_deal_1_company='Gizmo', recent_deal_1_date='2026-04',
    recent_deal_1_source_url='https://techcrunch.com/2026/04/15/ai-learning-app-gizmo-levels-up-with-13m-users-and-a-22m-investment/',
    recent_deal_2_company='MOTHER.tech (Degen app)', recent_deal_2_date='2026-05',
    recent_deal_2_source_url='https://techfundingnews.com/mother-tech-15m-seed-gv-lerer-hippeau-degen-ai-app/',
    deal_note="EVIDENCE ONLY BECAUSE THE FUND'S SITE COULD NOT BE READ (shinecapital.com refused every connection on 5-Sep-2026), so stage, cheque, geography and thesis are unverified. The deals are real first-cheque leads: TechCrunch, 15-Apr-2026, Gizmo's $22m Series A 'was led by Shine Capital'; Tech Funding News, 5-May-2026, MOTHER.tech $15m seed, 'Investors include GV, Lerer Hippeau Ventures, BoxGroup, and Shine Capital.' PROMOTE TO CALLABLE the day the site is read.",
    provenance=PROV + 'TechCrunch Gizmo, Tech Funding News MOTHER.tech; shinecapital.com unreachable.')

add(investor_key='tiny-vc', investor_name='Tiny VC', house_type='Micro VC', layer='EVIDENCE',
    geographies='mostly European startups', geographies_source='https://tiny.vc/',
    stage_bands='Pre-seed; Seed', first_cheque_low_m='0.2', first_cheque_high_m='0.25', cheque_currency='USD',
    cheque_range_source='https://tiny.vc/',
    thesis_one_liner='Backing great companies when they are tiny.',
    screening_categories=CONS, subsectors='pre-seed; seed; European startups',
    recent_deal_1_company='Marker', recent_deal_1_date='2026-07',
    recent_deal_1_source_url='https://pulse2.com/marker-raises-13-million-seed-funding-to-build-an-ai-native-word-processor/',
    deal_note="EVIDENCE, NOT CALLABLE, on the fund's own words: 'We don't lead rounds or join boards'. tiny.vc: 'We invest about 200-250K, mostly in European startups at pre-seed and seed stages.' Pulse 2.0, 10-Jul-2026: Marker $13m seed led by Index 'includes participation from LocalGlobe, Betaworks, Radical Ventures, Tiny VC and Otherwise Fund'.",
    provenance=PROV + 'tiny.vc, Pulse 2.0 Marker article.')

# ---------------------------------------------------------------- online learning
add(investor_key='reach-capital', investor_name='Reach Capital', house_type='VC', layer='CALLABLE',
    geographies='', geographies_source='NOT PUBLISHED',
    stage_bands='Pre-seed; Seed; Series A', first_cheque_low_m='0.1', first_cheque_high_m='12', cheque_currency='USD',
    cheque_range_source='https://www.reachcapital.com/about/',
    thesis_one_liner='Our belief is that when people are equipped to grow their skills, nurture relationships, be healthy, and find meaning in what they do, communities thrive.',
    screening_categories=LEARN + '; ' + CONS, subsectors='learning; health; work',
    recent_deal_1_company='Songscription', recent_deal_1_date='2025-11',
    recent_deal_1_source_url='https://www.songscription.ai/blog/seed-funding-announcement',
    recent_deal_2_company='Journify Learning', recent_deal_2_date='2026-05',
    recent_deal_2_source_url='https://www.reachcapital.com/resources/news/why-we-invested-in-journify-learning/',
    deal_note="Songscription's own post, 13-Nov-2025: 'Songscription has raised a $5M round led by Reach Capital', with Emerge Capital, 10x Founders and Dent Capital; a subscription tool for learners and musicians. Second deal is a school-facing seed (Journify Learning, May-2026) recorded for activity, not consumer fit. From reachcapital.com/about: 'typically makes initial investments in Pre-seed, Seed, and Series A rounds' and cheque 'typically ranges from $100K for Pre-seed to upwards of $12 million for later-stage startups'; the $12m top end is a later-stage figure, not a first cheque.",
    provenance=PROV + 'reachcapital.com, reachcapital.com/about/, reachcapital.com/companies/, songscription.ai blog, Reach news post on Journify.')

add(investor_key='emerge-capital', investor_name='Emerge', house_type='VC', layer='CALLABLE',
    geographies='Europe (the first specialist future of work and learning investor in Europe)', geographies_source='https://emergecapital.vc/aboutus/',
    stage_bands='Pre-seed; Seed', first_cheque_low_m='0.5', first_cheque_high_m='2.5', cheque_currency='USD',
    cheque_range_source='https://emergecapital.vc/',
    thesis_one_liner='First money in for founders building the future of human capital development.',
    screening_categories=LEARN, subsectors='human capital development; future of work; learning; skills',
    recent_deal_1_company='Songscription', recent_deal_1_date='2025-11',
    recent_deal_1_source_url='https://emergecapital.vc/songscription-raises-5m-to-become-the-shazam-for-sheet-music/',
    recent_deal_2_company='MyEdSpace', recent_deal_2_date='2025-09',
    recent_deal_2_source_url='https://emergecapital.vc/myedspace-raises-15m-series-a-to-stream-the-worlds-best-teachers-to-every-student/',
    deal_note="Emerge's own post, 13-Nov-2025: 'We're delighted to announce our investment in Songscription', a '$5M seed round led by Reach Capital alongside 10x Founders and Dent Capital'. Emerge's own post, 29-Sep-2025: 'MyEdSpace has raised $15M (GBP11.9M) in a Series A led by White Star Capital, with participation from Educapital, Active Partners, Coalition Capital, and us'; MyEdSpace streams live lessons to students at home who pay per hour. Cheque from emergecapital.vc: 'Early stage investment $500k-$2.5M'; stage 'Pre-seed and seed founders'.",
    provenance=PROV + 'emerge.education (redirects to emergecapital.vc), emergecapital.vc, /aboutus/, /portfolio/, two deal posts.')

add(investor_key='educapital', investor_name='Educapital', house_type='VC', layer='CALLABLE',
    geographies='Innovative European companies', geographies_source='https://www.educapitalvc.com/',
    stage_bands='Seed; Series A; Series B', first_cheque_high_m='10', cheque_currency='EUR',
    cheque_range_source='https://www.educapitalvc.com/',
    thesis_one_liner='Entrepreneurs shaping the future of education and future of work, with a high potential to scale and become global category leaders.',
    screening_categories=LEARN + '; ' + CONS, subsectors='K12; higher education; lifelong learning; skills and training',
    recent_deal_1_company='Vocal Image', recent_deal_1_date='2025-09',
    recent_deal_1_source_url='https://www.frenchweb.fr/vocal-image-leve-33-millions-deuros-pour-ameliorer-la-prise-de-parole-en-public-grace-a-lia/456791',
    recent_deal_2_company='Rocapine', recent_deal_2_date='2026-06',
    recent_deal_2_source_url='https://www.eu-startups.com/2026/06/paris-based-rocapine-raises-e11-2-million-to-scale-wellness-apps-that-hold-instead-of-hook/',
    deal_note="FrenchWeb, 2-Sep-2025: 'Vocal Image a annonce une levee de 3,3 millions d'euros en seed. Le tour a ete mene par Educapital'; a consumer voice-coaching app with about 50,000 paying users. EU-Startups, 16-Jun-2026: Rocapine 'announced a EUR11.2 million ($13 million) Series A round' led by Educapital; consumer-paid wellness apps. Educapital's own posts on both are on educapitalvc.com/news. From educapitalvc.com: 'From late seed to Series B' and 'Up to EUR10M per investment'; the low end is not published.",
    provenance=PROV + 'educapital.fr (redirects to educapitalvc.com), educapitalvc.com, /about-us, /news, FrenchWeb, EU-Startups.')

add(investor_key='magnify-ventures', investor_name='Magnify Ventures', house_type='VC', layer='CALLABLE',
    geographies='', geographies_source='NOT PUBLISHED',
    stage_bands='Pre-seed; Seed', first_cheque_low_m='0.25', first_cheque_high_m='2', cheque_currency='USD',
    cheque_range_source='https://www.magnify.vc/',
    thesis_one_liner='The fundamentals of family life are enduring; the systems around it are being rebuilt; we back the founders of the new care economy.',
    screening_categories=CONS, subsectors='family mental health; AI for the home; prenatal and maternal care; care economy',
    recent_deal_1_company='Joy', recent_deal_1_date='2025-11',
    recent_deal_1_source_url='https://magnifyvc.medium.com/ai-parenting-app-joy-raises-14m-to-redefine-family-support-a44446270d5c',
    deal_note="Magnify's own post, 14-Nov-2025: 'Joy Parenting Club, a San Francisco-based startup, has raised a $14 million Series A, co-led by Raga Partners and Forerunner Ventures', with Magnify investing; a consumer parenting app 'At $12 per month' with 50,000 paying members. Participation in a Series A by a pre-seed and seed fund: from magnify.vc, 'We invest at the pre-seed and seed stage companies, typically investing $250K to $2M.'",
    provenance=PROV + 'magnify.vc, magnify.vc/news, magnify.vc/portfolio, magnifyvc.medium.com Joy post.')

out = 'data/raw/2026-09-05_investor-pull-claude.csv'
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=COLS, lineterminator='\n')
    w.writeheader(); w.writerows(rows)
c = sum('CALLABLE' in r['layer'] for r in rows)
print('%d houses -> %s (%d CALLABLE, %d EVIDENCE)' % (len(rows), out, c, len(rows) - c))
for r in rows:
    print('  %-20s %-9s stage=%-26s cheque=%s-%s %s  deal=%s %s' % (r['investor_key'], r['layer'], r['stage_bands'] or '(empty)', r['first_cheque_low_m'] or '-', r['first_cheque_high_m'] or '-', r['cheque_currency'], r['recent_deal_1_date'], r['recent_deal_1_company']))
