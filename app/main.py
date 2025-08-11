from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterable, List

from app.models import PreFilterResult, TokenData
from app.utils.pre_filter import run_pre_filter


def _load_tokens_from_json(path: Path) -> List[TokenData]:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    if isinstance(payload, list):
        return [TokenData.model_validate(obj) for obj in payload]
    return [TokenData.model_validate(payload)]


def _serialize_results(results: Iterable[PreFilterResult]) -> str:
    return json.dumps([r.model_dump() for r in results], indent=2)


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/mock_data.json")
    if not path.exists():
        print(f"Input not found: {path}")
        return 2
    tokens = _load_tokens_from_json(path)
    results = [run_pre_filter(t) for t in tokens]
    print(_serialize_results(results))
    return 0 if all(r.passed for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())


