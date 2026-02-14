# proactive_insights.py
from core import load_data, TEXT_COL

def forecast_trend():
    df = load_data()
    # simple tickets per month (dd-mm-yyyy hh:mm)[file:1]
    df["month"] = df["created_date"].str[3:10]
    counts = df["month"].value_counts().sort_index().to_dict()
    return counts

def recommend_actions():
    return {
        "vpn": "Check VPN gateway status and authentication logs.",
        "firewall": "Review recent firewall rule changes and blocked traffic.",
        "refund": "Verify payment logs and billing entries before processing refund.",
    }

def suggest_kb_article(text: str):
    text_low = text.lower()
    if "password" in text_low:
        return "KB-001: Password reset and account lockout."
    if "vpn" in text_low:
        return "KB-002: VPN connection troubleshooting."
    if "refund" in text_low:
        return "KB-003: Billing disputes and refunds."
    if "phishing" in text_low:
        return "KB-004: Phishing email handling process."
    return "KB-000: General troubleshooting guide."
