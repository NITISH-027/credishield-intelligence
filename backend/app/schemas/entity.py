from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class EntityMatchCandidate(BaseModel):
    id: Optional[int] = None
    legal_name: str
    cin: Optional[str] = None
    gstin: Optional[str] = None
    pan: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    company_status: Optional[str] = None
    match_confidence: float            # 0.0 to 1.0
    match_status: str                  # MATCHED, LIKELY_MATCH, POSSIBLE_MATCH, UNRESOLVED
    match_signals: List[str] = []      # e.g., ["Exact CIN Match", "Name Jaro-Winkler: 0.94", "State: Maharashtra"]
    shared_directors_count: int = 0
    directors: List[Dict[str, Any]] = []

class EntityResolutionResult(BaseModel):
    query: str
    resolved_primary_id: Optional[int] = None
    resolved_primary_name: Optional[str] = None
    resolution_status: str             # MATCHED, LIKELY_MATCH, POSSIBLE_MATCH, UNRESOLVED
    best_candidate: Optional[EntityMatchCandidate] = None
    all_candidates: List[EntityMatchCandidate] = []
    explanation: str

class GraphNode(BaseModel):
    id: str
    label: str
    type: str                          # PRIMARY_BUYER, PARENT_HOLDING, SUBSIDIARY, SISTER_COMPANY, DIRECTOR, HISTORICAL_NAME
    company_status: Optional[str] = "Active"
    cin: Optional[str] = None
    risk_level: str                    # LOW, MEDIUM, HIGH, CRITICAL, NEUTRAL
    has_disputes: bool = False
    has_insolvency: bool = False
    details: Optional[Dict[str, Any]] = None

class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    label: str                         # 100% PARENT, 65% SUBSIDIARY, COMMON_DIRECTOR, FORMER_NAME
    relationship_type: str
    evidence: Optional[str] = None

class EntityGraphResponse(BaseModel):
    buyer_id: int
    primary_entity_name: str
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    total_related_entities: int
    risk_spillover_detected: bool
    summary: str
