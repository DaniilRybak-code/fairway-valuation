# -*- coding: utf-8 -*-
"""Triage 20 real Product Hunt companies through the engine, 31-Aug-2026.

REAL COMPANIES ONLY. Every one is taken from the Product Hunt monthly leaderboards for May, June
and July 2026, with the tagline as published. Nothing here is invented, per the standing rule.

WHAT A TRIAGE IS FOR. Not to prove the engine works. To find where it does not, at a rate of twenty
founders at a time, so the failures arrive here rather than in front of a paying one.
"""
import os, sys, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'selector'))
import match_reference as M

P = lambda **k: k
CASES = [
 ('fuzzy-ai', 'Warms prospects with research and touches before an outbound approach', P(
   archetype='Marketing & Customer Engagement', industry='Horizontal', function='Sales & Marketing',
   buyer='SMB', gtm_motion='PLG', revenue_model='SUBSCRIPTION', product_role='WORKFLOW',
   ai_stance='AI_NATIVE',
   product_tags='Outbound Prospecting|Lead Warming|Sales Intelligence|Buyer Signals|Email Sequencing|Account Research')),
 ('wispr-flow', 'Voice dictation that replaces typing across every desktop app', P(
   archetype='Consumer & Prosumer Software', industry='Horizontal', function='Productivity',
   buyer='PROSUMER', gtm_motion='PLG', revenue_model='SUBSCRIPTION', product_role='WORKFLOW',
   ai_stance='AI_NATIVE',
   product_tags='Voice Dictation|Speech To Text|Desktop Productivity|Transcription|Hands Free Input|Personal Software')),
 ('fypro', 'Turns a creator TikTok following into paying customers', P(
   archetype='Creator & Community Monetisation', archetype_secondary='Consumer & Prosumer Software',
   industry='Media & Entertainment', function='Sales & Marketing', buyer='PROSUMER',
   gtm_motion='PLG', revenue_model='TAKE_RATE', product_role='AGGREGATOR', ai_stance='AI_EMBEDDED',
   product_tags='Creator Monetisation|Social Commerce|TikTok Funnel|Fan Conversion|Link In Bio|Digital Products')),
 ('velo', 'Video infrastructure that turns voice and screen into training and sales content', P(
   archetype='Marketing & Customer Engagement', industry='Horizontal', function='Sales & Marketing',
   buyer='SMB', gtm_motion='PLG', revenue_model='SUBSCRIPTION', product_role='WORKFLOW',
   ai_stance='AI_NATIVE',
   product_tags='AI Video|Screen Recording|Sales Enablement|Product Demos|Async Video|Training Content')),
 ('exploreyc', 'Open-source API serving structured data on Y Combinator and a16z companies', P(
   archetype='Data, AI & Developer Tools', archetype_secondary='Financial Data & Index',
   industry='Financial Services', function='Data & Analytics', buyer='DEVELOPER',
   gtm_motion='PLG', revenue_model='USAGE', product_role='INFRA_LAYER', ai_stance='AI_NEUTRAL',
   product_tags='Company Data API|Startup Database|Venture Data|Structured Data|Open Source API|Firmographics')),
 ('lev8', 'Finds, researches and reaches the right people for a sales team', P(
   archetype='Marketing & Customer Engagement', industry='Horizontal', function='Sales & Marketing',
   buyer='SMB', gtm_motion='PLG', revenue_model='SUBSCRIPTION', product_role='WORKFLOW',
   ai_stance='AI_NATIVE',
   product_tags='Contact Enrichment|Prospect Research|Sales Outreach|Lead Database|Multichannel Sequences|Buyer Intent')),
 ('prefactor', 'Evaluates AI agents in real time and pinpoints where they fail', P(
   archetype='Data, AI & Developer Tools', industry='Horizontal', function='Engineering',
   buyer='DEVELOPER', gtm_motion='PLG', revenue_model='USAGE', product_role='INFRA_LAYER',
   ai_stance='AI_NATIVE',
   product_tags='Agent Evaluation|LLM Observability|Prompt Testing|Model Monitoring|Trace Analysis|Regression Testing')),
 ('viktor', 'An AI coworker that completes knowledge work end to end', P(
   archetype='Business Applications', industry='Horizontal', function='Productivity',
   buyer='SMB', gtm_motion='PLG', revenue_model='SUBSCRIPTION', product_role='WORKFLOW',
   ai_stance='AI_NATIVE',
   product_tags='AI Agent|Knowledge Work Automation|Task Execution|Digital Worker|Workflow Automation|Autonomous Assistant')),
 ('v2fun', 'Generates 3D characters with 8K textures and AI motion capture', P(
   archetype='Design & Engineering', industry='Media & Entertainment', function='Design',
   buyer='PROSUMER', gtm_motion='PLG', revenue_model='SUBSCRIPTION', product_role='WORKFLOW',
   ai_stance='AI_NATIVE',
   product_tags='3D Character Generation|Motion Capture|Game Assets|Texture Generation|Avatar Creation|Content Pipeline')),
 ('prelint', 'Stops AI-written code drifting from the product it was meant to build', P(
   archetype='Data, AI & Developer Tools', industry='Horizontal', function='Engineering',
   buyer='DEVELOPER', gtm_motion='PLG', revenue_model='SUBSCRIPTION', product_role='WORKFLOW',
   ai_stance='AI_NATIVE',
   product_tags='Code Review|Static Analysis|AI Code Quality|Product Drift|Developer Guardrails|CI Checks')),
 ('osaurus', 'Open-source agents that run entirely locally on a Mac', P(
   archetype='Data, AI & Developer Tools', industry='Horizontal', function='Engineering',
   buyer='DEVELOPER', gtm_motion='PLG', revenue_model='SUBSCRIPTION', product_role='INFRA_LAYER',
   ai_stance='AI_NATIVE',
   product_tags='Local LLM|On Device Agents|Open Source Runtime|Privacy First AI|Mac Native|Offline Inference')),
 ('storeclaw', 'Agents that run merchandising and pricing to grow store profit', P(
   archetype='Commerce & Payments Software', archetype_secondary='Commerce Enablement & Fulfilment',
   industry='Retail & E-commerce', function='Commerce & Fulfilment', buyer='SMB',
   gtm_motion='PLG', revenue_model='SUBSCRIPTION', product_role='WORKFLOW', ai_stance='AI_NATIVE',
   product_tags='Ecommerce Automation|Merchandising|Pricing Optimisation|Marketplace Listings|Store Operations|Seller Tools')),
 ('pollyreach', 'Gives an AI agent a real phone number and voice to make calls', P(
   archetype='Communications & Collaboration', industry='Horizontal', function='Sales & Marketing',
   buyer='SMB', gtm_motion='PLG', revenue_model='USAGE', product_role='INFRA_LAYER',
   ai_stance='AI_NATIVE',
   product_tags='Voice AI|Outbound Calling|Telephony API|Conversational Agents|Call Automation|Speech Synthesis')),
 ('brew', 'Design-led email marketing built the way a design tool works', P(
   archetype='Marketing & Customer Engagement', industry='Horizontal', function='Sales & Marketing',
   buyer='SMB', gtm_motion='PLG', revenue_model='SUBSCRIPTION', product_role='WORKFLOW',
   ai_stance='AI_EMBEDDED',
   product_tags='Email Marketing|Campaign Design|Template Builder|Lifecycle Messaging|Newsletter|Audience Segmentation')),
 ('rankspot', 'SEO blog content generated from deep competitor intelligence', P(
   archetype='Marketing & Customer Engagement', industry='Horizontal', function='Sales & Marketing',
   buyer='SMB', gtm_motion='PLG', revenue_model='SUBSCRIPTION', product_role='WORKFLOW',
   ai_stance='AI_NATIVE',
   product_tags='SEO Content|Keyword Research|Competitor Analysis|Content Generation|Rank Tracking|Organic Growth')),
 ('own-page', 'Personal website builder using bento tiles', P(
   archetype='Consumer & Prosumer Software', industry='Horizontal', function='Design',
   buyer='CONSUMER', gtm_motion='PLG', revenue_model='SUBSCRIPTION', product_role='WORKFLOW',
   ai_stance='AI_NEUTRAL',
   product_tags='Website Builder|Personal Page|Link In Bio|Portfolio|Templates|No Code')),
 ('spellar', 'Meeting assistant that remembers across meetings', P(
   archetype='Communications & Collaboration', industry='Horizontal', function='Productivity',
   buyer='SMB', gtm_motion='PLG', revenue_model='SUBSCRIPTION', product_role='WORKFLOW',
   ai_stance='AI_NATIVE',
   product_tags='Meeting Notes|Transcription|Cross Meeting Memory|Action Items|Recording|Team Knowledge')),
 ('socleads', 'Scrapes contact details from social platforms and maps by location', P(
   archetype='Marketing & Customer Engagement', industry='Horizontal', function='Sales & Marketing',
   buyer='SMB', gtm_motion='PLG', revenue_model='SUBSCRIPTION', product_role='AGGREGATOR',
   ai_stance='AI_NEUTRAL',
   product_tags='Lead Scraping|Contact Data|Local Business Data|Email Finder|Social Data|List Building')),
 ('naptick', 'AI sleep companion that helps people fall asleep', P(
   archetype='Consumer Subscription', archetype_secondary='Consumer & Prosumer Software',
   industry='Healthcare & Life Sciences', function='Consumer Wellbeing', buyer='CONSUMER',
   gtm_motion='PAID_ACQUISITION', revenue_model='SUBSCRIPTION', product_role='WORKFLOW',
   ai_stance='AI_NATIVE',
   product_tags='Sleep|Consumer Health App|Wellness Subscription|Guided Audio|Habit Tracking|Mental Wellbeing')),
 ('tycoon-ai', 'Runs a one-person company entirely on AI agents', P(
   archetype='Business Applications', industry='Horizontal', function='Operations',
   buyer='SMB', gtm_motion='PLG', revenue_model='SUBSCRIPTION', product_role='WORKFLOW',
   ai_stance='AI_NATIVE',
   product_tags='Solo Founder Tools|Business Automation|AI Agents|Back Office|Operations Automation|Micro SaaS')),
]

def main():
    rows, empty, thin, noband = [], [], [], []
    for key, label, prof in CASES:
        core, sec, ltier = M.peer_groups(prof, M.listed)
        which, _r = M.denominator(prof, core)
        lrange = M.group_range(prof, core, which, ltier)
        picked, months, ptier = M.select_private(prof, M.private)
        prange = M.private_range(prof, picked, ptier)
        rows.append((key, label, ltier, len(core), len(sec), lrange, ptier, len(picked), prange))
        if not core and not sec: empty.append(key)
        if lrange and lrange.get('n', 0) < 3: thin.append(key + ' listed n=%d' % lrange['n'])
        if prange and prange.get('n', 0) < 3: thin.append(key + ' private n=%d' % prange['n'])
        if not lrange and not prange: noband.append(key)

    def fmt(r):
        return 'none' if not r else '%s to %sx, mid %sx, n=%d' % (r['low'], r['high'], r['mid'], r['n'])
    for k, l, lt, nc, ns, lr, pt, np_, pr in rows:
        print('\n%-12s %s' % (k, l[:64]))
        print('   listed  tier %-8s core %d secondary %d   %s' % (lt, nc, ns, fmt(lr)))
        print('   private tier %-8s names %-11d %s' % (pt, np_, fmt(pr)))
    print('\n' + '=' * 76)
    print('%d companies triaged' % len(rows))
    print('  no listed peers at all      : %d %s' % (len(empty), empty))
    print('  no price on either lane     : %d %s' % (len(noband), noband))
    print('  a range built on fewer than three names: %d' % len(thin))
    for t in thin: print('      ' + t)

if __name__ == '__main__':
    main()
