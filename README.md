# DVM Scoring Engine

A sophisticated token analysis system that extracts data from multiple sources, scores tokens based on momentum, smart money flow, sentiment, and events, and provides AI-powered investment insights.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 16+

### API Keys Required
1. **Copy the environment file**:
   ```bash
   cp ENV.sample .env
   ```

2. **Configure your API keys in `.env`**:
   - **OPENAI_API_KEY**: Required for AI analysis reports (get from https://platform.openai.com/api-keys)
   - **BIRDEYE_API_KEY**: Already provided in ENV.sample
   - **HELIUS_API_KEY**: Already provided in ENV.sample

   Without the OpenAI API key, the system uses dynamic reports based on actual token data.
- Chrome browser (for GMGN scraping)

### Backend Setup
```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API keys
# Copy ENV.sample to .env and add your keys:
# - BIRDEYE_API_KEY (required for price data)
# - HELIUS_API_KEY (required for transaction analysis)
# - OPENAI_API_KEY (optional for AI reports)

# Run the API server
python -m uvicorn app.api.server:app --reload --port 8000
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Configure environment (for production deployments)
cp env.example .env.local
# Edit .env.local with your API URL

# Run development server
npm run dev

# For production build
npm run build
npm start
```

Access the application at http://localhost:3000

**Note**: The frontend uses environment-based configuration. See `frontend/CONFIG.md` for detailed setup instructions.

## 📊 Data Sources

### 1. **DexScreener** (No API key required)
- Token info (name, symbol, address)
- Current price and market cap
- Trading volume (5m, 24h)
- Liquidity data
- LP count
- Transaction counts

### 2. **Birdeye** (API key required)
- Price changes (5m, 15m, 30m, 1h, 24h)
- Most accurate for short-term price movements

### 3. **Helius** (API key required)
- Transaction pattern analysis
- DCA wallet detection
- Used for whale activity estimation

### 4. **GMGN.ai** (Web scraping)
- Most accurate holder count (543K vs 48 from Helius)
- Top 10 holders percentage (24.3% vs 99.8% from Helius)

## 🎯 Features

### 1. **Token Extraction** (`/extract`)
- Fetches data from all sources
- Combines and prioritizes most accurate data
- 100% coverage through intelligent defaults

### 2. **Token Scoring** (`/score`)
- Pre-filter checks (security, liquidity, age)
- Multi-category scoring:
  - **Momentum** (37.5%): Volume, price changes, ATH, holder growth
  - **Smart Money** (37.5%): Whale activity, DCA accumulation, net inflows
  - **Sentiment** (12.5%): Social metrics, KOL activity, polarity
  - **Event** (12.5%): Inflow/mcap ratio, upgrades/staking

### 3. **Token Ranking** (`/rank`)
- Categories: New, Surging, All
- Time-based weighting for "New" tokens
- Custom formulas from client specifications

### 4. **AI Reports** (`/report`)
- Natural language investment analysis
- Two modes:
  - Dynamic reports based on token scores (no API key needed)
  - GPT-4 powered analysis (requires OpenAI API key)
- Comprehensive token evaluation with risk assessment

## 🏗️ Architecture

```
The-DVM-Scoring-Engine/
├── app/                    # Backend application
│   ├── api/               # FastAPI server and schemas
│   ├── engine/            # Scoring logic
│   ├── models/            # Data models
│   ├── ranker/            # Ranking formulas
│   ├── utils/             # Pre-filter and utilities
│   └── ai/                # AI report generation
├── extractors/            # Data extraction modules
│   ├── perfect_extractor.py    # Main extractor combining all sources
│   ├── gmgn_selenium_scraper.py # GMGN web scraper
│   └── unified_extractor.py    # Wrapper for extraction
├── frontend/              # Next.js frontend
│   ├── pages/            # Application pages
│   ├── components/       # React components
│   └── styles/           # Tailwind CSS styles
└── tests/                # Test files
```

## 🔑 API Endpoints

- `GET /` - API documentation
- `POST /extract` - Extract token data
- `POST /score` - Score a single token
- `POST /rank` - Rank multiple tokens
- `POST /report` - Generate AI report
- `GET /health` - Health check

## 📈 Scoring Variables

### Pre-filter Requirements
- Token age > 1 hour
- No honeypot/blacklist
- Buy/sell tax < 3%
- Liquidity locked (if > $1000)
- Volume > $5k in 5 minutes
- Holders > 100
- LP count > 1
- LP/MCap ratio > 0.02
- Top 10 holders < 30%
- Bundle rate < 40%

### Scoring Metrics
See `EXTRACTION_SOURCES_ANALYSIS.md` for complete variable list and sources.

## 🛠️ Development

### Running Tests
```bash
pytest tests/
```

### Code Structure
- **Extractors**: Modular data extraction from each source
- **Engine**: Scoring logic implementation
- **Models**: Pydantic models for data validation
- **API**: FastAPI server with CORS support
- **Frontend**: Next.js with TypeScript and Tailwind CSS

## 📝 License

Proprietary - All rights reserved