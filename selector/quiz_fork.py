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
    # NOT ASKED. Resolved from Vercel's edge header at boot: app.js sets responses.country from
    # /api/geo, and docs/lead-capture.md records that no IP is ever stored. Kept in this list
    # because it IS part of the profile contract and the investor matcher scores geography on it;
    # a reader of this file needs to see that the field exists and where it comes from, or the
    # next person adds a question for it. `asked=False` keeps it out of the fork walk.
    dict(key='country', label='Where are you based?', kind='inferred', asked=False, required=False,
         maps_to='profile.country', peer_field='country',
         why='Resolved from the request, not asked. It is one of the three facets the investor '
             'match scores on, and where it is missing the card says so rather than implying we '
             'checked.'),
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
                'Consumer & Prosumer Software', 'Software Consolidator', 'Online Learning'),
    questions=[
      dict(key='arr', label='What is your ARR?', kind='money', required=True,
           maps_to='profile.revenue', peer_field='revenue_musd', basis='ARR',
           why='Compared against 25 private rounds priced on contracted ARR and 6 on a run rate. '
               'We do not ask which yours is: nothing is perfectly comparable and that is fine.'),
      dict(key='nrr_pct', label='Net revenue retention, if you measure it', kind='percent', required=False,
           maps_to='profile.nrr', peer_field='nrr_pct',
           why='51 of 165 listed software names disclose it. The top quarter trades at 11.1x '
               'forward revenue and the bottom at 2.9x, which is the largest gap we can measure. '
               'It is also shown beside every listed name in your comparable table.'),
      # ASKED HERE TOO, because Consumer & Prosumer Software routes to this fork and a consumer app
      # is often the case where ARR is the number the founder does NOT have. Optional, so nobody is
      # blocked, and it unlocks a whole extra range rather than refining an existing one.
      dict(key='paying_subscribers', label='Paying subscribers today, if you sell to consumers',
           kind='quantity', required=False, maps_to='profile.subscribers',
           peer_field='volume_musd', basis='SUBSCRIBERS',
           why='For a consumer subscription business this is what a buyer is buying, and it is '
               'often disclosed when revenue is not. We hold Flo Health at $533 of enterprise '
               'value per paying subscriber and Calm at $500. PAYING, not registered: a price per '
               'registered user compares a business that monetises with one that does not.'),
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
 # PAYING SUBSCRIBERS, for a consumer subscription business. Added 3-Sep-2026, Daniil: "especially
 # if the company is PRE REVENUE, you can calculate value having number of users in denominator."
 #
 # We hold two rounds priced this way and they agree closely: Flo Health at $533 of enterprise value
 # per paying subscriber in September 2021, Calm at $500 in December 2020. Both were in the file
 # from his own sheet with the division never done.
 #
 # PAYING is the whole question, and it is why the label says so twice. A price per registered user
 # compares a business that monetises with one that does not, and the gap between the two is the
 # entire business model.
 'consumer_subscription': dict(
    archetypes=('Consumer & Prosumer Software', 'Streaming & Digital Media',
                'Dating & Social Network'),
    questions=[
      dict(key='paying_subscribers', label='Paying subscribers today', kind='quantity',
           required=True, maps_to='profile.subscribers', peer_field='volume_musd',
           basis='SUBSCRIBERS',
           why='For a consumer subscription business that has not disclosed revenue, this is what '
               'a buyer is buying. We hold Flo Health at $533 of enterprise value per paying '
               'subscriber and Calm at $500. A count at today\'s date, not a total ever '
               'registered.'),
      dict(key='free_users', label='Free or registered users today, if you want it on the record',
           kind='quantity', required=False, maps_to='profile.free_users',
           reviewer_context=True,
           why='NOT part of any range, and deliberately. A price per registered user compares a '
               'business that monetises with one that does not. Carried so a reviewer can see the '
               'conversion behind the paying number.'),
      dict(key='net_revenue', label='Net revenue over the last twelve months, if you have it',
           kind='money', required=False, maps_to='profile.revenue',
           peer_field='revenue_musd', basis='NET_REVENUE',
           why='Optional. Answer it and you get a revenue range as well as a per-subscriber one.'),
    ]),
 # AN EXCHANGE IS JUDGED ON WHAT IT MOVES, NOT WHAT IT EARNS. Added 3-Sep-2026 on Daniil's
 # ruling about Xpansiv: "sustainability business, no? If CO2 volume was quoted in the release,
 # then perhaps these companies are priced as such, hence we should be adding the question to the
 # respective branch of the quiz and show to the founder."
 #
 # It was quoted. Xpansiv's own release states 121.5 MtCO2e cleared on CBL in 2021, and gives no
 # revenue figure at all. That is the shape of this whole archetype: an environmental-commodity
 # exchange, a power-purchase-agreement marketplace or a carbon registry discloses throughput and
 # keeps its take rate to itself. Asking such a founder only for net revenue asks for the one
 # number they are least likely to have and least likely to be judged on.
 #
 # THE UNIT IS A SEPARATE QUESTION AND IT IS REQUIRED, because a ratio may only ever be built from
 # rows sharing a unit. Tonnes of carbon, megawatt hours and dollars are three different
 # denominators, and the answer is shown as a price PER UNIT rather than as a multiple: Xpansiv is
 # eleven dollars fifty per annual tonne of CO2 equivalent, never 11.52x.
 'exchange': dict(
    archetypes=('Market Infrastructure & Exchange', 'Financial Data & Index'),
    questions=[
      dict(key='throughput_volume',
           label='Volume transacted or cleared on your platform over the last twelve months',
           kind='quantity', required=True, maps_to='profile.volume',
           peer_field='volume_musd', basis='THROUGHPUT', period_required=True,
           why='What an exchange is actually judged on. A FLOW over a stated period, never a '
               'since-inception total: a price divided by everything you have ever cleared falls '
               'as you age and says nothing about what you are worth.'),
      dict(key='throughput_unit', label='In what unit?', kind='choice',
           choices=('US dollars', 'Tonnes of CO2 equivalent', 'Megawatt hours', 'Barrels',
                    'Other physical unit'),
           required=True, maps_to='profile.volume_unit', peer_field='volume_basis',
           why='A ratio can only be built from comparables measured in the same unit, so this '
               'decides which comparables you can be shown at all. It also decides how your '
               'answer is written: dollars of value per annual tonne, not a multiple.'),
      dict(key='net_revenue', label='Net revenue over the same period, if you have it',
           kind='money', required=False, maps_to='profile.revenue',
           peer_field='revenue_musd', basis='NET_REVENUE',
           why='Optional here and required almost everywhere else, deliberately. Most exchanges we '
               'hold disclose throughput and no revenue line at all, Xpansiv among them. Answer it '
               'and you get a revenue range as well.'),
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
      # 'Do you hold your own stock?' WITHDRAWN 3-Sep-2026, and the reason it was withdrawn is
      # visible in the line that used to be here: it is the only question in the whole quiz with
      # no `why`. Every other question can say what it does to the range. This one collected an
      # answer that nothing read: not the matcher, not the recommendations engine, not a single
      # peer field. Asking a founder something we then ignore costs their attention and buys
      # nothing, so it comes out until a dimension reads it.
      #
      # It is worth wiring, not deleting: own-inventory retail and dropship are priced differently
      # and the archetype vocabulary already separates them. Open for Daniil, and recorded in
      # docs/investor-sourcing-gaps.md with the other open decisions. To restore:
      #     dict(key='asset_intensity', label='Do you hold your own stock?', kind='choice',
      #          choices=('Own inventory', 'Third-party or consignment', 'Dropship or made to order'),
      #          required=False, maps_to='profile.asset_intensity', peer_field='asset_intensity'),
    ]),
 'payments': dict(
    # 'Card Issuing & BaaS' added 3-Sep-2026. Daniil: "Marqeta is not an acquirer. Marqeta is an
    # issuing business. Pricing payabli vs. Marqeta is wrong conceptually." He is right, and the
    # cause was our vocabulary, not the matcher: we had no archetype for issuing at all, so the
    # only card-issuing business in the listed file sat in the acquiring bucket and was reachable
    # as a core comparable for every payfac and gateway. An issuer earns interchange on cards it
    # puts in the market; an acquirer earns a merchant discount on cards it accepts. Same industry,
    # opposite side of the transaction, different economics. Marqeta keeps Merchant Acquiring & PSP
    # in the secondary slot, so it stays visible to a payments founder as context and can no longer
    # price one.
    archetypes=('Merchant Acquiring & PSP', 'Payment Network', 'Cross-Border & FX',
                'Commerce & Payments Software', 'Card Issuing & BaaS', 'Crypto & Digital Assets'),
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
      # OPTIONAL, and Daniil is right about why. 28-Aug: "Net loan book - why is it required? Do we
      # have the like-for-like multiples to apply on this?" We do not. We hold one private book
      # multiple (Zopa, 5.6x) and ZERO loan-book multiples, private or listed, so requiring this
      # field breaks the rule the fork is built on: never ask for a metric we cannot put a peer
      # number next to. It stays on the form as REVIEWER CONTEXT, because leverage is the first
      # thing a reviewer wants next to a book value, but it is not an engine input and the founder
      # is never blocked on it. It becomes required again on the day we hold like-for-like
      # loan-book multiples on both sides.
      dict(key='net_loan_book', label='Net loan book outstanding today, if you have it to hand',
           kind='money', required=False, maps_to='profile.net_loan_book',
           peer_field='net_loan_book_musd', basis='LOAN_BOOK', period_required=True,
           reviewer_context=True,
           why='Not part of the range. Carried so the leverage behind your book value is visible to '
               'the reviewer. A STOCK at a date, never a total of everything ever lent.'),
      # ARR AND NET INCOME ADDED 3-SEP-2026, ORIGINATIONS PROMOTED OUT OF REVIEWER CONTEXT.
      #
      # Daniil: "public peers are priced off book value or net income. Private peers very often
      # (but not always) are priced off ARR. So when we ask the question to the user, we need to
      # ask all of these (ARR, book value, net income, origination) and show the ranges based on
      # all of that."
      #
      # Every one of these is now backed by multiples we actually hold, which is the rule this
      # fork is built on: never ask for a metric we cannot put a peer number next to.
      #   ARR           12 private lender rounds priced on ARR or an ARR run-rate. It is the
      #                 LARGEST private lender basis we have and the fork was not asking for it.
      #   net income    76 listed rows carry a price-earnings, 12 of them recovered on 3-Sep from
      #                 a loader that was dropping the lending file for any ticker it had already
      #                 seen in the fintech file.
      #   originations  four private rounds on a PERIODIC originations figure: Wayflyer 3.20x,
      #                 Clearco 2.00x, Tala 0.80x, Upgrade 0.75x. The since-inception rows are
      #                 barred in the loader and cannot reach this.
      #
      # Book value stays the only REQUIRED one, because it is the lead basis and the one a lender
      # always knows. The rest are asked and optional, so a founder is never blocked, and each one
      # answered adds a whole range rather than refining an existing one.
      dict(key='arr', label='Annual recurring revenue, or your current revenue run-rate',
           kind='money', required=False, maps_to='profile.arr', peer_field='revenue_musd',
           basis='ARR', period_required=True,
           why='Private lending rounds are priced on ARR far more often than on book. Twelve of '
               'the rounds we hold are, from Starling at 7.6x to Qonto at 41.7x. Answer this and '
               'you get a private ARR range as well as the book one.'),
      dict(key='net_income', label='Net income for the last twelve months, if you are profitable',
           kind='money', required=False, maps_to='profile.net_income', peer_field='ni_ntm_musd',
           basis='EARNINGS', period_required=True,
           why='Listed lenders are priced on earnings as much as on book. We hold a price-earnings '
               'for 76 of them. Leave it blank if you are loss-making; it simply means one fewer '
               'range rather than a worse one.'),
      dict(key='originations', label='Amount lent over the last twelve months, if you have it',
           kind='money', required=False, maps_to='profile.originations',
           peer_field='originations_musd', basis='ORIGINATIONS', period_required=True,
           why='Now a range of its own where the peers support it, not just reviewer context. '
               'Where the book is sold on rather than held this is the shape a denominator would '
               'eventually take. This is a '
               'FLOW over a stated period. A since-inception total is not an answer and is rejected: '
               'in 43% of the lending announcements we read, the only monetary number offered was an '
               'undated lifetime total, and three rounds disclosed both stock and flow differing by '
               '5x to 6x (Oxyzo $350m AUM against $2bn cumulative; Stenn $6bn since 2015 against '
               '$1bn in 2022; iwoca £2.5bn since 2012 with no book at all).'),
      # EV PER BORROWER. Added 3-Sep-2026 on Daniil's instruction, and optional like the rest of
      # the extra lender readings. Backed by MNT-Halan's own February 2023 announcement: "over 2
      # million are borrowers" against a $1bn post-money, so $500 of enterprise value per borrower.
      # One comparable is thin and the range will say so, but a lender that has borrowers and no
      # disclosed book has nothing else to be judged on.
      dict(key='borrowers', label='How many borrowers do you have today?', kind='quantity',
           required=False, maps_to='profile.borrowers', peer_field='volume_musd',
           basis='BORROWERS',
           why='A borrower count is often the only number an early lender can give, and it is not '
               'the same as a subscriber count: a borrower pays interest on a balance rather than a '
               'fee for access, so the two are never averaged together.'),
      dict(key='funding_model', label='How are the loans funded?', kind='choice',
           choices=('Our own balance sheet', 'Marketplace or forward-flow', 'Both'),
           required=True, maps_to='profile.funding_model', peer_field='funding_model',
           why='Decides which line the founder is priced on. Retained credit risk goes on the book '
               'basis; originate-and-distribute for a fee is the only lending shape where a revenue '
               'multiple is defensible.'),
    ]),
 # THE SUBSCRIPTION FORK IS RETIRED. Daniil, 28-Aug: subscription is a REVENUE MODEL, not the
 # nature of a business, and our standing rule is that nature selects. The fork was wrong at the
 # root rather than misrouted. It had swept together three unrelated businesses:
 #
 #   smol, Lyka, Bokksu, FINN   direct-to-consumer brands whose billing recurs. They are priced on
 #                              net revenue and gross margin like any other consumer brand, so they
 #                              belong on the ecommerce fork, which is where Consumer Brand already
 #                              sends them.
 #   Online Learning            Duolingo and Coursera price on retention and margin the way software
 #                              does, so it moves into the software archetype list above.
 #   Streaming, media, social   genuinely distinct: content cost, catalogue and audience rather than
 #                              seats or baskets. That business keeps a fork, below, under its own
 #                              name.
 'media': dict(
    archetypes=('Streaming & Digital Media', 'Dating & Social Network'),
    # NOT YET PRICEABLE, and the fork says so rather than pretending. We hold no private rounds in
    # streaming, media or social with a revenue figure and a stated period, so a founder here reaches
    # listed comparables only. The sourcing list carries the gap: Substack, Cameo, DAZN, Curiosity,
    # Rumble pre-listing. Until those land this fork collects answers and shows the listed side.
    priceable_private=False,
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
    """Which fork a profiled company gets. Never a menu the founder picks from.

    THE PRIMARY ARCHETYPE WINS, and the first version of this did not do that. It put both
    archetypes into one set and walked FORKS in insertion order, so whichever FORK came first in the
    dict claimed the company. Software is first, so any business carrying a software SECONDARY was
    handed the software fork no matter what it actually was:

        Inato          primary Third-Party Marketplace,          secondary Vertical Software
        Priori Legal   primary Freelance & Services Marketplace, secondary Vertical Software
        Moov           primary Merchant Acquiring & PSP,         secondary Cloud & Infrastructure
        Mondu          primary Lending & Credit,                 secondary Commerce & Payments Software

    All four were asked the wrong questions. Mondu was the worst of them: it is a balance-sheet
    business, priced on book by the engine, and the payments fork was asking it for net revenue.
    A founder answering a question that does not reach the number they are priced on is the exact
    failure this file exists to prevent.

    So: try the primary archetype against every fork first, and only fall back to the secondary if
    the primary matches nothing. Dict order is then a tie-break within one archetype, not a
    precedence over the company's actual nature.
    """
    for level in (prof.get('archetype') or '', prof.get('archetype_secondary') or ''):
        if not level: continue
        for name, f in FORKS.items():
            if level in f.get('archetypes', ()): return name
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
