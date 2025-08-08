The DVM Scoring Engine
======================

Day 1 deliverable: project scaffold, Dockerfile, mock data, and the On-Chain Risk Pre-Filter with client-updated rule for Fees Paid (SOL).

Project structure
-----------------

```
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
- Fees paid (SOL): if present, enforce threshold
  - Default: `fees_paid_sol ≥ 20`
  - If `is_migrated_token` is true: `fees_paid_sol ≥ 5` (client suggestion 5–10)
  - Data sources: `gmgn`, `Axiom`, `Padre` (normalized to `fees_paid_sol`)

CLI
---

```
python -m dvm_scoring.main data/mock_data.json
```

Exit code is 0 when all tokens pass, 1 otherwise. Output is JSON.

Run tests
---------

```
pytest -q
```

Next steps
----------
- Implement Momentum and Smart Money scoring (Week 1 Day 2)
- Add Sentiment and Event/Narrative plus penalties (Day 3)
- Integrate into `ScoringEngine` with tests (Day 4–5)


