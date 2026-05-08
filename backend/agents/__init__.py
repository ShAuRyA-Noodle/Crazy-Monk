"""Agent registry. Imports + exposes all 13 agents and the orchestrator."""
from __future__ import annotations

from .articulation_agent import articulation_agent
from .base import PrometheusAgent
from .brand_identity_agent import brand_identity_agent
from .business_model_agent import business_model_agent
from .competitive_analysis_agent import competitive_analysis_agent
from .executive_summary_agent import executive_summary_agent
from .financial_model_agent import financial_model_agent
from .gates import wave_1_gate, wave_2_gate, wave_3_gate
from .go_to_market_agent import go_to_market_agent
from .idea_parser_agent import idea_parser_agent
from .landing_page_agent import landing_page_agent
from .legal_documents_agent import legal_documents_agent
from .market_research_agent import market_research_agent
from .orchestrator import build_orchestrator
from .pitch_deck_agent import pitch_deck_agent
from .risk_analysis_agent import risk_analysis_agent
from .tech_architecture_agent import tech_architecture_agent

__all__ = [
    "PrometheusAgent",
    "articulation_agent",
    "brand_identity_agent",
    "build_orchestrator",
    "business_model_agent",
    "competitive_analysis_agent",
    "executive_summary_agent",
    "financial_model_agent",
    "go_to_market_agent",
    "idea_parser_agent",
    "landing_page_agent",
    "legal_documents_agent",
    "market_research_agent",
    "pitch_deck_agent",
    "risk_analysis_agent",
    "tech_architecture_agent",
    "wave_1_gate",
    "wave_2_gate",
    "wave_3_gate",
]
