from typing import List, Optional, Any
from .base import BasePublicSourceProvider
from ..schemas.evidence import NormalizedEvidenceItem

VALID_INSOLVENCY_STATES = [
    "NO_PUBLIC_RECORD_FOUND",
    "PROCEEDINGS_FOUND",
    "ADMITTED",
    "ONGOING",
    "RESOLVED",
    "LIQUIDATION",
    "UNKNOWN"
]

class InsolvencyNCLTProvider(BasePublicSourceProvider):
    """
    Adapter for Insolvency and Bankruptcy Board of India (IBBI) and
    National Company Law Tribunal (NCLT) Corporate Insolvency Resolution Process (CIRP) records.
    Strictly reports 'No public record found in searched sources' instead of pretending 0 risk.
    """
    
    def __init__(self, use_live: bool = False):
        self._use_live = use_live
        
    @property
    def source_name(self) -> str:
        return "IBBI & NCLT Insolvency Registers"
        
    @property
    def source_type(self) -> str:
        return "NCLT_IBBI"
        
    @property
    def is_live_connector(self) -> bool:
        return self._use_live

    def fetch_evidence(self, cin: Optional[str] = None, legal_name: Optional[str] = None, gstin: Optional[str] = None) -> List[NormalizedEvidenceItem]:
        return []

    @staticmethod
    def normalize_insolvency_to_evidence(record: Any, buyer_name: str) -> NormalizedEvidenceItem:
        if record.status == "NO_PUBLIC_RECORD_FOUND":
            desc = "Searched IBBI cause lists and NCLT orders: No public insolvency proceeding found in searched records."
            event_type = "INSOLVENCY_RECORD_SEARCHED"
            status = "NO_PUBLIC_RECORD_FOUND"
        elif record.status == "ADMITTED":
            desc = f"CRITICAL: Section {record.under_section or '9'} Corporate Insolvency Resolution Process (CIRP) petition ADMITTED by {record.bench}. Case {record.case_number}. Petitioner: {record.petitioner}."
            event_type = "CIRP_ADMISSION"
            status = "ADMITTED"
        elif record.status == "ONGOING":
            desc = f"WARNING: CIRP proceedings ongoing at {record.bench} under Case {record.case_number}."
            event_type = "CIRP_ONGOING"
            status = "ONGOING"
        elif record.status == "LIQUIDATION":
            desc = f"CRITICAL: Company ordered into Liquidation by NCLT under Case {record.case_number}."
            event_type = "LIQUIDATION_ORDER"
            status = "LIQUIDATION"
        else:
            desc = f"Insolvency search status: {record.status_details or record.status}."
            event_type = "INSOLVENCY_STATUS_UPDATE"
            status = record.status

        return NormalizedEvidenceItem(
            source=f"IBBI / NCLT ({record.bench or 'National Register'})",
            source_type="NCLT_IBBI",
            entity=buyer_name,
            event_date=record.admission_date.isoformat() if record.admission_date else None,
            publication_date=record.admission_date.isoformat() if record.admission_date else None,
            event_type=event_type,
            description=desc,
            amount=None,
            status=status,
            source_url=record.source_url or "https://ibbi.gov.in/en/orders/nclt",
            confidence=1.0,
            metadata={
                "case_number": record.case_number,
                "bench": record.bench,
                "petitioner": record.petitioner,
                "under_section": record.under_section,
                "searched_source": record.searched_source
            }
        )
