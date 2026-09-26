from typing import List, Dict, Any
from ..schemas.entity import GraphNode, GraphEdge, EntityGraphResponse

def build_entity_graph(buyer: Any, related_links: List[Any]) -> EntityGraphResponse:
    """
    Constructs an interactive ownership & group relationship graph.
    Surfaces holding companies, subsidiaries, common director entities,
    historical names, and cross-entity risk spillovers.
    """
    nodes: List[GraphNode] = []
    edges: List[GraphEdge] = []
    
    # Primary Node
    primary_node_id = f"buyer_{buyer.id}"
    primary_risk = "LOW"
    if buyer.profile:
        if buyer.profile.evidence_state == "INSUFFICIENT_EVIDENCE":
            primary_risk = "NEUTRAL"
        elif buyer.profile.late_payment_prob and buyer.profile.late_payment_prob > 0.65:
            primary_risk = "HIGH"
        elif buyer.profile.late_payment_prob and buyer.profile.late_payment_prob > 0.35:
            primary_risk = "MEDIUM"
            
    nodes.append(GraphNode(
        id=primary_node_id,
        label=buyer.legal_name,
        type="PRIMARY_BUYER",
        company_status=buyer.company_status or "Active",
        cin=buyer.cin,
        risk_level=primary_risk,
        has_disputes=len(buyer.disputes) > 0,
        has_insolvency=any(r.status not in ("NO_PUBLIC_RECORD_FOUND", "UNKNOWN") for r in buyer.insolvency_records),
        details={
            "cin": buyer.cin,
            "gstin": buyer.gstin,
            "state": buyer.state,
            "status": buyer.company_status,
            "role": "Subject Company"
        }
    ))
    
    # Previous Names Nodes
    for idx, prev_name in enumerate(buyer.previous_names or []):
        prev_node_id = f"prev_{buyer.id}_{idx}"
        nodes.append(GraphNode(
            id=prev_node_id,
            label=prev_name,
            type="HISTORICAL_NAME",
            company_status="Former Legal Name",
            risk_level="NEUTRAL",
            details={"description": "Company previously registered under this corporate name"}
        ))
        edges.append(GraphEdge(
            id=f"edge_prev_{idx}",
            source=primary_node_id,
            target=prev_node_id,
            label="FORMER_NAME",
            relationship_type="HISTORICAL_RENAME",
            evidence="ROC filing change of name certificate"
        ))
        
    risk_spillover = False
    
    # Related Entities Links
    for link in related_links:
        rel_node_id = f"rel_{link.id}"
        node_risk = "CRITICAL" if link.has_insolvency_event else ("HIGH" if link.has_known_disputes else "LOW")
        if link.has_insolvency_event or link.has_known_disputes:
            risk_spillover = True
            
        nodes.append(GraphNode(
            id=rel_node_id,
            label=link.related_entity_name,
            type=link.relationship_type,
            company_status="Active" if not link.has_insolvency_event else "Under CIRP / Default",
            cin=link.related_cin,
            risk_level=node_risk,
            has_disputes=link.has_known_disputes,
            has_insolvency=link.has_insolvency_event,
            details={
                "relationship": link.relationship_type,
                "shared_directors": link.shared_directors,
                "ownership_percentage": f"{link.ownership_percentage}%" if link.ownership_percentage else "Common Control",
                "evidence": link.evidence_notes
            }
        ))
        
        edges.append(GraphEdge(
            id=f"edge_rel_{link.id}",
            source=primary_node_id,
            target=rel_node_id,
            label=link.relationship_type.replace("_", " "),
            relationship_type=link.relationship_type,
            evidence=link.evidence_notes
        ))
        
    summary = f"Identified {len(related_links)} connected corporate entities across ownership and directorship linkages."
    if risk_spillover:
        summary += " WARNING: Cross-entity defaults or insolvency events detected in related group companies."
        
    return EntityGraphResponse(
        buyer_id=buyer.id,
        primary_entity_name=buyer.legal_name,
        nodes=nodes,
        edges=edges,
        total_related_entities=len(related_links),
        risk_spillover_detected=risk_spillover,
        summary=summary
    )
