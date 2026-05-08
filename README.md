# PROMETHEUS

> **Tagline:** "You whisper a startup idea. 75 seconds later you have a full company."

PROMETHEUS is the operating layer between an idea and a company. A swarm of specialized AI agents — running on Google ADK + Gemini 2.5 Pro/Flash — fans out across three dependency waves to produce a coherent, real-data-grounded, editable company package: brand, business model, market research, competitive analysis, financial model, pitch deck, landing page, legal docs, GTM plan, risk register, technical architecture, and executive summary.

This is the **V2 production rebuild** of the original blueprint. Real-data integrations, validation gates, structured outputs, ownership transfer, payments, persistence, mobile, accessibility, and a streaming UX with in-app deck/landing/financial editors. No demo theater, no fabricated stats, no service-account-owned files.

## Quickstart

```bash
# Backend (Python 3.11+)
cd backend
python -m venv .venv && source .venv/Scripts/activate  # Windows: .venv\Scripts\Activate
pip install -r requirements.txt
cp ../.env.example ../.env  # fill in credentials
uvicorn main:app --reload --port 8080

# Frontend (Node 20+)
cd frontend
npm install
npm run dev  # http://localhost:5173
```

## Repo structure

See `PROMETHEUS_BLUEPRINT_V2.md` for the full architecture and `PROMETHEUS_ROADMAP.md` for the 6-month product plan.

```
backend/   FastAPI gateway + Cloud Tasks worker + 13 ADK agents + 16 services
frontend/  React 18 + Vite + TS + Tailwind v4 + Framer Motion + in-app editors
infrastructure/  Cloud Run, Firestore rules, Cloud Tasks queue, Cloud Armor
scripts/   setup, dev, deploy, test, benchmark, seed
docs/      ARCHITECTURE, SECURITY, DEPLOYMENT, REFERENCE_*
.claude/   Claude Code project config (commands, skills, settings)
```

## Stack

**Backend:** Python 3.11, FastAPI, Pydantic v2, Google ADK, Gemini 2.5 Pro/Flash, Vertex AI Agent Engine, Cloud Tasks, Cloud Run, Firestore, Workload Identity Federation, OpenTelemetry → Cloud Trace.

**Frontend:** React 18 + TypeScript 5, Vite 5, Tailwind CSS v4, Framer Motion 11, Firebase JS SDK, DOMPurify, Tiptap (deck editor), Recharts (financial), cmdk (Cmd-K palette), PostHog.

**Real-data integrations:** USPTO TESS (trademark), Domainr (domain availability), Crunchbase / Statista (market & competitor data), SimilarWeb (traffic proxies), Imagen 3 + Recraft (logo & hero images), Deepgram Nova-2 (cross-browser STT), Termly / iubenda (legal templates), Cloudflare Workers + Registrar (deploy + domain purchase), Stripe (billing).

## License
Proprietary. All rights reserved.
