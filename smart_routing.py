# smart_routing.py
import joblib
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

from core import MODELS_DIR, load_data, split_targets, build_preprocessor

def train_smart_routing():
    df = load_data()
    X_train, X_test, _, _, y_rt_train, y_rt_test, _, _ = split_targets(df)
    pre = build_preprocessor()

    model = Pipeline([
        ("pre", pre),
        ("clf", RandomForestClassifier(
            n_estimators=20,
            max_depth=10,
            random_state=42,
            class_weight="balanced",
        )),
    ])
    model.fit(X_train, y_rt_train)
    print("Routing:\n", classification_report(y_rt_test, model.predict(X_test)))
    joblib.dump(model, MODELS_DIR / "routing_model.pkl")

def load_smart_routing():
    return joblib.load(MODELS_DIR / "routing_model.pkl")

def explain_routing(description: str, group: str) -> str:
    return f"Assigned to {group} based on historical tickets with similar language and features."
