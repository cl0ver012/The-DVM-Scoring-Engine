import React, { useState } from 'react';
import Link from 'next/link';
import axios from 'axios';
import TrenchReport from '../components/TrenchReport';

// Example data for scoring demo
const SCORE_EXAMPLES = [
  {
    id: 'high-quality',
    name: 'High Quality Token',
    description: 'Well-distributed, high liquidity token',
    data: {
      token_address: 'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263',
      token_symbol: 'BONK',
      token_name: 'Bonk',
      token_age_minutes: 90, // > 60 minutes to pass pre-filter
      price_now: 0.00002,
      mc_now: 1500000000,
      volume_24h_usd: 50000000,
      liquidity_usd: 5000000,
      holders_count: 500000,
      top_10_holders_percent: 25,
      lp_count: 2, // Must be > 1
      lp_mcap_ratio: 0.05,
      bundle_percent: 15,
      degen_audit: {
        is_honeypot: false,
        has_blacklist: false,
        buy_tax_percent: 0,
        sell_tax_percent: 0
      },
      // Additional required fields
      liquidity_locked_percent: 100,
      volume_5m_usd: 500000, // > $5k requirement
      
      // Scoring metrics
      price_change_percent: 15,
      vol_over_avg_ratio: 2.5,
      whale_buy_usd: 500000,
      whale_buy_supply_percent: 2,
      dca_accumulation_supply_percent: 5,
      net_inflow_wallets_gt_10k_usd: 300000,
      mentions_velocity_ratio: 3,
      tier1_kol_buy_supply_percent: 1,
      influencer_reach: 50000,
      polarity_positive_percent: 75,
      inflow_over_mcap_percent: 0.02,
      upgrade_or_staking_live: false,
      holders_growth_percent: 10,
      ath_hit: false
    }
  },
  {
    id: 'risky-token',
    name: 'Risky Token',
    description: 'New token with concentrated holdings',
    data: {
      token_address: 'RISKYxxx123456789',
      token_symbol: 'RISKY',
      token_name: 'Risky Token',
      token_age_minutes: 120, // > 60 minutes to pass pre-filter
      price_now: 0.0000001,
      mc_now: 100000,
      volume_24h_usd: 50000,
      liquidity_usd: 10000,
      holders_count: 50, // Fail: < 100
      top_10_holders_percent: 85, // Fail: > 30%
      lp_count: 1, // Fail: not > 1
      lp_mcap_ratio: 0.1,
      bundle_percent: 60, // Fail: > 40%
      degen_audit: {
        is_honeypot: false,
        has_blacklist: false,
        buy_tax_percent: 2,
        sell_tax_percent: 2
      },
      // Additional required fields
      liquidity_locked_percent: 0, // Fail: < 100%
      volume_5m_usd: 2000, // Fail: < $5k
      
      // Scoring metrics  
      price_change_percent: -20,
      vol_over_avg_ratio: 0.5,
      whale_buy_usd: 0,
      whale_buy_supply_percent: 0,
      dca_accumulation_supply_percent: 0,
      net_inflow_wallets_gt_10k_usd: -10000,
      mentions_velocity_ratio: 0.5,
      tier1_kol_buy_supply_percent: 0,
      influencer_reach: 100,
      polarity_positive_percent: 30,
      inflow_over_mcap_percent: -0.1,
      upgrade_or_staking_live: false,
      holders_growth_percent: -5,
      ath_hit: false
    }
  }
];

// Example data for ranking demo
const RANK_EXAMPLES = {
  'New': [
    { id: 'NEW1xxx', symbol: 'NEW1', name: 'New Token 1', price_now: 0.0001, mc_now: 500000, vol_now: 100000, mc_change_pct: 50, top10_pct: 0.3, bundle_pct: 0.1, minutes_since_peak: 10 },
    { id: 'NEW2xxx', symbol: 'NEW2', name: 'New Token 2', price_now: 0.00005, mc_now: 300000, vol_now: 80000, mc_change_pct: 30, top10_pct: 0.4, bundle_pct: 0.2, minutes_since_peak: 20 },
    { id: 'NEW3xxx', symbol: 'NEW3', name: 'New Token 3', price_now: 0.00002, mc_now: 200000, vol_now: 50000, mc_change_pct: 20, top10_pct: 0.5, bundle_pct: 0.3, minutes_since_peak: 30 }
  ],
  'Surging': [
    { id: 'SURGE1xxx', symbol: 'SURGE1', name: 'Surging Token 1', price_now: 0.001, mc_now: 5000000, vol_now: 1000000, mc_change_pct: 100, ath_flag: 1, whale_buy_count: 10, kolusd_now: 50000 },
    { id: 'SURGE2xxx', symbol: 'SURGE2', name: 'Surging Token 2', price_now: 0.0005, mc_now: 3000000, vol_now: 800000, mc_change_pct: 80, ath_flag: 0, whale_buy_count: 8, kolusd_now: 30000 },
    { id: 'SURGE3xxx', symbol: 'SURGE3', name: 'Surging Token 3', price_now: 0.0002, mc_now: 2000000, vol_now: 500000, mc_change_pct: 60, ath_flag: 1, whale_buy_count: 5, kolusd_now: 20000 }
  ],
  'All': [
    { id: 'ALL1xxx', symbol: 'ALL1', name: 'All Token 1', price_now: 0.01, mc_now: 10000000, vol_now: 2000000, mc_change_pct: 25, vol_to_mc: 0.2, netflow_now: 500000, kol_velocity: 15 },
    { id: 'ALL2xxx', symbol: 'ALL2', name: 'All Token 2', price_now: 0.005, mc_now: 8000000, vol_now: 1500000, mc_change_pct: 20, vol_to_mc: 0.18, netflow_now: 400000, kol_velocity: 12 },
    { id: 'ALL3xxx', symbol: 'ALL3', name: 'All Token 3', price_now: 0.002, mc_now: 5000000, vol_now: 1000000, mc_change_pct: 15, vol_to_mc: 0.2, netflow_now: 300000, kol_velocity: 10 }
  ]
};

export default function Demo() {
  const [activeDemo, setActiveDemo] = useState<'score' | 'rank'>('score');
  const [selectedExample, setSelectedExample] = useState<string>('');
  const [selectedCategory, setSelectedCategory] = useState<'New' | 'Surging' | 'All'>('New');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>(null);

  const handleScoreDemo = async (example: any) => {
    setLoading(true);
    setSelectedExample(example.id);
    try {
      const response = await axios.post('http://localhost:8000/score', {
        token: example.data,
        metrics: {}
      });
      setResults(response.data);
    } catch (error: any) {
      console.error('Score demo error:', error);
      alert(error.response?.data?.detail || 'Failed to score token');
    } finally {
      setLoading(false);
    }
  };

  const handleRankDemo = async () => {
    setLoading(true);
    try {
      const tokens = RANK_EXAMPLES[selectedCategory];
      const response = await axios.post('http://localhost:8000/rank', {
        tab: selectedCategory,
        rows: tokens.map(t => ({
          ...t,
          price_change_pct: t.mc_change_pct || 0,
          mc_change_pct: t.mc_change_pct || 0,
          vol_change_pct: 0,
          lp_now: 100000,
          lp_change_pct: 0,
          lp_count: 2,
          holders_now: 1000,
          holders_change_pct: 0,
          holders_per_mc: 0.0001,
          netflow_now: t.netflow_now || 100000,
          netflow_change_pct: 0,
          whale_buy_count: t.whale_buy_count || 5,
          kolusd_now: t.kolusd_now || 10000,
          kolusd_change_pct: 0,
          kol_velocity: t.kol_velocity || 5,
          tx_now: 1000,
          tx_change_pct: 0,
          netbuy_usd_now: 50000,
          fee_sol_now: 10,
          fee_to_mc_pct: 0.01,
          minutes_since_peak: t.minutes_since_peak || 30,
          top10_pct: t.top10_pct || 0.3,
          bundle_pct: t.bundle_pct || 0.2,
          dca_flag: 0,
          ath_flag: t.ath_flag || 0,
          vol_to_mc: t.vol_to_mc || (t.vol_now / t.mc_now)
        }))
      });
      setResults(response.data);
    } catch (error: any) {
      console.error('Rank demo error:', error);
      alert(error.response?.data?.detail || 'Failed to rank tokens');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 py-6 flex justify-center items-center relative">
          <Link href="/" className="absolute left-6 text-sm text-gray-600 hover:text-gray-700">
            ← Back
          </Link>
          <div className="text-center">
            <h1 className="text-xl font-normal text-gray-900">Demo</h1>
            <p className="text-sm text-gray-500 mt-1">Pre-configured examples for testing</p>
          </div>
        </div>
      </div>

      {/* Demo Type Selector */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-1 inline-flex">
          <button
            onClick={() => {
              setActiveDemo('score');
              setResults(null);
            }}
            className={`px-6 py-2 rounded-md font-medium transition-colors ${
              activeDemo === 'score'
                ? 'bg-blue-600 text-white'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Scoring Demo
          </button>
          <button
            onClick={() => {
              setActiveDemo('rank');
              setResults(null);
            }}
            className={`px-6 py-2 rounded-md font-medium transition-colors ${
              activeDemo === 'rank'
                ? 'bg-blue-600 text-white'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            Ranking Demo
          </button>
        </div>
      </div>

      {/* Score Demo */}
      {activeDemo === 'score' && (
        <div className="max-w-7xl mx-auto px-6 pb-12">
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Token Scoring Examples</h2>
            <p className="text-gray-600">Select an example to see how different tokens are scored</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            {SCORE_EXAMPLES.map((example) => (
              <div
                key={example.id}
                className={`bg-white rounded-lg shadow-sm border-2 p-6 cursor-pointer transition-all ${
                  selectedExample === example.id
                    ? 'border-blue-500'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
                onClick={() => handleScoreDemo(example)}
              >
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{example.name}</h3>
                <p className="text-gray-600 mb-4">{example.description}</p>
                <div className="space-y-1 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-500">Market Cap:</span>
                    <span className="font-medium">${(example.data.mc_now / 1e6).toFixed(2)}M</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Holders:</span>
                    <span className="font-medium">{example.data.holders_count.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-500">Top 10 Holders:</span>
                    <span className="font-medium">{example.data.top_10_holders_percent}%</span>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Score Results */}
          {results && activeDemo === 'score' && (
            <div className="space-y-6">
              {/* Input Data Section */}
              <details className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <summary className="cursor-pointer font-semibold text-gray-900 hover:text-blue-600">
                  📊 View Input Data
                </summary>
                <div className="mt-4 space-y-4">
                  <div>
                    <h4 className="font-medium text-gray-700 mb-2">Token Data:</h4>
                    <pre className="bg-gray-50 p-4 rounded-lg overflow-x-auto text-sm">
                      {JSON.stringify(selectedExample ? SCORE_EXAMPLES.find(e => e.id === selectedExample)?.data : {}, null, 2)}
                    </pre>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-700 mb-2">Metrics:</h4>
                    <pre className="bg-gray-50 p-4 rounded-lg overflow-x-auto text-sm">
                      {JSON.stringify({}, null, 2)}
                    </pre>
                  </div>
                </div>
              </details>

              {/* Scoring Results */}
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Scoring Results</h3>
                
                <div className="mb-6">
                  <div className="text-center">
                    <div className="text-4xl font-bold text-gray-900 mb-2">
                      {results.total?.toFixed(2) || '0.00'}
                    </div>
                    <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                      results.passed_prefilter 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {results.passed_prefilter ? '✓ Passed Pre-filter' : '✗ Failed Pre-filter'}
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="bg-gray-50 rounded-lg p-4">
                    <div className="text-sm text-gray-600 mb-1">Momentum</div>
                    <div className="text-xl font-semibold text-gray-900">
                      {results.momentum?.toFixed(2) || '0.00'}
                    </div>
                  </div>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <div className="text-sm text-gray-600 mb-1">Smart Money</div>
                    <div className="text-xl font-semibold text-gray-900">
                    {results.smart_money?.toFixed(2) || '0.00'}
                  </div>
                </div>
                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="text-sm text-gray-600 mb-1">Sentiment</div>
                  <div className="text-xl font-semibold text-gray-900">
                    {results.sentiment?.toFixed(2) || '0.00'}
                  </div>
                </div>
                <div className="bg-gray-50 rounded-lg p-4">
                  <div className="text-sm text-gray-600 mb-1">Event</div>
                  <div className="text-xl font-semibold text-gray-900">
                    {results.event?.toFixed(2) || '0.00'}
                  </div>
                </div>
              </div>

              {results.failed_checks && results.failed_checks.length > 0 && (
                <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-4">
                  <h4 className="text-sm font-medium text-red-800 mb-2">Failed Checks:</h4>
                  <ul className="list-disc list-inside text-sm text-red-700 space-y-1">
                    {results.failed_checks.map((check: string, index: number) => (
                      <li key={index}>{check}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* AI Report */}
            {results.trench_report_markdown && (
              <TrenchReport markdown={results.trench_report_markdown} />
            )}
          </div>
          )}
        </div>
      )}

      {/* Rank Demo */}
      {activeDemo === 'rank' && (
        <div className="max-w-7xl mx-auto px-6 pb-12">
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Token Ranking Examples</h2>
            <p className="text-gray-600">See how tokens are ranked in different categories</p>
          </div>

          {/* Category Selector */}
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Select Category</h3>
            <div className="flex gap-4">
              {(['New', 'Surging', 'All'] as const).map((category) => (
                <button
                  key={category}
                  onClick={() => setSelectedCategory(category)}
                  className={`px-6 py-2 rounded-lg font-medium transition-colors ${
                    selectedCategory === category
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {category}
                </button>
              ))}
            </div>
            <button
              onClick={handleRankDemo}
              className="mt-4 w-full bg-blue-600 text-white py-2 rounded-lg font-medium hover:bg-blue-700 transition-colors"
              disabled={loading}
            >
              {loading ? 'Processing...' : 'Run Ranking Demo'}
            </button>
          </div>

          {/* Rank Results */}
          {results && activeDemo === 'rank' && (
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
              <div className="px-6 py-4 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900">
                  {results.tab} Category Rankings
                </h3>
              </div>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Rank
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Token
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Price
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Market Cap
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Score
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {results.rows.map((row: any, index: number) => (
                      <tr key={row.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          #{index + 1}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div>
                            <div className="text-sm font-medium text-gray-900">{row.symbol}</div>
                            <div className="text-sm text-gray-500">{row.name}</div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          ${row.price_now.toFixed(6)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          ${(row.mc_now / 1e6).toFixed(2)}M
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          {row.rank_score?.toFixed(4) || '0.0000'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Loading Overlay */}
      {loading && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 shadow-xl">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-700">Processing...</p>
          </div>
        </div>
      )}
    </div>
  );
}