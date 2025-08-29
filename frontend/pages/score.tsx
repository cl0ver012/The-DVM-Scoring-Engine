import { useState } from 'react'
import { toast, Toaster } from 'react-hot-toast'
import { motion } from 'framer-motion'
import Link from 'next/link'
import { ArrowLeftIcon } from '@heroicons/react/24/outline'
import PreFilterResults from '../components/PreFilterResults'
import ScoreGauge from '../components/ScoreGauge'
import LoadingAnimation from '../components/LoadingAnimation'
import TrenchReport from '../components/TrenchReport'
import { api } from '../lib/api-client'

export default function ScorePage() {
  const [tokenAddress, setTokenAddress] = useState('')
  const [loading, setLoading] = useState(false)
  const [scoreData, setScoreData] = useState<any>(null)
  const [extractedData, setExtractedData] = useState<any>(null)

  const analyzeToken = async () => {
    if (!tokenAddress.trim()) {
      toast.error('Please enter a token address')
      return
    }

    setLoading(true)
    setScoreData(null)
    setExtractedData(null)

    try {
      // First extract data
      toast.loading('Extracting token data...', { id: 'extract' })
      const extractData = await api.extract(tokenAddress)
      const extractRes = { data: extractData }
      
      // Check if extraction was successful
      if (!extractRes.data.success || !extractRes.data.data) {
        toast.error('Failed to extract token data', { id: 'extract' })
        return
      }
      
      setExtractedData(extractRes.data.data)
      
      // Check if we have enough data
      if (extractRes.data.data.coverage?.percentage < 10) {
        toast.warning('Limited data available. Running in demo mode with defaults.', { id: 'extract' })
      }
      
      toast.success(`Extracted ${extractRes.data.data.coverage?.percentage || 0}% of data`, { id: 'extract' })

      // Prepare token data for scoring
      const combinedData = extractRes.data.data.combined_data || extractRes.data.data.pre_filter_data || {}
      const tokenData = {
        token_address: tokenAddress,
        token_symbol: combinedData.token_symbol || 'UNKNOWN',
        token_name: combinedData.token_name || 'Unknown Token',
        token_age_minutes: combinedData.token_age_minutes,
        degen_audit: combinedData.degen_audit,
        liquidity_locked_percent: combinedData.liquidity_locked_percent,
        volume_5m_usd: combinedData.volume_5m_usd,
        holders_count: combinedData.holders_count,
        lp_count: combinedData.lp_count,
        lp_mcap_ratio: combinedData.lp_mcap_ratio,
        top_10_holders_percent: combinedData.top_10_holders_percent,
        bundle_percent: combinedData.bundle_percent
      }

      // Prepare metrics from extracted data
      const scoringData = extractRes.data.data.scoring_data || {}
      const metrics = {
        vol_over_avg_ratio: scoringData.vol_over_avg_ratio,
        price_change_percent: scoringData.price_change_percent,
        ath_hit: scoringData.ath_hit,
        holders_growth_percent: scoringData.holders_growth_percent,
        whale_buy_usd: scoringData.whale_buy_usd,
        whale_buy_supply_percent: scoringData.whale_buy_supply_percent,
        dca_accumulation_supply_percent: scoringData.dca_accumulation_supply_percent,
        net_inflow_wallets_gt_10k_usd: scoringData.net_inflow_wallets_gt_10k_usd,
        mentions_velocity_ratio: scoringData.mentions_velocity_ratio,
        tier1_kol_buy_supply_percent: scoringData.tier1_kol_buy_supply_percent,
        influencer_reach: scoringData.influencer_reach,
        polarity_positive_percent: scoringData.polarity_positive_percent,
        inflow_over_mcap_percent: scoringData.inflow_over_mcap_percent,
        upgrade_or_staking_live: scoringData.upgrade_or_staking_live
      }

      // Then score the token
      toast.loading('Analyzing token...', { id: 'score' })
      const scoreData = await api.score(tokenData, metrics)
      const scoreRes = { data: scoreData }
      setScoreData(scoreRes.data)
      toast.success('Analysis complete!', { id: 'score' })

    } catch (error: any) {
      console.error('Analysis error:', error)
      toast.dismiss('extract')
      toast.dismiss('score')
      
      if (error.code === 'ERR_NETWORK') {
        toast.error('Cannot connect to backend server. Please ensure the API is running on port 8000.')
      } else if (error.response) {
        toast.error(error.response.data?.detail || error.response.data?.message || 'Analysis failed')
      } else {
        toast.error(error.message || 'Analysis failed')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Toaster position="top-right" />
      
      {/* Header */}
      <div className="bg-white border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 py-6 flex justify-center items-center relative">
          <Link href="/" className="absolute left-6 text-sm text-gray-600 hover:text-gray-700">
            ← Back
          </Link>
          <div className="text-center">
            <h1 className="text-xl font-normal text-gray-900">DVM Token Analyzer</h1>
            <p className="text-sm text-gray-500 mt-1">Professional token analysis and scoring</p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Input Section */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Analyze Token</h2>
          <div className="flex gap-3">
            <input
              type="text"
              placeholder="Enter token address (e.g., EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v)"
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all text-gray-900 placeholder-gray-400"
              value={tokenAddress}
              onChange={(e) => setTokenAddress(e.target.value)}
            />
            <button 
              onClick={analyzeToken}
              disabled={loading}
              className="px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Analyzing...' : 'Analyze Token'}
            </button>
          </div>
          
          {/* Data Coverage Indicator */}
          {extractedData && extractedData.coverage && (
            <div className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-700">Data Coverage</span>
                <span className="text-sm font-semibold text-gray-900">
                  {Math.min(extractedData.coverage?.percentage || 0, 100)}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full transition-all ${
                    (extractedData.coverage?.percentage || 0) >= 80 ? 'bg-green-600' : 
                    (extractedData.coverage?.percentage || 0) >= 60 ? 'bg-blue-600' : 
                    (extractedData.coverage?.percentage || 0) >= 40 ? 'bg-yellow-500' : 'bg-red-500'
                  }`}
                  style={{ width: `${Math.min(extractedData.coverage?.percentage || 0, 100)}%` }}
                />
              </div>
              <div className="text-xs text-gray-600 mt-2">
                {(extractedData.coverage?.percentage || 0) >= 80 ? (
                  <span className="text-green-600">✓ Excellent data coverage</span>
                ) : (extractedData.coverage?.percentage || 0) >= 60 ? (
                  <span className="text-blue-600">✓ Good data coverage</span>
                ) : (extractedData.coverage?.percentage || 0) >= 40 ? (
                  <span className="text-yellow-600">⚠ Limited data coverage</span>
                ) : (
                  <span className="text-red-600">⚠ Low data coverage - results may be less accurate</span>
                )}
              </div>
              {(extractedData.coverage?.percentage || 0) < 20 && (
                <div className="text-xs text-amber-600 mt-2 flex items-center">
                  <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                  Limited data available. Token may be very new or not widely traded.
                </div>
              )}
            </div>
          )}
        </div>

        {/* Loading State */}
        {loading && <LoadingAnimation />}

        {/* Results Section */}
        {scoreData && !loading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            {/* Pre-filter Results */}
            <div className="mb-8">
              <PreFilterResults 
                passed={scoreData.passed_prefilter}
                failedChecks={scoreData.failed_checks}
              />
            </div>

            {/* Score Display */}
            {scoreData.passed_prefilter && (
              <>
                {/* Score Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
                  {/* Total Score */}
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <h3 className="text-sm font-medium text-gray-600 mb-2">Total Score</h3>
                    <div className="text-3xl font-bold text-gray-900">{scoreData.total.toFixed(1)}</div>
                    <div className="text-xs text-gray-500 mt-1">Out of 100</div>
                  </div>

                  {/* Category Scores */}
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <h3 className="text-sm font-medium text-gray-600 mb-2">Momentum</h3>
                    <div className="text-2xl font-semibold text-blue-600">{scoreData.momentum.toFixed(1)}</div>
                  </div>

                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <h3 className="text-sm font-medium text-gray-600 mb-2">Smart Money</h3>
                    <div className="text-2xl font-semibold text-green-600">{scoreData.smart_money.toFixed(1)}</div>
                  </div>

                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <h3 className="text-sm font-medium text-gray-600 mb-2">Sentiment</h3>
                    <div className="text-2xl font-semibold text-purple-600">{scoreData.sentiment.toFixed(1)}</div>
                  </div>

                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                    <h3 className="text-sm font-medium text-gray-600 mb-2">Event</h3>
                    <div className="text-2xl font-semibold text-orange-600">{scoreData.event.toFixed(1)}</div>
                  </div>
                </div>

                {/* Timeframe Scores */}
                {scoreData.new_scores && (
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
                    <h3 className="text-lg font-medium text-gray-900 mb-4">Timeframe Analysis</h3>
                    <div className="grid grid-cols-4 gap-4">
                      {Object.entries(scoreData.new_scores).map(([timeframe, score]) => (
                        <div key={timeframe} className="text-center">
                          <div className="text-sm font-medium text-gray-600 mb-1">{timeframe}</div>
                          <div className="text-xl font-semibold text-gray-900">{(score as number).toFixed(1)}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* AI Report */}
                {scoreData.trench_report_markdown && (
                  <TrenchReport markdown={scoreData.trench_report_markdown} />
                )}
              </>
            )}
          </motion.div>
        )}
      </div>
    </div>
  )
}
