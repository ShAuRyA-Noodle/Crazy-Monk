"""User and role models."""
from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field

from .billing_models import SubscriptionTier


class UserRole(str, Enum):
    USER = "user"
    COHORT_ADMIN = "cohort_admin"
    INTERNAL = "internal"


class UsageCounter(BaseModel):
    period: str  # "2026-05" or "2026-W19" or "2026-05-08"
    generations: int = 0
    tokens: int = 0
    cost_usd: float = 0.0


class User(BaseModel):
    uid: str
    email: EmailStr | None = None
    display_name: str | None = None
    role: UserRole = UserRole.USER
    tier: SubscriptionTier = SubscriptionTier.WHISPER
    stripe_customer_id: str | None = None
    cohort_id: str | None = None
    created_at: datetime
    last_active_at: datetime | None = None
    counters: dict[str, UsageCounter] = Field(default_factory=dict)
    consent: dict[str, bool] = Field(default_factory=dict)  # gdpr, marketing, retention
    locale: str = "en-US"
    region: str = "US"
