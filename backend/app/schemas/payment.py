from typing import Optional, List
from pydantic import BaseModel
from datetime import date

class TransactionItem(BaseModel):
    id: int
    invoice_id: str
    supplier_name: str
    invoice_amount: float
    issue_date: str
    due_date: str
    payment_date: Optional[str] = None
    delay_days: Optional[int] = None
    status: str                        # PAID, OVERDUE, DISPUTED
    payment_terms_days: int

class PaymentBehaviourAnalytics(BaseModel):
    buyer_id: int
    buyer_name: str
    invoice_count: int
    average_payment_days: float
    median_payment_days: float
    average_delay_days: float
    median_delay_days: float
    late_payment_percentage: float
    on_time_percentage: float
    early_payment_percentage: float
    maximum_delay_days: int
    recent_delay_trend: str            # IMPROVING, STABLE, DETERIORATING
    payment_amount_weighted_delay: float
    segment: str                       # EARLY_PAYER, MEDIUM_DURATION, PROLONGED_PAYER, THIN_FILE
    delay_distribution: dict           # {"on_time": 10, "1_15_days": 4, "16_30_days": 3, "31_60_days": 2, "over_60_days": 5}
    recent_invoices: List[TransactionItem] = []
