# CrediShield Intelligence — PS-09-S2
### “Will This Buyer Actually Pay?” — Evidence-First B2B Buyer Risk Platform for MSMEs

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React%2018%20%2B%20Vite-61DAFB.svg?style=flat&logo=react)](https://react.dev)
[![TailwindCSS](https://img.shields.io/badge/Styling-Tailwind%20CSS-38B2AC.svg?style=flat&logo=tailwind-css)](https://tailwindcss.com)
[![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-F7931E.svg?style=flat&logo=scikit-learn)](https://scikit-learn.org)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python)](https://python.org)

---

## 1. Problem Statement
Delayed payments to micro, small, and medium enterprises (MSMEs) represent a crippling barrier to growth and liquidity in the Indian commercial ecosystem. While Section 15 of the MSMED Act 2006 mandates payment within 45 days, Indian B2B suppliers routinely wait 65 to 120 days for settlement.

Public records regarding buyer solvency and settlement track records exist across fragmented government portals (MSME Samadhaan MSEFC councils, Ministry of Corporate Affairs MCA21 filings, and NCLT/IBBI insolvency registries). However, suppliers lack the tools to:
1. Resolve who the true legal buyer is behind informal trade names and abbreviations.
2. Uncover corporate group linkages where promoters default under one legal entity and procure goods under another.
3. Quantify expected payment turnaround and formulate enforceable commercial terms (advance %, credit duration).
4. Distinguish between **known delinquency** and **unverified thin-file buyers** without unjustly punishing new small businesses.

**CrediShield Intelligence** delivers an evidence-grounded, explainable intelligence platform that answers: **“Will this buyer actually pay, when, and on what commercial terms?”**

---

## 2. Technical Bases & Adapted Open-Source Foundations
Rather than building from scratch, the system integrates proven architectural patterns from five open-source technical foundations:

| Reference Repository | Key Architectural Concepts Adapted |
|:---|:---|
| **A. CrediShield AI** | FastAPI backend structure, Pydantic schemas, transaction analytics, credit recommendation tiers, and human-in-the-loop review. |
| **B. Invoice Payment Prediction** | 3-step decision structure: on-time vs late classification, overdue thresholding, and continuous expected delay days regression. |
| **C. B2B Vendor Payment Delay Prediction** | Behavioral segmentation (Early, Medium, Prolonged payers), leakage-free feature computation strictly prior to invoice issue dates, and amount-weighted delays. |
| **D. Corporate Ownership Entity Resolution** | Indian legal suffix normalization (`Pvt Ltd`, `LLP`, `Ltd`), blocking key generation, multi-signal Jaro-Winkler string linkage, and corporate directorship graph traversal. |
| **E. UK Financial Risk Intelligence** | Grounded citation preservation (filing year, form type, auditor notes snippet), and honest negative reporting (*"No public record found in searched sources"* rather than claiming zero risk). |

---

## 3. System Architecture & Workflow

```
[Supplier Search / Lookup]
           │
           ▼
[Entity Resolution Engine] ──────────► [Corporate Ownership Graph]
(Suffix strip, CIN/GSTIN exact,         (Holding, Subsidiaries,
 Jaro-Winkler, Former names)             Common Director DINs, Contagion)
           │                                    │
           ├────────────────────────────────────┘
           ▼
[Public Source Intelligence Layer]
 ├── MSME Samadhaan (Section 18 disputes, claim amounts, council orders)
 ├── MCA21 / ROC (Form AOC-4, Going Concern warnings, CARO auditor notes)
 └── NCLT / IBBI (CIRP Insolvency Petitions, Sections 7/9/10, Liquidation)
           │
           ▼
[Universal Evidence Normalization]
           │
           ▼
[Payment Behaviour Analytics] ───► [ML Prediction Models]
(Turnaround days, late %,           (Random Forest Classifier: Late Prob
 recency-weighted delay trend)       Gradient Boosting: Expected Delay Days)
           │                                    │
           └─────────────────┬──────────────────┘
                             ▼
              [Commercial Recommendation Engine]
              ├── Expected Payment Window (e.g. 65–75 days)
              ├── Suggested Advance % (e.g. 40% upfront)
              ├── Recommended Credit Period (e.g. 15–30 days)
              ├── Mandatory Fairness Guardrail ("We don't know")
              └── Explainable "Why?" Evidence Cards
```

---

## 4. Key Differentiators

### A. Corporate Group Graph & Phoenix Entity Detection
A common failure mode in B2B credit is a promoter group abandoning a debt-ridden entity and creating a clean shell. CrediShield links entities sharing common **Director Identification Numbers (DINs)** or parent holding equity. If a sister entity is admitted to NCLT CIRP insolvency or has unpaid MSME awards, the system flags **Group Risk Spillover Alert**.

### B. Ethical Fairness & The "We Don't Know" State
A small enterprise with zero trade receivables history is **never** scored as high risk. The platform implements 4 explicit evidence states:
- `SUFFICIENT_EVIDENCE`: High observation depth across invoices, filings, and registers.
- `LIMITED_EVIDENCE`: Moderate depth with wider variance.
- `INSUFFICIENT_EVIDENCE`: Thin-file profile. System outputs: *"We don't know with high confidence. Recommend conservative milestone terms until payment history matures."*
- `UNRESOLVED_ENTITY`: Entity could not be linked to registered records.

### C. Explainable Evidence Cards
Every conclusion is tied to an auditable public record with source provenance, date, and document snippet. No black-box magic scores.

---

## 5. Machine Learning Pipeline & Performance

The late-payment engine employs a dual-stage architecture evaluated on held-out test data (80/20 stratified split):

### 1. Late-Payment Classification Model (Random Forest)
- **Target**: `will_pay_late` (Binary: 0 = On Time, 1 = Late)
- **Accuracy**: 84.3%
- **ROC-AUC**: 0.888
- **Recall**: 93.8% (Optimized to prevent false negatives for supplier protection)
- **Precision**: 80.2%

### 2. Expected Delay Days Regressor (Gradient Boosting)
- **Target**: `actual_delay_days` (Continuous days beyond contractual terms)
- **Mean Absolute Error (MAE)**: 5.76 days
- **R² Score**: 0.756

Model artifacts are persisted via `joblib` in `backend/app/ml/models/`.

---

## 6. Curated Benchmark Archetypes (Demo Dataset)

To ensure reliable, transparent hackathon evaluation without fabricating live government data, the platform includes 5 curated Indian buyer archetypes:

| Archetype | Legal Entity | Key Evidence Pattern | Recommended Terms | Evidence State |
|:---|:---|:---|:---|:---|
| **Buyer A** | Apex Precision Technologies India Pvt Ltd | 100% on-time settlement across 24 invoices, 0 MSME disputes, clean ROC filings, profitable. | 0% Advance, 30 Days Credit, Turnaround 25–33d. | `SUFFICIENT_EVIDENCE` |
| **Buyer B** | Bharat Infra Ventures Limited | Chronic delays (+48 days), 4 active MSME Samadhaan disputes, deteriorating cash flow. | 40% Advance, 15 Days Credit, Turnaround 65–85d. | `SUFFICIENT_EVIDENCE` |
| **Buyer C** | Champaran Agro-Foods Pvt Ltd | Severe distress: Negative Net Worth (-11.8 Cr), CARO Going Concern auditor uncertainty, Sec 9 insolvency. | 60% Advance, 15 Days Credit, Audit Exceptions. | `SUFFICIENT_EVIDENCE` |
| **Buyer D** | Deccan Precision Tools LLP | Newly incorporated SME with 0 trade invoices and no filings yet. Ethical fairness test. | 50% Milestone Advance, 15 Days Credit (*"We Don't Know"*). | `INSUFFICIENT_EVIDENCE` |
| **Buyer E** | Empire Solar EPC Limited | Rebranded entity from former name; sister company under common promoter DIN admitted to NCLT CIRP insolvency. | 40% Advance, Corporate Group Risk Spillover. | `SUFFICIENT_EVIDENCE` |

---

## 7. Quickstart Guide

### Step 1: Start Backend (Port 8000)
```bash
# In workspace root
pip install -r requirements.txt
python -m backend.app.demo_data.loader
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

### Step 2: Start Frontend (Port 3000)
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` in your browser.

---

## 8. Limitations & Future Improvements
1. **Live Government Captchas**: State MSEFC councils and MCA21 portals utilize rotating captchas; production rollout requires authenticated API access or official MCA corporate data feeds.
2. **GST Inward E-Invoicing**: Integration with GSTN GSTR-2B reconciliation would provide near real-time invoice matching.
3. **Automated MSME Council Filing**: Enabling MSME suppliers to draft and lodge Form 1 complaints directly from within the platform.
