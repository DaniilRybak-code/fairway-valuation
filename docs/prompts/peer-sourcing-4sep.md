# Data pull, 4-Sep-2026. Two parts, one paste.

**Part A, peers.** Seventeen lanes where the engine narrowed the world for a real company and then
ran out of comparables carrying a revenue figure.

**Part B, funds.** The two sectors where a founder finishes the quiz and is told nobody is writing
cheques into their market, because we hold nobody.

They are one pull because they are one gap: the same two corners of the market are thin in the
comparables file and thin in the investor file. Two output files, both into `data/raw/`, both under
the durability rules (a figure with no source does not exist, and a screenshot is not a delivery).

---

# Part A. Peer sourcing

Run this in the other chat. It is the output of the march to 100: every place where the engine
narrowed the world for a real company and then ran out of comparables that carry a revenue figure.

## What this is

We test the engine against 102 real companies (Y Combinator batches and Product Hunt launches).
For each one it picks a core lane of listed peers, a secondary lane of listed peers, and a private
lane of funding rounds. **Seventeen of those lanes end up holding exactly one usable name.** One
name is not a range, so the fixture fails.

For each gap below the engine has already checked our own database and confirmed the next best
comparable **is not in it**. The only names left were unrelated ones that our own rule bars.

## What I need back

One CSV, `data/raw/2026-09-04_peer-sourcing.csv`, with these columns exactly:

```
gap_key,company_name,ticker_or_private,is_listed,round_date,revenue_musd,revenue_basis,revenue_period,ev_musd,ev_revenue_x,growth_pct,source_url
```

Rules, and they matter more than coverage:

1. **Every figure needs the URL where it actually appears.** A company's own release, its filed
   accounts, or an exchange announcement. A figure with no source does not go in the file. In this
   project a figure with no source does not exist.
2. **Do not estimate a revenue number.** If a private round did not disclose revenue, leave the
   row out entirely rather than filling it. A round we cannot price is not a comparable.
3. **`revenue_basis`** is what the number actually is: NET_REVENUE, GROSS_REVENUE, ARR, GMV, or
   REVENUE_FROM_OPERATIONS for Indian filers. Say which, do not normalise it yourself.
4. **`revenue_period`** is the window: LTM, FY2025, ANNUALISED_Q4, RUN_RATE. If the source does not
   say, write NOT STATED rather than guessing.
5. **Listed names:** give the ticker with its exchange. **Private rounds:** give the announcement
   date and the post-money.
6. Aim for **four to six names per gap**. Three good ones beat eight loose ones.

## The seventeen gaps

Each row is a real company we tested. Find comparables for the company as described, not for the
sector word: the whole point is that the sector word already matched and was not enough.

| gap | the company we tested | what it does | lane(s) short | its own vocabulary |
|---|---|---|---|---|
| `agentcard` | Card Issuing & BaaS / Commerce & Payments Software | Debit cards for AI agents | secondary, private | Agent Payments, Virtual Card Issuing, Programmatic Spend Controls, Machine To Machine Payments, Card API |
| `evergrove` | Insurance Technology / Vertical Software | Voice agents that accelerate care coordination in workers' comp | secondary | Workers Compensation, Voice Agents, Care Coordination, Claims Communication, Case Management |
| `finn` | Owned-Inventory Retail / Local Delivery & On-Demand | All-inclusive monthly car subscription on an owned fleet, delivered to the door | private | Car Subscription, All Inclusive Monthly Car, Owned Vehicle Fleet, Ownership Alternative, EV Fleet, Delivered To Door |
| `goldfish` | Consumer & Prosumer Software | Local-first AI memory layer for Mac and Windows that drafts in your own tone | secondary | AI Memory, Local-First Desktop App, Context-Aware Writing Assistant, Tone Matching, Cross-App Context Capture, Inline Reply Drafting |
| `honen` | Online Learning / Business Applications | Turns company documents and recordings into structured courses with a 1:1 AI tutor | secondary | AI Course Creation, AI Tutor, Corporate Training Platform, LMS Integration, Workforce Development, Auto-Graded Assessments, Certification Prep |
| `insurf` | Insurance Technology / Vertical Software | The AI-native decision layer for health insurance | secondary | Payer Decisioning, Prior Authorisation, Claims Review, Health Plan Automation, Utilisation Management |
| `levelten` | Market Infrastructure & Exchange / Third-Party Marketplace | Two-sided marketplace for renewable power purchase agreements and clean energy transactions | private | PPA Marketplace, Renewable Energy Procurement, Power Purchase Agreements, Clean Energy Transactions, Developer Marketplace, Energy Price Index |
| `marble` | Vertical Software | The autonomous back-of-house for restaurants | private | Restaurant Back Office, Inventory And Ordering, Food Cost Management, Vendor Invoice Automation, Restaurant Operations |
| `orchids` | Design & Engineering / Data, AI & Developer Tools | The best way to build any app | secondary | AI App Builder, No Code App Generation, Prompt To App, Web App Scaffolding, Vibe Coding |
| `osseus` | Design & Engineering / Data, AI & Developer Tools | The intelligent development platform for robotics | private | Robotics Development Platform, Simulation And Test, Robot Fleet Tooling, Embedded Deployment, Robotics CI |
| `payna` | Vertical Software | AI licensing agent for regulated industries | private | Licensing Compliance, Regulatory Filing Automation, Permit Management, Multi State Licensing, Compliance Workflow |
| `priori-legal` | Freelance & Services Marketplace / Vertical Software | Marketplace of flexible legal talent plus panel and RFP management for in-house teams | private | Legal Talent Marketplace, Flexible Lawyers, Outside Counsel Management, RFP Management, Panel Management, In-House Legal Staffing |
| `projectx` | Cloud & Infrastructure / Data, AI & Developer Tools | Agent native workspace for heavy parallel workflows on the web | secondary | Agent Workspace, Parallel Browser Compute, Headless Runtime, Agent Sandboxing, Cloud Execution Environment |
| `tash` | Wealth & Capital Markets Platform / Third-Party Marketplace | The investment platform for sports and trading cards | private | Collectibles Investing, Fractional Ownership, Trading Card Marketplace, Alternative Assets, Portfolio Tracking |
| `wispr-flow` | Consumer & Prosumer Software / Communications & Collaboration | Voice productivity for your writing and your meetings | secondary, private | Voice Dictation, Speech To Text, Writing Assistant, Desktop Productivity, Hands Free Input |

**core** and **secondary** lanes want LISTED companies with a disclosed revenue figure and an
enterprise value. **private** lanes want FUNDING ROUNDS where the company's revenue or ARR was
disclosed at announcement, 2023 onwards.

## The four that are hardest, and why

- `agentcard` and `unifold` sit in agent payments and multi-chain deposits. Our card-issuing set
  is three names. Anything issuing-led, BaaS, or stablecoin-rails with a disclosed figure helps.
- `tash` is fractional ownership of collectibles. The engine reached for neobanks, which is wrong.
  Collectibles, fractional alternative assets, sports memorabilia marketplaces.
- `wispr-flow` is voice dictation for consumers. It reached for enterprise voice and conversation
  intelligence. Consumer productivity subscriptions with a disclosed ARR are what is missing.
- `marble`, `payna`, `priori-legal` and `osseus` are all vertical software for a specific trade.
  Restaurant back-office, licensing and compliance, legal talent, robotics tooling.

## What NOT to send

- Anything without a revenue figure. It cannot price and it will be rejected on load.
- Aggregator profile pages as the sole source. Crunchbase and PitchBook profiles do not count.
- Companies already in `data/peers-*.csv` or `data/private-rounds*.csv`. Check first.


---

# Part B. Consumer and consumer-education funds

## What this is, corrected on 4 September at 20:02 UK

This section originally said that seven founders were shown nobody to call and that not one house
in the file carried their sector. That was true when it was written and it is no longer the whole
truth: the cause was half an empty shelf and half a vocabulary fault. A house reaches a founder
only when the founder's sector name appears in the house's own sector column as an exact string,
and the enrichment pulls had written the market in their own words ("Personal Software /
Productivity" where our name is "Consumer & Prosumer Software"). That is now translated at read
time, and the seven founders get eight houses each.

**What is left is a real and much narrower gap, which is what this pull is for.**

| our sector name | callable houses that now reach it | what they are |
|---|---|---|
| Consumer & Prosumer Software | 14 | mostly generalists: Accel, Sequoia, Andreessen Horowitz, Index, Dawn, Notion, South Park Commons, Uncork |
| Online Learning | 3 | Founders Factory, Mercia Ventures, SFC Capital |

Three houses is not a call list, and a consumer AI app founder handed four multi-stage generalists
is being told something they already knew. The founders behind this pull are `goldfish` (local-first
AI memory layer), `acti` (agentic mobile keyboard), `welltory` (heart-rate variability tracking),
`planeat` (meal planning), `wondering` (gamified consumer learning) and `befreed` (audio learning).

**So the bar for this pull is specialists, not names.** A generalist that also does consumer is
already here. What is missing is the fund whose portfolio page is mostly consumer apps, or mostly
consumer education, and which led a first cheque into one in the last twelve months.

## What I need back

One CSV, `data/raw/2026-09-04_investor-pull.csv`, with these columns exactly. They are the columns
of `data/investors.csv`, so the file loads without a translation step:

```
investor_key,investor_name,house_type,layer,geographies,stage_bands,first_cheque_low_m,
first_cheque_high_m,cheque_currency,thesis_one_liner,screening_categories,subsectors,
recent_deal_1_company,recent_deal_1_date,recent_deal_1_source_url,recent_deal_2_company,
recent_deal_2_date,recent_deal_2_source_url,cheque_range_source,geographies_source,last_verified
```

**Fifteen houses per cluster, thirty in total, and a house we already hold does not count towards the fifteen.** Six good houses beat twelve loose ones, and a house
that fails any rule below is worth less than no house at all, because a founder who calls a fund
that does not write their cheque stops believing the rest of the page.

## The rules, and they decide whether a row renders at all

1. **Question zero: does this house write FIRST cheques?** The founders here are raising roughly
   $0.5m to $20m. A house that appears in late rounds is not on this list. Write `CALLABLE` in
   `layer` only if the fund leads or co-leads pre-seed, seed or Series A today. If it is a real and
   relevant investor but a growth or crossover house, write `EVIDENCE` and it stays in the database
   without reaching a call list.
2. **A named, dated deal from the last twelve months, with the URL it was read on.** The fund's own
   announcement, the company's own release, or a filing. Crunchbase and PitchBook profile pages do
   not count. Both `recent_deal_1_*` columns are required; the second deal is optional and welcome.
   Date format `YYYY-MM`.
3. **`screening_categories` must use OUR sector names, spelled exactly.** This is the one that
   decides whether the house is ever seen. The engine matches the founder's sector to this column by
   exact string. For this pull the two values are `Consumer & Prosumer Software` and
   `Online Learning`. A house can carry several, separated by `; `. Do not invent names, do not
   translate them into your own words, and do not write "Consumer software" or "EdTech": those match
   nothing and the house becomes invisible, which is the exact failure this pull exists to fix.
   The full vocabulary, if a house genuinely spans more: Business Applications; Card Issuing & BaaS;
   Cloud & Infrastructure; Commerce & Payments Software; Commerce Enablement & Fulfilment;
   Communications & Collaboration; Consumer & Prosumer Software; Consumer Brand; Cross-Border & FX;
   Crypto & Digital Assets; Cybersecurity; Data, AI & Developer Tools; Design & Engineering;
   Digital Bank & Deposits; Financial Data & Index; Freelance & Services Marketplace;
   Insurance Technology; Lending & Credit; Local Delivery & On-Demand;
   Market Infrastructure & Exchange; Marketing & Customer Engagement; Merchant Acquiring & PSP;
   Online Learning; Owned-Inventory Retail; Third-Party Marketplace; Vertical Software;
   Wealth & Capital Markets Platform.
4. **`subsectors` in the fund's own words**, semicolon separated, four at most: what they actually
   back inside the sector ("consumer AI apps; mobile-first subscriptions; health and wearables").
5. **The cheque range is what they publish, never what you estimate.** Fill
   `first_cheque_low_m` / `first_cheque_high_m` in millions with `cheque_currency` (USD, GBP, EUR),
   and put the page it came from in `cheque_range_source`. If the fund publishes no cheque size,
   leave both empty and write `NOT PUBLISHED` in `cheque_range_source`. The card says "first cheque
   not published", which is a fact about the fund and reads as one. An invented range is the one
   error a founder cannot detect.
6. **`stage_bands` is a hard gate**, semicolon separated from `Pre-seed; Seed; Series A; Series B`.
   Use only what the fund states. If it states nothing, leave the cell empty: silence is not a
   claim, and an empty cell keeps the house eligible while a wrong band removes it.
7. **`geographies` in the fund's own words** ("UK and Europe", "US and Canada", "Global"), with the
   page in `geographies_source`. If they publish none, leave it empty.
8. **No contact details of any kind.** No email, no phone, no partner name, no LinkedIn, no logo
   URL. The compliance check strips or refuses them and the row fails on load.
9. **`thesis_one_liner`** is one sentence in the fund's own language about what they back. Not
   marketing prose about how helpful they are.
10. **`last_verified`** is the date you read the page, `YYYY-MM-DD`. `investor_key` is a lowercase
    slug of the name, `house_type` is one of `VC`, `Micro VC`, `Angel syndicate`, `Accelerator`,
    `Family office`, `Corporate VC`.

## Where to look, and what good looks like

**Cluster 1, consumer and prosumer software.** Funds that lead seed rounds in consumer AI apps,
desktop and mobile productivity, personal health and wellbeing apps, and consumer subscriptions.
The test is a named consumer app in their portfolio from the last twelve months, not a stated
interest in consumers.

**Cluster 2, consumer online learning.** Funds writing first cheques into consumer education:
learning apps, audio learning, gamified and self-paced products, creator-led education. Education
funds that only back schools and universities belong in `EVIDENCE`, not on a call list for a
consumer app: the founders here sell subscriptions to individuals.

For both, prefer funds that publish their cheque size and stage, because those are the rows that
render. Angel syndicates and micro funds count and are often the honest answer at pre-seed.

## What NOT to send

- A house with no dated deal in the last twelve months. Activity is the whole feature.
- A house whose sector is written in your words rather than ours. It will load and never be seen.
- An estimated cheque range, an estimated geography, or a stage band the fund does not state.
- Anything from behind a login, and anything with a person's contact details on it.
