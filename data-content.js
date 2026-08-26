/* Content tables. The reviewers edit this file; nothing here is logic.
 *
 * Split out of app.js so a copy change is a small diff and a logic change is a
 * separate one. Loaded BEFORE app.js.
 *
 * Every investor entry must be true of a fund that is actually active at this
 * stage in that sector. Every concern must be one a founder would recognise.
 */

const SECTORS = [
  'SaaS / B2B software', 'AI / ML', 'Fintech', 'Insurtech',
  'Healthtech / Digital health', 'Biotech / Life sciences', 'Medtech / Devices',
  'Consumer / D2C', 'E-commerce / Retail', 'Marketplaces',
  'Climate / Energy', 'Deeptech / Hardware', 'Cybersecurity',
  'Logistics / Supply chain', 'Proptech', 'Edtech',
  'Legaltech / Regtech', 'HR tech / Future of work', 'Adtech / Martech',
  'Media / Content', 'Gaming', 'Travel / Hospitality', 'Food / Beverage',
  'Agritech', 'Web3 / Digital assets', 'Defence / Gov tech',
  'Telecoms / Connectivity', 'Mobility / Automotive',
  'Agencies / Professional services', 'Other'
];

/* How the revenue is earned. Single select. This changes which multiple set applies
   more than sector does in several cases, which is why it is asked separately. */
const REVENUE_MODELS = [
  'Subscription / SaaS', 'Usage or consumption', 'Transaction fee / take rate',
  'Marketplace commission', 'One-off sales or licences', 'Services / retainer',
  'Advertising', 'Hardware plus software', 'Interest / spread', 'Other'
];

/* Display only. All maths runs in the founder's own currency, because a multiple is a
   ratio and does not need converting. The one place a rate is used is the US dollar
   stage anchor on the field, and that is converted at a published ECB rate with a date. */
const CURRENCY_SYMBOL = {
  USD: '$', EUR: '€', GBP: '£', CAD: 'C$'
};

const CONCERNS = [
  'Valuation looks high', 'Market size', 'Traction is early', 'Unit economics',
  'Churn or retention', 'Competition', 'Team gaps', 'Regulatory risk',
  'Concentration in a few customers', 'Nothing specific yet'
];

const INVESTORS = {
  'SaaS / B2B software': [
    { name: 'Playfair Capital', note: 'AI, enterprise software and developer tools. First cheques £100k to £1.5M.' },
    { name: 'Episode 1 Ventures', note: 'UK-only B2B software. £250k to £3M.' },
    { name: 'Concept Ventures', note: 'AI, deep tech and infrastructure software. Around £1M average first cheque.' }
  ],
  'AI / ML': [
    { name: 'Concept Ventures', note: 'AI, deep tech and infrastructure software. Around £1M average first cheque.' },
    { name: 'MMC Ventures', note: 'AI-first companies. Around $3.2M average seed cheque.' },
    { name: 'Playfair Capital', note: 'AI, enterprise software and developer tools. £100k to £1.5M.' }
  ],
  'Fintech': [
    { name: 'Seedcamp', note: 'Fintech, AI, developer tools and marketplaces. First cheques $350k to $1M.' },
    { name: 'Passion Capital', note: 'Fintech, insurtech and marketplaces. £1M to £2M.' },
    { name: 'LocalGlobe / Latitude', note: 'Fintech, health, climate and marketplaces. £500k to £2M at seed.' }
  ],
  'Insurtech': [
    { name: 'Passion Capital', note: 'Fintech, insurtech and marketplaces. £1M to £2M.' },
    { name: 'Octopus Ventures', note: 'Fintech, B2B SaaS, health and climate. Active seed through Series A.' },
    { name: 'Seedcamp', note: 'Fintech, AI, developer tools and marketplaces. $350k to $1M.' }
  ],
  'Healthtech / Digital health': [
    { name: 'Octopus Ventures', note: 'Healthtech and biotech alongside B2B SaaS. Active seed through Series A.' },
    { name: 'Ada Ventures', note: 'Healthy ageing and economic empowerment theses. £250k to £1.5M.' },
    { name: 'Mercia Ventures', note: 'Life sciences, software and deeptech. Among the most active UK early-stage funds by deal count.' }
  ],
  'Biotech / Life sciences': [
    { name: 'Mercia Ventures', note: 'Life sciences, software and deeptech. Among the most active UK early-stage funds by deal count.' },
    { name: 'Future Planet Capital', note: 'Deeptech, health and engineering biology out of the university ecosystem.' },
    { name: 'Backed VC', note: 'AI therapeutics and frontier science. $500k to $5M.' }
  ],
  'Consumer / D2C': [
    { name: 'Hoxton Ventures', note: 'Broad tech with a consumer and fintech lean. $500k to $5M.' },
    { name: 'Fuel Ventures', note: 'B2C and B2B via SEIS/EIS. High early-stage deal volume. £100k to £1M.' },
    { name: 'Cherry Ventures', note: 'Europe-wide, sector-agnostic at seed. €2M to €7M.' }
  ],
  'Marketplaces': [
    { name: 'Seedcamp', note: 'Marketplaces, fintech, AI and developer tools. First cheques $350k to $1M.' },
    { name: 'Fuel Ventures', note: 'B2B SaaS and marketplaces via SEIS/EIS. £100k to £1M.' },
    { name: 'Passion Capital', note: 'Marketplaces, fintech and insurtech. £1M to £2M.' }
  ],
  'Climate / Energy': [
    { name: 'Octopus Ventures', note: 'Climate tech alongside B2B SaaS and deeptech. Active seed through Series A.' },
    { name: 'Ada Ventures', note: 'Climate equity thesis. £250k to £1.5M.' },
    { name: 'Future Planet Capital', note: 'Climate, deeptech and engineering biology. High early-stage deal volume.' }
  ],
  'Deeptech / Hardware': [
    { name: 'Concept Ventures', note: 'Deep tech, AI and infrastructure software. Around £1M average first cheque.' },
    { name: 'Mercia Ventures', note: 'Deeptech, life sciences and software. Among the most active UK early-stage funds.' },
    { name: 'Future Planet Capital', note: 'Deeptech, space, defence and engineering biology.' }
  ],
  'Cybersecurity': [
    { name: 'Playfair Capital', note: 'Enterprise software, AI and developer tools. £100k to £1.5M.' },
    { name: 'Episode 1 Ventures', note: 'UK-only B2B software including infrastructure and security. £250k to £3M.' },
    { name: 'Octopus Ventures', note: 'B2B SaaS and deeptech. Active seed through Series A.' }
  ],
  'Logistics / Supply chain': [
    { name: 'Maven Capital Partners', note: 'SaaS, transport and energy. Among the most active UK early-stage investors by deal count.' },
    { name: 'Fuel Ventures', note: 'B2B SaaS and marketplaces via SEIS/EIS. £100k to £1M.' },
    { name: 'Backed VC', note: 'Manufacturing and automation alongside frontier tech. $500k to $5M.' }
  ],
  'Proptech': [
    { name: 'Fuel Ventures', note: 'B2B SaaS and marketplaces via SEIS/EIS. £100k to £1M.' },
    { name: 'Concept Ventures', note: 'Infrastructure software and AI. Around £1M average first cheque.' },
    { name: 'SFC Capital', note: 'The most active UK early-stage investor by deal count. SEIS-led, £100k to £300k.' }
  ],
  'Edtech': [
    { name: 'Founders Factory', note: 'Multi-sector early-stage via corporate partners. £30k to £250k.' },
    { name: 'SFC Capital', note: 'The most active UK early-stage investor by deal count. SEIS-led, £100k to £300k.' },
    { name: 'Mercia Ventures', note: 'Software and consumer alongside deeptech. High early-stage deal volume.' }
  ],
  'Other': [
    { name: 'SFC Capital', note: 'The most active UK early-stage investor by deal count. SEIS-led, £100k to £300k.' },
    { name: 'SyndicateRoom', note: 'Sector-agnostic, high-volume early-stage syndicate.' },
    { name: 'Fuel Ventures', note: 'B2B SaaS, marketplaces and fintech via SEIS/EIS. £100k to £1M.' }
  ]
};

const FIX_BY_REVENUE = {
  'Pre-revenue': { title: 'Turn your pipeline into signed evidence.', body: 'Three named design partners with a start date and a price does more for a pre-revenue range than any traction slide. At this stage the range is priced on proof of demand, not on product.' },
  'Under $10k/mo': { title: 'Show retention before you show growth.', body: 'At this revenue the first question is whether the early customers stay. A three-month cohort chart pre-empts it and defends the top of your range. A cumulative revenue line invites it.' },
  '$10k–$50k/mo': { title: 'Lead with gross margin and net revenue retention, not top line.', body: 'At this level the range is set by the quality of the revenue rather than the size of it. Gross margin, NRR and payback are the three numbers that move it.' },
  '$50k–$150k/mo': { title: 'Bring CAC payback by channel.', body: 'At this revenue the objection is efficiency, not demand. Payback in months, split by channel, moves the range further than another month of growth does.' },
  '$150k+/mo': { title: 'Expect the range to be argued on multiples, not story.', body: 'Above this level the conversation moves to ARR multiples against recent comparable rounds. The defensible argument is why your growth and margin profile sits above the median for that comp set.' }
};

const FIX_BY_GROWTH = {
  'Too early to measure': { title: 'The team is currently the only asset being priced.', body: 'Pre-traction ranges are argued on founder-market fit and on what the first 90 days after close will prove. Both need to be explicit and dated, or the range defaults to the bottom of the band.' },
  'Growing, under 100% a year': { title: 'This growth rate will be read as a market-size problem.', body: 'Steady growth invites the question of whether the ceiling is low. The answer is a segment-level breakdown showing where growth is constrained by your capacity rather than by demand.' },
  'Growing, 100% or more a year': { title: 'This growth is probably being attributed to one channel.', body: 'Fast growth gets discounted when it looks like a single acquisition channel that will saturate. Two channels with independent payback curves removes the discount.' }
};

const FIX_BY_PROFIT = {
  'Profitable': { title: 'Profitability at this stage invites a growth-ceiling question.', body: 'Investors read early profitability either as discipline or as under-investment. The defence is showing what happens to growth once the round is deployed, modelled rather than asserted.' },
  'Around break-even': { title: 'Break-even makes the raise itself the question.', body: 'If you do not need the money to survive, the round has to be justified by what it accelerates. Tie the raise to a specific milestone and to the timeline for reaching it without the money.' },
  'Burning, 12+ months runway': { title: 'Your burn multiple will be checked before your growth rate.', body: 'Net new revenue divided by net burn is the number that decides whether growth is being bought or earned. Bring it before you are asked for it.' },
  'Burning, under 12 months runway': { title: 'Your runway is shorter than the raise will take.', body: 'Under twelve months, the round gets priced against your deadline rather than your business. Either extend runway before opening the process or arrive with a bridge already committed. This is the single largest downward pressure on your range.' }
};

const hooks = {
  frustration: {
    kicker: '',
    headline: 'We pick your comparables. Then we defend them.',
    sub: 'The number depends entirely on which companies you are held against. We choose yours deliberately, show you why each one is in the set, and source every figure behind it.',
    cta: 'Try it free'
  },
  readiness: {
    kicker: 'Before your next raise',
    headline: 'Are you actually ready to defend your valuation?',
    sub: 'Nine questions, four minutes. You get the football field a banker would build, the three concerns investors will raise against it, and the funds writing cheques into your sector right now. Reviewed by former bulge bracket bankers.',
    cta: 'Find out in four minutes'
  },
  reveal: {
    kicker: 'The number problem',
    headline: 'Two founders with the same metrics raise at $2M and $4M.',
    sub: 'The difference is rarely the business. It is whether the number survives being pushed on. Nine questions gets you every method that prices you, the concerns coming at it, and a banker review of both.',
    cta: 'Show me the methods'
  }
};
