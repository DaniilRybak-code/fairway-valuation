#!/usr/bin/env python3
"""
Adds columns AA (valuation source) and AB (revenue / metric source) from Daniil's sheet to
data/raw/2026-09-01_private-transactions-daniil.csv.

WHY THIS SCRIPT EXISTS, recorded so it does not happen a third time. Daniil sent these two
columns twice: in the 16 screenshots of 01-Sep and again in the 12 of 02-Sep. Both times the
multiples in column Y were transcribed off those same images and the two source columns beside
them were not, and the transcription schema had no field to put them in. Then he was asked for
them a third time. The failure was not the screenshots and not the reading; it was that the
target schema had no column, so there was nowhere for the data to land and nothing flagged its
absence.

THE RULE THAT COMES OUT OF IT, and it belongs in the data durability protocol: a transcription
schema must carry EVERY column the source has. Dropping a column at transcription time is the
one loss the protocol did not cover, because rules 1 to 10 all assume that what arrives is
either written down or visibly missing. A column that was never in the schema is neither.
"""
import csv, io, re, sys

P = 'data/raw/2026-09-01_private-transactions-daniil.csv'


def n(s):
    return re.sub(r'[^a-z0-9]', '', (s or '').lower())


# (company, date prefix) -> (valuation source, revenue / metric source)
# A cell holding several URLs keeps them separated by ' | ', as the sheet has them.
S = {
 ('Oxylabs', '2026-07'): ('https://warburgpincus.com/2026/07/09/oxylabs-announces-130-million-investment-from-warburg-pincus/', 'https://oxylabs.io/blog/oxylabs-receives-investment'),
 ('Sierra', '2026-05'): ('https://www.axios.com/pro/enterprise-software-deals/2026/05/04/sierra-ai-valuation-agentic-enterprise', 'https://www.axios.com/pro/enterprise-software-deals/2026/05/04/sierra-ai-valuation-agentic-enterprise'),
 ('WHOOP', '2026-03'): ('https://techcrunch.com/2026/03/31/whoop-valuation-10b-series-g-fundraise/', 'https://techcrunch.com/2026/03/31/whoop-valuation-10b-series-g-fundraise/'),
 ('Quince', '2026-03'): ('https://techcrunch.com/2026/03/11/quince-series-e-10b-valuation-with-500m-round-led-by-iconiq/', 'https://techcrunch.com/2026/03/11/quince-series-e-10b-valuation-with-500m-round-led-by-iconiq/'),
 ('Notion', '2026-01'): ('https://www.notion.com/blog/gic-sequoia-index-purchase-notion-shares', 'https://www.notion.com/blog/gic-sequoia-index-purchase-notion-shares'),
 ('Mews', '2026-01'): ('https://www.mews.com/en/press/mews-secures-300-million-investment', 'https://www.mews.com/en/press/mews-secures-major-investment'),
 ('Decagon', '2026-01'): ('https://decagon.ai/blog/series-d-announcement', 'https://decagon.ai/blog/series-d-announcement'),
 ('Clay', '2026-01'): ('https://www.clay.com/about', 'https://www.clay.com/about'),
 ('Lovable', '2025-12'): ('https://lovable.dev/blog/series-b', 'https://techcrunch.com/2025/12/18/vibe-coding-startup-lovable-raises-330m-at-a-6-6b-valuation/'),
 ('Creditas', '2025-12'): ('https://www.creditas.com/ir/regulatory/creditas-concludes-acquisition-of-bank-andbank-brasil-and-finalizes-initial/', 'https://www.creditas.com/ir/financial-reports/creditas-financial-results-q3-2025/'),
 ('Revolut', '2025-11'): ('https://www.revolut.com/news/revolut_completes_fundraising_process_establishing_75_billion_valuation/', 'https://www.revolut.com/news/revolut_completes_fundraising_process_establishing_75_billion_valuation/'),
 ('Gamma', '2025-11'): ('https://gamma.app/insights/how-we-built-a-usd100m-business-differently', 'https://gamma.app/insights/how-we-built-a-usd100m-business-differently'),
 ('Ramp', '2025-11'): ('https://techcrunch.com/2025/11/17/ramp-hits-32b-valuation-just-three-months-after-hitting-22-5b/', 'https://techcrunch.com/2025/11/17/ramp-hits-32b-valuation-just-three-months-after-hitting-22-5b/ | https://techcrunch.com/2025/09/09/ramp-says-it-has-hit-1b-in-annualized-revenue/'),
 ('Gong', '2025-11'): ('https://sacra.com/c/gong/', 'https://sacra.com/c/gong/'),
 ('SKIMS', '2025-11'): ('https://am.gs.com/en-int/institutions/news/press-release/2025/skims', 'https://am.gs.com/en-int/institutions/news/press-release/2025/skims'),
 ('LangChain', '2025-10'): ('https://www.langchain.com/blog/series-b', 'https://www.langchain.com/blog/series-b | https://www.forbes.com/sites/rashishrivastava/2025/07/09/ai-startup-langchain-is-in-talks-to-raise-100-million/'),
 ('Deel', '2025-10'): ('https://www.deel.com/blog/new-investment-valuation/', 'https://www.deel.com/blog/new-investment-valuation/'),
 ('Kriya', '2025-10'): ('https://www.allica.bank/hubfs/pdf/allica-bank_annual-report-2025.pdf', 'https://find-and-update.company-information.service.gov.uk/company/07330525/filing-history'),
 ('Supabase', '2025-10'): ('https://supabase.com/blog/series-e', 'https://www.theinformation.com/articles/database-startup-supabase-talks-double-valuation-10-billion'),
 ('Invisible Technologies', '2025-09'): ('https://sacra.com/research/invisible-at-134m-in-revenue/', 'https://sacra.com/research/invisible-at-134m-in-revenue/'),
 ('Perplexity', '2025-09'): ('https://techcrunch.com/2025/09/10/perplexity-reportedly-raised-200m-at-20b-valuation/', 'https://techcrunch.com/2025/09/10/perplexity-reportedly-raised-200m-at-20b-valuation/'),
 ('Replit', '2025-09'): ('https://replit.com/news/funding-announcement-series-c', 'https://replit.com/news/funding-announcement-series-c'),
 ('Sierra', '2025-09'): ('https://techcrunch.com/2025/09/04/bret-taylors-sierra-raises-350m-at-a-10b-valuation/', 'https://techcrunch.com/2025/09/04/bret-taylors-sierra-raises-350m-at-a-10b-valuation/'),
 ('Canva', '2025-08'): ('https://sacra.com/c/canva/', 'https://sacra.com/c/canva/'),
 ('Ramp', '2025-07'): ('https://techcrunch.com/2025/07/30/ramp-raises-500m-at-22-5b-valuation/', 'https://techcrunch.com/2025/09/09/ramp-says-it-has-hit-1b-in-annualized-revenue/'),
 ('Perplexity', '2025-07'): ('https://news.bloomberglaw.com/private-equity/ai-startup-perplexity-valued-at-18-billion-with-new-funding', 'https://news.bloomberglaw.com/private-equity/ai-startup-perplexity-valued-at-18-billion-with-new-funding'),
 ('Harvey', '2025-06'): ('https://www.harvey.ai/blog/harvey-raises-series-e', 'https://techcrunch.com/2025/05/15/harvey-reportedly-in-discussions-to-raise-250m-at-5b-valuation/'),
 ('Scale AI', '2025-06'): ('https://news.bloomberglaw.com/private-equity/scale-ai-expects-to-more-than-double-sales-to-2-billion-in-2025', 'https://news.bloomberglaw.com/private-equity/scale-ai-expects-to-more-than-double-sales-to-2-billion-in-2025'),
 ('Glean', '2025-06'): ('https://www.glean.com/press/glean-raises-150m-series-f-at-7-2b-valuation-to-accelerate-enterprise-ai-agent-innovation-globally', 'https://www.glean.com/press/glean-achieves-100m-arr-in-three-years-delivering-true-ai-roi-to-the-enterprise | https://www.glean.com/press/glean-surpasses-300m-arr-unrivaled-enterprise-context-fuels-ai-adoption'),
 ('Anysphere / Cursor', '2025-06'): ('https://www.cursor.com/blog/series-c', 'https://www.cursor.com/blog/series-c'),
 ('Strava', '2025-05'): ('https://www.techmeme.com/250522/h1115', 'https://www.techmeme.com/250522/h1115'),
 ('Airwallex', '2025-12'): ('https://www.airwallex.com/newsroom/airwallex-series-g', 'https://www.airwallex.com/newsroom/airwallex-series-g'),
 ('Airwallex', '2025-05'): ('https://www.airwallex.com/newsroom/airwallex-raises-300m-series-f', 'https://www.airwallex.com/newsroom/airwallex-raises-300m-series-f'),
 ('Plaid', '2025-04'): ('https://techcrunch.com/2025/04/03/fintech-plaid-raises-575m-at-6-1b-valuation-says-it-will-not-go-public-in-2025/', 'https://techcrunch.com/2025/04/03/fintech-plaid-raises-575m-at-6-1b-valuation-says-it-will-not-go-public-in-2025/'),
 ('OpenAI', '2025-03'): ('https://openai.com/index/march-funding-updates/', 'https://openai.com/index/march-funding-updates/'),
 ('Mercury', '2025-03'): ('https://mercury.com/blog/series-c', 'https://mercury.com/blog/annual-letter-2025'),
 ('Turing', '2025-03'): ('https://techcrunch.com/2025/03/06/turing-a-key-coding-provider-for-openai-and-other-llm-producers-raises-111m-at-a-2-2b-valuation/', 'https://techcrunch.com/2025/03/06/turing-a-key-coding-provider-for-openai-and-other-llm-producers-raises-111m-at-a-2-2b-valuation/'),
 ('Weights & Biases', '2025-03'): ('https://www.coreweave.com/news/coreweave-to-acquire-weights-biases---industry-leading-ai-developer-platform-for-building-and-deploying-ai-applications', 'https://www.theinformation.com/newsletters/ai-agenda/revenue-lags-ai-evaluation-startups'),
 ('Anthropic', '2025-03'): ('https://www.anthropic.com/news/anthropic-raises-series-e-at-usd61-5b-post-money-valuation', 'https://www.bloomberg.com/news/articles/2025-03-03/anthropic-finalizes-megaround-at-61-5-billion-valuation'),
 ('Stripe', '2025-02'): ('https://stripe.com/newsroom/news/2025-employee-tender', 'https://techcrunch.com/2024/02/28/fintech-giant-stripe-valuation-spikes-65b-employee-stock-sale/'),
 ('OLIPOP', '2025-02'): ('https://www.bloomberg.com/news/articles/2025-02-12/olipop-valued-at-1-85-billion-in-50-million-funding-round', 'https://www.bloomberg.com/news/articles/2025-02-12/olipop-valued-at-1-85-billion-in-50-million-funding-round'),
 ('ElevenLabs', '2025-01'): ('https://elevenlabs.io/blog/series-c', 'https://techcrunch.com/2025/01/24/elevenlabs-has-raised-a-new-round-at-3b-valuation-led-by-iconiq-growth-sources-say/'),
 ('Rokt', '2025-01'): ('https://www.rokt.com/blog/rokt-announces-secondary-transaction-increasing-valuation-to-us-3-5-billion-and-appointment-of-anita-sands-to-the-board-of-directors-wfrly', 'https://www.rokt.com/blog/rokt-announces-secondary-transaction-increasing-valuation-to-us-3-5-billion-and-appointment-of-anita-sands-to-the-board-of-directors-wfrly'),
 ('Whatnot', '2025-01'): ('https://techcrunch.com/2025/01/08/livestream-shopping-app-whatnot-raises-265m-pinning-valuation-at-nearly-5b/', 'https://www.greycroft.com/perspectives/reimagining-commerce-leading-whatnots-series-e/'),
 ('Perplexity', '2024-12'): ('https://www.bloomberg.com/news/articles/2024-12-18/ai-startup-perplexity-closes-funding-round-at-9-billion-value', 'https://www.theinformation.com/articles/perplexity-nears-9-billion-valuation-in-investment-led-by-ivp | https://www.bloomberg.com/news/articles/2024-12-18/ai-startup-perplexity-closes-funding-round-at-9-billion-value'),
 ('Olive & June', '2024-12'): ('https://investor.helenoftroy.com/press-releases/press-release-details/2024/Helen-of-Troy-Completes-Acquisition-of-Olive--June-LLC/default.aspx', 'https://www.sec.gov/Archives/edgar/data/916789/000091678924000039/ex-991xpressreleasexoliv.htm'),
 ('Writer', '2024-11'): ('https://writer.com/blog/series-c-funding-writer-press-release/', 'https://writer.com/blog/series-c-funding-writer-press-release/'),
 ('Vinted', '2024-10'): ('https://company.vinted.com/newsroom/secondary-investment', 'https://company.vinted.com/newsroom/secondary-investment'),
 ('Zepz', '2024-10'): ('https://news.bloomberglaw.com/private-equity/accel-tcv-and-world-bank-support-zepzs-267-million-fundraise', 'https://news.bloomberglaw.com/private-equity/accel-tcv-and-world-bank-support-zepzs-267-million-fundraise'),
 ('Alan', '2024-09'): ('https://techcrunch.com/2024/09/20/health-insurance-startup-alan-reaches-45-billion-valuation-with-new-funding-round/', 'https://techcrunch.com/2024/09/20/health-insurance-startup-alan-reaches-45-billion-valuation-with-new-funding-round/'),
 ('Flink', '2024-09'): ('https://techcrunch.com/2024/09/16/flink-the-quick-commerce-startup-raises-another-150m-at-a-valuation-of-just-under-1b/', 'https://techcrunch.com/2024/09/16/flink-the-quick-commerce-startup-raises-another-150m-at-a-valuation-of-just-under-1b/'),
 ('Revolut', '2024-08'): ('https://www.revolut.com/news/revolut-completes-secondary-share-sale/', 'https://www.revolut.com/news/revolut-annual-report-2023/'),
 ('Abnormal Security', '2024-08'): ('https://abnormal-website-rd-sandbox.vercel.app/newsroom/press-releases/series-d-5b-valuation', 'https://abnormal-website-rd-sandbox.vercel.app/newsroom/press-releases/series-d-5b-valuation'),
 ('Vanta', '2024-07'): ('https://www.vanta.com/resources/vanta-announces-series-c', 'https://www.vanta.com/resources/vanta-announces-series-c'),
 ('Clio', '2024-07'): ('https://techcrunch.com/2024/07/23/clio-raises-900m-at-a-3b-valuation-plans-to-double-down-on-ai-and-fintech/', 'https://techcrunch.com/2024/07/23/clio-raises-900m-at-a-3b-valuation-plans-to-double-down-on-ai-and-fintech/'),
 ('Huntress', '2024-06'): ('https://www.huntress.com/press-release/150m-boost-for-huntress-powers-new-products', 'https://www.huntress.com/press-release/150m-boost-for-huntress-powers-new-products'),
 ('AlphaSense', '2024-06'): ('https://news.bloomberglaw.com/private-equity/market-data-firm-alphasense-valued-at-4-billion-in-fundraise | https://theprint.in/tech/alphasense-valued-at-4-billion-after-latest-funding-round/2127015/', 'https://news.bloomberglaw.com/private-equity/market-data-firm-alphasense-valued-at-4-billion-in-fundraise | https://theprint.in/tech/alphasense-valued-at-4-billion-after-latest-funding-round/2127015/'),
 ('Canva', '2024-05'): ('https://www.forbes.com/sites/alexkonrad/2024/05/23/canva-new-tools-cozy-up-corporations/', 'https://www.forbes.com/sites/alexkonrad/2024/05/23/canva-new-tools-cozy-up-corporations/'),
 ('Scale AI', '2024-05'): ('https://techcrunch.com/2024/05/21/data-labeling-startup-scale-ai-raises-1b-as-valuation-doubles-to-13-8b/', 'https://techcrunch.com/2024/05/21/data-labeling-startup-scale-ai-raises-1b-as-valuation-doubles-to-13-8b/'),
 ('Figma', '2024-05'): ('https://www.axios.com/2024/05/16/figma-tender-12-billion', 'https://www.axios.com/2024/05/16/figma-tender-12-billion'),
 ('Vercel', '2024-05'): ('https://www.streetinsider.com/Reuters/Exclusive-Vercel+completes+%24250+million+Series+E+round+at+%243.25+billion+valuation/23238755.html', 'https://www.streetinsider.com/Reuters/Exclusive-Vercel+completes+%24250+million+Series+E+round+at+%243.25+billion+valuation/23238755.html'),
 ('Monzo', '2024-05'): ('https://monzo.com/blog/monzo-funding-2024', 'https://monzo.com/annual-report/2024'),
 ('Wiz', '2024-05'): ('https://www.wiz.io/blog/celebrating-our-1-billion-funding-round-and-12-billion-valuation', 'https://www.wiz.io/blog/celebrating-our-1-billion-funding-round-and-12-billion-valuation'),
 ('Rippling', '2024-04'): ('https://techcrunch.com/2024/04/22/ripplings-parker-conrad-on-the-companys-brand-new-round-its-brand-new-sf-lease-and-also-its-brand-new-critic/', 'https://research.contrary.com/report/rippling'),
 ('FloQast', '2024-04'): ('https://www.floqast.com/press-releases/floqast-secures-100-million-in-series-e-funding-achieving-1-6-billion-valuation', 'https://www.floqast.com/press-releases/floqast-secures-100-million-in-series-e-funding-achieving-1-6-billion-valuation'),
 ('Guesty', '2024-04'): ('https://techcrunch.com/2024/04/10/guesty-snaps-up-130m-at-900m-valuation-to-help-property-managers-list-on-airbnb-and-beyond/', 'https://techcrunch.com/2024/04/10/guesty-snaps-up-130m-at-900m-valuation-to-help-property-managers-list-on-airbnb-and-beyond/'),
 ('Cyera', '2024-04'): ('https://www.cyera.com/press-releases/data-security-leader-cyera-raises-300-million-at-1-4-billion-valuation', 'https://www.cyera.com/press-releases/data-security-leader-cyera-raises-300-million-at-1-4-billion-valuation'),
 ('Chime', '2024-04'): ('https://www.forbes.com/sites/jeffkauflin/2024/05/03/exclusive-the-inside-story-of-chime-americas-biggest-digital-bank/', 'https://www.forbes.com/sites/jeffkauflin/2024/05/03/exclusive-the-inside-story-of-chime-americas-biggest-digital-bank/'),
 ('Liquid Death', '2024-03'): ('https://www.bloomberg.com/news/articles/2024-03-11/liquid-death-is-valued-at-1-4-billion-in-new-financing-round', 'https://www.bloomberg.com/news/articles/2024-03-11/liquid-death-is-valued-at-1-4-billion-in-new-financing-round'),
 ('Mews', '2024-03'): ('https://www.mews.com/en/blog/new-mews-funding-shape-hospitalitys-future', 'https://www.kinnevik.com/investor-relations/press-releases/2024/kinnevik-leads-funding-round-in-mews/'),
 ('Stripe', '2024-02'): ('https://techcrunch.com/2024/02/28/fintech-giant-stripe-valuation-spikes-65b-employee-stock-sale/', 'https://techcrunch.com/2024/02/28/fintech-giant-stripe-valuation-spikes-65b-employee-stock-sale/'),
 ('TravelPerk', '2024-01'): ('https://www.travelperk.com/uk/press-release/travelperk-secures-over-100m-in-funding-to-expand-hypergrowth-platform/', 'https://ionanalytics.com/insights/mergermarket/travelperk-could-study-opportunistic-acquisitions/'),
 ('Perplexity', '2024-01'): ('https://techcrunch.com/2024/01/04/ai-powered-search-engine-perplexity-ai-now-valued-at-520m-raises-70m/', 'https://techcrunch.com/2024/01/04/ai-powered-search-engine-perplexity-ai-now-valued-at-520m-raises-70m/'),
 ('SumUp', '2023-12'): ('https://techcrunch.com/2023/12/10/sumup-taps-e285m-more-in-growth-funding-to-weather-the-fintech-storm/', 'https://techcrunch.com/2023/12/10/sumup-taps-e285m-more-in-growth-funding-to-weather-the-fintech-storm/'),
 ('Checkout.com', '2023-12'): ('https://sifted.eu/articles/checkout-com-300m-losses-2023', 'https://sifted.eu/articles/checkout-com-300m-losses-2023'),
 ('Revolut', '2023-11'): ('https://www.revolut.com/news/revolut-annual-report-2023/', 'https://www.revolut.com/news/revolut-annual-report-2023/'),
 ('Atom Bank', '2023-11'): ('https://www.atombank.co.uk/newsroom/investors-back-atom/', 'https://www.atombank.co.uk/~/docs/annual-report-22-23-holdco.pdf'),
 ('AlphaSense', '2023-09'): ('https://techcrunch.com/2023/09/28/alphasense-an-ai-based-market-intel-firm-snaps-up-150m-at-a-2-5b-valuation/', 'https://techcrunch.com/2023/09/28/alphasense-an-ai-based-market-intel-firm-snaps-up-150m-at-a-2-5b-valuation/'),
 ('HiBob', '2023-09'): ('https://www.hibob.com/news/mid-market-hr-tech-leader-hibob-adds-150m-in-new-round-of-funding-to-support-continued-expansion/', 'https://www.hibob.com/news/mid-market-hr-tech-leader-hibob-adds-150m-in-new-round-of-funding-to-support-continued-expansion/'),
 ('Cato Networks', '2023-09'): ('https://www.catonetworks.com/news/cato-networks-raises-238m-in-equity-investment-at-over-3b-valuation/', 'https://www.catonetworks.com/news/cato-networks-raises-238m-in-equity-investment-at-over-3b-valuation/'),
 ('Writer', '2023-09'): ('https://writer.com/blog/series-b-funding-writer/', 'https://writer.com/blog/series-b-funding-writer/'),
 ('Databricks', '2023-09'): ('https://www.axios.com/2023/09/14/databricks-43-billion-ai-nvidia', 'https://www.axios.com/2023/09/14/databricks-43-billion-ai-nvidia'),
 ('Apollo.io', '2023-08'): ('https://www.apollo.io/magazine/apollo-reaches-150-million-arr-fueled-by-ai', 'https://www.apollo.io/magazine/apollo-reaches-150-million-arr-fueled-by-ai'),
 ('OneTrust', '2023-07'): ('https://techcrunch.com/2023/07/24/onetrust-raises-150m-at-a-4-5b-valuation/', 'https://techcrunch.com/2023/07/24/onetrust-raises-150m-at-a-4-5b-valuation/'),
 ('SKIMS', '2023-07'): ('https://www.retaildive.com/news/kim-kardashian-skims-reaches-4-billion-valuation-dtc/688400/', 'https://www.retaildive.com/news/kim-kardashian-skims-reaches-4-billion-valuation-dtc/688400/'),
 ('Cohere', '2023-06'): ('https://techcrunch.com/2023/06/08/ai-startup-cohere-now-valued-at-over-2-1b-raises-270m/', 'https://techcrunch.com/2023/06/08/ai-startup-cohere-now-valued-at-over-2-1b-raises-270m/'),
 ('Anthropic', '2023-05'): ('https://www.anthropic.com/news/anthropic-series-c', 'https://www.anthropic.com/news/anthropic-series-c'),
 ('SHEIN', '2023-05'): ('https://www.investing.com/news/stock-market-news/fashion-giant-shein-raises-2-billion-but-lowers-valuation-by-a-third-wsj-3084504', 'https://research.contrary.com/company/shein'),
 ('Raisin', '2023-03'): ('https://www.raisin.com/en/corporate/press/series-e/', 'https://www.raisin.com/en/corporate/press/Raisin-Announces-Profitability'),
 ('Stripe', '2023-03'): ('https://techcrunch.com/2023/03/15/stripe-raises-6-5b-at-a-50b-valuation/ | https://stripe.com/en-ch/newsroom/news/stripe-series-i-employee-liquidity', 'https://techcrunch.com/2023/03/15/stripe-raises-6-5b-at-a-50b-valuation/ | https://stripe.com/annual-updates/2022'),
 ('Snyk', '2022-12'): ('https://snyk.io/news/snyk-raises-196-5-million-series-g/', 'https://snyk.io/news/snyk-raises-196-5-million-series-g/'),
 ('Huel', '2022-11'): ('https://techcrunch.com/2022/11/30/huel-idris-elba-plant-based/', 'https://techcrunch.com/2022/11/30/huel-idris-elba-plant-based/'),
 ('Jasper', '2022-10'): ('https://www.jasper.ai/blog/jasper-announces-125m-series-a-funding', 'https://sacra-pdfs.s3.us-east-2.amazonaws.com/jasper.pdf'),
 ('Airwallex', '2022-10'): ('https://www.airwallex.com/newsroom/airwallex-raises-us100-million-series-e2', 'https://www.airwallex.com/newsroom/airwallex-raises-us100-million-series-e2'),
 ('Factorial', '2022-10'): ('https://techcrunch.com/2022/10/11/factorial-raises-120m-at-a-1b-valuation-for-its-hr-software-for-smbs/', 'https://techcrunch.com/2022/10/11/factorial-raises-120m-at-a-1b-valuation-for-its-hr-software-for-smbs/'),
 ('Celonis', '2022-08'): ('https://www.celonis.com/press/celonis-secures-1-billion-in-additional-funds', 'https://www.celonis.com/press/celonis-secures-1-billion-in-additional-funds'),
 ('Incredible Health', '2022-08'): ('https://www.forbes.com/sites/maggiemcgrath/2022/08/17/dr-iman-abuzeid-leads-incredible-health-to-unicorn-status-with-80-million-series-b/ | https://www.incrediblehealth.com/blog/series-b-funding-2022/', 'https://www.forbes.com/sites/maggiemcgrath/2022/08/17/dr-iman-abuzeid-leads-incredible-health-to-unicorn-status-with-80-million-series-b/ | https://www.incrediblehealth.com/blog/series-b-funding-2022/'),
 ('Contentsquare', '2022-07'): ('https://contentsquare.com/press/contentsquare-raises-600-million/', 'https://contentsquare.com/press/contentsquare-raises-600-million/'),
 ('Wefox', '2022-07'): ('https://www.wefox.com/en-de/newsroom/wefox-raises-400m-series-d', 'https://www.wefox.com/en-de/newsroom/wefox-raises-400m-series-d'),
 ('Klarna', '2022-07'): ('https://www.klarna.com/international/press/klarna-announces-800m-financing-at-6-7bn-valuation/ | https://investors.klarna.com/News--Events/news/news-details/2022/Klarna-closes-major-financing-round-during-worst-stock-downturn-in-50-years-holding/default.aspx', 'https://owp.klarna.com/legacy/assets/sites/15/2022/03/28054315/Klarna-Holding-AB-Annual-Report-2021-EN.pdf'),
 ('Coalition', '2022-07'): ('https://www.coalitioninc.com/announcements/series-f', 'https://www.coalitioninc.com/announcements/series-f'),
 ('Xpansiv', '2022-07'): ('https://www.xpansiv.com/press/xpansivs-cbl-sees-near-tripling-in-carbon-trade-in-2021 | https://www.afr.com/street-talk/xpansiv-ipo-ready-to-go-20220501-p5ahin', 'https://www.xpansiv.com/press/xpansivs-cbl-sees-near-tripling-in-carbon-trade-in-2021 | https://www.reportsonline.net.au?documentid=97A1BB23BD8849ED86073FE30C3B90AD'),
 ('SumUp', '2022-06'): ('https://sumup.com/press/sumup-raises-eur590m/ | https://www.sumup.com/en-us/press/global-fintech-sumup-raises-590-million-euros/', 'https://sumup.com/press/sumup-raises-eur590m/ | https://www.sumup.com/en-us/press/global-fintech-sumup-raises-590-million-euros/'),
 ('Personio', '2022-06'): ('https://www.personio.com/about-personio/press/personio-raises-200-million/', 'https://www.personio.com/about-personio/press/personio-raises-200-million/'),
 ('AlphaSense', '2022-06'): ('https://techcrunch.com/2022/06/15/alphasense-an-analysis-and-business-intel-search-engine-finds-225m-at-a-1-7b-valuation/', 'https://techcrunch.com/2022/06/15/alphasense-an-analysis-and-business-intel-search-engine-finds-225m-at-a-1-7b-valuation/'),
 ('Chainalysis', '2022-05'): ('https://www.chainalysis.com/blog/series-f/', 'https://www.chainalysis.com/blog/series-f/'),
 ('Deel', '2022-05'): ('https://www.deel.com/blog/series-d-extension/', 'https://www.deel.com/blog/series-d-extension/'),
 ('Stenn', '2022-04'): ('https://techcrunch.com/2022/04/11/stenn-banks-50m-on-a-900m-valuation-for-a-platform-to-finance-smbs-that-trade-internationally/', 'https://techcrunch.com/2022/04/11/stenn-banks-50m-on-a-900m-valuation-for-a-platform-to-finance-smbs-that-trade-internationally/'),
 ('Remote', '2022-04'): ('https://remote.com/blog/series-c', 'https://remote.com/blog/series-c'),
 ('Docker', '2022-03'): ('https://www.docker.com/blog/docker-series-c/', 'https://www.docker.com/blog/docker-series-c/'),
 ('Blockchain.com', '2022-03'): ('https://techcrunch.com/2022/03/30/blockchain-com-raises-at-14b-valuation/', 'https://techcrunch.com/2022/03/30/blockchain-com-raises-at-14b-valuation/'),
 ('dbt Labs', '2022-02'): ('https://www.getdbt.com/blog/series-d', 'https://www.getdbt.com/blog/series-d'),
 ('GoCardless', '2022-02'): ('https://gocardless.com/blog/series-g/ | https://gocardless.com/en-us/blog/gocardless-secures-312m-to-accelerate-growth-in-open-banking', 'https://gocardless.com/blog/series-g/ | https://find-and-update.company-information.service.gov.uk/company/07495895/filing-history'),
 ('Hopper', '2022-02'): ('https://techcrunch.com/2022/02/03/hopper/', 'https://techcrunch.com/2022/02/03/hopper/'),
 ('Loadsmart', '2022-02'): ('https://blog.loadsmart.com/2022/02/01/loadsmart-raises-200-million-in-series-d-financing-reaching-1-3-billion-valuation', 'https://venturebeat.com/transportation/supply-chain-startup-loadsmart-raises-200m-to-automate-logistics-processes | https://blog.loadsmart.com/2022/02/01/loadsmart-raises-200-million-in-series-d-financing-reaching-1-3-billion-valuation'),
 ('Wayflyer', '2022-02'): ('https://www.irishtimes.com/business/technology/wayflyer-in-no-rush-to-float-after-becoming-tech-unicorn-1.4790911 | https://wayflyer.com/press-releases/wayflyer-series-b', 'https://www.irishtimes.com/business/technology/wayflyer-in-no-rush-to-float-after-becoming-tech-unicorn-1.4790911 | https://wayflyer.com/press-releases/wayflyer-series-b'),
 ('Fireblocks', '2022-01'): ('https://www.fireblocks.com/blog/series-e/', 'https://www.fireblocks.com/blog/series-e/'),
 ('AG1 (Athletic Greens)', '2022-01'): ('https://techcrunch.com/2022/01/25/athletic-greens-valued-at-1-2b-nutrition-drink/', 'https://techcrunch.com/2022/01/25/athletic-greens-valued-at-1-2b-nutrition-drink/'),
 ('Creditas', '2022-01'): ('https://www.creditas.com/ir/non-regulatory/creditas-announces-usd260-million-series-f-fundraising-round/', 'https://www.creditas.com/ir/non-regulatory/creditas-announces-usd260-million-series-f-fundraising-round/'),
 ('6sense', '2022-01'): ('https://6sense.com/newsroom/6sense-announces-200-million-series-e-round-increasing-valuation-to-5-2-billion/', 'https://6sense.com/newsroom/6sense-announces-200-million-series-e-round-increasing-valuation-to-5-2-billion/'),
 ('1Password', '2022-01'): ('https://1password.com/newsroom/1password-raises-620-million/', 'https://1password.com/newsroom/1password-raises-620-million/'),
 ('Spendesk', '2022-01'): ('https://www.spendesk.com/blog/spendesk-series-c/ | https://www.spendesk.com/blog/unicorn-fundraising/', 'https://www.spendesk.com/blog/spendesk-series-c/ | https://www.spendesk.com/blog/unicorn-fundraising/'),
 ('Brex', '2022-01'): ('https://techcrunch.com/2022/01/11/brex-confirms-12-3b-valuation-hires-meta-exec-to-serve-as-its-chief-product-officer/', 'https://techcrunch.com/2022/01/11/brex-confirms-12-3b-valuation-hires-meta-exec-to-serve-as-its-chief-product-officer/'),
 ('Qonto', '2022-01'): ('https://qonto.com/en/blog/qonto/inside-qonto/series-d | https://techcrunch.com/2022/01/10/business-banking-startup-qonto-raises-552-million-at-5-billion-valuation/', 'https://qonto.com/en/blog/qonto/inside-qonto/series-d | https://techcrunch.com/2022/01/10/business-banking-startup-qonto-raises-552-million-at-5-billion-valuation/'),
 ('PayFit', '2022-01'): ('https://techcrunch.com/2022/01/06/payfit-raises-289-million-for-its-payroll-and-hr-solution/ | https://payfit.com/payfit-becomes-a-unicorn/', 'https://techcrunch.com/2022/01/06/payfit-raises-289-million-for-its-payroll-and-hr-solution/ | https://payfit.com/payfit-becomes-a-unicorn/'),
 ('Miro', '2022-01'): ('https://miro.com/newsroom/miro-raises-400-million-in-series-c-financing/', 'https://miro.com/newsroom/miro-raises-400-million-in-series-c-financing/'),
 ('Glovo', '2021-12'): ('https://www.deliveryhero.com/newsroom/tech-champions-join-forces/', 'https://www.lavanguardia.com/economia/20210922/7737767/glovo-ingresos-resultados-beneficio.html'),
 ('Salesloft', '2021-12'): ('https://www.salesloft.com/company/newsroom/salesloft-announces-strategic-growth-investment-from-vista-equity-partners', 'https://www.salesloft.com/company/newsroom/salesloft-surpasses-100-million-in-annual-recurring-revenue'),
 ('Mambu', '2021-12'): ('https://www.mambu.com/press/mambu-raises-eur235m-series-e', 'https://www.mambu.com/press/mambu-raises-eur235m-series-e'),
 ('Pleo', '2021-12'): ('https://www.pleo.io/en/blog/series-c-extension', 'https://www.pleo.io/en/blog/series-c-extension'),
 ('Jobandtalent', '2021-12'): ('https://www.kinnevik.com/investor-relations/press-releases/2021/kinnevik-invests-usd-115-million-in-jobandtalent-the-worlds-leading-digital-temp-staffing-agency/ | https://techcrunch.com/2021/12/01/jobandtalent-series-e/', 'https://techcrunch.com/2021/12/01/jobandtalent-series-e/ | https://www.xrates.eu/exchange-rate-1-december-2021'),
 ('Tipalti', '2021-12'): ('https://tipalti.com/newsroom/tipalti-raises-270-million-in-series-f-funding-at-8-3-billion-valuation/', 'https://tipalti.com/press/series-f-pr/'),
 ('Fundbox', '2021-11-30'): ('https://www.globenewswire.com/news-release/2021/11/30/2343283/0/en/Fundbox-Closes-100M-Series-D-Fueled-by-Record-Growth.html | https://techcrunch.com/2021/11/30/fundbox-raises-100m/', 'https://techcrunch.com/2021/11/30/fundbox-raises-100m/'),
 ('MoonPay', '2021-11'): ('https://www.moonpay.com/newsroom/series-a', 'https://www.moonpay.com/newsroom/series-a'),
 ('Airwallex', '2021-11'): ('https://www.airwallex.com/global/newsroom/airwallex-raises-additional-usd100-million-in-series-e1-led-by-lone-pine', 'https://www.airwallex.com/global/newsroom/airwallex-raises-additional-usd100-million-in-series-e1-led-by-lone-pine'),
 ('Faire', '2021-11'): ('https://news.faire.com/2021/11/16/announcing-400-million-in-series-g/', 'https://news.faire.com/2021/11/16/announcing-400-million-in-series-g/'),
 ('Upgrade', '2021-11'): ('https://www.upgrade.com/en-ca/press/releases/upgrade-raises-280-million-at-6-billion-valuation/', 'https://www.upgrade.com/en-ca/press/releases/upgrade-raises-280-million-at-6-billion-valuation/'),
 ('Wolt', '2021-11'): ('https://ir.doordash.com/news/news-details/2021/DoorDash-to-Acquire-Wolt/default.aspx', 'https://press.wolt.com/en-WW/196005-wolt-closes-530-million-financing-round-to-continue-expanding-beyond-the-restaurant/'),
 ('Thrasio', '2021-10'): ('https://techcrunch.com/2021/10/25/thrasio-the-amazon-aggregator-raises-1b-in-fresh-funding-at-a-valuation-of-up-to-10-billion/', 'https://economictimes.indiatimes.com/tech/funding/thrasio-raises-1-billion-in-funding-led-by-silver-lake/articleshow/87259346.cms'),
 ('Brex', '2021-10'): ('https://www.brex.com/journal/series-d', 'https://www.brex.com/journal/series-d'),
 ('Gorillas', '2021-10'): ('https://www.deliveryhero.com/newsroom/delivery-hero-invests-in-gorillas/ | https://www.theinformation.com/articles/gorillas-raising-950-million-amidst-european-delivery-wars', 'https://www.deliveryhero.com/newsroom/delivery-hero-invests-in-gorillas/ | https://www.theinformation.com/articles/gorillas-raising-950-million-amidst-european-delivery-wars'),
 ('Zopa', '2021-10-19'): ('https://www.zopa.com/blog/article/zopa-raises-gbp220-million-to-build-the-uk-s-best-bank-for-borrowing-and-savings | https://techcrunch.com/2021/10/18/zopa-raises-300m-at-a-1b-valuation-to-expand-its-p2p-lending-and-savings-neobank-in-the-uk/', 'https://www.datocms-assets.com/23873/1658822618-zopa-group-limited-annual-report-and-financial-statements-2020.pdf | https://techcrunch.com/2021/10/18/zopa-raises-300m-at-a-1b-valuation-to-expand-its-p2p-lending-and-savings-neobank-in-the-uk/'),
 ('N26', '2021-10'): ('https://n26.com/en-eu/press/press-release/n26-raises-more-than-900-million', 'https://n26.com/en-eu/press/press-release/n26-raises-more-than-900-million'),
 ('Tala', '2021-10'): ('https://tala.co/tala-series-e/', 'https://tala.co/tala-series-e/'),
 ('Airwallex', '2021-09'): ('https://www.airwallex.com/newsroom/series-e | https://www.airwallex.com/global/newsroom/airwallex-raised-usd200-million-series-e-funding-round-led-by-lone-pine', 'https://www.airwallex.com/newsroom/series-e | https://www.airwallex.com/global/newsroom/airwallex-raised-usd200-million-series-e-funding-round-led-by-lone-pine'),
 ('Flo Health', '2021-09'): ('https://www.globenewswire.com/7/news-release/2021/09/09/2294372/0/en/Flo-Announces-50-Million-Series-B-Funding-Round-Bringing-Company-to-800M-Valuation.html', 'https://www.globenewswire.com/7/news-release/2021/09/09/2294372/0/en/Flo-Announces-50-Million-Series-B-Funding-Round-Bringing-Company-to-800M-Valuation.html'),
 ('Packable', '2021-09'): ('https://www.sec.gov/Archives/edgar/data/1828817/000114036121030752/brhc10028753_ex99-1.htm', 'https://www.sec.gov/Archives/edgar/data/1828817/000110465922022113/tm2128362-32_defm14a.htm'),
 ('Ramp', '2021-08'): ('https://ramp.com/blog/series-c', 'https://ramp.com/blog/series-c'),
 ('Carta', '2021-08'): ('https://carta.com/blog/series-g/', 'https://carta.com/blog/series-g/'),
 ('Chime', '2021-08'): ('https://techcrunch.com/2021/08/13/chime-raises-750m-at-a-25b-valuation/', 'https://techcrunch.com/2021/08/13/chime-raises-750m-at-a-25b-valuation/'),
 ('Upgrade', '2021-08'): ('https://www.upgrade.com/press/releases/upgrade-closes-105-million-series-e-round-at-3-325-billion-valuation/', 'https://www.pymnts.com/digital-first-banking/2021/upgrade-valued-3-billion-dollars-series-e-fundraising-round'),
 ('Trendyol', '2021-08'): ('https://cdn.dsmcdn.com/web/static-pages/trendyol-funding-round-release.pdf', 'https://cdn.dsmcdn.com/web/static-pages/trendyol-funding-round-release.pdf'),
 ('Rapyd', '2021-08'): ('https://techcrunch.com/2021/08/03/rapyd-raises-300m-on-8-75b-valuation-as-fintech-as-a-service-continues-to-boom/', 'https://techcrunch.com/2021/08/03/rapyd-raises-300m-on-8-75b-valuation-as-fintech-as-a-service-continues-to-boom/'),
 ('Gopuff', '2021-07'): ('https://techcrunch.com/2021/07/30/gopuff-confirms-new-1b-cash-injection-at-a-15b-valuation-to-expand-its-instant-grocery-delivery-service/ | https://www.gopuff.com/gb/blog/news/gopuff-announces-fundraise/', 'https://techcrunch.com/2021/07/30/gopuff-confirms-new-1b-cash-injection-at-a-15b-valuation-to-expand-its-instant-grocery-delivery-service/ | https://www.gopuff.com/gb/blog/news/gopuff-announces-fundraise/'),
 ('Algolia', '2021-07'): ('https://www.algolia.com/fr/about/news/algolia-advances-api-first-software-development-valuation-soars-to-2-25-billion-with-150-million-series-d-funding', 'https://www.inc.com/peter-cohan/algolias-ceo-has-a-vision-for-google-challenger.html'),
 ('Fireblocks', '2021-07'): ('https://www.fireblocks.com/blog/series-d/', 'https://www.fireblocks.com/blog/series-d/'),
 ('Revolut', '2021-07'): ('https://www.revolut.com/news/revolut-raises-800m-series-e/', 'https://www.revolut.com/news/revolut-raises-800m-series-e/'),
 ('Clearco', '2021-07'): ('https://techcrunch.com/2021/07/08/clearco-gets-the-softbank-stamp-of-approval-in-new-215m-round', 'https://techcrunch.com/2021/07/08/clearco-gets-the-softbank-stamp-of-approval-in-new-215m-round'),
 ('Chainalysis', '2021-06'): ('https://www.chainalysis.com/blog/series-e/', 'https://www.chainalysis.com/blog/series-e/'),
 ('GOAT Group', '2021-06'): ('https://www.goatgroup.com/news/goat-group-valuation-more-than-doubles-to-3-7-billion-after-closing-series-f-funding-round-of-195-million', 'https://www.goatgroup.com/news/goat-group-valuation-more-than-doubles-to-3-7-billion-after-closing-series-f-funding-round-of-195-million'),
 ('Mollie', '2021-06'): ('https://www.mollie.com/news/mollie-raises-800-million | https://www.mollie.com/news/mollie-series-c', 'https://www.mollie.com/news/mollie-raises-800-million | https://find-and-update.company-information.service.gov.uk/company/FC037866/filing-history'),
 ('Klarna', '2021-06'): ('https://www.klarna.com/international/press/klarna-raises-639m/ | https://techcrunch.com/2021/06/10/fintech-giant-klarna-raises-639m-at-a-45-6b-valuation/', 'https://www.klarna.com/international/press/klarna-raises-639m/ | https://techcrunch.com/2021/06/10/fintech-giant-klarna-raises-639m-at-a-45-6b-valuation/'),
 ('Gong', '2021-06'): ('https://www.gong.io/press/gong-raises-250-million-in-series-e-funding-at-7-25-billion-valuation', 'https://en.globes.co.il/en/article-gong-raises-250-million-at-72b-valuation-1001373264'),
 ('Clearco', '2021-04'): ('https://techcrunch.com/2021/04/20/clearbanc-rebrands-as-clearco-gets-a-350m-valuation-boost', 'https://techcrunch.com/2021/04/20/clearbanc-rebrands-as-clearco-gets-a-350m-valuation-boost'),
 ('StockX', '2021-04'): ('https://stockx.com/about/press-release-stockx-valuation-surges-to-3-8-billion-with-255-million-financing/', 'https://stockx.com/about/press-release-stockx-valuation-surges-to-3-8-billion-with-255-million-financing/'),
 ('Patreon', '2021-04'): ('https://news.patreon.com/articles/the-second-renaissance-is-here | https://www.theinformation.com/articles/patreon-considers-public-listing-as-soon-as-this-year', 'https://news.patreon.com/articles/the-second-renaissance-is-here | https://www.theinformation.com/articles/patreon-considers-public-listing-as-soon-as-this-year'),
 ('Plaid', '2021-04'): ('https://plaid.com/blog/series-d/', 'https://plaid.com/blog/series-d/'),
 ('dLocal', '2021-04'): ('https://dlocal.gcs-web.com/node/6351/pdf | https://techcrunch.com/2021/04/02/uruguayan-payments-startup-dlocal-quadruples-valuation-to-5b-with-150m-raise/', 'https://dlocal.gcs-web.com/static-files/79d4e12d-3783-411ad-9202-d178038ec0ca | https://techcrunch.com/2021/04/02/uruguayan-payments-startup-dlocal-quadruples-valuation-to-5b-with-150m-raise/'),
 ("Harry's", '2021-03'): ('https://www.forbes.com/sites/stevenbertoni/2021/03/31/exclusive-harrys-raises-a-155-million-series-e--at-17-billion-a-year-after-the-ftc-blocked-its-billion-dollar-sale-to-edgewell/', 'https://www.forbes.com/sites/stevenbertoni/2021/03/31/exclusive-harrys-raises-a-155-million-series-e--at-17-billion-a-year-after-the-ftc-blocked-its-billion-dollar-sale-to-edgewell/'),
 ('Loft', '2021-03'): ('https://techcrunch.com/2021/03/23/real-estate-platform-loft-raises-425m-at-a-2-2b-valuation-in-one-of-brazils-largest-venture-rounds/', 'https://techcrunch.com/2021/03/23/real-estate-platform-loft-raises-425m-at-a-2-2b-valuation-in-one-of-brazils-largest-venture-rounds/'),
 ('Yotpo', '2021-03'): ('https://techcrunch.com/2021/03/18/yotpo-series-f/', 'https://techcrunch.com/2021/03/18/yotpo-series-f/'),
 ('Savage X Fenty', '2021-02'): ('https://www.lcatterton.com/pdf/2021-LC-SavageXFenty.pdf | https://www.forbes.com/sites/korihale/2021/02/16/rihannas-savage-x-fenty-reaches-1-billion-valuation-in-lingerie-equity/', 'https://www.lcatterton.com/pdf/2021-LC-SavageXFenty.pdf | https://www.forbes.com/sites/korihale/2021/02/16/rihannas-savage-x-fenty-reaches-1-billion-valuation-in-lingerie-equity/'),
 ('Calendly', '2021-01'): ('https://research.contrary.com/company/calendly', 'https://research.contrary.com/company/calendly'),
 ('Rapyd', '2021-01'): ('https://www.calcalistech.com/ctech/articles/0,7340,L-3887513,00.html', 'https://www.calcalistech.com/ctech/articles/0,7340,L-3887513,00.html'),
 ('Creditas', '2020-12'): ('https://www.creditas.com/ir/non-regulatory/creditas-announces-ususd255-million-series-e/', 'https://www.creditas.com/ir/regulatory/creditas-financial-results-q3-2020/'),
 ('Calm', '2020-12'): ('https://www.globenewswire.com/news-release/2020/12/08/2141185/0/en/Calm-Hits-2-Billion-Valuation-Expands-into-Wellness-at-Work.html', 'https://www.globenewswire.com/news-release/2020/12/08/2141185/0/en/Calm-Hits-2-Billion-Valuation-Expands-into-Wellness-at-Work.html'),
 ('Loadsmart', '2020-11'): ('https://blog.loadsmart.com/2020/11/20/news-digital-freight-platform-loadsmart-raises-90m-in-series-c-funding-round-led-by-blackrocks-managed-funds', 'https://www.freightwaves.com/news/analysis-what-greenbriar-and-blackrocks-digital-freight-brokerage-deals-mean'),
 ('Mollie', '2020-09'): ('https://techcrunch.com/2020/09/07/dutch-payments-startup-mollie-raises-106m-at-1b-valuation', 'https://techcrunch.com/2020/09/07/dutch-payments-startup-mollie-raises-106m-at-1b-valuation'),
 ('Thrasio', '2020-07'): ('https://news.crunchbase.com/startups/thrasio-gets-its-horn-260m-series-c-round-provides-1b-valuation/', 'https://news.crunchbase.com/startups/thrasio-gets-its-horn-260m-series-c-round-provides-1b-valuation/'),
 ('Marqeta', '2020-05'): ('https://www.marqeta.com/blog/marqeta-raises-150-million-in-new-capital | https://www.forbes.com/sites/jeffkauflin/2020/05/28/payments-startup-marqeta-more-than-doubles-valuation-to-43-billion/', 'https://www.forbes.com/sites/jeffkauflin/2020/05/28/payments-startup-marqeta-more-than-doubles-valuation-to-43-billion/'),
 ('Tala', '2019-08'): ('https://tala.co/blog/2019/08/21/tala-raises-110m-series-d-to-accelerate-financial-agency-for-all/', 'https://tala.co/blog/2019/08/21/tala-raises-110m-series-d-to-accelerate-financial-agency-for-all/'),
 ('Calm', '2019-07'): ('https://www.cnbc.com/2019/07/01/calm-raises-27-million-at-1-billion-valuation.html', 'https://www.cnbc.com/2019/07/01/calm-raises-27-million-at-1-billion-valuation.html'),
 ('Marqeta', '2019-05'): ('https://techcrunch.com/2019/05/21/payment-card-startup-marqeta-confirms-260m-round-at-close-to-2b-valuation/', 'https://www.forbes.com/sites/jeffkauflin/2019/03/26/it-took-three-tries-but-this-entrepreneur-transformed-his-struggling-startup-into-a-2b-unicorn/'),
 ('Away', '2019-05'): ('https://www.forbes.com/sites/amyfeldman/2019/05/14/at-a-valuation-as-high-as-145b-valuation/', 'https://www.forbes.com/sites/amyfeldman/2019/05/14/at-a-valuation-as-high-as-145b-valuation/'),
 ('Salesloft', '2019-04'): ('https://techcrunch.com/2019/04/25/salesloft-funding/', 'https://getlatka.com/blog/salesloft-revenue-hits-50m-will-be-ipo-ready-in-2020-with-140m-raised/'),
 ('Rent the Runway', '2019-03'): ('https://techcrunch.com/2019/03/21/rent-the-runway-hits-a-1-billion-valuation/', 'https://techcrunch.com/2019/03/21/rent-the-runway-hits-a-1-billion-valuation/'),
 ('Glossier', '2019-03'): ('https://techcrunch.com/2019/03/19/glossier-triples-valuation-enters-unicorn-club-with-100m-round/', 'https://techcrunch.com/2019/03/19/glossier-triples-valuation-enters-unicorn-club-with-100m-round/'),
 ('Calm', '2019-02'): ('https://www.globenewswire.com/news-release/2019/02/06/1711311/0/en/Calm-Raises-88M-Becomes-First-Mental-Health-Unicorn.html', 'https://www.globenewswire.com/news-release/2019/02/06/1711311/0/en/Calm-Raises-88M-Becomes-First-Mental-Health-Unicorn.html'),
 ('Deezer', '2018-08'): ('https://newsroom-deezer.com/fr/2018/08/deezer-annonce-une-levee-de-fonds-de-160-millions-deuros-aupres-dinvestisseurs-nouveaux-et-existants/', 'https://www.cfnews.net/L-actualite/Capital-innovation/Operations/7eme-tour/Deezer-une-autre-licorne-francaise-276762'),
 ('Bright Data / Luminati', '2017-08'): ('https://www.emk.capital/news/emk-acquires-luminati-the-worlds-largest-ip-proxy-network-which-brings-transparency-to-the-internet', 'https://brightdata.com.br/static/brd/bright-data-press-kit.pdf'),
 ('Buffer', '2014-10'): ('https://buffer.com/resources/raising-3-5m-funding-valuation-term-sheet/', 'https://buffer.com/resources/buffer-october-2014-investor-report/'),
}

raw = open(P).read().split('\n')
head = [l for l in raw if l.startswith('#')]
body = '\n'.join([l for l in raw if not l.startswith('#') and l.strip()])
rows = list(csv.DictReader(io.StringIO(body)))
cols = list(rows[0].keys())
for c in ('valuation_source_url', 'revenue_source_url'):
    if c not in cols:
        cols.append(c)

lookup = {}
for (co, dp), v in S.items():
    lookup.setdefault(n(co), []).append((dp, v))

filled = 0
missed = []
for r in rows:
    hit = None
    for dp, v in sorted(lookup.get(n(r['company']), []), key=lambda x: -len(x[0])):
        if (r['txn_date'] or '').startswith(dp):
            hit = v
            break
    if hit:
        r['valuation_source_url'], r['revenue_source_url'] = hit
        filled += 1
    else:
        r['valuation_source_url'] = r['revenue_source_url'] = ''
        missed.append('%s %s' % (r['company'], r['txn_date']))

head = [l for l in head if 'Columns kept are the ones' not in l]
if not any('COLUMNS AA AND AB ADDED' in l for l in head):
    head += ['# COLUMNS AA AND AB ADDED 02-Sep-2026, read off the same two screenshot batches that were',
             '# already in the repo. They had been dropped twice because this schema had no field for',
             '# them. The post-mortem is at the top of tools/add_sheet_source_urls_2sep.py.']

out = io.StringIO()
w = csv.DictWriter(out, fieldnames=cols)
w.writeheader()
for r in rows:
    w.writerow({c: r.get(c, '') for c in cols})
open(P, 'w').write('\n'.join(head) + '\n' + out.getvalue())

print('%d of %d rows now carry both source URLs.' % (filled, len(rows)))
if missed:
    print('\n%d rows without, each one a row whose source cell was cut off at the screenshot width:'
          % len(missed))
    for m in missed:
        print('   ', m)
