# Ticker request, 4 September 2026. For Daniil, not for an LLM.

**The division of labour, set by Daniil on 4 September.** Claude never pulls Capital IQ. Claude
selects the public NAMES and hands them over as a shopping list; Daniil pulls the data from his own
screen. Anything to do with PRIVATE rounds and investor houses is Claude's own work and lives in
`docs/prompts/work-order-claude-4sep.md`.

**Checked against the universe at 20:45 UK.** The first draft of this list had 41 names. Eighteen of
them are already in the file, which is the most useful thing this document found. What is left is
23 names across seven lanes, and four lanes turn out not to need a pull at all.

---

## Read this part first: four lanes are not a data problem

| lane | how many of my candidates we already hold | what that means |
|---|---|---|
| `orchids` | 5 of 5: Wix, Appian, Pegasystems, GitLab, JFrog | nothing to pull. The names are in the file and the matcher is not reaching them |
| `projectx` | 4 of 5: DigitalOcean, Fastly, Akamai, Nutanix | one name to pull, the rest is matcher work |
| `goldfish` | 4 of 5: Asana, Box, Cerence, Docebo | one name to pull, the rest is matcher work |
| `wispr-flow` | 3 of 5: SoundHound, Cerence, NICE | two names to pull, the rest is matcher work |

The thin-lane diagnosis said the next best comparable was not in our database. For these four lanes
that reading was wrong, or right only in the narrow sense that our own relevance gate bars the names
before they can be counted. Either way it is my work to fix, not a pull for you: the question is why
a prompt-to-app builder does not reach Wix, and the answer is in the tag vocabulary or the axis-B
gate, not in Capital IQ. I have put it on the status document.

---

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

## The list, 23 names

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

### `evergrove` — voice agents for workers' compensation care coordination. 5 names
The engine reached for general insurance software. The business is claims and care coordination.

| company | ticker | why it belongs |
|---|---|---|
| CorVel | NASDAQ:CRVL | workers' compensation claims and care management, the exact end market |
| Crawford & Company | NYSE:CRD.B | claims management and adjusting at scale |
| ExlService | NASDAQ:EXLS | insurance claims operations and analytics |
| Sapiens International | NASDAQ:SPNS | core insurance software including claims |
| Verisk Analytics | NASDAQ:VRSK | claims data and decisioning, the reference point for the asset class |

### `insurf` — the AI decision layer for health insurance. 5 names
Payer decisioning and utilisation management, not general insurtech.

| company | ticker | why it belongs |
|---|---|---|
| Evolent Health | NYSE:EVH | payer decisioning and specialty utilisation management, the direct comparable |
| MultiPlan | NYSE:MPLN | claims pricing and payment integrity for payers |
| Accolade | NASDAQ:ACCD | care navigation sold to payers and employers |
| Alignment Healthcare | NASDAQ:ALHC | technology-led payer, the buyer's own economics |
| Progyny | NASDAQ:PGNY | managed benefit with a decisioning layer, useful as a margin read |

### `honen` — company documents turned into courses with an AI tutor. 4 names
Corporate training, not consumer learning. We already hold Docebo.

| company | ticker | why it belongs |
|---|---|---|
| Skillsoft | NYSE:SKIL | enterprise training content and platform |
| D2L | TSX:DTOL | learning platform sold to institutions and employers |
| Learning Technologies Group | AIM:LTG | corporate learning and talent, UK-listed |
| Udemy | NASDAQ:UDMY | its business segment is enterprise upskilling, which is honen's market |

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
