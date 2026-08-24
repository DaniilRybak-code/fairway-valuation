# -*- coding: utf-8 -*-
"""THIRD VOCABULARY FAMILY: consumer, commerce and marketplace businesses.

WHY THIS FAMILY EXISTS AT ALL

The software vocabulary asks three questions: what kind of software is it
(archetype), what job does it do (function), who does it sell into (industry).
The fintech vocabulary keeps that shape and swaps the archetypes for economic
engines, because a bank and a payment network are not two kinds of software.

Neither shape survives contact with this set, for one measurable reason.

  GROSS MARGIN IN THE SOFTWARE SET RANGES 24% TO 98%, MEDIAN 77%.
  GROSS MARGIN IN THIS SET RANGES 8% TO 100%, AND IT IS BIMODAL.

Everything follows from that. In software, revenue means roughly the same thing
from one company to the next, so EV/revenue is a fair comparison. Here it is not.
Measured on the 62 names in this set that carry a usable gross profit line:

    gross margin      median EV/NTM revenue      median EV/NTM gross profit
    under 30%   n=7           0.7x                        2.4x
    30-50%      n=13          2.2x                        5.0x
    50-70%      n=14          1.8x                        3.0x
    70% and up  n=28          3.2x                        3.6x

EV/revenue moves 4.4x across the margin buckets. EV/gross profit moves 2.1x.
Most of what looks like a valuation difference between Carvana and Rightmove is
not a valuation difference, it is an accounting one: one of them books the price
of the car as revenue and the other books the listing fee.

THE THREE RULES THAT FOLLOW

  1. For any subject tagged into this family, GROSS PROFIT IS THE PRIMARY
     DENOMINATOR and revenue is the secondary one. The reveal shows both. It
     leads with gross profit whenever the subject's gross margin sits more than
     15 points from the peer group median, because on those the revenue multiple
     is measuring the business model, not the business.

  2. asset_intensity is the single most load-bearing tag in the family. It is
     what makes the margin bimodal, so it must be matched before anything else.
     A founder at 80% gross margin is not comparable to Carvana whatever else
     they have in common.

  3. Revenue growth is NOT downweighted here the way it is for private rounds.
     In this set growth ranges -47% to +73% and it is priced.

WHAT CARRIES OVER AND WHAT DOES NOT

  CARRIES OVER, unchanged, because it still discriminates:
    industry      the consumer category. Six new values are added below.
    buyer         who actually bears the monetisation. See the convention below.
    ai_stance     Chegg is at -47% NTM revenue growth and 0.4x. AI_EXPOSED is
                  not a label here, it is the whole story of a name.
    in_medians    a row can be visible and still be out of every median.

  REPLACED, because the software values carry no information here:
    archetype     twelve consumer engines, below.
    function      four operating cores, below.
    revenue_model four new values. GMV_RETAIL versus TAKE_RATE is the Carvana
                  versus eBay distinction and it is worth about 3x of multiple.
    gtm_motion    three new values. Paid-acquisition dependence is a real driver.
    product_role  three new values.

  NEW FIELDS, which software and fintech rows do not have today:
    asset_intensity
    purchase_frequency
  Both default for the existing sets: a software or fintech row that has not been
  given one reads as asset_intensity=NONE, purchase_frequency=SUBSCRIPTION, which
  is true for almost all of them. The defaults are applied in the loader, not
  written into those files, so nothing already reviewed gets edited silently.
"""

# ---------------------------------------------------------------------------
# ARCHETYPE. Twelve engines. Same discipline as the fintech family: each one is
# defined by HOW THE MONEY IS MADE, not by what the company sells.
# ---------------------------------------------------------------------------
ECOM_ARCHETYPES = {
 'Owned-Inventory Retail':
   'buys the goods, holds them, sells them. Revenue is the full ticket price, so '
   'gross margin is 8-35% and the revenue multiple is close to meaningless',
 'Third-Party Marketplace':
   'matches a buyer and a seller and never owns the goods. Revenue is the take '
   'rate on volume it did not fund',
 'Local Delivery & On-Demand':
   'matches supply and demand inside a geography and carries a physical '
   'fulfilment leg, so it has real variable cost per order and city-level density',
 'Travel Booking & OTA':
   'sells third-party travel inventory for a commission, holds no rooms or seats '
   'and takes no inventory risk',
 'Classifieds & Listings':
   'charges the supply side to be listed and found. No transaction, no inventory, '
   'no take rate. This is why it clears the highest multiples in the set',
 'Freelance & Services Marketplace':
   'matches labour rather than goods, and leaks whenever the two sides can '
   'transact off-platform',
 'Dating & Social Network':
   'monetises a social graph directly, through subscription or a-la-carte, with '
   'no supply side to pay',
 'Streaming & Digital Media':
   'licenses or produces content and rents access to it, so the content is an '
   'asset on the balance sheet and a cost in the P&L',
 'Gaming & Virtual Economy':
   'earns on virtual goods and creator economics inside a world it operates',
 'Online Learning':
   'sells learning outcomes to a consumer or an enterprise, and is the part of '
   'this set most directly exposed to generative AI',
 'Consumer Brand':
   'designs its own product, owns the brand and the inventory, and sells it '
   'direct and through wholesale',
 'Commerce Enablement & Fulfilment':
   'operates the store, the logistics or the cross-border layer on behalf of '
   'someone else\'s brand, for a service fee',
}

# ---------------------------------------------------------------------------
# FUNCTION. Four operating cores. This is orthogonal to the archetype: it is
# what the company actually runs, and it is what makes the SECONDARY peer group
# in peer_groups() work. A cars-classifieds founder and a jobs-classifieds
# founder share 'Listings & Discovery' but sit in different industries, so one
# lands in core and the other in secondary. That is the intended mechanism.
# ---------------------------------------------------------------------------
ECOM_FUNCTIONS = {
 'Commerce Operations':   'takes the order and is accountable for the goods reaching the customer',
 'Marketplace Operations':'runs the matching layer and the trust, payments and dispute machinery around it',
 'Listings & Discovery':  'runs a search and listing surface, and is paid for placement rather than for a transaction',
 'Content & Community':   'produces, licenses or hosts what the user came for',
}

# ---------------------------------------------------------------------------
# REVENUE MODEL. Four new values. TAKE_RATE and ADVERTISING already exist in the
# software vocabulary and keep their meaning.
# ---------------------------------------------------------------------------
ECOM_REVENUE_MODELS = {
 'GMV_RETAIL':
   'revenue IS the merchandise. Carvana books the whole price of the car; eBay '
   'books a fee on the same car. Never compare the two on revenue',
 'LISTING_FEE':
   'the supply side pays to be listed whether or not anything transacts. It is a '
   'subscription that happens to be sold to a business, and it prices like one',
 'SUBSCRIPTION_CONSUMER':
   'a recurring fee from the end user, cancellable monthly. Churn, not contract '
   'value, is the thing to look at',
 'PRODUCT_SALES':
   'owns the brand and the inventory and sells its own product. Gross margin is '
   'a brand outcome (e.l.f. at 70%, YETI at 57%), not a software outcome',
}

# ---------------------------------------------------------------------------
# NEW FIELD 1: ASSET_INTENSITY. The most load-bearing tag in the family.
# ---------------------------------------------------------------------------
# Split after the first pass, because the first cut did not survive the data.
# "Owns inventory" lumped Chewy with e.l.f. and produced a bucket spanning 8% to
# 74% gross margin, which is no bucket at all. A retailer's cost of goods is the
# wholesale price it paid; a brand's cost of goods is what it cost to make. Same
# working capital, completely different margin, so they are separate values.
# Observed on this set: RESALE_INVENTORY n=11, gross margin 30% median, EV/NTM
# revenue 0.7x. OWN_PRODUCT n=7, gross margin 63% median, EV/NTM revenue 2.3x.
ASSET_INTENSITY = {
 'RESALE_INVENTORY':
              'buys finished goods at wholesale and resells them, or buys the '
              'cars and the houses. Gross margin 8-35%',
 'OWN_PRODUCT':
              'designs or manufactures what it sells, so gross margin is a brand '
              'outcome. 55-75%',
 'CONTENT':   'owns or licenses the content asset. Gross margin 30-50%, and the '
              'cost sits in amortisation rather than in cost of goods',
 'FLEET_OPS': 'owns no goods but runs a physical operating network of couriers, '
              'drivers or shoppers. Gross margin 25-55% and it scales with density',
 'NONE':      'asset-light. Gross margin 70-100%',
}

# ---------------------------------------------------------------------------
# NEW FIELD 2: PURCHASE_FREQUENCY. Separates Rightmove from eBay inside the same
# end market, and Netflix from Carvana inside the same margin band.
# ---------------------------------------------------------------------------
PURCHASE_FREQUENCY = {
 'SUBSCRIPTION':       'contractual recurring revenue, consumer or supply side',
 'REPEAT_TRANSACTION': 'high frequency, no contract. The cohort is the asset',
 'EPISODIC':           'low frequency and high ticket. Every sale is re-acquired',
}

# ---------------------------------------------------------------------------
# GTM MOTION. Three new values. ENT_SALES and CHANNEL keep their software meaning
# and are used where they are literally true (field sales to agents and dealers;
# wholesale distribution for a brand).
# ---------------------------------------------------------------------------
ECOM_GTM = {
 'PAID_ACQUISITION': 'demand is bought. Marketing is a variable cost of revenue in all but name',
 'ORGANIC_BRAND':    'demand arrives direct or through search because of the brand',
 'NETWORK_EFFECT':   'supply brings demand and demand brings supply, so acquisition cost falls with scale',
}

# ---------------------------------------------------------------------------
# PRODUCT ROLE. Three new values.
# ---------------------------------------------------------------------------
ECOM_PRODUCT_ROLES = {
 'DESTINATION': 'the consumer goes there on purpose and by name',
 'AGGREGATOR':  'sits above someone else\'s supply and is substitutable with another aggregator',
 'BRAND':       'the product itself is the reason to buy',
}

# ---------------------------------------------------------------------------
# THE buyer CONVENTION FOR TWO-SIDED BUSINESSES
#
# buyer = THE SIDE THAT BEARS THE MONETISATION, not the side that clicks.
#   eBay, Etsy            SMB       the seller pays the fee
#   Booking, Expedia      SMB       the hotel pays the commission
#   Airbnb                CONSUMER  the guest pays the larger half of the fee
#   DoorDash, Delivery Hero SMB     the restaurant commission is the larger half
#   REA, Rightmove, SEEK  SMB       the agent, dealer or employer pays
#   CoStar                LOB       a commercial-property professional inside a firm
#   Netflix, Match, YETI  CONSUMER  nobody else pays
#
# This is the who-pays axis and it is why buyer survives into this family when
# gtm_motion and product_role had to be rebuilt.
# ---------------------------------------------------------------------------

NEW_INDUSTRIES = {
 'Travel':                 'flights, hotels, packages, experiences',
 'Food & Grocery':         'restaurant delivery, grocery, quick commerce',
 'Apparel & Beauty':       'clothing, footwear, cosmetics, resale',
 'Education':              'consumer and enterprise learning',
 'Recruitment & Work':     'jobs, hiring, freelance labour',
 'Dating & Relationships': 'dating and social discovery',
}

# Added after the first pass over the data: consolidated gross margin on the
# largest names blends an asset-light core with owned-inventory or cloud
# segments. asset_intensity describes the CONSOLIDATED cost structure, because
# that is what the reported gross margin reflects and matching on it is the
# point. Amazon, Alibaba, Sea, Meituan, Zomato, Swiggy and The RealReal are MIXED.
ASSET_INTENSITY['MIXED'] = ('an asset-light core consolidated with an '
   'owned-inventory, logistics or cloud segment, so the reported gross margin '
   'is not a read on either one')
