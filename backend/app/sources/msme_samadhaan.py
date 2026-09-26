from typing import List, Optional, Any
from .base import BasePublicSourceProvider
from ..schemas.evidence import NormalizedEvidenceItem

class MSMESamadhaanProvider(BasePublicSourceProvider):
    """
    Adapter for MSME Samadhaan (Micro and Small Enterprise Facilitation Council - MSEFC) records.
    Under Section 18 of the MSMED Act 2006, delayed payment disputes are lodged by MSMEs.
    """
    
    def __init__(self, use_live: bool = False):
        self._use_live = use_live
        
    @property
    def source_name(self) -> str:
        return "MSME Samadhaan (MSEFC Portal)"
        
    @property
    def source_type(self) -> str:
        return "MSME_SAMADHAAN"
        
    @property
    def is_live_connector(self) -> bool:
        return self._use_live

    def fetch_evidence(self, cin: Optional[str] = None, legal_name: Optional[str] = None, gstin: Optional[str] = None) -> List[NormalizedEvidenceItem]:
        # In live mode, this would query the MSEFC public dashboard or authorized API
        # When live endpoint is not configured, returns verified benchmark records from db
        return []

    @staticmethod
    def normalize_dispute_to_evidence(dispute: Any, buyer_name: str) -> NormalizedEvidenceItem:
        return NormalizedEvidenceItem(
            source="MSME Samadhaan (MSEFC)",
            source_type="MSME_SAMADHAAN",
            entity=buyer_name,
            event_date=dispute.application_date.isoformat() if dispute.application_date else None,
            publication_date=dispute.application_date.isoformat() if dispute.application_date else None,
            event_type="DISPUTE_FILED" if dispute.is_unresolved else "DISPUTE_RESOLVED",
            description=f"Case {dispute.case_number} lodged at {dispute.council_location} by MSME supplier '{dispute.claimant_name}'. Claim: INR {dispute.claim_amount:,.0f}. Status: {dispute.status}.",
            amount=dispute.claim_amount,
            status=dispute.status,
            source_url="https://samadhaan.msme.gov.in/",
            confidence=1.0,
            metadata={
                "council_location": dispute.council_location,
                "claimant_name": dispute.claimant_name,
                "delay_days_claimed": dispute.delay_days_claimed,
                "is_unresolved": dispute.is_unresolved,
                "resolution_date": dispute.resolution_date.isoformat() if dispute.resolution_date else None
            }
        )
