## 1. Seed investors — LANDED PROPERLY, two small things left

Daniil's screen arrived on 2 September and was revised the same day. **Version 2 is the one we
use**: `data/raw/2026-09-02_seed-investor-screen-v2.csv`, **132 deal rows, 66 fund-sector pairs,
52 funds, 8 sectors**, with a new column K carrying the source for each cheque range. Version 1
stays on disk as the record of what it said.

**What v2 fixed.** In v1 the two deals were per fund, not per sector, so Seedcamp carried the same
two companies in all six of its sectors. That proved the fund was active and nothing more, and it
meant no card could say a fund had backed a company like yours. In v2 the two deals are per fund
IN THE NAMED SECTOR, and the file bears it out: of the 9 funds appearing in more than one sector,
none repeats a deal pair. The three rules the sheet sets itself all hold: every pair carries
exactly two deals, no pair's newest deal is older than 2 September 2025, and all 132 rows carry a
cheque-range source. Project A, which failed our activity rule on a June-2025 deal, is simply not
in v2.

**The callable list now renders 124 houses, against 100 on v1 and 73 before the screen.** 60 of
the 140 callable rows band at seed, 46 of those render, and every fork has someone to call at
seed: B2B 6, payments 7, banking and lending 6, marketplaces 8, consumer brands 7, delivery 8,
healthcare 8, insurance 8.

Two things remain, neither of them a pull of any size.

**a. Fourteen of the original curated funds still have no dated deal** and are still refused: Ada
Ventures, Backed VC, Concept Ventures, Founders Factory, Fuel Ventures, Future Planet Capital,
Hoxton Ventures, LocalGlobe / Latitude, MMC Ventures, Maven Capital Partners, Mercia Ventures,
Passion Capital, SFC Capital, SyndicateRoom. If any of them matter, they need the same two columns
the screen has. If they do not, say so and I will drop them, because an unrenderable row is
clutter.

**b. Five rows have a citation problem, and 88 URLs need a text copy.** Three deal links point at
a listing page rather than the announcement: QED for Skalar cites `skalar.de/presse`, Trucks for
Maritime Fusion cites `maritimefusion.com/blog`, Nina for IO Health cites `nina.capital/2025-news`.
Two are attributed to another house: Kfund's Pollen row cites Pale Blue Dot's own portfolio page,
and Felix Capital's Lasso row cites a balderton.com announcement. Separately, 88 of the 132 URLs
are marked low confidence and 19 company names could not be read, because these are photographs of
a screen at an angle. That last part is our transcription limit, not a fault in your pull.

> Paste columns H and J of the version 2 screen as text, all 132 rows, fund and sector alongside
> so the rows can be matched back.

**The geography gap is still open and it is the bigger one.** We hold no country field anywhere:
not on the rounds, not on the company tags, not on our own investor files. The screen fixes this
for its own 52 funds, which carry a real Region. The other 74 promoted houses render in the
broader-fit tier because we cannot match them to a founder's country.

> For each investor in the attached list, state the countries or regions it invests in, with the
> page that says so. Where a fund says "global" or "sector agnostic", say that rather than
> guessing a list.
