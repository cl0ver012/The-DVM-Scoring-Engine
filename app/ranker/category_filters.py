"""
Category-specific filters for ranking
Each category has different requirements
"""

from typing import Dict, Any


def is_eligible_for_new(token_data: Dict[str, Any]) -> bool:
    """
    New category: Fresh tokens (1-24 hours old) that passed pre-filter
    Focus on early gems with good fundamentals
    """
    age_minutes = token_data.get('token_age_minutes', 0)
    # Must be between 1 hour and 24 hours (fresh tokens)
    # Pre-filter already ensures > 1 hour
    return age_minutes <= 1440  # age <= 24h


def is_eligible_for_surging(token_data: Dict[str, Any]) -> bool:
    """
    Surging category: Tokens showing strong momentum (any age)
    Focus on tokens that are actively pumping
    Pre-filter already ensures > 1h
    """
    # No age restriction for surging - pre-filter handles safety
    return True


def is_eligible_for_all(token_data: Dict[str, Any]) -> bool:
    """
    All category: Any token that passed pre-filter
    General ranking across all safe tokens
    Pre-filter already ensures > 1h
    """
    # No age restriction for all - pre-filter handles safety
    return True


def get_category_filter(category: str):
    """Get the appropriate filter function for a category"""
    filters = {
        "New": is_eligible_for_new,
        "Surging": is_eligible_for_surging,
        "All": is_eligible_for_all
    }
    return filters.get(category, is_eligible_for_all)
