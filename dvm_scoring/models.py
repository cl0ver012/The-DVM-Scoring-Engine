from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class DegenAudit(BaseModel):
    """Represents results from a degen audit provider (e.g., gmgn.ai)."""

    is_honeypot: bool = Field(description="True if token exhibits honeypot behavior")
    has_blacklist: bool = Field(description="True if contract has blacklist mechanisms")
    buy_tax_percent: float = Field(ge=0, description="Buy tax percentage (0-100)")
    sell_tax_percent: float = Field(ge=0, description="Sell tax percentage (0-100)")


class TokenData(BaseModel):
    """Input data model for a token used by the pre-filter.

    Note: This mirrors the fields required by the requirements document.
    """

    token_address: str
    token_symbol: str
    token_name: str
    token_age_minutes: int = Field(ge=0)

    # On-chain risk inputs
    degen_audit: DegenAudit
    liquidity_locked_percent: float = Field(
        ge=0, description="Percentage of liquidity locked (0-100+)"
    )
    volume_5m_usd: float = Field(ge=0)
    holders_count: int = Field(ge=0)
    lp_pool_count: int = Field(ge=0)
    liquidity_usd: float = Field(ge=0, description="Total liquidity in USD")
    market_cap_usd: float = Field(ge=0, description="Market capitalization in USD")
    top_10_holders_percent: float = Field(
        ge=0, le=100, description="Percentage of supply held by top 10 holders"
    )
    bundle_buys_percent: float = Field(
        ge=0, le=100, description="Percentage of bundle buys in last window"
    )

    # Optional metadata
    last_updated_iso: Optional[str] = None


class PreFilterResult(BaseModel):
    """Result of running the pre-filter checks."""

    token_address: str
    passed: bool
    failed_checks: List[str] = Field(default_factory=list)
    details: Dict[str, object] = Field(default_factory=dict)

