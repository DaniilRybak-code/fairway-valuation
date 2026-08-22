/* Result-screen support: the cost card, and the stage anchor it is keyed to.
 *
 * The metric tiles that used to sit at the top of this screen are gone. Handing
 * a founder back the three numbers they typed in four minutes earlier is not a
 * finding, it is filler, and it pushed the football field below the fold.
 */

/* The median post-money for the stage, in the founder's currency. Real, sourced
   and dated, which is why it is the only valuation-scale anchor the free page is
   allowed to use until the peer engine ships. */
function stageAnchorLocal() {
  const anchor = (typeof STAGE_ANCHOR !== 'undefined') ? STAGE_ANCHOR[responses.stage] : null;
  if (!anchor || !anchor.post_median_m) return null;
  const cur = responses.currency || 'USD';
  const v = cur === 'USD' ? anchor.post_median_m : fxConvert(anchor.post_median_m, 'USD', cur);
  return (typeof v === 'number' && isFinite(v)) ? v : null;
}

/* What being priced ten per cent low COSTS.
 *
 * Framed as a loss, not a gain. A founder reads "you could gain £94k" and files
 * it under nice-to-have; they read "being priced 10% low costs you £94k" and
 * they argue. Same arithmetic, and it is the honest direction: the default
 * outcome of walking in without evidence is the lower price, not the higher one. */
function paintCostCard(r) {
  const card = document.querySelector('.cost-card');
  if (!card) return;
  const anchorM = stageAnchorLocal();
  if (!anchorM) { card.style.display = 'none'; return; }
  card.style.display = '';

  const raise = r.raise;
  const preHigh = Math.max(0.1, anchorM - raise);
  const preLow = preHigh / 1.1;
  const dilLow = raise / (preHigh + raise) * 100;
  const dilHigh = raise / (preLow + raise) * 100;
  const pts = dilHigh - dilLow;
  const costNow = (pts / 100) * (preHigh + raise);

  document.getElementById('cost-headline').textContent =
    'Being priced 10% low costs you ' + money(costNow) + ' of this company.';
  document.getElementById('cost-body').textContent =
    'On a ' + money(raise) + ' raise against the ' + (responses.stage || 'stage') + ' median post-money of ' +
    money(anchorM) + ', published by Carta, you give away ' + dilLow.toFixed(1) + '%. Get pushed 10% below it and you give away ' +
    dilHigh.toFixed(1) + '% instead. Nothing about the business changed between those two numbers, only whether you had the evidence to hold the higher one.';
  document.getElementById('cost-future').innerHTML =
    '<strong>Those ' + pts.toFixed(1) + ' points are worth about ' + money(costNow) +
    ' today, and about ' + money(costNow * CONFIG.valuationGrowth12m) + ' if the company is worth ' +
    CONFIG.valuationGrowth12m + ' times as much in twelve months.</strong> ' +
    'You do not get that back at the next round. It is diluted again alongside everything else.';

  const anchorLine = document.getElementById('price-anchor');
  if (anchorLine) {
    anchorLine.textContent = 'One point of a ' + money(anchorM) + ' company, the median at your stage, is worth about ' +
      curSymbol() + Math.round(anchorM * 10000).toLocaleString() + '.';
  }
}
