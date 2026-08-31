# TO DO: the CAGR refresh, 192 listed names

**Owner: Daniil. Status: OPEN, promised for the next dataset refresh.**
Written 31 August 2026 after his ruling on growth ranking.

## The ruling this comes from

His words, 31 August:

> In general, for growth - we need to take longer-term numbers to rank the peers (i.e. the CAGR).
> Year 1 and 2 numbers are only there to estimate the TPV / GMV, where available, but should not
> be used to categorise the peers.

That is now wired. `match_reference.py` carries a separate field, `g_rank`, which is populated only
when the growth basis starts with CAGR. The scorer and the band filter both read `g_rank`, not `g`.
A row whose only growth figure is a single forward year no longer votes on how fast a peer grows.

## What the ruling costs us until the refresh lands

Reproduce with:

    cd selector && python3 -c "import match_reference as M; \
      print(sum(1 for r in M.listed if r.get('g_rank') is not None), 'of', len(M.listed))"

Today: **321 of 513 listed rows can rank on growth. 192 cannot.** Those 192 hold `g_basis=NTM` —
one forward year, no multi-year series. They still price, they still match on business nature, they
still appear in a range. They are simply invisible to the growth dimension of the match, which is
one of the three things the selector reads after family and archetype.

Split of the 192: **105 consumer, 75 fintech, 12 software.** The consumer file takes the worst of
it, which matters because consumer is where the growth spread between a hypergrowth D2C brand and a
mature retailer is widest.

## What is needed

`docs/cagr-needed-pull-list.tsv` — 192 rows, tab separated, pastable into Excel. Columns:
exchange ticker, company name, family, archetype, what is needed.

For each name: **revenue CAGR from CY+0 to CY+2, in local currency.** Local currency, because the
growth rate must not carry an FX movement inside it — that was the Wise error on 31 August, where a
sterling year sat next to a dollar year and printed as a 10.9% decline.

If the export can carry CY+0 through CY+3, take it: 72 rows already sit on `CAGR_CY1_CY3` and a
consistent CY+0 to CY+2 window across the whole file would let the bands be refit on one basis
instead of two.

## What happens when it arrives

1. The 192 rows get their CAGR and `g_basis` moves from NTM to CAGR_CY0_CY2.
2. `python3 tools/refit_growth_bands.py` — the MATURE / GROWING / HYPER boundaries were last fit on
   51 rates. With 513 they move, and they should.
3. Re-run the golden suite. Fixtures WILL move, and that is the point: today they are being ranked
   by a growth dimension that two in five peers cannot participate in.
4. Update this file's status to CLOSED and strike the line in the tracker.

## Standing caution

Nothing here is urgent enough to block the pilot. It is urgent enough that the peer ordering inside
a range is not yet fully evidenced for 37% of the listed universe, and a founder reading the range
would not know that. Until it closes, the growth ranking is honest but partial.
