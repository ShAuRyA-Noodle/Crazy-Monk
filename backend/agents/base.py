"""Base agent class. All 13 agents inherit. Wraps Gemini structured output, retry, cost telemetry."""
from __future__ import annotations

import asyncio
import time
from abc import ABC, abstractmethod
from typing import Any, ClassVar, Generic, TypeVar

import structlog
from pydantic import BaseModel, ValidationError

from config import settings
from models.session_models import AgentName, AgentStatusValue, Wave

T = TypeVar("T", bound=BaseModel)
log = structlog.get_logger()


# ─── Cost table (USD per 1M tokens) ─────────────────────────────────────────

_PRICING: dict[str, tuple[float, float]] = {
    "gemini-2.5-pro": (1.25, 10.0),
    "gemini-2.5-flash": (0.50, 3.0),
}


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    in_rate, out_rate = _PRICING.get(model, (1.25, 10.0))
    return (input_tokens * in_rate + output_tokens * out_rate) / 1_000_000


# ─── Errors ──────────────────────────────────────────────────────────────────


class PrometheusError(Exception):
    code: ClassVar[str] = "PROMETHEUS_ERROR"


class AgentTimeoutError(PrometheusError):
    code = "AGENT_TIMEOUT"


class AgentValidationError(PrometheusError):
    code = "AGENT_VALIDATION"


class AgentSafetyBlocked(PrometheusError):
    code = "SAFETY_BLOCKED"


class GateRejectedError(PrometheusError):
    code = "GATE_REJECTED"


class CostBudgetExceeded(PrometheusError):
    code = "COST_BUDGET_EXCEEDED"


# ─── Result envelope ─────────────────────────────────────────────────────────


class AgentResult(BaseModel, Generic[T]):
    output: T | None
    status: AgentStatusValue
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    duration_ms: int = 0
    retry_count: int = 0
    error_code: str | None = None
    error_message: str | None = None


# ─── Base agent ──────────────────────────────────────────────────────────────


class PrometheusAgent(ABC, Generic[T]):
    """Concrete agents implement `prompt_template`, `output_schema`, `model`, `wave`, `name`,
    and optionally `before_model` / `after_model` hooks."""

    name: ClassVar[AgentName]
    wave: ClassVar[Wave]
    model: ClassVar[str]
    output_schema: ClassVar[type[BaseModel]]
    prompt_template: ClassVar[str]
    requires_grounding: ClassVar[bool] = False
    timeout_seconds: ClassVar[int] = 60
    temperature: ClassVar[float] = 0.4

    def __init__(self) -> None:
        self.logger = log.bind(agent=self.name.value, wave=self.wave.value)

    # ---- Subclass hooks ----

    def render_prompt(self, state: dict[str, Any]) -> str:
        return self.prompt_template.format(**state)

    async def before_model(self, state: dict[str, Any]) -> dict[str, Any]:
        return state

    async def after_model(self, output: T, state: dict[str, Any]) -> T:
        return output

    # ---- Core run ----

    async def run(self, state: dict[str, Any]) -> AgentResult[T]:
        from services.gemini_client import call_gemini_structured  # local to avoid cycles

        started = time.perf_counter()
        retry = 0
        last_error: Exception | None = None

        while retry <= settings.agent_max_retries:
            try:
                state = await self.before_model(state)
                rendered = self.render_prompt(state)

                self.logger.info("agent.start", retry=retry, prompt_chars=len(rendered))

                raw, in_tok, out_tok, was_blocked = await asyncio.wait_for(
                    call_gemini_structured(
                        model=self.model,
                        prompt=rendered,
                        response_schema=self.output_schema,
                        grounded=self.requires_grounding,
                        temperature=self.temperature,
                    ),
                    timeout=self.timeout_seconds,
                )

                if was_blocked:
                    raise AgentSafetyBlocked("model returned safety block")

                try:
                    output = self.output_schema.model_validate(raw)
                except ValidationError as ve:
                    if retry < settings.agent_max_retries:
                        self.logger.warning("agent.validation_retry", error=str(ve))
                        state["_validation_error"] = str(ve)
                        retry += 1
                        last_error = ve
                        continue
                    raise AgentValidationError(str(ve)) from ve

                output = await self.after_model(output, state)  # type: ignore[arg-type]
                cost = estimate_cost(self.model, in_tok, out_tok)
                duration = int((time.perf_counter() - started) * 1000)

                self.logger.info(
                    "agent.complete",
                    duration_ms=duration,
                    in_tokens=in_tok,
                    out_tokens=out_tok,
                    cost_usd=round(cost, 4),
                )

                return AgentResult[T](
                    output=output,
                    status=AgentStatusValue.COMPLETED,
                    input_tokens=in_tok,
                    output_tokens=out_tok,
                    cost_usd=cost,
                    duration_ms=duration,
                    retry_count=retry,
                )

            except AgentSafetyBlocked as e:
                self.logger.warning("agent.safety_blocked")
                return AgentResult[T](
                    output=None,
                    status=AgentStatusValue.SAFETY_BLOCKED,
                    duration_ms=int((time.perf_counter() - started) * 1000),
                    retry_count=retry,
                    error_code=e.code,
                    error_message=str(e),
                )
            except TimeoutError as e:
                last_error = e
                if retry < settings.agent_max_retries:
                    retry += 1
                    self.logger.warning("agent.timeout_retry", retry=retry)
                    continue
                self.logger.error("agent.timeout_final")
                return AgentResult[T](
                    output=None,
                    status=AgentStatusValue.ERROR,
                    duration_ms=int((time.perf_counter() - started) * 1000),
                    retry_count=retry,
                    error_code=AgentTimeoutError.code,
                    error_message="agent timeout",
                )
            except PrometheusError as e:
                self.logger.error("agent.error", code=e.code, message=str(e))
                return AgentResult[T](
                    output=None,
                    status=AgentStatusValue.ERROR,
                    duration_ms=int((time.perf_counter() - started) * 1000),
                    retry_count=retry,
                    error_code=e.code,
                    error_message=str(e),
                )
            except Exception as e:  # noqa: BLE001
                self.logger.exception("agent.unexpected")
                last_error = e
                if retry < settings.agent_max_retries:
                    retry += 1
                    continue
                return AgentResult[T](
                    output=None,
                    status=AgentStatusValue.ERROR,
                    duration_ms=int((time.perf_counter() - started) * 1000),
                    retry_count=retry,
                    error_code="UNEXPECTED",
                    error_message=str(e),
                )

        return AgentResult[T](
            output=None,
            status=AgentStatusValue.ERROR,
            duration_ms=int((time.perf_counter() - started) * 1000),
            retry_count=retry,
            error_code="UNEXPECTED",
            error_message=str(last_error) if last_error else "unknown",
        )

    @property
    @abstractmethod
    def output_key(self) -> str:
        """Session-state key downstream agents read this agent's output from."""

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} model={self.model} wave={self.wave.value}>"
