# -*- coding: utf-8 -*-
"""Dated deals for the fourteen curated funds that had none, so they can render.

Daniil, 3-Sep-2026: "Fourteen investor funds -> go and do the research on them, try to find a
couple of deals for each at least."

Every entry below was confirmed by reading a page that NAMES THE FUND and the round. Candidates
that only appeared on an aggregator, or on the fund's own portfolio page without the fund being
named in the round coverage, were rejected rather than recorded: CuspAI for Hoxton, Luffy AI for
Future Planet, Frontier Health for MMC, Play Padel for Mercia. That is the same standard the
private rounds are held to.

Three caveats travel with the data and are written onto the rows, because a reveal that says
"recently backed X" needs to be true in the sense a founder will read it:
  Future Planet Capital  both deals are its REGIONAL arm, formerly Midven. The main fund's news
                         page has published nothing since 2022.
  Maven and Mercia       these are regional fund deployments (MEIF II, NPIF II) where the house is
                         named as fund manager rather than writing a balance-sheet venture cheque.
  SyndicateRoom          its Access EIS monthly disclosure posts stop after April 2025, so its two
                         deals are 2025 rather than 2026. Its 2026 posts describe follow-on rounds
                         by existing portfolio companies without saying Access EIS took part.
"""
import csv
import io
import sys

PATH = 'data/investors.csv'

DEALS = {
 'Ada Ventures': [
   ('Cascade', '2026-07', 'https://techcrunch.com/2026/07/22/cascade-raises-3-5m-to-help-construction-firms-find-and-win-projects/'),
   ('Gizmo', '2026-04', 'https://techcrunch.com/2026/04/15/ai-learning-app-gizmo-levels-up-with-13m-users-and-a-22m-investment/')],
 'Backed VC': [
   ('Round', '2026-04', 'https://www.finsmes.com/2026/04/round-raises-6m-in-seed-funding.html'),
   ('Novogaia', '2026-01', 'https://www.backed.vc/insights/developing-new-medicines-from-fungi-using-ai')],
 'Concept Ventures': [
   ('Archestra.AI', '2026-06', 'https://archestra.ai/blog/archestra-announces-10m-seed'),
   ('Dex', '2026-04', 'https://fortune.com/2026/04/28/exclusive-dex-ai-powered-recruiting-startup-raises-seed-round-notion-capital/')],
 'Founders Factory': [
   ('Telgea', '2026-06', 'https://app.dealroom.co/news/feed/telgea-raises-funding-from-founders-factory-and-vodafone-to-automate-90-of-telecom-operations-with-ai')],
 'Fuel Ventures': [
   ('PANTA', '2026-05', 'https://www.uktechnews.info/2026/05/14/panta-secures-3-million-seed-investment-led-by-fuel-ventures/'),
   ('Arrival', '2026-04', 'https://www.uktechnews.info/2026/04/14/arrival-raises-500000-pre-seed-funding-from-fuel-ventures/')],
 'Future Planet Capital': [
   ('Furbnow', '2026-07', 'https://bdaily.co.uk/articles/2026/07/24/proptech-firm-heats-up-growth-plans-with-25-million-support'),
   ('Rem3dy Health', '2026-06', 'https://thenextweb.com/news/rem3dy-health-nourished-14m-personalised-nutrition-3d-printing')],
 'Hoxton Ventures': [
   ('Phagos', '2025-10', 'https://www.eu-startups.com/2025/10/paris-based-phagos-raises-e25-million-to-create-a-sustainable-alternative-to-antibiotics/'),
   ('Everbloom', '2025-08', 'https://www.wsgr.com/en/insights/wilson-sonsini-advises-everbloom-on-dollar8-million-financing-to-advance-sustainable-luxury-textiles.html')],
 'LocalGlobe / Latitude': [
   ('Microagi', '2026-07', 'https://sifted.eu/articles/munich-robotics-startup-microagi-raises-55m-germanys-largest-ever-seed-round'),
   ('Trent AI', '2026-04', 'https://www.finsmes.com/2026/04/trent-ai-raises-13m-in-seed-funding.html')],
 'MMC Ventures': [
   ('Fifth Dimension', '2026-05', 'https://www.vestbee.com/insights/articles/london-based-fifth-dimension-raises-26-m-series-a-led-by-hv-capital'),
   ('Cloover', '2026-01', 'https://www.goodwinlaw.com/en/news-and-events/news/2026/01/announcements-technology-goodwin-advises-mmc-ventures-cloover')],
 'Maven Capital Partners': [
   ('Xentra', '2026-07', 'https://www.uktech.news/cybersecurity/cybersecurity-provider-xentra-secures-2-7m-20260720'),
   ('Spirit Health', '2026-07', 'https://www.mavencp.com/latest-news/spirit-healthcare-secures-2-million-debt-finance-package-from-meif-ii')],
 'Mercia Ventures': [
   ('VisaDoc', '2026-08', 'https://www.mercia.co.uk/business-visa-platform-raises-funding-to-meet-overwhelming-demand/'),
   ('TaiSan', '2026-07', 'https://www.mercia.co.uk/taisan-raises-4-65m-to-bring-sodium-ion-batteries-to-mass-market/')],
 'Passion Capital': [
   ('geoSurge', '2026-07', 'https://www.eu-startups.com/2026/07/londons-geosurge-raises-e10-million-to-help-brands-understand-ai-generated-outputs/'),
   ('Paypercut', '2026-06', 'https://tech.eu/2026/06/03/paypercut-secures-eur5m-to-scale-cross-border-payments-in-cee/')],
 'SFC Capital': [
   ('Prema Cognition', '2026-05', 'https://www.uktechnews.info/2026/05/18/prema-cognition-secures-550k-investment-led-by-sfc-capital/'),
   ('Pontiro', '2026-02', 'https://www.uktechnews.info/2026/02/20/pontiro-secures-357500-investment-led-by-sfc-capital/')],
 'SyndicateRoom': [
   ('The Ova', '2025-04', 'https://www.syndicateroom.com/articles/april-2025-investments-summary'),
   ('MindSpire', '2025-03', 'https://www.syndicateroom.com/articles/march-2025-investments-summary')],
}

CAVEAT = {
 'Future Planet Capital': 'Both deals are Future Planet Capital Regional, formerly Midven. The main fund has published no deal news since 2022.',
 'Maven Capital Partners': 'Regional fund deployments (MEIF II) with Maven named as fund manager, not balance-sheet venture cheques.',
 'Mercia Ventures': 'Regional fund deployments (NPIF II) with Mercia named as fund manager. Play Padel excluded: that was Mercia Business Loans, not Mercia Ventures.',
 'SyndicateRoom': 'Access EIS monthly disclosure posts stop after April 2025, so these are the most recent individually disclosed deals rather than 2026 ones.',
 'Founders Factory': 'ONE dated deal only. Immoly is confirmed as a Founders Factory venture on three pages, none of which states a month, so it is not recorded rather than dated by guess.',
}


def main():
    raw = io.open(PATH, encoding='utf-8').read()
    head = ''.join(l for l in raw.splitlines(True) if l.startswith('#'))
    body = [l for l in raw.splitlines(True) if not l.startswith('#')]
    rd = csv.DictReader(body)
    cols, rows = rd.fieldnames, list(rd)
    before = len(rows)
    hit = 0
    for r in rows:
        deals = DEALS.get(r['investor_name'])
        if not deals:
            continue
        for i, (co, dt, url) in enumerate(deals[:2], start=1):
            r['recent_deal_%d_company' % i] = co
            r['recent_deal_%d_date' % i] = dt
            r['recent_deal_%d_source_url' % i] = url
        cav = CAVEAT.get(r['investor_name'])
        if cav and 'deal_note' in cols:
            r['deal_note'] = cav
        hit += 1
    assert len(rows) == before
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=cols, lineterminator='\n')
    w.writeheader()
    for r in rows:
        w.writerow({c: r.get(c, '') for c in cols})
    io.open(PATH, 'w', encoding='utf-8').write(head + buf.getvalue())
    print('rows in %d, rows out %d, funds filled %d of %d' % (before, len(rows), hit, len(DEALS)))
    for name, c in sorted(CAVEAT.items()):
        print('   CAVEAT %s: %s' % (name, c))
    return 0


if __name__ == '__main__':
    sys.exit(main())
