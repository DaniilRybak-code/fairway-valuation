# Ticker request, 4 September 2026. For Daniil, not for an LLM.

**The division of labour, set by Daniil on 4 September.** Claude never pulls Capital IQ. Claude
selects the public NAMES and hands them over as a shopping list; Daniil pulls the data from his own
screen. Anything to do with PRIVATE rounds and investor houses is Claude's own work and lives in
`docs/prompts/work-order-claude-4sep.md`.

**Checked against the universe at 20:45 UK.** The first draft of this list had 41 names. Eighteen of
them are already in the file, which is the most useful thing this document found. What is left is
19 names across six lanes, after four more came out for no longer being listed.

---

## Read this first: two things I got wrong, and one thing the engine is doing

### 1. Four of my names no longer trade. My error, checked at 21:10 UK.

| name | what happened | still listed? |
|---|---|---|
| Sapiens International | Advent take-private, $2.5bn at $43.50 a share, completed | no |
| Learning Technologies Group | General Atlantic take-private, about $1bn, completed | no |
| Udemy | acquired by Coursera, delisted from Nasdaq (Form 25) | no |
| Accolade | acquired by Transcarent, $621m, completed April 2025 | no |

They are out of the list below. None of them is in our data, so nothing we already hold is stale
because of this. The lesson is a rule rather than an apology: **a listed comparable has to still be
listed**, and I proposed four that were not. Nothing in the pipeline checks that today.

These four are not worthless. Every one is a priced control transaction with a disclosed value, and
rulebook B6 already says a control deal prices and carries its label. They are now targets in the
private work order, where they belong.

### 2. Wix and JFrog are in the database. Here is exactly why the engine does not use them.

You are right that they are held, and the honest answer is that two different rules exclude them.

**Wix is excluded by its own tags.** For `orchids` it scores 4.6 against a relative floor of 5.9
(45 per cent of the best score in the universe, 13.2) and an absolute floor of 5.0. It is in the
family and it passes the relevance gate: it simply scores too low, because in our file Wix is
archetyped **Cloud & Infrastructure / Commerce & Payments Software** with buyer **SMB**, while
`orchids` is Design & Engineering / Data, AI & Developer Tools with buyer PROSUMER. No archetype
overlap, different buyer, 1.6 tag points out of a possible 12. That is a tagging judgement, not a
bug: whoever tagged Wix read it as hosting plus payments. I would argue Wix's primary archetype
should be **Design & Engineering** with Commerce & Payments Software secondary, because what Wix
sells is building a site or an app. That is a data ruling and it is yours: it changes which founders
see Wix.

**JFrog and GitLab are excluded by the relevance gate, and they score well above the floor.**

| name | score | floor | family | relevance gate | shared tag tokens |
|---|---|---|---|---|---|
| GitLab | 9.0 | 5.9 | yes | **fails** | 0 |
| JFrog | 6.5 | 5.9 | yes | **fails** | 0 |
| Akamai (for `projectx`) | 6.0 | 5.5 | yes | **fails** | 0 |
| Nutanix (for `projectx`) | 5.1 | 5.5 | yes | passes | 0.1 |

`_relevant` says a candidate must share at least one product-tag token, or share a specific
non-Horizontal industry. GitLab and JFrog share `orchids`' secondary archetype exactly, Data, AI &
Developer Tools, and that counts for nothing in the gate. Both are Horizontal, so the industry route
fails too, and they are dropped despite scoring 9.0 and 6.5.

That gate was added on 26 August, after Publora was handed Perplexity, LangChain and Semrush on
nothing but "developer-facing and consumption-priced". It was right then and it is wrong here.
**My proposal, and it needs your ruling because it will move fixtures: an exact archetype match, in
either slot, should satisfy relevance on its own.** Sharing "Data, AI & Developer Tools" as a named
archetype is a stronger statement than sharing one tag word, and the tag-word test was only ever a
proxy for it. Nutanix is a separate and smaller question: it scores 5.1 against a 5.5 relative
floor, so it is excluded by arithmetic and would arrive with a slightly wider floor.

### 3. Three of my other candidates were simply bad picks

For `goldfish` I proposed Asana (scores 3.0), Box (1.0) and Docebo (0.0), and for `wispr-flow`,
NICE (1.0). The engine is right to refuse them: a corporate learning platform is not a comparable
for a local-first AI memory app. Those are gone from the list.

## What to bring back

The standard listed screen, same columns as `data/peers-fintech.csv`, so the file loads with no
translation step:

```
row,company_name,exchange_ticker,country,market_cap_musd,net_debt_musd,minority_interest_musd,
associates_musd,equity_to_av_bridge_musd,enterprise_value_musd,revenue_ntm_musd,gross_margin_pct,
gross_profit_musd,ev_ntm_revenue_x,ev_ntm_gp_x,revenue_growth_ntm_pct,paying_users_k,
paying_users_basis,revenue_local_cy0,revenue_local_cy2,revenue_growth_cagr_cy0_cy2_pct,
recurring_revenue_pct,as_of,gmv_cy0_musd,gmv_ntm_musd,ev_ntm_gmv_x
```

Two things that matter more than the list:

1. **One screen, one `as_of` date.** The loader treats any row whose `as_of` differs from the newest
   date in the file as stale and refuses to let it price. Pull these in the same run as a refresh of
   the existing names, or the new names load and sit unpriceable until you do.
2. **Every new ticker needs a tag row**, or the loader drops it in silence. That is my job: send me
   the pull before it is loaded and I will write the archetype, industry, function, buyer, motion,
   revenue model, product role, AI stance, product tags and one-line description. This is the join
   that lost 29 lenders on 30 August.

## The list, 19 names

Tickers are my best reading and are to be confirmed on the screen. If one does not resolve, the
company name is the thing I mean.

### `agentcard` — debit cards for AI agents (Card Issuing & BaaS). 5 names
Our card-issuing set is three names. We already hold Pathward Financial.

| company | ticker | why it belongs |
|---|---|---|
| Green Dot | NYSE:GDOT | banking-as-a-service and programme management, the closest listed analogue to issuing as infrastructure |
| Paysign | NASDAQ:PAYS | prepaid and virtual card issuing at small scale, which is where agentcard sits |
| CPI Card Group | NASDAQ:PMTS | card issuance and personalisation, the physical end of the same chain |
| Edenred | ENXTPA:EDEN | issued instruments with programmatic spend controls, the nearest listed read on controlled agent spend |
| Pluxee | ENXTPA:PLX | the Sodexo spin-out, same shape as Edenred and a cleaner read |

### `evergrove` — voice agents for workers' compensation care coordination. 4 names
The engine reached for general insurance software. The business is claims and care coordination.

| company | ticker | why it belongs |
|---|---|---|
| CorVel | NASDAQ:CRVL | workers' compensation claims and care management, the exact end market |
| Crawford & Company | NYSE:CRD.B | claims management and adjusting at scale |
| ExlService | NASDAQ:EXLS | insurance claims operations and analytics |
| Verisk Analytics | NASDAQ:VRSK | claims data and decisioning, the reference point for the asset class |

### `insurf` — the AI decision layer for health insurance. 4 names
Payer decisioning and utilisation management, not general insurtech.

| company | ticker | why it belongs |
|---|---|---|
| Evolent Health | NYSE:EVH | payer decisioning and specialty utilisation management, the direct comparable |
| MultiPlan | NYSE:MPLN | claims pricing and payment integrity for payers |
| Alignment Healthcare | NASDAQ:ALHC | technology-led payer, the buyer's own economics |
| Progyny | NASDAQ:PGNY | managed benefit with a decisioning layer, useful as a margin read |

### `honen` — company documents turned into courses with an AI tutor. 2 names
Corporate training, not consumer learning. We already hold Docebo.

| company | ticker | why it belongs |
|---|---|---|
| Skillsoft | NYSE:SKIL | enterprise training content and platform |
| D2L | TSX:DTOL | learning platform sold to institutions and employers |

**Two names is thin, and the reason is the answer.** Listed corporate learning has been bought out
one company at a time: Learning Technologies Group by General Atlantic, Udemy into Coursera,
Instructure and PowerSchool before them. The public set for this lane is disappearing, which is an
argument for pricing `honen` off precedent transactions rather than off listed comparables. Those
take-privates are in the private work order.

### Three single names for the matcher lanes

| lane | company | ticker | why |
|---|---|---|---|
| `goldfish` | Monday.com | NASDAQ:MNDY | prosumer-to-team productivity on a subscription, the one name in that set we do not hold |
| `projectx` | Confluent | NASDAQ:CFLT | consumption-priced infrastructure sold to developers |
| `wispr-flow` | Verint Systems | NASDAQ:VRNT | speech-to-text and conversation analytics, the enterprise anchor |
| `wispr-flow` | LivePerson | NASDAQ:LPSN | conversational software, useful as the distressed-end boundary |

---

## What I am NOT asking you for

- Enterprise values or multiples for anything private. Those come from announcements and filings and
  they are mine to find.
- Investor or fund data. Also mine.
- Any judgement about whether a name fits. If one looks wrong, say so and I will replace it. That is
  a comparable-selection question and it is the part I am supposed to be able to defend.
