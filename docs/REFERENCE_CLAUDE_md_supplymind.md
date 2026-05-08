# CLAUDE.md - SupplyMind OpenEnv Environment

## Project Overview

SupplyMind is an OpenEnv-compliant environment that simulates **supply chain risk management**. An AI agent acts as a supply chain risk manager: it receives disruption signals (typhoons, strikes, sanctions, cascading crises) and takes actions (reroute shipments, activate backup suppliers, hedge commodities) to minimize financial impact on a global supply chain network.

**Stack:** Python 3.11 + FastAPI + Pydantic v2 + NetworkX + NumPy
**Framework:** OpenEnv (Meta + Hugging Face standard for AI agent environments)

---

## Competition Rules (MUST FOLLOW - Disqualification if violated)

### OpenEnv Spec Compliance (MANDATORY)
- Implement full OpenEnv interface with typed Pydantic models
- `step(action)` → returns observation, reward, done, info
- `reset()` → returns initial observation (clean state every time)
- `state()` → returns current episode metadata
- `openenv.yaml` with environment metadata and task list
- Must pass `openenv validate`

### Tasks & Graders (MANDATORY)
- Minimum 3 tasks with programmatic graders
- Difficulty progression: easy → medium → hard
- Graders produce scores between 0.0 and 1.0
- Graders MUST be deterministic and reproducible
- Graders MUST return DIFFERENT scores for different agent strategies
- **DISQUALIFICATION:** Graders that always return the same score

### Reward Function (MANDATORY)
- Provide signal over full trajectory (NOT just end-of-episode binary)
- Reward partial progress toward task completion
- Penalize clearly undesirable behavior (infinite loops, destructive actions, unnecessary spending)

### Baseline Inference Script (MANDATORY)
- Uses OpenAI API client (NOT Anthropic/Claude)
- Reads API credentials from `OPENAI_API_KEY` environment variable
- Produces reproducible baseline score on ALL 3 tasks
- **DISQUALIFICATION:** No baseline inference script

### Deployment (MANDATORY)
- Working Dockerfile: `docker build + docker run` must work cleanly
- Deploy to Hugging Face Spaces as containerized Docker space
- Tag with `openenv`
- **DISQUALIFICATION:** Environment does not deploy or respond

### Required API Endpoints
- `POST /reset` - Reset environment, optionally with task_id
- `POST /step` - Execute action, return observation
- `GET /state` - Return current episode state
- `GET /tasks` - Return list of tasks and action schema
- `POST /grader` - Return grader score after episode completed
- `POST /baseline` - Trigger baseline inference and return scores for all 3 tasks
- `GET /health` - Health check endpoint

### Documentation (MANDATORY)
- README.md must include:
  - Environment description and motivation
  - Action and observation space definitions
  - Task descriptions with expected difficulty
  - Setup and usage instructions
  - Baseline scores

---

## Evaluation Criteria (How We Are Scored)

| Criterion | Weight | What Judges Look For |
|-----------|--------|---------------------|
| **Real-world utility** | 30% | Genuine task modeling, would someone use this to train/evaluate agents? |
| **Task & grader quality** | 25% | Clear objectives, fair graders, meaningful difficulty progression, hard task challenges frontier models |
| **Environment design** | 20% | Clean state management, sensible action/observation spaces, good reward shaping, proper episode boundaries |
| **Code quality & spec compliance** | 15% | OpenEnv spec compliance, clean structure, typed models, documented, tested, Dockerfile works |
| **Creativity & novelty** | 10% | Novel domain, interesting mechanics, clever reward design, original approach |

---

## Disqualification Criteria (AVOID AT ALL COSTS)

1. Environment does not deploy or respond
2. Plagiarized or trivially modified existing environments
3. Graders that always return the same score
4. No baseline inference script

---

## Pre-Submission Checklist (ALL must pass)

- [ ] HF Space deploys: Automated ping returns 200 + responds to reset()
- [ ] OpenEnv spec: openenv.yaml valid, typed models, step/reset/state endpoints work
- [ ] Dockerfile builds: `docker build` on submitted repo succeeds
- [ ] Baseline reproduces: Inference script completes without error, produces scores
- [ ] 3+ tasks with graders: All enumerate, graders return scores in [0.0, 1.0]
- [ ] Graders produce different scores for different strategies

---

## Judging Process

1. **Phase 1 - Automated Validation:** Pass/fail gate — HF Space deploys, OpenEnv spec compliance, Dockerfile builds, baseline reproduces, 3+ tasks with graders
2. **Phase 2 - Agentic Evaluation:** Scored — baseline re-run, standard Open LLM (e.g. Nemotron 3 Super) run against environment, score variance check
3. **Phase 3 - Human Review:** Top submissions reviewed by Meta and Hugging Face engineers for real-world utility, creativity, exploit checks

---

## Code Conventions

### Python Style
- Python 3.11+ with type hints everywhere
- Pydantic v2 for all data models (BaseModel, not dataclass)
- Use `from __future__ import annotations` for forward references
- Snake_case for functions/variables, PascalCase for classes
- Docstrings on all public functions

### Project Structure
- `models.py` at root - THE single source of truth for agent-environment contract
- `server/engine/` - Pure simulation logic, no HTTP concerns
- `server/tasks/` - Task definitions, isolated per difficulty
- `server/graders/` - Grading logic, deterministic
- `server/app.py` - FastAPI only, thin layer over environment
- `server/data/` - JSON data files for graphs and scenarios
- `tests/` - pytest tests

### Key Design Principles
- Pre-scripted disruptions (not random) for deterministic, reproducible grading
- Single action per step (forces prioritization)
- Dense per-step rewards (7 components, not sparse binary)
- Budget constraints that tighten with difficulty
- Dual observation format: structured Pydantic fields + natural language situation_summary

### Dependencies (keep minimal)
- fastapi, uvicorn - HTTP server
- pydantic>=2.0 - Data models
- networkx>=3.2 - Supply chain graph
- numpy - Monte Carlo, numerical ops
- openai>=1.0 - Baseline inference only

### Testing
- pytest for all tests
- Test grader variance: different strategies MUST produce different scores
- Test do-nothing agent scores low (~0.15-0.35)
- Test that reset() produces clean state

---

## Environment Design

### 7 Action Types
1. `do_nothing` - No action (may be optimal when no disruption)
2. `activate_backup_supplier` - Switch to backup supplier (15-30% cost premium)
3. `reroute_shipment` - Use alternative shipping route/port
4. `increase_safety_stock` - Order extra inventory buffer
5. `expedite_order` - Upgrade transport mode (sea→air, 5-10x cost)
6. `hedge_commodity` - Hedge against commodity price spikes
7. `issue_supplier_alert` - Request status update from supplier (free, info-only)

### 3 Tasks
1. **Easy - "Typhoon Response"**: 12 nodes, 30 steps, $5M budget, single disruption
2. **Medium - "Multi-Front Crisis"**: 25 nodes, 45 steps, $8M budget, 3 concurrent disruptions
3. **Hard - "Cascading Crisis"**: 40 nodes, 60 steps, $10M budget, geopolitical cascade

### Reward Components (per step, range [-1.0, 1.0])
- Revenue preservation: 35%
- Proactive action bonus: 15%
- Cost penalty: 10%
- Stockout penalty: 25%
- Unnecessary action penalty: 5%
- Health score maintenance: 5%
- SLA compliance: 5%
