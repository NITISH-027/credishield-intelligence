# Entity Resolution & Group Graph Specification

Adapted from `corporate-ownership-entity-resolution`.

## 1. Indian Corporate Suffix Normalization
The engine normalizes 20+ corporate suffix and prefix variations common in Indian registrations:
- `Private Limited`, `Pvt Ltd`, `Pvt. Ltd.`, `Pvt`
- `Limited`, `Ltd.`, `Ltd`
- `Limited Liability Partnership`, `LLP`
- `One Person Company`, `OPC`
- `Enterprises`, `Industries`, `Technologies`, `Solutions`, `India`

## 2. Blocking & Candidate Retrieval
Avoids quadratic $O(N^2)$ comparisons by blocking across derived candidate keys:
- `tok1:<first_token>`
- `pref:<first_4_chars>`
- `fp:<token_fingerprint>`
- `st:<state_code>`
- `cin_roc:<roc_code>`

## 3. Multi-Signal Matching Function
- **Exact CIN Match**: 1.0 (MATCHED)
- **Exact GSTIN Match**: 1.0 (MATCHED)
- **Exact Normalized Legal Name**: 0.95 (MATCHED)
- **Historical / Former Name Match**: 0.92 (MATCHED)
- **Weighted String Distance**: $0.5 \times \text{Jaro-Winkler} + 0.3 \times \text{Token Overlap} + 0.2 \times \text{SequenceMatcher}$
- **Thresholds**:
  - `MATCHED`: $\ge 0.88$
  - `LIKELY_MATCH`: $0.70 - 0.87$
  - `POSSIBLE_MATCH`: $0.50 - 0.69$
  - `UNRESOLVED`: $< 0.50$
