# Quick Setup & Execution Guide — PS-09-S2

This guide outlines how to run the complete end-to-end platform locally.

---

## 1. Prerequisites
- **Python**: 3.10+ (tested on Python 3.11)
- **Node.js**: v18+ (tested on Node v24)
- **npm**: v9+ (tested on npm 11)

---

## 2. Backend Setup & Run

### A. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### B. Seed the Benchmark Database
Initializes the SQLite database schema and seeds the 5 curated buyer archetypes:
```bash
python -m backend.app.demo_data.loader
```

### C. (Optional) Retrain ML Models
The model artifacts are pre-trained and saved in `backend/app/ml/models/`. If you wish to retrain from scratch:
```bash
python -m backend.app.ml.train
```

### D. Start the FastAPI Backend Server
```bash
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
API Documentation will be live at: `http://127.0.0.1:8000/docs`

---

## 3. Frontend Setup & Run

### A. Navigate to Frontend Directory
```bash
cd frontend
```

### B. Install Dependencies
```bash
npm install
```

### C. Start Development Server
```bash
npm run dev
```
The modern Web UI will be live at: `http://localhost:3000`

---

## 4. End-to-End Evaluation Flow
1. Open `http://localhost:3000` in your web browser.
2. Read the landing page message: *"Before you give credit, know who you're dealing with."*
3. Click **"Check a Buyer"** or use the search box:
   - Try typing `Apex Machining` to test historical name entity resolution.
   - Try searching `Bharat Infra` to inspect chronic MSME disputes and delayed payments.
   - Try searching `SunPower Heavy` to see the corporate group phoenix detection in action.
   - Try searching `Deccan Precision` to see the ethical fairness / "We don't know" state.
4. Inspect the **Recommended Commercial Terms**: Suggested Advance %, Credit Period, and Payment Window.
5. Review the **"WHY?"** section with auditable evidence cards citing sources and dates.
6. Explore the **Interactive Tabs**:
   - **Payment Behaviour**: Recharts delay distribution and transaction ledger.
   - **Entity Graph**: Visual corporate network with zoom/pan and node inspector.
   - **Public Evidence**: MSME Samadhaan council cases and MCA21 ROC filings.
   - **Evidence Timeline**: Chronological events with clickable evidence dialogs.
