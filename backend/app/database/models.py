from datetime import date, datetime
from sqlalchemy import (
    Column, Integer, String, Date, DateTime, Float, Boolean, Text, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from .session import Base

class Buyer(Base):
    __tablename__ = "buyers"

    id = Column(Integer, primary_key=True, index=True)
    legal_name = Column(String(255), unique=True, index=True, nullable=False)
    trade_name = Column(String(255), nullable=True)
    cin = Column(String(21), unique=True, index=True, nullable=True)  # e.g., U72200MH2015PTC123456
    gstin = Column(String(15), index=True, nullable=True)             # e.g., 27AABCU9603R1ZM
    pan = Column(String(10), index=True, nullable=True)
    registered_address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    pincode = Column(String(10), nullable=True)
    incorporation_date = Column(Date, nullable=True)
    company_status = Column(String(50), default="Active")            # Active, Strike-Off, Dormant, Liquidation
    company_class = Column(String(50), nullable=True)               # Private, Public, LLP
    industry = Column(String(100), nullable=True)
    authorized_capital = Column(Float, nullable=True)
    paid_up_capital = Column(Float, nullable=True)
    
    # Structural metadata (JSON lists)
    directors = Column(JSON, default=list)                         # [{"din": "01234567", "name": "Rajesh Sharma", "designation": "Director"}]
    promoters = Column(JSON, default=list)
    previous_names = Column(JSON, default=list)                    # ["Apex Fabricators Pvt Ltd"]
    
    # Demo flag & metadata
    is_demo = Column(Boolean, default=False)
    demo_tag = Column(String(50), nullable=True)                   # Buyer A, Buyer B, Buyer C, Buyer D, Buyer E
    demo_scenario = Column(Text, nullable=True)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="buyer", cascade="all, delete-orphan")
    disputes = relationship("MSMEDispute", back_populates="buyer", cascade="all, delete-orphan")
    filing_signals = relationship("MCAFilingSignal", back_populates="buyer", cascade="all, delete-orphan")
    insolvency_records = relationship("InsolvencyRecord", back_populates="buyer", cascade="all, delete-orphan")
    related_entities = relationship("RelatedEntityLink", foreign_keys="RelatedEntityLink.source_buyer_id", back_populates="source_buyer", cascade="all, delete-orphan")
    profile = relationship("ReliabilityProfile", uselist=False, back_populates="buyer", cascade="all, delete-orphan")


class RelatedEntityLink(Base):
    __tablename__ = "related_entity_links"

    id = Column(Integer, primary_key=True, index=True)
    source_buyer_id = Column(Integer, ForeignKey("buyers.id"), nullable=False)
    related_entity_name = Column(String(255), nullable=False)
    related_cin = Column(String(21), nullable=True)
    relationship_type = Column(String(50), nullable=False)  # PARENT, SUBSIDIARY, SISTER_COMMON_DIRECTOR, HISTORICAL_NAME, CROSS_GUARANTOR
    shared_directors = Column(JSON, default=list)           # List of director names shared
    ownership_percentage = Column(Float, nullable=True)
    evidence_notes = Column(Text, nullable=True)
    has_known_disputes = Column(Boolean, default=False)
    has_insolvency_event = Column(Boolean, default=False)
    
    source_buyer = relationship("Buyer", foreign_keys=[source_buyer_id], back_populates="related_entities")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("buyers.id"), nullable=False)
    invoice_id = Column(String(100), unique=True, index=True, nullable=False)
    supplier_name = Column(String(255), nullable=False)
    invoice_amount = Column(Float, nullable=False)
    issue_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    payment_date = Column(Date, nullable=True)
    delay_days = Column(Integer, nullable=True)             # payment_date - due_date (positive = late, negative/0 = on-time)
    status = Column(String(30), default="PAID")            # PAID, OVERDUE, DISPUTED
    payment_terms_days = Column(Integer, default=30)
    
    buyer = relationship("Buyer", back_populates="transactions")


class MSMEDispute(Base):
    __tablename__ = "msme_disputes"

    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("buyers.id"), nullable=False)
    case_number = Column(String(100), index=True, nullable=False)
    claimant_name = Column(String(255), nullable=False)     # MSME supplier filing dispute
    claim_amount = Column(Float, nullable=False)            # INR
    application_date = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)             # UNDER_ARBITRATION, MUTUALLY_SETTLED, ORDER_PASSED_UNPAID, PENDING_CONCILIATION
    council_location = Column(String(100), nullable=False)  # e.g., MSEFC Mumbai, MSEFC Bengaluru
    delay_days_claimed = Column(Integer, nullable=True)
    resolution_date = Column(Date, nullable=True)
    is_unresolved = Column(Boolean, default=True)
    description = Column(Text, nullable=True)
    source_portal = Column(String(100), default="MSME Samadhaan")

    buyer = relationship("Buyer", back_populates="disputes")


class MCAFilingSignal(Base):
    __tablename__ = "mca_filing_signals"

    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("buyers.id"), nullable=False)
    financial_year = Column(String(10), nullable=False)     # e.g., FY23-24
    filing_date = Column(Date, nullable=False)
    form_type = Column(String(50), nullable=False)         # AOC-4 (Financials), MGT-7 (Annual Return), CHG-1 (Charges)
    revenue_inr_cr = Column(Float, nullable=True)
    net_profit_inr_cr = Column(Float, nullable=True)
    net_worth_inr_cr = Column(Float, nullable=True)
    total_debt_inr_cr = Column(Float, nullable=True)
    auditor_qualification_flag = Column(Boolean, default=False)
    auditor_notes = Column(Text, nullable=True)
    going_concern_warning = Column(Boolean, default=False)
    negative_net_worth_flag = Column(Boolean, default=False)
    active_charges_count = Column(Integer, default=0)
    filing_delay_days = Column(Integer, default=0)
    document_reference = Column(String(255), nullable=True)
    snippet = Column(Text, nullable=True)

    buyer = relationship("Buyer", back_populates="filing_signals")


class InsolvencyRecord(Base):
    __tablename__ = "insolvency_records"

    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("buyers.id"), nullable=False)
    status = Column(String(50), default="NO_PUBLIC_RECORD_FOUND") # NO_PUBLIC_RECORD_FOUND, ADMITTED, ONGOING, RESOLVED, LIQUIDATION, UNKNOWN
    case_number = Column(String(100), nullable=True)
    bench = Column(String(100), nullable=True)              # NCLT New Delhi Bench, NCLT Mumbai
    petitioner = Column(String(255), nullable=True)         # Operational Creditor / Financial Creditor
    under_section = Column(String(50), nullable=True)       # Section 7, Section 9, Section 10
    admission_date = Column(Date, nullable=True)
    status_details = Column(Text, nullable=True)
    source_url = Column(String(255), nullable=True)
    searched_source = Column(String(100), default="IBBI / NCLT Public Cause Lists")
    last_verified_at = Column(DateTime, default=datetime.utcnow)

    buyer = relationship("Buyer", back_populates="insolvency_records")


class ReliabilityProfile(Base):
    __tablename__ = "reliability_profiles"

    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("buyers.id"), unique=True, nullable=False)
    evidence_state = Column(String(50), default="LIMITED_EVIDENCE") # SUFFICIENT_EVIDENCE, LIMITED_EVIDENCE, INSUFFICIENT_EVIDENCE, UNRESOLVED_ENTITY
    
    # Payment Behaviour stats
    total_invoices_observed = Column(Integer, default=0)
    average_payment_days = Column(Float, default=0.0)
    median_payment_days = Column(Float, default=0.0)
    average_delay_days = Column(Float, default=0.0)
    median_delay_days = Column(Float, default=0.0)
    late_payment_percentage = Column(Float, default=0.0)
    on_time_percentage = Column(Float, default=0.0)
    max_delay_days = Column(Integer, default=0)
    recent_trend = Column(String(50), default="STABLE")     # IMPROVING, STABLE, DETERIORATING
    
    # ML Outputs
    late_payment_prob = Column(Float, nullable=True)
    expected_delay_days = Column(Float, nullable=True)
    prediction_confidence = Column(Float, nullable=True)
    
    # Commercial Recommendation
    suggested_advance_pct = Column(Float, default=0.0)
    recommended_credit_days = Column(Integer, default=30)
    expected_payment_window = Column(String(50), default="30-45 days")
    recommendation_tier = Column(String(50), default="STANDARD")  # SECURED_ADVANCE, RESTRICTED_CREDIT, STANDARD_CREDIT, PREFERRED_CREDIT, CONSERVATIVE_UNVERIFIED
    
    commercial_summary = Column(Text, nullable=True)
    rationale_bullets = Column(JSON, default=list)
    confidence_reason = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)

    buyer = relationship("Buyer", back_populates="profile")
