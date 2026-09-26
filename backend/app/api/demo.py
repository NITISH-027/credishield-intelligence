from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from ..database.session import get_db
from ..database.models import Buyer
from ..demo_data.seed_buyers import seed_demo_database

router = APIRouter(prefix="/demo", tags=["Demo"])

@router.get("/buyers")
def list_demo_archetypes(db: Session = Depends(get_db)):
    """
    Returns curated 5 demo buyer archetypes with distinct evidence patterns.
    """
    demo_buyers = db.query(Buyer).filter(Buyer.is_demo == True).order_by(Buyer.demo_tag).all()
    results = []
    for b in demo_buyers:
        profile = b.profile
        ins_status = b.insolvency_records[0].status if b.insolvency_records else "NO_PUBLIC_RECORD_FOUND"
        results.append({
            "id": b.id,
            "demo_tag": b.demo_tag,
            "legal_name": b.legal_name,
            "trade_name": b.trade_name,
            "industry": b.industry,
            "state": b.state,
            "demo_scenario": b.demo_scenario,
            "evidence_state": profile.evidence_state if profile else "LIMITED_EVIDENCE",
            "commercial_tier": profile.recommendation_tier if profile else "STANDARD",
            "suggested_advance_pct": profile.suggested_advance_pct if profile else 0.0,
            "recommended_credit_days": profile.recommended_credit_days if profile else 30,
            "expected_payment_window": profile.expected_payment_window if profile else "30-45 days",
            "invoice_count": profile.total_invoices_observed if profile else 0,
            "disputes_count": len(b.disputes),
            "insolvency_status": ins_status,
            "has_related_defaults": any(r.has_insolvency_event for r in b.related_entities)
        })
    return results

@router.post("/reset")
def reset_demo_data(db: Session = Depends(get_db)):
    """
    Resets the database back to clean benchmark seed state.
    """
    seed_demo_database(db)
    return {"status": "success", "message": "Demo data successfully reseeded."}
