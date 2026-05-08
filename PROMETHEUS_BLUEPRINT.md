# PROMETHEUS: Master Blueprint
**"You whisper a startup idea. 4 minutes later you have a full company."**

---

## Context

Founders today spend 40-200 hours and $2,000-$15,000 assembling the startup toolkit — business plan, financial model, pitch deck, landing page, legal docs, brand identity, competitive analysis, go-to-market strategy. Each artifact requires different expertise and is produced by different tools that don't talk to each other, leading to inconsistent narratives, fabricated data, and massive time waste.

PROMETHEUS solves this by deploying a swarm of 12 specialized AI agents running in parallel — powered by Google ADK and Gemini 2.5 — that produce a complete, coherent, interconnected company package in under 4 minutes from a single voice input.

---

## SECTION 1: PROBLEM DEFINITION & VISION

### 1.1 The Problem
A founder with an idea faces a gauntlet:
- **Business plan**: 20-40 hours writing, or $1,500-$5,000 for a consultant
- **Financial model**: 10-20 hours in spreadsheets, or $2,000 for an analyst
- **Pitch deck**: 15-30 hours designing, or $1,000-$7,000 for an agency
- **Landing page**: 10-20 hours building, or $500-$3,000 for a developer
- **Legal docs**: $2,000-$10,000 for a lawyer for basic ToS/Privacy
- **Brand identity**: 5-15 hours, or $500-$5,000 for a designer
- **Market research**: 20-40 hours, or $3,000-$15,000 for a research firm
- **GTM strategy**: 10-20 hours of planning

**Total: 100-200 hours, $10,000-$45,000, and 2-6 weeks of elapsed time.** Most solo founders skip half these steps, launching with gaps that cost them investor meetings, customers, and credibility.

### 1.2 Market Quantification
- ~137 million new businesses started globally per year
- 23+ AI business plan generators exist, 23+ AI pitch deck tools — none cover the full lifecycle
- AI SaaS market: $71.5B (2024) → $775B by 2031
- 88% of startups using AI-generated decks report increased investor engagement
- Average pitch deck agency charges $3,500 — total addressable market for deck generation alone: ~$4.8B/year

### 1.3 Why Now?
- **Gemini 2.5 Pro/Flash** (March 2026): 1M token context, grounded search via ADK tools, multimodal I/O — enough to synthesize entire companies
- **Google ADK**: Native ParallelAgent, SequentialAgent, and LoopAgent primitives — purpose-built for multi-agent orchestration
- **Firestore real-time listeners**: Enable live dashboard UX with zero WebSocket infrastructure
- **Google Workspace APIs**: Free programmatic creation of Slides, Docs, Sheets — real editable documents, not static PDFs
- **Cost collapse**: A full 12-agent run costs ~$0.28 in API calls — making this economically viable at scale

### 1.4 Vision Statement
PROMETHEUS is the world's first AI co-founding team — a system of 12 specialized agents that collectively possess the expertise of a strategist, analyst, designer, developer, lawyer, and marketer, all working simultaneously to transform an idea into a launch-ready company in minutes.

### 1.5 Three-Year North Star
- **Year 1**: The "startup in a box" — voice → full company package in under 4 minutes
- **Year 2**: Iterative refinement — agents that learn from user feedback, A/B test strategies, and improve outputs over multiple sessions
- **Year 3**: Execution layer — agents that don't just plan but DO (launch ads, set up Stripe, deploy landing pages, file incorporation papers)

### 1.6 Existing Tools & Their Failures
| Tool | What It Does | Where It Fails |
|---|---|---|
| PrometAI | Market research + business plan | 5-30 min, no parallelism, no deck/legal/landing |
| Upmetrics | Guided questionnaire → plan | Rigid, sequential, no downstream assets |
| VentureKit | Quick business plan | **Fabricates market statistics** — presents fake data as real |
| Beautiful.ai | AI pitch deck | Decks only, no plan/financials/legal, rigid templates |
| PlusAI | 300-word brief → slides | Thin output, generic images, no brand consistency |
| IdeaProof | 120-second validation | Shallow analysis, no artifact generation |
| ValidatorAI | Idea scoring + competitor ID | Advisory only — doesn't build anything |

**Gap**: No tool produces all artifacts. No tool runs agents in parallel. No tool grounds research in real-time web data. No tool shows agents working live.

### 1.7 The Unique Insight
Startup creation is not a single-LLM problem — it's a **coordination** problem. A business plan written without market data is fiction. A financial model without a business model is meaningless. A pitch deck without brand identity is generic. The insight: **12 specialized agents sharing state and sequencing their work through dependency waves produce output that is qualitatively different from 12 independent prompts.** The orchestration IS the product.

---

## SECTION 2: CORE TECHNICAL ARCHITECTURE

### 2.1 System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React + Vite)                       │
│  ┌──────────┐  ┌──────────────────┐  ┌───────────────────────────┐  │
│  │Voice/Text│→ │  POST /generate  │→ │  Firestore Real-Time      │  │
│  │  Input   │  │  (session_id)    │  │  Listeners → Dashboard    │  │
│  └──────────┘  └──────────────────┘  └───────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ HTTPS
┌──────────────────────────────▼──────────────────────────────────────┐
│                    BACKEND (FastAPI on Cloud Run)                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │              PROMETHEUS ORCHESTRATOR (Google ADK)             │    │
│  │                                                               │    │
│  │  ┌─────────┐   Agent 0: Idea Parser (Flash)                  │    │
│  │  │ Voice   │──→ Extracts: industry, product_type, target,    │    │
│  │  │ Text    │    geography, differentiator                     │    │
│  │  └─────────┘                                                  │    │
│  │       │                                                       │    │
│  │       ▼ WAVE 1 (ParallelAgent — 6 agents, no dependencies)   │    │
│  │  ┌──────────┬──────────┬──────────┬──────────┬──────┬──────┐ │    │
│  │  │Market    │Compete   │Business  │Brand     │Risk  │Tech  │ │    │
│  │  │Research  │Analysis  │Model     │Identity  │Analy │Arch  │ │    │
│  │  │[Pro]     │[Pro]     │[Flash]   │[Flash]   │[Fl]  │[Fl]  │ │    │
│  │  │~20s      │~20s      │~10s      │~10s      │~10s  │~10s  │ │    │
│  │  └────┬─────┴────┬─────┴────┬─────┴────┬─────┴──────┴──────┘ │    │
│  │       │          │          │          │                      │    │
│  │       ▼ WAVE 2 (ParallelAgent — 4 agents, partial deps)      │    │
│  │  ┌──────────┬──────────┬──────────┬──────────┐               │    │
│  │  │Financial │Landing   │Legal     │Go-to-    │               │    │
│  │  │Model     │Page      │Documents │Market    │               │    │
│  │  │[Pro]     │[Flash]   │[Flash]   │[Flash]   │               │    │
│  │  │~15s      │~12s      │~12s      │~12s      │               │    │
│  │  └────┬─────┴────┬─────┴────┬─────┴────┬─────┘               │    │
│  │       │          │          │          │                      │    │
│  │       ▼ WAVE 3 (ParallelAgent — 2 agents, full deps)         │    │
│  │  ┌──────────┬──────────┐                                     │    │
│  │  │Pitch     │Executive │                                     │    │
│  │  │Deck      │Summary   │                                     │    │
│  │  │[Pro]     │[Pro]     │                                     │    │
│  │  │~25s      │~18s      │                                     │    │
│  │  └──────────┴──────────┘                                     │    │
│  └─────────────────────────────────────────────────────────────┘    │
│       │                    │                    │                    │
│  ┌────▼────┐         ┌────▼────┐         ┌────▼────┐              │
│  │Firestore│         │Workspace│         │ Drive   │              │
│  │State    │         │APIs     │         │ Export  │              │
│  │Sync     │         │Slides/  │         │         │              │
│  │         │         │Docs/    │         │         │              │
│  │         │         │Sheets   │         │         │              │
│  └─────────┘         └─────────┘         └─────────┘              │
└────────────────────────────────────────────────────────────────────┘

TOTAL WALL-CLOCK TIME: ~75 seconds (Wave 1: 20s + Wave 2: 15s + Wave 3: 25s + overhead: 15s)
```

### 2.2 Swarm Orchestration Design

**Framework**: Google Agent Development Kit (ADK) — chosen because:
- Native `ParallelAgent`, `SequentialAgent` primitives — no custom orchestration code needed
- ADK `output_key` mechanism enables agents to read each other's outputs from shared session state
- Direct path to Vertex AI Agent Engine for production deployment
- Judges at Google hackathons recognize and favor ADK usage (10,400 participants in ADK Hackathon)

**Orchestration pattern**: `SequentialAgent` wrapping `ParallelAgent` groups:
```
SequentialAgent("prometheus_pipeline"):
  → idea_parser_agent
  → ParallelAgent("wave1"): [6 agents]
  → ParallelAgent("wave2"): [4 agents]
  → ParallelAgent("wave3"): [2 agents]
```

**Dependency resolution**: Each wave's `ParallelAgent` only starts after the previous `SequentialAgent` step completes. Within each wave, all agents run concurrently. ADK's `output_key` mechanism automatically populates session state, so Wave 2 agents can read Wave 1 results via `{market_research_result}` template syntax in their instructions.

**Inter-agent conflict resolution**: The Brand Identity Agent (Wave 1) is the single source of truth for company name, colors, and voice. All downstream agents reference its output. No agent independently generates a company name.

**Failure handling**: 2 retries per agent, then fallback to hardcoded templates (see Section 11). Failed agents mark `completed_with_fallback` status. Pipeline never fully fails — degrades gracefully.

### 2.3 The 13 Agents (0-12)

#### Agent 0: Idea Parser (Pre-processing)
- **Model**: Gemini 2.5 Flash | **Wave**: Pre-Wave | **Latency**: ~3s
- **Input**: Raw voice transcript text
- **Output**: `parsed_idea` — structured JSON with `idea_summary`, `industry`, `product_type`, `target_market`, `geography`, `key_differentiator`, `data_collection`, `brand_personality_hints`
- **Google APIs**: None (pure LLM)

#### Agent 1: Market Research Agent
- **Model**: Gemini 2.5 Pro (complex reasoning + grounded search) | **Wave**: 1 | **Latency**: 15-25s
- **Input**: `parsed_idea` fields
- **Output**: `market_research_result` — TAM/SAM/SOM with sources, CAGR, industry trends (top 5), target demographics, market timing score
- **Google APIs**: Google Search (via ADK `google_search` tool), Firestore
- **Tokens**: ~2K in / ~3K out | **Cost**: ~$0.033

#### Agent 2: Competitive Analysis Agent
- **Model**: Gemini 2.5 Pro (grounded search + analysis) | **Wave**: 1 | **Latency**: 15-25s
- **Input**: `parsed_idea` fields
- **Output**: `competitive_analysis_result` — top 5-8 competitors with funding/revenue/features/weaknesses, feature comparison matrix, positioning gaps, market concentration
- **Google APIs**: Google Search (via ADK `google_search` tool), Firestore
- **Tokens**: ~2K in / ~4K out | **Cost**: ~$0.043

#### Agent 3: Business Model Agent
- **Model**: Gemini 2.5 Flash | **Wave**: 1 | **Latency**: 8-12s
- **Input**: `parsed_idea` fields
- **Output**: `business_model_result` — revenue model, pricing tiers (3), unit economics (CAC/LTV/gross margin/payback), full Business Model Canvas (9 blocks)
- **Google APIs**: Firestore
- **Tokens**: ~1.5K in / ~3K out | **Cost**: ~$0.005

#### Agent 4: Financial Model Agent
- **Model**: Gemini 2.5 Pro (numerical reasoning) | **Wave**: 2 | **Latency**: 12-18s
- **Depends on**: `market_research_result`, `business_model_result`
- **Output**: `financial_model_result` — 3-year P&L projections, cost projections with headcount, funding requirements (seed amount, runway, use of funds), key metrics (break-even, margins), Sheets-ready data arrays
- **Google APIs**: Google Sheets API (creates spreadsheet with P&L, Cash Flow, Key Metrics tabs + charts), Firestore
- **Tokens**: ~4K in / ~4K out | **Cost**: ~$0.045

#### Agent 5: Brand Identity Agent
- **Model**: Gemini 2.5 Flash | **Wave**: 1 | **Latency**: 8-12s
- **Input**: `parsed_idea` fields
- **Output**: `brand_identity_result` — company name, tagline, brand voice (tone + personality traits + sample copy), color palette (5 hex codes), typography (heading + body Google Fonts), logo concept (description + SVG code)
- **Google APIs**: Firestore
- **Tokens**: ~1.5K in / ~2.5K out | **Cost**: ~$0.004

#### Agent 6: Pitch Deck Agent
- **Model**: Gemini 2.5 Pro (synthesis of multiple sources) | **Wave**: 3 | **Latency**: 20-30s
- **Depends on**: brand, financials, market, competitive, business model, GTM
- **Output**: `pitch_deck_result` — 10-12 slide content (Title → Problem → Solution → Market → Business Model → Traction → Competition → GTM → Financials → Team → The Ask → Contact), with speaker notes per slide, Google Slides presentation ID
- **Google APIs**: Google Slides API (creates presentation, batch inserts all slides with brand colors/fonts), Google Drive API, Firestore
- **Tokens**: ~8K in / ~6K out | **Cost**: ~$0.070

#### Agent 7: Landing Page Agent
- **Model**: Gemini 2.5 Flash | **Wave**: 2 | **Latency**: 10-15s
- **Depends on**: `brand_identity_result`
- **Output**: `landing_page_result` — complete self-contained HTML file (hero, features, how-it-works, pricing, CTA, footer) with brand colors/fonts, meta tags, responsive design
- **Google APIs**: Firestore
- **Tokens**: ~3K in / ~5K out | **Cost**: ~$0.008

#### Agent 8: Legal Documents Agent
- **Model**: Gemini 2.5 Flash | **Wave**: 2 | **Latency**: 10-15s
- **Depends on**: `brand_identity_result` (company name)
- **Output**: `legal_documents_result` — Terms of Service, Privacy Policy, incorporation checklist with estimated costs, legal disclaimers, Google Docs IDs
- **Google APIs**: Google Docs API (creates 2 documents), Firestore
- **Tokens**: ~2K in / ~5K out | **Cost**: ~$0.008

#### Agent 9: Go-to-Market Strategy Agent
- **Model**: Gemini 2.5 Flash | **Wave**: 2 | **Latency**: 10-15s
- **Depends on**: `market_research_result`, `competitive_analysis_result`
- **Output**: `go_to_market_result` — launch strategy (type + phased timeline), ranked marketing channels with estimated CAC, first 90-day action plan (3 phases), KPIs with 3-month and 12-month targets, potential partnerships
- **Google APIs**: Firestore
- **Tokens**: ~4K in / ~3.5K out | **Cost**: ~$0.006

#### Agent 10: Risk Analysis Agent
- **Model**: Gemini 2.5 Flash | **Wave**: 1 | **Latency**: 8-12s
- **Input**: `parsed_idea` fields
- **Output**: `risk_analysis_result` — risk matrix (category/probability/impact/mitigation), regulatory considerations by jurisdiction, worst-case scenario, 2-3 pivot options
- **Google APIs**: Firestore
- **Tokens**: ~1.5K in / ~2.5K out | **Cost**: ~$0.004

#### Agent 11: Technical Architecture Agent
- **Model**: Gemini 2.5 Flash | **Wave**: 1 | **Latency**: 8-12s
- **Input**: `parsed_idea` fields
- **Output**: `technical_architecture_result` — recommended stack (frontend/backend/database/hosting/services), Mermaid architecture diagram, MVP scope (core features + nice-to-have + dev time + team size), monthly infrastructure cost estimates, security considerations
- **Google APIs**: Firestore
- **Tokens**: ~1.5K in / ~3K out | **Cost**: ~$0.005

#### Agent 12: Executive Summary Agent
- **Model**: Gemini 2.5 Pro (highest quality synthesis) | **Wave**: 3 | **Latency**: 15-20s
- **Depends on**: ALL other agent outputs
- **Output**: `executive_summary_result` — 500-700 word executive summary, one-liner, 30-second elevator pitch, 60-second pitch, key metric highlights, Google Docs ID
- **Google APIs**: Google Docs API, Firestore
- **Tokens**: ~12K in / ~3K out | **Cost**: ~$0.045

### 2.4 Synthesis Layer
The Executive Summary Agent IS the synthesis layer. It receives all 11 prior agent outputs in its instruction context and produces a coherent narrative that weaves together market opportunity, competitive positioning, business model, financials, brand story, and GTM into a single cohesive document. The Pitch Deck Agent serves as a secondary synthesis layer, combining 6+ agent outputs into a visual narrative.

### 2.5 State Management
Three layers:
1. **ADK Session State** (in-memory): Primary data sharing. Each agent writes via `output_key`. Downstream agents read via `{key}` template syntax.
2. **Firestore** (persistent + real-time): After-agent callbacks sync results for frontend dashboard. Structure: `sessions/{id}` (status, agent_status map) + `sessions/{id}/agent_outputs/{agent_name}` (full results).
3. **Google Workspace** (persistent artifacts): Slides/Docs/Sheets created via API. IDs stored in both ADK state and Firestore.

**Company name consistency**: Brand Identity Agent (Wave 1) is the single source of truth. All agents needing a company name are in Wave 2/3.

### 2.6 Real-Time Dashboard
- **Mechanism**: Firestore `onSnapshot` listeners — zero WebSocket infrastructure
- **Frontend listens to**: `sessions/{id}` for agent_status map (12 fields), `sessions/{id}/agent_outputs` subcollection for streaming results
- **Status states**: `pending` (gray) → `running` (blue pulse) → `completed` (green) → `error` (red) → `completed_with_fallback` (yellow)
- **Layout**: 3-row grid organized by wave, with dependency arrows, overall progress bar (X/12), elapsed timer

---

## SECTION 3: GOOGLE API INTEGRATION PLAN

### 3.1 Gemini 2.5 Pro — Orchestrator + Complex Agents
- **Use**: Market Research, Competitive Analysis, Financial Model, Pitch Deck, Executive Summary (5 agents)
- **Why Pro**: These agents require grounded web search, numerical reasoning, or multi-source synthesis
- **Endpoint**: `generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent`
- **Rate limits (paid)**: Up to 30,000 RPM per region
- **Cost**: $1.25/1M input, $10/1M output

### 3.2 Gemini 2.5 Flash — Parallel Specialist Agents
- **Use**: Idea Parser, Business Model, Brand Identity, Landing Page, Legal Docs, GTM, Risk Analysis, Tech Architecture (8 agents)
- **Why Flash over Pro**: 6x cheaper output ($3 vs $10/1M), faster latency, sufficient quality for structured/template output
- **Cost**: $0.50/1M input, $3/1M output

### 3.3 Google ADK — Agent Orchestration
- **Package**: `google-adk` (Python)
- **Key classes**: `LlmAgent`, `ParallelAgent`, `SequentialAgent`, `Runner`, `InMemorySessionService`
- **Tools**: `google_search` (built-in for grounded web search)
- **Session state**: `output_key` for inter-agent data sharing, `{key}` template syntax in instructions

### 3.4 Google Slides API — Pitch Deck Generation
- **Endpoint**: `slides.googleapis.com/v1/presentations`
- **Flow**: `create()` → `batchUpdate()` with `createSlide`, `createShape`, `insertText`, `updateTextStyle`, `updatePageProperties` requests
- **Brand application**: Background colors, text colors, font sizes set via batch update
- **Rate limits**: Per-project quota (adjustable), exponential backoff on 429

### 3.5 Google Docs API — Business Plan & Legal Docs
- **Endpoint**: `docs.googleapis.com/v1/documents`
- **Flow**: `create()` → `batchUpdate()` with `insertText`, `updateParagraphStyle` requests
- **Documents generated**: Terms of Service, Privacy Policy, Executive Summary (3 docs)

### 3.6 Google Sheets API — Financial Model
- **Endpoint**: `sheets.googleapis.com/v4/spreadsheets`
- **Flow**: `create()` (3 tabs: P&L, Cash Flow, Key Metrics) → `values().batchUpdate()` → `batchUpdate()` for charts
- **Rate limits**: 300 reads/min
- **Formulas**: Written as cell values with `USER_ENTERED` input option — Sheets evaluates them

### 3.7 Google Search + ADK Grounding
- **Tool**: ADK built-in `google_search` tool
- **Used by**: Market Research Agent (TAM/SAM data, industry trends), Competitive Analysis Agent (competitor identification, funding data)
- **Grounding**: Results include source URLs, which agents include in their output for citation

### 3.8 Cloud Run — Backend Deployment
- **Config**: 2 vCPU, 1 GiB RAM, timeout 300s, concurrency 80, min-instances 1
- **Cold start mitigation**: min-instances=1 (always warm for demo)
- **Cost**: Free tier covers hackathon; ~$50/month at 1K users/day

### 3.9 Firebase / Firestore
- **Firestore**: Real-time dashboard state, session persistence, agent output storage
- **Firebase Hosting**: Frontend deployment
- **Security rules**: Read/write limited to session owner (by session_id)

### 3.10-3.12 (Secondary APIs)
- **Google Fonts**: Referenced in Brand Identity Agent output — fonts loaded via CSS in Landing Page Agent
- **Maps/BigQuery**: Stretch goals for market geography analysis — not in MVP

---

## SECTION 4: FRONTEND ARCHITECTURE

### 4.1 Tech Stack
| Technology | Purpose | Justification |
|---|---|---|
| React 18 + TypeScript | UI framework | Component model, hooks for state, TypeScript for agent output types |
| Vite | Build tool | Fast HMR, instant dev server, optimal production builds |
| Tailwind CSS v4 | Styling | Rapid iteration, dark mode support, responsive design in minutes |
| Firebase JS SDK | Real-time data | `onSnapshot` listeners for live dashboard — zero WebSocket code |
| Framer Motion | Animations | Agent card status transitions, pulse effects, progress animations |
| Web Speech API | Voice input | Built into Chrome/Edge, zero dependencies, zero cost |

### 4.2 Voice Input UX
- Large pulsing microphone button on dark background
- Real-time transcript display as user speaks (interim results shown in gray, final in white)
- "Stop & Generate" button appears after first words detected
- Fallback: text input field for browsers without Speech API or for typing
- Library: Browser-native `SpeechRecognition` / `webkitSpeechRecognition`

### 4.3 Real-Time Swarm Dashboard
- **Layout**: 3-row grid organized by wave
  - Row 1 (Wave 1): 6 agent cards — Market Research, Competitive Analysis, Business Model, Brand Identity, Risk Analysis, Tech Architecture
  - Row 2 (Wave 2): 4 agent cards — Financial Model, Landing Page, Legal Documents, Go-to-Market
  - Row 3 (Wave 3): 2 agent cards — Pitch Deck, Executive Summary
- **Agent card states**: pending (gray, 50% opacity) → running (blue border, pulse animation) → completed (green border, checkmark) → error (red border, X icon)
- **Visual connections**: Dependency arrows between wave rows
- **Progress**: Top bar showing "7/12 agents complete" with fill animation
- **Timer**: Elapsed seconds counter, prominently displayed

### 4.4 Output Delivery
After completion, a tabbed results view:
1. **Executive Summary** — rendered markdown with key metric callouts
2. **Pitch Deck** — embedded Google Slides `iframe` (editable in Google)
3. **Financial Model** — embedded Google Sheets `iframe` (editable)
4. **Landing Page** — live `iframe` preview of generated HTML
5. **Market Research** — structured cards with TAM/SAM/SOM visualization
6. **Legal Documents** — embedded Google Docs `iframe`
7. **All Others** — expandable accordion sections

### 4.5 Google Drive Export
"Export to Google Drive" button creates a shared folder containing all Slides/Docs/Sheets + landing page HTML + JSON data files. Uses Drive API `files.create` with folder parent.

### 4.6 Mobile
Responsive via Tailwind breakpoints. Agent grid collapses to single column. Voice input works on mobile Chrome. Not a priority for hackathon demo (judges use laptops).

### 4.7 Error States
- Agent failure: Card shows red with "Retrying..." then "Using template" if fallback kicks in
- Full pipeline failure: "Something went wrong. Try again." with retry button
- No mic access: Graceful fallback to text input
- Slow generation: Timer shows elapsed time; no hard timeout visible to user

---

## SECTION 5: BACKEND ARCHITECTURE

### 5.1 FastAPI Server
- **Framework**: FastAPI (async-native, auto-generated OpenAPI docs, Pydantic validation)
- **Endpoints**:
  - `POST /api/generate` — accepts idea text, returns session_id, kicks off pipeline in background
  - `GET /api/session/{id}` — fallback polling endpoint
  - `GET /api/session/{id}/outputs` — fetch all completed agent outputs
  - `POST /api/session/{id}/export` — export to Google Drive

### 5.2 Orchestration Engine
ADK `SequentialAgent` wrapping `ParallelAgent` groups. The `Runner` class drives execution. No custom orchestration code beyond the agent definitions and callbacks.

### 5.3 Parallel Execution
ADK's `ParallelAgent` handles concurrency internally. FastAPI launches the pipeline via `asyncio.create_task()` so the `/generate` endpoint returns immediately with `session_id`.

### 5.4 Agent Communication
Via ADK session state `output_key` mechanism. Each agent writes its result to a named key. Downstream agents read via `{key}` template syntax in instructions. No explicit message passing needed.

### 5.5 Caching
- Idea parsing results cached by transcript hash (avoid re-parsing on retry)
- Google Workspace service objects created once at startup
- No LLM response caching (each idea is unique)

### 5.6 Authentication
- **Hackathon**: No auth (open access for demo)
- **Production**: Google OAuth 2.0, Firestore security rules scoped to user UID

### 5.7 Rate Limiting
- Backend: FastAPI middleware limits to 5 concurrent generations
- Gemini: Paid tier provides 30K RPM — no bottleneck
- Workspace APIs: Exponential backoff on 429s

### 5.8 Logging & Observability
- Structured JSON logging via Python `logging` module
- Each agent logs: start time, end time, token usage, output key, success/failure
- Firestore stores full execution trace per session
- Cloud Run logs visible in Google Cloud Console

### 5.9 Database Schema (Firestore)
```
sessions/{session_id}
  ├── idea_text: string
  ├── status: "pending" | "running" | "completed" | "error"
  ├── created_at: timestamp
  ├── completed_at: timestamp
  ├── agents_completed: number (0-12)
  ├── agents_total: 12
  ├── agent_status: map { agent_name: status_string }
  ├── parsed_idea: map
  ├── company_name: string
  ├── error_message: string
  └── agent_outputs/{agent_name}
      ├── status: string
      ├── result: map (full JSON output)
      ├── completed_at: timestamp
      └── token_usage: { input: number, output: number }

exports/{export_id}
  ├── session_id: string
  ├── drive_folder_id: string
  ├── drive_folder_url: string
  ├── files: [{ name, type, google_id, url }]
  └── created_at: timestamp
```

---

## SECTION 6: COMPLETE FILE & FOLDER STRUCTURE

```
prometheus/
├── README.md                              # Project overview and setup
├── .gitignore                             # Python + Node ignores
├── .env.example                           # Template for environment variables
│
├── backend/
│   ├── main.py                            # FastAPI app, routes, CORS, lifespan
│   ├── pipeline.py                        # ADK Runner integration, pipeline execution
│   ├── config.py                          # Environment vars, constants, model names
│   ├── requirements.txt                   # Python dependencies
│   ├── Dockerfile                         # Cloud Run container image
│   │
│   ├── agents/
│   │   ├── __init__.py                    # Agent registry — exports all agents
│   │   ├── orchestrator.py                # SequentialAgent wrapping ParallelAgents
│   │   ├── idea_parser_agent.py           # Agent 0: transcript → structured idea
│   │   ├── market_research_agent.py       # Agent 1: TAM/SAM/SOM with search
│   │   ├── competitive_analysis_agent.py  # Agent 2: competitors with search
│   │   ├── business_model_agent.py        # Agent 3: revenue model + canvas
│   │   ├── financial_model_agent.py       # Agent 4: 3-year P&L + Sheets
│   │   ├── brand_identity_agent.py        # Agent 5: name, colors, fonts, voice
│   │   ├── pitch_deck_agent.py            # Agent 6: 12-slide deck + Slides
│   │   ├── landing_page_agent.py          # Agent 7: full HTML/CSS page
│   │   ├── legal_documents_agent.py       # Agent 8: ToS + Privacy + Docs
│   │   ├── go_to_market_agent.py          # Agent 9: launch strategy + 90-day plan
│   │   ├── risk_analysis_agent.py         # Agent 10: risk matrix + mitigations
│   │   ├── tech_architecture_agent.py     # Agent 11: tech stack + MVP scope
│   │   └── executive_summary_agent.py     # Agent 12: synthesis of all outputs
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── google_workspace.py            # Slides/Docs/Sheets/Drive API wrappers
│   │   ├── firestore_service.py           # Firestore read/write helpers
│   │   └── export_service.py              # Google Drive folder export
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── request_models.py              # Pydantic request schemas
│   │   ├── response_models.py             # Pydantic response schemas
│   │   └── agent_schemas.py               # JSON schemas + validation per agent
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── slides_tool.py                 # ADK tool wrapper for Slides creation
│   │   ├── sheets_tool.py                 # ADK tool wrapper for Sheets creation
│   │   └── docs_tool.py                   # ADK tool wrapper for Docs creation
│   │
│   └── tests/
│       ├── test_pipeline.py               # End-to-end pipeline test
│       ├── test_agents.py                 # Individual agent output validation
│       └── test_workspace.py              # Workspace API integration tests
│
├── frontend/
│   ├── package.json                       # React dependencies and scripts
│   ├── vite.config.ts                     # Vite config with backend proxy
│   ├── tailwind.config.js                 # Custom dark theme
│   ├── tsconfig.json                      # TypeScript config
│   ├── index.html                         # HTML entry point
│   │
│   ├── public/
│   │   ├── favicon.ico                    # Prometheus flame icon
│   │   └── og-image.png                   # Social preview image
│   │
│   └── src/
│       ├── main.tsx                       # React entry with providers
│       ├── App.tsx                        # Root component with routing
│       ├── index.css                      # Tailwind imports + global styles
│       │
│       ├── lib/
│       │   ├── firebase.ts                # Firebase init + Firestore export
│       │   ├── api.ts                     # Backend API client
│       │   └── constants.ts               # Agent names, display names, waves
│       │
│       ├── hooks/
│       │   ├── useSessionListener.ts      # Firestore real-time listener
│       │   ├── useVoiceInput.ts           # Web Speech API hook
│       │   └── useExport.ts               # Drive export trigger
│       │
│       ├── components/
│       │   ├── VoiceInput.tsx             # Mic button + live transcript
│       │   ├── TextInput.tsx              # Fallback text input
│       │   ├── AgentDashboard.tsx         # 12-agent grid with wave layout
│       │   ├── AgentCard.tsx              # Individual agent status card
│       │   ├── WaveConnector.tsx          # Dependency arrows between waves
│       │   ├── ProgressBar.tsx            # Overall X/12 progress
│       │   ├── ResultsView.tsx            # Tabbed output viewer
│       │   ├── SlidePreview.tsx           # Google Slides embed
│       │   ├── SheetPreview.tsx           # Google Sheets embed
│       │   ├── DocPreview.tsx             # Google Docs embed
│       │   ├── LandingPagePreview.tsx     # iframe of generated page
│       │   ├── ExportButton.tsx           # "Export to Drive" button
│       │   └── Timer.tsx                  # Elapsed time counter
│       │
│       ├── pages/
│       │   ├── HomePage.tsx               # Hero + voice input CTA
│       │   ├── GeneratePage.tsx           # Dashboard during generation
│       │   └── ResultsPage.tsx            # Full results viewer
│       │
│       └── types/
│           ├── agents.ts                  # Agent status/output types
│           └── session.ts                 # Session state types
│
├── infrastructure/
│   ├── cloudbuild.yaml                    # Cloud Build CI/CD
│   ├── firestore.rules                    # Firestore security rules
│   ├── firestore.indexes.json             # Composite indexes
│   └── cors.json                          # Cloud Storage CORS
│
└── scripts/
    ├── setup.sh                           # One-command project setup
    ├── dev.sh                             # Start backend + frontend locally
    └── deploy.sh                          # Deploy to Cloud Run + Firebase Hosting
```

---

## SECTION 7: AGENT PROMPT ENGINEERING

### 7.1 Orchestrator Decomposition Prompt (Idea Parser)
```
You are a startup idea parser. Given a raw voice transcript, extract structured information.
If a field cannot be determined, make a reasonable inference based on context.
Output ONLY valid JSON matching this schema:
{
  "idea_summary": "2-3 sentence clear description",
  "industry": "one of: fintech, healthtech, edtech, saas, ecommerce, marketplace, social, ai_ml, sustainability, logistics, entertainment, other",
  "product_type": "one of: saas, marketplace, mobile_app, hardware, api_service, platform, content, other",
  "target_market": "description of ideal customer",
  "geography": "primary market geography",
  "key_differentiator": "what makes this unique",
  "data_collection": true/false,
  "brand_personality_hints": "any tone/style preferences detected"
}
```

### 7.2 Sample Agent Prompts (abbreviated — full prompts in implementation)

**Market Research Agent:**
```
You are a market research analyst. Using the google_search tool, research the following startup idea and provide data-backed market analysis.

Startup: {parsed_idea}

You MUST use the google_search tool to find real data. Do NOT fabricate statistics.
For each data point, include the source URL.

Output JSON: { tam, sam, som, cagr_percent, industry_trends, target_demographics, market_timing_score, key_sources }
```

**Brand Identity Agent:**
```
You are a brand strategist and visual designer. Create a complete brand identity for:

Idea: {parsed_idea}

Generate a memorable, available-sounding company name (not generic), a punchy tagline,
brand voice with 3-5 personality traits, a 5-color palette (hex codes that work together
on dark and light backgrounds), Google Font pairings, and a simple SVG logo concept.

Output JSON: { company_name, tagline, brand_voice, color_palette, typography, logo_concept }
```

### 7.3 Synthesis Prompt (Executive Summary Agent)
```
You are a senior startup strategist writing a compelling executive summary.
Synthesize ALL of the following agent outputs into a coherent 500-700 word narrative:

Market Research: {market_research_result}
Competitive Analysis: {competitive_analysis_result}
Business Model: {business_model_result}
Financial Model: {financial_model_result}
Brand Identity: {brand_identity_result}
Go-to-Market: {go_to_market_result}
Risk Analysis: {risk_analysis_result}
Technical Architecture: {technical_architecture_result}

Weave these into a single compelling story. Do NOT simply list each section.
Create narrative flow: problem → opportunity → solution → why now → business model → traction path → financials → team needs → the ask.

Output JSON: { executive_summary_text, one_liner, elevator_pitch_30s, elevator_pitch_60s, key_highlights }
```

### 7.4 Prompt Chaining
ADK `output_key` + `{key}` template syntax handles chaining automatically. Wave 2 agents have Wave 1 results injected into their instructions. Wave 3 agents receive all prior outputs.

### 7.5 Hallucination Prevention
- Market Research and Competitive Analysis agents use ADK `google_search` tool for grounded data
- Agent instructions explicitly state: "Do NOT fabricate statistics. Use the search tool."
- Output schemas require `source` fields for data points
- Financial Model agent derives numbers from Market Research data, not invented figures

---

## SECTION 8: HACKATHON DEMO PLAN

### 8.1 Demo Script (5 minutes)
| Time | Action | What the Audience Sees |
|---|---|---|
| 0:00-0:30 | Problem statement | "A founder today spends 200 hours and $15K building what should take minutes..." |
| 0:30-1:00 | Introduce PROMETHEUS | "12 AI agents. Working simultaneously. Full company in under 4 minutes." |
| 1:00-1:15 | Open the app, click microphone | Dark UI with glowing mic button |
| 1:15-1:45 | Speak the idea live | "An AI-powered pet health monitoring collar that tracks vital signs and alerts vets in real-time" |
| 1:45-2:00 | Hit "Generate". Timer starts. | 12 agent cards light up. Wave 1 starts pulsing blue. |
| 2:00-3:00 | LIVE GENERATION | Cards flip to green one by one. Wave 2 triggers. Wave 3 triggers. Real-time progress. |
| 3:00-3:15 | All 12 agents complete | Completion animation. Confetti or glow effect. |
| 3:15-4:00 | Walk through outputs | Tab through: Pitch Deck (open Google Slides), Financial Model (open Sheets with charts), Landing Page (live preview), Legal Docs |
| 4:00-4:30 | Show Google Drive export | "Every document is real, editable, in your Google Drive" |
| 4:30-5:00 | Close | "PROMETHEUS: From idea to company in 75 seconds. 12 agents. One whisper. A full startup." |

### 8.2 The Countdown Moment
Large centered timer counting up from 0:00 with per-wave milestones. When all 12 agents complete, the timer freezes and a "COMPLETE" banner appears. The dramatic moment: watching the timer stay under 2 minutes while the audience realizes 12 complex tasks just ran simultaneously.

### 8.3 Demo Startup Idea
**"An AI-powered pet health monitoring collar that tracks vital signs and alerts vets in real-time"**
- Universally relatable (everyone loves pets)
- Clear market (pet tech is $200B+)
- Visually rich outputs (brand colors, landing page hero, financial charts)
- Not controversial, not niche

### 8.4 Pre-Demo Checklist
- [ ] Cloud Run min-instances=1 (warm)
- [ ] Run one test generation 10 minutes before demo
- [ ] Chrome tab open to app, logged in
- [ ] Microphone tested and working
- [ ] Backup text input ready (pre-typed idea in clipboard)
- [ ] Backup video recording of successful run ready to play
- [ ] WiFi confirmed working, cellular hotspot as backup

### 8.5 Fallback Plan
**If live demo breaks**: "Let me show you a run we completed earlier" → play pre-recorded video of identical flow. Frame it as: "The system ran this 30 minutes ago in 73 seconds — let me walk you through what it produced."

### 8.6 The "Audience Gasps" Moment
When the timer shows ~70 seconds and ALL 12 agent cards are green — then you click the Pitch Deck tab and a fully formatted Google Slides deck appears with brand colors, market data, financial charts, and 12 professional slides. A full company materialized from a whispered sentence.

### 8.7 The Closing Line
"Every founder deserves a team. PROMETHEUS gives you twelve. In one whisper."

---

## SECTION 9: 24-HOUR BUILD SPRINT

### Hours 0-1: Setup & Scaffolding
- Initialize GitHub repo, Python venv, React/Vite project
- Enable Google Cloud APIs (Gemini, Slides, Docs, Sheets, Drive)
- Create service account, download credentials
- Create Firestore database
- Set up `.env` files
- **Verify**: One Gemini call + one Firestore write + one Slides API call
- **Risk**: API enablement can take 5-10 min. Do this first.

### Hours 1-3: Core Agents (Wave 1)
- Implement `config.py`, `idea_parser_agent.py`
- Implement all 6 Wave 1 agents with prompts and output schemas
- Test each agent individually with hardcoded input
- **Deliverable**: Each agent produces valid JSON independently
- **Cut if behind**: Skip quality validation, use raw LLM output

### Hours 3-5: Orchestration + Wave 2-3
- Implement `orchestrator.py` (SequentialAgent + ParallelAgent)
- Implement `pipeline.py` with ADK Runner
- Implement `callbacks.py` for Firestore sync
- Implement Wave 2 agents (Financial Model, Landing Page, Legal, GTM)
- Implement Wave 3 agents (Pitch Deck, Executive Summary)
- **Deliverable**: Full pipeline runs end-to-end from text input to 12 outputs
- **Risk**: ADK parallel execution bugs. Test with 2 agents first, then scale to 6.

### Hours 5-7: Google Workspace Integration
- Implement `google_workspace.py` (Slides, Docs, Sheets creation)
- Wrap as ADK tools in `/backend/tools/`
- Integrate into relevant agents
- **Deliverable**: Generated Slides deck opens correctly in Google Slides
- **Cut if behind**: Skip Sheets charts, skip Docs formatting

### Hours 7-8: FastAPI Server
- Implement `main.py` with all routes
- Implement Pydantic models
- Test with curl
- **Deliverable**: `POST /generate` returns session_id, pipeline runs in background

### Hours 8-10: Frontend — Voice + Basic UI
- Set up Tailwind dark theme
- Implement Firebase config
- Implement VoiceInput, TextInput, HomePage
- Implement API client
- **Deliverable**: Speak idea → see transcript → submit to backend

### Hours 10-13: Frontend — Real-Time Dashboard
- Implement `useSessionListener.ts`
- Implement AgentCard, AgentDashboard, ProgressBar, Timer
- Implement GeneratePage
- **Deliverable**: Submit idea → watch 12 cards animate in real-time
- **THIS IS THE WOW MOMENT — invest extra time here on animations**

### Hours 13-15: Frontend — Results View
- Implement ResultsView with tabs
- Implement Slides/Sheets/Docs embeds
- Implement LandingPagePreview
- Implement ExportButton
- **Deliverable**: Full flow from voice input to viewing all results

### Hours 15-17: Error Handling + Polish
- Retry logic, fallback templates
- Output validation
- Loading/error states in frontend
- **Cut if behind**: Use console.error instead of UI error states

### Hours 17-19: Deployment
- Dockerfile, Cloud Run deploy, Firebase Hosting deploy
- CORS, security rules, environment variables
- **Deliverable**: Production URL works end-to-end
- **Risk**: CORS issues. Test early.

### Hours 19-21: Demo Optimization
- min-instances=1, pre-warm, demo mode
- Polish animations
- Record backup video
- **Deliverable**: 5 successful demo runs in a row

### Hours 21-23: Presentation Prep
- Create project slides
- Practice pitch 3+ times
- Prepare for Q&A

### Hours 23-24: Final Checks
- 3 end-to-end tests with different ideas
- Fix last bugs
- Rest.

---

## SECTION 10: PRODUCTION DEPLOYMENT

### 10.1 Cloud Run
- **Dockerfile**: Python 3.11-slim, pip install, uvicorn
- **Config**: 2 vCPU, 1 GiB RAM, timeout 300s, concurrency 80, min-instances 1, max-instances 5
- **Region**: us-central1

### 10.2 Firebase
- **Firestore**: Session and agent output storage (schema in Section 5.9)
- **Hosting**: Frontend SPA deployment
- **Security rules**: `allow read, write: if request.auth != null` (production); open for hackathon

### 10.3 Environment Variables
```
# Google Cloud
GOOGLE_CLOUD_PROJECT=prometheus-hackathon
GOOGLE_APPLICATION_CREDENTIALS=service-account.json
GEMINI_API_KEY=<key>

# Firebase (frontend)
VITE_FIREBASE_API_KEY=<key>
VITE_FIREBASE_AUTH_DOMAIN=<project>.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=<project>
VITE_FIREBASE_STORAGE_BUCKET=<project>.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=<id>
VITE_FIREBASE_APP_ID=<id>

# Backend
BACKEND_URL=https://prometheus-backend-xxxxx-uc.a.run.app
CORS_ORIGINS=https://<project>.web.app,http://localhost:5173
```

### 10.4 CI/CD
Cloud Build triggered on push to `main` → build Docker image → deploy to Cloud Run → deploy frontend to Firebase Hosting

### 10.5 Monitoring
- Cloud Run metrics: request latency, instance count, error rate
- Custom metric: generation time per session (logged to Firestore)
- Alert: if median generation time > 120s or error rate > 10%

### 10.6 Cost Estimation
| Scale | Gemini | Firestore | Cloud Run | Total/month |
|---|---|---|---|---|
| Hackathon (50 runs) | $14 | $0.05 | Free | ~$15 |
| 100 users/day | $840 | $5 | $20 | ~$865 |
| 1,000 users/day | $8,400 | $50 | $50 | ~$8,500 |
| 10,000 users/day | $84,000 | $500 | $200 | ~$84,700 |

### 10.7 Performance Optimization
- **Bottleneck**: Gemini Pro agents in Wave 1 (~20s). Optimization: Pre-fetch search results in parallel before agents start.
- **Bottleneck**: Pitch Deck Agent (~25s, most complex). Optimization: Split into content generation + Slides API call (parallel).
- **Target**: Sub-60s generation by optimizing prompt length and reducing output token limits.

---

## SECTION 11: TECHNICAL RISKS & MITIGATIONS

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Gemini rate limits hit during demo | Low (paid tier: 30K RPM) | High | Use paid tier, pre-warm |
| Agent produces invalid JSON | Medium | Medium | Regex extraction fallback, retry 2x, then template |
| ADK ParallelAgent bug/race condition | Low | High | Test wave-by-wave before combining; fallback to sequential |
| Google Slides API batch update fails | Low | Medium | Retry with exponential backoff; fallback to markdown output |
| Pipeline takes >4 min | Medium | Medium | Optimize prompts, reduce output tokens, pre-cache search results |
| Agents produce contradictory data | Low | Low | Brand agent = single source for naming; financial agent reads market data |
| WiFi fails during demo | Medium | Critical | Cellular hotspot + pre-recorded video backup |
| Cold start delays on Cloud Run | Low | Medium | min-instances=1 |
| Cost overrun from too many runs | Low | Low | $0.28/run; 1000 runs = $280 |
| Agent hallucinates market data | Medium | Medium | Grounded search required for Market/Competitive agents; source URL validation |

---

## SECTION 12: BUSINESS MODEL & POST-HACKATHON VISION

### 12.1 Pricing
- **Free tier**: 1 generation/month (limited to 6 agents)
- **Pro**: $29/month — unlimited generations, all 12 agents, Google Drive export
- **Teams**: $99/month — collaboration, version history, custom agent prompts
- **Enterprise**: Custom — white-label, custom agents, API access

### 12.2 Target Customers
1. Solo founders (first 1,000 users) — viral, word-of-mouth
2. Startup accelerators (YC, Techstars, 500 Global) — batch onboarding of cohorts
3. University entrepreneurship programs — curriculum integration
4. Corporate innovation teams — rapid ideation validation
5. VCs — portfolio company toolkit

### 12.3 Go-to-Market
- Launch on Product Hunt (optimized for "first AI co-founding team" narrative)
- Free tier drives viral adoption
- Partnership with 2-3 accelerators for cohort licensing
- Content marketing: "We generated a full company for [famous startup idea]" comparisons

### 12.4 Partnerships
- YCombinator / Techstars / 500 Global: Offer PROMETHEUS as a standard tool for batch companies
- Google for Startups: Showcase as ADK + Gemini success story
- Stripe Atlas: Integration with incorporation flow

### 12.5 $1M ARR Path
~2,900 Pro subscribers ($29/mo) or ~850 Teams subscribers ($99/mo). At 5% conversion from free tier, need ~58,000 free users for Pro or ~17,000 for Teams. Achievable in 12-18 months with strong Product Hunt launch + accelerator partnerships.

### 12.6 Competitive Moat
- **Orchestration intelligence**: The dependency graph, wave execution, and inter-agent data sharing are hard to replicate well
- **Prompt portfolio**: 12 deeply tuned agent prompts with quality validation — months of iteration
- **Network effects**: As more startups are generated, we build a dataset of what works, enabling better recommendations
- **Google ecosystem lock-in**: Deep Workspace API integration (Slides/Docs/Sheets) creates switching cost

### 12.7 Acquisition Targets
- **Google**: Showcase for Gemini + ADK capabilities; integrate into Google Workspace
- **Canva**: Expand from design into full business creation
- **Notion**: Add AI-powered startup templates
- **Stripe**: Complement Atlas incorporation with full company generation

---

## SECTION 13: JUDGING CRITERIA ALIGNMENT

### 13.1 Feature-to-Criteria Map
| Feature | Technical Execution (40%) | Innovation (30%) | Impact (20%) | Presentation (10%) |
|---|---|---|---|---|
| 12-agent parallel swarm | Deep ADK + async architecture | First multi-agent startup builder | Democratizes entrepreneurship | Live dashboard is visual spectacle |
| Real-time dashboard | Firestore listeners, Framer Motion | Novel UX for AI systems | Transparency in AI | "Audience gasps" moment |
| Google Workspace output | Slides/Docs/Sheets API integration | Editable real documents | Immediately useful artifacts | Clickable, tangible results |
| Voice input | Web Speech API integration | Natural interaction | Accessible to non-technical | Dramatic demo start |
| Grounded search | ADK google_search tool | Real data, not hallucinations | Trustworthy output | "These are real numbers" |

### 13.2 Most Technically Impressive Because:
12 AI agents running in parallel across 3 dependency waves, sharing state through ADK session management, producing 6 Google Workspace documents, all orchestrated in under 90 seconds — this is a production-grade distributed AI system, not a chatbot wrapper.

### 13.3 Most Commercially Valuable Because:
Replaces $10,000-$45,000 and 200 hours of work with a $0.28 API call. Clear path to $1M ARR with freemium model. 137 million potential users per year globally.

### 13.4 Google AI Showcase Because:
Uses Gemini 2.5 Pro AND Flash (model selection strategy), Google ADK (ParallelAgent, SequentialAgent, output_key, google_search tool), Firestore (real-time listeners), Google Slides API, Google Docs API, Google Sheets API, Google Drive API, Cloud Run, Firebase Hosting — more Google APIs deeply integrated than any other team.

### 13.5 One-Sentence Pitch
"PROMETHEUS turns a whispered startup idea into a complete company — business plan, financial model, pitch deck, landing page, legal docs, and more — in under 4 minutes using 12 AI agents working simultaneously."

### 13.6 30-Second Pitch
"Every founder starts with an idea but needs 200 hours and $15,000 to build the toolkit — the business plan, pitch deck, financial model, legal docs, brand identity, and go-to-market strategy. PROMETHEUS eliminates that entire process. You speak your idea. 12 specialized AI agents — powered by Gemini and Google ADK — fan out in parallel, each an expert in their domain, sharing data and building on each other's work. 75 seconds later, you have a complete, coherent, Google Drive-ready company. Not templates. Not outlines. A full startup toolkit with real market data and editable documents."

### 13.7 3-Minute Pitch Structure
1. **The Pain** (30s): Founder's 200-hour, $15K gauntlet
2. **The Solution** (30s): 12 agents, 3 waves, 75 seconds
3. **Live Demo** (60s): Voice input → watch agents → show outputs
4. **How It Works** (30s): Architecture slide — ADK, waves, Firestore, Workspace APIs
5. **Business Model** (15s): Freemium, $29/mo Pro, accelerator partnerships
6. **Market** (15s): 137M new businesses/year, $4.8B TAM for deck generation alone

---

## SECTION 14: APPENDICES

### 14.1 Tech Stack Table
| Library | Version | Purpose |
|---|---|---|
| Python | 3.11 | Backend runtime |
| FastAPI | 0.115+ | API server |
| uvicorn | 0.30+ | ASGI server |
| google-adk | 1.0+ | Agent orchestration |
| google-genai | 1.0+ | Gemini API client |
| firebase-admin | 6.5+ | Firestore server SDK |
| google-api-python-client | 2.140+ | Workspace APIs |
| pydantic | 2.8+ | Data validation |
| React | 18 | Frontend framework |
| TypeScript | 5.x | Type safety |
| Vite | 5.x | Build tool |
| Tailwind CSS | 4.x | Styling |
| Firebase JS SDK | 10.x | Firestore client |
| Framer Motion | 11.x | Animations |

### 14.2 Google API Documentation URLs
- Gemini API: https://ai.google.dev/gemini-api/docs
- Google ADK: https://google.github.io/adk-docs/
- Slides API: https://developers.google.com/workspace/slides/api
- Docs API: https://developers.google.com/workspace/docs/api
- Sheets API: https://developers.google.com/workspace/sheets/api
- Drive API: https://developers.google.com/drive/api
- Cloud Run: https://cloud.google.com/run/docs
- Firestore: https://firebase.google.com/docs/firestore

### 14.3 Sample .env.example
```
GOOGLE_CLOUD_PROJECT=prometheus-hackathon
GOOGLE_APPLICATION_CREDENTIALS=./service-account.json
GEMINI_API_KEY=your-api-key
VITE_FIREBASE_API_KEY=your-firebase-key
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
BACKEND_URL=http://localhost:8080
CORS_ORIGINS=http://localhost:5173
```

### 14.5 Recommended Team (4-person)
| Role | Responsibilities | Hours Focus |
|---|---|---|
| **Backend Lead** | Agent prompts, ADK orchestration, pipeline | Hours 1-8 |
| **API Integrator** | Workspace APIs, Firestore, Cloud Run deployment | Hours 3-10, 17-19 |
| **Frontend Lead** | React dashboard, voice input, results view, animations | Hours 8-17 |
| **Presenter/PM** | Demo script, pitch, backup video, testing, polish | Hours 15-24 |

### 14.6 Key Metrics to Instrument
- Generation time (total wall-clock)
- Per-agent latency
- Per-agent token usage
- Per-agent success/failure/fallback rate
- Cost per generation
- User conversion (free → paid)
- Output quality score (future: user ratings)

---

## Verification Plan

1. **Unit test each agent**: Hardcode input, verify JSON output parses and matches schema
2. **Integration test pipeline**: Run full 12-agent pipeline with sample idea, verify all outputs present
3. **Workspace API test**: Verify generated Slides, Docs, Sheets open correctly in Google
4. **Frontend E2E test**: Voice input → dashboard animation → results view → Drive export
5. **Performance test**: Time 5 consecutive runs, verify all complete under 120 seconds
6. **Failure test**: Kill one agent mid-run, verify fallback kicks in and pipeline completes
7. **Demo rehearsal**: Run the exact demo script 3+ times, time it, fix any issues

---

## Critical Files for Implementation (Start Here)

1. **`/backend/agents/orchestrator.py`** — The core: SequentialAgent wrapping ParallelAgents, wave management
2. **`/backend/pipeline.py`** — ADK Runner integration, Firestore state sync
3. **`/backend/agents/idea_parser_agent.py`** — First agent to build, validates entire flow
4. **`/backend/services/google_workspace.py`** — Slides/Docs/Sheets API calls
5. **`/frontend/src/hooks/useSessionListener.ts`** — Firestore real-time listener powering the dashboard
6. **`/frontend/src/components/AgentDashboard.tsx`** — The visual centerpiece judges see during demo
