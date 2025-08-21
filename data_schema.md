# DVM Scoring Engine - Data Schema

## Required Token Data Fields

Based on the Figma UI design and scoring engine requirements, here are the exact data fields needed for token extraction:

### Core Token Info
```json
{
  "token_address": "string",
  "token_symbol": "string", 
  "token_name": "string",
  "token_age_minutes": "number"
}
```

### Degen Audit
```json
{
  "degen_audit": {
    "is_honeypot": "boolean",
    "has_blacklist": "boolean", 
    "buy_tax_percent": "number",
    "sell_tax_percent": "number"
  }
}
```

### On-Chain Metrics
```json
{
  "liquidity_locked_percent": "number",
  "volume_5m_usd": "number",
  "holders_count": "number",
  "top_10_holders_percent": "number",
  "fees_paid_sol": "number"
}
```

### Momentum Metrics (from Figma UI)
```json
{
  "momentum": {
    "mc_5m": "number",     // Market cap 5min ago
    "vol_5m": "number",    // Volume 5min
    "vol_15m": "number",   // Volume 15min  
    "vol_30m": "number",   // Volume 30min
    "vol_1h": "number",    // Volume 1hour
    "holders_mc": "number", // Holders/MC ratio
    "net_flow": "number",  // Net flow
    "evt_buy": "number",   // Event buy volume
    "tx_buys": "number",   // Transaction buys
    "dev_holdings": "number", // Dev holdings %
    "bundle_holdings": "number", // Bundle holdings %
    "lp_burned": "boolean", // LP burned status
    "mutables": "string"   // Mutable status
  }
}
```

### Smart Money Metrics
```json
{
  "smart_money": {
    "whale_buy_amount": "number",
    "dca_accumulation": "number", 
    "net_inflow": "number",
    "whale_count": "number"
  }
}
```

## Data Sources

- **On-chain metrics**: DexScreener, GMGN.ai, Axiom
- **Degen audit**: GMGN.ai honeypot checker
- **Smart money**: KOL scan, whale tracking
- **Social sentiment**: Twitter/X mentions (when available)

## Sample Data Format

See the JSON snippet in the user's message - that's the exact format our scoring engine expects.
