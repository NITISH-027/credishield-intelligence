# Machine Learning Prediction Pipeline

Adapted from `invoice-payment-prediction` and `B2B-Vendor-Payment-Delay-Prediction`.

## 1. Feature Engineering
- `invoice_count`: Number of prior observed transactions
- `historical_late_pct`: Percentage of past invoices settled past agreed terms
- `historical_avg_delay`: Mean delay days across prior settled transactions
- `amt_weighted_delay`: Turnaround delay weighted by invoice value (prevents masking large delinquent invoices with small prompt payments)
- `disputes_count`: Active MSME Samadhaan Section 18 cases
- `auditor_qualification`: CARO qualification flag (1 or 0)
- `going_concern_warning`: Statutory auditor Going Concern uncertainty (1 or 0)
- `cirp_insolvency_flag`: NCLT CIRP petition admitted (1 or 0)
- `related_group_defaults`: Cross-entity directorship default detected (1 or 0)

## 2. Models
1. **Late Payment Classifier**: `RandomForestClassifier(n_estimators=100, max_depth=6)`
   - Accuracy: 84.3%
   - ROC-AUC: 0.888
   - Recall: 93.8%
2. **Expected Delay Days Regressor**: `GradientBoostingRegressor(n_estimators=100, max_depth=4)`
   - MAE: 5.76 days
   - R²: 0.756
