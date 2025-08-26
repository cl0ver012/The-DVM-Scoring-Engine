// Comprehensive demo data for realistic demonstrations

export const DEMO_METRICS = {
  'high-quality': {
    // Momentum metrics - showing strong growth
    momentum: {
      vol_over_avg_ratio: 4.5,  // 450% of average volume
      price_change_percent: 38.7,  // 38.7% price increase
      ath_hit: true,  // Hit all-time high
      lp_mcap_delta_percent: 15.2,  // LP growing faster than market cap
      holders_growth_percent: 18.9  // 18.9% holder growth
    },
    // Smart money metrics - whales accumulating
    smart_money: {
      whale_buy_usd: 678000,  // $678k whale buys
      whale_buy_supply_percent: 8.5,  // Whales bought 8.5% of supply
      dca_accumulation_supply_percent: 3.2,  // 3.2% being DCA'd
      net_inflow_wallets_gt_10k_usd: 456000  // $456k net inflow from big wallets
    },
    // Sentiment metrics - viral growth
    sentiment: {
      mentions_velocity_ratio: 5.2,  // 520% increase in mentions
      tier1_kol_buy_supply_percent: 2.8,  // Top KOLs bought 2.8%
      influencer_reach: 2897000,  // 2.9M total reach
      polarity_positive_percent: 85  // 85% positive sentiment
    },
    // Event metrics - major catalysts
    event: {
      inflow_over_mcap_percent: 12.5,  // 12.5% of mcap flowing in
      liquidity_outflow_percent: -2.1,  // 2.1% liquidity added (negative = inflow)
      upgrade_or_staking_live: true  // Major upgrade or staking launched
    }
  },
  'average-token': {
    // Momentum metrics - moderate growth
    momentum: {
      vol_over_avg_ratio: 1.8,  // 180% of average volume
      price_change_percent: 8.9,  // 8.9% price increase
      ath_hit: false,  // Not at ATH
      lp_mcap_delta_percent: 3.4,  // LP growing slightly
      holders_growth_percent: 4.5  // 4.5% holder growth
    },
    // Smart money metrics - some interest
    smart_money: {
      whale_buy_usd: 45000,  // $45k whale buys
      whale_buy_supply_percent: 2.1,  // Whales bought 2.1% of supply
      dca_accumulation_supply_percent: 0.8,  // 0.8% being DCA'd
      net_inflow_wallets_gt_10k_usd: 23000  // $23k net inflow from big wallets
    },
    // Sentiment metrics - normal activity
    sentiment: {
      mentions_velocity_ratio: 1.5,  // 150% increase in mentions
      tier1_kol_buy_supply_percent: 0.6,  // Top KOLs bought 0.6%
      influencer_reach: 378000,  // 378k total reach
      polarity_positive_percent: 60  // 60% positive sentiment
    },
    // Event metrics - few catalysts
    event: {
      inflow_over_mcap_percent: 3.2,  // 3.2% of mcap flowing in
      liquidity_outflow_percent: 1.5,  // 1.5% liquidity removed
      upgrade_or_staking_live: false  // No major upgrades
    }
  },
  'failed-prefilter': {
    // Momentum metrics - declining
    momentum: {
      vol_over_avg_ratio: 0.5,  // 50% of average volume (declining)
      price_change_percent: -17.8,  // -17.8% price drop
      ath_hit: false,  // Far from ATH
      lp_mcap_delta_percent: -8.9,  // LP shrinking faster than market cap
      holders_growth_percent: -8.9  // -8.9% holders leaving
    },
    // Smart money metrics - dumping
    smart_money: {
      whale_buy_usd: 2000,  // Only $2k whale buys
      whale_buy_supply_percent: 0.1,  // Whales bought only 0.1% of supply
      dca_accumulation_supply_percent: 0,  // No DCA activity
      net_inflow_wallets_gt_10k_usd: -89000  // -$89k net outflow from big wallets
    },
    // Sentiment metrics - negative
    sentiment: {
      mentions_velocity_ratio: 0.3,  // 30% of previous mentions (declining)
      tier1_kol_buy_supply_percent: 0,  // No KOL interest
      influencer_reach: 45000,  // Only 45k reach
      polarity_positive_percent: 18  // Only 18% positive sentiment
    },
    // Event metrics - no catalysts
    event: {
      inflow_over_mcap_percent: -5.6,  // -5.6% outflow relative to mcap
      liquidity_outflow_percent: 8.9,  // 8.9% liquidity removed
      upgrade_or_staking_live: false  // No upgrades
    }
  }
}

// Realistic token data for ranking demos
export const RANKING_DEMO_DATA = {
  'top-performers': [
    {
      id: 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
      symbol: 'USDC',
      name: 'USD Coin',
      price_now: 1.0001,
      price_change_pct: 0.01,
      mc_now: 2845000000,
      mc_change_pct: 0.02,
      vol_now: 487000000,
      vol_change_pct: 15.3,
      vol_to_mc: 0.171,
      lp_now: 89000000,
      lp_change_pct: 2.1,
      lp_count: 127,
      holders_now: 1245000,
      holders_change_pct: 0.8,
      holders_per_mc: 0.000437,
      netflow_now: 12000000,
      netflow_change_pct: 45.2,
      whale_buy_count: 89,
      kolusd_now: 2300000,
      kolusd_change_pct: 34.5,
      kol_velocity: 1.87,
      tx_now: 45678,
      tx_change_pct: 12.3,
      netbuy_usd_now: 8900000,
      fee_sol_now: 234.5,
      fee_to_mc_pct: 0.0082,
      minutes_since_peak: 15,
      top10_pct: 12.3,
      bundle_pct: 8.7,
      dca_flag: 1,
      ath_flag: 0
    },
    {
      id: 'So11111111111111111111111111111111111111112',
      symbol: 'SOL',
      name: 'Wrapped SOL',
      price_now: 196.45,
      price_change_pct: 5.67,
      mc_now: 91234000000,
      mc_change_pct: 6.12,
      vol_now: 2345000000,
      vol_change_pct: 23.4,
      vol_to_mc: 0.0257,
      lp_now: 456000000,
      lp_change_pct: 8.9,
      lp_count: 234,
      holders_now: 3456000,
      holders_change_pct: 2.3,
      holders_per_mc: 0.0000379,
      netflow_now: 45000000,
      netflow_change_pct: 67.8,
      whale_buy_count: 156,
      kolusd_now: 8900000,
      kolusd_change_pct: 45.6,
      kol_velocity: 2.34,
      tx_now: 123456,
      tx_change_pct: 18.9,
      netbuy_usd_now: 34000000,
      fee_sol_now: 567.8,
      fee_to_mc_pct: 0.0062,
      minutes_since_peak: 8,
      top10_pct: 8.9,
      bundle_pct: 5.4,
      dca_flag: 1,
      ath_flag: 1
    },
    {
      id: 'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB',
      symbol: 'USDT',
      name: 'Tether USD',
      price_now: 0.9998,
      price_change_pct: -0.02,
      mc_now: 3123000000,
      mc_change_pct: 0.01,
      vol_now: 234000000,
      vol_change_pct: 8.7,
      vol_to_mc: 0.0749,
      lp_now: 67000000,
      lp_change_pct: 1.2,
      lp_count: 98,
      holders_now: 987000,
      holders_change_pct: 0.5,
      holders_per_mc: 0.000316,
      netflow_now: 5600000,
      netflow_change_pct: 12.3,
      whale_buy_count: 45,
      kolusd_now: 890000,
      kolusd_change_pct: 23.4,
      kol_velocity: 0.98,
      tx_now: 23456,
      tx_change_pct: 6.7,
      netbuy_usd_now: 3400000,
      fee_sol_now: 123.4,
      fee_to_mc_pct: 0.0039,
      minutes_since_peak: 45,
      top10_pct: 15.6,
      bundle_pct: 12.3,
      dca_flag: 0,
      ath_flag: 0
    }
  ],
  'mixed-quality': [
    {
      id: 'NewMemeCoin123456789',
      symbol: 'MEME',
      name: 'New Meme Coin',
      price_now: 0.00000234,
      price_change_pct: 234.5,
      mc_now: 2345000,
      mc_change_pct: 189.3,
      vol_now: 890000,
      vol_change_pct: 456.7,
      vol_to_mc: 0.3795,
      lp_now: 45000,
      lp_change_pct: 123.4,
      lp_count: 3,
      holders_now: 1234,
      holders_change_pct: 89.2,
      holders_per_mc: 0.000526,
      netflow_now: 23000,
      netflow_change_pct: 234.5,
      whale_buy_count: 12,
      kolusd_now: 34000,
      kolusd_change_pct: 567.8,
      kol_velocity: 4.56,
      tx_now: 2345,
      tx_change_pct: 123.4,
      netbuy_usd_now: 45000,
      fee_sol_now: 12.3,
      fee_to_mc_pct: 0.0052,
      minutes_since_peak: 2,
      top10_pct: 35.6,
      bundle_pct: 28.9,
      dca_flag: 1,
      ath_flag: 1
    },
    {
      id: 'RugPullToken987654321',
      symbol: 'RUG',
      name: 'Suspicious Token',
      price_now: 0.0000000123,
      price_change_pct: -78.9,
      mc_now: 12300,
      mc_change_pct: -82.1,
      vol_now: 2340,
      vol_change_pct: -67.8,
      vol_to_mc: 0.1902,
      lp_now: 1200,
      lp_change_pct: -45.6,
      lp_count: 1,
      holders_now: 45,
      holders_change_pct: -34.5,
      holders_per_mc: 0.00366,
      netflow_now: -8900,
      netflow_change_pct: -234.5,
      whale_buy_count: 0,
      kolusd_now: 0,
      kolusd_change_pct: -100,
      kol_velocity: 0,
      tx_now: 12,
      tx_change_pct: -89.2,
      netbuy_usd_now: -5600,
      fee_sol_now: 0.1,
      fee_to_mc_pct: 0.0081,
      minutes_since_peak: 180,
      top10_pct: 89.5,
      bundle_pct: 67.8,
      dca_flag: 0,
      ath_flag: 0
    },
    {
      id: 'StableProject555555555',
      symbol: 'STABLE',
      name: 'Stable Growth Token',
      price_now: 0.0234,
      price_change_pct: 12.3,
      mc_now: 5670000,
      mc_change_pct: 15.6,
      vol_now: 234000,
      vol_change_pct: 23.4,
      vol_to_mc: 0.0413,
      lp_now: 123000,
      lp_change_pct: 8.9,
      lp_count: 5,
      holders_now: 3456,
      holders_change_pct: 12.3,
      holders_per_mc: 0.00061,
      netflow_now: 12000,
      netflow_change_pct: 34.5,
      whale_buy_count: 8,
      kolusd_now: 23000,
      kolusd_change_pct: 45.6,
      kol_velocity: 1.23,
      tx_now: 1234,
      tx_change_pct: 23.4,
      netbuy_usd_now: 8900,
      fee_sol_now: 3.4,
      fee_to_mc_pct: 0.0006,
      minutes_since_peak: 30,
      top10_pct: 23.4,
      bundle_pct: 15.6,
      dca_flag: 1,
      ath_flag: 0
    },
    {
      id: 'PumpToken111111111',
      symbol: 'PUMP',
      name: 'Pump and Dump',
      price_now: 0.0000567,
      price_change_pct: 567.8,
      mc_now: 567000,
      mc_change_pct: 456.7,
      vol_now: 345000,
      vol_change_pct: 789.2,
      vol_to_mc: 0.6085,
      lp_now: 12000,
      lp_change_pct: 234.5,
      lp_count: 2,
      holders_now: 234,
      holders_change_pct: 123.4,
      holders_per_mc: 0.000413,
      netflow_now: 45000,
      netflow_change_pct: 567.8,
      whale_buy_count: 23,
      kolusd_now: 56000,
      kolusd_change_pct: 890.1,
      kol_velocity: 7.89,
      tx_now: 3456,
      tx_change_pct: 234.5,
      netbuy_usd_now: 67000,
      fee_sol_now: 8.9,
      fee_to_mc_pct: 0.0157,
      minutes_since_peak: 1,
      top10_pct: 67.8,
      bundle_pct: 45.6,
      dca_flag: 0,
      ath_flag: 1
    }
  ]
}
