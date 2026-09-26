from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import date, datetime
from .entity import EntityMatchCandidate, GraphNode, GraphEdge
from .payment import PaymentBehaviourAnalytics, TransactionItem
from .recommendation import CommercialRecommendation
from .evidence import NormalizedEvidenceItem, TimelineEvent

class DirectorItem(BaseModel):
    din: Optional[str] = None
    name: str
    designation: Optional[str] = "Director"
    appointment_date: Optional[str] = None

class BuyerSummary(BaseModel):
    id: int
    legal_name: str
    trade_name: Optional[str] = None
    cin: Optional[str] = None
    gstin: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    industry: Optional[str] = None
    company_status: Optional[str] = "Active"
    is_demo: bool = False
    demo_tag: Optional[str] = None
    evidence_state: Optional[str] = "LIMITED_EVIDENCE"
    late_payment_prob: Optional[float] = None
    expected_delay_days: Optional[float] = None
    total_disputes: int = 0
    insolvency_status: str = "NO_PUBLIC_RECORD_FOUND"

class BuyerDetail(BaseModel):
    id: int
    legal_name: str
    trade_name: Optional[str] = None
    cin: Optional[str] = None
    gstin: Optional[str] = None
    pan: Optional[str] = None
    registered_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    incorporation_date: Optional[str] = None
    company_status: Optional[str] = "Active"
    company_class: Optional[str] = None
    industry: Optional[str] = None
    authorized_capital: Optional[float] = None
    paid_up_capital: Optional[float] = None
    directors: List[DirectorItem] = []
    promoters: List[str] = []
    previous_names: List[str] = []
    is_demo: bool = False
    demo_tag: Optional[str] = None
    demo_scenario: Optional[str] = None
    
    # Aggregated Sub-Engines
    payment_analytics: Optional[PaymentBehaviourAnalytics] = None
    commercial_recommendation: Optional[CommercialRecommendation] = None
    disputes_count: int = 0
    unresolved_disputes_count: int = 0
    total_dispute_amount: float = 0.0
    filing_signals_count: int = 0
    auditor_qualification_present: bool = False
    going_concern_warning_present: bool = False
    insolvency_status: str = "NO_PUBLIC_RECORD_FOUND"
    related_entities_count: int = 0
    evidence_state: str = "LIMITED_EVIDENCE"
    last_verified: str = "Live verification completed"
