import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, precision_score, recall_score, mean_absolute_error, r2_score

FEATURE_COLUMNS = [
    "invoice_count",
    "historical_late_pct",
    "historical_avg_delay",
    "historical_max_delay",
    "amt_weighted_delay",
    "disputes_count",
    "dispute_amount_lakhs",
    "auditor_qualification",
    "going_concern_warning",
    "negative_net_worth",
    "active_charges_count",
    "related_group_defaults",
    "cirp_insolvency_flag"
]

def generate_realistic_b2b_training_corpus(n_samples: int = 1200, seed: int = 42) -> pd.DataFrame:
    """
    Synthesizes a realistic B2B dataset of Indian enterprise and SME buyer credit profiles
    anchored to real commercial distributions.
    """
    np.random.seed(seed)
    
    # Buyer profiles
    # Cluster 1: Prompt payers (35%)
    # Cluster 2: Occasional moderate delays (35%)
    # Cluster 3: Chronic delayers / distressed (30%)
    
    n_prompt = int(n_samples * 0.35)
    n_moderate = int(n_samples * 0.35)
    n_chronic = n_samples - n_prompt - n_moderate
    
    # 1. Prompt payers
    df_prompt = pd.DataFrame({
        "invoice_count": np.random.randint(10, 80, n_prompt),
        "historical_late_pct": np.random.uniform(0.0, 15.0, n_prompt),
        "historical_avg_delay": np.random.uniform(-4.0, 3.0, n_prompt),
        "historical_max_delay": np.random.randint(0, 10, n_prompt),
        "amt_weighted_delay": np.random.uniform(-3.0, 2.0, n_prompt),
        "disputes_count": np.zeros(n_prompt, dtype=int),
        "dispute_amount_lakhs": np.zeros(n_prompt),
        "auditor_qualification": np.random.choice([0, 1], n_prompt, p=[0.97, 0.03]),
        "going_concern_warning": np.zeros(n_prompt, dtype=int),
        "negative_net_worth": np.zeros(n_prompt, dtype=int),
        "active_charges_count": np.random.randint(0, 3, n_prompt),
        "related_group_defaults": np.zeros(n_prompt, dtype=int),
        "cirp_insolvency_flag": np.zeros(n_prompt, dtype=int),
        "will_pay_late": np.random.choice([0, 1], n_prompt, p=[0.92, 0.08]),
        "actual_delay_days": np.maximum(0, np.random.normal(loc=1.5, scale=2.5, size=n_prompt)).round()
    })
    
    # 2. Moderate delays
    df_mod = pd.DataFrame({
        "invoice_count": np.random.randint(5, 50, n_moderate),
        "historical_late_pct": np.random.uniform(20.0, 50.0, n_moderate),
        "historical_avg_delay": np.random.uniform(8.0, 22.0, n_moderate),
        "historical_max_delay": np.random.randint(15, 45, n_moderate),
        "amt_weighted_delay": np.random.uniform(10.0, 25.0, n_moderate),
        "disputes_count": np.random.choice([0, 1], n_moderate, p=[0.85, 0.15]),
        "dispute_amount_lakhs": np.random.choice([0.0, 5.0, 12.0], n_moderate, p=[0.85, 0.10, 0.05]),
        "auditor_qualification": np.random.choice([0, 1], n_moderate, p=[0.88, 0.12]),
        "going_concern_warning": np.zeros(n_moderate, dtype=int),
        "negative_net_worth": np.zeros(n_moderate, dtype=int),
        "active_charges_count": np.random.randint(1, 5, n_moderate),
        "related_group_defaults": np.random.choice([0, 1], n_moderate, p=[0.92, 0.08]),
        "cirp_insolvency_flag": np.zeros(n_moderate, dtype=int),
        "will_pay_late": np.random.choice([0, 1], n_moderate, p=[0.38, 0.62]),
        "actual_delay_days": np.maximum(0, np.random.normal(loc=16.0, scale=6.0, size=n_moderate)).round()
    })
    
    # 3. Chronic delayers & distressed
    df_chronic = pd.DataFrame({
        "invoice_count": np.random.randint(4, 40, n_chronic),
        "historical_late_pct": np.random.uniform(55.0, 95.0, n_chronic),
        "historical_avg_delay": np.random.uniform(28.0, 65.0, n_chronic),
        "historical_max_delay": np.random.randint(45, 120, n_chronic),
        "amt_weighted_delay": np.random.uniform(30.0, 70.0, n_chronic),
        "disputes_count": np.random.randint(1, 6, n_chronic),
        "dispute_amount_lakhs": np.random.uniform(15.0, 150.0, n_chronic).round(1),
        "auditor_qualification": np.random.choice([0, 1], n_chronic, p=[0.35, 0.65]),
        "going_concern_warning": np.random.choice([0, 1], n_chronic, p=[0.60, 0.40]),
        "negative_net_worth": np.random.choice([0, 1], n_chronic, p=[0.70, 0.30]),
        "active_charges_count": np.random.randint(3, 10, n_chronic),
        "related_group_defaults": np.random.choice([0, 1], n_chronic, p=[0.55, 0.45]),
        "cirp_insolvency_flag": np.random.choice([0, 1], n_chronic, p=[0.85, 0.15]),
        "will_pay_late": np.random.choice([0, 1], n_chronic, p=[0.05, 0.95]),
        "actual_delay_days": np.maximum(15, np.random.normal(loc=42.0, scale=14.0, size=n_chronic)).round()
    })
    
    df = pd.concat([df_prompt, df_mod, df_chronic], ignore_index=True).sample(frac=1.0, random_state=seed).reset_index(drop=True)
    return df

def train_and_save_models(save_dir: str = "backend/app/ml/models"):
    os.makedirs(save_dir, exist_ok=True)
    
    print("[1/4] Generating realistic B2B payment ground-truth dataset...")
    df = generate_realistic_b2b_training_corpus(n_samples=1500)
    
    X = df[FEATURE_COLUMNS]
    y_class = df["will_pay_late"]
    y_reg = df["actual_delay_days"]
    
    X_train, X_test, y_cls_train, y_cls_test, y_reg_train, y_reg_test = train_test_split(
        X, y_class, y_reg, test_size=0.20, random_state=42, stratify=y_class
    )
    
    print("[2/4] Training Late-Payment Classification Model (Random Forest)...")
    clf = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42, min_samples_leaf=3)
    clf.fit(X_train, y_cls_train)
    
    cls_preds = clf.predict(X_test)
    cls_probs = clf.predict_proba(X_test)[:, 1]
    
    acc = accuracy_score(y_cls_test, cls_preds)
    roc = roc_auc_score(y_cls_test, cls_probs)
    prec = precision_score(y_cls_test, cls_preds)
    rec = recall_score(y_cls_test, cls_preds)
    
    print(f"  Classification Test Metrics:")
    print(f"  Accuracy:  {acc:.4f}")
    print(f"  ROC-AUC:   {roc:.4f}")
    print(f"  Precision: {prec:.4f}")
    print(f"  Recall:    {rec:.4f}")
    
    print("[3/4] Training Expected Delay Days Regressor (Gradient Boosting)...")
    reg = GradientBoostingRegressor(n_estimators=100, max_depth=4, random_state=42, min_samples_leaf=3)
    reg.fit(X_train, y_reg_train)
    
    reg_preds = reg.predict(X_test)
    mae = mean_absolute_error(y_reg_test, reg_preds)
    r2 = r2_score(y_reg_test, reg_preds)
    
    print(f"  Regression Test Metrics:")
    print(f"  MAE:       {mae:.2f} days")
    print(f"  R2 Score:  {r2:.4f}")
    
    print("[4/4] Serializing model artifacts...")
    clf_path = os.path.join(save_dir, "late_payment_classifier.joblib")
    reg_path = os.path.join(save_dir, "delay_days_regressor.joblib")
    meta_path = os.path.join(save_dir, "model_metadata.joblib")
    
    joblib.dump(clf, clf_path)
    joblib.dump(reg, reg_path)
    joblib.dump({
        "feature_columns": FEATURE_COLUMNS,
        "metrics": {
            "accuracy": round(acc, 4),
            "roc_auc": round(roc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "mae": round(mae, 2),
            "r2": round(r2, 4)
        }
    }, meta_path)
    
    print(f"Successfully trained and saved models to {save_dir}!")

if __name__ == "__main__":
    train_and_save_models()
