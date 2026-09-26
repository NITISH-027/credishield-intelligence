from typing import List, Optional, Any
from .base import BasePublicSourceProvider
from ..schemas.evidence import NormalizedEvidenceItem

class MCAFilingsProvider(BasePublicSourceProvider):
    """
    Adapter for Ministry of Corporate Affairs (MCA21 / ROC) statutory filings.
    Extracts financial distress signals, auditor qualifications, going concern doubts,
    negative net worth flags, and active charge registrations.
    """
    
    def __init__(self, use_live: bool = False):
        self._use_live = use_live
        
    @property
    def source_name(self) -> str:
        return "Ministry of Corporate Affairs (MCA21 / ROC)"
        
    @property
    def source_type(self) -> str:
        return "MCA21_FILING"
        
    @property
    def is_live_connector(self) -> bool:
        return self._use_live

    def fetch_evidence(self, cin: Optional[str] = None, legal_name: Optional[str] = None, gstin: Optional[str] = None) -> List[NormalizedEvidenceItem]:
        return []

    @staticmethod
    def normalize_filing_to_evidence(signal: Any, buyer_name: str) -> NormalizedEvidenceItem:
        event_type = "STATUTORY_FILING"
        desc_parts = [f"Filing {signal.form_type} for {signal.financial_year}."]
        
        if signal.revenue_inr_cr is not None:
            desc_parts.append(f"Revenue: INR {signal.revenue_inr_cr} Cr.")
        if signal.net_profit_inr_cr is not None:
            desc_parts.append(f"Net Profit: INR {signal.net_profit_inr_cr} Cr.")
            
        if signal.going_concern_warning:
            event_type = "GOING_CONCERN_WARNING"
            desc_parts.append("WARNING: Statutory Auditor emphasized material uncertainty regarding Going Concern.")
        elif signal.auditor_qualification_flag:
            event_type = "AUDITOR_QUALIFICATION"
            desc_parts.append(f"Auditor Note: {signal.auditor_notes}")
            
        if signal.negative_net_worth_flag:
            desc_parts.append("CRITICAL: Negative Net Worth flagged in annual balance sheet.")
            
        if signal.active_charges_count > 0:
            desc_parts.append(f"Active registered bank/lender charges: {signal.active_charges_count}.")

        return NormalizedEvidenceItem(
            source=f"MCA21 Portal (Form {signal.form_type})",
            source_type="MCA21_FILING",
            entity=buyer_name,
            event_date=signal.filing_date.isoformat() if signal.filing_date else None,
            publication_date=signal.filing_date.isoformat() if signal.filing_date else None,
            event_type=event_type,
            description=" ".join(desc_parts),
            amount=signal.revenue_inr_cr,
            status="FILED_WITH_ROC",
            source_url="https://www.mca.gov.in/content/mcaformsearch/portal/mca/mcaportal/viewCompanyMasterData.html",
            confidence=1.0,
            document_ref=signal.document_reference,
            metadata={
                "financial_year": signal.financial_year,
                "form_type": signal.form_type,
                "auditor_qualification": signal.auditor_qualification_flag,
                "going_concern_warning": signal.going_concern_warning,
                "negative_net_worth": signal.negative_net_worth_flag,
                "snippet": signal.snippet
            }
        )
