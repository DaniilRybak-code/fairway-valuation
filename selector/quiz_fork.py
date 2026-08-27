# -*- coding: utf-8 -*-
"""The sector-adaptive quiz: what we ask, and how the answers reach the engine.

Built 27-Aug-2026 from the fork Daniil signed off in Fairway_quiz_fork_and_metrics_26Aug.md, after
he cut it down. Everything he dropped is gone from here. Everything he kept is here and maps onto a
field the engine already reads, because that was the rule the whole design turned on:

    ONLY ASK FOR A METRIC WE CAN PUT A PEER NUMBER NEXT TO.

AND A SECOND RULE, from Daniil on 27-Aug: DO NOT ASK FOR A FIELD THAT DOES NOT IMPACT THE VALUATION.
"We should not be asking for the sake of asking." Applied literally, question by question:

  DROPPED, because he said they do not move the range:  seats versus usage pricing, take rate
  (marketplace and payments), cohort retention, originations, loss rate, ARPU, churn, content cost,
  orders per customer, contribution margin per order, and TOTAL PAYMENT VOLUME.

  GROSS MARGIN IS NOW ASKED IN ONE FORK ONLY, e-commerce. He endorsed it there and it earns its
  place: across our listed consumer set the revenue multiple moves 0.9x to 2.8x between the lowest
  and highest margin quartile while the gross-profit multiple sits at 3.6x and 3.1x. For software the
  same measurement gives 3.4x against 5.0x on revenue, a much smaller effect, and he explicitly said
  margin does not enter the valuation for an AI-native company. So it comes out of every other fork.
  The peer-side column stays populated everywhere, and `denominator()` still switches to gross profit
  on a wide peer-group margin spread without needing the founder to answer anything.

  VOLUME (GMV, GTV) IS OPTIONAL AND LABELLED AS A CROSS-CHECK, never a valuation input. TPV is gone
  altogether on his instruction. Recording one dissent and then dropping it: a founder who says
  "$40m revenue" when they mean $40m of processed volume is out by about a hundred times, and holding
  both numbers is the only way to catch that. His call stands.

  NRR STAYS, and that one is mine rather than his. He asked to enrich the database, not to ask the
  founder. I have kept the question because it is the largest gap we can measure: across the 51
  listed software names that disclose it, the top quarter trades at 11.1x forward revenue and the
  bottom at 2.9x. It is optional. Say the word and it goes.

A question the peer set cannot answer makes the reveal look thinner, not richer. So every field
below names the peer-side column it is compared against, and `unbacked()` fails loudly if a question
is ever added without one.

TWO ANSWERS DO REAL WORK IN THE ENGINE TODAY:
  growth_pct   places the founder in a growth band, which gates the private comparables and drives
               the regression method. Required.
  gross_margin decides whether the reveal leads on revenue or gross profit. On the consumer set the
               revenue multiple moves 0.9x to 2.8x across margin quartiles while the gross-profit
               multiple sits at 3.6x and 3.1x, so for a consumer founder this is not a nicety.

The rest are stored, shown next to the peer figure, and will earn their keep as coverage grows.
"""

CORE = [
    dict(key='what_it_does', label='What does the company do?', kind='text',
         maps_to='profile.product_tags via the profiler', required=True, peer_field='product_tags'),
    dict(key='website', label='Website', kind='url', required=True,
         maps_to='profiler input', peer_field=''),
    dict(key='country', label='Where are you based?', kind='choice', required=True,
         maps_to='profile.country', peer_field='country'),
    dict(key='stage', label='Stage and last round', kind='choice', required=True,
         maps_to='context only', peer_field=''),
    # Context only, and marked so the guard below does not treat it as an unbacked metric. It is
    # not compared against anything; it turns the multiple into a pre-money the founder can use.
    dict(key='raise_amount', label='How much are you raising?', kind='money', required=False,
         maps_to='context only', peer_field='', context_only=True),
    dict(key='growth_pct', label='How fast did revenue grow over the last twelve months?',
         kind='percent', required=True, maps_to='profile.growth',
         peer_field='revenue_growth_ntm_pct / growth_pct_at_round',
         why='Places you in a growth band, which decides which private rounds you are compared '
             'against and whether the regression method can run at all.'),
]

# Every fork keys off the archetype the profiler assigns, so the founder never picks from a menu.
FORKS = {
 'software': dict(
    archetypes=('Business Applications', 'Vertical Software', 'Cybersecurity', 'Data, AI & Developer Tools',
                'Cloud & Infrastructure', 'Design & Engineering', 'Communications & Collaboration',
                'Consumer & Prosumer Software', 'Software Consolidator'),
    questions=[
      dict(key='arr', label='What is your ARR?', kind='money', required=True,
           maps_to='profile.revenue', peer_field='revenue_musd', basis='ARR',
           why='Compared against 25 private rounds priced on contracted ARR and 6 on a run rate. '
               'We do not ask which yours is: nothing is perfectly comparable and that is fine.'),
      dict(key='nrr_pct', label='Net revenue retention, if you measure it', kind='percent', required=False,
           maps_to='profile.nrr', peer_field='nrr_pct',
           why='51 of 165 listed software names disclose it. The top quarter trades at 11.1x '
               'forward revenue and the bottom at 2.9x, which is the largest gap we can measure.'),
    ]),
 'marketplace': dict(
    archetypes=('Third-Party Marketplace', 'Classifieds & Listings', 'Freelance & Services Marketplace',
                'Travel Booking & OTA', 'Gaming & Virtual Economy'),
    questions=[
      dict(key='gmv', label='Gross merchandise value, if you have it to hand', kind='money',
           required=False, maps_to='profile.volume', peer_field='gmv_musd / volume_musd',
           why='NOT a valuation input. We price on net revenue. This is a cross-check: a founder '
               'who gives GMV when they mean revenue is out by roughly the take rate, and holding '
               'both numbers is the only way to catch it.'),
      dict(key='net_revenue', label='Net revenue over the same period', kind='money', required=True,
           maps_to='profile.revenue', peer_field='revenue_musd', basis='NET_REVENUE',
           why='The figure we actually price on.'),
    ]),
 'ecommerce': dict(
    archetypes=('Consumer Brand', 'Owned-Inventory Retail', 'Commerce Enablement & Fulfilment'),
    questions=[
      dict(key='net_revenue', label='Net revenue over the last twelve months', kind='money',
           required=True, maps_to='profile.revenue', peer_field='revenue_musd', basis='NET_REVENUE',
           why='NET, not gross or retail sales. This is where OLIPOP went wrong: its $400m is gross '
               'sales, and it is the only priced consumer row in the file on a gross basis.'),
      dict(key='gross_margin', label='Gross margin', kind='percent', required=True,
           maps_to='profile.gm', peer_field='gross_margin_pct',
           why='Not optional for a consumer brand. Across our listed consumer set the revenue '
               'multiple moves from 0.9x to 2.8x between the lowest and highest margin quartile, '
               'while the gross-profit multiple sits at 3.6x and 3.1x. We price you on gross profit.'),
      dict(key='asset_intensity', label='Do you hold your own stock?', kind='choice',
           choices=('Own inventory', 'Third-party or consignment', 'Dropship or made to order'),
           required=False, maps_to='profile.asset_intensity', peer_field='asset_intensity'),
    ]),
 'payments': dict(
    archetypes=('Merchant Acquiring & PSP', 'Payment Network', 'Cross-Border & FX',
                'Commerce & Payments Software', 'Crypto & Digital Assets'),
    questions=[
      dict(key='net_revenue', label='Net revenue after interchange and scheme fees', kind='money',
           required=True, maps_to='profile.revenue', peer_field='revenue_musd', basis='NET_REVENUE',
           why='Gross and net revenue on a payments business differ by roughly an order of '
               'magnitude, and we store net.'),
    ]),
 # A LENDER IS NOT ASKED FOR REVENUE. For a lending business, revenue contains interest earned on
 # BORROWED money, so it scales with leverage rather than with value, and enterprise value adds back
 # the debt that IS the product. EV/revenue double-counts the funding book: once in the numerator as
 # debt, once in the denominator as the interest that debt generates. Two lenders with identical
 # economics at 3x and 10x leverage price 3x apart on revenue and identically on book.
 #
 # Evidence from our own listed pull: Multitude AG returns a NEGATIVE enterprise value and therefore
 # a negative multiple; Japan Post minus $105bn. OSB Group shows a 2% gross margin and 168x EV/gross
 # profit, Banca IFIS 262x, Cholamandalam 239x. All artefacts of a screen putting gross interest
 # income on the revenue line and interest expense in cost of revenue.
 #
 # And the revenue question cannot be answered from the comparables anyway. Across 30 private lending
 # rounds, net interest income after funding cost was disclosed in 0, and tangible equity in 0. So we
 # ask for the two things a lending founder always knows and a listed lender always reports.
 'lending': dict(
    archetypes=('Lending & Credit', 'Digital Bank & Deposits', 'Insurance Technology'),
    valuation_basis='BOOK',
    questions=[
      dict(key='book_value', label='Book value of the business today', kind='money',
           required=True, maps_to='profile.book_value', peer_field='book_value_musd',
           basis='BOOK', period_required=True,
           why='A lender is priced on price to book, because book value nets the funding off the '
               'assets. A multiple of the loan book alone ignores the liabilities that financed it, '
               'so two lenders with the same book and different leverage would read identically.'),
      dict(key='net_loan_book', label='Net loan book outstanding today', kind='money',
           required=True, maps_to='profile.net_loan_book', peer_field='net_loan_book_musd',
           basis='LOAN_BOOK', period_required=True,
           why='Carried alongside book value so the leverage is visible, and as the fallback where '
               'book value is immaterial. A STOCK at a date, never a total of everything ever lent.'),
      dict(key='originations', label='Amount lent over the last twelve months', kind='money',
           required=False, maps_to='profile.originations', peer_field='originations_musd',
           basis='ORIGINATIONS', period_required=True,
           why='The alternative denominator where the book is sold on rather than held. This is a '
               'FLOW over a stated period. A since-inception total is not an answer and is rejected: '
               'in 43% of the lending announcements we read, the only monetary number offered was an '
               'undated lifetime total, and three rounds disclosed both stock and flow differing by '
               '5x to 6x (Oxyzo $350m AUM against $2bn cumulative; Stenn $6bn since 2015 against '
               '$1bn in 2022; iwoca £2.5bn since 2012 with no book at all).'),
      dict(key='funding_model', label='How are the loans funded?', kind='choice',
           choices=('Our own balance sheet', 'Marketplace or forward-flow', 'Both'),
           required=True, maps_to='profile.funding_model', peer_field='funding_model',
           why='Decides which line the founder is priced on. Retained credit risk goes on the book '
               'basis; originate-and-distribute for a fee is the only lending shape where a revenue '
               'multiple is defensible.'),
    ]),
 'subscription': dict(
    archetypes=('Streaming & Digital Media', 'Dating & Social Network', 'Online Learning'),
    questions=[
      dict(key='net_revenue', label='Net revenue over the last twelve months', kind='money',
           required=True, maps_to='profile.revenue', peer_field='revenue_musd', basis='NET_REVENUE'),
      dict(key='paying_users_k', label='Paying subscribers', kind='count', required=False,
           maps_to='profile.paying_users_k', peer_field='paying_users_k',
           why='Paying, not registered or monthly active. Lets us show an enterprise value per '
               'subscriber alongside the revenue multiple.'),
    ]),
 'delivery': dict(
    archetypes=('Local Delivery & On-Demand',),
    questions=[
      dict(key='gmv', label='Gross transaction value, if you have it to hand', kind='money',
           required=False, maps_to='profile.volume', peer_field='volume_musd',
           why='Cross-check only, not a valuation input, same as GMV on a marketplace.'),
      dict(key='net_revenue', label='Your own revenue over the same period', kind='money',
           required=True, maps_to='profile.revenue', peer_field='revenue_musd', basis='NET_REVENUE',
           why='Flink reports the full basket as gross revenue and Glovo reports a commission. Same '
               'category, revenue figures about ten times apart, so we have to know which one this is.'),
    ]),
}

# AI-NATIVE IS A MODIFIER, NOT A FORK, and the first version got this wrong.
#
# Treating it as its own fork sent 13 of the 21 real profiles down an AI branch that asked only for a
# run rate and a three-month growth figure. OpenSEO and Context.dev are AI-native SaaS businesses:
# losing the retention and margin questions for them is a straight loss, and being AI-native tells
# you nothing about which yardstick applies. So the archetype still picks the fork, and AI-native
# adds one question on top.
AI_NATIVE_EXTRA = [
  dict(key='growth_3m_pct', label='And over the last three months?', kind='percent', required=False,
       maps_to='profile.growth_3m', peer_field='growth_pct_at_round',
       why='An annual rate means little for a company doubling every two months, which is what '
           'Cursor disclosed at its Series C. Where this is given we annualise it for the band.'),
]

FALLBACK = 'software'

def fork_for(prof):
    """Which fork a profiled company gets. Never a menu the founder picks from."""
    a = {prof.get('archetype'), prof.get('archetype_secondary')} - {None, ''}
    for name, f in FORKS.items():
        if a & set(f.get('archetypes', ())): return name
    return FALLBACK

def questions_for(prof):
    qs = CORE + FORKS[fork_for(prof)]['questions']
    if (prof.get('ai_stance') or '') == 'AI_NATIVE': qs = qs + AI_NATIVE_EXTRA
    return qs

def apply_answers(prof, answers):
    """Map answers onto the profile fields the engine reads. Returns a NEW profile."""
    p = dict(prof)
    m = {'growth_pct': 'growth', 'gross_margin': 'gm', 'arr': 'revenue', 'net_revenue': 'revenue',
         'gmv': 'volume', 'tpv': 'volume', 'nrr_pct': 'nrr', 'paying_users_k': 'paying_users_k',
         'funding_model': 'funding_model', 'asset_intensity': 'asset_intensity',
         'growth_3m_pct': 'growth_3m', 'country': 'country'}
    for k, v in (answers or {}).items():
        if v in (None, ''): continue
        if k in m: p[m[k]] = v
    # a three-month rate annualises, and it wins over a stale annual one for an AI-native company
    if p.get('growth_3m') not in (None, ''):
        try: p['growth'] = round(((1 + float(p['growth_3m'])/100.0) ** 4 - 1) * 100, 1)
        except (TypeError, ValueError): pass
    for q in questions_for(prof):
        if q.get('basis') and q['key'] in (answers or {}): p['revenue_basis'] = q['basis']
    return p

def unbacked():
    """Every question that asks for a metric we cannot show a peer figure for. Must stay empty."""
    out = []
    for name, f in list(FORKS.items()) + [('core', dict(questions=CORE)),
                                          ('ai_native_extra', dict(questions=AI_NATIVE_EXTRA))]:
        for q in f['questions']:
            if q.get('context_only'): continue
            if q.get('kind') in ('money', 'percent', 'count') and not q.get('peer_field'):
                out.append((name, q['key']))
    return out
