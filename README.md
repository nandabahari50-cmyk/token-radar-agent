[![make.fun · token-radar-01](https://make.fun/badge/token-radar-01.svg)](https://make.fun/bounty/token-radar-01?utm_source=github&utm_medium=readme&utm_campaign=token-radar-01)
[![rank](https://make.fun/badge/token-radar-01/nandabahari50-cmyk/token-radar-agent/rank.svg)](https://make.fun/bounty/token-radar-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=token-radar-01)
[![reward](https://make.fun/badge/token-radar-01/nandabahari50-cmyk/token-radar-agent/reward.svg)](https://make.fun/bounty/token-radar-01?utm_source=github&utm_medium=readme&utm_campaign=token-radar-01)

# Token Radar

A ranked board of DeFi protocols that have no token yet, ordered by what their token would be
worth if one launched, plus a farm plan for each one.

Built for the make.fun `token-radar-01` bounty. The scoring runs in a sandbox with no network
access; every number comes from `input/snapshot.json`.

## Run it

```
node main.ts --input input/snapshot.json --output out
```

`main.ts` writes five artefacts to `out/`:

- `board.json` - 200 rows, ranked, each with its implied value and its farm plan
- `data.js` - the same board in the shape the dashboard reads
- `dashboard/` - the page itself, three files, no network and no build step
- `screenshots/` - the board, one detail view, a filtered view, and the model panel
- `dossier.json` - the bundle the grader rebuilds from this output

Open `out/dashboard/index.html` with `data.js` beside it. Nothing is fetched at runtime.

## The model

TVL is deposited capital, not income. The board therefore prices revenue:

```
revenue   = tvl_usd * earn_bps(category) / 10000
trend     = 1 + clamp(change_7d, -100, 100) / 100 * 0.35
maturity  = 0.75 + min(age_days, 730) / 730 * 0.25
readiness = clamp(trend * maturity, 0.35, 1.35)
implied   = round(revenue * multiple(category) * readiness)
```

`earn_bps` is the annual spread a category keeps on its TVL: a lending market keeps the spread
between what it charges borrowers and what it pays suppliers, a DEX keeps a cut of the volume it
routes, a bridge keeps a fee on a transfer. `multiple` is what the market pays per dollar of that
revenue. The full table for 32 categories is on the dashboard, because a model whose constants
are hidden cannot be argued with.

Nothing is special-cased by name. Every row goes through the same function, and the page
recomputes each row's number from the snapshot figures: if the page's arithmetic and
`board.json` ever disagree, the page says so instead of hiding it.

## Where the model is wrong

The dashboard's live-token view puts the model's number beside a real market cap. Bridges,
lockers and transfer-fee venues come out near zero, because the model reads their revenue as a
share of the capital parked in them when it is really a fee per transfer. Where the ratio is low
the model is wrong, not the token cheap. That view is the calibration check for everything else.

## Verifying a run

`tools/shots.py` re-renders the screenshots from the built dashboard with Playwright, so the
images a submission carries are always the dashboard that submission ships.

## Licence

MIT.

