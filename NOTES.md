# What the radar found
Snapshot 2026-11-14, source DefiLlama https://api.llama.fi/protocols, fetched 2026-11-14T01:18:33.201Z. 40 watchlist protocols and 160 early-radar protocols were scored; 200 rows made the board.

## The model's claim
A token is worth a multiple of the revenue its protocol can claim, not a multiple of the capital deposited in it. Two protocols with the same TVL are not worth the same if one lends and one bridges. Every row is scored by one function, and the constants it uses are printed on the dashboard.

## The top of the board
- **1. Steakhouse Financial** (Risk Curators) - TVL 2,754M earns 140 bps, so 38.6M of revenue at 26x readiness 0.9288 gives 931M.
- **2. Gauntlet** (Risk Curators) - TVL 1,578M earns 140 bps, so 22.1M of revenue at 26x readiness 0.9545 gives 548M.
- **3. Veda** (Onchain Capital Allocator) - TVL 1,563M earns 135 bps, so 21.1M of revenue at 24x readiness 0.9384 gives 475M.
- **4. USDD** (CDP) - TVL 1,056M earns 85 bps, so 9.0M of revenue at 20x readiness 0.9498 gives 170M.
- **5. Upshift** (Onchain Capital Allocator) - TVL 499M earns 135 bps, so 6.7M of revenue at 24x readiness 1.022 gives 165M.


## Where the model is wrong
The live-token table puts the model's number beside a real market cap. Across the 24 protocols that already trade, the model reads low far more often than high: bridges, lockers and transfer-fee venues sit near zero because their revenue scales with transfers, not with the capital parked in them. Treat a low ratio as a limitation of the model, not as a cheap token.
