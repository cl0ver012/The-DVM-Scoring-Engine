# DVM Scoring Engine - Final Ranking Logic

## Pre-Filter (Safety Requirements)
ALL tokens must pass these checks before scoring/ranking:

1. **Token Age > 1 hour** - Safety against fresh rugs
2. **No Honeypot/Blacklist** - Must be safe to trade
3. **Tax < 3%** - Reasonable trading fees
4. **Liquidity Locked 100%** - Prevents rug pulls
5. **Volume > $5k (5min)** - Real trading activity
6. **Holders > 100** - Distributed ownership
7. **LP Count > 1** - Multiple liquidity sources
8. **LP/MCap > 0.02** - Adequate liquidity ratio
9. **Top 10 < 30%** - Not too concentrated
10. **Bundle < 40%** - Not heavily botted

## Ranking Categories

After passing pre-filter, tokens are categorized:

### 🆕 New
- **Age Range**: 1-24 hours old
- **Purpose**: Catch early gems
- **Note**: Pre-filter ensures minimum 1 hour age

### 🚀 Surging
- **Age Range**: Any age (> 1 hour from pre-filter)
- **Purpose**: Momentum plays
- **Focus**: Formula-based on price/volume/whale activity

### 📊 All
- **Age Range**: Any age (> 1 hour from pre-filter)
- **Purpose**: General ranking
- **Focus**: Balanced scoring

## Process Flow
```
1. Extract Data (DexScreener, Birdeye, Helius)
2. Apply Pre-Filter (Safety checks including > 1 hour)
3. Calculate Scores (Momentum, Smart Money, Sentiment, Event)
4. Apply Category Filter (New: ≤24h, Others: any age)
5. Rank by Category-Specific Formula
6. Generate AI Report
```

## Key Point
The > 1 hour age requirement in pre-filter ensures ALL tokens shown (regardless of category) have passed the minimum safety threshold.
