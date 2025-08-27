/**
 * API Configuration
 * Centralized configuration for all API-related settings
 */

interface ApiConfig {
  baseUrl: string
  timeout: number
  headers: Record<string, string>
}

interface EnvironmentConfig {
  development: ApiConfig
  production: ApiConfig
  test: ApiConfig
}

const environments: EnvironmentConfig = {
  development: {
    baseUrl: process.env.NEXT_PUBLIC_API_URL || 'http://192.168.146.41:8000',
    timeout: 30000, // 30 seconds
    headers: {
      'Content-Type': 'application/json',
    }
  },
  production: {
    baseUrl: process.env.NEXT_PUBLIC_API_URL || 'https://api.dvm-scoring.com',
    timeout: 60000, // 60 seconds
    headers: {
      'Content-Type': 'application/json',
    }
  },
  test: {
    baseUrl: process.env.NEXT_PUBLIC_API_URL || 'http://192.168.146.41:8000',
    timeout: 5000, // 5 seconds
    headers: {
      'Content-Type': 'application/json',
    }
  }
}

// Determine current environment
const currentEnv = (process.env.NEXT_PUBLIC_ENVIRONMENT || 'development') as keyof EnvironmentConfig

// Export the configuration for the current environment
export const apiConfig = environments[currentEnv]

// Helper function to build full API URLs
export const buildApiUrl = (endpoint: string): string => {
  const baseUrl = apiConfig.baseUrl.replace(/\/$/, '') // Remove trailing slash
  const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`
  return `${baseUrl}${cleanEndpoint}`
}

// Export individual config values for convenience
export const API_BASE_URL = apiConfig.baseUrl
export const API_TIMEOUT = apiConfig.timeout
export const API_HEADERS = apiConfig.headers
