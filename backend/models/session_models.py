"""Session, agent name, status, wave enums."""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AgentName(str, Enum):
    IDEA_PARSER = "idea_parser"
    ARTICULATION = "articulation"
    MARKET_RESEARCH = "market_research"
    COMPETITIVE_ANALYSIS = "competitive_analysis"
    BUSINESS_MODEL = "business_model"
    BRAND_IDENTITY = "brand_identity"
    RISK_ANALYSIS = "risk_analysis"
    TECH_ARCHITECTURE = "tech_architecture"
    FINANCIAL_MODEL = "financial_model"
    LANDING_PAGE = "landing_page"
    LEGAL_DOCUMENTS = "legal_documents"
    GO_TO_MARKET = "go_to_market"
    PITCH_DECK = "pitch_deck"
    EXECUTIVE_SUMMARY = "executive_summary"


class Wave(str, Enum):
    PRE = "pre"
    WAVE_1 = "wave_1"
    WAVE_2 = "wave_2"
    WAVE_3 = "wave_3"


class AgentStatusValue(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"
    GATE_REJECTED = "gate_rejected"
    SAFETY_BLOCKED = "safety_blocked"
    SKIPPED = "skipped"


class SessionStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    PARTIAL = "partial"
    ERROR = "error"
    CANCELED = "canceled"
    SAFETY_BLOCKED = "safety_blocked"
    BUDGET_EXCEEDED = "budget_exceeded"


class AgentRecord(BaseModel):
    name: AgentName
    wave: Wave
    status: AgentStatusValue = AgentStatusValue.PENDING
    started_at: datetime | None = None
    completed_at: datetime | None = None
    duration_ms: int | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    retry_count: int = 0
    error_message: str | None = None
    output_ref: str | None = None  # Firestore subcollection doc id


class CostTelemetry(BaseModel):
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_cost_usd: float = 0.0
    grounding_calls: int = 0
    workspace_api_calls: int = 0
    image_generations: int = 0


class Session(BaseModel):
    session_id: str
    user_uid: str
    company_id: str | None = None
    branch_id: str | None = None
    parent_session_id: str | None = None
    idempotency_key: str
    idea_text_hash: str  # NEVER store raw idea_text in logs
    idea_text: str  # stored in Firestore only with TTL 30d
    status: SessionStatus = SessionStatus.QUEUED
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    canceled_at: datetime | None = None
    agents: dict[AgentName, AgentRecord] = Field(default_factory=dict)
    cost: CostTelemetry = Field(default_factory=CostTelemetry)
    company_name: str | None = None
    error_code: str | None = None
    error_message: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
