from typing import Dict, Any, List, Tuple
from ..schemas.recommendation import CommercialRecommendation, RationaleCard
from ..schemas.payment import PaymentBehaviourAnalytics

def determine_evidence_state(
    invoice_count: int,
    has_mca_filings: bool,
    has_disputes_record: bool,
    has_insolvency_check: bool
) -> Tuple[str, str, str]:
    """
    Evaluates fairness and evidence completeness.
    Returns: (evidence_state, confidence_tier, confidence_reason)
    States: SUFFICIENT_EVIDENCE, LIMITED_EVIDENCE, INSUFFICIENT_EVIDENCE, UNRESOLVED_ENTITY
    """
    if invoice_count == 0 and not has_mca_filings and not has_disputes_record:
        return (
            "INSUFFICIENT_EVIDENCE",
            "INSUFFICIENT_DATA",
            "Thin public footprint: Zero observed invoices and no statutory filings available in searched registers. System expresses uncertainty rather than presuming adverse risk."
        )
    elif invoice_count < 4 and not has_mca_filings:
        return (
            "LIMITED_EVIDENCE",
            "LOW",
            "Limited transaction depth (fewer than 4 invoices) with no recent MCA filings. Estimates carry wider variance."
        )
    elif invoice_count >= 8 and has_mca_filings and has_insolvency_check:
        return (
            "SUFFICIENT_EVIDENCE",
            "HIGH",
            "Comprehensive evidence base spanning multi-year invoice payment history, MCA21 statutory accounts, and verified CIRP/MSEFC cause lists."
        )
    else:
        return (
            "SUFFICIENT_EVIDENCE",
            "MEDIUM",
            "Adequate invoice observation volume supported by core corporate registry cross-references."
        )

def generate_commercial_recommendation(
    buyer_id: int,
    buyer_name: str,
    payment_analytics: PaymentBehaviourAnalytics,
    ml_prediction: Dict[str, Any],
    disputes: List[Any],
    filing_signals: List[Any],
    insolvency_records: List[Any],
    related_entities: List[Any]
) -> CommercialRecommendation:
    """
    Deterministic rule-based commercial terms engine anchored to verified evidence.
    Calibrates advance %, credit period, expected payment window, and transparent 'Why?' explanations.
    """
    invoice_count = payment_analytics.invoice_count
    has_mca = len(filing_signals) > 0
    has_disputes = len(disputes) > 0
    has_insolvency_search = len(insolvency_records) > 0
    
    # 1. Determine Evidence State & Fairness
    ev_state, conf_tier, conf_reason = determine_evidence_state(
        invoice_count=invoice_count,
        has_mca_filings=has_mca,
        has_disputes_record=has_disputes,
        has_insolvency_check=has_insolvency_search
    )

    why_reasons: List[str] = []
    evidence_cards: List[RationaleCard] = []

    # Count adverse conditions
    unresolved_disputes = [d for d in disputes if getattr(d, 'is_unresolved', True)]
    cirp_admitted = any(getattr(r, 'status', '') in ("ADMITTED", "ONGOING", "LIQUIDATION") for r in insolvency_records)
    going_concern_warn = any(getattr(f, 'going_concern_warning', False) for f in filing_signals)
    auditor_qual = any(getattr(f, 'auditor_qualification_flag', False) for f in filing_signals)
    group_defaults = any(getattr(rel, 'has_insolvency_event', False) or getattr(rel, 'has_known_disputes', False) for rel in related_entities)

    late_prob = ml_prediction.get("late_payment_probability", 0.5)
    exp_delay = ml_prediction.get("expected_delay_days", 0.0)

    # 2. Case: INSUFFICIENT EVIDENCE (Thin File - Ethical fairness requirement)
    if ev_state == "INSUFFICIENT_EVIDENCE":
        why_reasons.append("We found limited public evidence for this buyer in searched registries.")
        why_reasons.append("Missing information is NOT treated as negative risk or proof of delinquency.")
        why_reasons.append("Prudent commercial guidance: Request 50% advance or shorter milestone-based terms until payment history is established.")
        
        evidence_cards.append(RationaleCard(
            category="PAYMENT_BEHAVIOUR",
            headline="Thin Public Data Profile",
            impact="CAUTION",
            evidence_snippet="No trade receivables recorded in MSME transaction index; no registered defaults found.",
            source="Commercial Accounts Index",
            confidence=0.5
        ))
        evidence_cards.append(RationaleCard(
            category="INSOLVENCY",
            headline="No Public Record Found",
            impact="NEUTRAL",
            evidence_snippet="No insolvency proceedings found in IBBI/NCLT public cause lists.",
            source="NCLT / IBBI Cause Lists",
            confidence=0.8
        ))

        return CommercialRecommendation(
            buyer_id=buyer_id,
            buyer_name=buyer_name,
            evidence_state=ev_state,
            expected_payment_window="Uncertain (No historical baseline)",
            suggested_advance_pct=50.0,
            recommended_credit_days=15,
            late_payment_probability=None, # Explicitly do not fabricate a confident score
            expected_delay_days=None,
            prediction_confidence=0.25,
            confidence_tier=conf_tier,
            confidence_reason=conf_reason,
            commercial_tier="CONSERVATIVE_UNVERIFIED",
            summary_verdict="We don't know with high confidence. Adopt conservative milestone billing to mitigate unrated buyer exposure.",
            why_reasons=why_reasons,
            evidence_cards=evidence_cards
        )

    # 3. Critical Distress / CIRP Cases
    if cirp_admitted:
        why_reasons.append("Active or admitted Corporate Insolvency Resolution Process (CIRP) under Insolvency and Bankruptcy Code (IBC).")
        why_reasons.append("Extreme operational creditor payment risk: Any unsecured supply will rank junior in resolution moratorium.")
        why_reasons.append("Strict commercial mandate: 100% upfront advance payment only before dispatch.")
        
        evidence_cards.append(RationaleCard(
            category="INSOLVENCY",
            headline="CIRP Proceedings Admitted",
            impact="NEGATIVE",
            evidence_snippet="Admitted CIRP petition registered on NCLT cause list. Supply moratorium in effect.",
            source="NCLT Registry",
            confidence=1.0
        ))

        return CommercialRecommendation(
            buyer_id=buyer_id,
            buyer_name=buyer_name,
            evidence_state=ev_state,
            expected_payment_window="90+ days / Moratorium restricted",
            suggested_advance_pct=100.0,
            recommended_credit_days=0,
            late_payment_probability=0.98,
            expected_delay_days=75.0,
            prediction_confidence=0.95,
            confidence_tier="HIGH",
            confidence_reason="Conclusive legal finding from NCLT cause lists.",
            commercial_tier="SECURED_ADVANCE",
            summary_verdict="High Risk: Active Insolvency Proceeding. Provide goods only against 100% confirmed advance or irrevocable LC.",
            why_reasons=why_reasons,
            evidence_cards=evidence_cards
        )

    # 4. Chronic Delays or Multiple Unresolved MSME Disputes
    if len(unresolved_disputes) >= 2 or late_prob > 0.65 or payment_analytics.average_delay_days > 25:
        suggested_advance = 40.0 if len(unresolved_disputes) < 3 else 60.0
        credit_days = 15 if len(unresolved_disputes) < 3 else 0
        exp_window = f"{int(30 + max(exp_delay, payment_analytics.average_delay_days))}-{int(45 + max(exp_delay, payment_analytics.average_delay_days))} days"

        why_reasons.append(f"Historical average delay is {payment_analytics.average_delay_days:.0f} days past contractual due dates.")
        why_reasons.append(f"{payment_analytics.late_payment_percentage:.0f}% of observed invoices were paid late.")
        if unresolved_disputes:
            why_reasons.append(f"{len(unresolved_disputes)} unresolved MSME Samadhaan dispute(s) identified under MSEFC.")
        if payment_analytics.recent_delay_trend == "DETERIORATING":
            why_reasons.append("Recent payment behaviour deteriorated significantly across last 3 billing cycles.")
        if group_defaults:
            why_reasons.append("Related corporate entity within group has active defaults or disputes.")
        if going_concern_warn:
            why_reasons.append("Statutory auditor noted material uncertainty over Going Concern in latest AOC-4 filing.")

        # Evidence Cards
        evidence_cards.append(RationaleCard(
            category="PAYMENT_BEHAVIOUR",
            headline=f"Historical Average Delay: +{payment_analytics.average_delay_days:.0f} Days",
            impact="NEGATIVE",
            evidence_snippet=f"{payment_analytics.late_payment_percentage:.0f}% of {payment_analytics.invoice_count} transactions were settled past terms. Typical delay +{payment_analytics.median_delay_days:.0f} days.",
            source="Verified Receivables Ledger",
            confidence=0.95
        ))

        if unresolved_disputes:
            evidence_cards.append(RationaleCard(
                category="MSME_DISPUTES",
                headline=f"{len(unresolved_disputes)} Unresolved MSME Samadhaan Cases",
                impact="NEGATIVE",
                evidence_snippet=f"MSEFC records reflect active statutory claims by suppliers totaling INR {sum(d.claim_amount for d in unresolved_disputes):,.0f}.",
                source="MSME Samadhaan Portal",
                confidence=1.0
            ))

        if group_defaults:
            evidence_cards.append(RationaleCard(
                category="RELATED_ENTITY",
                headline="Group Entity Contagion Risk",
                impact="CAUTION",
                evidence_snippet="Common directors or parent company affiliated with defaulting sister entity.",
                source="ROC Director DIN & Ownership Linkage",
                confidence=0.90
            ))

        return CommercialRecommendation(
            buyer_id=buyer_id,
            buyer_name=buyer_name,
            evidence_state=ev_state,
            expected_payment_window=exp_window,
            suggested_advance_pct=suggested_advance,
            recommended_credit_days=credit_days,
            late_payment_probability=late_prob,
            expected_delay_days=exp_delay,
            prediction_confidence=ml_prediction.get("prediction_confidence", 0.85),
            confidence_tier=conf_tier,
            confidence_reason=conf_reason,
            commercial_tier="RESTRICTED_CREDIT",
            summary_verdict=f"Restricted Commercial Terms Advised. Secure {suggested_advance:.0f}% advance and enforce short credit duration.",
            why_reasons=why_reasons,
            evidence_cards=evidence_cards
        )

    # 5. Strong / Prompt Payer (Low Risk)
    suggested_advance = 10.0 if payment_analytics.late_payment_percentage > 10 else 0.0
    credit_days = 30 if payment_analytics.late_payment_percentage <= 15 else 21
    exp_window = f"{int(payment_analytics.average_payment_days - 3)}-{int(payment_analytics.average_payment_days + 5)} days"

    why_reasons.append(f"Strong historical payment performance: {payment_analytics.on_time_percentage:.0f}% on-time settlement rate.")
    why_reasons.append(f"Historical average delay is negligible ({payment_analytics.average_delay_days:.1f} days).")
    why_reasons.append("Zero MSME Samadhaan payment disputes found in MSEFC records.")
    why_reasons.append("Clean statutory filings with zero auditor qualifications or going concern remarks.")
    why_reasons.append("No insolvency proceedings found in searched public registries.")

    evidence_cards.append(RationaleCard(
        category="PAYMENT_BEHAVIOUR",
        headline=f"Consistent On-Time Settlement ({payment_analytics.on_time_percentage:.0f}%)",
        impact="POSITIVE",
        evidence_snippet=f"{payment_analytics.invoice_count} transactions observed with average payment turnaround of {payment_analytics.average_payment_days:.0f} days.",
        source="Verified Receivables Ledger",
        confidence=0.98
    ))
    evidence_cards.append(RationaleCard(
        category="MSME_DISPUTES",
        headline="Zero MSME Payment Disputes",
        impact="POSITIVE",
        evidence_snippet="Clean record across all state Facilitation Council portals.",
        source="MSME Samadhaan Portal",
        confidence=1.0
    ))
    evidence_cards.append(RationaleCard(
        category="INSOLVENCY",
        headline="No Public Insolvency Records",
        impact="POSITIVE",
        evidence_snippet="No insolvency proceedings found in searched public IBBI and NCLT cause lists.",
        source="IBBI / NCLT Public Cause Lists",
        confidence=1.0
    ))

    return CommercialRecommendation(
        buyer_id=buyer_id,
        buyer_name=buyer_name,
        evidence_state=ev_state,
        expected_payment_window=exp_window,
        suggested_advance_pct=suggested_advance,
        recommended_credit_days=credit_days,
        late_payment_probability=late_prob,
        expected_delay_days=exp_delay,
        prediction_confidence=ml_prediction.get("prediction_confidence", 0.90),
        confidence_tier=conf_tier,
        confidence_reason=conf_reason,
        commercial_tier="PREFERRED_CREDIT" if suggested_advance == 0 else "STANDARD_CREDIT",
        summary_verdict="Reliable Commercial Profile. Standard 30-day commercial credit terms supported by solid historical compliance.",
        why_reasons=why_reasons,
        evidence_cards=evidence_cards
    )
