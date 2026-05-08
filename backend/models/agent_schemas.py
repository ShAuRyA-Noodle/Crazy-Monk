"""Agent output schemas — single source of truth.

Every agent's `response_schema` is derived from these Pydantic models.
Downstream agents read upstream outputs typed against these classes.
NEVER allow free-form JSON to flow between agents.
"""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, HttpUrl, field_validator

# ─── Pre-Wave ────────────────────────────────────────────────────────────────


class ParsedIdea(BaseModel):
    """Output of Idea Parser (Agent 0)."""

    idea_summary: str = Field(..., min_length=20, max_length=500)
    industry: Literal[
        "fintech", "healthtech", "edtech", "saas", "ecommerce", "marketplace",
        "social", "ai_ml", "sustainability", "logistics", "entertainment",
        "consumer_hardware", "developer_tools", "enterprise_saas", "other",
    ]
    product_type: Literal[
        "saas", "marketplace", "mobile_app", "hardware", "api_service",
        "platform", "content", "physical_product", "service", "other",
    ]
    target_market: str = Field(..., min_length=5, max_length=300)
    geography: str = Field(default="Global")
    key_differentiator: str = Field(..., min_length=5, max_length=400)
    data_collection: bool = False
    regulated_data: bool = False
    brand_personality_hints: str = Field(default="", max_length=300)
    moderation_flags: list[str] = Field(default_factory=list)


class ArticulationOutput(BaseModel):
    """Output of Articulation Agent — pre-step polish."""

    polished_idea: str = Field(..., min_length=20, max_length=600)
    clarifying_questions: list[str] = Field(default_factory=list, max_length=3)
    assumptions: list[str] = Field(default_factory=list, max_length=5)
    confidence: float = Field(..., ge=0.0, le=1.0)


# ─── Citation primitive ──────────────────────────────────────────────────────


class Citation(BaseModel):
    text: str
    source_url: HttpUrl
    publisher: str | None = None
    accessed_at: str | None = None


class DataPoint(BaseModel):
    """Surface every numeric claim with provenance."""

    label: str
    value: float | str
    unit: str | None = None
    confidence: Literal["sourced", "derived", "estimated", "inferred"]
    source: Citation | None = None
    derivation: str | None = None  # if confidence == "derived"


# ─── Wave 1 ──────────────────────────────────────────────────────────────────


class MarketResearchResult(BaseModel):
    tam: DataPoint
    sam: DataPoint
    som: DataPoint
    cagr: DataPoint
    industry_trends: list[str] = Field(..., min_length=3, max_length=7)
    target_demographics: list[str] = Field(..., min_length=2, max_length=6)
    market_timing_score: float = Field(..., ge=0.0, le=10.0)
    market_timing_rationale: str
    sources: list[Citation] = Field(..., min_length=3)


class CompetitorEntry(BaseModel):
    name: str
    url: HttpUrl | None = None
    description: str
    funding: DataPoint | None = None
    revenue: DataPoint | None = None
    employee_count: DataPoint | None = None
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    data_disclosed: bool = True


class CompetitiveAnalysisResult(BaseModel):
    competitors: list[CompetitorEntry] = Field(..., min_length=3, max_length=10)
    feature_matrix: dict[str, dict[str, bool | str]]
    positioning_gaps: list[str] = Field(..., min_length=2)
    market_concentration: Literal["fragmented", "moderate", "concentrated", "monopolized"]
    sources: list[Citation] = Field(..., min_length=3)


class PricingTier(BaseModel):
    name: str
    price_usd_monthly: float
    features: list[str]
    target_segment: str


class UnitEconomics(BaseModel):
    cac_usd: DataPoint
    ltv_usd: DataPoint
    gross_margin_pct: DataPoint
    payback_months: DataPoint
    ltv_cac_ratio: float


class BusinessModelResult(BaseModel):
    revenue_model: str
    pricing_tiers: list[PricingTier] = Field(..., min_length=2, max_length=4)
    unit_economics: UnitEconomics
    business_model_canvas: dict[str, list[str]]  # 9 standard blocks
    primary_revenue_stream: str


class ColorEntry(BaseModel):
    name: str
    hex: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")
    role: Literal["primary", "secondary", "accent", "neutral_dark", "neutral_light", "background", "text"]
    contrast_on_white: float | None = None
    contrast_on_black: float | None = None
    wcag_aa_normal: bool | None = None


class Typography(BaseModel):
    heading_font: str
    body_font: str
    heading_google_font_url: HttpUrl | None = None
    body_google_font_url: HttpUrl | None = None


class NameCandidate(BaseModel):
    name: str
    rationale: str
    domain_com_available: bool | None = None
    uspto_conflicts: list[str] = Field(default_factory=list)
    handle_x_available: bool | None = None
    handle_instagram_available: bool | None = None


class BrandIdentityResult(BaseModel):
    company_name: str
    name_alternatives: list[NameCandidate] = Field(default_factory=list, max_length=5)
    tagline: str = Field(..., max_length=120)
    brand_voice_traits: list[str] = Field(..., min_length=3, max_length=5)
    brand_voice_sample_copy: str
    color_palette: list[ColorEntry] = Field(..., min_length=3, max_length=5)
    typography: Typography
    logo_concept_description: str
    logo_image_url: HttpUrl | None = None  # Imagen output
    logo_svg_sanitized: str | None = None  # bleach/nh3 sanitized
    industry_keywords: list[str] = Field(default_factory=list, max_length=10)


class RiskEntry(BaseModel):
    category: Literal["market", "execution", "regulatory", "technical", "financial", "team", "ip", "macro"]
    description: str
    probability: Literal["low", "medium", "high"]
    impact: Literal["low", "medium", "high"]
    mitigation: str


class RiskAnalysisResult(BaseModel):
    risk_matrix: list[RiskEntry] = Field(..., min_length=5, max_length=12)
    regulatory_considerations: dict[str, list[str]]  # by jurisdiction
    worst_case_scenario: str
    pivot_options: list[str] = Field(..., min_length=2, max_length=4)


class TechArchitectureResult(BaseModel):
    recommended_stack: dict[str, str]  # frontend / backend / db / hosting / etc.
    architecture_diagram_mermaid: str
    mvp_core_features: list[str] = Field(..., min_length=3)
    mvp_nice_to_have: list[str] = Field(default_factory=list)
    estimated_dev_weeks: int = Field(..., ge=1, le=104)
    estimated_team_size: int = Field(..., ge=1, le=20)
    monthly_infra_cost_usd_estimate: DataPoint
    security_considerations: list[str] = Field(..., min_length=3)


# ─── Wave 2 ──────────────────────────────────────────────────────────────────


class FinancialProjectionRow(BaseModel):
    year: int
    revenue_usd: float
    cogs_usd: float
    gross_profit_usd: float
    opex_usd: float
    ebitda_usd: float
    headcount: int
    cash_usd: float


class FinancialModelResult(BaseModel):
    """Generated by deterministic Python finance engine (services/finance_engine.py),
    NOT by raw Gemini. Gemini supplies *assumptions only*."""

    assumptions: dict[str, Any]
    projections: list[FinancialProjectionRow] = Field(..., min_length=3, max_length=5)
    funding_seed_usd: float
    runway_months: float
    breakeven_month: int | None
    key_metrics: dict[str, float]
    sheets_id: str | None = None
    sheets_url: HttpUrl | None = None
    reconciliation_passed: bool


class LandingPageResult(BaseModel):
    """HTML is sanitized server-side. CSP injected. Iframe-rendered with sandbox."""

    html_sanitized: str
    css: str
    title: str
    meta_description: str
    og_tags: dict[str, str]
    hero_image_url: HttpUrl | None = None  # Imagen
    feature_image_urls: list[HttpUrl] = Field(default_factory=list)
    deploy_url: HttpUrl | None = None  # set after Cloudflare deploy
    custom_domain: str | None = None
    layouts_alternative: list[str] = Field(default_factory=list, max_length=2)


class LegalDocumentsResult(BaseModel):
    """Generated via Termly/iubenda template-fill, NEVER raw LLM."""

    tos_template_id: str
    tos_doc_id: str | None = None
    tos_doc_url: HttpUrl | None = None
    privacy_template_id: str
    privacy_doc_id: str | None = None
    privacy_doc_url: HttpUrl | None = None
    incorporation_checklist: list[dict[str, str]]
    jurisdictions_covered: list[str]
    lawyer_review_cta: bool = True


class GoToMarketResult(BaseModel):
    launch_strategy_type: Literal["soft_launch", "product_hunt", "press", "community_first", "founder_led"]
    launch_phases: list[dict[str, str]]  # phase / week range / actions
    marketing_channels: list[dict[str, Any]]  # channel / cac_estimate / priority
    first_90_days_plan: dict[str, list[str]]  # weeks 1-4, 5-8, 9-12
    kpis: dict[str, dict[str, float]]  # metric -> {3mo, 12mo}
    partnerships: list[str] = Field(default_factory=list)


# ─── Wave 3 ──────────────────────────────────────────────────────────────────


class PitchSlide(BaseModel):
    slide_number: int
    layout: Literal[
        "title", "problem", "solution", "market", "business_model", "traction",
        "competition", "gtm", "financials", "team", "ask", "contact",
    ]
    title: str
    body: str
    speaker_notes: str
    image_url: HttpUrl | None = None


class PitchDeckResult(BaseModel):
    slides: list[PitchSlide] = Field(..., min_length=10, max_length=14)
    presentation_id: str | None = None
    presentation_url: HttpUrl | None = None
    pdf_url: HttpUrl | None = None


class ExecutiveSummaryResult(BaseModel):
    summary_text: str = Field(..., min_length=400, max_length=900)
    one_liner: str = Field(..., max_length=160)
    elevator_pitch_30s: str
    elevator_pitch_60s: str
    key_highlights: list[str] = Field(..., min_length=3, max_length=6)
    coherence_score: float = Field(..., ge=0.0, le=1.0)
    doc_id: str | None = None
    doc_url: HttpUrl | None = None

    @field_validator("summary_text")
    @classmethod
    def word_count(cls, v: str) -> str:
        words = len(v.split())
        if not 90 <= words <= 800:
            raise ValueError(f"summary_text must be 90-800 words, got {words}")
        return v


# ─── Status alias re-export ──────────────────────────────────────────────────

from .session_models import AgentStatusValue as AgentStatus  # noqa: E402

__all__ = [
    "AgentStatus",
    "ArticulationOutput",
    "BrandIdentityResult",
    "BusinessModelResult",
    "Citation",
    "ColorEntry",
    "CompetitiveAnalysisResult",
    "CompetitorEntry",
    "DataPoint",
    "ExecutiveSummaryResult",
    "FinancialModelResult",
    "FinancialProjectionRow",
    "GoToMarketResult",
    "LandingPageResult",
    "LegalDocumentsResult",
    "MarketResearchResult",
    "NameCandidate",
    "ParsedIdea",
    "PitchDeckResult",
    "PitchSlide",
    "PricingTier",
    "RiskAnalysisResult",
    "RiskEntry",
    "TechArchitectureResult",
    "Typography",
    "UnitEconomics",
]
