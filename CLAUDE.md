# CLAUDE.md — PROMETHEUS

Guidance for Claude Code when working in this repo. Read this before generating code.

## Project Overview

PROMETHEUS is a multi-agent system that turns a voice/text startup idea into a coherent company package (brand, business model, market research, competitive analysis, financials, deck, landing page, legal docs, GTM, risk, architecture, exec summary) in ~75–120 seconds. It uses Google ADK orchestration with Gemini 2.5 Pro (synthesis/grounded search) and Flash (structured output), Firestore for durable state, Cloud Tasks for queue/worker decoupling, Vertex AI Agent Engine for production session management, and SSE for live streaming reasoning to the React frontend.

The whole point of V2 is **anti-fakery**: real data sources (USPTO, Domainr, Crunchbase/Statista), deterministic financial engine, content moderation, validation gates between waves, structured outputs (no regex JSON repair), proper auth and persistence, sandboxed iframe rendering, files owned by users (not service account), GDPR/CCPA compliance, and the killer UX layer (streaming reasoning sidebar, progressive artifact rendering, in-app deck editor, financial scenario sliders, branching, watched dashboard, Cmd-K).

## Hard Constraints (DO NOT violate)

1. **Never write `service-account.json` paths into Docker layers.** Use Workload Identity Federation in prod; local dev mounts via Secret Manager mock.
2. **Drive scope is `drive.file` only.** Never request the full `drive` scope.
3. **No raw HTML/SVG from agents goes to the DOM unsanitized.** All HTML/SVG agent outputs MUST pass through `services/sanitization.py` (server) AND DOMPurify (client) before rendering.
4. **Iframes for generated landing pages are `sandbox="allow-forms"` only** — no `allow-scripts`, no `allow-same-origin`. CSP headers injected server-side.
5. **No agent ever writes ToS/Privacy from scratch.** Use template-fill via Termly/iubenda APIs + lawyer-review CTA. Generation pipeline calls `services/legal_template_service.py`, never asks Gemini for legal text.
6. **Every agent uses Gemini structured output** (`response_mime_type="application/json"`, `response_schema=AgentOutputSchema`). No "regex extraction fallback" code. On validation failure → 1 re-prompt with Pydantic error injected → fail with structured error.
7. **Validation gates between waves are mandatory** (Pydantic + Vertex Safety + USPTO/domain check for Brand). Wave N+1 cannot start until Wave N gates pass.
8. **Idea text length cap = 2000 chars** enforced in Pydantic request model. Reject 413.
9. **Vertex AI Safety pre-filter on `idea_text`** before any agent runs. Block CSAM, weapons, IP infringement, fraud categories.
10. **Idempotency-Key header required on POST /api/generate.** Repeat = same session_id, no re-run.
11. **Cost telemetry per session.** Hard cap `MAX_COST_USD_PER_SESSION` ($2.50 default). Worker aborts on breach.
12. **No `idea_text` in Cloud Logging.** Hash before log. Raw text only in Firestore with TTL 30 days.
13. **Owner transfer of generated files.** Use OAuth → user owns at creation. Service account never holds permanent assets.

## Code Conventions

### Python (backend/)
- Python 3.11+, `from __future__ import annotations` at top of every module
- Pydantic v2 only. Never v1. Never `dataclass` for I/O models.
- `models.py`-style: every agent has its `OutputSchema` Pydantic model in `backend/models/agent_schemas.py` — single source of truth.
- Async-first. FastAPI handlers `async def`. Workspace API calls wrapped in `run_in_executor`.
- File naming: `{role}_agent.py`, output state keys: `{role}_result`.
- Imports: stdlib → third-party → local. `ruff` enforced.
- Type hints mandatory. `mypy --strict` on `backend/agents/`, `backend/services/`, `backend/models/`.
- Logging via `structlog` JSON. Never `print`. Never log `idea_text`.
- Errors raise `PrometheusError` subclasses (`AgentTimeoutError`, `AgentValidationError`, `GateRejectedError`, `CostBudgetExceeded`).
- Tests: pytest, `pytest-asyncio`, golden ideas in `backend/tests/golden/ideas.json` (50 entries).

### TypeScript (frontend/)
- TS 5 strict mode. `noImplicitAny`, `strictNullChecks`, `noUncheckedIndexedAccess`.
- React 18 functional components only. Hooks: `useXxx.ts`. Components: `Xxx.tsx` PascalCase.
- Tailwind v4 via `@tailwindcss/postcss`. Use `min-h-[100dvh]` not `h-screen` (taste-skill rule). CSS Grid not flex-math.
- No `any`. Agent output types in `src/types/agents.ts` mirror backend Pydantic schemas.
- Framer Motion: spring physics `stiffness: 100, damping: 20` (taste-skill rule). Animate `transform` + `opacity` only.
- DOMPurify mandatory for any agent-emitted HTML/SVG. Centralize in `lib/purify.ts`.
- Anti-slop rules from `~/.claude/skills/design-taste-frontend/SKILL.md` apply: no Inter font, no purple/blue gradients, no generic 3-card row, no "John Doe" / "99.99%" sample data, no "Acme/Nexus/Flow" fake names.

### Naming
- **Codenames**: uppercase mythological (kept this for PROMETHEUS).
- Files: `*_BLUEPRINT.md`, snake_case Python, PascalCase classes, camelCase TS hooks.
- Agent files: `{role}_agent.py`. Output state keys: `{role}_result`.
- Frontend: `useXxx.ts`, `Xxx.tsx`, `lib/xxx.ts`.

### Documentation
- Every blueprint opens with `> **Tagline:** "..."` blockquote.
- Section structure: Context → Problem → Insight → Architecture → APIs → File Tree → Prompts → Demo → Sprint → Risks → Business → Judging → Appendices.
- Comparison tables for tools/competitors. Dollar-anchor every problem. ASCII box diagrams for architecture.
- Latency annotations next to each component. Cost-per-run summary.
- "Cut if behind" markers in build plans.

### Commits
- Conventional Commits style (`feat:`, `fix:`, `chore:`, `refactor:`, `test:`, `docs:`).
- Co-author trailer: `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>`.
- Never bypass hooks (`--no-verify`).

## Project Structure (top-level)

```
backend/        FastAPI + ADK + 13 agents + services + middleware + workers + tests
frontend/       React/Vite/TS/Tailwind4/Framer + in-app editors + Cmd-K + PostHog
infrastructure/ Cloud Run, Firestore rules/indexes, Cloud Tasks, Cloud Armor, budget alerts
scripts/        setup.sh, dev.sh, deploy.sh, test.sh, benchmark.sh, seed-golden-ideas.sh
docs/           ARCHITECTURE, SECURITY, DEPLOYMENT, REFERENCE_CLAUDE_md_supplymind
reference_blueprints/  NEXUS, SYMPHONY, SUPPLYMIND_PHASES (architecture grammar reference)
.claude/        commands/, skills/, settings.json
```

## The 13 Agents (waves)

- **Pre-Wave** (Flash, ~3s each): Idea Parser, Articulation (NEW — polishes user input before pipeline)
- **Wave 1** (parallel, no dependencies): Market Research [Pro+grounding], Competitive Analysis [Pro+grounding], Business Model [Flash], Brand Identity [Flash], Risk Analysis [Flash], Tech Architecture [Flash]
- **Gate 1**: Pydantic schema validation + Vertex Safety + USPTO trademark + Domainr domain check on Brand → re-roll if conflict
- **Wave 2** (parallel, partial deps): Financial Model [Pro, deterministic engine], Landing Page [Flash + Imagen heroes], Legal Docs [template-fill, NOT pure LLM], Go-to-Market [Flash]
- **Gate 2**: schema + WCAG palette validation + landing HTML sanitization
- **Wave 3** (parallel, full deps): Pitch Deck [Pro, template-copy + Imagen], Executive Summary [Pro]
- **Gate 3**: final cross-artifact coherence check

## Dependencies

Pin everything. `pip install --require-hashes -r requirements.txt`. `npm ci` (lockfile). `pip-audit` + `Snyk` in CI.

## Testing

- pytest unit tests per agent (mock Gemini, assert schema)
- Golden idea regression suite (50 ideas in `backend/tests/golden/ideas.json`)
- Integration test: full pipeline end-to-end on a real Gemini call (1 idea, gated by `RUN_INTEGRATION=1`)
- Frontend: Vitest for hooks, Playwright for e2e
- Security: pre-commit `git-secrets`, weekly `pip-audit` + `npm audit`

## Environment

See `.env.example`. Local dev: copy to `.env`, fill required keys. Prod: Secret Manager + Workload Identity.

## Useful commands

```bash
./scripts/dev.sh          # spin backend + frontend together
./scripts/test.sh         # full test suite
./scripts/benchmark.sh    # latency + cost benchmark on golden ideas
./scripts/deploy.sh       # Cloud Build + Cloud Run + Firebase Hosting
```
