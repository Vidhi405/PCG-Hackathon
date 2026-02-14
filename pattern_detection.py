# pattern_detection.py
from core import load_data, TEXT_COL

def recurring_incidents(top_n: int = 10):
    df = load_data()
    desc = df[TEXT_COL].str.lower().fillna("")
    keys = ["password", "network", "vpn", "refund", "phishing", "latency", "error", "deployment"]
    counts = {k: int(desc.str.contains(k).sum()) for k in keys}
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)[:top_n]

def noisy_alert_sources(top_n: int = 5):
    df = load_data()
    return df["source"].value_counts().head(top_n).to_dict()  # source present[file:1]

def top_drivers():
    df = load_data()
    return {
        "by_group": df["assigned_group"].value_counts().to_dict(),
        "by_priority": df["priority"].value_counts().to_dict(),
    }
