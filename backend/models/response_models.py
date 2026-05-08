"""Outbound response models."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel

from .session_models import AgentRecord, CostTelemetry, SessionStatus


class GenerateResponse(BaseModel):
    session_id: str
    status: SessionStatus
    sse_url: str
    estimated_completion_seconds: int


class AgentOutputResponse(BaseModel):
    agent: str
    status: str
    completed_at: datetime | None
    result: dict[str, Any]
    cost_usd: float


class SessionResponse(BaseModel):
    session_id: str
    status: SessionStatus
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    company_name: str | None
    agents: dict[str, AgentRecord]
    cost: CostTelemetry
    error_code: str | None = None


class HealthResponse(BaseModel):
    ok: bool
    env: str
    version: str
    git_sha: str | None = None
