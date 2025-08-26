import { useEffect, useRef } from 'react'
import { motion } from 'framer-motion'

interface ScoreGaugeProps {
  score: number
  label: string
  max?: number
  size?: 'small' | 'large'
  gradient?: string
}

export default function ScoreGauge({ 
  score, 
  label, 
  max = 100, 
  size = 'small',
  gradient = 'from-purple-600 to-pink-600' 
}: ScoreGaugeProps) {
  const percentage = (score / max) * 100
  const radius = size === 'large' ? 80 : 60
  const strokeWidth = size === 'large' ? 12 : 8
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (percentage / 100) * circumference

  return (
    <div className="bg-white/10 backdrop-blur-md rounded-xl p-4 text-center">
      <h3 className="text-lg font-semibold text-white mb-2">{label}</h3>
      
      <div className="relative inline-flex items-center justify-center">
        <svg 
          className="transform -rotate-90"
          width={radius * 2 + 20} 
          height={radius * 2 + 20}
        >
          {/* Background circle */}
          <circle
            cx={radius + 10}
            cy={radius + 10}
            r={radius}
            stroke="rgba(255,255,255,0.2)"
            strokeWidth={strokeWidth}
            fill="none"
          />
          
          {/* Progress circle */}
          <motion.circle
            cx={radius + 10}
            cy={radius + 10}
            r={radius}
            stroke={`url(#gradient-${label})`}
            strokeWidth={strokeWidth}
            fill="none"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 1, ease: "easeOut" }}
            strokeLinecap="round"
          />
          
          {/* Gradient definition */}
          <defs>
            <linearGradient id={`gradient-${label}`} x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor={
                gradient.includes('purple') ? '#8B5CF6' :
                gradient.includes('blue') ? '#3B82F6' :
                gradient.includes('green') ? '#10B981' :
                gradient.includes('yellow') ? '#F59E0B' :
                gradient.includes('red') ? '#EF4444' :
                '#8B5CF6'
              } />
              <stop offset="100%" stopColor={
                gradient.includes('pink') ? '#EC4899' :
                gradient.includes('cyan') ? '#06B6D4' :
                gradient.includes('emerald') ? '#059669' :
                gradient.includes('orange') ? '#F97316' :
                gradient.includes('pink') ? '#EC4899' :
                '#EC4899'
              } />
            </linearGradient>
          </defs>
        </svg>
        
        {/* Score text */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <motion.div
            className={`${size === 'large' ? 'text-4xl' : 'text-2xl'} font-bold text-white`}
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.5 }}
          >
            {score.toFixed(1)}
          </motion.div>
          <div className="text-xs text-gray-300">/ {max}</div>
        </div>
      </div>
      
      {/* Rating */}
      <div className="mt-2">
        <span className={`text-sm font-semibold ${
          percentage >= 80 ? 'text-green-400' :
          percentage >= 60 ? 'text-yellow-400' :
          percentage >= 40 ? 'text-orange-400' :
          'text-red-400'
        }`}>
          {percentage >= 80 ? 'Excellent' :
           percentage >= 60 ? 'Good' :
           percentage >= 40 ? 'Fair' :
           'Poor'}
        </span>
      </div>
    </div>
  )
}
