import { useState } from 'react'
import axios from 'axios'
import { toast, Toaster } from 'react-hot-toast'
import { motion } from 'framer-motion'
import Link from 'next/link'
import { ArrowLeftIcon, PlusIcon, XMarkIcon } from '@heroicons/react/24/outline'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function RankPage() {
  const [tokens, setTokens] = useState<string[]>([''])
  const [category, setCategory] = useState('New')
  const [timeframe, setTimeframe] = useState('1h')
  const [loading, setLoading] = useState(false)
  const [rankingData, setRankingData] = useState<any>(null)

  const addToken = () => {
    setTokens([...tokens, ''])
  }

  const removeToken = (index: number) => {
    setTokens(tokens.filter((_, i) => i !== index))
  }

  const updateToken = (index: number, value: string) => {
    const newTokens = [...tokens]
    newTokens[index] = value
    setTokens(newTokens)
  }

  const rankTokens = async () => {
    const validTokens = tokens.filter(t => t.trim())
    if (validTokens.length === 0) {
      toast.error('Please enter at least one token address')
      return
    }

    setLoading(true)
    setRankingData(null)

    try {
      toast.loading('Ranking tokens...', { id: 'rank' })
      
      // Prepare rows for ranking with all required fields
      const rows = validTokens.map((token, index) => ({
        id: token,
        symbol: `TOKEN${index + 1}`,
        name: `Token ${index + 1}`,
        price_now: 1.0,
        price_change_pct: 0.0,
        mc_now: 1000000,
        mc_change_pct: 0.0,
        vol_now: 100000,
        vol_change_pct: 0.0,
        vol_to_mc: 0.1,
        lp_now: 50000,
        lp_change_pct: 0.0,
        lp_count: 1,
        holders_now: 1000,
        holders_change_pct: 0.0,
        holders_per_mc: 0.001,
        netflow_now: 0.0,
        netflow_change_pct: 0.0,
        whale_buy_count: 0,
        kolusd_now: 0.0,
        kolusd_change_pct: 0.0,
        kol_velocity: 0.0,
        tx_now: 100,
        tx_change_pct: 0.0,
        netbuy_usd_now: 0.0,
        fee_sol_now: 0.0,
        fee_to_mc_pct: 0.0,
        minutes_since_peak: 0.0,
        top10_pct: 0.0,
        bundle_pct: 0.0,
        dca_flag: 0,
        ath_flag: 0,
      }))

      const res = await axios.post(`${API_URL}/rank`, {
        tab: category,
        rows
      })
      
      setRankingData(res.data)
      toast.success('Ranking complete!', { id: 'rank' })
    } catch (error: any) {
      const errorMessage = typeof error.response?.data?.detail === 'string' 
        ? error.response.data.detail 
        : error.response?.data?.detail?.[0]?.msg || 'Ranking failed'
      toast.error(errorMessage, { id: 'rank' })
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
                <h1 className="text-2xl font-semibold text-gray-900">Token Ranking</h1>
                <p className="text-sm text-gray-600 mt-1">Compare and rank multiple tokens</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/score">
                <button className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 transition-colors">
                  Single Token Analysis
                </button>
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Input Section */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <h2 className="text-lg font-medium text-gray-900 mb-4">Rank Tokens</h2>
          
          {/* Category and Timeframe Selection */}
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Category</label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="New">New Launches</option>
                <option value="Surging">Surging Tokens</option>
                <option value="All">All Tokens</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Timeframe</label>
              <select
                value={timeframe}
                onChange={(e) => setTimeframe(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="5m">5 minutes</option>
                <option value="15m">15 minutes</option>
                <option value="30m">30 minutes</option>
                <option value="1h">1 hour</option>
              </select>
            </div>
          </div>

          {/* Token Inputs */}
          <div className="space-y-3 mb-4">
            {tokens.map((token, index) => (
              <div key={index} className="flex gap-2">
                <input
                  type="text"
                  placeholder="Enter token address"
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  value={token}
                  onChange={(e) => updateToken(index, e.target.value)}
                />
                {tokens.length > 1 && (
                  <button
                    onClick={() => removeToken(index)}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                  >
                    <XMarkIcon className="w-5 h-5" />
                  </button>
                )}
              </div>
            ))}
          </div>

          {/* Add Token Button */}
          <button
            onClick={addToken}
            className="flex items-center space-x-2 text-blue-600 hover:text-blue-700 transition-colors mb-6"
          >
            <PlusIcon className="w-5 h-5" />
            <span>Add Another Token</span>
          </button>

          {/* Rank Button */}
          <button
            onClick={rankTokens}
            disabled={loading}
            className="w-full px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Ranking...' : 'Rank Tokens'}
          </button>
        </div>

        {/* Results Section */}
        {rankingData && !loading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
          >
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Ranking Results - {rankingData.tab} Category
            </h3>

            {/* Ranking Table */}
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead>
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Rank
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Token
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Total Score
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Momentum
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Smart Money
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Sentiment
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Event
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {rankingData.rows.map((row: any, index: number) => (
                    <tr key={row.id} className={index === 0 ? 'bg-blue-50' : ''}>
                      <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                        #{index + 1}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap">
                        <div>
                          <div className="text-sm font-medium text-gray-900">{row.symbol}</div>
                          <div className="text-xs text-gray-500">{row.id.slice(0, 8)}...</div>
                        </div>
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm font-semibold text-gray-900">
                        {row.score?.toFixed(1) || '0.0'}
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm text-blue-600">
                        -
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm text-green-600">
                        -
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm text-purple-600">
                        -
                      </td>
                      <td className="px-4 py-3 whitespace-nowrap text-sm text-orange-600">
                        -
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Summary Stats */}
            <div className="mt-6 grid grid-cols-3 gap-4 pt-6 border-t border-gray-200">
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900">
                  {rankingData.rows.length}
                </div>
                <div className="text-sm text-gray-600">Tokens Ranked</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900">
                  {(rankingData.rows.reduce((sum: number, row: any) => sum + (row.score || 0), 0) / rankingData.rows.length).toFixed(1)}
                </div>
                <div className="text-sm text-gray-600">Average Score</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-gray-900">
                  {Math.max(...rankingData.rows.map((row: any) => row.score || 0)).toFixed(1)}
                </div>
                <div className="text-sm text-gray-600">Highest Score</div>
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  )
}
