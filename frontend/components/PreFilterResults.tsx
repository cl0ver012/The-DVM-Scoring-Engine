import { CheckCircleIcon, XCircleIcon, ExclamationTriangleIcon } from '@heroicons/react/24/solid'

interface PreFilterResultsProps {
  passed: boolean
  failedChecks: string[]
}

export default function PreFilterResults({ passed, failedChecks }: PreFilterResultsProps) {
  const failureReasons = {
    'age_gt_1h': 'Token is younger than 1 hour',
    'degen_audit_pass': 'Failed security audit (honeypot/blacklist/high tax)',
    'liquidity_locked_100': 'Liquidity is not 100% locked',
    'volume_5m_usd_gte_5000': 'Volume (5m) is less than $5,000',
    'holders_gt_100': 'Has 100 or fewer holders',
    'lp_count_gt_1': 'Has only 1 liquidity pool',
    'lp_mcap_ratio_gt_002': 'LP/MCap ratio is less than 2%',
    'top10_pct_lt_30': 'Top 10 holders own 30% or more',
    'bundle_pct_lt_40': 'Bundle percentage is 40% or higher',
  }

  return (
    <div className={`rounded-lg p-6 border ${
      passed 
        ? 'bg-green-50 border-green-200' 
        : 'bg-red-50 border-red-200'
    }`}>
      <div className="flex items-center gap-3 mb-4">
        {passed ? (
          <>
            <CheckCircleIcon className="w-6 h-6 text-green-600" />
            <h2 className="text-lg font-semibold text-green-900">Pre-Filter Passed</h2>
          </>
        ) : (
          <>
            <XCircleIcon className="w-6 h-6 text-red-600" />
            <h2 className="text-lg font-semibold text-red-900">Pre-Filter Failed</h2>
          </>
        )}
      </div>

      {!passed && failedChecks.length > 0 && (
        <div>
          <p className="text-sm text-gray-700 mb-3">This token does not meet the following requirements:</p>
          <p className="text-xs text-gray-600 mb-3">The DVM Scoring Engine requires tokens to be at least 1 hour old for safety</p>
          
          <div className="space-y-2">
            {failedChecks.map((check) => (
              <div key={check} className="flex items-start gap-2">
                <ExclamationTriangleIcon className="w-4 h-4 text-red-600 mt-0.5" />
                <span className="text-sm text-gray-700">
                  {failureReasons[check as keyof typeof failureReasons] || check}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {passed && (
        <p className="text-sm text-green-700">
          This token has passed all pre-filter requirements and is eligible for scoring.
        </p>
      )}
    </div>
  )
}
