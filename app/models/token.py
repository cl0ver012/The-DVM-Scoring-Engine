from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class DegenAudit(BaseModel):
    is_honeypot: bool
    has_blacklist: bool
    buy_tax_percent: float = Field(ge=0)
    sell_tax_percent: float = Field(ge=0)


class TokenData(BaseModel):
    token_address: str
    token_symbol: str
    token_name: str

    token_age_minutes: int = Field(ge=0, description="Age since launch in minutes")

    # 1. Token Age (<1h is required by pre-filter to focus on new launches)
    # Covered by token_age_minutes

    # 2. Basic Security Audit (gmgn.ai)
    degen_audit: DegenAudit

    # 3. Liquidity Lock (DexScreener)
    liquidity_locked_percent: float = Field(ge=0)

    # 4. Initial Volume (gmgn.ai)
    volume_5m_usd: float = Field(ge=0)

    # 5. Initial Holders (gmgn.ai)
    holders_count: int = Field(ge=0)

    # 6. Holder Distribution (gmgn.ai)
    top_10_holders_percent: float = Field(ge=0, le=100)

    # 7. Creator Fees Paid (Axiom/Padre/GMGN)
    fees_paid_sol: float = Field(ge=0)
    token_age_days: Optional[float] = Field(
        default=None, description="Age in days (optional; if None, derived from minutes)"
    )


