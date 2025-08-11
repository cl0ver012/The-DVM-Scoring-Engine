from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel


class PreFilterResult(BaseModel):
    token_address: str
    passed: bool
    failed_checks: List[str]
    details: Dict[str, object]


