The DVM Scoring Engine
======================

Day 1 deliverable: project scaffold, Dockerfile, mock data, and the On-Chain Risk Pre-Filter that enforces the minimum eligibility rules exactly as specified. Includes client-requested global fees paid > 20 SOL.

Project structure
-----------------

```text
.
├─ dvm_scoring/
│  ├─ __init__.py
│  ├─ models.py
│  └─ prefilter.py
├─ data/
│  └─ mock_data.json
├─ tests/
│  └─ test_prefilter.py
├─ Dockerfile
├─ requirements.txt
└─ README.md
```

Pre-Filter logic (minimum eligibility)
--------------------------------------
- New tokens only: `token_age_minutes < 60`
- Degen audit must pass: no honeypot, no blacklist, buy/sell tax < 3%
- Liquidity locked: 100%
- Volume (5m): ≥ $5,000
- Holders: > 100
- LP pools: > 1
- LP/MCap ratio: > 0.02
- Top 10 holders: < 30%
- Bundle buys: < 40%
- Global fees paid: > 20 SOL (client priority requirement)
  - Overrides per client update:
    - New pairs: minimum fees ≥ 5 SOL (configurable)
    - Migrated tokens: minimum fees ≥ 5–10 SOL (default 5; configurable)
    - Old/legacy tokens with missing historical compute: by default we do not hard-fail this check (can be enforced via `APPLY_FEES_TO_OLD=true`)

Quickstart (Windows)
--------------------

1) Create a virtual environment and install deps:

```bat
cd C:\Users\user\Desktop\DVM\Project\The-DVM-Scoring-Engine
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

2) Run the pre-filter against the mock data:

```bat
python -m dvm_scoring.main data\mock_data.json
```

Exit code is 0 when all tokens pass, 1 otherwise. Output is JSON.

Run tests
---------

```bat
python -m pytest -q
```

Docker
------

```bat
docker build -t dvm-scoring-engine:day1 .
docker run --rm dvm-scoring-engine:day1
```

Next steps
----------
- Implement Momentum and Smart Money scoring (Week 1 Day 2-3)
- Add optional inputs: quality_of_holders, fresh_wallets_percent, wallets_with_bad_reputation_percent, sniper_activity_score
- Integrate into `ScoringEngine` with tests, then API + AI summary in Week 2

Config
------
Environment variables to tune fees logic:

```text
FEES_MIN_SOL_NEW=5          # threshold for new tokens
FEES_MIN_SOL_MIGRATED=5     # threshold for migrated tokens
APPLY_FEES_TO_OLD=false     # if true, enforce fees on old tokens too
```
