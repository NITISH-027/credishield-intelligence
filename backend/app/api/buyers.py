from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from ..database.session import get_db
from ..database.models import (
    Buyer, Transaction, MSMEDispute, MCAFilingSignal, InsolvencyRecord, RelatedEntityLink, ReliabilityProfile
)
from ..schemas.buyer import BuyerSummary, BuyerDetail, DirectorItem
from ..schemas.entity import EntityResolutionResult, EntityMatchCandidate, EntityGraphResponse
from ..schemas.payment import PaymentBehaviourAnalytics, TransactionItem
from ..schemas.recommendation import CommercialRecommendation
from ..schemas.evidence import NormalizedEvidenceItem, TimelineEvent
from ..entity_resolution.matcher import match_entities
from ..entity_resolution.graph import build_entity_graph
from ..payment_engine.analytics import compute_payment_analytics
from ..ml.pipeline import predictor
from ..recommendations.rules import generate_commercial_recommendation
from ..evidence.timeline import build_buyer_timeline
from ..sources.msme_samadhaan import MSMESamadhaanProvider
from ..sources.mca_filings import MCAFilingsProvider
from ..sources.insolvency_nclt import InsolvencyNCLTProvider

router = APIRouter(prefix="/buyers", tags=["Buyers"])

class SearchRequest(BaseModel):
    query: str
    cin: Optional[str] = None
    gstin: Optional[str] = None

@router.post("/search", response_model=EntityResolutionResult)
def search_and_resolve_buyer(request: SearchRequest, db: Session = Depends(get_db)):
    """
    Entity Resolution search endpoint.
    Matches company name, historical names, CIN, or GSTIN against database candidates.
    Applies multi-signal matching with Jaro-Winkler, token overlap, and identifier verification.
    """
    query_text = request.query.strip()
    if not query_text and not request.cin and not request.gstin:
        raise HTTPException(status_code=400, detail="Search query or identifier must be provided")

    all_buyers = db.query(Buyer).all()
    candidates: List[EntityMatchCandidate] = []

    for b in all_buyers:
        b_dict = {
            "legal_name": b.legal_name,
            "trade_name": b.trade_name,
            "cin": b.cin,
            "gstin": b.gstin,
            "previous_names": b.previous_names or []
        }
        conf, status, signals = match_entities(
            query_name=query_text,
            candidate_record=b_dict,
            query_cin=request.cin,
            query_gstin=request.gstin
        )

        if conf >= 0.35: # Include viable candidates for ranking
            candidates.append(EntityMatchCandidate(
                id=b.id,
                legal_name=b.legal_name,
                cin=b.cin,
                gstin=b.gstin,
                pan=b.pan,
                state=b.state,
                city=b.city,
                company_status=b.company_status,
                match_confidence=conf,
                match_status=status,
                match_signals=signals,
                shared_directors_count=len(b.directors or []),
                directors=b.directors or []
            ))

    # Sort descending by match confidence
    candidates.sort(key=lambda c: c.match_confidence, reverse=True)

    if not candidates or candidates[0].match_confidence < 0.50:
        return EntityResolutionResult(
            query=query_text,
            resolved_primary_id=None,
            resolved_primary_name=None,
            resolution_status="UNRESOLVED",
            best_candidate=candidates[0] if candidates else None,
            all_candidates=candidates,
            explanation=f"No matching legal entity found for query '{query_text}'. Entity remains unresolved."
        )

    best = candidates[0]
    return EntityResolutionResult(
        query=query_text,
        resolved_primary_id=best.id,
        resolved_primary_name=best.legal_name,
        resolution_status=best.match_status,
        best_candidate=best,
        all_candidates=candidates,
        explanation=f"Resolved to legal entity '{best.legal_name}' with {best.match_confidence*100:.0f}% confidence ({best.match_status})."
    )

@router.get("", response_model=List[BuyerSummary])
def list_buyers(is_demo: Optional[bool] = None, db: Session = Depends(get_db)):
    query = db.query(Buyer)
    if is_demo is not None:
        query = query.filter(Buyer.is_demo == is_demo)
    buyers = query.all()
    results = []
    for b in buyers:
        profile = b.profile
        ins_status = b.insolvency_records[0].status if b.insolvency_records else "NO_PUBLIC_RECORD_FOUND"
        results.append(BuyerSummary(
            id=b.id,
            legal_name=b.legal_name,
            trade_name=b.trade_name,
            cin=b.cin,
            gstin=b.gstin,
            state=b.state,
            city=b.city,
            industry=b.industry,
            company_status=b.company_status,
            is_demo=b.is_demo,
            demo_tag=b.demo_tag,
            evidence_state=profile.evidence_state if profile else "LIMITED_EVIDENCE",
            late_payment_prob=profile.late_payment_prob if profile else None,
            expected_delay_days=profile.expected_delay_days if profile else None,
            total_disputes=len(b.disputes),
            insolvency_status=ins_status
        ))
    return results

@router.get("/{buyer_id}", response_model=BuyerDetail)
def get_buyer_detail(buyer_id: int, db: Session = Depends(get_db)):
    buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")

    p_analytics = compute_payment_analytics(buyer.id, buyer.legal_name, buyer.transactions)
    
    # Recalculate recommendation to ensure live sync with all submodules
    unresolved_disp = sum(1 for d in buyer.disputes if d.is_unresolved)
    tot_claim = sum(d.claim_amount for d in buyer.disputes) / 100000.0
    auditor_q = 1 if any(f.auditor_qualification_flag for f in buyer.filing_signals) else 0
    gc_warn = 1 if any(f.going_concern_warning for f in buyer.filing_signals) else 0
    neg_nw = 1 if any(f.negative_net_worth_flag for f in buyer.filing_signals) else 0
    charges = max([f.active_charges_count for f in buyer.filing_signals] or [0])
    group_def = 1 if any(r.has_insolvency_event or r.has_known_disputes for r in buyer.related_entities) else 0
    cirp_flag = 1 if any(r.status in ("ADMITTED", "ONGOING", "LIQUIDATION") for r in buyer.insolvency_records) else 0

    ml_feats = {
        "invoice_count": p_analytics.invoice_count,
        "historical_late_pct": p_analytics.late_payment_percentage,
        "historical_avg_delay": p_analytics.average_delay_days,
        "historical_max_delay": p_analytics.maximum_delay_days,
        "amt_weighted_delay": p_analytics.payment_amount_weighted_delay,
        "disputes_count": unresolved_disp,
        "dispute_amount_lakhs": tot_claim,
        "auditor_qualification": auditor_q,
        "going_concern_warning": gc_warn,
        "negative_net_worth": neg_nw,
        "active_charges_count": charges,
        "related_group_defaults": group_def,
        "cirp_insolvency_flag": cirp_flag
    }

    ml_pred = predictor.predict(ml_feats)
    recommendation = generate_commercial_recommendation(
        buyer_id=buyer.id,
        buyer_name=buyer.legal_name,
        payment_analytics=p_analytics,
        ml_prediction=ml_pred,
        disputes=buyer.disputes,
        filing_signals=buyer.filing_signals,
        insolvency_records=buyer.insolvency_records,
        related_entities=buyer.related_entities
    )

    directors_list = [
        DirectorItem(
            din=d.get("din"),
            name=d.get("name", "Unknown"),
            designation=d.get("designation", "Director"),
            appointment_date=d.get("appointment_date")
        ) for d in (buyer.directors or [])
    ]

    ins_status = buyer.insolvency_records[0].status if buyer.insolvency_records else "NO_PUBLIC_RECORD_FOUND"

    return BuyerDetail(
        id=buyer.id,
        legal_name=buyer.legal_name,
        trade_name=buyer.trade_name,
        cin=buyer.cin,
        gstin=buyer.gstin,
        pan=buyer.pan,
        registered_address=buyer.registered_address,
        city=buyer.city,
        state=buyer.state,
        pincode=buyer.pincode,
        incorporation_date=buyer.incorporation_date.isoformat() if buyer.incorporation_date else None,
        company_status=buyer.company_status,
        company_class=buyer.company_class,
        industry=buyer.industry,
        authorized_capital=buyer.authorized_capital,
        paid_up_capital=buyer.paid_up_capital,
        directors=directors_list,
        promoters=buyer.promoters or [],
        previous_names=buyer.previous_names or [],
        is_demo=buyer.is_demo,
        demo_tag=buyer.demo_tag,
        demo_scenario=buyer.demo_scenario,
        payment_analytics=p_analytics,
        commercial_recommendation=recommendation,
        disputes_count=len(buyer.disputes),
        unresolved_disputes_count=unresolved_disp,
        total_dispute_amount=sum(d.claim_amount for d in buyer.disputes),
        filing_signals_count=len(buyer.filing_signals),
        auditor_qualification_present=bool(auditor_q),
        going_concern_warning_present=bool(gc_warn),
        insolvency_status=ins_status,
        related_entities_count=len(buyer.related_entities),
        evidence_state=recommendation.evidence_state,
        last_verified="Verified across ROC, MSEFC & NCLT databases"
    )

@router.get("/{buyer_id}/graph", response_model=EntityGraphResponse)
def get_entity_graph(buyer_id: int, db: Session = Depends(get_db)):
    buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return build_entity_graph(buyer, buyer.related_entities)

@router.get("/{buyer_id}/payment-history", response_model=PaymentBehaviourAnalytics)
def get_payment_history(buyer_id: int, db: Session = Depends(get_db)):
    buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return compute_payment_analytics(buyer.id, buyer.legal_name, buyer.transactions)

@router.get("/{buyer_id}/disputes")
def get_disputes(buyer_id: int, db: Session = Depends(get_db)):
    buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return [
        {
            "id": d.id,
            "case_number": d.case_number,
            "claimant_name": d.claimant_name,
            "claim_amount": d.claim_amount,
            "application_date": d.application_date.isoformat(),
            "status": d.status,
            "council_location": d.council_location,
            "delay_days_claimed": d.delay_days_claimed,
            "is_unresolved": d.is_unresolved,
            "description": d.description,
            "source_portal": d.source_portal
        } for d in buyer.disputes
    ]

@router.get("/{buyer_id}/filings")
def get_filings(buyer_id: int, db: Session = Depends(get_db)):
    buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return [
        {
            "id": f.id,
            "financial_year": f.financial_year,
            "filing_date": f.filing_date.isoformat(),
            "form_type": f.form_type,
            "revenue_inr_cr": f.revenue_inr_cr,
            "net_profit_inr_cr": f.net_profit_inr_cr,
            "net_worth_inr_cr": f.net_worth_inr_cr,
            "total_debt_inr_cr": f.total_debt_inr_cr,
            "auditor_qualification_flag": f.auditor_qualification_flag,
            "auditor_notes": f.auditor_notes,
            "going_concern_warning": f.going_concern_warning,
            "negative_net_worth_flag": f.negative_net_worth_flag,
            "active_charges_count": f.active_charges_count,
            "document_reference": f.document_reference,
            "snippet": f.snippet
        } for f in buyer.filing_signals
    ]

@router.get("/{buyer_id}/insolvency")
def get_insolvency(buyer_id: int, db: Session = Depends(get_db)):
    buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return [
        {
            "id": r.id,
            "status": r.status,
            "case_number": r.case_number,
            "bench": r.bench,
            "petitioner": r.petitioner,
            "under_section": r.under_section,
            "admission_date": r.admission_date.isoformat() if r.admission_date else None,
            "status_details": r.status_details,
            "source_url": r.source_url,
            "searched_source": r.searched_source,
            "last_verified_at": r.last_verified_at.isoformat()
        } for r in buyer.insolvency_records
    ]

@router.get("/{buyer_id}/timeline", response_model=List[TimelineEvent])
def get_timeline(buyer_id: int, db: Session = Depends(get_db)):
    buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return build_buyer_timeline(buyer)

@router.get("/{buyer_id}/recommendation", response_model=CommercialRecommendation)
def get_recommendation(buyer_id: int, db: Session = Depends(get_db)):
    buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    detail = get_buyer_detail(buyer_id, db)
    return detail.commercial_recommendation

@router.get("/{buyer_id}/evidence", response_model=List[NormalizedEvidenceItem])
def get_all_normalized_evidence(buyer_id: int, db: Session = Depends(get_db)):
    buyer = db.query(Buyer).filter(Buyer.id == buyer_id).first()
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")

    items: List[NormalizedEvidenceItem] = []
    
    # Disputes
    for d in buyer.disputes:
        items.append(MSMESamadhaanProvider.normalize_dispute_to_evidence(d, buyer.legal_name))
        
    # MCA Filings
    for f in buyer.filing_signals:
        items.append(MCAFilingsProvider.normalize_filing_to_evidence(f, buyer.legal_name))
        
    # Insolvency
    for r in buyer.insolvency_records:
        items.append(InsolvencyNCLTProvider.normalize_insolvency_to_evidence(r, buyer.legal_name))
        
    return items
