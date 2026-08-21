/* Fairway valuation drivers: the content layer.
 *
 * This file is the one the reviewers maintain. It holds what each sector is priced
 * on and what each revenue model implies, plus the logic that assembles those into
 * the drivers a given founder sees. Nothing here is generic: every driver either
 * quotes the founder's own number back or comes from the sector table, and a driver
 * that cannot be tailored is not rendered.
 *
 * Loaded after app.js, which declares `responses`, `track` and `escapeHtml`.
 */

/* ---------------- what actually moves the multiple, by sector ----------------
   One entry per sector. `pays` is what that market rewards, `cuts` is what compresses
   the multiple there, `metric` is the number investors index on before anything else.
   Written to be specific enough that a founder in the sector recognises it. */
const SECTOR_DRIVERS = {
  'SaaS / B2B software': { metric: 'Net revenue retention', pays: 'Net revenue retention above 110% is what separates a software multiple from a services one, because it means the installed base grows without new sales.', cuts: 'Logo churn above 2% a month caps the multiple regardless of new business, since it implies the revenue has to be re-won every three years.' },
  'AI / ML': { metric: 'Gross margin after inference cost', pays: 'Proprietary data or a workflow the model is embedded in, rather than the model itself, because the model is the part that commoditises fastest.', cuts: 'Inference cost inside cost of sales. AI companies routinely report 40% to 60% gross margins where buyers price 75%+, and that gap is applied straight to the multiple.' },
  'Fintech': { metric: 'Revenue net of interchange and funding cost', pays: 'Net revenue after partner and interchange costs, plus a regulatory permission that takes a competitor two years to obtain.', cuts: 'Gross transaction value quoted as revenue. Investors restate it, and the restated multiple is what gets discussed.' },
  'Insurtech': { metric: 'Loss ratio and commission share', pays: 'Distribution economics with a stable loss ratio, or an MGA model where you keep commission without carrying underwriting risk.', cuts: 'Any balance sheet risk. Carrying underwriting moves you from a software multiple to an insurance one, which is a different order of magnitude.' },
  'Healthtech / Digital health': { metric: 'Contracted lives or sites, and reimbursement route', pays: 'A live reimbursement pathway and multi-year contracts with providers or payers, because both make the revenue predictable through a long sales cycle.', cuts: 'Pilot revenue counted as recurring. Pilots that have not converted are valued as pipeline, not as ARR.' },
  'Biotech / Life sciences': { metric: 'Programme stage and IP position', pays: 'Programmes past a de-risking milestone, with composition of matter protection and a credible route to partnering.', cuts: 'Revenue multiples do not apply here at all. Value is priced on risk-adjusted programme value, so the football field is built on precedent rounds and licensing deals instead.' },
  'Medtech / Devices': { metric: 'Regulatory clearance and reimbursement code', pays: 'Clearance already in hand and a reimbursement code, since together they convert a science risk into a commercial one.', cuts: 'Hardware gross margin. Device margins sit well below software and the multiple follows the margin.' },
  'Consumer / D2C': { metric: 'Contribution margin after CAC, and repeat rate', pays: 'Repeat purchase inside 90 days and contribution margin that survives paid acquisition, because that is what makes growth self-funding.', cuts: 'Revenue bought with paid media. Consumer businesses are priced on contribution margin, and a large paid mix pulls the multiple towards retail rather than tech.' },
  'E-commerce / Retail': { metric: 'Contribution margin and inventory turns', pays: 'Own brand with pricing power, high repeat rate and inventory that turns quickly enough not to consume the raise.', cuts: 'Reselling third-party product. Thin gross margin puts you on a retail multiple, typically well under 2x revenue.' },
  'Marketplaces': { metric: 'Net revenue, take rate and liquidity', pays: 'Take rate holding as volume grows, plus repeat activity on both sides, which is the evidence that the marketplace and not the subsidy is doing the work.', cuts: 'Quoting GMV. Investors price net revenue, and a founder who leads with GMV usually gets a lower number than one who leads with take rate.' },
  'Climate / Energy': { metric: 'Contracted offtake and unit economics without subsidy', pays: 'Signed offtake agreements and economics that work at unsubsidised prices, because subsidy risk is what buyers discount hardest.', cuts: 'Project-heavy capital intensity, which shifts pricing towards infrastructure returns rather than software multiples.' },
  'Deeptech / Hardware': { metric: 'Technology readiness level and first commercial contract', pays: 'A first paid commercial deployment and defensible IP, since together they mark the transition from grant funding to a priced business.', cuts: 'Time to revenue. Long development timelines are discounted for the capital needed to reach the next milestone.' },
  'Cybersecurity': { metric: 'Net revenue retention and displacement rate', pays: 'Displacing an incumbent tool rather than adding to the stack, plus expansion inside existing accounts.', cuts: 'A crowded category with a large incumbent. Buyers assume the incumbent ships a good-enough feature and discount accordingly.' },
  'Logistics / Supply chain': { metric: 'Revenue quality: software fee versus freight margin', pays: 'A software or data fee separated cleanly from freight, since that part earns a software multiple and the rest does not.', cuts: 'Blended revenue. Mixing freight and software gets you the lower multiple applied to everything until it is separated.' },
  'Proptech': { metric: 'Recurring share and transaction dependence', pays: 'Revenue tied to a recurring service or a software fee rather than to transaction volume in a cyclical market.', cuts: 'Dependence on transaction volumes, which are priced with a cycle discount because the market can halve.' },
  'Edtech': { metric: 'Retention past the first cohort and B2B mix', pays: 'Institutional or employer contracts that renew, which is what moves you off consumer churn rates.', cuts: 'Consumer subscription churn. High first-90-day churn caps the multiple whatever the growth rate is.' },
  'Legaltech / Regtech': { metric: 'Seats or matters under contract, and renewal rate', pays: 'Multi-year enterprise contracts and a compliance mandate that makes the spend non-discretionary.', cuts: 'Long procurement cycles at law firms and banks, which lengthen payback and are discounted for it.' },
  'HR tech / Future of work': { metric: 'Net revenue retention against headcount changes', pays: 'Pricing that is not purely per-seat, so that revenue does not fall when a customer freezes hiring.', cuts: 'Seat-based pricing in a soft hiring market, where net retention drops below 100% without a single logo lost.' },
  'Adtech / Martech': { metric: 'Net revenue and platform dependence', pays: 'Direct relationships with advertisers and revenue that does not sit inside one platform.', cuts: 'Gross billings quoted as revenue, and dependence on a single platform whose policy change can remove the business.' },
  'Media / Content': { metric: 'Owned audience and revenue per user', pays: 'A first-party audience and diversified revenue, since owned distribution is the asset being bought.', cuts: 'Advertising cyclicality and algorithm dependence, both of which are discounted heavily at seed.' },
  'Gaming': { metric: 'D30 retention and lifetime value against CAC', pays: 'Retention curves that flatten, plus a live-ops cadence that lifts revenue per user over time.', cuts: 'Hit-driven revenue concentration in one title, which is priced as a single-product risk.' },
  'Travel / Hospitality': { metric: 'Net revenue and repeat booking rate', pays: 'Repeat bookings and direct relationships rather than paid intermediated demand.', cuts: 'Seasonality and cyclicality, which widen the range and pull the mid-point down.' },
  'Food / Beverage': { metric: 'Gross margin and velocity per point of distribution', pays: 'Rate of sale in existing doors, which is what a retailer and an investor both look at first.', cuts: 'Physical gross margin and working capital. This is priced on consumer packaged goods multiples, usually a small multiple of revenue.' },
  'Agritech': { metric: 'Contracted acreage or output, and season-over-season retention', pays: 'Multi-season contracts and measurable yield or cost improvement per hectare.', cuts: 'Single-season sales cycles, which mean one bad season resets the growth rate.' },
  'Web3 / Digital assets': { metric: 'Protocol or platform revenue excluding token effects', pays: 'Real fee revenue that would exist without token incentives.', cuts: 'Token-driven activity and regulatory uncertainty, which together produce the widest ranges of any sector we see.' },
  'Defence / Gov tech': { metric: 'Contract vehicle and framework position', pays: 'A place on a framework or an incumbent programme, since that is what converts a long sales cycle into predictable revenue.', cuts: 'Budget cycle timing and procurement length, which stretch payback well beyond commercial norms.' },
  'Telecoms / Connectivity': { metric: 'ARPU, churn and capital intensity', pays: 'Low churn on a contracted base, and asset-light delivery.', cuts: 'Network capital expenditure, which moves the pricing towards infrastructure multiples on EBITDA rather than revenue.' },
  'Mobility / Automotive': { metric: 'Utilisation of the asset, and revenue per vehicle or trip', pays: 'Asset-light models where someone else owns the fleet, plus utilisation high enough to cover depreciation.', cuts: 'Owning the assets. Balance sheet intensity moves the pricing from a software multiple to an infrastructure one.' },
  'Agencies / Professional services': { metric: 'Utilisation, and revenue per head', pays: 'Productised delivery or a recurring retainer, which is the only route to a multiple above the services range.', cuts: 'Revenue that scales with headcount. This is priced on a small multiple of profit, not of revenue, and no growth rate changes that.' },
  'Other': { metric: 'Recurring share and gross margin', pays: 'Contracted, repeatable revenue at software-like gross margin.', cuts: 'Revenue that has to be re-won each period, which is priced on profit rather than on revenue.' }
};

/* Where the multiple set is not revenue-based at all. Used to change the copy honestly
   rather than showing a revenue multiple that no investor in that sector would use. */
const NON_REVENUE_SECTORS = ['Biotech / Life sciences', 'Medtech / Devices'];

/* ---------------- what moves your valuation, tailored ----------------
   Built from sector, stage, size, growth, recurring share and revenue model. Nothing in
   here is a fixed paragraph: every driver either quotes the founder's own number back or
   is drawn from the sector table. If we cannot tailor a driver, we do not show it. */

const MODEL_NOTE = {
  'Subscription / SaaS': 'On a subscription model the argument is won on net revenue retention. Gross retention tells an investor whether the base holds; net tells them whether it grows on its own.',
  'Usage or consumption': 'Usage pricing has no floor, so investors discount for the month a large customer runs less. A committed minimum on your largest accounts removes most of that discount.',
  'Transaction fee / take rate': 'Transaction revenue is priced on whether the take rate holds as volume grows. If it has compressed, show why, before someone assumes it will keep compressing.',
  'Marketplace commission': 'Lead with net revenue, not GMV. Investors restate GMV to net revenue in their own model anyway, and the founder who quotes GMV usually ends up defending a lower number than the one who quoted take rate.',
  'One-off sales or licences': 'One-off revenue has to be re-won every period, so it is valued closer to a services multiple. Any maintenance, support or renewal component should be separated out and shown on its own line.',
  'Services / retainer': 'Services revenue scales with headcount, which is why it is priced on a multiple of profit rather than of revenue. The route to a higher multiple is productising a repeatable part of the delivery.',
  'Advertising': 'Advertising revenue is cyclical and usually concentrated. Show the share coming from your largest three advertisers before you are asked for it.',
  'Hardware plus software': 'Split hardware from software revenue explicitly. Blended, the whole thing gets the hardware multiple; split, the software line can carry its own.',
  'Interest / spread': 'Spread revenue is rate sensitive, so investors will want to see the range at a lower rate environment. Model it rather than waiting for the question.',
  'Other': 'The first thing an investor will do is work out how much of this revenue repeats without a new sale. Answer it before they ask.'
};

function stageNote(stage, arrM) {
  if (stage === 'Series A') {
    return 'At Series A the range is argued on multiples against recent comparable rounds, and the burden of proof sits on why your growth and margin profile deserves to sit above the median of that comp set.';
  }
  if (stage === 'Seed') {
    return arrM >= 0.5
      ? 'At seed with real revenue you are in the narrow band where a multiple can actually be applied. That is an advantage, because a sourced multiple is far easier to defend than a story.'
      : 'At seed with limited revenue, price is usually set by the intersection of the round size and the lead fund ownership target rather than by any multiple. Knowing that target before the meeting is worth more than another slide.';
  }
  return 'At pre-seed there is no published median to anchor against, which is why ranges at this stage are wide. What narrows them is evidence of demand with a date and a price attached to it.';
}

function sizeNote(arrM) {
  if (arrM <= 0) return null;
  if (arrM < 0.25) {
    return { title: 'Size, and why the discount is large here', body: 'At roughly ' + Math.round(arrM * 1000) + 'k of ARR, a listed peer multiple cannot be applied without a substantial size and illiquidity discount. The report states that discount as a number with a reason, rather than burying it inside the range.' };
  }
  if (arrM < 1) {
    return { title: 'Size, and the discount that comes with it', body: 'At about ' + arrM.toFixed(2).replace(/0$/, '') + 'M of ARR you are below the level where a comparable round set gets dense, so the range stays wider than it will be at 1M. The discount to listed peers is still material and should be shown, not assumed.' };
  }
  return { title: 'Size, and where the argument moves next', body: 'Above 1M of ARR the conversation stops being about the story and starts being about which comparable set you belong in. Getting into the right comp set is worth more than any single metric, because it resets the multiple before anything else is discussed.' };
}

function buildDrivers() {
  const out = [];
  const sector = responses.sector === 'Other' ? 'Other' : (responses.sector || 'Other');
  const sd = SECTOR_DRIVERS[sector] || SECTOR_DRIVERS['Other'];
  const monthly = responses.revenue_exact || 0;
  const arrM = monthly * 12 / 1e6;
  const g = responses.growth_exact;
  const rec = responses.recurring_pct;
  const nonRev = NON_REVENUE_SECTORS.indexOf(sector) !== -1;
  /* A founder who chose the band fallback still has revenue, they just have not
     told us the figure. Treat them as revenue-stage and say what the band costs them. */
  const hasRevenue = monthly > 0 || (responses.revenue && responses.revenue !== 'Pre-revenue');

  /* 1. growth, or proof of demand when there is nothing to multiply */
  if (hasRevenue && monthly === 0) {
    out.push({
      title: 'The band you gave is wider than any method behind it',
      body: 'You chose a revenue range rather than a figure, which is fine, but ' + (responses.revenue || 'that band') +
        ' is roughly a three times spread in ARR before a multiple is applied. That alone makes this range wider than the methods that produced it. An exact figure, here or in the reply to the review email, is the single cheapest thing you can do to narrow it.'
    });
  } else if (monthly > 0 && g !== null && g !== undefined && g !== 0) {
    const annual = Math.round((Math.pow(1 + g / 100, 12) - 1) * 100);
    out.push({
      title: 'Growth at ' + g + '% a month is the largest single lever you have',
      body: 'That compounds to roughly ' + annual + '% a year. Revenue multiples are not flat, they are fitted against growth, so this is the input the range is most sensitive to. ' +
        (g >= 15
          ? 'At this rate the risk is not the number, it is that a single acquisition channel is doing all of it. Two channels with independent payback curves removes the discount that assumption creates.'
          : 'At this rate expect the market-size question. The answer is a segment-level view showing growth constrained by your own capacity rather than by demand.')
    });
  } else {
    out.push({
      title: 'With no revenue to multiply, demand evidence is the range',
      body: 'Pre-revenue ranges are argued on proof that someone will pay, not on product. Three named design partners with a start date and a price moves the number further than any traction slide, because it converts an opinion into a dated commitment.'
    });
  }

  /* 2. revenue quality, from the recurring share and the model */
  if (hasRevenue && rec !== null && rec !== undefined) {
    let lead;
    if (rec >= 80) {
      lead = rec + '% of your revenue recurs without a new sale. That is what puts you in the software multiple set rather than the services one, and the gap between those two sets is usually wider than any other single factor on this page.';
    } else if (rec >= 40) {
      lead = rec + '% of your revenue recurs and the rest has to be re-won each period. Investors will value the two parts separately, so present them separately. Blended, the lower multiple tends to get applied to the whole.';
    } else {
      lead = 'Only ' + rec + '% of your revenue recurs. Expect the non-recurring part to be priced closer to a services multiple, which is typically a small multiple of revenue rather than a software one. Moving this number is the highest-value change available to you.';
    }
    const note = MODEL_NOTE[responses.revenue_model] || MODEL_NOTE['Other'];
    out.push({ title: 'Revenue quality, not revenue size', body: lead + ' ' + note });
  }

  /* 3. the sector, from the table */
  out.push({
    title: 'In ' + (responses.sector === 'Other' ? (responses.sector_detail || 'your sector') : sector) + ', the number they index on is ' + sd.metric.toLowerCase(),
    body: sd.pays + ' The other side of it: ' + sd.cuts.charAt(0).toLowerCase() + sd.cuts.slice(1)
  });

  /* 4. size and stage */
  const sz = sizeNote(arrM);
  if (sz && !nonRev) out.push(sz);
  out.push({ title: 'Your stage sets how wide the range starts', body: stageNote(responses.stage, arrM) });

  /* 5. runway, only when it is the binding constraint */
  if (responses.profit === 'Burning, under 12 months runway') {
    out.push({
      title: 'Under twelve months of runway is priced before anything else',
      body: 'A round takes longer than the runway you have, so the price gets set against your deadline rather than against the business. Nothing else in this list outweighs it. Either extend runway before opening the process or arrive with a bridge already committed.'
    });
  }

  if (nonRev) {
    out.splice(1, 0, {
      title: 'Revenue multiples do not apply in this sector',
      body: 'Companies here are priced on programme stage, regulatory position and precedent transactions, not on a multiple of revenue. The football field in your report is built from those instead, which is why it looks different from the software version.'
    });
  }

  return out;
}

function renderDrivers() {
  const list = document.getElementById('drivers-list');
  if (!list) return;
  const drivers = buildDrivers();
  list.innerHTML = '';
  drivers.forEach(function (d, i) {
    const row = document.createElement('div');
    row.className = 'item';
    row.innerHTML = '<div class="num">' + (i + 1) + '</div><div><h3>' +
      escapeHtml(d.title) + '</h3><p>' + escapeHtml(d.body) + '</p></div>';
    list.appendChild(row);
  });
  document.getElementById('drivers-foot').textContent =
    'These are selected for your sector, stage, size and revenue model. They are the levers, not the arithmetic. The report shows which of them your range is actually sitting on, and what each one is worth in points.';
  track('drivers_view', { count: drivers.length, sector: responses.sector || null });
}
