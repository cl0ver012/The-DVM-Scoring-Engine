import { useState } from 'react'
import Link from 'next/link'
import { ArrowLeftIcon, PlayIcon } from '@heroicons/react/24/outline'
import { motion } from 'framer-motion'
import axios from 'axios'
import { DEMO_METRICS, RANKING_DEMO_DATA } from '../utils/demoData'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Demo scenarios
const DEMO_SCENARIOS = {
  scoring: [
    {
      id: 'high-quality',
      name: 'High Quality Token',
      description: 'A new token with excellent metrics across all categories',
      token: {
        token_address: 'HighQualityToken123',
        token_symbol: 'QUALITY',
        token_name: 'Quality Token',
        token_age_minutes: 30,
        degen_audit: {
          is_honeypot: false,
          has_blacklist: false,
          buy_tax_percent: 0.0,
          sell_tax_percent: 0.0
        },
        liquidity_locked_percent: 100.0,
        volume_5m_usd: 15000.0,
        holders_count: 500,
        lp_count: 5,
        lp_mcap_ratio: 0.08,
        top_10_holders_percent: 20.0,
        bundle_percent: 5.0
      }
    },
    {
      id: 'average-token',
      name: 'Average Token',
      description: 'A typical new launch with moderate metrics',
      token: {
        token_address: 'AverageToken456',
        token_symbol: 'AVG',
        token_name: 'Average Token',
        token_age_minutes: 45,
        degen_audit: {
          is_honeypot: false,
          has_blacklist: false,
          buy_tax_percent: 2.0,
          sell_tax_percent: 2.0
        },
        liquidity_locked_percent: 100.0,
        volume_5m_usd: 6000.0,
        holders_count: 150,
        lp_count: 2,
        lp_mcap_ratio: 0.03,
        top_10_holders_percent: 28.0,
        bundle_percent: 20.0
      }
    },
    {
      id: 'failed-prefilter',
      name: 'Failed Pre-filter Token',
      description: 'An older token that fails pre-filter checks',
      token: {
        token_address: 'OldToken789',
        token_symbol: 'OLD',
        token_name: 'Old Token',
        token_age_minutes: 120, // Too old
        degen_audit: {
          is_honeypot: false,
          has_blacklist: false,
          buy_tax_percent: 0.0,
          sell_tax_percent: 0.0
        },
        liquidity_locked_percent: 50.0, // Not fully locked
        volume_5m_usd: 3000.0, // Too low
        holders_count: 80, // Too few
        lp_count: 1, // Only one LP
        lp_mcap_ratio: 0.01, // Too low
        top_10_holders_percent: 45.0, // Too concentrated
        bundle_percent: 50.0 // Too high
      }
    }
  ],
  ranking: [
    {
      id: 'top-performers',
      name: 'Top Performing Tokens',
      description: 'Rank the best new launches',
      tokens: [
        'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
        'So11111111111111111111111111111111111111112',
        'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB'
      ]
    },
    {
      id: 'mixed-quality',
      name: 'Mixed Quality Tokens',
      description: 'Compare tokens with varying quality',
      tokens: [
        'TokenA123456789',
        'TokenB987654321',
        'TokenC555555555',
        'TokenD111111111'
      ]
    }
  ]
}

export default function DemoPage() {
  const [activeTab, setActiveTab] = useState<'scoring' | 'ranking'>('scoring')
  const [selectedScenario, setSelectedScenario] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  const runScoringDemo = async (scenario: any) => {
    setLoading(true)
    setResult(null)
    try {
      // Use comprehensive realistic metrics from demoData
      const metrics = DEMO_METRICS[scenario.id as keyof typeof DEMO_METRICS]

      const response = await axios.post(`${API_URL}/score`, {
        token: scenario.token,
        metrics: metrics
      })
      setResult({ type: 'scoring', data: response.data })
    } catch (error) {
      console.error('Demo failed:', error)
    } finally {
      setLoading(false)
    }
  }

  const runRankingDemo = async (scenario: any) => {
    setLoading(true)
    setResult(null)
    try {
      // Use realistic ranking data
      const rows = RANKING_DEMO_DATA[scenario.id as keyof typeof RANKING_DEMO_DATA]

      const response = await axios.post(`${API_URL}/rank`, {
        tab: 'New',
        rows
      })
      setResult({ type: 'ranking', data: response.data })
    } catch (error) {
      console.error('Demo failed:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link href="/">
                <button className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors">
                  <ArrowLeftIcon className="w-5 h-5" />
                  <span>Back</span>
                </button>
              </Link>
              <div className="border-l border-gray-300 h-6 mx-2"></div>
              <div>
                <h1 className="text-2xl font-semibold text-gray-900">Demo Mode</h1>
                <p className="text-sm text-gray-600 mt-1">Try pre-configured examples</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Tab Selection */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-1 mb-8">
          <div className="flex">
            <button
              onClick={() => {
                setActiveTab('scoring')
                setSelectedScenario(null)
                setResult(null)
              }}
              className={`flex-1 px-4 py-2 rounded-md font-medium transition-colors ${
                activeTab === 'scoring' 
                  ? 'bg-blue-600 text-white' 
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Token Scoring Demos
            </button>
            <button
              onClick={() => {
                setActiveTab('ranking')
                setSelectedScenario(null)
                setResult(null)
              }}
              className={`flex-1 px-4 py-2 rounded-md font-medium transition-colors ${
                activeTab === 'ranking' 
                  ? 'bg-blue-600 text-white' 
                  : 'text-gray-600 hover:text-gray-900'
              }`}
            >
              Token Ranking Demos
            </button>
          </div>
        </div>

        {/* Instructions */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <p className="text-sm text-blue-800">
            Click any "Run Demo" button below to see the scoring engine in action. No setup required!
          </p>
        </div>

        {/* Scenario Selection */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {DEMO_SCENARIOS[activeTab].map((scenario) => (
            <div
              key={scenario.id}
              className={`bg-white rounded-lg shadow-sm border-2 p-6 cursor-pointer transition-all ${
                selectedScenario === scenario.id
                  ? 'border-blue-500 shadow-lg'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
              onClick={() => setSelectedScenario(scenario.id)}
            >
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {scenario.name}
              </h3>
              <p className="text-sm text-gray-600 mb-4">
                {scenario.description}
              </p>
              
              {activeTab === 'scoring' && selectedScenario === scenario.id && (
                <div className="text-xs text-gray-500 space-y-1 mb-4">
                  <div>Age: {(scenario as any).token.token_age_minutes} min</div>
                  <div>Volume: ${(scenario as any).token.volume_5m_usd.toLocaleString()}</div>
                  <div>Holders: {(scenario as any).token.holders_count}</div>
                </div>
              )}
              
              {activeTab === 'ranking' && selectedScenario === scenario.id && (
                <div className="text-xs text-gray-500 mb-4">
                  {(scenario as any).tokens.length} tokens to rank
                </div>
              )}
              
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  setSelectedScenario(scenario.id)
                  if (activeTab === 'scoring') {
                    runScoringDemo(scenario)
                  } else {
                    runRankingDemo(scenario)
                  }
                }}
                disabled={loading}
                className="w-full flex items-center justify-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <PlayIcon className="w-4 h-4" />
                <span>{loading && selectedScenario === scenario.id ? 'Running...' : 'Run Demo'}</span>
              </button>
            </div>
          ))}
        </div>

        {/* Results Display */}
        {result && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
          >
            {result.type === 'scoring' ? (
              <>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Scoring Results</h3>
                
                {/* Pre-filter Status */}
                <div className={`mb-6 p-4 rounded-lg ${
                  result.data.passed_prefilter 
                    ? 'bg-green-50 border border-green-200' 
                    : 'bg-red-50 border border-red-200'
                }`}>
                  <div className="flex items-center">
                    <span className={`text-lg font-semibold ${
                      result.data.passed_prefilter ? 'text-green-800' : 'text-red-800'
                    }`}>
                      Pre-filter: {result.data.passed_prefilter ? '✅ PASSED' : '❌ FAILED'}
                    </span>
                  </div>
                  {!result.data.passed_prefilter && (
                    <div className="mt-2 text-sm text-red-700">
                      Failed checks: {result.data.failed_checks.join(', ')}
                    </div>
                  )}
                </div>

                {result.data.passed_prefilter && (
                  <>
                    {/* Total Score */}
                    <div className="text-center mb-6">
                      <div className="text-4xl font-bold text-gray-900">
                        {result.data.total.toFixed(1)}
                      </div>
                      <div className="text-sm text-gray-600">Total Score (out of 100)</div>
                    </div>

                    {/* Category Scores */}
                    <div className="grid grid-cols-4 gap-4 mb-6">
                      <div className="text-center">
                        <div className="text-2xl font-semibold text-blue-600">
                          {result.data.momentum.toFixed(1)}
                        </div>
                        <div className="text-sm text-gray-600">Momentum</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-semibold text-green-600">
                          {result.data.smart_money.toFixed(1)}
                        </div>
                        <div className="text-sm text-gray-600">Smart Money</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-semibold text-purple-600">
                          {result.data.sentiment.toFixed(1)}
                        </div>
                        <div className="text-sm text-gray-600">Sentiment</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-semibold text-orange-600">
                          {result.data.event.toFixed(1)}
                        </div>
                        <div className="text-sm text-gray-600">Event</div>
                      </div>
                    </div>

                    {/* Timeframe Analysis */}
                    {result.data.new_scores && (
                      <div className="border-t border-gray-200 pt-4">
                        <h4 className="text-sm font-medium text-gray-700 mb-3">Timeframe Analysis</h4>
                        <div className="grid grid-cols-4 gap-4">
                          {Object.entries(result.data.new_scores).map(([tf, score]) => (
                            <div key={tf} className="text-center">
                              <div className="text-lg font-semibold text-gray-900">
                                {(score as number).toFixed(1)}
                              </div>
                              <div className="text-xs text-gray-600">{tf}</div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* AI Report */}
                    {result.data.trench_report_markdown && (
                      <div className="border-t border-gray-200 pt-6 mt-6">
                        <h4 className="text-lg font-semibold text-gray-900 mb-4">AI Analysis Report</h4>
                        <div className="bg-gray-50 rounded-lg p-6 prose prose-sm max-w-none">
                          <div className="text-gray-700 whitespace-pre-wrap">
                            {result.data.trench_report_markdown}
                          </div>
                        </div>
                      </div>
                    )}
                  </>
                )}
              </>
            ) : (
              <>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Ranking Results - {result.data.tab} Category
                </h3>
                
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead>
                      <tr>
                        <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase">Rank</th>
                        <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase">Token</th>
                        <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase">Score</th>
                        <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase">Price</th>
                        <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase">24h %</th>
                        <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase">Market Cap</th>
                        <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase">Volume</th>
                        <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase">Holders</th>
                        <th className="px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase">Whales</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      {result.data.rows.map((row: any, index: number) => (
                        <tr key={row.id} className={index === 0 ? 'bg-blue-50' : ''}>
                          <td className="px-3 py-3 text-sm font-medium text-gray-900">#{index + 1}</td>
                          <td className="px-3 py-3">
                            <div>
                              <div className="text-sm font-medium text-gray-900">{row.symbol}</div>
                              <div className="text-xs text-gray-500">{row.name}</div>
                            </div>
                          </td>
                          <td className="px-3 py-3">
                            <div className="text-sm font-bold text-gray-900">{row.score?.toFixed(1) || '0.0'}</div>
                            <div className="text-xs text-gray-500">
                              {row.ath_flag ? '🔥 ATH' : ''} {row.dca_flag ? '💎 DCA' : ''}
                            </div>
                          </td>
                          <td className="px-3 py-3 text-sm text-gray-900">
                            ${row.price_now < 0.01 ? row.price_now.toExponential(2) : row.price_now.toFixed(4)}
                          </td>
                          <td className={`px-3 py-3 text-sm font-medium ${row.price_change_pct > 0 ? 'text-green-600' : 'text-red-600'}`}>
                            {row.price_change_pct > 0 ? '+' : ''}{(row.price_change_pct * 100).toFixed(2)}%
                          </td>
                          <td className="px-3 py-3 text-sm text-gray-600">
                            ${row.mc_now > 1000000 ? `${(row.mc_now / 1000000).toFixed(1)}M` : `${(row.mc_now / 1000).toFixed(1)}K`}
                          </td>
                          <td className="px-3 py-3 text-sm text-gray-600">
                            ${row.vol_now > 1000000 ? `${(row.vol_now / 1000000).toFixed(1)}M` : `${(row.vol_now / 1000).toFixed(1)}K`}
                          </td>
                          <td className="px-3 py-3 text-sm text-gray-600">
                            {row.holders_now > 1000 ? `${(row.holders_now / 1000).toFixed(1)}K` : row.holders_now}
                          </td>
                          <td className="px-3 py-3 text-sm text-gray-600">
                            {row.whale_buy_count} buys
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </>
            )}
          </motion.div>
        )}
      </div>
    </div>
  )
}