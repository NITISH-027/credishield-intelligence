# API Specification — PS-09-S2 Buyer Intelligence Platform

The platform exposes RESTful endpoints with Pydantic schema validation.

Base URL: `http://localhost:8000/api`

---

## 1. Entity Resolution & Search

### `POST /buyers/search`
Resolves user input (company name, trade alias, CIN, GSTIN) against corporate records using multi-signal matching.

**Request Body:**
```json
{
  "query": "Apex Machining",
  "cin": "U28112MH2016PTC284910",
  "gstin": null
}
```

**Response (200 OK):**
```json
{
  "query": "Apex Machining",
  "resolved_primary_id": 1,
  "resolved_primary_name": "Apex Precision Technologies India Pvt Ltd",
  "resolution_status": "LIKELY_MATCH",
  "best_candidate": {
    "id": 1,
    "legal_name": "Apex Precision Technologies India Pvt Ltd",
    "cin": "U28112MH2016PTC284910",
    "gstin": "27AABCA1234F1Z5",
    "match_confidence": 0.712,
    "match_status": "LIKELY_MATCH",
    "match_signals": ["Name Jaro-Winkler: 0.83, Token Overlap: 0.33", "Trade name match: 'Apex Technologies'"]
  },
  "explanation": "Resolved to legal entity 'Apex Precision Technologies India Pvt Ltd' with 71% confidence (LIKELY_MATCH)."
}
```

---

## 2. Buyer Profile & Dossier

### `GET /buyers/{buyer_id}`
Returns full legal identity, directors with DINs, promoters, address, and summary risk counts.

### `GET /buyers/{buyer_id}/graph`
Returns corporate ownership network with holding company, subsidiaries, sister entities (common DIN), and cross-entity default spillover alerts.

### `GET /buyers/{buyer_id}/payment-history`
Returns recency-weighted delay analytics, invoice distribution, turnaround days, and observed trade ledger.

### `GET /buyers/{buyer_id}/disputes`
Returns MSME Samadhaan (MSEFC) records under Section 18 MSMED Act with claimant, claim value, status, and awards.

### `GET /buyers/{buyer_id}/filings`
Returns MCA21 statutory filing signals, CARO audit notes, Going Concern flags, and registered bank charges.

### `GET /buyers/{buyer_id}/insolvency`
Returns NCLT / IBBI CIRP petition status (ADMITTED, ONGOING, NO_PUBLIC_RECORD_FOUND).

### `GET /buyers/{buyer_id}/timeline`
Returns chronological evidence events from incorporation to latest lookup with source citations.

### `GET /buyers/{buyer_id}/recommendation`
Returns deterministic commercial terms (Suggested Advance %, Credit Days, Payment Window) with explainable evidence cards.

---

## 3. Demo Benchmark Management

### `GET /demo/buyers`
Lists the 5 curated buyer archetypes.

### `POST /demo/reset`
Reseeds the database to standard benchmark state.
