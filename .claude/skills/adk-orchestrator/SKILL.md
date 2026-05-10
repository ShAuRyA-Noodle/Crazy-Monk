---
name: adk-orchestrator
description: PROMETHEUS Google ADK orchestrator discipline — auto-invokes when editing backend/agents/orchestrator.py or backend/agents/gates.py. Enforces SequentialAgent[ParallelAgent] topology, output_key contract, gate insertion between waves, pre-summarization for Wave 3, idempotency, cost telemetry per agent, callback hooks.
---

# ADK Orchestrator Discipline

You are working in PROMETHEUS's wave orchestrator. The system uses Google ADK with Gemini 2.5 Pro/Flash to run 13 agents in three dependency waves with hard gates between them.

This file applies whenever you are editing:
- `backend/agents/orchestrator.py`
- `backend/agents/gates.py`
- `backend/agents/base.py`
- `backend/agents/_summarize.py`

## The topology

```
SequentialAgent(
  PreWave         = SequentialAgent(idea_parser, articulation),
  Wave1           = ParallelAgent(market, competitive, business, brand, risk, tech),
  Gate1           = WaveGate(GATE_1),
  Wave2           = ParallelAgent(financial, landing, legal, gtm),
  Gate2           = WaveGate(GATE_2),
  Wave3PreSummary = SequentialAgent(per-agent _summarizer × 11),
  Wave3           = ParallelAgent(pitch_deck, executive_summary),
  Gate3           = WaveGate(GATE_3),
)
```

Pre-summarization sits **between** Gate 2 and Wave 3 — never inside Wave 3 itself.

## Hard rules

### R1. Output-key contract
Every agent writes its result under the state key `{name}_result`. Never invent new keys. The orchestrator reads/writes ONLY through these keys. Other modules (gates, frontend, summarizer) depend on this contract.

### R2. Gate insertion is mandatory
Wave N+1 cannot start until Gate N passes. A gate failure sets:
- `state["status"] = "PARTIAL"`
- All downstream agents to `"SKIPPED"`
- A structured `GateResult` with `issues: list[GateIssue]` for the user

### R3. Idempotency invariants
- The worker is idempotent. If `session.status` is already in `RUNNING` or terminal at the start of `/internal/run`, return 200 immediately.
- Re-running a session must NOT re-charge cost (cost-per-agent is recorded at agent completion, not start).
- Cloud Tasks retries on 5xx; the worker MUST distinguish 4xx (terminal) from 5xx (retryable).

### R4. Cost telemetry per agent
- After every Gemini call, record `cost_usd` on `state["agent_cost"][agent_name]`.
- Sum into `session.cost_total` after each agent.
- Before each agent runs, check `session.cost_total >= MAX_COST_USD_PER_SESSION` → raise `CostBudgetExceeded`.
- Aborts the pipeline; status → `FAILED`; user sees structured error.

### R5. Pre-summarization for Wave 3 only
- Wave 3 agents read up to 10 upstream outputs.
- Raw concat balloons context to 15K+ tokens.
- Solution: `_summarize.py` runs Flash with `response_schema=AgentSummary` per upstream agent (≤500 chars + `key_numbers[]`).
- The Wave 3 prompts include only the summaries.
- Effect: cost drops from $0.18 to $0.085 on `pitch_deck`; coherence improves.

### R6. Callback hooks
ADK provides `before_model_callback` and `after_model_callback`. Use these (not custom wrappers) to:
- Emit SSE events ("agent X started" / "agent X completed")
- Record cost telemetry
- Inject grounded-search sanitization

### R7. Structured outputs always
- Every Gemini call uses `response_mime_type="application/json"` + `response_schema=<Pydantic>`.
- Never call Gemini without a schema. Never use regex to parse output.
- On schema validation fail: 1 retry with the Pydantic error injected into the next prompt; if 2nd fails, raise `AgentValidationError`.

### R8. Safety pre-filter is upstream of the orchestrator
- The orchestrator assumes `idea_text` has already been Vertex-Safety-checked (gateway middleware).
- Do NOT re-check inside the orchestrator (cost amplification).
- Wave 1 outputs that contain potentially-unsafe text run a Vertex Safety check at Gate 1 (text fields like `worst_case_scenario`).

### R9. Async-first
- `async def run()` for every agent.
- Wave parallelism via `asyncio.gather()` — NEVER threading.
- External calls wrapped in `run_in_executor` only when the SDK is sync-only (Workspace API).

### R10. No mutable shared state
- The orchestrator owns the state dict.
- Each agent receives a copy and returns its result.
- Do not let agents mutate sibling agents' outputs.

## Anti-patterns

- ❌ "Quick optimization": skip Gate 2 for runs you trust. **Never.** Gates are non-negotiable.
- ❌ Combining Wave 1 + Wave 2 into a single `ParallelAgent` to save 1.2s on a gate. The gate is the dependency boundary; you cannot remove it.
- ❌ Caching agent outputs across sessions. Agent runs are scoped to a session+branch. Cache external API calls (USPTO, Domainr) instead.
- ❌ Adding a 14th agent without a wave assignment. Every new agent must declare its wave + dependencies + cost budget.

## When you change orchestrator.py or gates.py

You MUST also:
1. Update `docs/ARCHITECTURE.md` (sequence diagram + topology) in the same PR
2. Add or update tests in `backend/tests/test_orchestrator.py` and `backend/tests/test_gates.py`
3. Add a regression test if you closed a V1 audit finding (`backend/tests/security/`)
4. If a gate threshold changed, document the new threshold in `docs/SECURITY.md` (defense-in-depth catalog)

## Reading order before editing

1. `CLAUDE.md` — hard constraints
2. `PROMETHEUS_BLUEPRINT_V2.md` §3 (the 13 agents) and §6 (backend architecture)
3. The current `orchestrator.py` and `gates.py`
4. `docs/ARCHITECTURE.md` — current sequence diagrams
