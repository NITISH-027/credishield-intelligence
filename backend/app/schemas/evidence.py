from typing import Optional, Any
from pydantic import BaseModel
from datetime import date, datetime

class NormalizedEvidenceItem(BaseModel):
    source: str
    source_type: str                   # MSME_SAMADHAAN, MCA21_FILING, NCLT_IBBI, INVOICE_HISTORY, CORPORATE_REGISTRY
    entity: str
    event_date: Optional[str] = None
    publication_date: Optional[str] = None
    event_type: str                    # DISPUTE_FILED, SETTLEMENT_ORDER, AUDITOR_QUALIFICATION, REVENUE_DROP, CIRP_ADMISSION, INVOICE_DELAY, DIRECTOR_CHANGE
    description: str
    amount: Optional[float] = None
    status: str
    source_url: Optional[str] = None
    confidence: float = 1.0
    document_ref: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None

class TimelineEvent(BaseModel):
    id: str
    year: int
    date: str
    category: str                      # DISPUTE, FILING, INSOLVENCY, INCORPORATION, PAYMENT_TREND
    title: str
    description: str
    severity: str                      # LOW, MEDIUM, HIGH, CRITICAL, INFO
    entity_name: str
    source: str
    amount: Optional[float] = None
    status: Optional[str] = None
    source_url: Optional[str] = None
    confidence: float = 1.0
