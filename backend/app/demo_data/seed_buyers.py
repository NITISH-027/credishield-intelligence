import datetime
from typing import List, Dict, Any
from ..database.models import (
    Buyer, Transaction, MSMEDispute, MCAFilingSignal, InsolvencyRecord, RelatedEntityLink, ReliabilityProfile
)
from ..payment_engine.analytics import compute_payment_analytics
from ..ml.pipeline import predictor
from ..recommendations.rules import generate_commercial_recommendation

def seed_demo_database(db):
    """
    Seeds 5 distinct, commercially realistic Indian buyer archetypes.
    Idempotent: clears existing demo buyers before seeding.
    """
    # Delete existing demo data
    demo_buyers = db.query(Buyer).filter(Buyer.is_demo == True).all()
    for b in demo_buyers:
        db.delete(b)
    db.commit()

    # ==========================================
    # BUYER A: Apex Precision Technologies India Pvt Ltd (Prompt Payer)
    # ==========================================
    buyer_a = Buyer(
        legal_name="Apex Precision Technologies India Pvt Ltd",
        trade_name="Apex Technologies",
        cin="U28112MH2016PTC284910",
        gstin="27AABCA1234F1Z5",
        pan="AABCA1234F",
        registered_address="Plot No. B-42, Chakan Industrial Area, Phase II, Pune",
        city="Pune",
        state="Maharashtra",
        pincode="410501",
        incorporation_date=datetime.date(2016, 4, 12),
        company_status="Active",
        company_class="Private Limited",
        industry="Automotive Components & Precision Tooling",
        authorized_capital=50000000.0,
        paid_up_capital=38000000.0,
        directors=[
            {"din": "01849201", "name": "Vikramaditya Kulkarni", "designation": "Managing Director", "appointment_date": "2016-04-12"},
            {"din": "07482910", "name": "Meera V. Kulkarni", "designation": "Director", "appointment_date": "2018-09-01"}
        ],
        promoters=["Kulkarni Family Trust", "Apex Precision International BV"],
        previous_names=["Apex Machining Works Pvt Ltd"],
        is_demo=True,
        demo_tag="Buyer A",
        demo_scenario="Prime tier-1 manufacturing buyer with 100% on-time settlement record, zero MSME disputes, robust profitability, and exemplary ROC filing compliance."
    )
    db.add(buyer_a)
    db.flush()

    # Buyer A Transactions (24 prompt invoices)
    base_date = datetime.date(2024, 1, 10)
    for i in range(24):
        issue = base_date + datetime.timedelta(days=i * 35)
        due = issue + datetime.timedelta(days=30)
        delay = -2 if i % 3 == 0 else (0 if i % 2 == 0 else 1) # virtually 0 or early
        pay = due + datetime.timedelta(days=delay)
        tx = Transaction(
            buyer_id=buyer_a.id,
            invoice_id=f"INV-APEX-2024-{i+101}",
            supplier_name="Mahindra Castings & Forgings MSME",
            invoice_amount=round(450000.0 + (i * 25000.0), 2),
            issue_date=issue,
            due_date=due,
            payment_date=pay,
            delay_days=delay,
            status="PAID",
            payment_terms_days=30
        )
        db.add(tx)

    # Buyer A MCA Filings
    db.add(MCAFilingSignal(
        buyer_id=buyer_a.id,
        financial_year="FY22-23",
        filing_date=datetime.date(2023, 10, 25),
        form_type="AOC-4",
        revenue_inr_cr=142.5,
        net_profit_inr_cr=16.8,
        net_worth_inr_cr=78.2,
        total_debt_inr_cr=12.4,
        auditor_qualification_flag=False,
        going_concern_warning=False,
        negative_net_worth_flag=False,
        active_charges_count=1,
        filing_delay_days=0,
        document_reference="MCA21-AOC4-SRN-Q2849102",
        snippet="Unmodified statutory audit opinion. All statutory dues including MSME payments settled within stipulated timelines under Sec 15 MSMED Act."
    ))
    db.add(MCAFilingSignal(
        buyer_id=buyer_a.id,
        financial_year="FY23-24",
        filing_date=datetime.date(2024, 10, 20),
        form_type="AOC-4",
        revenue_inr_cr=178.4,
        net_profit_inr_cr=21.5,
        net_worth_inr_cr=94.6,
        total_debt_inr_cr=9.8,
        auditor_qualification_flag=False,
        going_concern_warning=False,
        negative_net_worth_flag=False,
        active_charges_count=1,
        filing_delay_days=0,
        document_reference="MCA21-AOC4-SRN-R9182041",
        snippet="Clean financial disclosures. Operating cash flows positive at INR 24.2 Cr."
    ))

    # Buyer A Insolvency Record
    db.add(InsolvencyRecord(
        buyer_id=buyer_a.id,
        status="NO_PUBLIC_RECORD_FOUND",
        case_number=None,
        bench=None,
        status_details="Comprehensive search across IBBI registers and NCLT cause lists: No public record found.",
        searched_source="IBBI / NCLT Public Cause Lists",
        last_verified_at=datetime.datetime.utcnow()
    ))

    # Buyer A Related Entities
    db.add(RelatedEntityLink(
        source_buyer_id=buyer_a.id,
        related_entity_name="Apex Precision Europe BV",
        related_cin="NL-84910294",
        relationship_type="PARENT",
        ownership_percentage=74.0,
        evidence_notes="Holding company registered in Netherlands, owning 74% equity.",
        has_known_disputes=False,
        has_insolvency_event=False
    ))

    # ==========================================
    # BUYER B: Bharat Infra Ventures Limited (Chronic Delays & Disputes)
    # ==========================================
    buyer_b = Buyer(
        legal_name="Bharat Infra Ventures Limited",
        trade_name="Bharat Infra",
        cin="L45200DL2012PLC238491",
        gstin="07AABCB9876K1ZQ",
        pan="AABCB9876K",
        registered_address="12th Floor, Barakhamba Tower, Connaught Place, New Delhi",
        city="New Delhi",
        state="Delhi",
        pincode="110001",
        incorporation_date=datetime.date(2012, 8, 20),
        company_status="Active",
        company_class="Public Limited",
        industry="Civil Infrastructure & Heavy Engineering",
        authorized_capital=150000000.0,
        paid_up_capital=125000000.0,
        directors=[
            {"din": "02948192", "name": "Suresh Chandra Aggarwal", "designation": "Director", "appointment_date": "2012-08-20"},
            {"din": "03819204", "name": "Pradeep Singhania", "designation": "Whole-time Director", "appointment_date": "2015-02-14"}
        ],
        promoters=["Aggarwal Holdings LLP", "Singhania Infra Trust"],
        previous_names=["Bharat Earthmovers & Roads Ltd"],
        is_demo=True,
        demo_tag="Buyer B",
        demo_scenario="Large infrastructure contractor with prolonged payment cycles (+48 days average delay), 4 active MSME Samadhaan disputes, and deteriorating cash flow."
    )
    db.add(buyer_b)
    db.flush()

    # Buyer B Transactions (20 chronic late invoices)
    base_b = datetime.date(2024, 1, 15)
    for i in range(20):
        issue = base_b + datetime.timedelta(days=i * 32)
        due = issue + datetime.timedelta(days=30)
        delay = 35 + (i * 2) # Delay worsening from 35 to 73 days
        pay = due + datetime.timedelta(days=delay) if i < 18 else None # Last 2 open & overdue!
        tx = Transaction(
            buyer_id=buyer_b.id,
            invoice_id=f"INV-BIVL-2024-{i+201}",
            supplier_name=f"MSME Cement & Aggregate Supplier {i%4 + 1}",
            invoice_amount=round(1200000.0 + (i * 80000.0), 2),
            issue_date=issue,
            due_date=due,
            payment_date=pay,
            delay_days=delay if pay else 55,
            status="PAID" if pay else "OVERDUE",
            payment_terms_days=30
        )
        db.add(tx)

    # Buyer B MSME Disputes (4 cases)
    db.add(MSMEDispute(
        buyer_id=buyer_b.id,
        case_number="MSEFC/DL/2024/00481",
        claimant_name="Shree Ram Ready Mix Concrete LLP",
        claim_amount=4850000.0,
        application_date=datetime.date(2024, 3, 14),
        status="ORDER_PASSED_UNPAID",
        council_location="MSEFC New Delhi",
        delay_days_claimed=142,
        is_unresolved=True,
        description="Award passed under Sec 18(3) MSMED Act directing Bharat Infra to pay compound interest at three times RBI rate. Unpaid to date."
    ))
    db.add(MSMEDispute(
        buyer_id=buyer_b.id,
        case_number="MSEFC/DL/2024/00892",
        claimant_name="Vanguard Steel Fabrication Works",
        claim_amount=2840000.0,
        application_date=datetime.date(2024, 7, 22),
        status="UNDER_ARBITRATION",
        council_location="MSEFC New Delhi",
        delay_days_claimed=98,
        is_unresolved=True,
        description="Conciliation failed due to non-appearance by respondent; matter referred to statutory arbitration."
    ))
    db.add(MSMEDispute(
        buyer_id=buyer_b.id,
        case_number="MSEFC/HR/2024/00194",
        claimant_name="Gurgaon Heavy Earthmoving Equipments",
        claim_amount=1750000.0,
        application_date=datetime.date(2024, 9, 5),
        status="PENDING_CONCILIATION",
        council_location="MSEFC Haryana",
        delay_days_claimed=75,
        is_unresolved=True,
        description="Notice issued to respondent for non-settlement of equipment leasing invoices."
    ))
    db.add(MSMEDispute(
        buyer_id=buyer_b.id,
        case_number="MSEFC/DL/2023/00712",
        claimant_name="Krishna Electricals & Hardware",
        claim_amount=1200000.0,
        application_date=datetime.date(2023, 11, 10),
        status="MUTUALLY_SETTLED",
        council_location="MSEFC New Delhi",
        delay_days_claimed=120,
        resolution_date=datetime.date(2024, 2, 18),
        is_unresolved=False,
        description="Settled after 3 hearings with 15% discount accepted by small supplier."
    ))

    # Buyer B MCA Filings
    db.add(MCAFilingSignal(
        buyer_id=buyer_b.id,
        financial_year="FY23-24",
        filing_date=datetime.date(2024, 12, 15),
        form_type="AOC-4",
        revenue_inr_cr=310.0,
        net_profit_inr_cr=-18.4,
        net_worth_inr_cr=42.0,
        total_debt_inr_cr=265.0,
        auditor_qualification_flag=True,
        auditor_notes="Material delay in deposition of statutory dues and trade payables to MSME enterprises totaling INR 12.8 Cr remaining unpaid for >45 days.",
        going_concern_warning=False,
        negative_net_worth_flag=False,
        active_charges_count=8,
        filing_delay_days=45,
        document_reference="MCA21-AOC4-SRN-B8192044",
        snippet="Note 24 (Trade Payables): Principal amount due to Micro and Small Enterprises remaining unpaid at year end: INR 12,84,50,000."
    ))

    # Buyer B Insolvency
    db.add(InsolvencyRecord(
        buyer_id=buyer_b.id,
        status="NO_PUBLIC_RECORD_FOUND",
        status_details="No admitted CIRP proceedings found in searched NCLT cause lists.",
        searched_source="IBBI / NCLT Public Cause Lists",
        last_verified_at=datetime.datetime.utcnow()
    ))

    # ==========================================
    # BUYER C: Champaran Agro-Foods Pvt Ltd (Financial Distress & Auditor Note)
    # ==========================================
    buyer_c = Buyer(
        legal_name="Champaran Agro-Foods Pvt Ltd",
        trade_name="Champaran Foods",
        cin="U15400BR2014PTC022190",
        gstin="10AABCC4567M1ZV",
        pan="AABCC4567M",
        registered_address="Industrial Area, Phase-I, Fatuha, Patna",
        city="Patna",
        state="Bihar",
        pincode="803201",
        incorporation_date=datetime.date(2014, 3, 10),
        company_status="Active",
        company_class="Private Limited",
        industry="Agro-Processing & Cold Storage",
        authorized_capital=30000000.0,
        paid_up_capital=24000000.0,
        directors=[
            {"din": "01948201", "name": "Alok Kumar Verma", "designation": "Director", "appointment_date": "2014-03-10"},
            {"din": "06481920", "name": "Sunil Shrivastava", "designation": "Director", "appointment_date": "2017-06-12"}
        ],
        promoters=["Verma Agro Trust"],
        previous_names=["Champaran Cold Storage Pvt Ltd"],
        is_demo=True,
        demo_tag="Buyer C",
        demo_scenario="Food processor exhibiting severe balance sheet distress: negative net worth (-14 Cr), statutory auditor Going Concern doubt in CARO report, and expanding bank charges."
    )
    db.add(buyer_c)
    db.flush()

    # Buyer C Invoices (12 invoices, delays 20-55 days)
    for i in range(12):
        issue = datetime.date(2024, 2, 1) + datetime.timedelta(days=i * 30)
        due = issue + datetime.timedelta(days=30)
        delay = 22 + (i * 3)
        pay = due + datetime.timedelta(days=delay) if i < 10 else None
        db.add(Transaction(
            buyer_id=buyer_c.id,
            invoice_id=f"INV-CHAMP-2024-{i+301}",
            supplier_name="Packaging MSME Cartons & Plastics",
            invoice_amount=round(350000.0 + (i * 15000.0), 2),
            issue_date=issue,
            due_date=due,
            payment_date=pay,
            delay_days=delay if pay else 48,
            status="PAID" if pay else "OVERDUE",
            payment_terms_days=30
        ))

    # Buyer C MSME Disputes (2 cases)
    db.add(MSMEDispute(
        buyer_id=buyer_c.id,
        case_number="MSEFC/BR/2024/00142",
        claimant_name="Bihar Agricultural Produce Supplier MSME",
        claim_amount=1850000.0,
        application_date=datetime.date(2024, 4, 18),
        status="ORDER_PASSED_UNPAID",
        council_location="MSEFC Patna",
        delay_days_claimed=110,
        is_unresolved=True,
        description="MSEFC Patna order passed for non-settlement of raw produce supplies. Respondent cited negative working capital."
    ))
    db.add(MSMEDispute(
        buyer_id=buyer_c.id,
        case_number="MSEFC/BR/2024/00388",
        claimant_name="Vaishali Cold Chain Maintenance Services",
        claim_amount=920000.0,
        application_date=datetime.date(2024, 8, 5),
        status="UNDER_ARBITRATION",
        council_location="MSEFC Patna",
        delay_days_claimed=85,
        is_unresolved=True,
        description="Claim for unpaid annual refrigeration maintenance contracts. Matter pending arbitral hearing."
    ))

    # Buyer C MCA Filing
    db.add(MCAFilingSignal(
        buyer_id=buyer_c.id,
        financial_year="FY23-24",
        filing_date=datetime.date(2024, 11, 28),
        form_type="AOC-4",
        revenue_inr_cr=26.4,
        net_profit_inr_cr=-14.2,
        net_worth_inr_cr=-11.8, # Negative Net Worth
        total_debt_inr_cr=44.0,
        auditor_qualification_flag=True,
        auditor_notes="Material uncertainty regarding Going Concern due to continuous operating losses and negative net worth.",
        going_concern_warning=True,
        negative_net_worth_flag=True,
        active_charges_count=4,
        filing_delay_days=60,
        document_reference="MCA21-AOC4-SRN-C918204",
        snippet="Auditor's Report Page 4, Paragraph 3: 'The Company has accumulated losses resulting in complete erosion of its net worth. These events indicate the existence of a material uncertainty that may cast significant doubt on the Company's ability to continue as a going concern.'"
    ))

    # Buyer C Related Entities
    db.add(RelatedEntityLink(
        source_buyer_id=buyer_c.id,
        related_entity_name="Champaran Cold Chain Logistics LLP",
        related_cin="AAN-9102",
        relationship_type="SISTER_COMMON_DIRECTOR",
        shared_directors=["Alok Kumar Verma"],
        ownership_percentage=50.0,
        evidence_notes="Shares common promoter and registered address at Fatuha Industrial Area.",
        has_known_disputes=True,
        has_insolvency_event=False
    ))

    # Buyer C Insolvency
    db.add(InsolvencyRecord(
        buyer_id=buyer_c.id,
        status="PROCEEDINGS_FOUND",
        case_number="CP(IB)/148/KB/2024",
        bench="NCLT Kolkata Bench",
        petitioner="Bihari Farmers Cold Storage Association (Operational Creditor)",
        under_section="Section 9",
        admission_date=datetime.date(2024, 8, 12),
        status_details="Section 9 application filed by operational creditor for default of INR 85 Lakhs; notice issued.",
        searched_source="NCLT Kolkata Bench Cause List",
        last_verified_at=datetime.datetime.utcnow()
    ))

    # ==========================================
    # BUYER D: Deccan Precision Tools LLP (Thin File / Insufficient Evidence)
    # ==========================================
    buyer_d = Buyer(
        legal_name="Deccan Precision Tools LLP",
        trade_name="Deccan Tools",
        cin="AAH-4921",
        gstin="36AABCD1122P1ZX",
        pan="AABCD1122P",
        registered_address="Shed 14, ALEAP Industrial Estate, Gajularamaram, Hyderabad",
        city="Hyderabad",
        state="Telangana",
        pincode="500090",
        incorporation_date=datetime.date(2024, 1, 15),
        company_status="Active",
        company_class="Limited Liability Partnership",
        industry="Industrial Machine Tooling",
        authorized_capital=1000000.0,
        paid_up_capital=500000.0,
        directors=[
            {"din": "09812401", "name": "Venkatesh Rao", "designation": "Designated Partner", "appointment_date": "2024-01-15"}
        ],
        promoters=["Venkatesh Rao"],
        previous_names=[],
        is_demo=True,
        demo_tag="Buyer D",
        demo_scenario="Newly incorporated SME with ZERO trade receivables history and no annual filings yet. Demonstrates the mandatory fairness requirement: system outputs 'We don't know' rather than penalizing an honest small business as high risk."
    )
    db.add(buyer_d)
    db.flush()

    # Buyer D Insolvency check
    db.add(InsolvencyRecord(
        buyer_id=buyer_d.id,
        status="NO_PUBLIC_RECORD_FOUND",
        status_details="No public insolvency record found in searched IBBI registries.",
        searched_source="IBBI / NCLT Public Cause Lists",
        last_verified_at=datetime.datetime.utcnow()
    ))

    # ==========================================
    # BUYER E: Empire Solar EPC Limited (Phoenix Corporate Group)
    # ==========================================
    buyer_e = Buyer(
        legal_name="Empire Solar EPC Limited",
        trade_name="Empire Solar",
        cin="L40106GJ2018PLC104512",
        gstin="24AABCE8899N1ZS",
        pan="AABCE8899N",
        registered_address="Empire House, SG Highway, Bodakdev, Ahmedabad",
        city="Ahmedabad",
        state="Gujarat",
        pincode="380054",
        incorporation_date=datetime.date(2018, 9, 5),
        company_status="Active",
        company_class="Public Limited",
        industry="Renewable Energy & Solar EPC",
        authorized_capital=120000000.0,
        paid_up_capital=95000000.0,
        directors=[
            {"din": "02849102", "name": "Rajesh Varma", "designation": "Promoter & Chairman", "appointment_date": "2018-09-05"},
            {"din": "07491029", "name": "Harish Dave", "designation": "Managing Director", "appointment_date": "2020-04-01"}
        ],
        promoters=["Varma Solar Holdings", "Rajesh Varma"],
        previous_names=["SunPower Heavy Engineering Pvt Ltd"],
        is_demo=True,
        demo_tag="Buyer E",
        demo_scenario="Demonstrates entity-graph intelligence: entity was recently rebranded from 'SunPower Heavy Engineering' after its sister entity 'Empire Green Power Pvt Ltd' (sharing same promoter DIN: 02849102 Rajesh Varma) defaulted and was admitted to NCLT CIRP insolvency!"
    )
    db.add(buyer_e)
    db.flush()

    # Buyer E Transactions (15 invoices with moderate delays)
    for i in range(15):
        issue = datetime.date(2024, 1, 10) + datetime.timedelta(days=i * 28)
        due = issue + datetime.timedelta(days=30)
        delay = 18 + (i * 2)
        pay = due + datetime.timedelta(days=delay)
        db.add(Transaction(
            buyer_id=buyer_e.id,
            invoice_id=f"INV-ESOL-2024-{i+501}",
            supplier_name="Solar PV Module MSME Manufacturer",
            invoice_amount=round(1800000.0 + (i * 100000.0), 2),
            issue_date=issue,
            due_date=due,
            payment_date=pay,
            delay_days=delay,
            status="PAID",
            payment_terms_days=30
        ))

    # Buyer E Related Entities (Critical Phoenix Graph)
    db.add(RelatedEntityLink(
        source_buyer_id=buyer_e.id,
        related_entity_name="Empire Green Power Pvt Ltd",
        related_cin="U40100GJ2015PTC082910",
        relationship_type="SISTER_COMMON_DIRECTOR",
        shared_directors=["Rajesh Varma (DIN: 02849102)"],
        ownership_percentage=48.0,
        evidence_notes="Sister entity under common promoter Rajesh Varma. Admitted to NCLT Ahmedabad CIRP Insolvency after defaulting on INR 42 Cr MSME supplier debt.",
        has_known_disputes=True,
        has_insolvency_event=True
    ))
    db.add(RelatedEntityLink(
        source_buyer_id=buyer_e.id,
        related_entity_name="Empire Group Global Holdings Ltd",
        related_cin="U65990MH2014PLC251029",
        relationship_type="PARENT",
        shared_directors=["Rajesh Varma"],
        ownership_percentage=72.0,
        evidence_notes="Parent holding entity controlling 72% voting equity across group entities.",
        has_known_disputes=False,
        has_insolvency_event=False
    ))
    db.add(RelatedEntityLink(
        source_buyer_id=buyer_e.id,
        related_entity_name="Empire Inverters & Transformers Pvt Ltd",
        related_cin="U31100GJ2020PTC115920",
        relationship_type="SUBSIDIARY",
        shared_directors=["Harish Dave"],
        ownership_percentage=60.0,
        evidence_notes="60% owned manufacturing subsidiary.",
        has_known_disputes=False,
        has_insolvency_event=False
    ))

    # Buyer E MCA Filing
    db.add(MCAFilingSignal(
        buyer_id=buyer_e.id,
        financial_year="FY23-24",
        filing_date=datetime.date(2024, 10, 30),
        form_type="AOC-4",
        revenue_inr_cr=165.0,
        net_profit_inr_cr=4.2,
        net_worth_inr_cr=38.0,
        total_debt_inr_cr=98.0,
        auditor_qualification_flag=True,
        auditor_notes="Corporate guarantee issued of INR 35 Cr on behalf of defaulting sister concern Empire Green Power Pvt Ltd invoked by lenders.",
        going_concern_warning=False,
        negative_net_worth_flag=False,
        active_charges_count=5,
        filing_delay_days=15,
        document_reference="MCA21-AOC4-SRN-E1045124",
        snippet="Note 31: Contingent Liabilities — Corporate guarantee of INR 35,00,00,000 extended to sister company Empire Green Power Pvt Ltd."
    ))

    # Buyer E Insolvency
    db.add(InsolvencyRecord(
        buyer_id=buyer_e.id,
        status="NO_PUBLIC_RECORD_FOUND",
        status_details="No direct insolvency petition against Empire Solar EPC Ltd; however sister entity Empire Green Power Pvt Ltd is actively under NCLT CIRP.",
        searched_source="IBBI / NCLT Public Cause Lists",
        last_verified_at=datetime.datetime.utcnow()
    ))

    db.commit()

    # ==========================================
    # Precompute Profiles for all 5 Buyers
    # ==========================================
    for buyer in [buyer_a, buyer_b, buyer_c, buyer_d, buyer_e]:
        txs = db.query(Transaction).filter(Transaction.buyer_id == buyer.id).all()
        disputes = db.query(MSMEDispute).filter(MSMEDispute.buyer_id == buyer.id).all()
        filings = db.query(MCAFilingSignal).filter(MCAFilingSignal.buyer_id == buyer.id).all()
        insolvencies = db.query(InsolvencyRecord).filter(InsolvencyRecord.buyer_id == buyer.id).all()
        related = db.query(RelatedEntityLink).filter(RelatedEntityLink.source_buyer_id == buyer.id).all()

        p_analytics = compute_payment_analytics(buyer.id, buyer.legal_name, txs)

        # Prepare feature vector for ML
        unresolved_disp = sum(1 for d in disputes if d.is_unresolved)
        tot_claim = sum(d.claim_amount for d in disputes) / 100000.0 # in lakhs
        auditor_q = 1 if any(f.auditor_qualification_flag for f in filings) else 0
        gc_warn = 1 if any(f.going_concern_warning for f in filings) else 0
        neg_nw = 1 if any(f.negative_net_worth_flag for f in filings) else 0
        charges = max([f.active_charges_count for f in filings] or [0])
        group_def = 1 if any(r.has_insolvency_event or r.has_known_disputes for r in related) else 0
        cirp_flag = 1 if any(r.status in ("ADMITTED", "ONGOING", "LIQUIDATION") for r in insolvencies) else 0

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
        rec = generate_commercial_recommendation(
            buyer_id=buyer.id,
            buyer_name=buyer.legal_name,
            payment_analytics=p_analytics,
            ml_prediction=ml_pred,
            disputes=disputes,
            filing_signals=filings,
            insolvency_records=insolvencies,
            related_entities=related
        )

        profile = ReliabilityProfile(
            buyer_id=buyer.id,
            evidence_state=rec.evidence_state,
            total_invoices_observed=p_analytics.invoice_count,
            average_payment_days=p_analytics.average_payment_days,
            median_payment_days=p_analytics.median_payment_days,
            average_delay_days=p_analytics.average_delay_days,
            median_delay_days=p_analytics.median_delay_days,
            late_payment_percentage=p_analytics.late_payment_percentage,
            on_time_percentage=p_analytics.on_time_percentage,
            max_delay_days=p_analytics.maximum_delay_days,
            recent_trend=p_analytics.recent_delay_trend,
            late_payment_prob=rec.late_payment_probability,
            expected_delay_days=rec.expected_delay_days,
            prediction_confidence=rec.prediction_confidence,
            suggested_advance_pct=rec.suggested_advance_pct,
            recommended_credit_days=rec.recommended_credit_days,
            expected_payment_window=rec.expected_payment_window,
            recommendation_tier=rec.commercial_tier,
            commercial_summary=rec.summary_verdict,
            rationale_bullets=rec.why_reasons,
            confidence_reason=rec.confidence_reason
        )
        db.add(profile)

    db.commit()
    print("Demo dataset seeded successfully with 5 buyer archetypes!")
