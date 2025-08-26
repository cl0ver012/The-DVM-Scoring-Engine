import { useState } from 'react'
import axios from 'axios'
import { toast, Toaster } from 'react-hot-toast'
import { motion } from 'framer-motion'
import Link from 'next/link'
import { ArrowLeftIcon } from '@heroicons/react/24/outline'
import PreFilterResults from '../components/PreFilterResults'
import ScoreGauge from '../components/ScoreGauge'
import LoadingAnimation from '../components/LoadingAnimation'
import TrenchReport from '../components/TrenchReport'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

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
      const extractRes = await axios.post(`${API_URL}/extract`, {
        token_address: tokenAddress
      })
      setExtractedData(extractRes.data)
      
      // Check if we have enough data
      if (extractRes.data.coverage.percentage < 10) {
        toast.warning('Limited data available. Running in demo mode with defaults.', { id: 'extract' })
      }
      
      toast.success(`Extracted ${extractRes.data.coverage.percentage}% of data`, { id: 'extract' })

      // Prepare token data for scoring
      const tokenData = {
        token_address: tokenAddress,
        token_symbol: extractRes.data.combined_data.token_symbol || 'UNKNOWN',
        token_name: extractRes.data.combined_data.token_name || 'Unknown Token',
        token_age_minutes: extractRes.data.combined_data.token_age_minutes ?? 30,
        degen_audit: extractRes.data.combined_data.degen_audit || {
          is_honeypot: false,
          has_blacklist: false,
          buy_tax_percent: 0.0,
          sell_tax_percent: 0.0
        },
        liquidity_locked_percent: extractRes.data.combined_data.liquidity_locked_percent || 0.0,
        volume_5m_usd: extractRes.data.combined_data.volume_5m_usd || 0.0,
        holders_count: extractRes.data.combined_data.holders_count || 1000,
        lp_count: extractRes.data.combined_data.lp_count || 1,
        lp_mcap_ratio: extractRes.data.combined_data.lp_mcap_ratio || 0.01,
        top_10_holders_percent: extractRes.data.combined_data.top_10_holders_percent || 50.0,
        bundle_percent: extractRes.data.combined_data.bundle_percent || null
      }

      // Then score the token
      toast.loading('Analyzing token...', { id: 'score' })
      const scoreRes = await axios.post(`${API_URL}/score`, {
        token: tokenData
      })
      setScoreData(scoreRes.data)
      toast.success('Analysis complete!', { id: 'score' })

    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Analysis failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Toaster position="top-right" />
      
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
                <h1 className="text-2xl font-semibold text-gray-900">DVM Token Analyzer</h1>
                <p className="text-sm text-gray-600 mt-1">Professional token analysis and scoring</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/rank">
                <button className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 transition-colors">
                  Rank Multiple Tokens
                </button>
              </Link>
              <button className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 transition-colors">
                API
              </button>
            </div>
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
          {extractedData && (
            <div className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium text-gray-700">Data Coverage</span>
                <span className="text-sm font-semibold text-gray-900">
                  {extractedData.coverage.percentage}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all"
                  style={{ width: `${extractedData.coverage.percentage}%` }}
                />
              </div>
              {extractedData.coverage.percentage < 20 && (
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
