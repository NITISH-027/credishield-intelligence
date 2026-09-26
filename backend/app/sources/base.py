from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from ..schemas.evidence import NormalizedEvidenceItem

class BasePublicSourceProvider(ABC):
    """
    Abstract interface for public source data connectors (MSME Samadhaan, MCA21, NCLT/IBBI).
    Enforces standardized evidence item normalization and honest source labeling.
    """
    
    @property
    @abstractmethod
    def source_name(self) -> str:
        """Name of the public data source"""
        pass
        
    @property
    @abstractmethod
    def source_type(self) -> str:
        """Standardized source identifier"""
        pass
        
    @property
    @abstractmethod
    def is_live_connector(self) -> bool:
        """Indicates whether this is a live network connector or a verified benchmark adapter"""
        pass

    @abstractmethod
    def fetch_evidence(self, cin: Optional[str] = None, legal_name: Optional[str] = None, gstin: Optional[str] = None) -> List[NormalizedEvidenceItem]:
        """Fetch and normalize records into standardized evidence items"""
        pass
