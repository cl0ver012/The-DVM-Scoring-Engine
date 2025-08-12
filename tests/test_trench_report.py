from app.ai.client import MockChatClient
from app.ai.trench_report import TrenchInput, generate_trench_report


def test_trench_report_builds_and_calls_client():
    mock = MockChatClient(response="# Report\nOK\n```json\n{}\n```\n")
    data = TrenchInput(
        token={"symbol": "DVM", "name": "Deep Value Memetics", "address": "So111..."},
        prefilter={"passed": True, "failed_checks": []},
        scores={"momentum": 30.0, "smart_money": 35.0, "sentiment": 8.0, "event": 10.0, "total": 83.0},
        signals=["5m: vol/avg 2.1x", "5m: price +9.2%"],
        metrics={"holders": 1200, "top10_pct": 22.0, "lp_usd": 50000, "mcap_usd": 275000},
        timeframe="5m",
        as_of_utc="2025-08-08T12:34:56Z",
    )
    out = generate_trench_report(mock, data)
    assert out.startswith("# Report")


