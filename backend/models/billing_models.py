"""Billing / subscription models."""
from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel


class SubscriptionTier(str, Enum):
    WHISPER = "whisper"  # free, 1 quick run/mo
    FOUNDER = "founder"  # $29/mo
    FOUNDER_PRO = "founder_pro"  # $79/mo
    TEAM = "team"  # $149/mo / 5 seats
    COHORT = "cohort"  # custom $5K-$50K
    INTERNAL = "internal"  # bypass


class StripeWebhookEvent(BaseModel):
    id: str
    type: str
    data: dict[str, Any]
    created: int
    livemode: bool


class CheckoutRequest(BaseModel):
    tier: SubscriptionTier
    seats: int = 1
    success_url: str
    cancel_url: str


class MarketplaceJob(BaseModel):
    job_type: str  # "lawyer_review", "brand_polish", "cfo_review"
    company_id: str
    price_usd: float
    provider: str
    status: str
    created_at: str
