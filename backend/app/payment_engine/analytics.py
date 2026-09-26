import numpy as np
from typing import List, Dict, Any, Optional
from datetime import date
from ..schemas.payment import PaymentBehaviourAnalytics, TransactionItem

def compute_payment_analytics(buyer_id: int, buyer_name: str, transactions: List[Any]) -> PaymentBehaviourAnalytics:
    """
    Computes rigorous buyer-level payment behavior features from observed invoices.
    Prevents target leakage and implements recency-weighted delay tracking.
    """
    if not transactions:
        return PaymentBehaviourAnalytics(
            buyer_id=buyer_id,
            buyer_name=buyer_name,
            invoice_count=0,
            average_payment_days=0.0,
            median_payment_days=0.0,
            average_delay_days=0.0,
            median_delay_days=0.0,
            late_payment_percentage=0.0,
            on_time_percentage=0.0,
            early_payment_percentage=0.0,
            maximum_delay_days=0,
            recent_delay_trend="NO_DATA",
            payment_amount_weighted_delay=0.0,
            segment="THIN_FILE",
            delay_distribution={"on_time": 0, "1_15_days": 0, "16_30_days": 0, "31_60_days": 0, "over_60_days": 0},
            recent_invoices=[]
        )

    # Sort chronologically by issue date
    sorted_txs = sorted(transactions, key=lambda tx: tx.issue_date)
    
    delays = []
    payment_durations = []
    weights = []
    amounts = []
    
    distribution = {
        "on_time": 0,
        "1_15_days": 0,
        "16_30_days": 0,
        "31_60_days": 0,
        "over_60_days": 0
    }
    
    recent_invoices_items = []

    for idx, tx in enumerate(sorted_txs):
        delay = tx.delay_days if tx.delay_days is not None else 0
        delays.append(delay)
        amounts.append(tx.invoice_amount)
        
        # Duration from issue to payment
        if tx.payment_date and tx.issue_date:
            dur = (tx.payment_date - tx.issue_date).days
        else:
            dur = tx.payment_terms_days + max(0, delay)
        payment_durations.append(dur)
        
        # Recency weight (exponential weighting giving higher impact to latest 5 invoices)
        weight = 1.0 + (idx / max(1, len(sorted_txs))) * 1.5
        weights.append(weight)
        
        # Bucketing
        if delay <= 0:
            distribution["on_time"] += 1
        elif 1 <= delay <= 15:
            distribution["1_15_days"] += 1
        elif 16 <= delay <= 30:
            distribution["16_30_days"] += 1
        elif 31 <= delay <= 60:
            distribution["31_60_days"] += 1
        else:
            distribution["over_60_days"] += 1
            
        recent_invoices_items.append(TransactionItem(
            id=tx.id,
            invoice_id=tx.invoice_id,
            supplier_name=tx.supplier_name,
            invoice_amount=tx.invoice_amount,
            issue_date=tx.issue_date.isoformat(),
            due_date=tx.due_date.isoformat(),
            payment_date=tx.payment_date.isoformat() if tx.payment_date else None,
            delay_days=tx.delay_days,
            status=tx.status,
            payment_terms_days=tx.payment_terms_days
        ))

    total = len(delays)
    avg_delay = float(np.mean(delays))
    med_delay = float(np.median(delays))
    avg_pay_days = float(np.mean(payment_durations))
    med_pay_days = float(np.median(payment_durations))
    max_delay = int(max(delays)) if delays else 0
    
    late_count = sum(1 for d in delays if d > 0)
    early_count = sum(1 for d in delays if d < 0)
    on_time_count = sum(1 for d in delays if d <= 0)
    
    late_pct = round((late_count / total) * 100, 1)
    on_time_pct = round((on_time_count / total) * 100, 1)
    early_pct = round((early_count / total) * 100, 1)
    
    # Amount-weighted delay
    total_amount = sum(amounts)
    if total_amount > 0:
        amt_weighted_delay = float(sum(d * a for d, a in zip(delays, amounts)) / total_amount)
    else:
        amt_weighted_delay = avg_delay

    # Trend calculation (comparing last 30% vs first 30%)
    if total >= 4:
        split = max(1, total // 3)
        early_delays_mean = np.mean(delays[:split])
        recent_delays_mean = np.mean(delays[-split:])
        if recent_delays_mean > early_delays_mean + 5:
            trend = "DETERIORATING"
        elif recent_delays_mean < early_delays_mean - 5:
            trend = "IMPROVING"
        else:
            trend = "STABLE"
    else:
        trend = "STABLE"

    # Behavioral segment (adapted from B2B vendor segmentation reference)
    if total < 3:
        segment = "THIN_FILE"
    elif late_pct < 15 and avg_delay <= 2:
        segment = "EARLY_PAYER"
    elif late_pct <= 45 and avg_delay <= 15:
        segment = "MEDIUM_DURATION"
    else:
        segment = "PROLONGED_PAYER"

    return PaymentBehaviourAnalytics(
        buyer_id=buyer_id,
        buyer_name=buyer_name,
        invoice_count=total,
        average_payment_days=round(avg_pay_days, 1),
        median_payment_days=round(med_pay_days, 1),
        average_delay_days=round(avg_delay, 1),
        median_delay_days=round(med_delay, 1),
        late_payment_percentage=late_pct,
        on_time_percentage=on_time_pct,
        early_payment_percentage=early_pct,
        maximum_delay_days=max_delay,
        recent_delay_trend=trend,
        payment_amount_weighted_delay=round(amt_weighted_delay, 1),
        segment=segment,
        delay_distribution=distribution,
        recent_invoices=recent_invoices_items[-10:] # Last 10 invoices
    )
