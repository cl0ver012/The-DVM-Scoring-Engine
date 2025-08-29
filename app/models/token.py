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

    # Pre-filter variables per document requirements
    token_age_minutes: int = Field(ge=0, description="Age since launch in minutes")

    # 1. Token Age (>1h is required by pre-filter for safety)
    # Covered by token_age_minutes

    # 2. Basic Security Audit (GoPlus API)
    degen_audit: DegenAudit

    # 3. Liquidity Lock (DexScreener)
    liquidity_locked_percent: float = Field(ge=0)

    # 4. Initial Volume (DexScreener)
    volume_5m_usd: float = Field(ge=0)

    # 5. Initial Holders (Mobyscreener)
    holders_count: int = Field(ge=0)

    # 6. LP Count (DexScreener)
    lp_count: int = Field(ge=1, description="Number of liquidity pools")

    # 7. LP/MCap Ratio (DexScreener)
    lp_mcap_ratio: float = Field(ge=0, description="Liquidity to Market Cap ratio")
    
    # 8. Holder Distribution (Mobyscreener)
    top_10_holders_percent: float = Field(ge=0, le=100)

    # 9. Bundle Percentage (skipped for now - no free API)
    bundle_percent: Optional[float] = Field(
        default=None, ge=0, le=100, description="Percentage of bundled transactions"
    )


