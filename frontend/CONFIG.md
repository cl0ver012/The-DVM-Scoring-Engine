# Frontend Configuration Guide

## Overview

This frontend uses environment variables and a centralized configuration system for professional deployment across different environments.

## Configuration Files

### 1. Environment Variables (`.env.local`)

Create a `.env.local` file in the frontend directory:

```bash
# Copy from example
cp env.example .env.local

# Edit with your values
# For development:
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENVIRONMENT=development

# For production:
NEXT_PUBLIC_API_URL=https://api.your-domain.com
NEXT_PUBLIC_ENVIRONMENT=production
```

### 2. API Configuration (`config/api.ts`)

Centralized API configuration with environment-specific settings:

- **Development**: Local backend, shorter timeouts
- **Production**: Production API, longer timeouts
- **Test**: Test configuration for CI/CD

### 3. API Client (`lib/api-client.ts`)

Professional HTTP client with:
- Axios instance with interceptors
- Centralized error handling
- Request/response logging
- Rate limit handling
- Network error recovery

## Environment Setup

### Development

```bash
# Default configuration works out of the box
npm run dev
```

### Production

```bash
# Set production environment
NEXT_PUBLIC_API_URL=https://api.your-domain.com
NEXT_PUBLIC_ENVIRONMENT=production
npm run build
npm start
```

### Docker

```dockerfile
# In your Dockerfile
ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_ENVIRONMENT

ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_ENVIRONMENT=$NEXT_PUBLIC_ENVIRONMENT
```

## API Endpoints

All API calls go through the centralized client:

```typescript
import { api } from '../lib/api-client'

// Extract token data
const data = await api.extract(tokenAddress)

// Score token
const score = await api.score(tokenData, metrics)

// Rank tokens
const ranking = await api.rank(tokens, category)
```

## Error Handling

The API client handles errors professionally:

- Network errors
- Rate limiting (429)
- Server errors (5xx)
- Authentication errors (401)
- Validation errors (422)

## Security

- API keys should never be exposed in frontend code
- Use environment variables for sensitive configuration
- CORS should be properly configured on the backend
- Consider implementing request signing for production

## Deployment Checklist

- [ ] Set `NEXT_PUBLIC_API_URL` to production backend
- [ ] Set `NEXT_PUBLIC_ENVIRONMENT` to `production`
- [ ] Ensure CORS is configured on backend
- [ ] Test API connectivity before deployment
- [ ] Monitor API errors in production
