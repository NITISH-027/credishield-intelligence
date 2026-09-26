# Architecture Specification — PS-09-S2 Buyer Payment Risk Intelligence

## 1. System Philosophy
The platform is designed around the tenet:
```
Buyer Lookup ──> Identity Resolution ──> Evidence Normalization ──> Behaviour Engine ──> Commercial Terms & Explainability
```
The system never produces an opaque risk score. Every commercial term (Advance %, Credit Days, Payment Window) is deterministically calibrated and backed by auditable public evidence.

---

## 2. Technical Stack
- **Backend**: Python 3.11, FastAPI, Pydantic v2, SQLAlchemy 2.0, SQLite / PostgreSQL.
- **Machine Learning**: scikit-learn, Random Forest Classifier (Late Payment Probability), Gradient Boosting Regressor (Expected Delay Days), joblib serialization.
- **Entity Resolution**: Custom Indian legal form normalizer (Pvt Ltd, Ltd, LLP), token fingerprint blocking, Jaro-Winkler & Levenshtein string metrics, directorship linkage.
- **Frontend**: React 18, Vite 5, Tailwind CSS, Lucide Icons, Recharts, SVG-based Interactive Corporate Graph.
- **Public Intelligence Adapters**:
  - `MSMESamadhaanProvider`: Section 18 MSMED Act council disputes.
  - `MCAFilingsProvider`: ROC annual accounts, CARO audit notes, Going Concern uncertainty, net worth erosion.
  - `InsolvencyNCLTProvider`: IBBI / NCLT CIRP petition registry with honest negative status handling.

---

## 3. Data Flow Architecture

```
                    ┌────────────────────────┐
                    │      SUPPLIER UI       │
                    │  (Landing / Search)    │
                    └───────────┬────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │  POST /api/buyers/     │
                    │         search         │
                    └───────────┬────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │   ENTITY RESOLUTION    │
                    │   - Suffix Stripping   │
                    │   - CIN/GSTIN Exact    │
                    │   - Jaro-Winkler Match │
                    │   - Former Name Lookup │
                    └───────────┬────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │ CORPORATE GRAPH ENGINE │
                    │  - Holding Structures  │
                    │  - Common Director DIN │
                    │  - Spillover Contagion │
                    └───────────┬────────────┘
                                │
                                ▼
         ┌──────────────────────┼──────────────────────┐
         ▼                      ▼                      ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  MSME SAMADHAAN  │  │   MCA21 / ROC    │  │   NCLT / IBBI    │
│ Payment Disputes │  │ Statutory Filing │  │  Insolvency CIRP │
└────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │ EVIDENCE NORMALIZATION │
                    │ (Common Evidence Model)│
                    └───────────┬────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │   PAYMENT BEHAVIOUR    │
                    │ - Recency Weighting    │
                    │ - Leakage-Free Stats   │
                    │ - Delay Distribution   │
                    └───────────┬────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │    ML INFERENCE        │
                    │ - Late Payment Prob    │
                    │ - Expected Delay Days  │
                    │ - Model Confidence     │
                    └───────────┬────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │  COMMERCIAL RECOMMEND  │
                    │ - Suggested Advance %  │
                    │ - Credit Period (Days) │
                    │ - Explainable "Why?"   │
                    │ - Ethical Unknown Rule │
                    └────────────────────────┘
```

---

## 4. Entity Resolution & Phoenix Detection
Corporate groups in India frequently default on supplier dues under one corporate entity (e.g. EPC subsidiary) and later initiate fresh procurement under a newly incorporated vehicle or sister firm sharing the same promoters.
CrediShield addresses this via:
1. **Legal Suffix Normalization**: Cleans 20+ corporate variations (Pvt Ltd, Private Limited, Limited Liability Partnership, Inc, etc.).
2. **Deterministic Keys**: CIN (21-char) and GSTIN (15-char) exact resolution.
3. **Historical Name Cross-Reference**: Preserves ROC former legal names.
4. **Directorship Graph Traversal**: Detects sister entities sharing Director Identification Numbers (DINs) and propagates risk flags if a related entity has unresolved disputes or active CIRP.

---

## 5. Ethical Fairness & Unknown Handling
Traditional black-box scoring systems unjustly penalize new or unrated small buyers due to absence of data.
CrediShield implements an explicit 4-tier Evidence State:
- `SUFFICIENT_EVIDENCE`: High transaction and filing volume.
- `LIMITED_EVIDENCE`: Moderate transaction depth.
- `INSUFFICIENT_EVIDENCE`: Thin-file profile. **Absence of public records is NOT treated as delinquent.** The system explicitly responds: *"We don't know with high confidence. Recommend conservative milestone terms."*
- `UNRESOLVED_ENTITY`: Query cannot be matched to any registered entity.
