# Public Source Intelligence Layer

Adapted from `uk-financial-risk-intelligence`.

## 1. MSME Samadhaan (MSEFC Councils)
- Ingests delayed payment dispute records under Section 18 of the Micro, Small and Medium Enterprises Development (MSMED) Act 2006.
- Tracks: Case number, Council jurisdiction (MSEFC Mumbai, Delhi, etc.), Claimant MSME, Claim amount, Resolution status, and statutory interest awards (3x RBI bank rate).

## 2. MCA21 / ROC Statutory Filings
- Ingests Form AOC-4 (Financial Statements), Form MGT-7 (Annual Return), and Form CHG-1 (Charges).
- Extracts revenue, profit/loss, net worth erosion, active registered bank charges, and statutory auditor disclosures.
- Preserves document reference SRN, page, and snippet.

## 3. NCLT & IBBI Insolvency
- Queries Corporate Insolvency Resolution Process (CIRP) records under Sections 7, 9, and 10 of the Insolvency and Bankruptcy Code 2016.
- Strictly adheres to the negative reporting principle: returns `"No public record found in searched sources"` rather than claiming zero insolvency risk.
