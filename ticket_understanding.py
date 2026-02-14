# ticket_understanding.py
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from core import MODELS_DIR, TEXT_COL, ID_COL, load_data

def build_duplicate_index():
    df = load_data()
    texts = df[TEXT_COL].fillna("")
    vec = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), min_df=1)
    X = vec.fit_transform(texts)
    joblib.dump(
        {"vectorizer": vec, "matrix": X, "ticket_ids": df[ID_COL].tolist()},
        MODELS_DIR / "duplicate_index.pkl",
    )

def find_duplicates(description: str, top_k: int = 5, threshold: float = 0.85):
    idx = joblib.load(MODELS_DIR / "duplicate_index.pkl")
    vec = idx["vectorizer"]
    X = idx["matrix"]
    ticket_ids = idx["ticket_ids"]
    q = vec.transform([description])
    sims = cosine_similarity(q, X).ravel()
    order = np.argsort(sims)[::-1][:top_k]
    return [
        {"ticket_id": ticket_ids[i], "similarity": float(sims[i])}
        for i in order if sims[i] >= threshold
    ]

def summarize(text: str, max_len: int = 140) -> str:
    if len(text) <= max_len:
        return text
    return text[:max_len].rsplit(" ", 1)[0] + "..."

def extract_entities(text: str):
    text_low = text.lower()
    entities = []
    for kw in ["vpn", "firewall", "database", "load balancer", "refund", "phishing"]:
        if kw in text_low:
            entities.append({"type": "keyword", "value": kw})
    return entities

def detect_missing_info(text: str):
    text_low = text.lower()
    hints = []
    for kw in ["error code", "screenshot", "steps", "hostname"]:
        if kw not in text_low:
            hints.append(f"Consider adding {kw}.")
    return hints
