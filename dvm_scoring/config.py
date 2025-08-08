from __future__ import annotations

import os


def _get_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, default))
    except Exception:
        return default


# Thresholds can be tuned via env vars
FEES_MIN_SOL_NEW = _get_float("FEES_MIN_SOL_NEW", 5.0)
FEES_MIN_SOL_MIGRATED = _get_float("FEES_MIN_SOL_MIGRATED", 5.0)

# By default, we do NOT enforce fees for legacy/old tokens because upstream
# sources may not have historical compute. This can be overridden.
APPLY_FEES_TO_OLD = os.getenv("APPLY_FEES_TO_OLD", "false").lower() in {
    "1",
    "true",
    "yes",
}

