from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from .evidence import NormalizedEvidenceItem

class RationaleCard(BaseModel):
    category: str                      # PAYMENT_BEHAVIOUR, MSME_DISPUTES, MCA_SIGNALS, INSOLVENCY, RELATED_ENTITY
    headline: str
    impact: str                        # POSITIVE, NEGATIVE, NEUTRAL, CAUTION
    evidence_snippet: str
    source: str
    source_url: Optional[str] = None
    confidence: float = 1.0

class CommercialRecommendation(BaseModel):
    buyer_id: int
    buyer_name: str
    evidence_state: str                # SUFFICIENT_EVIDENCE, LIMITED_EVIDENCE, INSUFFICIENT_EVIDENCE, UNRESOLVED_ENTITY
    expected_payment_window: str       # e.g., "65-75 days", "30-35 days", "Uncertain"
    suggested_advance_pct: float       # 0% to 100%
    recommended_credit_days: int       # e.g., 30 days, 15 days, 0 days (Strict Advance)
    late_payment_probability: Optional[float] = None
    expected_delay_days: Optional[float] = None
    prediction_confidence: float
    confidence_tier: str               # HIGH, MEDIUM, LOW, INSUFFICIENT_DATA
    confidence_reason: str
    commercial_tier: str               # PREFERRED_CREDIT, STANDARD_CREDIT, RESTRICTED_CREDIT, SECURED_ADVANCE, CONSERVATIVE_UNVERIFIED
    summary_verdict: str
    why_reasons: List[str]             # Core bullet points
    evidence_cards: List[RationaleCard] = []
    disclaimer: str = "Indicative commercial guidance based strictly on documented public records and verified historical payment behaviour. Does not constitute a financial guarantee."
