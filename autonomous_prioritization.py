# autonomous_prioritization.py
import joblib
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import classification_report, mean_absolute_error, roc_auc_score

from core import MODELS_DIR, load_data, split_targets, build_preprocessor

def train_autonomous_prioritization():
    df = load_data()
    X_train, X_test, y_pr_train, y_pr_test, _, _, y_sla_train, y_sla_test = split_targets(df)
    pre = build_preprocessor()

    # priority (encoded)[file:1]
    pr_model = Pipeline([
        ("pre", pre),
        ("clf", RandomForestClassifier(
            n_estimators=20,
            max_depth=10,
            random_state=42,
            class_weight="balanced",
        )),
    ])
    pr_model.fit(X_train, y_pr_train)
    print("Priority:\n", classification_report(y_pr_test, pr_model.predict(X_test)))
    joblib.dump(pr_model, MODELS_DIR / "priority_model.pkl")

    # risk_score regressor[file:1]
    y_risk = df["risk_score"]
    risk_model = Pipeline([
        ("pre", pre),
        ("reg", RandomForestRegressor(n_estimators=200, random_state=42)),
    ])
    risk_model.fit(X_train, y_risk.loc[X_train.index])
    y_risk_pred = risk_model.predict(X_test)
    print("Risk MAE:", mean_absolute_error(y_risk.loc[X_test.index], y_risk_pred))
    joblib.dump(risk_model, MODELS_DIR / "risk_model.pkl")

    # SLA breach classifier[file:1]
    sla_model = Pipeline([
        ("pre", pre),
        ("clf", RandomForestClassifier(
            n_estimators=50,
            max_depth=10,
            random_state=42,
            class_weight="balanced",
        )),
    ])
    sla_model.fit(X_train, y_sla_train)
    y_sla_proba = sla_model.predict_proba(X_test)[:, 1]
    print("SLA ROC-AUC:", roc_auc_score(y_sla_test, y_sla_proba))
    joblib.dump(sla_model, MODELS_DIR / "sla_model.pkl")

def load_autonomous_prioritization():
    pr = joblib.load(MODELS_DIR / "priority_model.pkl")
    risk = joblib.load(MODELS_DIR / "risk_model.pkl")
    sla = joblib.load(MODELS_DIR / "sla_model.pkl")
    return pr, risk, sla
